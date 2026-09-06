## 1. Validate the change

- [x] 1.1 Run `openspec validate --changes`; confirm every MODIFIED header resolves against the main specs
- [x] 1.2 Confirm the four additions (#14 one horizon, #17 ranged fallback, #20 subject test, #22 commitment cancellation) each have a scenario the implementation's reading would fail

## 2. README: resolution and consistency (#14, #16, #17, #19, #22)

- [x] 2.1 RESOLUTION record: add `supply` after `displaced` in the example and prose; say it is what the selector saw, not what the placement rests on
- [x] 2.2 Resolution lifecycle diagram: add the range, the grid, and the ranged-duration fallback; note that a replacing selection cancels a live commitment
- [x] 2.3 Resolution preconditions paragraph: a placed intention is refused unless replacing; state what replacing does
- [x] 2.4 Consistency flag table: `intention-inconsistency` says pairwise; add a rests-on paragraph after the transparency paragraph
- [x] 2.5 Design Principles: a sentence under "Flags, never decisions" or a new principle that resolution is a function of workspace, configuration, and now

## 3. README: availability, window, intention (#15, #18, #20, #21)

- [x] 3.1 AVAILABILITY prose: capacity is consumed per occasion, placement and commitment count once, transparent consumes nothing
- [x] 3.2 AVAILABILITY scope: `personal` visible only to its subject's or a party's resolution; `resolver.scope` as ceiling
- [x] 3.3 WINDOW relational anchor: the four-row bounds table, absent gap semantics, retired or cancelled target blocks
- [x] 3.4 INTENTION instances paragraph: `location` in the copied list; window is the occurrence plus the recurring intention's clock

## 4. README: configuration

- [x] 4.1 `intentions.yaml`: replace `generation.horizon` with `resolver.horizon`; add `step` and `scope` as optional; prose on stale keys
- [x] 4.2 Instance generation text: horizon is `resolver.horizon`

## 5. Archive and close out

- [x] 5.1 Archive with sync so the six deltas land in the main specs
- [x] 5.2 Commit and push the intentions repo, one close keyword per issue number
- [x] 5.3 Close #14 to #22 with a comment naming the commit; on #14, #17, #20, #22 say what was added to the implementation's choice
- [x] 5.4 Knowledge workspace: claims for the function principle, the subject test, and the re-selection rule; one synthesis; open list carried forward; commit and push
