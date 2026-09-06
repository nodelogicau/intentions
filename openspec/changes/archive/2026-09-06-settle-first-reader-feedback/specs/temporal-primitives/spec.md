## MODIFIED Requirements

### Requirement: DURATION is an ISO 8601 duration

A DURATION SHALL be an ISO 8601 duration string (for example `PT90M`, `P2D`). A DURATION MAY additionally carry `min` and `max` ISO 8601 durations to express a range; when present, the nominal value SHALL lie within the range. A zero duration SHALL be written `P0D`, on disk and in the projection.

#### Scenario: Nominal duration
- **WHEN** an intention declares `duration: PT90M`
- **THEN** resolution seeks a placement of ninety minutes

#### Scenario: Ranged duration
- **WHEN** an intention declares `duration: {nominal: PT1H, min: PT30M, max: PT2H}`
- **THEN** resolution may propose any placement between thirty minutes and two hours, preferring one hour

#### Scenario: Zero gap
- **WHEN** a writer is given a relational anchor with a minimum gap of zero
- **THEN** the file carries `gap: {min: P0D, ...}` and not `PT0S`

### Requirement: WINDOW stores an expression, never computed bounds

A WINDOW SHALL store the anchoring expression as written and SHALL NOT store a computed start and end datetime. Bounds SHALL be computed at resolution time from the resolver context (`resolver.timezone`, and `resolver.hemisphere` for neutral season codes) declared in `intentions.yaml` or overridden on the resolver. Week granules are ISO weeks, Monday to Sunday, in every resolver context.

#### Scenario: Week window across timezones
- **WHEN** a WINDOW is `2026-W36` and the resolver context timezone changes
- **THEN** the stored WINDOW is unchanged and the computed bounds differ

#### Scenario: Week is ISO in every context
- **WHEN** a WINDOW is `2026-W36`
- **THEN** its bounds are Monday 31 August to Sunday 6 September 2026 in the resolver's timezone, whatever day the person considers the start of their week

### Requirement: Calendar anchor uses EDTF

A WINDOW MAY carry a `calendar` anchor, which SHALL be an ISO 8601-2 / EDTF expression from the admitted subset: reduced-precision dates (`2026`, `2026-09`, `2026-W36`, `2026-09-04`); EDTF season codes, both neutral (`2026-21` through `2026-24` for spring, summer, autumn, winter) and hemisphere-specific (`2026-25` through `2026-28` for Northern spring, summer, autumn, winter; `2026-29` through `2026-32` for Southern); EDTF quarter codes (`2026-33` through `2026-36`); bounded intervals between any two admitted expressions (`2026-W36/2026-W38`); and open intervals (`../2026-09`, `2026-09/..`). A neutral season SHALL resolve through `resolver.hemisphere`. Northern spring, summer, autumn and winter SHALL be March to May, June to August, September to November, and December to February; Southern spring, summer, autumn and winter SHALL be September to November, December to February, March to May, and June to August. A season that begins in December SHALL start in the granule's year and run into the next. EDTF uncertain and approximate qualifiers (`?`, `~`, `%`) SHALL NOT be admitted.

#### Scenario: Deadline
- **WHEN** a WINDOW is `calendar: ../2026-09`
- **THEN** resolution treats any placement ending before the end of September 2026 as within the window

#### Scenario: Quarter
- **WHEN** a WINDOW is `calendar: 2026-35`
- **THEN** resolution treats the third quarter of 2026 as the window

#### Scenario: Neutral season in the south
- **WHEN** a WINDOW is `calendar: 2026-21` and the resolver context has `hemisphere: south`
- **THEN** the window is September through November 2026

#### Scenario: Explicit Northern winter
- **WHEN** a WINDOW is `calendar: 2026-28`
- **THEN** the window is December 2026 through February 2027 regardless of the resolver's hemisphere

#### Scenario: Qualifier rejected
- **WHEN** a WINDOW is written as `calendar: 2026-09~`
- **THEN** the write is refused and validation reports an error

### Requirement: Deixis is resolved at write time, bounds at resolution time

A deictic expression ("this week", "next month") SHALL be resolved by the writing tool to the named granule it denotes at the moment of writing, in the resolver's timezone, and the named granule SHALL be what is stored. The granule's bounds SHALL NOT be resolved at write time. A writer that accepts deictic terms SHALL recognise at least `today`, `tomorrow`, `this-week`, `next-week`, `this-month`, `next-month`, `this-quarter`, `next-quarter`, and `this-year`, each denoting the granule containing the current instant or the one after it. Because weeks are ISO weeks, `this-week` on a Sunday denotes the week ending that day; a writer talking to a person whose week starts on Sunday MAY ask which week was meant.

#### Scenario: "This week" captured
- **WHEN** a person writes "this week" on 2026-09-04
- **THEN** the WINDOW stores `calendar: 2026-W36` and the object means the same week when read a month later

#### Scenario: Next quarter
- **WHEN** a writer receives `next-quarter` on 2026-09-06
- **THEN** the WINDOW stores `calendar: 2026-36`

### Requirement: Cadence borrows RRULE grammar

Where an object carries a `cadence`, it SHALL be an iCalendar RRULE expression (RFC 5545 section 3.3.10) using only its date-level parts. `BYHOUR`, `BYMINUTE`, and `BYSECOND` SHALL NOT be admitted: time of day is expressed by the window's `clock` anchor and nowhere else. An object carrying `cadence` SHALL have a window with a calendar anchor. The rule SHALL expand from a seed: the first local day of the calendar anchor's lower bound, or, when that bound is open (`../X`), the first day of the expansion horizon the caller supplies. `WKST` SHALL default to `MO` unless the rule states otherwise. Cadence SHALL express only a generating pattern; exception handling (RDATE, EXDATE, RECURRENCE-ID) SHALL NOT be used, because a skipped occurrence is represented by retiring the generated instance.

#### Scenario: Weekly cadence
- **WHEN** a standing intention carries `cadence: FREQ=WEEKLY;BYDAY=TU`
- **THEN** instances may be generated for each Tuesday on demand

#### Scenario: Seed from the anchor
- **WHEN** an object carries `cadence: FREQ=WEEKLY` and `window.calendar: 2026-09-16/2026-12`
- **THEN** the rule expands from Wednesday 16 September 2026 and every occurrence is a Wednesday

#### Scenario: Seed from the horizon
- **WHEN** an object carries `cadence: FREQ=MONTHLY` and `window.calendar: ../2026-12`, and generation runs over a horizon starting 2026-09-10
- **THEN** the rule expands from 10 September and occurrences fall on the tenth of each month

#### Scenario: Cadence without a calendar anchor
- **WHEN** an object is written with `cadence` and a window carrying only a `relative` anchor
- **THEN** the write is refused and validation reports an error

#### Scenario: Sub-day part rejected
- **WHEN** an object is written with `cadence: FREQ=WEEKLY;BYDAY=TU;BYHOUR=9`
- **THEN** the write is refused and validation reports an error naming `clock` as the place for time of day
