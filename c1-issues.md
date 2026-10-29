# C1: issues in `bad-recap.md`

Recap: `workers/output/bad-recap.md` (Loop Athletic weekly, 15 Sep 2026). Source: `bad-recap-source.md`. "L9" is recap line 9. Times are from the transcript.

Severity: **Critical** harms the client if they read it. **High** misleads the team or risks a client commitment. **Medium** loses context. **Low** is format.

| # | Issue | Evidence | Rule broken | Severity |
|---|---|---|---|---|
| 1 | L9 and L14 ("Keep an eye on the account review risk") carry Theo's private DM about his CEO, our fees and a possible review. Recaps go to Theo's own Slack channel too. | 00:44 Lena, after Theo left at 00:42: "Pasting Theo's DM from this morning into my notes". `NOW.md`: the recap agent "posts to the client's Slack channel". | SANITIZER #2 (private), #3 (fees), #1 (opinions). Fails check questions 1 and 3. | Critical |
| 2 | Once the DM is removed, the account risk reaches no one without a "held back" note. | No `## Flags for a person` section. | SANITIZER closing rule. | High |
| 3 | GMV is retyped, and the conflict with the sheet isn't flagged: $95K vs $62K, about 53% higher. It drops Theo's "about", and his "this month" isn't the sheet's last 30 days. | 00:14 Theo: "we're at about ninety-five thousand GMV this month". Sheet: `gmv_last_30d_usd` = 62000 (2026-09-21). | RESOLVER "Where does this go?" #5, house rule #4. SANITIZER check question 2. | High |
| 4 | No action item has an owner or a due date. That includes the brief promised by Friday 2026-09-18, which Lena owns. | 00:26 to 00:30: "Brief by Friday?" "Friday works. I'll send it." 00:37, on the size chart: "Noted, we'll look into it." | RESOLVER house rule #3. | High |
| 5 | No link to 10 Sep. Theo owed the fall size chart by 11 Sep, and the recap doesn't say whether he sent it or whether it's the same issue. The try-on switch, decided on 10 Sep at 8 of 12 delivered, reads as new. | 10 Sep recap: Theo Grant, "Send the fall size chart", due 2026-09-11. "Decision: the last 4 videos move to the try-on format." | RESOLVER house rule #5. | Medium |
| 6 | No Open questions section. Open: which size-chart issue Theo means, and whether his 11 Sep action was done. | 00:33 Theo: "someone should look at the size chart issue on the product page." | RESOLVER template. | Medium |
| 7 | Frontmatter lacks `attendees` and `source`.<br>The title isn't `# Loop Athletic: weekly`.<br>`## Next steps` replaces the `## Action items` table.<br>The summary is a paragraph, not 3 to 6 bullets, with filler and Theo's claim as fact.<br>It should be `brain/knowledge/meetings/2026-09-15-loop-athletic.md`, like the 22 and 24 Sep recaps. Older recaps add a suffix (`-weekly`). | L1 to L5: only `type`, `date`, `account`.<br>L7: "# Loop Athletic weekly, 15 Sep".<br>L11: `## Next steps`.<br>L9: "Great call with Theo." "performing much better" (Theo, 00:14).<br>Saved as `workers/output/bad-recap.md`. | RESOLVER template, "Where does this go?" #4. | Low |
| 8 | Follow-up, not a recap fault: the account page doesn't list this meeting, and its focus is out of date. Change it by proposal. | `loop-athletic.md`: "creator videos for the fall collection". 00:26: "12 more, all try-on". | RESOLVER house rule #2. | Low |

## `recap_check.py` vs this review

`python extra/recap_check.py workers/output/bad-recap.md` exits with code 1: 10 FAIL, 3 WARN.

- **It caught nothing this review missed.** All its findings are in rows 1 and 7.
- **Keyword matching can't trace DM provenance.** It fails L9 on "frustrated" and "agency fees" but misses L14. "Theo's leadership may revisit the relationship in Q1" would pass and still leak the DM.
- **It doesn't compare numbers with the sheet.** The number rule only runs under `brain/`, so it skipped `$95K GMV`. A copy under `brain\knowledge\meetings\` did fail, but the checker never checks the figure against 62000.
- **There is no check for prior meetings.** It misses the open 10 Sep size-chart action and the earlier try-on decision.

## Root cause

`workers/skills/skill-recap.md` says "Include everything relevant, so nothing gets lost" (step 2) and "Include the key numbers mentioned on the call" (step 3). It never points to `RESOLVER.md` or `SANITIZER.md`, and it says "Post it" (step 5) without a check. That produces rows 1 and 3. Fix the skill.
