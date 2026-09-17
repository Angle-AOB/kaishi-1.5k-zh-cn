"""
诊断：为什么更新后的 apkg 在 Anki 里播放不出新音频、显示不出新图片。

对每个 apkg：
1) 解开 media 索引（可能是明文 JSON，也可能是 zstd 压缩的 JSON）
2) 打开 collection.anki21b（SQLite），取出 flds 中含「おじいさん」或「どんどん」的笔记
3) 从笔记 HTML 中抽出所有 [sound:...] 和 <img src="..."> 引用
4) 检查每个引用是否存在于 media 索引里
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

try:
    import zstandard as zstd
except ImportError:
    zstd = None

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")
APKGS = {
    "updated":  ROOT / "updated",
    "zhcn":     ROOT / "zhcn",
    "upstream": ROOT / "upstream",
}

TARGETS = ["おじいさん", "どんどん"]

SOUND_RE = re.compile(r"\[sound:([^\]]+)\]", re.IGNORECASE)
IMG_RE   = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def load_media_index(apkg_dir: Path) -> dict:
    """media 文件可能是明文 JSON，也可能是 zstd 压缩 JSON。返回 {编号 -> 文件名}。"""
    p = apkg_dir / "media"
    raw = p.read_bytes()
    # zstd magic: 28 B5 2F FD
    if raw[:4] == b"\x28\xb5\x2f\xfd":
        if zstd is None:
            raise RuntimeError("需要 zstandard 库来解压 upstream 的 media")
        raw = zstd.ZstdDecompressor().decompress(raw, max_output_size=64 * 1024 * 1024)
    return json.loads(raw.decode("utf-8"))


def query_notes(apkg_dir: Path, keywords: list[str]) -> list[tuple[int, str]]:
    """优先从 collection.anki21b 读；否则回退到 collection.anki2。返回 [(nid, flds), ...]"""
    for dbname in ("collection.anki21b", "collection.anki2"):
        db = apkg_dir / dbname
        if not db.exists():
            continue
        try:
            con = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
            cur = con.cursor()
            # notes 表：id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data
            rows: list[tuple[int, str]] = []
            for kw in keywords:
                # 用 LIKE 匹配 flds（用 \x1f 分隔的字段串）
                cur.execute(
                    "SELECT id, flds FROM notes WHERE flds LIKE ? ESCAPE '\\'",
                    (f"%{kw}%",),
                )
                rows.extend(cur.fetchall())
            con.close()
            if rows:
                return rows
        except sqlite3.Error as e:
            print(f"  ! {dbname} 读取失败: {e}", file=sys.stderr)
    return []


def extract_refs(flds: str) -> list[str]:
    """从字段串里抽出所有媒体引用。"""
    refs = []
    refs.extend(SOUND_RE.findall(flds))
    refs.extend(IMG_RE.findall(flds))
    # 去重保序
    seen = set()
    out = []
    for r in refs:
        r = r.strip()
        if r and r not in seen:
            seen.add(r)
            out.append(r)
    return out


def main() -> None:
    # 让 Windows 控制台按 UTF-8 输出
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    for label, apkg_dir in APKGS.items():
        print(f"\n{'='*70}")
        print(f"[{label}] {apkg_dir}")
        print(f"{'='*70}")

        try:
            media = load_media_index(apkg_dir)
        except Exception as e:
            print(f"  ! media 解析失败: {e}")
            continue

        # 建立 "文件名 -> 编号" 反查表
        name_to_ids: dict[str, list[str]] = {}
        for num, name in media.items():
            name_to_ids.setdefault(name, []).append(num)
        print(f"  media 条目数: {len(media)}")

        notes = query_notes(apkg_dir, TARGETS)
        # 按 id 去重
        uniq = {}
        for nid, flds in notes:
            uniq[nid] = flds
        print(f"  命中笔记数: {len(uniq)}")

        for nid, flds in sorted(uniq.items()):
            # 只显示前 3 个字段（一般是 Word / Word Meaning / Word Furigana）
            head_fields = flds.split("\x1f")[:3]
            print(f"\n  --- nid={nid}  word={head_fields[0]!r}")
            refs = extract_refs(flds)
            if not refs:
                print(f"      (无媒体引用)")
                continue
            for r in refs:
                present = r in name_to_ids
                mark = "OK" if present else "MISSING"
                extra = f" -> media#{','.join(name_to_ids[r])}" if present else ""
                print(f"      [{mark:7}] {r}{extra}")


if __name__ == "__main__":
    main()
