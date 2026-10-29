# Execution plan: Ironside Biz Ops case study v1.2

**Setup:** Cursor agent plus Python 3.13. Results go on one HTML page hosted with GitHub Pages, with a public GitHub repo behind it. All 9 questions plus extra credit. A1 is treated as not done.
**Full plan is about 5 h.** You decide where to stop; the checkpoint column in the table below shows what you can ship at each point.

> **Keep this file away from the AI.** It contains the expected answers. If Cursor reads it, its mistakes disappear and you have nothing honest to log. Step 0.2 hides it.

---

## 1. Order of work

| # | Step | Est. | Cumulative | Why here | Checkpoint (shippable if you stop) |
|---|---|---|---|---|---|
| 0 | Setup | 15m | 0:15 | Git baseline means `git diff` gives you every before/after for free | – |
| 1 | A1 recap call-1 | 20m | 0:35 | Teaches you the brain rules. A2, A3 and C1 reuse them | |
| 2 | A2 recap call-2 + proposals | 30m | 1:05 | Same rules. A3 needs its facts (Jess, budget, GMV conflict) | **Block A core** |
| 3 | A3 Dana briefing | 25m | 1:30 | Needs the A1 and A2 recaps to exist | **Block A done** |
| 4 | B1 rank + extra number | 15m | 1:45 | Script does the counting, you do the judgement | |
| 5 | B2 which pod and why | 15m | 2:00 | Builds on B1 output | |
| 6 | B3 `plan.md` | 30m | 2:30 | Needs the B2 diagnosis | **Block B done** |
| 7 | C1 bad-recap issues | 15m | 2:45 | The rules are fresh from Block A | |
| 8 | C2 skill + fresh rerun | 35m | 3:20 | Needs the C1 list | |
| 9 | C3 FDE ticket | 15m | 3:35 | Needs evidence from both B (latency) and C (content) | **All 9 done** |
| 10 | Extra: recap checker | 15m | 3:50 | Already built and tested, you only review and own it | |
| 11 | HTML results page | 35m | 4:25 | Needs all outputs | |
| 12 | Publish, log, book call | 20m | 4:45 | Last | **Submitted** |

**Minimum shippable cut:** steps 0–2, 4–5, 7, 11–12, about 2h45. List whatever you didn't do as skipped.

**Working rules for the whole session**
- Open a new Cursor agent chat per block (A, B, C). Use a separate window for the C2 rerun.
- Reference files with `@path` in prompts. Never let the AI edit `people/`, `accounts/` or `reference/`.
- Run `python extra/recap_check.py <file>` after every recap. A green result doesn't prove the content is right, so still do the manual checks.
- **Log mistakes the moment you catch them** in the scratch section of `log.md`: what was wrong, how you caught it, and whether you fixed the instruction or only the output.
- **Time log:** write a start and stop time per step in `log.md`. Count AI time as the minutes the agent was actually generating.
- `git commit` after every step, e.g. `git add -A; git commit -m "A1"`.

**Calendar cheat-sheet** (the most likely AI mistake is turning a weekday into the wrong date)

| Day | Date | Day | Date |
|---|---|---|---|
| Tue | 2026-09-15 (bad-recap call) | Thu | 2026-09-24 (call-2) |
| Fri | 2026-09-18 | Fri | 2026-09-25 |
| Tue | 2026-09-22 (call-1) | Tue | 2026-09-29 |
| Wed | 2026-09-23 | Thu | 2026-10-01 |
| Tue | 2026-10-06 (fall flavor launch) | Sat | 2026-10-31 (target date) |

---

## 2. Scripts (already in the folder and tested)

| Script | Used in | What it does |
|---|---|---|
| `scripts/pod_metrics.py` | B1, B2, B3, C3 | Ranks pods from `calls.csv` and cross-checks `adoption.csv`. Also prints the funnel (capture rate vs recorded-to-recap), poster and latency per pod, the weekly trend, and South's latency distribution |
| `extra/recap_check.py` | A1, A2, A3, C1, C2, Extra | Lints any `.md` against RESOLVER and SANITIZER: frontmatter, file name, sections, 3–6 bullets, one owner plus ISO due date per action, typed GMV, banned phrases, phone numbers, broken links |
| `scripts/make_c2_sandbox.py` | C2 | Builds `../c2-sandbox` with only the brain, the skill and the transcript (renamed so it doesn't say "bad"). `--collect` copies the new recap back |
| `scripts/check_html.py` | Step 11 | Checks that every GitHub link on the page maps to a real file, and lists every number on the page for a manual check |

**Automated:** counting, latency, ranking, dashboard cross-check, format and sanitizer linting, link checks, building the clean C2 session.
**By hand:** pod choice and diagnosis, judging what's sanitizer-sensitive in context, date interpretation, the message to the pod lead, proposal wording, and the final read of every file.

---

## 3. Step by step

### Step 0: Setup (15m)

- [ ] 0.1 Move the old call-1 recap out of the folder, since A1 starts from scratch: `Move-Item brain\knowledge\meetings\2026-09-22-kettle-and-crumb.md ..\old-call-1-recap.md`
- [ ] 0.2 Create `.cursorignore` in the root containing the line `execution-plan.md`. Also add `execution-plan.md` to `.gitignore`, unless you want reviewers to see it.
- [ ] 0.3 Back up the original skill for the C2 before/after: `Copy-Item workers\skills\skill-recap.md workers\skills\skill-recap.v1.md`
- [ ] 0.4 Install git: `winget install --id Git.Git -e`, then restart the terminal. Optionally `winget install --id GitHub.cli -e`.
- [ ] 0.5 Set up the repo: `git config --global user.name "..."`, `git config --global user.email "..."`, `git init`, `git add -A`, `git commit -m "Original case materials"`
- [ ] 0.6 Smoke test: `python scripts/pod_metrics.py` and `python extra/recap_check.py brain workers/output/bad-recap.md`. You should see `bad-recap.md` FAIL and everything in `brain/` PASS.
- [ ] 0.7 Create `log.md` from the template in section 5 and write down your start time.

---

### A1: Recap call-1 (20m)

**Read:** `brain/RESOLVER.md`, `brain/SANITIZER.md`, `inbox/call-1.md`, `brain/knowledge/reference/accounts-sheet.csv`, the 4 Kettle & Crumb meeting recaps, `people/dana-reyes.md`, `people/marcus-obi.md`, `accounts/kettle-and-crumb.md`
**Output:** `brain/knowledge/meetings/2026-09-22-kettle-and-crumb.md`

**Prompt** (this is your "first instruction" for the log, so copy it in verbatim):
```
Task: write the recap for @inbox/call-1.md into brain/knowledge/meetings/.

Before writing anything, read these in full and list each file back with one line on what you took from it:
@brain/RESOLVER.md @brain/SANITIZER.md @brain/NOW.md @brain/knowledge/reference/accounts-sheet.csv
every file in brain/knowledge/meetings/ for kettle-and-crumb, and the people and account pages for everyone on the call.
Do not assume anything that isn't in these files.

Then, before writing the file, show me a table: fact you plan to include | transcript timestamp | earlier recap that already covered it (link) or "new" | rule that applies.

Apply the rules literally:
- RESOLVER recap template exactly. File name YYYY-MM-DD-brand-slug.md. source: inbox/call-1.md.
- Performance numbers (GMV, ad spend, active affiliates, retention) are never typed. Link the sheet. If the call's number disagrees with the sheet, flag it in "Flags for a person" without copying the number.
- ONLY those four are performance numbers. State every other count as said on the call (e.g. new affiliates, posts, videos, creators).
- Check every new decision against earlier asks and targets in prior recaps, and flag conflicts as Open questions.
- Targets, budgets and rates the client agrees to are decisions: record them as said.
- Every action item has exactly one owner and an absolute YYYY-MM-DD due date. The call was Tuesday 2026-09-22. If an owner or date was not stated, put it under Open questions instead of guessing.
- Leave out anything said after the client left, any pasted DM and any opinion about a person. In Flags, say that something was held back without repeating it.
- If something was already told in an earlier meeting, say so and link that recap.
Write only this one file. Then run `python extra/recap_check.py <file>` and fix any FAIL.
```

**Done when:** the file exists, the checker passes, and every check below is ticked.

**Verify (manual, about 5 min):**
- [ ] Nothing from 01:44 onward appears anywhere: no "flaky", no Jess, no Amazon, no "plan like we won't have it". Flags says only that comments after Dana left were held back.
- [ ] The active affiliates count (32) and the weekly affiliate GMV ("a bit over four thousand") are **not typed**; the sheet is linked instead. The 32 matches the sheet, so there's no conflict to flag. Weekly affiliate GMV isn't a sheet column, so leave it out or link.
- [ ] "Up to $8 a box for now" is recorded as said. The monthly cap is still open: it goes under Open questions, with a Dana action due **2026-09-25**.
- [ ] Earlier meetings are linked: the 60 target goes to the 09-03 recap, the shipping budget to 08-12 and 09-03, the recuts close the 09-17 action, and the Wednesday summary goes to 09-03.
- [ ] Action items: Tomas sends 25 creators **09-22**; Dana approves them **09-23**; Dana approves the recuts **09-23**; Marcus adds top creators to the Wednesday summary **09-23**; Dana confirms the cap **09-25**.
- [ ] "Samples go out Thursday" has **no named owner**. It should be an open question, not an invented owner.
- [ ] 3–6 summary bullets, and every bullet traces back to a timestamp.

**Likely log entries:** a typed 32 or $4K, the Amazon "risk" sneaking in, an invented owner for samples, the wrong weekday date.

---

### A2: Recap call-2 + `proposed-changes.md` (30m)

**Read:** everything from A1, plus `inbox/call-2.md` and your new 09-22 recap
**Outputs:** `brain/knowledge/meetings/2026-09-24-kettle-and-crumb.md` and `proposed-changes.md` in the root

**Prompt 1** (same chat as A1 is fine):
```
Same task and same rules for @inbox/call-2.md (Thursday 2026-09-24). Re-read @brain/RESOLVER.md and @brain/SANITIZER.md first,
and read the 2026-09-22 recap you just wrote. Show the fact table before writing. Also check:
- Any number on this call vs accounts-sheet.csv. Quote the sheet value and date to me in chat. Don't copy the call's number onto the page; flag it.
- Which earlier open questions or action items this call closes. Link them.
- Relative dates ("next Tuesday", "the Thursday before"): give the date and your reasoning. If it's ambiguous, give the most likely date AND add an open question.
Write only the recap file, then run the checker.
```

**Prompt 2:**
```
Now write proposed-changes.md in the repo root. Do NOT edit any page in brain/.
First read every file in brain/knowledge/people/ and brain/knowledge/accounts/, and the sheet.
For each proposed edit give: file | current text (quoted) | proposed text | source (recap link + transcript timestamp) | approver.
Include new pages if a new person appeared. Apply SANITIZER to every proposed line, including anything you know about
that person from other calls. For the reference sheet: RESOLVER says consult, don't edit. Say exactly what you would ask
the sheet owner to verify before any GMV change, and why the call's figure may not be comparable.
End with a list of anything you were unsure about.
```

**Verify the recap:**
- [ ] The $210K GMV is **not typed** in the recap. It's flagged as disagreeing with the sheet, and the scope is unconfirmed: Marcus asked "TikTok Shop only?" and Dana deflected (00:43–00:46), while the account sells TikTok Shop plus DTC.
- [ ] "$8 a box, capped at $600 a month" is recorded as a client decision. It closes the thread from 08-12, 09-03 and 09-22, and those are linked. It also closes the call-1 "Dana confirms cap" action, answered by Jess.
- [ ] Jess Park is introduced as taking over ops and fulfillment, with samples and inventory going to her. **Nothing from the call-1 DM appears.**
- [ ] Dana is now VP Growth: she'll be at the monthly reviews, and Jess joins the weeklies.
- [ ] The 60-by-31-Oct target links to 09-03 and the 6 Oct fall flavor date links to 09-17. "Double the posting rate" has no baseline, so it's an open question.
- [ ] Action items: Marcus sends the fall flavor creator plan **2026-09-29**. Marcus sends the sample list to Jess on "the Thursday before", most likely **2026-10-01** (the Thursday before the 6 Oct launch), with an open question about the ambiguity.
- [ ] Bonus check: a $600 cap at $8 a box is 75 boxes a month, against about 70 fall flavor creators in October (09-17) plus ongoing affiliate samples. Did the AI notice?

**Verify `proposed-changes.md`:**
- [ ] `dana-reyes.md`: role becomes VP Growth (from 09-24). Adds 09-22 and 09-24 to "What she has told us". Closes the shipping-budget open thread with a link. Notes that samples and shipping now go through Jess. Does she still approve creators? That's an open question, not an assumption.
- [ ] New `jess-park.md`: ops and fulfillment, owns samples, inventory and the shipping budget, joins the weeklies, works with Marcus. **No DM, no Amazon.** (This is the hardest trap in the case.)
- [ ] `kettle-and-crumb.md`: Dana's title, Jess as ops contact, 09-22 and 09-24 added to the meetings list, fall flavor launch added to current focus.
- [ ] Sheet: **no "change GMV to 210000"**. Instead, a flag to the sheet owner: the call said $210K, which is finance's number with unconfirmed scope, while the sheet says $140K (updated 09-21). Verify against the export before changing anything.
- [ ] Approver is Marcus, as South pod lead. Nothing was actually edited: `git diff --stat brain/knowledge/people brain/knowledge/accounts brain/knowledge/reference` returns nothing.

**Likely log entries:** proposing 210K straight into the sheet, mentioning Jess's DM on her page, a wrong date for "the Thursday before".

---

### A3: `answer.md`, Dana briefing (25m)

**Read:** all Kettle & Crumb recaps (including your two new ones), `dana-reyes.md`, `kettle-and-crumb.md`, the sheet, `proposed-changes.md`

**Prompt** (new chat is better, since it tests whether the brain stands alone):
```
Question from a colleague: "I'm talking to Dana at Kettle & Crumb about affiliates, end to end. What do I need to know?"
Answer in answer.md (repo root). Use ONLY files in brain/ and proposed-changes.md. Read every kettle-and-crumb meeting,
Dana's people page, the account page and the sheet before writing. Every claim gets a relative link to its source file.
Structure: TL;DR (3 bullets) | Who's who now | The affiliate flow end to end, as Dana defined it | Where we are vs target |
Open threads and risks | What NOT to re-ask (things she already told us, with dates) | What not to bring up.
Rules: performance numbers come from the sheet, with its date. If sources conflict, show both and say which is unverified.
Nothing that came from a DM or side comment. One page max. Then run `python extra/recap_check.py answer.md`.
```

**Verify:**
- [ ] The checker passes, so all links resolve. Open 3 links at random and confirm the claim is really in that file.
- [ ] It says Dana is now VP Growth and that samples and shipping go to Jess. An end-to-end affiliates conversation should loop Jess in for samples.
- [ ] The flow covers: food and baking creators with 5K–100K followers; commission of 15% open and 20% targeted for the top 10; Dana approves every creator within 48h; one box per creator, sent only after they accept the targeted plan; posts; commission paid via TikTok Shop; the Wednesday summary plus top creators.
- [ ] Status: active affiliates **linked to the sheet** (32 as of 09-21) vs 60 by 31 Oct, so 28 to go in about 5 weeks. 25 creators were sent 09-22 for approval.
- [ ] The tension between the 75-box monthly cap and about 70 fall flavor creators is raised. The GMV conflict is shown as unresolved, without quoting $210K as fact.
- [ ] "Don't re-ask": she has explained the flow twice already (08-12 and 09-03), and the budget was asked three times before it was answered.
- [ ] No Amazon, no "flaky".

---

### B1: Rank pods + one more number (15m)

**Read:** `adoption.csv`, `calls.csv`, `brain/NOW.md`
**Output:** `metrics.md` in the root (B1 and B2 together)

**Steps:** run `python scripts/pod_metrics.py > metrics-raw.md`, then use the prompt below.

**Prompt** (new chat for Block B):
```
Read @adoption.csv, @calls.csv, @brain/NOW.md and @slack-thread.txt, then run `python scripts/pod_metrics.py`.
Before trusting the dashboard, recompute the number yourself from calls.csv: recaps posted within 60 min of call_end
divided by client calls held. Show the formula. Write section "B1" of metrics.md: ranking table, one line on any
dashboard discrepancy, then ONE extra number from the data that you think matters most and why (max 4 lines).
Only use numbers you can trace to calls.csv or the script output.
```

**Expected:** North 90%, **East 70%**, South 35%, West 10%. East's dashboard shows **75% because it divides 21 by 28 recorded calls** instead of 30 calls held.

**Recommended extra number:** the agent on its own posts within an hour on only **49% of calls (29/59), median 65 min**. No pod can hit 80% with the agent alone. North (33 of 38 recaps posted by the AM) and East (switched to AM posting in week 38, jumping from 43% to 100%) hit it because humans post. Backup option: West's capture rate of 13% (4 of 30 calls recorded).

**Verify:**
- [ ] Hand-check one pod: open `calls.csv` in Excel, filter pod = South, and count recaps within 60 min. It should be 14 of 40.
- [ ] The denominator is calls held, which matches the definition ("share of client calls"), not calls recorded.
- [ ] If the AI repeats 75% for East, **log it**: it trusted the dashboard over the raw data.

---

### B2: Which pod first, and the real cause (15m)

**Read:** `metrics-raw.md`, `slack-thread.txt`, `brain/NOW.md`, `people/marcus-obi.md`, `people/lena-varga.md`

**Prompt:**
```
Write section "B2" of metrics.md: which pod to work on first, and what is ACTUALLY causing its gap.
Compare at least South and West on: calls short of 80%, what's blocking them (capture vs conversion), and what is
fixable in one week. Use the funnel, poster/latency and weekly-trend tables, the Slack thread and NOW.md.
Separate what people say from what the data shows. Address Priya's proposal in the Slack thread explicitly.
Max 12 lines. Cite the file and number for every claim.
```

**Expected reasoning** (your call, but South is the strong answer):
- **South:** 18 calls short of 80%, but 90% of calls are already recorded and the content is fine (Marcus says so). The gap is speed and habit. The agent's median is 74 min, and **0 of 34** agent recaps landed under 30 min. Nobody in South posts manually; Marcus and Tomas email their own summaries instead. Where AMs post, the median is 18 min and 100% are within an hour. East proved the fix in week 38. Also, c117 and c140 (both K&C) were recorded and never got a recap at all.
- **West:** lower, but the cause is capture: 26 of 30 calls are on unrecorded WhatsApp. Recorded West calls convert at 75%. The fix is tooling plus client habit, and Lena is already on it. That belongs in the engineering ask, not this week's pod.
- **Priya:** counting emailed summaries changes the definition, not the outcome. Those summaries never reach the brain, the agents or the SANITIZER check. The honest alternative is to paste the summary you already write into the channel using the template.

**Verify:**
- [ ] The conclusion isn't just "the bot is slow". It names the missing human-posting routine plus latency, with numbers.
- [ ] Every number matches `metrics-raw.md`.

---

### B3: `plan.md` (30m)

**Prompt:**
```
Write plan.md for South for one week (state the dates; assume Mon 28 Sep - Fri 2 Oct 2026, the week after the data).
Read metrics.md, @slack-thread.txt, @brain/NOW.md, @brain/knowledge/people/marcus-obi.md first.
Top: the message to Marcus, max 5 lines, using his own words from the Slack thread, one small ask, what he gets.
Then max 4 lines: his likely pushback + my answer; what keeps the change going after I stop checking in.
Then 4 sections: what I do myself | what I ask of the pod | what I ask of engineering | the number I expect by Friday,
with the arithmetic (South runs ~10 calls/week; baseline from calls.csv). Be realistic, not 80% by default.
Total under one page. Don't rely on Priya's redefinition.
```

**Verify:**
- [ ] The message is ≤5 lines, sounds human, and quotes "if it posted in 10–15 min I'd use it".
- [ ] Pushback is covered, e.g. "double work, I already email Dana" or "Priya said emailed summaries count". So is sustainability: weekly pod dashboard, posting becoming the default step, the engineering latency fix, Priya aligned.
- [ ] Engineering asks: draft to the AM in ≤15 min for approve-and-post; alert when a recorded call has no recap (c117, c140).
- [ ] The Friday number has math, e.g. 7 of 10 calls is about 70%, vs a weekly baseline of 20–50%.
- [ ] Open `plan.md` and check the message is actually ≤5 lines.

---

### C1: What's wrong with `bad-recap.md` (15m)

**Read:** `workers/output/bad-recap.md`, `workers/output/bad-recap-source.md`, `RESOLVER.md`, `SANITIZER.md`, `meetings/2026-09-10-loop-athletic-weekly.md`, `accounts/loop-athletic.md`, the sheet
**Output:** `c1-issues.md`

**Steps:** run `python extra/recap_check.py workers/output/bad-recap.md`, then use the prompt below.

**Prompt** (new chat for Block C):
```
Compare @workers/output/bad-recap.md with its source @workers/output/bad-recap-source.md against @brain/RESOLVER.md,
@brain/SANITIZER.md, the sheet, and the earlier Loop Athletic recap and account page. Read all of them first.
Write c1-issues.md: table of issue | evidence (quote + transcript timestamp or file) | rule broken | severity (client-visible harm first).
Also run `python extra/recap_check.py workers/output/bad-recap.md` and note anything it catches that you missed, or vice versa.
```

**Your answer key** (check the AI's list against this):
1. A pasted DM after Theo left ("CEO frustrated with the agency fees… review in Q1"). This breaks the private-content rule and the commercial-terms rule. **Highest severity:** the agent posts to the client's Slack.
2. "Keep an eye on the account review risk" is an action built on that same DM.
3. "$95K GMV this month" is typed rather than linked. The sheet says $62K for the last 30 days, and the conflict isn't flagged. "This month" and "last 30 days" also aren't the same thing.
4. Next steps have no owners and no due dates. The brief is due Friday (**2026-09-18**, Lena). The size chart has an owner (Lena, "we'll look into it") but no due date, so it should be an open question.
5. No link to the 09-10 recap: the try-on decision was made there, and Theo owed the fall size chart by 09-11, which is probably related to the "size chart issue".
6. Not the template: frontmatter is missing attendees and source; the title format is wrong; it's a paragraph instead of 3–6 bullets; there are no Open questions or Flags sections.
7. "Great call" is an opinion, not a fact.
8. Wrong place and name: it's in `workers/output/bad-recap.md`, not `brain/knowledge/meetings/2026-09-15-loop-athletic.md`.
9. It's a rare West Meet call (thanks to Lena at 00:00), so it counts in the number. It posted in 55 min (c084) and therefore **counted as a success** despite the leak. The metric doesn't measure quality. Save this for C3.

**Verify:** every item has a quote, and every quote really is in the source. Search the transcript for each quote.

---

### C2: Fix the skill and rerun it fresh (35m)

**Output:** edited `workers/skills/skill-recap.md`, the new recap in `workers/output/after/`, and `c2-before-after.md`

**Prompt 1** (Block C chat):
```
Rewrite @workers/skills/skill-recap.md so every issue in @c1-issues.md cannot happen again. First read RESOLVER and SANITIZER.
Constraints: generic (no mention of Loop, Theo, $95K or this call); numbered steps an agent can follow; under 60 lines;
keep the frontmatter (type: skill), bump updated. Must cover: read RESOLVER, SANITIZER, the sheet and prior recaps for the
account first; stop at the moment the client leaves; exclude DMs, opinions and commercial terms; never type performance
numbers, compare them with the sheet and flag conflicts; one owner + absolute date per action (compute from call date + weekday),
otherwise Open questions; link earlier meetings; exact template, path and file name; a self-check before saving.
Then give me a table: C1 issue -> skill line that prevents it.
```

**Steps:**
1. Review the skill. The mapping table must cover all of your C1 items, and the skill must stay generic.
2. Run `python scripts/make_c2_sandbox.py`. In Cursor, go to **File > New Window > Open Folder** and pick `Desktop\c2-sandbox`, then start a **new** agent chat.
3. **Prompt 2**, in the sandbox chat only:
   ```
   Follow workers/skills/skill-recap.md exactly to recap inbox/2026-09-15-loop-athletic-call.md. Use only files in this folder.
   ```
4. Back in the main folder, run `python scripts/make_c2_sandbox.py --collect`, then `python extra/recap_check.py workers/output/after`.
5. If anything fails: **fix the skill, not the output**. Rebuild the sandbox, open a new chat and rerun. Log it as "fixed the instruction".
6. Write `c2-before-after.md`. AI can assemble it: skill v1 vs v2 (`git diff workers/skills/skill-recap.md`, or the `.v1` copy), bad recap vs new recap, checker output before and after, and a table of each C1 issue marked fixed or not fixed.

**Verify the new recap:**
- [ ] No DM, no fees, no review risk. Flags says something was held back.
- [ ] GMV isn't typed; the sheet conflict is flagged.
- [ ] Action items: Lena sends the October brief **2026-09-18**. The size chart owner is set but the due date is open, so it's an open question.
- [ ] The 09-10 recap is linked for the try-on decision and the size chart.
- [ ] The checker passes, and the file is named `2026-09-15-loop-athletic.md`.
- [ ] Delete `Desktop\c2-sandbox` once you're done.

---

### C3: `fde-ticket.md`, under 150 words (15m)

**Prompt:**
```
Write fde-ticket.md for the engineer who builds the recap agent: what must change that a skill file CANNOT fix.
Read metrics-raw.md, c1-issues.md, c2-before-after.md, @brain/NOW.md, @calls.csv. Max 4 asks, each with one line of evidence
(call IDs or numbers). Under 150 words total. Format: Title, Problem (1 line), Asks (numbered), Evidence, Done when.
```

**Strong asks with evidence:**
1. **Latency:** median 65 min, only 29 of 59 agent recaps within an hour, 0 of 34 South recaps under 30 min. Target a draft to the AM in ≤15 min.
2. **Silent failures:** c117 and c140 were recorded but never got a recap. Add an alert and a retry.
3. **Review gate before posting to the client's Slack:** c084 leaked a DM and still counted as on time. Also cut the transcript at the client's leave event, which is deterministic in a way a prompt isn't.
4. **WhatsApp capture:** 26 of 30 West calls never reach the agent. (Optional ask: fix the dashboard share formula, since East shows 75% when the real figure is 70%.)

**Verify:** count the words with `((Get-Content fde-ticket.md -Raw) -split '\s+' | ? {$_}).Count`, which must be under 150. Every number should match `metrics-raw.md`.

---

### Extra: recap checker (15m)

The tool is already at `extra/recap_check.py`, with `extra/README.md` (5 lines).
- [ ] Run it from a fresh terminal on `brain/` and on `workers/output/bad-recap.md`.
- [ ] Rewrite the README's "Why" line in your own words. Keep it to 5 lines.
- [ ] Optional 5-min tweak with AI, so the build is yours: "Add a check to extra/recap_check.py that compares any number on a line mentioning GMV with accounts-sheet.csv for the recap's account and FAILs on a mismatch. Read the script first."
- [ ] **One line for the page on why you picked it:** every recap goes to the client and the brain, so a single leaked DM or typed GMV is the most expensive mistake in this role, and this catches it in under a second.

---

### Step 11: HTML results page (35m)

**Output:** `docs/index.html`, a single file with inline CSS and no frameworks

**Prompt:**
```
Build docs/index.html: one client-ready page summarising my case study results. First read every deliverable:
log.md, metrics.md, plan.md, answer.md, proposed-changes.md, c1-issues.md, c2-before-after.md, fde-ticket.md,
extra/README.md, and the two new recaps. Use ONLY facts and numbers from those files; don't invent any.
Layout: header (name, role, time spent, "Skipped: none"), 3-line TL;DR, one card per block (A, B, C) with the
key result in 2-3 bullets and links to each file, a small pure-CSS bar chart of the 4 pods (real vs dashboard for East),
extra credit (1 line why), "What I'd automate next" (3 sentences, I'll edit), footer link to the repo and log.
Links to files use https://github.com/<USER>/<REPO>/blob/main/<path>. Single file, inline CSS, system fonts,
neutral palette with one accent colour, readable on mobile, no JavaScript needed.
```

**Verify:**
- [ ] `python scripts/check_html.py`: every link shows OK, and every listed number can be found in `metrics.md` or the source files.
- [ ] Open it in a browser at desktop width and at about 400 px.
- [ ] Read it as the client would: is it clear in 60 seconds, with no internal shorthand?

---

### Step 12: Publish, log, book (20m)

- [ ] Create a **public** repo on github.com, then: `git remote add origin https://github.com/<USER>/<REPO>.git`, `git branch -M main`, `git push -u origin main`
- [ ] Go to Settings > Pages > Deploy from branch > `main` / `/docs`. Wait about 1 min, then open `https://<USER>.github.io/<REPO>/` in an **incognito** window.
- [ ] Click every link on the live page.
- [ ] Finish `log.md` (section 5), commit and push.
- [ ] Book the session at tidycal.com/jeremycarr.
- [ ] Rehearse a live change: rerun the checker, edit the skill and rerun it in the sandbox, change a rule in `recap_check.py`.

---

## 4. Final deliverable checklist

**Repo files**
- [ ] `log.md`
- [ ] `brain/knowledge/meetings/2026-09-22-kettle-and-crumb.md`
- [ ] `brain/knowledge/meetings/2026-09-24-kettle-and-crumb.md`
- [ ] `proposed-changes.md`
- [ ] `answer.md`
- [ ] `metrics.md`, `metrics-raw.md`
- [ ] `plan.md`
- [ ] `c1-issues.md`
- [ ] `workers/skills/skill-recap.md` (v2) and `skill-recap.v1.md`
- [ ] `workers/output/after/2026-09-15-loop-athletic.md`
- [ ] `c2-before-after.md`
- [ ] `fde-ticket.md`
- [ ] `extra/recap_check.py` and `extra/README.md`
- [ ] `scripts/`
- [ ] `docs/index.html`
- [ ] People, account and sheet files **unchanged** (`git diff <first-commit> --stat brain/knowledge/people brain/knowledge/accounts brain/knowledge/reference` returns nothing)

**On the page**
- [ ] Repo link, public and tested in incognito
- [ ] **Time:** "About X h of my time, about Y h of AI time." Use the real numbers from your log. If you go past 4 h, say so plainly; the folder's cap is 6 h.
- [ ] **Skipped:** "None", or the exact question IDs you stopped before
- [ ] **Three sentences on what to automate next**, drafted below; make them yours:
  > 1. Put `recap_check` inside the recap agent as a gate, so nothing that fails SANITIZER or retypes a number can reach a client channel.
  > 2. Send the recap draft to the AM in Slack within 10 minutes for one-tap approve-and-post, because the data shows humans posting is the only thing that clears 80% today.
  > 3. Generate `proposed-changes` automatically from every recap into a pod-lead approval queue, so people and account pages stop going stale.

**Send**
- [ ] One link (the GitHub Pages URL)
- [ ] Session booked

---

## 5. `log.md` template (aim for about 10 lines)

```markdown
# Log
**Human:** ~X h · **AI:** ~Y h (agent generation time) · **Skipped:** none

**First instruction:** "<paste the A1 prompt verbatim>"

**Three things the AI got wrong**
1. <what> · Caught by: <checker / hand count / reading source at 01:47> · Fixed: instruction | output only
2. ...
3. ...

<!-- scratch: delete before submitting -->
| Step | Start | End | Notes / mistakes |
|---|---|---|---|
```

**Pick 3 that are real and varied** (for example, one rule violation, one data error, one judgement error). Strong candidates if they happen:
- It trusted East's 75% from the dashboard. You caught it with the pod_metrics cross-check, and fixed the instruction by adding "recompute from raw data".
- It put the DM or Amazon content into a page or proposal. You caught it by reading the text after 01:44 against SANITIZER, and fixed the instruction.
- It proposed writing 210K into the sheet. You caught it against the RESOLVER rule "consult, don't edit", and fixed only the output.
- Wrong date for "the Thursday before" or "next Tuesday". You caught it with the calendar cheat-sheet.
- In C2, the first skill rewrite still let something through. You caught it with the checker in the sandbox, fixed the skill, and reran.
