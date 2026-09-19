## Context

`SPEC-FEEDBACK.md` in intentions-cli is the authoritative record of what implementing the text forced the tool to decide. Its status table carries one row per issue with a status of adopted, settled with an addition, adopted with refinements, decided differently, or open. As of 2026-09-20: 25 rows; #5, #6, #8, #9 and #24 decided differently; #23 open. The README and the site were written against the thirteen-row table of 2026-09-06 and never updated when rows 14 to 25 arrived.

## Goals / Non-Goals

**Goals:**
- Both passages true against the feedback file today, with the file named as the source.
- A cheap way to notice the next drift.

**Non-Goals:**
- Answering #23. That is its own change.
- Automating the count into the page. The site has no build step by design.

## Decisions

**Say the counts, name the source, name the open one.** The paragraph becomes: a first implementation, intentions-cli (now v0.11.0), was written from this text and has raised twenty-five issues where it was ambiguous or silent, recorded in its `SPEC-FEEDBACK.md`; twenty-four are settled in the text as it now stands, five of them differently from what the implementation chose, and one, a reference tool set for harnesses, is open. Naming the open issue is honest and also tells a reader what is still moving.

**The site says the same thing with fewer words.** The proof lead keeps its shape and swaps the numbers, and "raised" becomes "has raised" so it reads as an ongoing record. The feedback file is linked from the lead.

**A requirement, not a script.** The `landing-site` spec already requires the page to be read against the README before publication. Adding a requirement that the second-reader counts agree with the feedback file makes the tally part of that read. The tally is one line, recorded here so it is not reinvented:

```
grep -c -E '^\| [0-9]+ \|' SPEC-FEEDBACK.md            # rows
grep -E '^\| [0-9]+ \|' SPEC-FEEDBACK.md | grep -c 'decided differently'
grep -E '^\| [0-9]+ \|' SPEC-FEEDBACK.md | grep -c '| open,'
```

**"Settled" counts everything that is not open.** Adopted, settled with an addition, adopted with refinements and decided differently are all settled in the text. The README's existing phrasing already uses "settled" this way.

## Risks / Trade-offs

- [The numbers drift again before anyone reads them] → The requirement and the tally make the check a thirty-second step in any site edit; the site is edited rarely and the numbers change rarely.
- [Naming the open issue dates the paragraph] → It already carries a version number. Dating is the point.

## Migration Plan

Prose only. Commit, push, Pages rebuilds, archive with sync.

## Open Questions

None.
