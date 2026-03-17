from __future__ import annotations

import re
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
    Ensure docs_generated/.vitepress/config.ts exists and re-exports the real config.

    这样无论是本地还是 GitHub Actions，使用 docs_generated 作为根目录构建时，
    都会复用 docs/.vitepress/config.ts 中的所有站点配置。
    """
    vp_dir = OUTPUT_DIR / ".vitepress"
    vp_dir.mkdir(parents=True, exist_ok=True)
    config_path = vp_dir / "config.ts"
    content = "import config from '../../../docs/.vitepress/config'\n\nexport default config\n"
    config_path.write_text(content, encoding="utf-8")


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

