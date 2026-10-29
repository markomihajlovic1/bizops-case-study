# Recap agent pipeline fixes

**Problem:** Recaps reach clients unchecked, late or never.

## Asks
1. Cut transcripts at last client exit (Meet participant events).
2. Draft to the AM within 15 min. Client Slack only after `recap_check.py` passes and AM approves.
3. Retry failures; alert AM if no draft by 30 min.
4. Capture WhatsApp calls.

## Evidence
1. c084: client left 00:42; 00:44 DM stayed.
2. Agent median 65 min; 29/59 within 60; South 0/34 under 30. c084 failed 10 checks yet counted on time (55 min). Marcus: "if it posted in 10-15 min I'd use it".
3. c117, c140: recorded, never posted.
4. 26/30 West calls unrecorded; West: 10%.

## Done when (one week)
Nothing after client exit; no FAIL posted; 90% drafted within 15 min; every recorded call recapped or alerted.
