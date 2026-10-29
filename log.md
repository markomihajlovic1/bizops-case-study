# Log
**Human:** ~1 h · **AI:** ~2 h · **Skipped:** none

**First instruction:**

```
I'm completing the attached case study. Build me an execution plan for it.

Constraints:
- Time budget: 1-4hrs
- Deliverable: one shareable artifact + a repo with all working files

The plan must include:
1. Order of work with a time estimate per question, and which questions to do first and why
2. For each question: the exact steps, the files to read, and what "done" looks like
3. Copy-paste prompts for every step where an AI helps, written so they tell the AI to inspect the files before assuming anything
4. Scripts (with code) wherever data analysis or validation is needed, and which parts should be automated vs. done by hand
5. A verification step per question, so I catch AI mistakes myself (I have to log three of them)
6. The final deliverable checklist, including what to say about time spent and skipped questions

Rules:
- Use only the material I give you in this chat. Ignore anything from earlier conversations.
- If anything is unclear or a file is missing, ask me before you write the plan, in one batch of questions.
- Be concise: tables and checklists over paragraphs, no filler.
```

**Three things the AI got wrong**
1. **A1: applied a rule too broadly.** It treated “link, don’t retype” as “never write numbers.” The call-1 recap hid 11 new affiliates and 19 posts live, which are not on RESOLVER’s performance-number list (GMV, ad spend, active affiliates, retention). Caught by: re-reading RESOLVER rule 5 against the first summary bullet. Fixed: instruction. Added “ONLY those four are performance numbers; state every other count as said.”
2. **B3: left the decisive stakeholder out of the plan.** The week plan for Marcus ignored Priya (Head of Ops), who had proposed counting emailed summaries as recaps. Without her agreement, his pushback (“Priya said emails count”) wins by default. It also wrote East’s first week as 7 of 8; it was 8 of 8. Caught by: reading the Slack thread and `metrics-raw.md` against the plan. Fixed: output only. Added a Monday step to agree the definition with Priya first, and corrected the number.
3. **C2: the skill rewrite would have broken its own test.** Step 11 told the agent to run `extra/recap_check.py`, but the fresh session sees only the skill, the brain and the transcript, so that file is not there. Caught by: comparing the skill’s steps with what the rerun folder contains. Fixed: instruction. Made the step conditional, with the self-check as the fallback, then reran. The rerun fixed every C1 issue on the first clean run.
