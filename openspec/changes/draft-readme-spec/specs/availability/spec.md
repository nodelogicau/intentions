## MODIFIED Requirements

### Requirement: Availability fields

An AVAILABILITY SHALL carry: `id`; `subject` (a URI identifying the particular whose availability this is); `source`; `duration` (the capacity offered, optionally ranged); `window`; optional `conditional` (a list of terms from the workspace activity-type vocabulary; absent means available for anything); optional `cadence`; optional `valid_until` (an admitted EDTF expression or a datetime); `scope` (one of `personal`, `organisation`, `public`); optional `title` and `description` (prose); and at most one `retired` record.

The scheduling projection of an AVAILABILITY SHALL be: `subject`, `duration`, `window`, `conditional`, `cadence`, `valid_until`, `retired.kind`.

#### Scenario: Room availability
- **WHEN** an availability is written with `subject: https://example.org/rooms/3`, `window.calendar: 2026-W37`, `duration: PT8H`, and a `source.author`
- **THEN** it is valid and resolution treats the room as a particular whose supply must be satisfied when an intention lists it in `parties`

#### Scenario: Availability without author
- **WHEN** an availability is written with no `source.author` and no workspace default
- **THEN** the write is refused

## ADDED Requirements

### Requirement: Availability retirement kinds

An availability's `retired.kind` SHALL be one of `retracted` (the disposition is withdrawn) or `superseded` (replaced by a specific other availability, in which case `superseded_by` SHALL carry that availability's id). A retired availability SHALL NOT be eligible supply for resolution.

#### Scenario: Retracted supply excluded
- **WHEN** an availability carries `retired: {kind: retracted, ...}`
- **THEN** resolution excludes it and any commitment resting on it carries an `expired-ground` flag

#### Scenario: Superseded availability
- **WHEN** an availability is retired with `kind: superseded` and `superseded_by: avl_B`
- **THEN** validation requires avl_B to exist, and resolution uses avl_B rather than the retired object
