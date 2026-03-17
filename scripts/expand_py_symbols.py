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


def clean_output_dir() -> None:
    if not OUTPUT_DIR.exists():
        return
    for p in sorted(OUTPUT_DIR.rglob("*"), reverse=True):
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            p.rmdir()


def main() -> None:
    clean_output_dir()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for md_path in DOCS_DIR.rglob("*.md"):
        rel = md_path.relative_to(DOCS_DIR)
        out_path = OUTPUT_DIR / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        text = md_path.read_text(encoding="utf-8")
        new_text = replace_block(text)
        out_path.write_text(new_text, encoding="utf-8")
        print(f"processed {rel}")

    print(f"All markdown files expanded into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

