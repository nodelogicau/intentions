## ADDED Requirements

### Requirement: Clock anchor expresses time of day

A WINDOW MAY carry a `clock` anchor: an ISO 8601 time-of-day interval written `HH:MM/HH:MM` (seconds optional), read in the resolver context's timezone, and applied to every local day that the window's other anchors admit. The start is inclusive and the end exclusive. The interval MAY cross midnight, in which case the day it belongs to is the local day of its start. A WINDOW without `clock` SHALL mean whole days. A placement SHALL satisfy every anchor the window carries. `clock` SHALL be stored as written; its bounds SHALL be computed at resolution time like every other anchor, and where a clock time does not exist on a given local day the resolver SHALL follow RFC 5545 section 3.3.5 for nonexistent local times. `clock` is part of `window` and therefore of every scheduling projection that includes `window`.

#### Scenario: Mornings
- **WHEN** an availability has `window: {calendar: 2026-09/2026-12, clock: 09:00/12:00}` and `cadence: FREQ=WEEKLY;BYDAY=TU`
- **THEN** it supplies 09:00 to 12:00 in the resolver's timezone on each Tuesday from September to December, and a placement at 14:00 on a Tuesday is outside it

#### Scenario: After five this week
- **WHEN** an availability has `window: {calendar: 2026-W37, clock: 17:00/21:00}` and no cadence
- **THEN** it supplies 17:00 to 21:00 on each day of ISO week 37 and expires with that week

#### Scenario: Crossing midnight
- **WHEN** a window has `clock: 22:00/02:00` and `cadence: FREQ=WEEKLY;BYDAY=FR`
- **THEN** each occurrence runs from Friday 22:00 to Saturday 02:00 local time and belongs to the Friday

#### Scenario: Whole days by default
- **WHEN** a window has `calendar: 2026-09-15` and no `clock`
- **THEN** its bounds are the whole of that local day

#### Scenario: Clock survives a timezone change
- **WHEN** a window has `clock: 09:00/12:00` and the resolver context timezone changes
- **THEN** the stored window is unchanged and the computed bounds move with the new zone

## MODIFIED Requirements

### Requirement: Cadence borrows RRULE grammar

Where an object carries a `cadence`, it SHALL be an iCalendar RRULE expression (RFC 5545 section 3.3.10) using only its date-level parts. `BYHOUR`, `BYMINUTE`, and `BYSECOND` SHALL NOT be admitted: time of day is expressed by the window's `clock` anchor and nowhere else. Cadence SHALL express only a generating pattern; exception handling (RDATE, EXDATE, RECURRENCE-ID) SHALL NOT be used, because a skipped occurrence is represented by retiring the generated instance.

#### Scenario: Weekly cadence
- **WHEN** a standing intention carries `cadence: FREQ=WEEKLY;BYDAY=TU`
- **THEN** instances may be generated for each Tuesday on demand

#### Scenario: Sub-day part rejected
- **WHEN** an object is written with `cadence: FREQ=WEEKLY;BYDAY=TU;BYHOUR=9`
- **THEN** the write is refused and validation reports an error naming `clock` as the place for time of day

### Requirement: Placement is the collapse to clock time

A `placement` is a concrete `start`, a DURATION, and an optional `location` (one absolute URI), and SHALL exist only on a resolved intention or a COMMITMENT. `start` SHALL be either an RFC 3339 datetime with offset or an EDTF calendar day. When `start` is a calendar day the placement is all-day: `duration` SHALL be a whole number of days and the placement SHALL span those local days in the resolver context's timezone, so that a day on which a timezone transition occurs is still one day. Resolution SHALL write datetime placements; a calendar-day `start` SHALL be written only by import. It is the single point where this specification touches clock time and fixed place, and it is written only as the result of a RESOLUTION or an import. When the intention or the supplying availability carries `location`, resolution SHALL set `placement.location` to one URI from their intersection; otherwise `placement.location` MAY be absent.

#### Scenario: Placement written by resolution
- **WHEN** a resolution is selected for an intention
- **THEN** the intention gains a `placement` with a datetime `start` and its `window` is preserved unchanged

#### Scenario: Placement location chosen
- **WHEN** an intention with `location: [home, office]` is resolved against availability with `location: [office]`
- **THEN** the placement carries `location: office` and the intention's `location` list is unchanged

#### Scenario: All-day placement
- **WHEN** an import writes `placement: {start: 2026-09-21, duration: P5D}`
- **THEN** the placement spans the five local days from 21 to 25 September in the resolver's timezone

#### Scenario: All-day with a fractional duration rejected
- **WHEN** a placement is written with `start: 2026-09-21` and `duration: PT4H`
- **THEN** the write is refused and validation reports an error
