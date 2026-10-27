## Context

Issue #30 sets out three options: keep the intention active, add a `habituated` retirement kind, or hold habit as live state. The review on the issue argues for live state. The grounding rule already reports an active intention whose terminus has been withdrawn, so a habit kept active can be checked against its reason with no new mechanism. A retired one would need a bespoke walk. The review also raised four gaps: option 1's cost is attention, not compute; instances that already exist need a rule; occupancy splits by cue; and a reworded reason isn't visible in the projection. This change takes option 3 with no reserved occupancy, the review's "3a".

## Goals / Non-Goals

**Goals:**
- A recurring intention that no longer needs a plan stops asking for one.
- The habit stays readable as a reason: active, grounded, and reported when its ground is withdrawn.
- Declaring a habit is the person's act, and reverting is an edit.

**Non-Goals:**
- Reserving time for a habit. That's left to availability.
- Detecting a habit whose terminus has been reworded but not withdrawn. A title isn't in the projection, so this belongs to a harness reading history or the DKF claim behind `reference`.
- Any rule about when something has become habit. That's the person's judgement, which a harness may prompt.
- Habit on one-off intentions or on termini.

## Decisions

**A field, not a third `stability` value.** `tentative → firm → habit` reads like a ladder, and it would inherit the person's-act rule for free. But `stability` means reconsideration cost in resolution. Every instance and every terminus carries it, and `firmed_under` is attached to it. Habit applies only to recurring intentions, and it means "not planned", not "costly to move". A habit can still be tentative or firm about its reason. Keeping the two apart lets each mean one thing.

**`habit`, boolean, default false, omitted at default.** Its place in canonical order is immediately after `cadence`, the field it qualifies. It's in the projection, because it changes what generation and resolution do with the object. Habituating or reverting changes the version, and an acknowledgement on the recurring intention lapses as it does for any projected change.

**Recurring only.** `habit` on an intention without `cadence` is a validation error. That covers instances, which carry `occurrence` and no `cadence`, and termini, which carry neither.

**Setting is the person's act. Clearing is anyone's.** A write that changes `habit` from absent to true is refused when its `source` carries a harness. No policy authorises it. Policies authorise firming and selection, which are acts within planning, and declaring that something no longer needs a plan isn't one of them. Clearing it brings generation back and puts the instances back in view, which only adds to what the person sees. That is the same reason a harness may set an intention tentative but may not firm it.

**The check is at write time only.** On an object, `source` records the last write. A harness that later edits a habit's description would leave a harness `source` on a file whose `habit` the person set, so validation can't tell after the fact who set the field. The refusal belongs on the write that sets it. `firm` avoids this problem with `firmed_under`, but habit has no policy for an equivalent to name.

**Existing instances are left alone and are dormant.** Retiring unplaced instances as `abandoned` was the alternative. It fails on revert: an abandoned occurrence is never regenerated, so reverting would leave up to `resolver.horizon` of occurrences with no plan. It would also write a retirement that misdescribes the occurrence, which is the misdescription this change exists to avoid. Instead, an unplaced, unretired instance whose recurring intention carries `habit` is *dormant*:
- resolution refuses it, with that reason
- `unresolved` omits it
- `intention-inconsistency` doesn't count it

Grounding still applies, through `instance-of`. Habituating is one edit to one file, and reverting is the same edit undone.

**Placed instances behave as before.** A placed instance occupies time, clashes, and can be re-resolved. Whether to keep it or retire it is the person's choice, as it is for any placement. Habituation doesn't reach into placements.

**Occupancy comes from availability.** A 6am habit means the person isn't available at 6am, and availability is the format's assertion of exactly that. A habit cued by after-dinner or after-coffee has no hour to reserve at all. Reserving capacity from a habit's window would need instances that are computed but never written, which breaks the rule that instances are written to disk. That can be revisited if the cost shows up in practice.

**Lands within `intentions/0.2`.** No existing file changes meaning, and no workspace needs migrating. A reader that doesn't know `habit` ignores it, keeps generating instances, and computes a different version for an intention that carries it. That disagreement is confined to recurring intentions the person has habituated, and is accepted as the cost of not waiting for a version bump.

**Grounding is unchanged.** A habit is an active non-terminus intention, so it must reach a firm terminus of its subject. When the person sets that terminus tentative, the habit is unserved, and validation reports it at the format's level for unserved intentions: a warning under 0.1, an error under 0.2. That report is the reflection prompt. This change adds no requirement to the grounding capability. It only adds a scenario under habit that says this happens.

## Risks / Trade-offs

- [A habit lapses unnoticed, because nothing asks about it any more] → That is what a habit is. Reflection runs from the termini down, and a harness may ask about habits at whatever cadence the person likes. The format adds no expiry, consistent with "reconsideration by conflict, not sweep".
- [Other intentions get placed over a habit's hour] → Only if the person's availability still offers that hour. The README should say that a fixed-hour habit is reflected in availability.
- [Dormant instances pile up] → None are created after habituation, so at most one horizon's worth exists, and those are already past-dated or close to it. They are ordinary files the person may retire.
- [A reason that drifts without being withdrawn] → A terminus is structural, so it's more likely to be reworded in place than ended, and a reword isn't in the projection. Only withdrawal, setting the terminus tentative, reaches the grounding check. Noticing drift is a harness reading history or the DKF claim behind `reference` (see Non-Goals).

## Migration Plan

The change is additive. Existing workspaces carry no `habit`, and nothing about them changes. Archive with sync. Open an issue on intentions-cli. Close #30 with a pointer.

## Open Questions

- **When a terminus may be retired.** The current spec allows any terminus to be retired: the policy rule says "retiring it ends it". The maintainer's view is that a terminus is structural rather than assertive. Retiring one that nothing points to is harmless, but while any active intention serves it, it shouldn't be retired. It can be withdrawn by setting it tentative instead, which is the path this change's scenario uses. A refusal along those lines would also settle the 0.2 ambiguity about whether such a retirement is refused or accepted with errors. This change doesn't depend on the answer, so it belongs in a separate change (#31).
