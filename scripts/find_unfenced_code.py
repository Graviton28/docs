#!/usr/bin/env python3
"""Report code-like text that is not annotated as code (missing ``` or ` `).

Scans prose lines (outside fenced blocks, ignoring text already in backticks)
for shell commands, R/Python fragments, prompts, and function calls. This is a
review tool: it prints candidates with file:line so a human can decide what to
fence, backtick, or leave alone.

Usage: python3 scripts/find_unfenced_code.py [docs]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = [
    ("shell-cmd", re.compile(
        r"^\s*(?:\$ )?(?:module (?:load|avail|spider)|sbatch|srun|salloc|squeue|scancel|sacct|seff|sinfo"
        r"|conda (?:create|activate|install|env)|pip3? install|qsub|qstat|Rscript|spack"
        r"|ssh |scp |rsync |wget |curl |tar |chmod |mkdir |export [A-Z_]+=)")),
    ("prompt", re.compile(r"^\s*\$ \S")),
    ("sbatch-directive", re.compile(r"#SBATCH\b")),
    ("r-assign", re.compile(r"\s<-\s")),
    ("pipe-op", re.compile(r"%>%|\|>\s")),
    ("fn-call", re.compile(r"(?<![`\w.\[/])([A-Za-z_][\w.]*\((?:\{\})?\))(?![`\w])")),
    ("path-cmd", re.compile(r"^\s*(?:cd|ls|cp|mv|rm)\s+\S+/")),
]


def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def scan(path: Path):
    hits = []
    fence = None
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in ("```", "~~~"):
            fence = None if fence == marker else (marker if fence is None else fence)
            continue
        if fence:
            continue
        if stripped.startswith("    ") or line.startswith("    ") and not line.startswith("    -"):
            continue  # indented code block (already renders as code)
        bare = strip_inline_code(line)
        if "](" in bare:  # markdown links produce false fn-call-ish shapes
            bare = re.sub(r"\[[^\]]*\]\([^)]*\)(?:\{[^}]*\})?", "", bare)
        for name, rx in PATTERNS:
            m = rx.search(bare)
            if m:
                hits.append((i, name, line.strip()[:110]))
                break
    return hits


def main():
    docs = Path(sys.argv[1] if len(sys.argv) > 1 else
                Path(__file__).resolve().parent.parent / "docs")
    total = 0
    for path in sorted(docs.rglob("*.md")):
        if "assets" in path.parts:
            continue
        hits = scan(path)
        if hits:
            print(f"\n{path.relative_to(docs)}")
            for line_no, kind, text in hits:
                print(f"  {line_no:>4}  [{kind}]  {text}")
            total += len(hits)
    print(f"\n{total} candidate line(s).")


if __name__ == "__main__":
    main()
