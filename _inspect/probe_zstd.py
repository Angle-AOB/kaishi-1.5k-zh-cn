"""验证：upstream 里的编号文件是不是每个都单独用 zstd 压缩过。"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path
import zstandard as zstd

sys.stdout.reconfigure(encoding="utf-8")

UP = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect\upstream")

# 索引里的目标（前面 diff_media.py 解出来的）
EXPECT = {
    "0":    ("pose_inoru_woman.webp", 13284, "b6bfadc70ff4fca5d787d6846d276902f435c9ec"),
    "1177": ("ojiisanS2.mp3",         41229, "a5a61697f27cf45c638c4e49cbd34f3b58114758"),
    "3362": ("tozan.png",            139185, "360b0fa3bcd125c848d108bac54d303f6fe03788"),
}

for num, (name, exp_size, exp_sha) in EXPECT.items():
    p = UP / num
    raw = p.read_bytes()
    print(f"\n--- upstream/{num}  (期望解压后 = {name}, size={exp_size}, sha1={exp_sha[:16]}..) ---")
    print(f"  实体大小: {len(raw)}")
    print(f"  头 4 字节 hex: {raw[:4].hex()}  (zstd magic = 28b52ffd)")
    if raw[:4] == b"\x28\xb5\x2f\xfd":
        try:
            with zstd.ZstdDecompressor().stream_reader(raw) as r:
                dec = r.read()
            sha = hashlib.sha1(dec).hexdigest()
            print(f"  ✓ zstd 解压后: size={len(dec)}, sha1={sha}")
            print(f"    size 匹配: {len(dec) == exp_size}")
            print(f"    sha1 匹配: {sha == exp_sha}")
            # 看解压后头几个字节，判断文件类型
            print(f"    解压后头 8 字节: {dec[:8].hex()}  (mp3=49443303 或 fffb.., png=89504e47, webp=52494646)")
        except Exception as e:
            print(f"  ✗ zstd 解压失败: {e}")
    else:
        # 尝试直接匹配
        sha = hashlib.sha1(raw).hexdigest()
        print(f"  非 zstd，直接 sha1={sha}, 匹配={sha == exp_sha}")
