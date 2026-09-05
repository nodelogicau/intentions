## ADDED Requirements

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
