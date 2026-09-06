## Context

This morning's thirteen issues were about files and hashes: two writers producing the same bytes. This afternoon's nine are about operations: two resolvers producing the same candidates and two checkers producing the same flags. The README had committed to the first kind of agreement and only gestured at the second. Every item here is a place where the text said "resolution produces" or "the check surfaces" without saying how.

## Goals / Non-Goals

**Goals:**
- Resolution is a pure function of the workspace, `intentions.yaml`, and the resolver's `now`. Two conformant implementations produce the same ranked candidate set.
- Consistency is likewise a function of the workspace and `now`.
- Every act that changes a placement or a party status remains a person's act or their policy's.

**Non-Goals:**
- Global feasibility across all intentions. Pairwise is the commitment.
- Optimising placements across several intentions at once. Resolution takes one intention.
- Declaring v0.1.

## Decisions

**Resolution is a function, and the design says so.** The step grid and the range rule together make the candidate set finite and determined. Without stating the principle, the next reader will treat enumeration as an implementation detail again. So: given the workspace, the configuration, and `now`, the candidate set and its order are fixed; `now` comes from the clock or an override on the call, which is what makes the function testable.

**One planning horizon.** The implementation proposed `resolver.horizon` beside the existing `generation.horizon`. They are one idea: how far ahead the workspace plans. Two keys would drift, and a resolution horizon longer than the generation horizon would rank candidates against instances that do not exist yet. `resolver.horizon` replaces `generation.horizon`, default four weeks, used by both.

**Candidates start on a grid aligned to supply.** `resolver.step`, default `PT15M`, aligned to each supply interval's start rather than to the hour, so that a capacity starting at 09:10 offers 09:10 first. The alternative, a global clock grid, would waste the first minutes of every oddly-aligned capacity. A ranged duration tries the nominal, and if nothing at all is found, the longest shorter duration down to `min` on the same grid. The implementation tried the nominal only, which makes ranges decoration, and the format's rule is that anything stored bears on resolution or is prose.

**Capacity is consumed.** "Capacity per occasion" already meant this; the text only said "length". An occasion offers its nominal (the `max` when ranged) less the opaque, unretired placements resting on it. A placement and its commitment are one placement. Transparent commitments consume nothing, consistently with the transparency change.

**Rests-on is recomputed; the record remembers what was chosen against.** Storing supply on the placement would go stale as availability changes, and flags are recomputed by design. So at check time a placement rests on every containing occasion of each involved particular, and the failures are reported by kind: no containing occasion is a `window-clash` without counterpart; containing occasions that all fail report why. Separately, the RESOLUTION record gains `supply`, the availability ids the selection was chosen against, sorted, outside the projection. This is provenance of the same kind as `firmed_under`: what the selector saw, in the file. It is not what the placement rests on now.

**Pairwise inconsistency.** Global feasibility is a scheduling problem, not a check. Pairwise, over active unplaced intentions of one subject with both duration and window whose ranges intersect: each has candidates alone but no non-overlapping pair exists. The flag's detail says so.

**Personal scope has a subject.** The visibility rule as written, "at or wider than the resolver's scope", would let a resolver acting for Ada use Rob's `personal` availability in an organisation workspace. Scope is a lattice, but `personal` is also an owner. The rule becomes: `personal` availability is visible only when its subject is the intention's subject or one of its parties; `organisation` and `public` are visible to any resolver at or below that scope. `resolver.scope` is kept as the implementation proposed, default `personal`, as a ceiling for tools that should see less.

**Re-selection cancels the commitment.** The implementation's `--replace` clears the placement and writes a new record, which is right. What it leaves unsaid is the commitment. A commitment's placement is in its projection and its parties accepted that placement; moving it under them would change what they accepted without their act, which the party-status rule forbids. So re-selection on an intention with a live commitment cancels it, with the new resolution's id as the reason, and creates a fresh commitment with every party tentative. The old record and the cancelled commitment remain as history.

**Instances inherit place and hours.** `location` joins the copied list, and the instance window is the occurrence day plus the recurring intention's `clock`. A Tuesday-mornings arrangement whose instances lost their mornings would surprise, and a place constraint that vanished on generation would too.

**Relation bounds are a table.** Four rows, one per relation, each bounding the candidate's start or end by the target's start or end plus `min` and `max`. An absent gap is zero to unbounded; an absent `max` is unbounded above. A retired or cancelled target counts as unplaced and blocks the dependent intention.

## Risks / Trade-offs

- [Removing `generation.horizon` breaks an existing `intentions.yaml`] → Same treatment as `week_start`: ignored and reported at info level; pre-v0.1.
- [A fifteen-minute grid may miss a fit that a finer grid would find] → The step is configurable, and aligning to supply start removes the commonest miss. A finer default costs enumeration on every long window.
- [Pairwise misses three-way infeasibility] → Stated as out of scope; the flag's detail names the pair so a person can see the pattern.
- [Cancelling a commitment on re-selection is heavier than moving it] → It is the only option consistent with party status being that party's act. The cost is visible in the file, which is the point.
- [`supply` on the record could be read as what the placement rests on now] → The spec says it is what the selection was chosen against, and the rests-on rule is separately stated.
