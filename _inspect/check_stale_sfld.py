"""扫描 updated.apkg 里所有 sfld 与 flds[0] 不一致的笔记（stale sfld）。"""
import sqlite3, zipfile, tempfile, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated"
APKG = os.path.join(ROOT, "Kaishi_15k_zh-CN_updated.apkg")

with zipfile.ZipFile(APKG) as z:
    data = z.read("collection.anki21")
with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tf:
    tf.write(data); tmp = tf.name

con = sqlite3.connect(tmp); cur = con.cursor()
cur.execute("SELECT id, guid, sfld, flds FROM notes")
mismatch = []
for _id, guid, sfld, flds in cur.fetchall():
    first = flds.split("\x1f", 1)[0]
    if sfld != first:
        mismatch.append((_id, guid, sfld, first))

print(f"updated.apkg 中 sfld != flds[0] 的笔记数: {len(mismatch)}")
for _id, guid, sfld, first in mismatch[:20]:
    print(f"  id={_id}  guid={guid!r}")
    print(f"    sfld    = {sfld!r}")
    print(f"    flds[0] = {first!r}")

con.close(); os.unlink(tmp)
