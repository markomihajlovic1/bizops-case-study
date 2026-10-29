# C2: recap before and after the skill fix

## 1. How the rerun was done

- I opened a fresh Cursor window on a folder holding only `brain/`, `workers/skills/skill-recap.md` and the transcript, renamed to `inbox/2026-09-15-loop-athletic-call.md`.
- Prompt, verbatim: "Please write the meeting recap for inbox/2026-09-15-loop-athletic-call.md by following the steps in workers/skills/skill-recap.md. Use only the files in this folder."
- The provider's safety filter blocked the first attempt because of the folder name. After I renamed the folder, the rerun went through.

## 2. Skill

v1 (`workers/skills/skill-recap.v1.md`), in full:

```markdown
---
type: skill
step: recap
owner: Brightline ops
updated: 2026-09-01
---

# Skill: recap a client call

You turn a recorded client call into a recap for the brain.

## Input
The transcript of one call.

## Output
A file in `brain/knowledge/meetings/`.

## Steps
1. Read the whole transcript.
2. Write a summary of the call. Include everything relevant, so nothing gets lost.
3. Include the key numbers mentioned on the call, so the team has them handy.
4. List the next steps.
5. Post it.
```

v2 is `workers/skills/skill-recap.md`, with 13 steps. This is how its steps map to the C1 issues:

| C1 row | v2 step that prevents it |
|---|---|
| 1. Private DM leaked, posted to the client's Slack | 3 (stop when the last client attendee leaves), 4 (leave out DMs, opinions and fees, and don't hint at them or turn them into a risk or action), 9 (self-check) |
| 2. No "held back" note | 8 (Flags: "Something from this call was held back under SANITIZER") |
| 3. GMV typed, conflict not flagged | 5 (never type it, compare it with the sheet, flag differences in value or period) |
| 4. No owner or due date | 6 (one owner, a `YYYY-MM-DD` date computed from the call's weekday, otherwise Open questions) |
| 5. Earlier meeting not linked | 2 (read prior recaps and open actions), 7 (link them and say whether each action was closed) |
| 6. No Open questions | 6, 7, 8 (the section is required, and unowned or unmentioned items go in it) |
| 7. Template, name and location | 8 (exact template), 10 (path and name), 11 (checker) |
| 8. Account page not updated | 12 (propose in `proposed-changes.md`, don't edit) |

## 3. Recap before and after

Before (`workers/output/bad-recap.md`):

```markdown
---
type: meeting
date: 2026-09-15
account: loop-athletic
---

# Loop Athletic weekly, 15 Sep

Great call with Theo. All 12 fall videos were delivered and the try-on format is performing much better. Loop Athletic is at $95K GMV this month. Theo wants 12 more videos for October, all try-on. There's a size chart issue on the product page. Theo's CEO is frustrated with the agency fees and might put us up for review in Q1.

## Next steps
- Send the October brief
- Look into the size chart issue
- Keep an eye on the account review risk
```

After (`workers/output/after/2026-09-15-loop-athletic.md`):

```markdown
---
type: meeting
date: 2026-09-15
account: loop-athletic
attendees: [Theo Grant, Lena Varga]
source: inbox/2026-09-15-loop-athletic-call.md
---

# Loop Athletic: weekly

## Summary
- Lena says all 12 fall collection creator videos are delivered, and the last 4 use the try-on format decided on 2026-09-10 ([recap](2026-09-10-loop-athletic-weekly.md)). This closes Lena's action from that call to brief creators on the try-on format.
- Theo says the try-on videos are performing much better, and that GMV this month shows the content is working ([sheet](../reference/accounts-sheet.csv)).
- Decision: an October batch of 12 more videos, all in the try-on format. This continues Theo's preference for try-on content, first raised on 2026-09-10 ([recap](2026-09-10-loop-athletic-weekly.md)).
- Theo raised a size chart issue on the product page. No owner or date was set (see Open questions).

## Action items
| Owner | Action | Due |
|---|---|---|
| Lena Varga | Send the brief for the October batch of 12 try-on videos | 2026-09-18 |

## Open questions
- Size chart issue on the product page: Theo asked that someone look at it, and Lena said "we'll look into it." There is no single owner and no due date. Who owns it, and by when?
- Theo's action from 2026-09-10 to send the fall size chart (due 2026-09-11) was not mentioned on this call ([recap](2026-09-10-loop-athletic-weekly.md)). Has it been sent?

## Flags for a person
- GMV: at 00:14 Theo stated a GMV figure for "this month." It differs from the sheet column `gmv_last_30d_usd`, both in value and in period (this month vs last 30 days). The number was not copied and the sheet is unchanged.
- Something from this call was held back under SANITIZER. Ask Lena Varga.
```

## 4. Result

| C1 row | Fixed? | Evidence from the after recap |
|---|---|---|
| 1. Private DM leaked | Yes | No line mentions the CEO, fees or a review. The last call content used is the size chart (00:33). |
| 2. No "held back" note | Yes | "Something from this call was held back under SANITIZER. Ask Lena Varga." |
| 3. GMV typed, not flagged | Yes, with the gap in section 5 | "It differs from the sheet column `gmv_last_30d_usd`, both in value and in period... The number was not copied and the sheet is unchanged." |
| 4. No owner or due date | Yes | "Lena Varga, Send the brief for the October batch of 12 try-on videos, 2026-09-18". The size chart item went to Open questions. |
| 5. Earlier meeting not linked | Yes | "`the last 4 use the try-on format decided on 2026-09-10 ([recap](2026-09-10-loop-athletic-weekly.md))`" |
| 6. No Open questions | Partly | "Theo's action from 2026-09-10 to send the fall size chart (due 2026-09-11) was not mentioned on this call... Has it been sent?" It doesn't ask which size-chart issue Theo means, or whether it's the same one. |
| 7. Template, name and location | Yes | Full frontmatter, `# Loop Athletic: weekly`, the four sections, 4 summary bullets, named `2026-09-15-loop-athletic.md`. |
| 8. Account page not updated | Yes | `workers/output/after/proposed-changes.md` proposes adding the 2026-09-15 meeting and the new focus, with Lena Varga (West pod lead) as approver. |

Checker (`extra/recap_check.py`): before, 10 FAIL and 3 WARN. After, PASS, run in place under `brain/knowledge/meetings/`.

## 5. Remaining gap

Summary bullet 2 puts a sheet link next to Theo's GMV claim, which reads as if the sheet supports it.
