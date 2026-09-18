"""在 upstream / zhcn(old) / updated / bkp 四个来源里搜索特定 note，看它们分别存在于哪里。"""
import sqlite3, zipfile, tempfile, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated"
APKGS = [
    ("upstream v2.4.3",  os.path.join(ROOT, "Kaishi.1.5k.v2.4.3.apkg")),
    ("zhcn old v1.4.0",  os.path.join(ROOT, "Kaishi_15k_zh-CN.apkg")),
    ("updated v1.5.0",   os.path.join(ROOT, "Kaishi_15k_zh-CN_updated.apkg")),
    # bkp 用 anki 库导入
]

TARGETS = ["だから", "連れて来る", "連れてくる", "欢迎来到 Kaishi"]


def read_from_sqlite_apkg(p):
    with zipfile.ZipFile(p) as z:
        for dbname in ["collection.anki21", "collection.anki2"]:
            try:
                data = z.read(dbname)
            except KeyError:
                continue
            with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tf:
                tf.write(data); tmp = tf.name
            con = sqlite3.connect(tmp); cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM notes")
            total = cur.fetchone()[0]
            results = {"total": total, "dbname": dbname, "matches": {}}
            for kw in TARGETS:
                cur.execute("SELECT id, guid, mid, sfld, substr(flds, 1, 100) FROM notes WHERE flds LIKE ?", (f"%{kw}%",))
                rows = cur.fetchall()
                if rows:
                    results["matches"][kw] = rows
            con.close(); os.unlink(tmp)
            return results
    return None


for tag, p in APKGS:
    print(f"\n=== {tag}: {os.path.basename(p)} ===")
    r = read_from_sqlite_apkg(p)
    if r is None:
        print("  (无 SQLite DB)")
        continue
    print(f"  [{r['dbname']}] notes total = {r['total']}")
    for kw, rows in r["matches"].items():
        print(f"    \"{kw}\": {len(rows)} 条")
        for row in rows[:5]:
            _id, guid, mid, sfld, flds_head = row
            print(f"      id={_id}  guid={guid!r}  sfld={sfld!r}")
            print(f"        flds[0:100]={flds_head!r}")

# 用 anki 库读 bkp
print("\n=== bkp (用户从 Anki 导出的) ===")
from anki.collection import Collection
from anki.import_export_pb2 import (
    ImportAnkiPackageOptions, ImportAnkiPackageRequest,
    ImportAnkiPackageUpdateCondition as UC,
)
tmp = tempfile.mkdtemp(prefix="anki_bkp_")
col_path = os.path.join(tmp, "collection.anki2")
col = Collection(col_path)
opts = ImportAnkiPackageOptions(
    update_notes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
    update_notetypes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
    with_scheduling=False, with_deck_configs=False,
)
req = ImportAnkiPackageRequest(package_path=os.path.join(ROOT, "Kaishi_15k_zh-CN.bkp.apkg"), options=opts)
col.import_anki_package(req)
print(f"  notes total = {col.note_count()}")
for kw in TARGETS:
    nids = col.find_notes(col.build_search_string(kw))
    if nids:
        print(f"    \"{kw}\": {len(nids)} 条")
        for nid in nids[:5]:
            n = col.get_note(nid)
            print(f"      id={n.id}  guid={n.guid!r}  fields[0]={n.fields[0]!r}")
col.close()
import shutil
shutil.rmtree(tmp, ignore_errors=True)
