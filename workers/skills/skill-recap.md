---
type: skill
step: recap
owner: Brightline ops
updated: 2026-09-24
---

# Skill: recap a client call

You turn one recorded client call into a recap for the brain. The recap is posted to the client's Slack channel, and anyone in the brain can read it, including the people named in it. Write every line as if the client is reading it.

## Input
The transcript of one call, in `inbox/`.

## Output
One recap at `brain/knowledge/meetings/YYYY-MM-DD-<slug>.md`, plus proposals for any account or people page changes.

## Steps
1. **Read the rules.** Read `brain/RESOLVER.md` and `brain/SANITIZER.md` in full. Where this skill and they differ, they win.
2. **Read the account's history.** In `brain/knowledge/reference/accounts-sheet.csv`, find the account's row (`account` is the slug). Read `brain/knowledge/accounts/<slug>.md` and every recap in `brain/knowledge/meetings/` whose name contains the slug, oldest first. Older names may have a suffix after the slug. Note their decisions, and every action item still open on the call date.
3. **Find the cut-off.** Use the transcript only up to the line where the last client attendee leaves, such as `[<name> left the call]`. Nothing after that line goes in, even if the recording continues.
4. **Leave out private and banned content, even before the cut-off.** That means anything quoted or pasted from a DM, chat or email, and anything marked "between us" or off the record. It also means opinions about people (write what happened, with a date), our fees, margins and rates, and personal data. Don't paraphrase or hint at what you left out, and don't turn it into a risk, a next step or an action. Targets, budgets and rates the client agrees to are decisions: record them as said.
5. **Never type performance numbers.** GMV, ad spend, active affiliates and retention are not typed. Name the metric and link `[sheet](../reference/accounts-sheet.csv)`. If the call states one, compare it with the sheet column. If the value differs, or the call's period differs from the column's (for example "this month" vs last 30 days), add a Flags line. Name the metric, the timestamp and the column, and say that the number was not copied and the sheet is unchanged. Never edit the sheet. State every other count (videos, posts, creators) as said.
6. **Action items need one owner and an absolute date.** Each row has one named person, who either said they would do it or was assigned it, and a due date as `YYYY-MM-DD`. Compute relative dates from the frontmatter date:
   - Work out the call's weekday first.
   - "Today" is the call date, and "tomorrow" is one day later.
   - A named weekday ("by Friday", "next Tuesday") is the first one after the call date. If that reading is doubtful, use it and add an Open question to confirm it.
   - Check that the due date is on or after the call date.
   If there is no single owner ("we", "someone", "the team") or no stated deadline, the item is not an action row. Put it in Open questions and say what is missing.
7. **Link earlier meetings.** If something was already said, decided or assigned in an earlier recap, say so and link it, for example `([recap](YYYY-MM-DD-<slug>.md))`. Don't present it as new. For each open action from step 2, say whether this call closed it. If the call didn't mention it, add an Open question.
8. **Write the recap in the RESOLVER template, exactly.**
   - Frontmatter: `type: meeting`, `date` (the call date), `account` (the sheet slug), `attendees` (from the transcript), `source: inbox/<transcript file>`.
   - Title: `# <Brand>: <meeting name>`.
   - Sections: `## Summary`, `## Action items`, `## Open questions`, `## Flags for a person`, with these names and in this order. Write "None." in an empty section.
   - Summary: 3 to 6 bullets of facts, decisions and what the client told us. Attribute claims ("<name> says ..."). No filler ("great call").
   - Action items: a `| Owner | Action | Due |` table.
   - Flags for a person: every sheet conflict from step 5. If you left anything out in step 3 or 4, write only "Something from this call was held back under SANITIZER. Ask <account manager from the sheet>." Otherwise write "Nothing held back under SANITIZER on this call."
9. **Self-check before saving.** Ask SANITIZER's three questions of every line. Then confirm each of these:
   - Nothing comes from after the cut-off or from a DM, even reworded.
   - No performance number is typed, and every one stated on the call was compared with the sheet and flagged if it differs.
   - Every action row has one owner and a `YYYY-MM-DD` date on or after the call date. Everything else is in Open questions.
   - Every open item from earlier recaps is closed, linked, or an Open question.
   - The frontmatter, title, sections, path and file name match steps 8 and 10.
   Fix anything that fails before you go on.
10. **Save** to `brain/knowledge/meetings/YYYY-MM-DD-<slug>.md`. Use the call date and the sheet slug, with no suffix. Save it nowhere else.
11. **Run the checker if there is one.** If `extra/recap_check.py` exists, run it on the saved file (`python extra/recap_check.py <saved file>`), fix every FAIL and read every WARN. If it doesn't exist, step 9 is the check. Its number rule only runs under `brain/`. It only matches keywords and never sees the transcript, so passing it doesn't replace step 9.
12. **Propose page changes. Don't make them.** If the call changes an account or person page (a meeting to list, a new focus, a new contact), add a row to `proposed-changes.md` with the file, the current text, the proposed text, the source, and the approver (the pod lead in `brain/NOW.md`). Create `proposed-changes.md` in the repo root if it doesn't exist.
13. **Post** the recap only after steps 9 and 11 pass.
