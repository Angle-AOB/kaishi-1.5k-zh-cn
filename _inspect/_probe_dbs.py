"""快速探测：两个 apkg 里的每个 SQLite DB 分别是什么内容。"""
import sqlite3, zipfile, tempfile, os, sys
sys.stdout.reconfigure(encoding="utf-8")

APKGS = [
    ("updated", r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\Kaishi_15k_zh-CN_updated.apkg"),
    ("bkp",     r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\Kaishi_15k_zh-CN.bkp.apkg"),
]

for tag, p in APKGS:
    print(f"\n=== {tag}: {p}")
    with zipfile.ZipFile(p) as z:
        for dbname in ["collection.anki2", "collection.anki21"]:
            try:
                data = z.read(dbname)
            except KeyError:
                print(f"  {dbname}: 不存在")
                continue
            with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tf:
                tf.write(data)
                tmpname = tf.name
            con = sqlite3.connect(tmpname)
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cur.fetchall()]
            print(f"  {dbname} (size={len(data)}): tables={tables}")
            if "notes" in tables:
                cur.execute("SELECT COUNT(*) FROM notes")
                print(f"    notes count = {cur.fetchone()[0]}")
            if "cards" in tables:
                cur.execute("SELECT COUNT(*) FROM cards")
                print(f"    cards count = {cur.fetchone()[0]}")
            if "col" in tables:
                cur.execute("SELECT COUNT(*) FROM col")
                print(f"    col rows = {cur.fetchone()[0]}")
                cur.execute("SELECT crt, mod, scm, ver FROM col")
                print(f"    col (crt, mod, scm, ver) = {cur.fetchone()}")
            con.close()
            os.unlink(tmpname)
