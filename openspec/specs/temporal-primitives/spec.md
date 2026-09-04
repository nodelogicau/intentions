# Temporal Primitives

## Purpose

Defines DURATION and WINDOW, the two temporal values carried by intentions and availability. Together with INTENTION they replace the fixed clock slot as the primary planning primitive. The design preserves what Heidegger calls datability (a time is dated by its significance, not by a coordinate) and spannedness (time is lived as a stretch, not a point): a WINDOW stores the expression the person actually meant, and its clock bounds are computed only when a resolver needs them.

## Requirements

### Requirement: DURATION is an ISO 8601 duration

A DURATION SHALL be an ISO 8601 duration string (for example `PT90M`, `P2D`). A DURATION MAY additionally carry `min` and `max` ISO 8601 durations to express a range; when present, the nominal value SHALL lie within the range.

#### Scenario: Nominal duration
- **WHEN** an intention declares `duration: PT90M`
- **THEN** resolution seeks a placement of ninety minutes

#### Scenario: Ranged duration
- **WHEN** an intention declares `duration: {nominal: PT1H, min: PT30M, max: PT2H}`
- **THEN** resolution may propose any placement between thirty minutes and two hours, preferring one hour

### Requirement: WINDOW stores an expression, never computed bounds

A WINDOW SHALL store the anchoring expression as written and SHALL NOT store a computed start and end datetime. Bounds SHALL be computed at resolution time from the resolver context (timezone, week start, calendar system) declared in `intentions.yaml` or overridden on the resolver.

#### Scenario: Week window across timezones
- **WHEN** a WINDOW is `2026-W36` and the resolver context timezone changes
- **THEN** the stored WINDOW is unchanged and the computed bounds differ

### Requirement: Calendar anchor uses EDTF

A WINDOW MAY carry a `calendar` anchor, which SHALL be an ISO 8601-2 / EDTF expression from the admitted subset: reduced-precision dates (`2026`, `2026-09`, `2026-W36`, `2026-09-04`), EDTF season and quarter codes (`2026-21` through `2026-24` for seasons, `2026-33` through `2026-36` for quarters), bounded intervals between any two admitted expressions (`2026-W36/2026-W38`), and open intervals (`../2026-09`, `2026-09/..`). EDTF uncertain and approximate qualifiers (`?`, `~`, `%`) SHALL NOT be admitted.

#### Scenario: Deadline
- **WHEN** a WINDOW is `calendar: ../2026-09`
- **THEN** resolution treats any placement ending before the end of September 2026 as within the window

#### Scenario: Quarter
- **WHEN** a WINDOW is `calendar: 2026-35`
- **THEN** resolution treats the third quarter of 2026 as the window

#### Scenario: Qualifier rejected
- **WHEN** a WINDOW is written as `calendar: 2026-09~`
- **THEN** the write is refused and validation reports an error

### Requirement: Deixis is resolved at write time, bounds at resolution time

A deictic expression ("this week", "next month") SHALL be resolved by the writing tool to the named granule it denotes at the moment of writing, and the named granule SHALL be what is stored. The granule's bounds SHALL NOT be resolved at write time.

#### Scenario: "This week" captured
- **WHEN** a person writes "this week" on 2026-09-04
- **THEN** the WINDOW stores `calendar: 2026-W36` and the object means the same week when read a month later

### Requirement: Relational anchor uses RFC 9253 temporal relations

A WINDOW MAY carry a `relative` anchor with fields `target` (the id of another intention or commitment), `relation` (one of `FINISHTOSTART`, `FINISHTOFINISH`, `STARTTOFINISH`, `STARTTOSTART`, as defined in RFC 9253), and an optional `gap` with `min` and `max` ISO 8601 durations. The dependent WINDOW SHALL hold the reference; the target SHALL NOT be modified. This inverts RFC 9253's convention of placing the relation on the predecessor, to match the outbound-reference rule of the object model.

A `relative` anchor whose target has no placement yet SHALL be treated as a constraint between two unresolved windows and SHALL NOT be reported as an error.

#### Scenario: After another intention
- **WHEN** a WINDOW is `relative: {target: int_A, relation: FINISHTOSTART, gap: {min: P0D, max: P3D}}`
- **THEN** resolution constrains the placement to start between zero and three days after intention A finishes

#### Scenario: Both anchors
- **WHEN** a WINDOW carries `calendar: 2026-09` and a `relative` anchor on int_A
- **THEN** resolution requires a placement satisfying both

#### Scenario: Unresolved target
- **WHEN** the target of a relative anchor has no placement
- **THEN** resolution reports the dependent intention as blocked on the target and does not place it

### Requirement: Cadence borrows RRULE grammar

Where an object carries a `cadence`, it SHALL be an iCalendar RRULE expression (RFC 5545 section 3.3.10). Cadence SHALL express only a generating pattern; exception handling (RDATE, EXDATE, RECURRENCE-ID) SHALL NOT be used, because a skipped occurrence is represented by retiring the generated instance.

#### Scenario: Weekly cadence
- **WHEN** a standing intention carries `cadence: FREQ=WEEKLY;BYDAY=TU`
- **THEN** instances may be generated for each Tuesday on demand

### Requirement: Placement is the collapse to clock time

A `placement` is a concrete `start` datetime with timezone, a DURATION, and an optional `location` (one absolute URI), and SHALL exist only on a resolved intention or a COMMITMENT. It is the single point where this specification touches clock time and fixed place, and it is written only as the result of a RESOLUTION or an import. When the intention or the supplying availability carries `location`, resolution SHALL set `placement.location` to one URI from their intersection; otherwise `placement.location` MAY be absent.

#### Scenario: Placement written by resolution
- **WHEN** a resolution is selected for an intention
- **THEN** the intention gains a `placement` and its `window` is preserved unchanged

#### Scenario: Placement location chosen
- **WHEN** an intention with `location: [home, office]` is resolved against availability with `location: [office]`
- **THEN** the placement carries `location: office` and the intention's `location` list is unchanged
