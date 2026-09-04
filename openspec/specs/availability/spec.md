# Availability

## Purpose

Defines AVAILABILITY, a standing statement that some particular (a person, a room, a piece of equipment, anything with a URI) has capacity for a kind of engagement within a window. Availability is assertive rather than commissive: it says what could be, not what will be. It sits alongside intention as a peer and is the supply that RESOLUTION matches intention's demand against.

Availability is closer to Heidegger's potentiality-for-being than to projection: a disposition rather than an act. It therefore needs no instance generation and, unlike an intention, can silently stop being true, which is why it carries a validity horizon.

## Requirements

### Requirement: Availability fields

An AVAILABILITY SHALL carry: `id`; `subject` (a URI identifying the particular whose availability this is); `duration` (the capacity offered, optionally ranged); `window`; optional `conditional` (a list of terms from the workspace activity-type vocabulary; absent means available for anything); optional `cadence`; optional `valid_until` (an admitted EDTF expression or a datetime); `scope` (one of `personal`, `organisation`, `public`); `status` (`active` or `retracted`); optional `title` and `description` (prose).

The scheduling projection of an AVAILABILITY SHALL be: `subject`, `duration`, `window`, `conditional`, `cadence`, `valid_until`, `status`.

#### Scenario: Room availability
- **WHEN** an availability is written with `subject: https://example.org/rooms/3`, `window.calendar: 2026-W37`, `duration: PT8H`
- **THEN** it is valid and resolution treats the room as a particular whose supply must be satisfied when an intention lists it in `parties`

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

A one-off availability (no `cadence`) SHALL expire at the end of its window and needs no `valid_until`. A recurring availability without an explicit `valid_until` SHALL be treated as having one equal to the timestamp encoded in its UUIDv7 id plus the workspace's `availability.default_horizon`. The specification's recommended default is one quarter (`P13W`). An explicit `valid_until` always takes precedence.

#### Scenario: Default applied
- **WHEN** a recurring availability is written on 2026-09-04 without `valid_until` and the workspace default is `P13W`
- **THEN** it is treated as valid until 2026-12-04

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

`scope` SHALL default to `personal`. Only availability with `scope` at or wider than a resolver's own scope SHALL be visible to it. Scope SHALL only ever be widened.

#### Scenario: Shared availability
- **WHEN** a person sets an availability's scope to `organisation`
- **THEN** a resolver acting for another party in the organisation may use it as supply
