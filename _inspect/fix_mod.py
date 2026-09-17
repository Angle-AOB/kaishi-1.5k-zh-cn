"""
v1.4.2 修复：提升 どんどん / おじいさん 两条笔记的 mod 时间戳，
让 Anki 下次导入时不再因 "mod 相等" 而跳过，从而触发媒体写入 collection.media。

步骤：
  1) 打开 _inspect/updated/collection.anki21（读写）
  2) UPDATE notes SET mod=<now_sec> WHERE id IN (1758347125968, 1758347125257)
  3) UPDATE col   SET mod=<now_ms>
  4) COMMIT
  5) 删除旧的 Kaishi_15k_zh-CN_updated.apkg，重新 zip 打包
  6) 重开新 apkg 验证：
       - 这两条笔记的 mod 已 > 1789610375
       - media 索引仍含 ojiisanS2.mp3 / tozan.png
       - 实体文件 4354 / 4355 仍存在且大小正确
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sqlite3
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated")
INSPECT = ROOT / "_inspect"
UPDATED_DIR = INSPECT / "updated"
DB_PATH = UPDATED_DIR / "collection.anki21"
OUT_APKG = ROOT / "Kaishi_15k_zh-CN_updated.apkg"

TARGET_NIDS = {
    1758347125968: "どんどん",
    1758347125257: "おじいさん",
}
OLD_MOD = 1789610375  # v1.4.0 / v1.4.1 里 109 条笔记共用的 mod


def fmt_ts(sec: int) -> str:
    return datetime.fromtimestamp(sec, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def step1_bump_mod() -> int:
    print("[1/4] 提升目标笔记 mod ...")
    now_sec = int(time.time())
    now_ms = now_sec * 1000
    print(f"    当前时间戳: {now_sec} ({fmt_ts(now_sec)})")
    print(f"    旧 mod:     {OLD_MOD} ({fmt_ts(OLD_MOD)})")
    assert now_sec > OLD_MOD, "当前时间戳必须大于旧 mod，否则 Anki 仍会跳过"

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # 修改前快照
    cur.execute("SELECT id, mod FROM notes WHERE id IN (?, ?)", tuple(TARGET_NIDS.keys()))
    before = {r[0]: r[1] for r in cur.fetchall()}
    for nid, word in TARGET_NIDS.items():
        print(f"    修改前 {word} (nid={nid}): mod={before.get(nid)} ({fmt_ts(before.get(nid, 0))})")

    # 执行 UPDATE
    cur.executemany(
        "UPDATE notes SET mod = ? WHERE id = ?",
        [(now_sec, nid) for nid in TARGET_NIDS.keys()],
    )
    affected = cur.rowcount
    print(f"    UPDATE notes 影响行数: {affected}")

    # 更新 col.mod（毫秒）
    cur.execute("SELECT mod FROM col")
    old_col_mod = cur.fetchone()[0]
    cur.execute("UPDATE col SET mod = ?", (now_ms,))
    print(f"    col.mod: {old_col_mod} -> {now_ms}")

    con.commit()

    # 修改后快照
    cur.execute("SELECT id, mod FROM notes WHERE id IN (?, ?)", tuple(TARGET_NIDS.keys()))
    after = {r[0]: r[1] for r in cur.fetchall()}
    for nid, word in TARGET_NIDS.items():
        print(f"    修改后 {word} (nid={nid}): mod={after.get(nid)} ({fmt_ts(after.get(nid, 0))})")
    con.close()
    return now_sec


def step2_repack() -> None:
    print("\n[2/4] 重新打包 apkg ...")
    if OUT_APKG.exists():
        old_size = OUT_APKG.stat().st_size
        OUT_APKG.unlink()
        print(f"    删除旧 apkg ({old_size:,} bytes)")

    files = sorted(p for p in UPDATED_DIR.rglob("*") if p.is_file())
    print(f"    共 {len(files)} 个文件待打包")

    tmp_out = OUT_APKG.with_suffix(".apkg.tmp")
    with zipfile.ZipFile(tmp_out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for f in files:
            zf.write(f, f.relative_to(UPDATED_DIR).as_posix())
    tmp_out.replace(OUT_APKG)
    print(f"    写出: {OUT_APKG.name}  ({OUT_APKG.stat().st_size:,} bytes)")


def step3_verify() -> None:
    print("\n[3/4] 闭环校验新 apkg ...")
    tmp = INSPECT / "_verify2"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(OUT_APKG) as zf:
        zf.extractall(tmp)

    # 3a) 数据库里两条笔记的 mod
    con = sqlite3.connect(f"file:{(tmp / 'collection.anki21').as_posix()}?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute("SELECT id, mod, flds FROM notes WHERE id IN (?, ?)", tuple(TARGET_NIDS.keys()))
    sound_re = re.compile(r"\[sound:([^\]]+)\]", re.IGNORECASE)
    img_re = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
    for nid, mod, flds in cur.fetchall():
        word = TARGET_NIDS[nid]
        bumped = mod > OLD_MOD
        print(f"    {word} (nid={nid}): mod={mod} ({fmt_ts(mod)})  {'✓ 已提升' if bumped else '✗ 未提升'}")
        refs = list(dict.fromkeys(sound_re.findall(flds) + img_re.findall(flds)))
        print(f"      引用: {refs}")
    con.close()

    # 3b) media 索引仍含两个新文件
    media = json.loads((tmp / "media").read_text("utf-8"))
    names = set(media.values())
    for target in ("ojiisanS2.mp3", "tozan.png"):
        ok = target in names
        num = next((k for k, v in media.items() if v == target), None)
        print(f"    media 索引含 {target}: {'✓' if ok else '✗'}  (编号 {num})")
        if num:
            p = tmp / num
            exists = p.exists()
            size = p.stat().st_size if exists else 0
            sha = hashlib.sha1(p.read_bytes()).hexdigest() if exists else ""
            print(f"      实体: 存在={exists}  size={size}  sha1={sha[:16]}..")

    shutil.rmtree(tmp)
    print("    清理临时目录完成")


def step4_summary(now_sec: int) -> None:
    print("\n[4/4] 总结")
    print(f"    新 mod 时间戳: {now_sec} ({fmt_ts(now_sec)})")
    print(f"    旧 mod 时间戳: {OLD_MOD} ({fmt_ts(OLD_MOD)})")
    print(f"    差值: {now_sec - OLD_MOD} 秒")
    print(f"    下次导入时 Anki 会看到 mod 变大 → 更新这 2 条笔记 → 写入媒体")


def main() -> None:
    now_sec = step1_bump_mod()
    step2_repack()
    step3_verify()
    step4_summary(now_sec)
    print("\n全部完成 ✅")


if __name__ == "__main__":
    main()
