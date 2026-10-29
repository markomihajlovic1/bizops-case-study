"""Block B metrics from calls.csv, cross-checked against adoption.csv.

Usage: python scripts/pod_metrics.py            (prints markdown tables)
       python scripts/pod_metrics.py > metrics-raw.md
"""
import csv
import math
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = 0.80


def load(name):
    with open(ROOT / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def minutes(c):
    if not c["recap_posted_at"]:
        return None
    end = datetime.fromisoformat(c["call_end"])
    posted = datetime.fromisoformat(c["recap_posted_at"])
    return (posted - end).total_seconds() / 60


def pct(n, d):
    return f"{n / d:.0%}" if d else "n/a"


calls = load("calls.csv")
dash = {r["pod"]: r for r in load("adoption.csv")}

pods = defaultdict(lambda: defaultdict(list))
for c in calls:
    p = pods[c["pod"]]
    p["all"].append(c)
    if c["recorded"] == "yes":
        p["recorded"].append(c)
    m = minutes(c)
    if m is not None:
        p["posted_" + c["posted_by"]].append(m)
        if m <= 60:
            p["in1h"].append(c)
    elif c["recorded"] == "yes":
        p["recorded_no_recap"].append(c)

order = sorted(pods, key=lambda k: len(pods[k]["in1h"]) / len(pods[k]["all"]), reverse=True)

print("## 1. Ranking on the number (recap within 1h / calls held)\n")
print("| Rank | Pod | Held | Recorded | In 1h | Share | Dashboard | Match | Calls short of 80% |")
print("|---|---|---|---|---|---|---|---|---|")
for i, k in enumerate(order, 1):
    p = pods[k]
    held, rec, ok = len(p["all"]), len(p["recorded"]), len(p["in1h"])
    d = dash[k]
    counts_match = (int(d["client_calls_held"]), int(d["calls_recorded"]), int(d["recaps_posted_within_1hr"])) == (held, rec, ok)
    share_match = d["share_of_calls_with_recap_within_1hr"] == pct(ok, held)
    match = "yes" if counts_match and share_match else ("counts ok, SHARE WRONG" if counts_match else "NO")
    short = max(0, math.ceil(TARGET * held) - ok)
    print(f"| {i} | {k} | {held} | {rec} | {ok} | {pct(ok, held)} | {d['share_of_calls_with_recap_within_1hr']} | {match} | {short} |")

print("\n## 2. Funnel: capture rate vs conversion of recorded calls\n")
print("| Pod | Capture (recorded/held) | Recorded -> recap in 1h | Recorded, no recap at all | Platforms |")
print("|---|---|---|---|---|")
for k in order:
    p = pods[k]
    plats = defaultdict(int)
    for c in p["all"]:
        plats[c["platform"]] += 1
    missing = ", ".join(f"{c['call_id']} ({c['account']}, {c['date']})" for c in p["recorded_no_recap"]) or "-"
    print(f"| {k} | {pct(len(p['recorded']), len(p['all']))} | {pct(len(p['in1h']), len(p['recorded']))} | {missing} | {dict(plats)} |")

print("\n## 3. Who posts, and how fast (minutes from call end)\n")
print("| Pod | Poster | Recaps | Within 1h | Median min | Max min |")
print("|---|---|---|---|---|---|")
all_agent = []
for k in order:
    for poster in ("AM", "agent"):
        ms = pods[k].get("posted_" + poster, [])
        if not ms:
            continue
        if poster == "agent":
            all_agent += ms
        n1 = sum(m <= 60 for m in ms)
        print(f"| {k} | {poster} | {len(ms)} | {n1} ({pct(n1, len(ms))}) | {statistics.median(ms):.0f} | {max(ms):.0f} |")
n1 = sum(m <= 60 for m in all_agent)
print(f"| ALL | agent | {len(all_agent)} | {n1} ({pct(n1, len(all_agent))}) | {statistics.median(all_agent):.0f} | {max(all_agent):.0f} |")

print("\n## 4. Weekly trend of the number (in 1h / held)\n")
weeks = sorted({datetime.fromisoformat(c["date"]).isocalendar().week for c in calls})
print("| Pod | " + " | ".join(f"wk{w}" for w in weeks) + " |")
print("|---|" + "---|" * len(weeks))
for k in order:
    cells = []
    for w in weeks:
        wk = [c for c in pods[k]["all"] if datetime.fromisoformat(c["date"]).isocalendar().week == w]
        ok = sum(1 for c in wk if (m := minutes(c)) is not None and m <= 60)
        am = sum(1 for c in wk if c["posted_by"] == "AM")
        cells.append(f"{ok}/{len(wk)} ({pct(ok, len(wk))}, AM {am})")
    print(f"| {k} | " + " | ".join(cells) + " |")

print("\n## 5. South: agent latency distribution\n")
south = sorted(pods["South"].get("posted_agent", []))
buckets = [(0, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90), (90, 999)]
for lo, hi in buckets:
    n = sum(lo < m <= hi for m in south)
    print(f"- {lo}-{hi if hi < 999 else '+'} min: {n}")
