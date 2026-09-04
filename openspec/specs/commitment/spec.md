# Commitment

## Purpose

Defines COMMITMENT, the interpersonal counterpart of an intention. Both are commissive: an intention involves no other party, a commitment is directed at someone and carries a negotiation history. A commitment is the only object with a placement by construction and the only object that references an external calendar, because it is the point at which this specification hands off to iCalendar or JSCalendar for interchange.

A commitment's status is a deontic fact about a party's will. Per Searle's felicity conditions it requires sincerity, so software SHALL never set it; it only records and flags.

## Requirements

### Requirement: Commitment fields

A COMMITMENT SHALL carry: `id`; `parties` (a list of `{uri, status}` where `status` is one of `tentative`, `accepted`, `declined`); `placement`; optional `intention` (the id of the intention it fulfils); `origin` (one of `resolution` with the resolution id, or `import`); optional `external` (`{system: icalendar|jscalendar, uid}`); `status` (`active` or `cancelled`); optional `title` and `description`; and `acknowledgements`.

The scheduling projection of a COMMITMENT SHALL be: `parties`, `placement`, `intention`, `origin`, `external`, `status`.

#### Scenario: Commitment from resolution
- **WHEN** a multi-party intention is resolved
- **THEN** a commitment is created with `origin: {resolution: res_...}`, `intention: int_...`, every party at `tentative`, and no `external`

### Requirement: Two origins

A commitment SHALL arise either endogenously from a RESOLUTION, in which case consistency with availability and intention holds by construction at creation, or exogenously by import from an external calendar, in which case consistency SHALL be checked at creation and any clash flagged. An imported commitment SHALL NOT create an intention or availability.

#### Scenario: Import clashes with availability
- **WHEN** an iCalendar event is imported whose placement falls outside the person's declared availability
- **THEN** the commitment is created with all parties as the import states them and carries a `window-clash` flag

### Requirement: Party status is set only by that party's explicit act

A party's `status` SHALL change only through an explicit act attributed to that party: a local action by the workspace owner for their own entry, or an imported iTIP reply for another party. No resolution, consistency check, flag, or policy SHALL change a party status.

#### Scenario: Flag does not decline
- **WHEN** a consistency check finds a commitment clashing with a firm intention
- **THEN** the commitment's party statuses are unchanged and a flag is reported

#### Scenario: Owner accepts
- **WHEN** the workspace owner accepts a tentative commitment
- **THEN** their party entry becomes `accepted` and the version changes

### Requirement: Cancellation

A commitment SHALL be cancelled by setting `status: cancelled`, which is terminal. Cancelling a commitment SHALL NOT retire its intention; the intention's placement SHALL be cleared so it may be re-resolved.

#### Scenario: Cancel and re-resolve
- **WHEN** a commitment created from int_A is cancelled
- **THEN** int_A loses its placement, keeps its window, and is eligible for resolution again

### Requirement: External reference only

`external.uid` SHALL be the only link between this specification and an external calendar object. The external object's recurrence, timezone definitions, alarms, and attendee metadata SHALL NOT be copied into the commitment. A recurring external event SHALL be imported as one commitment per occurrence the importer chooses to bring in, each carrying the same `uid` plus the occurrence's placement.

#### Scenario: Recurring import
- **WHEN** a weekly iCalendar event is imported for the next four occurrences
- **THEN** four commitments are created sharing one `external.uid` and differing in `placement`

### Requirement: Consistency check on create and update

A consistency check (see Consistency) SHALL run whenever a commitment is created or its projection changes, and whenever an availability or intention it rests on changes.

#### Scenario: Availability retracted after commitment
- **WHEN** the availability a resolved commitment rested on is retracted
- **THEN** the next consistency check reports an `expired-ground` flag on the commitment
