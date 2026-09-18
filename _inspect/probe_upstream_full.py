"""把 upstream v2.4.3 也用 anki 库导入临时 collection，看 だから 是否存在。"""
import os, sys, tempfile, shutil
sys.stdout.reconfigure(encoding="utf-8")

from anki.collection import Collection
from anki.import_export_pb2 import (
    ImportAnkiPackageOptions, ImportAnkiPackageRequest,
    ImportAnkiPackageUpdateCondition as UC,
)

ROOT = r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated"
APKGS = [
    ("upstream v2.4.3", os.path.join(ROOT, "Kaishi.1.5k.v2.4.3.apkg")),
]

TARGETS = ["だから", "連れて来る", "連れてくる", "Kaishi"]

for tag, p in APKGS:
    print(f"\n=== {tag}: {os.path.basename(p)} ===")
    tmp = tempfile.mkdtemp(prefix="anki_probe_")
    col = Collection(os.path.join(tmp, "collection.anki2"))
    opts = ImportAnkiPackageOptions(
        update_notes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
        update_notetypes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
        with_scheduling=False, with_deck_configs=False,
    )
    req = ImportAnkiPackageRequest(package_path=p, options=opts)
    col.import_anki_package(req)
    print(f"  notes total = {col.note_count()}")
    print(f"  notetypes   = {[(nt.id, nt.name) for nt in col.models.all_names_and_ids()]}")
    print(f"  decks       = {[(d.id, d.name) for d in col.decks.all_names_and_ids()]}")
    for kw in TARGETS:
        try:
            nids = col.find_notes(col.build_search_string(kw))
        except Exception as e:
            print(f"    \"{kw}\": search error {e!r}")
            continue
        if nids:
            print(f"    \"{kw}\": {len(nids)} 条")
            for nid in nids[:5]:
                n = col.get_note(nid)
                print(f"      id={n.id}  guid={n.guid!r}  fields[0]={n.fields[0]!r}")
    col.close()
    shutil.rmtree(tmp, ignore_errors=True)
