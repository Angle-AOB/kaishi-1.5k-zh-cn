"""检查 だから 笔记在 bkp 里属于哪个 deck，以及 updated.apkg 的 deck 名。"""
import os, sys, tempfile, shutil, sqlite3, zipfile, json
sys.stdout.reconfigure(encoding="utf-8")

from anki.collection import Collection
from anki.import_export_pb2 import (
    ImportAnkiPackageOptions, ImportAnkiPackageRequest,
    ImportAnkiPackageUpdateCondition as UC,
)

ROOT = r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated"

# --- updated.apkg 的 deck / notetype 名 ---
print("=== updated.apkg (SQLite) ===")
with zipfile.ZipFile(os.path.join(ROOT, "Kaishi_15k_zh-CN_updated.apkg")) as z:
    data = z.read("collection.anki21")
with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tf:
    tf.write(data); tmp = tf.name
con = sqlite3.connect(tmp); cur = con.cursor()
cur.execute("SELECT decks, models FROM col")
decks_s, models_s = cur.fetchone()
decks = json.loads(decks_s); models = json.loads(models_s)
print(f"  decks: {[(d['id'], d['name']) for d in decks.values()]}")
print(f"  models: {[(m['id'], m['name']) for m in models.values()]}")
# 数一下每个 deck 里的 card 数
cur.execute("SELECT did, COUNT(*) FROM cards GROUP BY did")
for did, cnt in cur.fetchall():
    dname = next((d["name"] for d in decks.values() if d["id"] == did), f"?{did}")
    print(f"  cards in deck {did} ({dname}): {cnt}")
con.close(); os.unlink(tmp)

# --- bkp.apkg: だから 的 deck 归属 ---
print("\n=== bkp.apkg (Anki import) ===")
tmp2 = tempfile.mkdtemp(prefix="anki_bkp2_")
col = Collection(os.path.join(tmp2, "collection.anki2"))
opts = ImportAnkiPackageOptions(
    update_notes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
    update_notetypes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
    with_scheduling=False, with_deck_configs=False,
)
req = ImportAnkiPackageRequest(package_path=os.path.join(ROOT, "Kaishi_15k_zh-CN.bkp.apkg"), options=opts)
col.import_anki_package(req)

print(f"  decks: {[(d.id, d.name) for d in col.decks.all_names_and_ids()]}")
print(f"  notetypes: {[(nt.id, nt.name) for nt in col.models.all_names_and_ids()]}")

# 找到 だか ら 那条 note
DAKARA_ID = 1777310248185
try:
    n = col.get_note(DAKARA_ID)
    print(f"\n  だから note (id={DAKARA_ID}):")
    print(f"    guid    = {n.guid!r}")
    print(f"    mid     = {n.mid}")
    print(f"    tags    = {list(n.tags)}")
    print(f"    fields  = {n.fields}")
    # 找到它对应的 card
    cids = n.card_ids()
    print(f"    card_ids = {cids}")
    for cid in cids:
        c = col.get_card(cid)
        print(f"      card did={c.did}  deck_name={col.decks.name(c.did)!r}  type={c.type}  queue={c.queue}")
except Exception as e:
    print(f"  找不到 だから note: {e!r}")

# 数一下每个 deck 里的 card 数
print("\n  cards per deck:")
for d in col.decks.all_names_and_ids():
    cnt = col.db.scalar("SELECT COUNT(*) FROM cards WHERE did = ?", d.id)
    print(f"    {d.id} ({d.name!r}): {cnt}")

col.close()
shutil.rmtree(tmp2, ignore_errors=True)
