"""
修复 Kaishi_15k_zh-CN_updated.apkg 的两个数据质量问题：

问题 A: 2 条笔记 sfld/csum 陈旧
  - id=1708637439853 (欢迎卡): sfld 说 1.3.0, flds[0] 说 1.4.0
  - id=1758347126305 (連れて来る): sfld 说 連れてくる, flds[0] 说 連れて来る

问题 B: 欢迎卡版本号 + zh-CH typo
  - flds[0]: '欢迎来到 Kaishi 1.5k zh-CH！（1.4.0 版）'
         -> '欢迎来到 Kaishi 1.5k zh-CN！（1.3.0.1 版）'

策略：
  - 欢迎卡: 改 flds -> 重算 sfld/csum -> 更新 mod (让 Anki 重导入时识别为更新)
  - 連れて来る: 只重算 sfld/csum, mod 不动 (flds 没变, 避免假"已更新"信号)
  - 重打包: 原 apkg 备份成 .old, 新 apkg 覆盖原名, 其他 entry 原样复制
"""
from __future__ import annotations

import hashlib
import os
import shutil
import sqlite3
import sys
import tempfile
import time
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated")
APKG = ROOT / "Kaishi_15k_zh-CN_updated.apkg"
BACKUP = ROOT / "Kaishi_15k_zh-CN_updated.apkg.old"

WELCOME_ID = 1708637439853
TSURETE_ID = 1758347126305

OLD_WELCOME_F0 = "欢迎来到 Kaishi 1.5k zh-CH！（1.4.0 版）"
NEW_WELCOME_F0 = "欢迎来到 Kaishi 1.5k zh-CN！（1.3.0.1 版）"


def csum_of(first_field: str) -> int:
    """Anki csum = int(sha1(first_field)[:8], 16)"""
    return int(hashlib.sha1(first_field.encode("utf-8")).hexdigest()[:8], 16)


def fix_db(db_path: Path) -> dict:
    """打开 SQLite, 修复 2 条笔记, 返回修改详情。"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    report = {}

    # --- 欢迎卡 ---
    cur.execute("SELECT flds, sfld, csum, mod FROM notes WHERE id = ?", (WELCOME_ID,))
    flds, sfld_old, csum_old, mod_old = cur.fetchone()
    fields = flds.split("\x1f")
    assert fields[0] == OLD_WELCOME_F0, f"欢迎卡 flds[0] 不匹配预期: {fields[0]!r}"
    fields[0] = NEW_WELCOME_F0
    new_flds = "\x1f".join(fields)
    new_sfld = NEW_WELCOME_F0
    new_csum = csum_of(new_sfld)
    new_mod = int(time.time())  # 秒级时间戳, 和 Anki 一致
    cur.execute(
        "UPDATE notes SET flds = ?, sfld = ?, csum = ?, mod = ? WHERE id = ?",
        (new_flds, new_sfld, new_csum, new_mod, WELCOME_ID),
    )
    report["welcome"] = {
        "id": WELCOME_ID,
        "flds[0]": (OLD_WELCOME_F0, NEW_WELCOME_F0),
        "sfld": (sfld_old, new_sfld),
        "csum": (csum_old, new_csum),
        "mod": (mod_old, new_mod),
    }

    # --- 連れて来る ---
    cur.execute("SELECT flds, sfld, csum, mod FROM notes WHERE id = ?", (TSURETE_ID,))
    flds, sfld_old, csum_old, mod_old = cur.fetchone()
    fields = flds.split("\x1f")
    new_sfld = fields[0]  # '連れて来る'
    new_csum = csum_of(new_sfld)
    # mod 不动
    cur.execute(
        "UPDATE notes SET sfld = ?, csum = ? WHERE id = ?",
        (new_sfld, new_csum, TSURETE_ID),
    )
    report["tsurete"] = {
        "id": TSURETE_ID,
        "sfld": (sfld_old, new_sfld),
        "csum": (csum_old, new_csum),
        "mod": (mod_old, mod_old),  # 不变
    }

    con.commit()

    # 验证: 全表扫一遍, 确保没有其他 sfld != flds[0]
    cur.execute("SELECT id, sfld, flds FROM notes")
    stale = []
    for _id, s, f in cur.fetchall():
        if s != f.split("\x1f", 1)[0]:
            stale.append(_id)
    report["remaining_stale"] = stale

    con.close()
    return report


def repack_apkg(orig: Path, fixed_db: Path, out: Path) -> None:
    """把 orig 里所有 entry 复制到 out, 但 collection.anki21 用 fixed_db 替换。
    保留每个 entry 的压缩方式。"""
    with zipfile.ZipFile(orig, "r") as zin, \
         zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "collection.anki21":
                # 用修复后的 DB
                data = fixed_db.read_bytes()
                # 保留原 entry 的元数据 (date_time, compress_type 等)
                new_info = zipfile.ZipInfo(item.filename, date_time=item.date_time)
                new_info.compress_type = item.compress_type
                new_info.external_attr = item.external_attr
                zout.writestr(new_info, data)
            else:
                # 原样复制 (保留压缩)
                data = zin.read(item.filename)
                new_info = zipfile.ZipInfo(item.filename, date_time=item.date_time)
                new_info.compress_type = item.compress_type
                new_info.external_attr = item.external_attr
                zout.writestr(new_info, data)


def verify_apkg(apkg: Path) -> None:
    """重打包后验证: notes 数, 2 条目标笔记的 sfld/csum/flds[0], media 数。"""
    print(f"\n=== 验证 {apkg.name} ===")
    with zipfile.ZipFile(apkg) as z:
        names = z.namelist()
        media_count = sum(1 for n in names if n.isdigit())
        print(f"  zip entries: {len(names)} (media: {media_count})")
        db_data = z.read("collection.anki21")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tf:
        tf.write(db_data); tmp = tf.name
    con = sqlite3.connect(tmp); cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM notes")
    print(f"  notes total: {cur.fetchone()[0]}")

    for nid, label in [(WELCOME_ID, "欢迎卡"), (TSURETE_ID, "連れて来る")]:
        cur.execute("SELECT flds, sfld, csum, mod FROM notes WHERE id = ?", (nid,))
        flds, sfld, csum, mod = cur.fetchone()
        f0 = flds.split("\x1f", 1)[0]
        ok_sfld = "OK" if sfld == f0 else "MISMATCH"
        ok_csum = "OK" if csum == csum_of(f0) else "MISMATCH"
        print(f"  [{label}] id={nid}")
        print(f"    flds[0] = {f0!r}")
        print(f"    sfld    = {sfld!r}  [{ok_sfld}]")
        print(f"    csum    = {csum}  [{ok_csum}]")
        print(f"    mod     = {mod}")

    # 全表 stale 检查
    cur.execute("SELECT id, sfld, flds FROM notes")
    stale = [r[0] for r in cur.fetchall() if r[1] != r[2].split("\x1f", 1)[0]]
    print(f"  全表 stale sfld 数: {len(stale)} {stale if stale else ''}")
    con.close(); os.unlink(tmp)


def main() -> None:
    print(f"原 apkg: {APKG}  ({APKG.stat().st_size} bytes)")

    # 1. 备份原文件
    if BACKUP.exists():
        print(f"  ! 备份 {BACKUP.name} 已存在, 先删除旧备份")
        BACKUP.unlink()
    shutil.copy2(APKG, BACKUP)
    print(f"  已备份 -> {BACKUP.name}  ({BACKUP.stat().st_size} bytes)")

    # 2. 提取 collection.anki21 到临时文件并修复
    with tempfile.TemporaryDirectory(prefix="fix_apkg_") as td:
        td = Path(td)
        db_path = td / "collection.anki21"
        with zipfile.ZipFile(APKG) as z:
            db_path.write_bytes(z.read("collection.anki21"))
        print(f"\n  提取 collection.anki21 ({db_path.stat().st_size} bytes)")

        report = fix_db(db_path)
        print("\n=== 修复详情 ===")
        for k, v in report.items():
            if k == "remaining_stale":
                print(f"  剩余 stale sfld: {v}")
                continue
            print(f"  [{k}] id={v['id']}")
            for fk, val in v.items():
                if fk == "id":
                    continue
                old, new = val
                print(f"    {fk}: {old!r} -> {new!r}")

        # 3. 重打包到临时文件, 再覆盖原文件
        tmp_apkg = td / "fixed.apkg"
        repack_apkg(APKG, db_path, tmp_apkg)
        print(f"\n  重打包完成 ({tmp_apkg.stat().st_size} bytes)")

        # 覆盖原文件
        shutil.move(str(tmp_apkg), str(APKG))
        print(f"  已覆盖 {APKG.name}  ({APKG.stat().st_size} bytes)")

    # 4. 验证
    verify_apkg(APKG)


if __name__ == "__main__":
    main()
