## 1. Validate the change

- [x] 1.1 Run `openspec validate --changes`; confirm the two RENAMED headers match the intention spec exactly and every MODIFIED header resolves
- [x] 1.2 Re-read the four differing decisions (#5, #6, #8, #9) against the design and confirm each has a scenario that fails under the implementation's reading

## 2. README: normalisation and files (#1, #2, #3, #7, #12, #13)

- [x] 2.1 Versioning: replace the normalisation parenthesis with the full rule list; state that booleans equal to their default are omitted; state that `version` is always written after `id`
- [x] 2.2 Field order: add `version` after `id`, the list-style rule, and the boolean-omission rule
- [x] 2.3 Values, DURATION: `P0D` is the one form of zero
- [x] 2.4 Examples: add a `version:` line after `id:` to the intention, availability, commitment, and resolution examples; remove `transparent: false` from the commitment example; write `conditional` as a block sequence
- [x] 2.5 Field tables: add a `version` row after `id` to the intention, availability, and commitment tables, and to the resolution record's field list

## 3. README: time (#4, #5, #6, #10)

- [x] 3.1 WINDOW: drop `resolver.week_start` from the resolver context sentence; say weeks are ISO weeks in every context; add `resolver.hemisphere` for neutral seasons
- [x] 3.2 Calendar anchor table: add the hemisphere-specific season rows and the month mapping
- [x] 3.3 Deixis paragraph: the vocabulary a writer recognises, the resolver-timezone rule, and the Sunday note
- [x] 3.4 Cadence: the seed, the calendar-anchor requirement, and `WKST` default
- [x] 3.5 `intentions.yaml`: remove `week_start`, add optional `hemisphere`; adjust the Design Principles sentence that mentions week start

## 4. README: intention (#8, #9, #11)

- [x] 4.1 INTENTION field table and example: add `firmed_under` after `stability`; `auto_select`/`auto_firm` become "termini only"
- [x] 4.2 Stability paragraph: `firmed_under` rule
- [x] 4.3 Rename throughout: cadenced kind is "recurring intention"; "standing intention" survives only where it means a terminus; policies are termini. Covers the Approach section, field table, serves-graph and instances paragraphs, Policies paragraph, RESOLUTION `selector` text, the object-model and lifecycle diagrams, and Design Principles
- [x] 4.4 Validation list: `firm` with a harness source and no `firmed_under`; `firmed_under` not naming an active policy of the subject; conditions on a non-terminus; `cadence` without a calendar anchor

## 5. Status, archive, and close out

- [x] 5.1 Status: record that a first implementation exists and that its thirteen issues are settled here; leave v0.1 undeclared
- [x] 5.2 Archive with sync so the six deltas land in the main specs
- [x] 5.3 Commit and push the intentions repo
- [x] 5.4 Close issues #1 to #13 with a comment naming the commit; on #5, #6, #8, #9 say how the answer differs from what the implementation chose
- [x] 5.5 Knowledge workspace: one synthesis on Philosophy of Calendaring recording the thirteen settlements, citing the four differing decisions with their reasoning; carry the open list forward with item 7 updated to "condition met, v0.1 awaiting declaration"; commit and push
