"""扫描 updated.apkg 里欢迎卡（id=1708637439853）的全部字段，找出版本号 / zh-CH 的所有出现位置。"""
import sqlite3, zipfile, tempfile, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated"
APKG = os.path.join(ROOT, "Kaishi_15k_zh-CN_updated.apkg")
WELCOME_ID = 1708637439853

with zipfile.ZipFile(APKG) as z:
    data = z.read("collection.anki21")
with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tf:
    tf.write(data); tmp = tf.name

con = sqlite3.connect(tmp); cur = con.cursor()
cur.execute("SELECT flds, sfld, csum, mod, usn, tags FROM notes WHERE id = ?", (WELCOME_ID,))
flds, sfld, csum, mod, usn, tags = cur.fetchone()
con.close(); os.unlink(tmp)

fields = flds.split("\x1f")
print(f"欢迎卡 id={WELCOME_ID}")
print(f"  sfld = {sfld!r}")
print(f"  csum = {csum}")
print(f"  mod  = {mod}")
print(f"  usn  = {usn}")
print(f"  tags = {tags!r}")
print(f"  字段数 = {len(fields)}")

# 搜版本号 / zh-CH 模式
PATTERNS = [
    (r"1\.[0-9]+\.[0-9]+(\.[0-9]+)?", "版本号 x.y.z[.w]"),
    (r"v?2\.[0-9]+\.[0-9]+",          "上游版本号 2.x.y"),
    (r"zh-CH",                          "zh-CH typo"),
    (r"zh-CN",                          "zh-CN 正确"),
    (r"版）",                           "「版）」结尾"),
    (r"version",                        "英文 version"),
]

print("\n=== 逐字段扫描 ===")
for i, f in enumerate(fields):
    hits = []
    for pat, label in PATTERNS:
        for m in re.finditer(pat, f, re.IGNORECASE):
            hits.append(f"{label}@{m.start()}: {m.group()!r}")
    if hits:
        print(f"\n  [{i:02d}] (len={len(f)})")
        for h in hits:
            print(f"      {h}")
        # 打印命中位置附近的上下文
        for pat, label in PATTERNS:
            for m in re.finditer(pat, f, re.IGNORECASE):
                s = max(0, m.start() - 30)
                e = min(len(f), m.end() + 30)
                print(f"      ctx[{label}]: ...{f[s:e]!r}...")
