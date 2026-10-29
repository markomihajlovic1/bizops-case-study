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

## B2

**Work on South first.** It is 18 calls short of 80% and West is 21 short (§1). South's gap is conversion, which North and East have already fixed. West's gap is capture, which is still unsolved. (§ = table in [metrics-raw.md](metrics-raw.md), the saved pod_metrics.py output.)

| | South | West |
|---|---|---|
| Short of 80% (§1) | 18 | 21 |
| Capture: recorded ÷ held (§2) | 36/40 = 90% | 4/30 = 13% |
| Conversion: recorded → ≤ 60 min (§2) | 14/36 = 39% | 3/4 = 75% |
| Weekly trend (§4) | 20, 50, 33, 40%; no account-manager posts | 0, 25, 11, 0%; no account-manager posts |
| Fixable in one week? | Yes: account managers post, as East did (§4) | No: WhatsApp capture still unsolved (`NOW.md`) |

**What people say vs what the data shows.** Marcus and Tomas say the agent is too slow, so they "skip it" (`slack-thread.txt`). The data agrees: South's agent median is 74 min, and 20 of its 34 recaps landed after 60 min (§3, §5). But the agent did post; what South lacks is account-manager recaps, which landed 45 of 45 within 60 min in North and East (§3).

**Actual cause.** A slow agent and zero account-manager recaps. Separately, c117 and c140 (both kettle-and-crumb) were recorded but never got a recap posted (§2), an agent failure separate from latency.

**Priya's proposal (count emailed summaries): don't adopt it.** Emailed summaries never reach the brain, so agents can't read them, SANITIZER never checks them, and they carry no action items with owners and dates (`RESOLVER.md` rules 1, 3). They also have no timestamp in `calls.csv`, and counting them would redefine the `NOW.md` number for South alone. Instead, account managers should post the summary they already write in the client's Slack channel.

**West:** start the capture work alongside South. 3/4 conversion is too small a sample to read (§2).
