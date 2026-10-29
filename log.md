# Log
**Total: 2h Human:** ~1h · **AI:** ~2h · **Skipped:** none

**First instruction:** "<paste your original A1 prompt verbatim>"

**Three things the AI got wrong**
1. **A2: missed a business risk.** It recorded the agreed sample budget ($8 a box, capped at $600 a month, so 75 boxes) without noticing that it can't cover the ~70 fall-flavor creators Dana asked for on 17 Sep plus the affiliate push to 60. Caught by: doing the arithmetic against the 17 Sep recap. Fixed: instruction (added "check every new decision against earlier asks and targets in prior recaps and flag conflicts").
2. **B3: left the decisive stakeholder out of the plan.** The plan for Marcus ignored Priya (Head of Ops), who had proposed counting emailed summaries as recaps. Without her agreement, Marcus's obvious pushback ("Priya said emails count") wins by default. It also misquoted East's first week as 7 of 8 when it was 8 of 8. Caught by: reading the Slack thread and `metrics-raw.md` against the plan. Fixed: output only (added a Monday step to agree the definition with Priya first, and corrected the number).
3. **C2: the skill rewrite would have broken its own test.** Step 11 told the agent to run `extra/recap_check.py`, but the fresh session sees only the skill, the brain and the transcript, so the tool wouldn't exist there. Caught by: comparing the skill's steps against what the rerun folder contains. Fixed: instruction (made the step conditional, with the self-check as the fallback), then reran. The rerun fixed every C1 issue on its first clean run.

