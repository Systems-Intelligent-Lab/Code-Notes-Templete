from __future__ import annotations

import ast
from pathlib import Path
from typing import Literal


SymbolType = Literal["function", "class"]


def extract_symbol_source(py_path: Path, symbol: str, symbol_type: SymbolType) -> str:
    """Extract the source code of a top-level function or class by name."""
    source = py_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    lines = source.splitlines()

    target_node: ast.AST | None = None
    for node in tree.body:
        if symbol_type == "function" and isinstance(node, ast.FunctionDef) and node.name == symbol:
            target_node = node
            break
        if symbol_type == "class" and isinstance(node, ast.ClassDef) and node.name == symbol:
            target_node = node
            break

    if target_node is None:
        raise ValueError(f"Symbol {symbol!r} ({symbol_type}) not found in {py_path}")

    # Python 3.8+ provides end_lineno on AST nodes
    if not hasattr(target_node, "end_lineno"):
        raise RuntimeError("Python version is too old: AST nodes lack end_lineno")

    start = target_node.lineno - 1  # convert to 0-based index
    end = target_node.end_lineno  # inclusive in terms of 1-based line numbers

    snippet_lines = lines[start:end]
    return "\n".join(snippet_lines)


__all__ = ["extract_symbol_source", "SymbolType"]

