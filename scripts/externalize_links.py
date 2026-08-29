#!/usr/bin/env python3
"""Sweep docs/ so every external hyperlink opens in a new browser tab.

Applies the same idempotent transform as the migration pipeline
(migrate_quickbytes.externalize_links): appends {target=_blank} to external
[text](http...) links, injects target=_blank into existing attr blocks, and
patches raw HTML anchors. Internal/relative links, mailto:, and fenced code
blocks are left untouched. Frontmatter is preserved byte-for-byte.

Usage: python3 scripts/externalize_links.py [docs]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_quickbytes import externalize_links  # noqa: E402


def split_frontmatter(text: str):
    if text.startswith("---"):
        m = re.match(r"^(---\s*\n.*?\n---\s*\n)", text, re.DOTALL)
        if m:
            return m.group(1), text[m.end():]
    return "", text


def main():
    docs = Path(sys.argv[1] if len(sys.argv) > 1 else
                Path(__file__).resolve().parent.parent / "docs")
    changed = 0
    for path in sorted(docs.rglob("*.md")):
        if "assets" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        new_body = externalize_links(body)
        if body.endswith("\n") and not new_body.endswith("\n"):
            new_body += "\n"  # splitlines/join must not eat the final newline
        if new_body != body:
            path.write_text(fm + new_body, encoding="utf-8")
            changed += 1
            print(f"  updated {path.relative_to(docs)}")
    print(f"{changed} file(s) updated.")


if __name__ == "__main__":
    main()
