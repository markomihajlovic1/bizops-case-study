# South: one-week plan, Mon 28 Sep – Fri 2 Oct 2026

**Message to Marcus**

> Marcus, you're right that the recap bot is slower than your own notes: South's took a median 74 min in September.
> By then you've "already sent the client my version", so the work is done, it just never counts.
> One ask this week: send that version in the client's Slack channel instead of email, with action items as Owner | Action | Due.
> You get credit for work you already do, and I take your "if it posted in 10–15 min I'd use it" to engineering as the target.
> Template coming this morning.

**Pushback:** "Priya said emails count, and I've got the K&C fall-flavor plan due Tue and the sample list Thu." **Answer:** emails can't be timed and never reach the brain. Slack instead of email is the same text and the same send.
**What keeps it going:** the Slack post is the shortest path, because the client already reads that channel. Engineering's 15-minute draft turns it into edit-and-post. South's number goes into `NOW.md` every Monday, split by poster, so a slip shows up without me.

## What I do myself
- **Mon, first:** agree the definition with Priya before messaging Marcus. Keep "posted within an hour" (`NOW.md`), and offer her the alternative: account managers post the summary they already write in Slack, so it counts and reaches the brain.
- **Mon:** send the message and a template (summary bullets, then Owner | Action | Due), client-safe by default per `SANITIZER.md`: nothing said after the client leaves, no DMs, no opinions. The example is the [22 Sep K&C recap](brain/knowledge/meetings/2026-09-22-kettle-and-crumb.md), which covers c117, a call the agent never recapped.
- **Daily:** nudge Marcus once if a call has nothing posted 40 min after it ends. Account-manager recaps elsewhere land at a median of 18 min and a max of 28 (§3, [metrics-raw.md](metrics-raw.md)). I don't post for him: it wouldn't outlast my check-ins.
- **Fri:** rerun `pod_metrics.py` and report South's number split by poster.

## What I ask of the pod
Marcus (K&C plus four other South accounts, `marcus-obi.md`) posts his own recap in the client's Slack channel within 60 min of every call, including phone calls. Tomas does the same for calls he leads (he already sends his own summary, per `slack-thread.txt`). 4 of South's 40 calls were by phone, and none got a recap (`calls.csv`).

## What I ask of engineering
- **Speed:** South's agent median is 74 min, with 20 of 34 recaps after 60 min (§3, §5). Target: 10–15 min. Interim: a draft sent to the account manager within 15 min.
- **Silent failures:** c117 and c140 were recorded but never got a recap, and nobody was alerted (§2). Ask: alert the account manager if a recorded call has no recap 45 min after it ends.

## The number I expect by Friday
- **Baseline (`calls.csv`):** 14/40 = 35% (1–24 Sep), and 4/10 = 40% last week. That's about 10 calls a week, about 9 of them recorded (4/40 were phone).
- **Agent alone:** 14/34 = 41% of its recaps land within 60 min (§3).
- **If Marcus posts on 5 calls:** 5 + (9 − 5) × 0.41 ≈ 6.6 → **expect 6–7 of 10, about 65%.**
- **Range:** 3 posts gives 3 + 6 × 0.41 ≈ 5.5 (55%). 7 posts gives 7 + 2 × 0.41 ≈ 7.8 (about 80%). East's first week with account-manager posts (wk38) was 8 of 8 within 60 min, 7 of them posted by account managers (§4). So 80% is possible, but not in a heavy K&C week.
