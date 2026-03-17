from __future__ import annotations

import re
import shutil
from pathlib import Path

from extract_snippet import extract_symbol_source, SymbolType


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
OUTPUT_DIR = ROOT / "docs_generated"


BLOCK_RE = re.compile(
    r"::: py-symbol\s+"
    r"path:\s*(?P<path>.+?)\s+"
    r"symbol:\s*(?P<symbol>.+?)\s+"
    r"type:\s*(?P<type>function|class)\s*"
    r":::",
    re.DOTALL,
)


def replace_block(md_text: str) -> str:
    def _repl(match: re.Match) -> str:
        path_str = match.group("path").strip()
        symbol = match.group("symbol").strip()
        symbol_type_str = match.group("type").strip()
        symbol_type: SymbolType = symbol_type_str  # type: ignore[assignment]

        py_path = ROOT / path_str
        code = extract_symbol_source(py_path, symbol, symbol_type)

        return f"```python\n{code}\n```"

    return BLOCK_RE.sub(_repl, md_text)


def ensure_vitepress_config() -> None:
    """
    Copy docs/.vitepress/config.ts into docs_generated/.vitepress/config.ts.

    直接复制而非 re-export，避免 esbuild 处理跨目录 ESM 导入链时出现的
    "ESM file cannot be loaded by require" 错误。
    """
    vp_dir = OUTPUT_DIR / ".vitepress"
    vp_dir.mkdir(parents=True, exist_ok=True)
    src_config = DOCS_DIR / ".vitepress" / "config.ts"
    dst_config = vp_dir / "config.ts"
    shutil.copy2(src_config, dst_config)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for md_path in DOCS_DIR.rglob("*.md"):
        rel = md_path.relative_to(DOCS_DIR)
        out_path = OUTPUT_DIR / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        text = md_path.read_text(encoding="utf-8")
        new_text = replace_block(text)
        out_path.write_text(new_text, encoding="utf-8")
        print(f"processed {rel}")

    ensure_vitepress_config()
    print(f"All markdown files expanded into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

