## Why

A person's understanding of who they are is refined over time, and one of the commonest refinements is finding that one self was really two: *being someone who looks after their health* turns out to be *being someone who is strong in old age* and *being someone with a calm mind*. The format can't record that today. A terminus's `superseded_by` names one terminus, so the person must either retire the old self as `abandoned`, which says it was dropped when it was differentiated, or supersede it by one successor, which is half true and drops the link to the other. Supersession is already the way a reason evolves. This change lets it say what actually happened.

## What Changes

- **A terminus may be superseded by several termini.** On a terminus only, `superseded_by` MAY be a list of two or more distinct termini of the same subject, each firm or tentative, as a single successor may be now. A single successor stays a single id. Desires, availability and intentions that are not termini keep a single `superseded_by`.
- **The walk follows every successor.** At a link to a terminus superseded by a list, the grounding walk continues at each successor and grounds if any of them grounds. The existing rule that a walk revisiting an intention through `superseded_by` ends without grounding applies on each branch.
- **Retiring a terminus into a split is accepted when any successor is firm.** The retirement refusal is computed by the walk, so it follows from the walk change: a split whose successors include a firm terminus leaves every dependent grounded.
- **A dependent still resting on a split terminus is reported at info level.** The list keeps dependents grounded, but it doesn't say which successor each one is for. Validation names each unretired intention whose `serves` targets a terminus superseded by a list, with the fix: re-point it to the successor or successors it is for. It is information, not a warning, because a dependent may honestly serve both.
- **Validation errors** for a list on anything but a terminus, a list with fewer than two entries or a repeated entry, and any entry that is not a terminus of the same subject.
- **Readers must be upgraded before anyone splits.** `superseded_by` is outside the projection, so no version changes. But a reader that predates this change expects a single id, so the Status paragraph adds this to the upgrade notes already there for `habit` and `external`.

Non-goals: deepening, where a terminus is found to serve a deeper self. A terminus stays a sink. Deepening is recorded as supersession, with the earlier wording kept in the retirement `reason` or in a DKF claim. Exploratory or inquiry termini need no special kind: they are early termini, refined by supersession like any other.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: the grounding walk follows each successor of a terminus superseded by a list. Retiring a terminus admits a list of successors.
- `object-model`: the retirement record admits a list-valued `superseded_by` on a terminus. Validation gains the list errors and the info finding for dependents of a split terminus.
- `harness-tools`: `intention_retire` accepts a list for `superseded_by` on a terminus and refuses one elsewhere.

## Impact

- README: the terminus retirement paragraph, Records/RETIREMENT (the example and the `superseded_by` rule), the serves-graph walk paragraph, Validation, the Reference Tool Set table and the `intention_retire` bullet, and the Status upgrade note.
- Lands within the `intentions/0.2` draft. No projection change and no file break for workspaces that don't split. `docs/example` holds no retired termini and needs no changes.
- intentions-cli: list parsing on a terminus's `superseded_by`, the branching walk, the new validation errors and info finding, a repeatable `--superseded-by` on `intention retire`, and the skill's "A reason changes by supersession" rule gaining the split case.
