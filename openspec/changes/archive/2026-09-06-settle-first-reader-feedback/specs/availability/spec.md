## MODIFIED Requirements

### Requirement: Availability fields

An AVAILABILITY SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose availability this is); optional `title` and `description` (prose); `duration` (the capacity offered, optionally ranged); `window`; optional `conditional` (a list of activity-vocabulary terms; absent means available for anything); optional `location` (a list of absolute URIs at which this capacity holds; absent means anywhere); optional `cadence`; optional `valid_until` (an admitted EDTF expression or a datetime); `scope` (one of `personal`, `organisation`, `public`); `source`; `timestamp`; and at most one `retired` record.

The scheduling projection of an AVAILABILITY SHALL be: `subject`, `duration`, `window`, `conditional`, `location`, `cadence`, `valid_until`, `retired.kind`.

#### Scenario: Room availability
- **WHEN** an availability is written with `subject: https://example.org/rooms/3`, `window.calendar: 2026-W37`, `duration: PT8H`, and a `source.author`
- **THEN** it is valid, carries `version` after `id`, and resolution treats the room as a particular whose supply must be satisfied when an intention lists it in `parties`

#### Scenario: Availability without author
- **WHEN** an availability is written with no `source.author` and no workspace default
- **THEN** the write is refused
