"""
调查 upstream apkg 的媒体存储机制：
  - protobuf 索引里的 list_pos 是否对应 zip 里的数字文件名？
  - 如果不对应，那实体文件到底怎么找？
  - ojiisanS2.mp3 / tozan.png 的实体在 upstream 里到底有没有？
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
import zstandard as zstd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")
UP = ROOT / "upstream"

def _read_varint(buf, i):
    r = 0; s = 0
    while True:
        b = buf[i]; i += 1
        r |= (b & 0x7F) << s
        if not (b & 0x80):
            return r, i
        s += 7

raw = (UP / "media").read_bytes()
with zstd.ZstdDecompressor().stream_reader(raw) as r:
    data = r.read()

entries = []
i = 0
while i < len(data):
    tag, i = _read_varint(data, i)
    f, w = tag >> 3, tag & 7
    if f == 1 and w == 2:
        ln, i = _read_varint(data, i)
        eb = data[i:i+ln]; i += ln
        j = 0
        rec = {}
        while j < len(eb):
            t2, j = _read_varint(eb, j)
            f2, w2 = t2 >> 3, t2 & 7
            if w2 == 2:
                l2, j = _read_varint(eb, j)
                val = eb[j:j+l2]; j += l2
                if f2 == 1: rec["name"] = val.decode("utf-8","replace")
                elif f2 == 3: rec["sha1"] = val.hex()
            elif w2 == 0:
                v, j = _read_varint(eb, j)
                if f2 == 2: rec["size"] = v
        entries.append(rec)

# 建立 sha1 -> entry 反查表
sha_to_entry = {e["sha1"]: e for e in entries if e.get("sha1")}

# 遍历 zip 里所有数字文件，计算 sha1，看反查得到什么名字
print("扫描 upstream/ 里的所有数字文件，通过 sha1 反查 protobuf 索引里的名字：\n")

# 先看几个采样点：0, 1, 2, 1177, 3362, 4353
sample_nums = [0, 1, 2, 3, 1177, 1178, 3361, 3362, 3363, 4353]
for n in sample_nums:
    p = UP / str(n)
    if not p.exists():
        print(f"  upstream/{n}: (不存在)")
        continue
    b = p.read_bytes()
    sha = hashlib.sha1(b).hexdigest()
    entry = sha_to_entry.get(sha)
    if entry:
        print(f"  upstream/{n}: size={len(b):7}  sha1={sha[:12]}..  -> name={entry['name']!r}  (list_pos={[i for i,e in enumerate(entries) if e is entry][0]})")
    else:
        print(f"  upstream/{n}: size={len(b):7}  sha1={sha[:12]}..  -> 索引里找不到匹配")

# 全量扫描：把 zip 里所有 sha1 收集起来
print("\n全量扫描 upstream 里所有数字文件的 sha1 ...")
zip_shas: dict[str, str] = {}   # sha -> zip 里的编号
for p in UP.iterdir():
    if p.is_file() and p.name.isdigit():
        sha = hashlib.sha1(p.read_bytes()).hexdigest()
        zip_shas.setdefault(sha, p.name)

print(f"  zip 里数字文件数: {sum(1 for p in UP.iterdir() if p.is_file() and p.name.isdigit())}")
print(f"  zip 里唯一 sha1 数: {len(zip_shas)}")
print(f"  索引声明的唯一 sha1 数: {len(sha_to_entry)}")

# 索引里声明但 zip 里没有的
missing_files = []
for e in entries:
    if e.get("sha1") and e["sha1"] not in zip_shas:
        missing_files.append(e)
print(f"\n索引里声明但 zip 里实体缺失的文件: {len(missing_files)}")
for e in missing_files[:20]:
    print(f"  - {e['name']!r}  size={e.get('size')}  sha1={e.get('sha1','')[:16]}..")
if len(missing_files) > 20:
    print(f"  ... 及 {len(missing_files)-20} 个")

# zip 里有但索引里没声明的（孤立文件）
index_shas = set(sha_to_entry.keys())
orphan = [n for s, n in zip_shas.items() if s not in index_shas]
print(f"\nzip 里有但索引里没声明的孤立文件数: {len(orphan)}")
for n in orphan[:10]:
    p = UP / n
    sha = hashlib.sha1(p.read_bytes()).hexdigest()
    print(f"  - upstream/{n}  size={p.stat().st_size}  sha1={sha[:16]}..")
