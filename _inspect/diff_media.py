"""完整对比 updated 与 upstream 的媒体清单，找出：
   1) 上游存在但 updated 缺失的媒体文件
   2) 上游和 updated 都存在但内容可能不同的媒体文件（用 SHA1 判断）

upstream/media 是 zstd 压缩的 protobuf；updated/media 是明文 JSON（{编号 -> 文件名}）。
protobuf 结构（Anki 23.10+）：
    message MediaEntry { string name = 1; uint32 size = 2; bytes sha1 = 3; }
    message Media      { repeated MediaEntry entries = 1; }   // 位置即 zindex
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
import zstandard as zstd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")


def _read_varint(buf: bytes, i: int) -> tuple[int, int]:
    result = 0
    shift = 0
    while True:
        b = buf[i]
        i += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, i
        shift += 7


def parse_media_protobuf(buf: bytes) -> list[dict]:
    """返回 [{zindex, name, size, sha1_hex}, ...]"""
    entries: list[dict] = []
    i = 0
    while i < len(buf):
        tag, i = _read_varint(buf, i)
        field, wire = tag >> 3, tag & 7
        if field == 1 and wire == 2:
            length, i = _read_varint(buf, i)
            entry_bytes = buf[i:i + length]
            i += length
            # 解析 MediaEntry
            j = 0
            name, size, sha1 = None, None, None
            while j < len(entry_bytes):
                t2, j = _read_varint(entry_bytes, j)
                f2, w2 = t2 >> 3, t2 & 7
                if f2 == 1 and w2 == 2:
                    l2, j = _read_varint(entry_bytes, j)
                    name = entry_bytes[j:j + l2].decode("utf-8")
                    j += l2
                elif f2 == 2 and w2 == 0:
                    size, j = _read_varint(entry_bytes, j)
                elif f2 == 3 and w2 == 2:
                    l2, j = _read_varint(entry_bytes, j)
                    sha1 = entry_bytes[j:j + l2].hex()
                    j += l2
                else:
                    # 跳过未知字段
                    if w2 == 0:
                        _, j = _read_varint(entry_bytes, j)
                    elif w2 == 2:
                        l2, j = _read_varint(entry_bytes, j)
                        j += l2
                    elif w2 == 1:
                        j += 8
                    elif w2 == 5:
                        j += 4
                    else:
                        raise ValueError(f"未知 wire type {w2}")
            entries.append({"zindex": len(entries), "name": name, "size": size, "sha1": sha1})
        else:
            raise ValueError(f"顶层未知字段 field={field} wire={wire}")
    return entries


# 1) upstream 媒体清单
raw = (ROOT / "upstream" / "media").read_bytes()
with zstd.ZstdDecompressor().stream_reader(raw) as r:
    data = r.read()
upstream_entries = parse_media_protobuf(data)
upstream_by_name: dict[str, dict] = {}
for e in upstream_entries:
    upstream_by_name.setdefault(e["name"], e)  # 保留首个（同名极少见）

# 2) updated 媒体清单（JSON: {"编号": "文件名"}）
updated_json = json.loads((ROOT / "updated" / "media").read_text("utf-8"))
updated_by_name: dict[str, str] = {}
for num, name in updated_json.items():
    updated_by_name.setdefault(name, num)

# 3) 计算 SHA1（updated 里的实体文件）
def sha1_of_updated(num: str) -> str:
    p = ROOT / "updated" / num
    return hashlib.sha1(p.read_bytes()).hexdigest()


print(f"upstream 条目数: {len(upstream_entries)}, 唯一文件名: {len(upstream_by_name)}")
print(f"updated  条目数: {len(updated_json)}, 唯一文件名: {len(updated_by_name)}")

# 4) 差集
missing_in_updated = sorted(set(upstream_by_name) - set(updated_by_name))
missing_in_upstream = sorted(set(updated_by_name) - set(upstream_by_name))
common = sorted(set(upstream_by_name) & set(updated_by_name))

print(f"\n[A] 上游有但 updated 缺失的文件: {len(missing_in_updated)}")
for n in missing_in_updated:
    e = upstream_by_name[n]
    print(f"    - {n}  (upstream zindex={e['zindex']}, size={e['size']})")

print(f"\n[B] updated 有但上游没有的文件: {len(missing_in_upstream)}")
for n in missing_in_upstream[:40]:
    print(f"    - {n}")
if len(missing_in_upstream) > 40:
    print(f"    ... 及 {len(missing_in_upstream)-40} 个")

# 5) 同名但 SHA1 不同（内容被替换）
print(f"\n[C] 同名文件 SHA1 对比（正在扫描 {len(common)} 个共同文件）...")
diff_sha = []
for name in common:
    up_sha = upstream_by_name[name]["sha1"]
    ud_num = updated_by_name[name]
    ud_sha = sha1_of_updated(ud_num)
    if up_sha and ud_sha and up_sha != ud_sha:
        diff_sha.append((name, ud_num, up_sha, ud_sha, upstream_by_name[name]))

print(f"    内容不同的同名文件: {len(diff_sha)}")
for name, ud_num, up_sha, ud_sha, e in diff_sha:
    print(f"    - {name}  updated#{ud_num} sha1={ud_sha[:12]}.. vs upstream#{e['zindex']} sha1={up_sha[:12]}..")

# 6) 关注的两个特定文件
print("\n[D] 特别关注：")
for target in ("ojiisanS2.mp3", "ojiisanS.mp3", "tozan.png", "speed_slow_turtle-788a833aeefbca2d4d02cd8dec150b5ee5c1fb47.webp"):
    up = upstream_by_name.get(target)
    ud = updated_by_name.get(target)
    print(f"    {target}:")
    print(f"        upstream: {up}")
    print(f"        updated : {'media#' + ud if ud else None}")
