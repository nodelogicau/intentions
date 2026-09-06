## Why

The implementation raised nine more issues (nodelogicau/intentions #14 to #22) this afternoon, all of one kind: the README describes resolution and consistency as operations with a ranking and a set of flag kinds, but not as functions. Two implementations reading the same workspace would enumerate different candidates, deplete capacity differently, compute different flags, and disagree on what re-selection does. This change makes resolution a pure function of the workspace, the configuration, and the resolver's clock, and closes the nine gaps so that v0.1 can be declared with the operations pinned as tightly as the objects.

## What Changes

- **Resolution is a function.** Given the workspace, `intentions.yaml`, and a `now`, the candidate set and its ranking are fully determined. The design says so explicitly, so later feedback is judged against it.
- **A bounded range** (#14): candidates lie between the later of the window's start and now, and the earlier of the window's end and now plus `resolver.horizon`. Open sides contribute nothing. Nothing before now is offered. `generation.horizon` is replaced by `resolver.horizon`, one planning horizon for both generation and resolution. **BREAKING** for `intentions.yaml`.
- **A step grid** (#17): candidate starts lie on `resolver.step`, default fifteen minutes, aligned to each supply interval's start. A ranged duration tries the nominal first and then the longest shorter duration down to `min` that yields a candidate, so ranges are not decoration.
- **Capacity depletes per occasion** (#15): an occasion offers its nominal duration, less the opaque placements already resting on it. An intention's placement and the commitment it produced count once.
- **What a placement rests on is recomputed** (#16), and the RESOLUTION record gains `supply`, the availabilities the selection was chosen against, outside the projection.
- **Relation bounds** (#18) are tabled per relation; an absent gap is zero to unbounded; a retired or cancelled target is unplaced.
- **`intention-inconsistency` is pairwise** (#19).
- **Scope has a subject test** (#20): `personal` availability is visible only when its subject is the intention's subject or one of its parties; `resolver.scope` is a ceiling, default `personal`.
- **Instances copy `location` and the clock anchor** (#21).
- **Re-selection replaces** (#22): selecting for a placed intention is an explicit replace that clears the placement, writes the new one, and adds a new record. A live commitment from the old placement is cancelled and a fresh one created with every party tentative, because a placement its parties accepted cannot change under them.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `resolution`: the range, the grid, ranged durations, depletion in eligibility, the subject test, `supply` on the record, and re-selection.
- `consistency`: pairwise inconsistency and the rests-on rule.
- `availability`: capacity consumed per occasion, and the scope visibility rule.
- `temporal-primitives`: relation bounds per relation.
- `intention`: instances copy `location` and `clock`; generation uses `resolver.horizon`.
- `object-model`: `resolver.horizon`, `resolver.step`, `resolver.scope`; `generation.horizon` removed.

## Impact

- Six spec files. README sections: AVAILABILITY prose, WINDOW relational anchor, RESOLUTION record and lifecycle diagram, Consistency flag table, INTENTION instances paragraph, `intentions.yaml`, and Design Principles, which gain a sentence on resolution being a function.
- Four issues are answered with an addition to what the implementation chose (#14 one horizon key, #17 ranged durations, #20 the subject test, #22 the commitment consequence); the close comments should say so.
- v0.1 is still not declared here. After this lands, nothing known stands between the text and the declaration.
- The knowledge workspace needs one synthesis after archive.
