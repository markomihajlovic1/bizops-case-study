"""Check the results page: every repo link points at a file that exists, and list every number for a manual check.

Usage: python scripts/check_html.py [docs/index.html]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
page = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "index.html"
html = page.read_text(encoding="utf-8")

bad = 0
print("Links:")
for href in sorted(set(re.findall(r'href="([^"]+)"', html))):
    m = re.search(r"github\.com/[^/]+/[^/]+/(?:blob|tree)/[^/]+/(.+)", href)
    if m:
        ok = (ROOT / m.group(1)).exists()
    elif href.startswith(("http", "mailto:", "#")):
        print(f"  EXTERNAL  {href}")
        continue
    else:
        ok = (page.parent / href).resolve().exists()
    bad += not ok
    print(f"  {'OK     ' if ok else 'MISSING'}  {href}")

text = re.sub(r"<(script|style).*?</\1>|<[^>]+>", " ", html, flags=re.S)
print("\nNumbers on the page (check each against metrics.md / the source files):")
for n in sorted(set(re.findall(r"\$?\d[\d,.]*\s?(?:%|K|k|min)?", text))):
    print(f"  {n.strip()}")
sys.exit(1 if bad else 0)
