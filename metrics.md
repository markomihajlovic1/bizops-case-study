# Metrics

## B1

**Number** = calls where `recap_posted_at − call_end ≤ 60 min` ÷ all client calls held for that pod (every row in `calls.csv`). Calls with no recap count as misses. Source: `calls.csv`, 1–24 Sep 2026, 140 calls.

| Rank | Pod | Lead | Calls held | Recap ≤ 60 min | Share | Dashboard | Calls short of 80% |
|---|---|---|---|---|---|---|---|
| 1 | North | Sam Whitaker | 40 | 36 | 36/40 = **90%** | 90% | 0 |
| 2 | East | Aisha Rahman | 30 | 21 | 21/30 = **70%** | 75% ⚠ | 3 |
| 3 | South | Marcus Obi | 40 | 14 | 14/40 = **35%** | 35% | 18 |
| 4 | West | Lena Varga | 30 | 3 | 3/30 = **10%** | 10% | 21 |

**Dashboard discrepancy:** `adoption.csv` shows East at 75%, but its own counts (21 of 30) give 70%. The dashboard divided by calls recorded (21/28 = 75%) instead of calls held (21/30 = 70%). East is 3 calls below target, not on the edge of it.

**What matters most: the agent alone can't hit a 60-minute target.** Only 29 of 59 agent-posted recaps (49%) landed within 60 minutes, with a median of 65 minutes. All 45 recaps posted by account managers landed within 60 minutes.
That accounts for most of the ranking. North's account managers posted 33 of its 38 recaps. South relied entirely on the agent and scored 35%. East went from 4/8 and 3/7 in weeks 36–37 (no account-manager posts) to 8/8 and 6/7 in weeks 38–39 (12 account-manager posts).
To reach 80%, a pod needs either a faster agent or account managers posting the recaps themselves.
