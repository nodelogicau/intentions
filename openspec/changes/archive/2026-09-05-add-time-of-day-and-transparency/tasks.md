## 1. Validate the change

- [x] 1.1 Run `openspec validate --changes` and confirm every MODIFIED header matches the main spec exactly
- [x] 1.2 Check the availability delta against the temporal-primitives delta so `clock` semantics are stated once and referenced, not restated differently

## 2. README: time of day

- [x] 2.1 WINDOW section: add `clock` beside `calendar` and `relative` in the example and prose, with the resolver-timezone, exclusive-end, and midnight-crossing rules
- [x] 2.2 Cadence section: state that `BYHOUR`, `BYMINUTE`, and `BYSECOND` are not admitted and why
- [x] 2.3 Availability example: add `clock: 09:00/12:00` to "Tuesday mornings for deep work" and mention that `duration` may be shorter than the interval
- [x] 2.4 Resolution lifecycle diagram and supply bullet: note that candidates lie within every clock interval present
- [x] 2.5 Validation list: add sub-day RRULE parts and a fractional all-day duration as errors

## 3. README: transparency and all-day

- [x] 3.1 PLACEMENT section: `start` may be a calendar day; all-day rules; resolution writes datetimes only
- [x] 3.2 COMMITMENT field table and example: add `transparent` after `origin`; add it to the scheduling projection line
- [x] 3.3 COMMITMENT "External reference only" paragraph: add the `TRANSP`, `freeBusyStatus`, `DATE`, and `showWithoutTime` mappings
- [x] 3.4 Consistency section: after the flag table, state that a transparent commitment is exempt from the four supply and overlap kinds and why
- [x] 3.5 Resolution ranking: overlap with a transparent commitment is not displacement
- [x] 3.6 Validation list: `transparent` on a resolution-born commitment is an error
- [x] 3.7 Versioning: note that the projection field sets changed before v0.1 and no format bump follows

## 4. Archive and record

- [x] 4.1 Archive with sync so the five deltas land in the main specs
- [x] 4.2 In the knowledge workspace, assert one claim per settled point quoting the README (`clock`, `transparent`, all-day placement) and write a synthesis citing the two gap claims as thesis and the new claims as antithesis, so the gaps close and the numbered open list is carried forward unchanged
- [x] 4.3 Commit and push both repositories
