## MODIFIED Requirements

### Requirement: Flag kinds

A flag SHALL have exactly one `kind` from: `window-clash` (a placement overlaps another placement or falls in a window with no eligible supply), `condition-mismatch` (the availability supplying a placement has a conditional that does not include the intention's activity), `location-mismatch` (the availability supplying a placement has a location list that does not include the placement's location, or the placement's location is not in the intention's location list), `expired-ground` (an availability the placement rests on has passed its horizon or been retired), `intention-inconsistency` (two active unplaced intentions of one subject, each with duration and window and with intersecting resolution ranges, each have candidates alone but no pair of non-overlapping candidates exists; the check is pairwise and never global), and `cycle` (the intention is in a strongly-connected component of the serves graph). Flags SHALL NOT carry a numeric severity.

#### Scenario: Kinds are exhaustive
- **WHEN** a consistency check finds a problem
- **THEN** it is reported under exactly one of the six kinds

#### Scenario: Imported meeting elsewhere
- **WHEN** an imported commitment carries `placement.location: office` and the subject's availability for that window carries `location: [home]`
- **THEN** the commitment carries a `location-mismatch` flag and its party statuses are unchanged

#### Scenario: Pairwise inconsistency
- **WHEN** two unplaced intentions of one subject each fit the subject's single three-hour occasion alone but not together
- **THEN** both carry an `intention-inconsistency` flag naming the other, with `detail` saying the check is pairwise

#### Scenario: Three-way infeasibility not reported
- **WHEN** three unplaced intentions each fit an occasion in pairs but not all three together
- **THEN** no `intention-inconsistency` flag is reported

## ADDED Requirements

### Requirement: What a placement rests on is recomputed

At check time a placement SHALL rest on every occasion, of each particular involved in it, that contains the placement. No containing occasion for some involved particular SHALL be reported as `window-clash` without counterpart. Where containing occasions exist but every one fails eligibility, the failure SHALL be reported by its kind: a retired or expired occasion as `expired-ground`, a conditional that excludes the activity as `condition-mismatch`, a location list that excludes the placement's location as `location-mismatch`. Nothing stored on the placement, the intention, or the RESOLUTION record SHALL be used to decide what a placement rests on.

#### Scenario: Availability replaced after selection
- **WHEN** the availability named in a resolution's `supply` is superseded by one that still contains the placement
- **THEN** the next check finds the placement resting on the new availability and reports nothing

#### Scenario: Only containing occasion expired
- **WHEN** the only occasion containing a placement has passed its validity horizon
- **THEN** the placement carries `expired-ground`, not `window-clash`

#### Scenario: No containing occasion
- **WHEN** no occasion of the subject contains a placement
- **THEN** the placement carries `window-clash` with no counterpart
