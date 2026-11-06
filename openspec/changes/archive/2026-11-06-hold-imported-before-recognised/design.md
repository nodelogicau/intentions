## Context

Issue #36. `hold-placed-intentions` (#34) gave a placed intention with no `parties` an optional `external`, the link to the busy hold a harness writes for its placement. Two rules keep a hold from becoming a commitment: on import, an event matching any intention's `external`, retired or not, creates no commitment; and validation reports two *intentions* carrying the same `system` and `uid` as an error.

Neither rule covers an intention and a commitment that share a link. There are three ways to get there:

- A harness wrote holds before the field existed, imported them as commitments, and later records the UID on the intention.
- An importer older than the recognition check imports a hold.
- Two branches merge: one sets `external` on the intention, the other imports the event.

In each case the commitment has `origin: import`, the subject as its only party, and the hold's `uid`. It overlaps the intention's placement, so `check` reports a `window-clash` on both, and nothing says why. intentions-cli v0.17.0 reports the three hold errors and nothing for this case.

## Goals / Non-Goals

**Goals:**
- Validation finds an intention and a commitment linked to one external event and names both.
- The finding tells the person how to fix each possible cause.
- No hash moves and no format version.

**Non-Goals:**
- Fixing it automatically.
- Changing `window-clash`, or the import rule.
- Modelling events imported from someone else, which is #35.

## Decisions

**Warning, not error.** The data is still well-formed. Every reference resolves, and each object passes validation on its own. What the UID match says about the two objects is a judgement only the person can make: usually the commitment is the intention's own hold, but it may be a real event that shares the UID. An error would make CI fail on a workspace that the person may decide is correct. This matches the other warnings, such as an end that was abandoned, or a selection made under a policy that has since been withdrawn. Alternative considered: an error, matching the error for two intentions sharing a link. Rejected: two intentions sharing a link always means a harness bug, because each hold is a separate event the harness wrote. A commitment's UID comes from outside, so a shared UID is less clear-cut.

**Only unretired commitments.** A commitment retired as `cancelled` occupies no time and causes no clash. It is also what the fix leaves behind, so it must not keep the warning alive.

**Any intention, retired or not.** This matches the import rule, which recognises a hold whether or not its intention is retired. Retirement keeps `external`, and a fulfilled intention's hold stays in the calendar, so an unretired duplicate commitment is still stale. A retired intention can't be edited, so for one, only the first fix applies.

**Fixes named in the finding.** The warning names the intention, the commitment, the shared `system` and `uid`, and two fixes:
1. If the commitment is the intention's own hold imported before it was recognised, retire the commitment as `cancelled`. An imported commitment carries no `intention`, so cancelling it clears no placement, and the intention is untouched.
2. If it is a real event that shares the UID, clear the intention's `external` (on an unretired intention). The harness then writes a new hold.

The second fix covers the case #35 raises, where a person points an intention at someone else's event (a venue's ticket invite). Whatever #35 decides, this warning is what tells the person the two objects need reconciling.

**One finding per pair.** A recurring imported event gives several commitments sharing one `uid`. Each that matches is reported with the intention. A hold is never recurring, so several matches suggest the second fix. The finding doesn't need to say so; the list of commitments shows it.

**Write time.** A write that sets `external` to a UID that an unretired commitment already carries can see the warning in advance. Under Validation's existing rule, it accepts the write and reports the warning in its result. No new refusal.

**Where the text lives.** The finding goes in object-model's Validation list of warnings, with a scenario. Calendar hold in intention gains a sentence after the import rule saying that recognition prevents the case from now on and validation finds earlier cases, with a scenario of its own. Consistency is unchanged: the `window-clash` stays until the person acts or acknowledges it.

## Risks / Trade-offs

- [A warning can be ignored, and the clash stays] → The clash is still reported by `check` too, so the person sees two findings pointing at the same pair. That's enough of a nudge for a problem that comes from the past.
- [Older readers report nothing] → They keep reporting the bare `window-clash`, as today. Nothing breaks.
- [A person cancels a real event by mistake] → The finding offers both fixes, and cancelling is the person's act. A cancelled commitment is retired, not deleted, so the record remains.

## Migration Plan

None. Only validation changes; no hash moves and no workspace needs migrating. intentions-cli adds the warning to `validate`, and adds it to the result of a write that sets `external`.

## Open Questions

None.
