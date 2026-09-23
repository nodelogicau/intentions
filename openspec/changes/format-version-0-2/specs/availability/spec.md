## MODIFIED Requirements

### Requirement: Availability fields

An AVAILABILITY SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose availability this is); optional `title` and `description` (prose); `capacity` (a DURATION: the capacity offered per occasion, optionally ranged); `window`; optional `activities` (a list of activity-vocabulary terms; absent means available for anything); optional `location` (a list of absolute URIs at which this capacity holds; absent means anywhere); optional `cadence`; optional `valid_until` (an admitted EDTF expression or a datetime); `scope` (one of `personal`, `organisation`, `public`); `source`; `timestamp`; and at most one `retired` record.

The scheduling projection of an AVAILABILITY SHALL be: `subject`, `capacity`, `window`, `activities`, `location`, `cadence`, `valid_until`, `retired.kind`.

#### Scenario: Room availability
- **WHEN** an availability is written with `subject: https://example.org/rooms/3`, `window.calendar: 2026-W37`, `capacity: PT8H`, and a `source.author`
- **THEN** it is valid, carries `version` after `id`, and resolution treats the room as a particular whose supply must be satisfied when an intention lists it in `parties`

#### Scenario: Availability without author
- **WHEN** an availability is written with no `source.author` and no workspace default
- **THEN** the write is refused

### Requirement: Conditional is a filter, not a reason

`activities` SHALL constrain which intention `activity` values this availability may supply. It SHALL NOT carry a chain of reasons and SHALL NOT reference the intention graph.

#### Scenario: Conditional match
- **WHEN** an availability has `activities: [deep-work]` and an intention has `activity: deep-work`
- **THEN** the availability is eligible supply for that intention

#### Scenario: Conditional mismatch
- **WHEN** an availability has `activities: [deep-work]` and an intention has `activity: meeting`
- **THEN** the availability is not eligible supply, and a commitment placed there anyway carries a `condition-mismatch` flag

### Requirement: Renewal is an edit, supersession is a change of terms

Renewing an availability SHALL be an edit to `valid_until` on the same object. Changing its `window`, `capacity`, `activities`, or `location` SHALL be done by creating a new availability and retiring the old one as `superseded`. A tool SHALL refuse an edit that changes those terms on an existing availability.

#### Scenario: Renewal keeps the id
- **WHEN** a person renews an expired availability
- **THEN** `valid_until` is advanced on the same object, its version changes, and every anchor or acknowledgement referencing its id remains valid

#### Scenario: Terms change refused
- **WHEN** an edit attempts to change an existing availability's `activities`
- **THEN** the write is refused with guidance to supersede

### Requirement: Time-of-day capacity

An availability whose `window` carries a `clock` anchor SHALL supply only the clock interval on each day its window and cadence admit. `capacity` is the capacity offered per occasion and MAY be shorter than the clock interval, in which case resolution MAY place the intention's duration anywhere within the interval. Because `clock` is part of `window`, changing it is a change of terms and SHALL be done by supersession, never by editing the existing availability.

#### Scenario: Mornings for deep work
- **WHEN** an availability is titled "Tuesday mornings for deep work" with `window: {calendar: 2026-09/2026-12, clock: 09:00/12:00}`, `capacity: PT3H`, and `cadence: FREQ=WEEKLY;BYDAY=TU`
- **THEN** it supplies exactly 09:00 to 12:00 on each Tuesday and nothing on a Tuesday afternoon

#### Scenario: Capacity shorter than the interval
- **WHEN** an availability has `clock: 09:00/17:00` and `capacity: PT3H`
- **THEN** resolution may place a three-hour intention at any point between 09:00 and 17:00, and a candidate at 15:00 to 18:00 is outside the supply

#### Scenario: Clock change is supersession
- **WHEN** an edit attempts to change an existing availability's `window.clock` from `09:00/12:00` to `13:00/16:00`
- **THEN** the write is refused with guidance to supersede

### Requirement: Capacity is consumed per occasion

Each occasion of an availability SHALL offer its `capacity` (the `max` when ranged). The opaque, unretired placements resting on an occasion SHALL consume it: a candidate SHALL fit within the offered capacity less what is already resting there. A commitment SHALL consume the capacity of a party only where that party's own entry is `tentative` or `accepted`; a party at `declined` SHALL have none of their capacity consumed by it. An intention's placement and the commitment created from it SHALL count once against the subject's capacity, and that placement consumes it whatever the subject's party entry says. Transparent commitments consume nothing.

#### Scenario: Two into three
- **WHEN** a three-hour Tuesday-morning occasion already holds a two-hour placement
- **THEN** a second two-hour intention has no candidate there and a one-hour one does

#### Scenario: Commitment does not double-count
- **WHEN** a one-hour intention is placed on an occasion and a commitment is created from it
- **THEN** the occasion's remaining capacity is reduced by one hour, not two

#### Scenario: Transparent import does not consume
- **WHEN** an imported commitment with `transparent: true` overlaps an occasion
- **THEN** the occasion's remaining capacity is unchanged

#### Scenario: Declined import does not consume
- **WHEN** the subject declines an imported one-hour commitment resting on a three-hour occasion
- **THEN** the occasion's remaining capacity returns to three hours for them

#### Scenario: Declining does not free a placed intention's hour
- **WHEN** the subject declines a commitment created from their own intention, which is still placed
- **THEN** the occasion's remaining capacity is unchanged, because the intention's placement consumes it
