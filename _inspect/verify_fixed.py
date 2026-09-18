"""端到端验证：用 Anki 库导入修复后的 apkg，确认欢迎卡正文、notes 数、无 zh-CH/1.4.0 残留。"""
import os, sys, tempfile, shutil
sys.stdout.reconfigure(encoding="utf-8")
from anki.collection import Collection
from anki.import_export_pb2 import (
    ImportAnkiPackageOptions, ImportAnkiPackageRequest,
    ImportAnkiPackageUpdateCondition as UC,
)

apkg = r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\Kaishi_15k_zh-CN_updated.apkg"
tmp = tempfile.mkdtemp(prefix="anki_verify_")
col = Collection(os.path.join(tmp, "collection.anki2"))
opts = ImportAnkiPackageOptions(
    update_notes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
    update_notetypes=UC.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_ALWAYS,
    with_scheduling=False, with_deck_configs=False,
)
log = col.import_anki_package(ImportAnkiPackageRequest(package_path=apkg, options=opts))
print(f"notes total = {col.note_count()}")
print(f"cards total = {col.card_count()}")
print(f"decks       = {[(d.id, d.name) for d in col.decks.all_names_and_ids()]}")
kaishi_nt = [(nt.id, nt.name) for nt in col.models.all_names_and_ids() if "Kaishi" in nt.name]
print(f"notetypes   = {kaishi_nt}")

# 欢迎卡
n = col.get_note(1708637439853)
print(f"\n欢迎卡 id={n.id}")
print(f"  fields[0] = {n.fields[0]!r}")

# 連れて来る
n2 = col.get_note(1758347126305)
print(f"\n連れて来る id={n2.id}")
print(f"  fields[0] = {n2.fields[0]!r}")

# 搜 zh-CH / 1.4.0 确认全库无残留
for kw in ["zh-CH", "1.4.0"]:
    hits = col.find_notes(col.build_search_string(kw))
    print(f'\n全库搜 "{kw}": {len(hits)} 条 (应为 0)')
    for nid in hits[:3]:
        nn = col.get_note(nid)
        print(f"    id={nid} fields[0]={nn.fields[0]!r}")

col.close()
shutil.rmtree(tmp, ignore_errors=True)
print("\n=== 验证完成 ===")
