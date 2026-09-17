"""upstream/media 前 4 字节是 zstd magic，但解压后不是 UTF-8 JSON。
Anki 23.10+ 改用 protobuf 编码 media 索引。这里尝试两种路径：
  (a) 直接看解压后前若干字节
  (b) 用 protobuf 结构解析（如果 a 显示是 protobuf）
"""
from __future__ import annotations
import sys
from pathlib import Path
import zstandard as zstd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")
raw = (ROOT / "upstream" / "media").read_bytes()
print(f"raw size: {len(raw)}, magic: {raw[:4].hex()}")

dctx = zstd.ZstdDecompressor()
# 流式解压（避免 max_output_size 限制）
with dctx.stream_reader(raw) as reader:
    data = reader.read()
print(f"decompressed size: {len(data)}")
print(f"head 64 bytes hex: {data[:64].hex()}")
print(f"head 200 bytes (latin-1): {data[:200].decode('latin-1', 'replace')!r}")
