"""C2: build a clean folder that holds only the skill, the brain and the transcript, for a fresh AI session.

Usage: python scripts/make_c2_sandbox.py           build ../recap-rerun (deletes an old one)
       python scripts/make_c2_sandbox.py --collect copy the new recap back to workers/output/after/
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOX = ROOT.parent / "recap-rerun"
TRANSCRIPT_NAME = "2026-09-15-loop-athletic-call.md"


def build():
    if BOX.exists():
        shutil.rmtree(BOX)
    shutil.copytree(ROOT / "brain", BOX / "brain")
    leftover = BOX / "brain" / "knowledge" / "meetings" / "2026-09-15-loop-athletic.md"
    leftover.unlink(missing_ok=True)
    (BOX / "workers" / "skills").mkdir(parents=True)
    shutil.copy(ROOT / "workers" / "skills" / "skill-recap.md", BOX / "workers" / "skills" / "skill-recap.md")
    (BOX / "inbox").mkdir()
    shutil.copy(ROOT / "workers" / "output" / "bad-recap-source.md", BOX / "inbox" / TRANSCRIPT_NAME)
    print(f"Built {BOX}")
    for p in sorted(BOX.rglob("*")):
        if p.is_file():
            print("  ", p.relative_to(BOX))
    print("\nNext: File > New Window > Open Folder > recap-rerun, then start a NEW agent chat there.")


def collect():
    new = [p for p in (BOX / "brain" / "knowledge" / "meetings").glob("2026-09-15-*.md")]
    if not new:
        sys.exit("No 2026-09-15-*.md recap found in the sandbox meetings folder.")
    dest = ROOT / "workers" / "output" / "after" / new[0].name
    dest.parent.mkdir(exist_ok=True)
    shutil.copy(new[0], dest)
    print(f"Copied {new[0].name} -> {dest}")


if __name__ == "__main__":
    collect() if "--collect" in sys.argv else build()
