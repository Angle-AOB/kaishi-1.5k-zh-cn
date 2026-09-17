"""验证 updated/ 里的媒体文件是明文存储还是 zstd 压缩。"""
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding="utf-8")

UPD = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect\updated")
ZSTD_MAGIC = bytes.fromhex("28b52ffd")

# 采样几个：0, 1, 2673 (ojiisanS.mp3), 1688 (speed_slow_turtle*.webp), 4353
for num in ("0", "1", "2", "1688", "2673", "4353"):
    p = UPD / num
    if not p.exists():
        print(f"updated/{num}: (不存在)")
        continue
    b = p.read_bytes()
    tag = []
    if b[:4] == ZSTD_MAGIC: tag.append("zstd")
    if b[:4] == b"RIFF":    tag.append("RIFF/webp")
    if b[:8] == bytes.fromhex("89504e470d0a1a0a"): tag.append("PNG")
    if b[:3] == b"ID3":     tag.append("ID3/mp3")
    if b[:2] == b"\xff\xfb" or b[:2] == b"\xff\xf3": tag.append("mp3-frame")
    if b[:4] == b"OggS":    tag.append("Ogg")
    print(f"updated/{num}: size={len(b):7}  head8={b[:8].hex()}  识别={tag or ['未知']}")
