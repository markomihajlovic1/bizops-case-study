"""Check brain pages against RESOLVER.md and SANITIZER.md before they are saved or posted.

Usage: python extra/recap_check.py <file.md> [more files or folders]
Exit code 1 if any FAIL. WARN lines need a human look, they are not always wrong.
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHEET = ROOT / "brain" / "knowledge" / "reference" / "accounts-sheet.csv"

REQUIRED_FM = ["type", "date", "account", "attendees", "source"]
REQUIRED_H2 = ["Summary", "Action items", "Open questions", "Flags for a person"]
PERF = r"(gmv|ad spend|active affiliates|retention)"
MONEY = r"(\$\s?\d|\d+(\.\d+)?\s?k\b|thousand|million)"
SANITIZER_FAIL = [r"between us", r"don'?t mention", r"\bflaky\b", r"\bchecked out\b", r"\bdifficult\b",
                  r"\bfrustrated\b", r"agency fees?", r"\bmargins?\b", r"\bour fees?\b"]
PHONE = re.compile(r"\+?\(?\d{2,4}\)?[\s.-]?\d{3}[\s.-]?\d{3,4}\b")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
SANITIZER_WARN = [r"\bDM(ed|s)?\b", r"after .* left the call", r"\bprivate(ly)?\b", r"\bfees?\b",
                  r"\bhealth\b", r"\bfamily\b", r"\baddress\b", r"amazon"]
OWNER_SPLIT = re.compile(r"\s(and|&)\s|/|,")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        h = re.match(r"##\s+(.*)", line)
        if h:
            cur = h.group(1).strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def check(path):
    fails, warns = [], []
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    fm, body = frontmatter(text)
    is_recap = fm.get("type") == "meeting"

    if is_recap:
        for k in REQUIRED_FM:
            if not fm.get(k):
                fails.append(f"frontmatter missing '{k}'")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md", path.name):
            fails.append(f"file name '{path.name}' is not YYYY-MM-DD-brand-slug.md")
        elif fm.get("date") and not path.name.startswith(fm["date"]):
            fails.append("file name date != frontmatter date")
        if fm.get("account") and fm["account"] not in path.name:
            warns.append("account slug not in file name")
        if "brain" not in path.parts or "meetings" not in path.parts:
            warns.append("recap is not saved under brain/knowledge/meetings/")
        if not re.search(r"^# .+: .+", body, re.M):
            fails.append("title is not '# <Brand>: <meeting name>'")

        secs = sections(body)
        for h in REQUIRED_H2:
            if h not in secs:
                fails.append(f"missing section '## {h}'")
        bullets = [l for l in secs.get("Summary", []) if l.strip().startswith("- ")]
        if "Summary" in secs and not 3 <= len(bullets) <= 6:
            fails.append(f"summary has {len(bullets)} bullets, template says 3 to 6")

        rows = [l for l in secs.get("Action items", []) if l.strip().startswith("|")]
        rows = [r for r in rows if not re.match(r"\|\s*-+", r) and "Owner" not in r]
        if "Action items" in secs and not rows:
            fails.append("no action items table rows")
        attendees = fm.get("attendees", "")
        meeting = date.fromisoformat(fm["date"]) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm.get("date", "")) else None
        for r in rows:
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            if len(cells) != 3:
                fails.append(f"action row needs 3 cells (Owner | Action | Due): {r.strip()}")
                continue
            owner, action, due = cells
            if not owner or OWNER_SPLIT.search(owner) or owner.lower() in {"team", "tbd", "we", "brightline"}:
                fails.append(f"action needs exactly one named owner: '{owner}' / {action}")
            elif owner.split()[0] not in attendees:
                warns.append(f"owner '{owner}' is not in attendees")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due):
                fails.append(f"due date not YYYY-MM-DD: '{due}' / {action}")
            elif meeting and date.fromisoformat(due) < meeting:
                fails.append(f"due date {due} is before the meeting / {action}")

    section = None
    rule_file = fm.get("type") in {"sanitizer", "resolver", "skill"}
    brain_page = "brain" in path.resolve().parts
    in_fence = False
    for n, line in enumerate([] if rule_file else text.splitlines(), 1):
        low = line.lower()
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and not brain_page:
            continue
        if h := re.match(r"##\s+(.*)", line):
            section = h.group(1).strip()
        if line.startswith(("source:", "account:", "date:", "updated:")):
            continue
        if not brain_page:
            pass
        elif re.search(PERF, low) and re.search(MONEY, low) and "accounts-sheet" not in low:
            fails.append(f"L{n} performance number typed, link the sheet instead: {line.strip()[:90]}")
        elif re.search(r"\d+\s+active affiliates", low) and "target" not in low and "accounts-sheet" not in low:
            warns.append(f"L{n} active affiliates count typed? link the sheet: {line.strip()[:90]}")
        for pat in SANITIZER_FAIL:
            if re.search(pat, line, re.I):
                fails.append(f"L{n} SANITIZER ({pat}): {line.strip()[:90]}")
        if PHONE.search(ISO_DATE.sub("", line)):
            fails.append(f"L{n} SANITIZER (phone number?): {line.strip()[:90]}")
        if section == "Flags for a person":
            continue
        for pat in SANITIZER_WARN:
            if re.search(pat, line, re.I):
                warns.append(f"L{n} sanitizer? ({pat}): {line.strip()[:90]}")

    prose = re.sub(r"```.*?```|`[^`\n]*`", "", text, flags=re.S)
    for target in re.findall(r"\]\(([^)#\s]+)", prose):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).resolve().exists():
            fails.append(f"broken link: {target}")
        elif "inbox" in Path(target).parts:
            warns.append(f"links to a raw transcript: {target}")

    return fails, warns


def main(args):
    files = []
    for a in args:
        p = Path(a)
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    bad = 0
    for f in files:
        fails, warns = check(f)
        status = "FAIL" if fails else ("WARN" if warns else "PASS")
        print(f"\n{status}  {f}")
        for m in fails:
            print(f"  FAIL  {m}")
        for m in warns:
            print(f"  WARN  {m}")
        bad += bool(fails)
    print(f"\n{len(files)} file(s), {bad} with FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
