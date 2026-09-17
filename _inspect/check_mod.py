"""
调查：
  1) 「いいえ」「さあ」「どんどん」「おじいさん」四条笔记的 mod 时间戳
  2) 全库 mod 分布：有多少个不同的 mod 值，各自多少条
  3) 上一次 v1.4.0 修改过的 109 条笔记，mod 是不是同一个值
  4) collection 表的 mod（全局时间戳）
"""
from __future__ import annotations
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")

def fmt_ts(sec: int) -> str:
    if sec <= 0:
        return f"{sec} (<=0)"
    try:
        return datetime.fromtimestamp(sec, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return str(sec)

for label in ("updated", "zhcn", "upstream"):
    print(f"\n{'='*70}\n[{label}]\n{'='*70}")
    # 选正确的 db 文件
    db = None
    for name in ("collection.anki21", "collection.anki21b"):
        p = ROOT / label / name
        if p.exists() and p.stat().st_size > 100_000:
            db = p
            break
    if db is None:
        print("  找不到主 db")
        continue
    print(f"  db: {db.name}")

    con = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    cur = con.cursor()

    # collection mod
    try:
        cur.execute("SELECT id, crt, mod, scm, ver FROM col")
        row = cur.fetchone()
        if row:
            col_id, crt, mod, scm, ver = row
            print(f"  col.id={col_id}")
            print(f"  col.crt (创建时间) = {crt} = {fmt_ts(crt)}")
            print(f"  col.mod (修改时间) = {mod} = {fmt_ts(mod // 1000 if mod > 10**11 else mod)}")
            print(f"  col.scm (schema 时间) = {scm} = {fmt_ts(scm // 1000 if scm > 10**11 else scm)}")
            print(f"  col.ver = {ver}")
    except sqlite3.Error as e:
        print(f"  col 查询失败: {e}")

    # notes mod 分布
    cur.execute("SELECT mod FROM notes")
    mods = [r[0] for r in cur.fetchall()]
    print(f"\n  notes 总数: {len(mods)}")
    cnt = Counter(mods)
    print(f"  唯一 mod 值数量: {len(cnt)}")
    print(f"  top 8 mod 值:")
    for m, c in cnt.most_common(8):
        print(f"    mod={m} ({fmt_ts(m)})  出现 {c} 次")

    # 目标四条
    print(f"\n  目标笔记：")
    for kw in ("いいえ", "さあ", "どんどん", "おじいさん"):
        cur.execute("SELECT id, guid, mod, usn, tags, substr(flds,1,60) FROM notes WHERE flds LIKE ? LIMIT 3", (f"%{kw}%",))
        for r in cur.fetchall():
            nid, guid, mod, usn, tags, head = r
            word = head.split("\x1f", 1)[0]
            # 只保留完全匹配的
            if word != kw:
                continue
            print(f"    {kw!r}: nid={nid}  guid={guid}  mod={mod} ({fmt_ts(mod)})  usn={usn}")
            break

    con.close()
