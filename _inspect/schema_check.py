"""检查 collection.anki2 / anki21b 的表结构，找到能读到 flds 明文的方式。"""
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")

for label in ("updated", "zhcn", "upstream"):
    print(f"\n{'='*70}\n[{label}]\n{'='*70}")
    for dbname in ("collection.anki2", "collection.anki21b"):
        db = ROOT / label / dbname
        if not db.exists():
            print(f"  {dbname}: (不存在)")
            continue
        print(f"\n  --- {dbname} ---")
        con = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
        cur = con.cursor()
        cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        print(f"  tables: {[t[0] for t in tables]}")
        # 检查 notes 表
        for tname, tsql in tables:
            if tname == "notes":
                print(f"  notes schema: {tsql}")
                cur.execute("PRAGMA table_info(notes)")
                cols = cur.fetchall()
                print(f"  notes columns: {[(c[1], c[2]) for c in cols]}")
                cur.execute("SELECT COUNT(*) FROM notes")
                print(f"  notes row count: {cur.fetchone()[0]}")
                # 取第一条看 flds 类型
                cur.execute("SELECT id, typeof(flds), length(flds), substr(flds, 1, 80) FROM notes LIMIT 1")
                row = cur.fetchone()
                if row:
                    print(f"  first row: id={row[0]}, typeof(flds)={row[1]}, len={row[2]}, head={row[3]!r}")
        con.close()
