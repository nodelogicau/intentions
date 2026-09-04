## MODIFIED Requirements

### Requirement: Flag kinds

A flag SHALL have exactly one `kind` from: `window-clash` (a placement overlaps another placement or falls in a window with no eligible supply), `condition-mismatch` (the availability supplying a placement has a conditional that does not include the intention's activity), `location-mismatch` (the availability supplying a placement has a location list that does not include the placement's location, or the placement's location is not in the intention's location list), `expired-ground` (an availability the placement rests on has passed its horizon or been retired), `intention-inconsistency` (two active intentions cannot both be placed within their windows given available supply), and `cycle` (the intention is in a strongly-connected component of the serves graph). Flags SHALL NOT carry a numeric severity.

#### Scenario: Kinds are exhaustive
- **WHEN** a consistency check finds a problem
- **THEN** it is reported under exactly one of the six kinds

#### Scenario: Imported meeting elsewhere
- **WHEN** an imported commitment carries `placement.location: office` and the subject's availability for that window carries `location: [home]`
- **THEN** the commitment carries a `location-mismatch` flag and its party statuses are unchanged


### Requirement: Acknowledgements are stored

An ACKNOWLEDGEMENT SHALL be an entry in the `acknowledgements` list of the intention or commitment it concerns, with fields `kind`, `counterpart` (id, or absent where the flag has none), `counterpart_version`, `reason` (prose), `timestamp`, and `source`. The list SHALL be append-only. Acknowledgements are excluded from the scheduling projection.

#### Scenario: Acknowledge a clash
- **WHEN** a person acknowledges the window-clash between cmt_X and int_Y with a reason
- **THEN** an acknowledgement is appended to cmt_X recording kind, counterpart int_Y, int_Y's current version, the reason, the time, and the person as `source.author`

#### Scenario: Acknowledgement on a retired object
- **WHEN** an acknowledgement is appended to an intention that carries a `retired` record
- **THEN** the append is accepted and no other field of the intention changes

### Requirement: Consistency never changes state

A consistency check SHALL NOT retire any object, nor change any object's stability, placement, or party status. Its only outputs are flags.

#### Scenario: Inconsistent intentions
- **WHEN** two firm intentions cannot both be placed
- **THEN** both carry an `intention-inconsistency` flag and neither gains a `retired` record
