"""Check the built paper against the ACIIDS 2027 limits and count the placeholders left.

ACIIDS 2027 full papers: 12-15 pages INCLUDING figures, tables and references (pages beyond 15
may be charged). Reads the page count from main.log (pdflatex), so build first:

    pdflatex main && bibtex main && pdflatex main && pdflatex main
    python check_pages.py

Exit code 1 when the page count is outside 12-15 or when placeholders are left.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
MIN_PAGES, MAX_PAGES = 12, 15
PLACEHOLDERS = {"\\tbd": r"\\tbd\b", "\\prelim": r"\\prelim\{", "\\todo": r"\\todo\{"}


def page_count() -> int:
    log = (HERE / "main.log").read_text(encoding="latin-1")
    found = re.findall(r"Output written on main\.pdf \((\d+) pages?", log)
    if not found:
        raise SystemExit("no 'Output written' line in main.log: build the paper first")
    return int(found[-1])


def placeholders() -> dict[str, int]:
    """Occurrences in the .tex sources, comment lines and the macro definitions excluded."""
    counts = dict.fromkeys(PLACEHOLDERS, 0)
    for tex in [HERE / "main.tex", *sorted((HERE / "sections").glob("*.tex")), *sorted((HERE / "figures").glob("*.tex"))]:
        for line in tex.read_text(encoding="utf-8").splitlines():
            code = re.sub(r"(?<!\\)%.*", "", line)
            if "\\newcommand" in code:
                continue
            for name, pattern in PLACEHOLDERS.items():
                counts[name] += len(re.findall(pattern, code))
    return counts


def main() -> int:
    pages = page_count()
    ok = MIN_PAGES <= pages <= MAX_PAGES
    print(f"pages: {pages} ({'OK' if ok else f'outside {MIN_PAGES}-{MAX_PAGES}'}; references included)")
    left = placeholders()
    print("placeholders left: " + ", ".join(f"{k} {v}" for k, v in left.items()))
    return 0 if ok and not any(left.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
