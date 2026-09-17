"""在 collection.anki21 (updated/zhcn) 和 collection.anki21b (upstream) 中查找
おじいさん / どんどん 的笔记，看引用了哪些媒体文件，与 media 索引对比。
"""
from __future__ import annotations
import json, re, sqlite3, sys
from pathlib import Path
try:
    import zstandard as zstd
except ImportError:
    zstd = None

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"c:\Users\awa\Anki\Kaishi_15k_zh-CN_updated\_inspect")

SOUND_RE = re.compile(r"\[sound:([^\]]+)\]", re.IGNORECASE)
IMG_RE   = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def load_media(apkg_dir: Path) -> dict:
    raw = (apkg_dir / "media").read_bytes()
    if raw[:4] == b"\x28\xb5\x2f\xfd":
        raw = zstd.ZstdDecompressor().decompress(raw, max_output_size=64 * 1024 * 1024)
    return json.loads(raw.decode("utf-8"))


def open_db(apkg_dir: Path) -> sqlite3.Connection:
    """按存在顺序尝试 collection.anki21 / collection.anki21b / collection.anki2"""
    for name in ("collection.anki21", "collection.anki21b", "collection.anki2"):
        p = apkg_dir / name
        if p.exists() and p.stat().st_size > 100_000:
            return sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True)
    raise FileNotFoundError(f"{apkg_dir}: 没有可用的 collection")


def dump_note(label: str, apkg_dir: Path, keywords: list[str]) -> None:
    print(f"\n{'='*70}\n[{label}]\n{'='*70}")
    media = load_media(apkg_dir)
    names = set(media.values())
    print(f"  media 索引条目数: {len(media)}, 唯一文件名: {len(names)}")

    con = open_db(apkg_dir)
    cur = con.cursor()
    # 检查 notes 表结构
    cur.execute("PRAGMA table_info(notes)")
    cols = [c[1] for c in cur.fetchall()]
    print(f"  notes 表列: {cols}")
    cur.execute("SELECT COUNT(*) FROM notes")
    print(f"  notes 总行数: {cur.fetchone()[0]}")

    for kw in keywords:
        print(f"\n  === 关键词 {kw!r} ===")
        # 用 hex 编码的 UTF-8 字节 LIKE 匹配（避免 anki21b 里 flds 是 blob 的问题）
        kw_bytes = kw.encode("utf-8")
        try:
            cur.execute(
                "SELECT id, flds FROM notes WHERE flds LIKE ? ESCAPE '\\'",
                (f"%{kw}%",),
            )
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print(f"    LIKE 查询失败: {e}")
            rows = []

        if not rows:
            # 尝试 CAST 或直接扫描
            cur.execute("SELECT id, flds FROM notes")
            all_rows = cur.fetchall()
            rows = [r for r in all_rows if kw_bytes in (r[1] if isinstance(r[1], bytes) else r[1].encode("utf-8", "ignore"))]

        # 去重
        seen = {}
        for nid, flds in rows:
            seen[nid] = flds
        print(f"    命中 {len(seen)} 条笔记")

        for nid, flds in sorted(seen.items()):
            if isinstance(flds, bytes):
                try:
                    flds_str = flds.decode("utf-8", "replace")
                except Exception:
                    flds_str = repr(flds[:200])
            else:
                flds_str = flds

            # 只取前 2 个字段做标识
            head = flds_str.split("\x1f")[:2]
            print(f"\n    --- nid={nid} word={head[0]!r}")
            refs = []
            refs.extend(SOUND_RE.findall(flds_str))
            refs.extend(IMG_RE.findall(flds_str))
            seen_refs = []
            for r in refs:
                r = r.strip()
                if r and r not in seen_refs:
                    seen_refs.append(r)
            if not seen_refs:
                print("        (无媒体引用)")
            for r in seen_refs:
                mark = "OK" if r in names else "MISSING"
                print(f"        [{mark:7}] {r}")
    con.close()


for label in ("updated", "zhcn", "upstream"):
    try:
        dump_note(label, ROOT / label, ["おじいさん", "どんどん"])
    except Exception as e:
        print(f"\n[{label}] 失败: {type(e).__name__}: {e}")
