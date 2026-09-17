"""
一次性修复 Kaishi_15k_zh-CN_updated.apkg 里缺失的两个媒体文件：
  - ojiisanS2.mp3 (来自 upstream zindex=1177, 41229 bytes)
  - tozan.png    (来自 upstream zindex=3362, 139185 bytes)

步骤：
  1) 校验 upstream/1177 与 upstream/3362 的 size + sha1 与 protobuf 索引一致
  2) 复制成 _inspect/updated/4354 与 _inspect/updated/4355
  3) 在 _inspect/updated/media JSON 里追加 {"4354":"ojiisanS2.mp3","4355":"tozan.png"}
  4) 重新 zip 打包为 Kaishi_15k_zh-CN_updated.apkg（保留原目录内所有其他文件）
  5) 重开新 apkg，用笔记里的实际引用做闭环校验
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import zipfile
from pathlib import Path

import zstandard as zstd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated")
INSPECT = ROOT / "_inspect"
UPDATED_DIR = INSPECT / "updated"
UPSTREAM_DIR = INSPECT / "upstream"
OUT_APKG = ROOT / "Kaishi_15k_zh-CN_updated.apkg"

# 从上游 protobuf 索引里已经解出来的两个新条目
# 注意：upstream 是 Anki 23.10+ 新格式，zip 里的编号文件是「单独 zstd 压缩」过的原始媒体；
# updated 是旧格式，媒体是明文存储。所以拷贝前必须先 zstd 解压。
NEW_ENTRIES = [
    # (upstream_zindex, 新 updated 编号, 文件名, 解压后 size, 解压后 sha1)
    (1177, 4354, "ojiisanS2.mp3", 41229,  "a5a61697f27cf45c638c4e49cbd34f3b58114758"),
    (3362, 4355, "tozan.png",     139185, "360b0fa3bcd125c848d108bac54d303f6fe03788"),
]


def sha1_bytes(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()


def zstd_decompress(raw: bytes) -> bytes:
    if raw[:4] != b"\x28\xb5\x2f\xfd":
        raise ValueError("源文件不是 zstd 压缩格式")
    with zstd.ZstdDecompressor().stream_reader(raw) as r:
        return r.read()


def step1_verify_upstream() -> None:
    print("[1/5] 从 upstream 拉取并 zstd 解压，校验 size + sha1 ...")
    for z_idx, _, name, size, sha in NEW_ENTRIES:
        src = UPSTREAM_DIR / str(z_idx)
        if not src.exists():
            raise FileNotFoundError(f"缺少 upstream 源文件: {src}")
        raw = src.read_bytes()
        dec = zstd_decompress(raw)
        actual_size = len(dec)
        actual_sha = sha1_bytes(dec)
        ok = (actual_size == size) and (actual_sha == sha)
        magic = dec[:8].hex()
        print(f"    zindex={z_idx:4}  {name}")
        print(f"      压缩前: {len(raw)} bytes  解压后: {actual_size} bytes (期望 {size})  head8={magic}")
        print(f"      sha1: {actual_sha}  {'✓' if ok else '✗'}")
        if not ok:
            raise RuntimeError(f"{name} 校验失败，中止")


def step2_copy_into_updated() -> None:
    print("\n[2/5] zstd 解压后写入 updated/ ...")
    for z_idx, new_num, name, _, _ in NEW_ENTRIES:
        src = UPSTREAM_DIR / str(z_idx)
        dst = UPDATED_DIR / str(new_num)
        if dst.exists():
            raise RuntimeError(f"目标已存在，中止以免覆盖: {dst}")
        dec = zstd_decompress(src.read_bytes())
        dst.write_bytes(dec)
        head = dec[:8].hex()
        print(f"    {src.name} --zstd-decompress--> {dst.name}  ({len(dec)} bytes, head8={head})  # {name}")


def step3_update_media_json() -> None:
    print("\n[3/5] 更新 updated/media JSON 索引 ...")
    media_path = UPDATED_DIR / "media"
    media = json.loads(media_path.read_text("utf-8"))
    before = len(media)
    for _, new_num, name, _, _ in NEW_ENTRIES:
        key = str(new_num)
        if key in media:
            raise RuntimeError(f"media JSON 中编号 {key} 已存在: {media[key]}")
        media[key] = name
    after = len(media)
    # 保持原格式：紧凑 JSON，无缩进（Anki 生成时就是紧凑的）
    media_path.write_text(json.dumps(media, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"    media 条目数: {before} -> {after}")
    for _, new_num, name, _, _ in NEW_ENTRIES:
        print(f"      + \"{new_num}\": \"{name}\"")


def step4_repack_apkg() -> None:
    print("\n[4/5] 重新打包 apkg ...")
    if OUT_APKG.exists():
        raise RuntimeError(f"输出文件已存在，中止: {OUT_APKG}")

    # 收集目录内所有文件；zip 内部路径使用相对路径，斜杠分隔
    entries = sorted(UPDATED_DIR.rglob("*"), key=lambda p: (str(p.parent), p.name))
    files = [p for p in entries if p.is_file()]
    print(f"    共 {len(files)} 个文件待打包")

    tmp_out = OUT_APKG.with_suffix(".apkg.tmp")
    # Anki apkg 用 deflate 压缩；media 索引和数据库都参与压缩
    with zipfile.ZipFile(tmp_out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for f in files:
            arcname = f.relative_to(UPDATED_DIR).as_posix()
            zf.write(f, arcname)
    tmp_out.replace(OUT_APKG)
    print(f"    写出: {OUT_APKG.name}  ({OUT_APKG.stat().st_size:,} bytes)")


def step5_verify_new_apkg() -> None:
    print("\n[5/5] 闭环校验新 apkg ...")
    tmp = INSPECT / "_verify"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(OUT_APKG) as zf:
        zf.extractall(tmp)

    media = json.loads((tmp / "media").read_text("utf-8"))
    names = set(media.values())
    print(f"    media 条目数: {len(media)}")

    # 从 collection.anki21 里查两条笔记的实际引用
    con = sqlite3.connect(f"file:{(tmp / 'collection.anki21').as_posix()}?mode=ro", uri=True)
    cur = con.cursor()
    sound_re = re.compile(r"\[sound:([^\]]+)\]", re.IGNORECASE)
    img_re = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)

    for kw in ("おじいさん", "どんどん"):
        cur.execute("SELECT id, flds FROM notes WHERE flds LIKE ?", (f"%{kw}%",))
        for nid, flds in cur.fetchall():
            word = flds.split("\x1f", 1)[0]
            refs = list(dict.fromkeys(sound_re.findall(flds) + img_re.findall(flds)))
            print(f"\n    nid={nid}  word={word!r}")
            for r in refs:
                mark = "OK" if r in names else "MISSING"
                num = next((k for k, v in media.items() if v == r), None)
                extra = f" -> media#{num}" if num else ""
                # 若是新增文件，再校验实体是否存在且大小合理
                if num:
                    p = tmp / num
                    exists = p.exists()
                    size = p.stat().st_size if exists else 0
                    extra += f"  (实体存在={exists}, size={size})"
                print(f"      [{mark:7}] {r}{extra}")
    con.close()

    shutil.rmtree(tmp)
    print("\n    清理临时目录完成")


def main() -> None:
    step1_verify_upstream()
    step2_copy_into_updated()
    step3_update_media_json()
    step4_repack_apkg()
    step5_verify_new_apkg()
    print("\n全部完成 ✅")


if __name__ == "__main__":
    main()
