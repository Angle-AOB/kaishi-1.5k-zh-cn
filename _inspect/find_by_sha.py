"""
用 SHA1 反查 upstream 里 ojiisanS2.mp3 和 tozan.png 的真实编号。
顺便重新解析 protobuf，把 field 4 (zindex) 也读出来，看清 schema。
"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path
import zstandard as zstd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")

TARGETS = {
    "a5a61697f27cf45c638c4e49cbd34f3b58114758": "ojiisanS2.mp3",
    "360b0fa3bcd125c848d108bac54d303f6fe03788": "tozan.png",
}

# --- 1) 扫描所有 upstream 数字文件，用 sha1 反查
print("[1] 扫描 upstream/ 下所有编号文件（4354 个），用 sha1 匹配 ...")
found: dict[str, tuple[str, int]] = {}
for p in (ROOT / "upstream").iterdir():
    if not p.is_file() or not p.name.isdigit():
        continue
    data = p.read_bytes()
    sha = hashlib.sha1(data).hexdigest()
    if sha in TARGETS:
        found[sha] = (p.name, len(data))
        print(f"    ✓ 命中 {TARGETS[sha]:22} -> upstream/{p.name}  size={len(data)}  sha1={sha}")

for sha, name in TARGETS.items():
    if sha not in found:
        print(f"    ✗ 未找到 {name} (sha1={sha})")

# --- 2) 重新解析 protobuf，看 field 4 是否存在
print("\n[2] 重新解析 protobuf media，dump 每个字段 ...")

def _read_varint(buf, i):
    r = 0; s = 0
    while True:
        b = buf[i]; i += 1
        r |= (b & 0x7F) << s
        if not (b & 0x80):
            return r, i
        s += 7

raw = (ROOT / "upstream" / "media").read_bytes()
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
        # parse MediaEntry
        j = 0
        rec = {"list_pos": len(entries)}
        while j < len(eb):
            t2, j = _read_varint(eb, j)
            f2, w2 = t2 >> 3, t2 & 7
            if w2 == 2:
                l2, j = _read_varint(eb, j)
                val = eb[j:j+l2]; j += l2
                if f2 == 1:
                    rec["name"] = val.decode("utf-8", "replace")
                elif f2 == 3:
                    rec["sha1"] = val.hex()
                else:
                    rec[f"field{f2}_bytes"] = val.hex()
            elif w2 == 0:
                v, j = _read_varint(eb, j)
                if f2 == 2:
                    rec["size"] = v
                else:
                    rec[f"field{f2}_varint"] = v
            else:
                raise ValueError(f"未处理 wire type {w2}")
        entries.append(rec)
    else:
        raise ValueError(f"顶层 field={f} wire={w}")

print(f"    共 {len(entries)} 条 entry")
# 打印前 3 条和两条目标
print("\n    前 3 条：")
for e in entries[:3]:
    print(f"      {e}")

target_names = {"ojiisanS2.mp3", "tozan.png", "pose_inoru_woman.webp"}
print("\n    目标条目：")
for e in entries:
    if e.get("name") in target_names:
        print(f"      {e}")

# --- 3) 检查所有字段名，看有没有 zindex 字段
print("\n[3] 全部字段名统计：")
keys = set()
for e in entries:
    keys.update(e.keys())
print(f"    {sorted(keys)}")
