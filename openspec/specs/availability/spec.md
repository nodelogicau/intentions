# Availability

## Purpose

Defines AVAILABILITY, a standing statement that some particular (a person, a room, a piece of equipment, anything with a URI) has capacity for a kind of engagement within a window. Availability is assertive rather than commissive: it says what could be, not what will be. It sits alongside intention as a peer and is the supply that RESOLUTION matches intention's demand against.

Availability is closer to Heidegger's potentiality-for-being than to projection: a disposition rather than an act. It therefore needs no instance generation and, unlike an intention, can silently stop being true, which is why it carries a validity horizon.

## Requirements

### Requirement: Availability fields

An AVAILABILITY SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose availability this is); optional `title` and `description` (prose); `duration` (the capacity offered, optionally ranged); `window`; optional `conditional` (a list of activity-vocabulary terms; absent means available for anything); optional `location` (a list of absolute URIs at which this capacity holds; absent means anywhere); optional `cadence`; optional `valid_until` (an admitted EDTF expression or a datetime); `scope` (one of `personal`, `organisation`, `public`); `source`; `timestamp`; and at most one `retired` record.

The scheduling projection of an AVAILABILITY SHALL be: `subject`, `duration`, `window`, `conditional`, `location`, `cadence`, `valid_until`, `retired.kind`.

#### Scenario: Room availability
- **WHEN** an availability is written with `subject: https://example.org/rooms/3`, `window.calendar: 2026-W37`, `duration: PT8H`, and a `source.author`
- **THEN** it is valid, carries `version` after `id`, and resolution treats the room as a particular whose supply must be satisfied when an intention lists it in `parties`

#### Scenario: Availability without author
- **WHEN** an availability is written with no `source.author` and no workspace default
- **THEN** the write is refused

### Requirement: Any URI-identified particular may be a subject

`subject` SHALL be any absolute URI. This specification SHALL NOT require the subject to exist in any registry, including a DKF particulars index. Person and resource availability are the same object type.

#### Scenario: Unknown subject
- **WHEN** an availability names a subject URI that no other object mentions
- **THEN** validation passes

### Requirement: Conditional is a filter, not a reason

`conditional` SHALL constrain which intention `activity` values this availability may supply. It SHALL NOT carry a chain of reasons and SHALL NOT reference the intention graph.

#### Scenario: Conditional match
- **WHEN** an availability has `conditional: [deep-work]` and an intention has `activity: deep-work`
- **THEN** the availability is eligible supply for that intention

#### Scenario: Conditional mismatch
- **WHEN** an availability has `conditional: [deep-work]` and an intention has `activity: meeting`
- **THEN** the availability is not eligible supply, and a commitment placed there anyway carries a `condition-mismatch` flag

### Requirement: Recurring availability needs no instances

An availability with `cadence` SHALL be a single object re-evaluated at resolution time. No instance objects SHALL be generated from it.

#### Scenario: Weekly availability evaluated
- **WHEN** an availability has `cadence: FREQ=WEEKLY;BYDAY=TU` and resolution considers 2026-09-15
- **THEN** the availability supplies that Tuesday without any instance object existing

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

### Requirement: Expiry means unusable, not false

Past its validity horizon an availability SHALL NOT be used as supply by RESOLUTION and SHALL NOT be treated as false or retracted. Any commitment resting on it SHALL carry an `expired-ground` flag. Reconfirmation SHALL be an explicit act that advances `valid_until`; it SHALL change the version.

#### Scenario: Expired supply ignored
- **WHEN** a recurring availability's horizon has passed
- **THEN** resolution excludes it and reports it as expired in its output

#### Scenario: Renewal
- **WHEN** a person renews an expired availability
- **THEN** `valid_until` is advanced and the object becomes eligible supply again

### Requirement: Horizon checked at resolution time

The validity horizon SHALL be checked when RESOLUTION runs and when a consistency check runs, not by any background process.

#### Scenario: No sweep
- **WHEN** an availability passes its horizon and nothing else happens
- **THEN** no file is modified and no flag exists until a resolution or consistency check next runs

### Requirement: Scope

`scope` SHALL default to `personal`. `personal` availability SHALL be visible to a resolver only when the availability's `subject` is the intention's `subject` or one of its `parties`. `organisation` and `public` availability SHALL be visible to a resolver whose `resolver.scope` is at or narrower than the availability's scope, where `personal` is narrowest and `public` widest. Scope SHALL only ever be widened.

#### Scenario: Shared availability
- **WHEN** a person sets an availability's scope to `organisation`
- **THEN** a resolver acting for another party in the organisation may use it as supply

#### Scenario: Personal stays personal
- **WHEN** an organisation workspace holds Priya's `personal` availability and Ada resolves an intention that does not involve Rob
- **THEN** it is not visible as supply

#### Scenario: Party's personal availability
- **WHEN** Ada's intention lists Rob in `parties` and Priya's availability is `personal`
- **THEN** it is visible as Priya's supply for that intention

### Requirement: Availability retirement kinds

An availability's `retired.kind` SHALL be one of `retracted` (the disposition is withdrawn) or `superseded` (replaced by a specific other availability with different terms, in which case `superseded_by` SHALL carry that availability's id). A retired availability SHALL NOT be eligible supply for resolution.

#### Scenario: Retracted supply excluded
- **WHEN** an availability carries `retired: {kind: retracted, ...}`
- **THEN** resolution excludes it and any commitment resting on it carries an `expired-ground` flag

#### Scenario: Superseded availability
- **WHEN** an availability is retired with `kind: superseded` and `superseded_by: avl_B`
- **THEN** validation requires avl_B to exist, and resolution uses avl_B rather than the retired object

### Requirement: Location filter

`location` on an availability and on an intention SHALL each be a list of absolute URIs, matched by exact string equality. An availability with `location` SHALL be eligible supply for an intention only if the intention has no `location` or the two lists share at least one URI; an availability without `location` SHALL be eligible for any location. The specification SHALL NOT define a hierarchy among locations, require coordinates, or distinguish physical from virtual: what a URI denotes is a fact about the URI, not about the format. `location` SHALL be treated as a change of terms for the purpose of renewal versus supersession.

#### Scenario: Location intersects
- **WHEN** an availability has `location: [https://example.com/places/home]` and an intention has `location: [https://example.com/places/home, https://example.com/places/office]`
- **THEN** the availability is eligible supply for that intention

#### Scenario: Location disjoint
- **WHEN** an availability has `location: [https://example.com/places/office]` and an intention has `location: [https://example.com/places/home]`
- **THEN** the availability is not eligible supply, and a commitment placed there anyway carries a `location-mismatch` flag

#### Scenario: Virtual location
- **WHEN** an availability has `location: [https://meet.example.com/ada]` and an intention has the same URI
- **THEN** they match by string equality with no special treatment of the scheme

#### Scenario: Booked room is also the place
- **WHEN** an intention lists `https://example.com/rooms/3` in both `parties` and `location`
- **THEN** resolution consumes the room's availability as a party and sets `placement.location` to the room

### Requirement: Renewal is an edit, supersession is a change of terms

Renewing an availability SHALL be an edit to `valid_until` on the same object. Changing its `window`, `duration`, `conditional`, or `location` SHALL be done by creating a new availability and retiring the old one as `superseded`. A tool SHALL refuse an edit that changes those terms on an existing availability.

#### Scenario: Renewal keeps the id
- **WHEN** a person renews an expired availability
- **THEN** `valid_until` is advanced on the same object, its version changes, and every anchor or acknowledgement referencing its id remains valid

#### Scenario: Terms change refused
- **WHEN** an edit attempts to change an existing availability's `conditional`
- **THEN** the write is refused with guidance to supersede

### Requirement: Time-of-day capacity

An availability whose `window` carries a `clock` anchor SHALL supply only the clock interval on each day its window and cadence admit. `duration` remains the capacity offered per occasion and MAY be shorter than the clock interval, in which case resolution MAY place the duration anywhere within the interval. Because `clock` is part of `window`, changing it is a change of terms and SHALL be done by supersession, never by editing the existing availability.

#### Scenario: Mornings for deep work
- **WHEN** an availability is titled "Tuesday mornings for deep work" with `window: {calendar: 2026-09/2026-12, clock: 09:00/12:00}`, `duration: PT3H`, and `cadence: FREQ=WEEKLY;BYDAY=TU`
- **THEN** it supplies exactly 09:00 to 12:00 on each Tuesday and nothing on a Tuesday afternoon

#### Scenario: Capacity shorter than the interval
- **WHEN** an availability has `clock: 09:00/17:00` and `duration: PT3H`
- **THEN** resolution may place a three-hour intention at any point between 09:00 and 17:00, and a candidate at 15:00 to 18:00 is outside the supply

#### Scenario: Clock change is supersession
- **WHEN** an edit attempts to change an existing availability's `window.clock` from `09:00/12:00` to `13:00/16:00`
- **THEN** the write is refused with guidance to supersede

### Requirement: Capacity is consumed per occasion

Each occasion of an availability SHALL offer its `duration` (the `max` when ranged). The opaque, unretired placements resting on an occasion SHALL consume it: a candidate SHALL fit within the offered duration less what is already resting there. A commitment SHALL consume the capacity of a party only where that party's own entry is `tentative` or `accepted`; a party at `declined` SHALL have none of their capacity consumed by it. An intention's placement and the commitment created from it SHALL count once against the subject's capacity, and that placement consumes it whatever the subject's party entry says. Transparent commitments consume nothing.

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
