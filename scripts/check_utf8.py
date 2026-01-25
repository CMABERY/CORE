#!/usr/bin/env python3
"""check_utf8.py

Fail if tracked text-like files cannot be decoded as UTF-8.

This is a lightweight guardrail against accidental encoding drift.
"""
from __future__ import annotations

import sys
from pathlib import Path

TEXT_EXTS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".js", ".ts", ".css", ".html", ".csv"
}

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}

def is_text_like(p: Path) -> bool:
    if p.suffix in TEXT_EXTS:
        return True
    # files with no suffix but likely text
    if p.name in {"LICENSE", "CODEOWNERS", ".gitignore", ".gitattributes", ".editorconfig"}:
        return True
    return False

def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    bad: list[str] = []
    for p in repo.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if not is_text_like(p):
            continue
        try:
            p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            bad.append(str(p.relative_to(repo)))
    if bad:
        print("FAIL: non-UTF-8 files detected:", file=sys.stderr)
        for b in bad:
            print(" -", b, file=sys.stderr)
        return 1
    print("OK: UTF-8 check passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
