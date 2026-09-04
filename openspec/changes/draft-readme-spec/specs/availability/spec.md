## ADDED Requirements

### Requirement: Availability retirement kinds

An availability's `retired.kind` SHALL be one of `retracted` (the disposition is withdrawn) or `superseded` (replaced by a specific other availability with different terms, in which case `superseded_by` SHALL carry that availability's id). A retired availability SHALL NOT be eligible supply for resolution.

#### Scenario: Retracted supply excluded
- **WHEN** an availability carries `retired: {kind: retracted, ...}`
- **THEN** resolution excludes it and any commitment resting on it carries an `expired-ground` flag

#### Scenario: Superseded availability
- **WHEN** an availability is retired with `kind: superseded` and `superseded_by: avl_B`
- **THEN** validation requires avl_B to exist, and resolution uses avl_B rather than the retired object

### Requirement: Renewal is an edit, supersession is a change of terms

Renewing an availability SHALL be an edit to `valid_until` on the same object. Changing its `window`, `duration`, or `conditional` SHALL be done by creating a new availability and retiring the old one as `superseded`. A tool SHALL refuse an edit that changes those terms on an existing availability.

#### Scenario: Renewal keeps the id
- **WHEN** a person renews an expired availability
- **THEN** `valid_until` is advanced on the same object, its version changes, and every anchor or acknowledgement referencing its id remains valid

#### Scenario: Terms change refused
- **WHEN** an edit attempts to change an existing availability's `conditional`
- **THEN** the write is refused with guidance to supersede

## MODIFIED Requirements

### Requirement: Availability fields

An AVAILABILITY SHALL carry, in canonical order: `id`; `subject` (a URI identifying the particular whose availability this is); optional `title` and `description` (prose); `duration` (the capacity offered, optionally ranged); `window`; optional `conditional` (a list of activity-vocabulary terms; absent means available for anything); optional `cadence`; optional `valid_until` (an admitted EDTF expression or a datetime); `scope` (one of `personal`, `organisation`, `public`); `source`; `timestamp`; and at most one `retired` record.

The scheduling projection of an AVAILABILITY SHALL be: `subject`, `duration`, `window`, `conditional`, `cadence`, `valid_until`, `retired.kind`.

#### Scenario: Room availability
- **WHEN** an availability is written with `subject: https://example.org/rooms/3`, `window.calendar: 2026-W37`, `duration: PT8H`, and a `source.author`
- **THEN** it is valid and resolution treats the room as a particular whose supply must be satisfied when an intention lists it in `parties`

#### Scenario: Availability without author
- **WHEN** an availability is written with no `source.author` and no workspace default
- **THEN** the write is refused

### Requirement: Validity horizon

A one-off availability (no `cadence`) SHALL expire at the end of its window and needs no `valid_until`. A recurring availability without an explicit `valid_until` SHALL be treated as having one equal to its `timestamp` plus the workspace's `availability.default_horizon`. The specification's recommended default is one quarter (`P13W`). An explicit `valid_until` always takes precedence.

#### Scenario: Default applied
- **WHEN** a recurring availability with `timestamp: 2026-09-04T00:00:00Z` has no `valid_until` and the workspace default is `P13W`
- **THEN** it is treated as valid until 2026-12-04

#### Scenario: Backdated origin
- **WHEN** a recurring availability written on 2026-09-04 carries `timestamp: 2026-08-01T00:00:00Z`
- **THEN** its default horizon is measured from 2026-08-01

#### Scenario: Explicit horizon wins
- **WHEN** a recurring availability carries `valid_until: 2026-10`
- **THEN** the workspace default is ignored
