"""
定位"多出来的那一张卡片"。

updated.apkg: 我们发布的 v1.5.0（内部 collection.anki21 = SQLite）
bkp.apkg    : 用户导入 updated 后从 Anki 导出的（内部 collection.anki21b = zstd+protobuf）

方案：
- updated.apkg  → 直接 sqlite3 读 collection.anki21
- bkp.apkg      → 建一个临时 Collection，用 import_anki_package 导入，再遍历 notes
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated")
UPDATED = ROOT / "Kaishi_15k_zh-CN_updated.apkg"
BKP     = ROOT / "Kaishi_15k_zh-CN.bkp.apkg"


def load_updated_notes(apkg: Path) -> list[dict]:
    """从 updated.apkg 的 collection.anki21 (SQLite) 读所有 notes。"""
    with zipfile.ZipFile(apkg) as z:
        data = z.read("collection.anki21")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".anki21") as tf:
        tf.write(data)
        tmp = tf.name
    con = sqlite3.connect(tmp)
    cur = con.cursor()
    cur.execute("SELECT id, guid, mid, mod, usn, tags, flds, sfld, csum FROM notes")
    rows = []
    for r in cur.fetchall():
        _id, guid, mid, mod, usn, tags, flds, sfld, csum = r
        rows.append({
            "id": _id, "guid": guid, "mid": mid, "mod": mod, "usn": usn,
            "tags": tags, "flds": flds, "sfld": sfld, "csum": csum,
            "fields": flds.split("\x1f"),
        })
    con.close()
    os.unlink(tmp)
    return rows


def load_bkp_notes_via_import(apkg: Path) -> tuple[list[dict], dict]:
    """建临时 Collection，把 bkp.apkg 导入进去，再遍历 notes。"""
    from anki.collection import Collection
    from anki.import_export_pb2 import (
        ImportAnkiPackageOptions,
        ImportAnkiPackageRequest,
        ImportAnkiPackageUpdateCondition as UC,
    )

    tmp = tempfile.mkdtemp(prefix="anki_bkp_")
    col_path = os.path.join(tmp, "collection.anki2")
    col = Collection(col_path)

    opts = ImportAnkiPackageOptions(
        update_notes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
        update_notetypes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
        with_scheduling=False,
        with_deck_configs=False,
    )
    req = ImportAnkiPackageRequest(package_path=str(apkg), options=opts)
    log = col.import_anki_package(req)

    notes = []
    for nid in col.find_notes(""):
        n = col.get_note(nid)
        notes.append({
            "id": n.id,
            "guid": n.guid,
            "mid": n.mid,
            "mod": n.mod,
            "usn": n.usn,
            "tags": list(n.tags),
            "flds": "\x1f".join(n.fields),
            "sfld": n.fields[0] if n.fields else "",
            "csum": n.csum if hasattr(n, "csum") else None,
            "fields": list(n.fields),
        })

    # 顺便记一下 deck/notetype 信息
    info = {
        "decks": [(d.id, d.name) for d in col.decks.all_names_and_ids()],
        "notetypes": [(nt.id, nt.name) for nt in col.models.all_names_and_ids()],
        "cards": col.card_count(),
        "notes": col.note_count(),
        "log_new": len(log.new if hasattr(log, "new") else []),
        "log_updated": len(log.updated if hasattr(log, "updated") else []),
        "log_duplicate": len(log.duplicate if hasattr(log, "duplicate") else []),
        "log_conflicting": len(log.conflicting if hasattr(log, "conflicting") else []),
        "log_first_field": len(log.first_field if hasattr(log, "first_field") else []),
        "log_missing_media": len(log.missing_media if hasattr(log, "missing_media") else []),
        "log_": None,
    }
    # 保留完整 log 对象以便 dump
    info["_log"] = log
    col.close()
    shutil.rmtree(tmp, ignore_errors=True)
    return notes, info


def csum_of(s: str) -> int:
    """Anki 的 csum = int(sha1(first_field)[:8], 16)"""
    import hashlib
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest()[:8], 16)


def fmt_short(s: str, n: int = 120) -> str:
    s = s.replace("\n", "\\n")
    return s if len(s) <= n else s[:n] + "..."


def main() -> None:
    print("=" * 70)
    print("[updated.apkg] collection.anki21 (SQLite)")
    print("=" * 70)
    upd_notes = load_updated_notes(UPDATED)
    print(f"  notes: {len(upd_notes)}")

    print("\n" + "=" * 70)
    print("[bkp.apkg] 用 anki.Collection.import_anki_package 读入")
    print("=" * 70)
    bkp_notes, bkp_info = load_bkp_notes_via_import(BKP)
    print(f"  notes: {len(bkp_notes)}")
    print(f"  cards: {bkp_info['cards']}")
    print(f"  notetypes: {bkp_info['notetypes']}")
    print(f"  decks: {bkp_info['decks']}")
    print(f"  import log:")
    print(f"    new         = {bkp_info['log_new']}")
    print(f"    updated     = {bkp_info['log_updated']}")
    print(f"    duplicate   = {bkp_info['log_duplicate']}")
    print(f"    conflicting = {bkp_info['log_conflicting']}")
    print(f"    first_field = {bkp_info['log_first_field']}")
    print(f"    missing_media = {bkp_info['log_missing_media']}")

    # 建索引 (mid, csum) -> note
    upd_idx = {}
    for n in upd_notes:
        key = (n["mid"], n["csum"])
        upd_idx.setdefault(key, []).append(n)

    bkp_idx = {}
    for n in bkp_notes:
        # 有些 n["csum"] 可能是 None，则从 sfld 计算
        csum = n["csum"] if n["csum"] is not None else csum_of(n["sfld"])
        key = (n["mid"], csum)
        bkp_idx.setdefault(key, []).append(n)

    print("\n" + "=" * 70)
    print("[diff] 用 (mid, csum) 做键")
    print("=" * 70)
    only_bkp_keys = set(bkp_idx.keys()) - set(upd_idx.keys())
    only_upd_keys = set(upd_idx.keys()) - set(bkp_idx.keys())
    print(f"  only in bkp    : {len(only_bkp_keys)}")
    print(f"  only in updated: {len(only_upd_keys)}")

    for key in only_bkp_keys:
        for n in bkp_idx[key]:
            print(f"\n  ★ 多出来的笔记 (仅存在于 bkp) ★")
            print(f"    id       = {n['id']}")
            print(f"    guid     = {n['guid']}")
            print(f"    mid      = {n['mid']}")
            print(f"    csum     = {n['csum']}")
            print(f"    tags     = {n['tags']}")
            print(f"    字段数   = {len(n['fields'])}")
            for i, f in enumerate(n["fields"]):
                print(f"      [{i:02d}] {fmt_short(f)!r}")

    for key in only_upd_keys:
        for n in upd_idx[key]:
            print(f"\n  ☆ 只在 updated 中 (bkp 里缺失) ☆")
            print(f"    id   = {n['id']}  guid={n['guid']}  sfld={n['sfld']!r}")
            print(f"    fields[0..3] = {[fmt_short(x, 80) for x in n['fields'][:4]]}")


if __name__ == "__main__":
    main()
