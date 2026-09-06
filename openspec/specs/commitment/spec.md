# Commitment

## Purpose

Defines COMMITMENT, the interpersonal counterpart of an intention. Both are commissive: an intention involves no other party, a commitment is directed at someone and carries a negotiation history. A commitment is the only object with a placement by construction and the only object that references an external calendar, because it is the point at which this specification hands off to iCalendar or JSCalendar for interchange.

A commitment's status is a deontic fact about a party's will. Per Searle's felicity conditions it requires sincerity, so software SHALL never set it; it only records and flags.

## Requirements

### Requirement: Commitment fields

A COMMITMENT SHALL carry, in canonical order: `id`; `version`; `parties` (a list of `{uri, status}` where `status` is one of `tentative`, `accepted`, `declined`, sorted by `uri`); `placement`; optional `intention` (the id of the intention it fulfils); `origin` (one of `resolution` with the resolution id, or `import`); optional `transparent` (a boolean; absent means false; true means the commitment occupies none of the subject's time; a writer SHALL omit it when false); optional `external` (`{system: icalendar|jscalendar, uid}`); optional `title` and `description`; `source`; `timestamp`; `acknowledgements`; and at most one `retired` record.

The scheduling projection of a COMMITMENT SHALL be: `parties`, `placement`, `intention`, `origin`, `transparent`, `external`, `retired.kind`, with `transparent` present only when true.

#### Scenario: Commitment from resolution
- **WHEN** a multi-party intention is resolved
- **THEN** a commitment is created with `version` after `id`, `origin: {resolution: res_...}`, `intention: int_...`, every party at `tentative`, `source` recording who performed the selection, no `transparent`, and no `external`

#### Scenario: Imported commitment source
- **WHEN** an iCalendar event is imported by a harness on the workspace owner's behalf
- **THEN** the commitment's `source` carries the owner as `author` and the harness as `harness`, and `origin` is `import`

#### Scenario: Transparency changes the version
- **WHEN** an imported commitment's `transparent` changes from absent to true on re-import
- **THEN** its projection hash changes and any acknowledgement naming it as counterpart lapses

#### Scenario: Explicit false is absent
- **WHEN** a file arrives carrying `transparent: false`
- **THEN** it hashes identically to the same file without the field, and a writer touching it drops the field

### Requirement: Two origins

A commitment SHALL arise either endogenously from a RESOLUTION, in which case consistency with availability and intention holds by construction at creation, or exogenously by import from an external calendar, in which case consistency SHALL be checked at creation and any clash flagged. An imported commitment SHALL NOT create an intention or availability.

#### Scenario: Import clashes with availability
- **WHEN** an iCalendar event is imported whose placement falls outside the person's declared availability
- **THEN** the commitment is created with all parties as the import states them and carries a `window-clash` flag

### Requirement: Party status is set only by that party's explicit act

A party's `status` SHALL change only through an explicit act attributed to that party: a local action by the workspace owner for their own entry, or an imported iTIP reply for another party. No resolution, consistency check, flag, or policy SHALL change a party status.

A status is also what decides whether the commitment occupies that party's time. A commitment SHALL occupy a party's time, consuming their capacity and standing to be displaced by their resolutions, exactly where that party's own entry is `tentative` or `accepted`. A party at `declined` SHALL NOT be occupied by it. This is per party: one party's decline SHALL NOT change what the commitment occupies for any other party, whose commitment still stands. Where the commitment fulfils an intention, that intention's placement occupies its subject's time on its own, so a decline by the subject frees nothing while the placement stands and is reported as a `party-declined` flag (see Consistency).

#### Scenario: Flag does not decline
- **WHEN** a consistency check finds a commitment clashing with a firm intention
- **THEN** the commitment's party statuses are unchanged and a flag is reported

#### Scenario: Owner accepts
- **WHEN** the workspace owner accepts a tentative commitment
- **THEN** their party entry becomes `accepted` and the version changes

#### Scenario: Decline frees the decliner only
- **WHEN** a counterparty declines a commitment
- **THEN** that hour no longer consumes their capacity, and it still consumes the capacity of every party at `tentative` or `accepted`

#### Scenario: Declining an import frees the hour
- **WHEN** the subject declines an imported commitment
- **THEN** the hour no longer consumes their capacity and no later candidate is ranked as displacing it

### Requirement: Cancellation

A commitment SHALL be cancelled by appending a `retired` record with `kind: cancelled`, which is terminal. `cancelled` SHALL be the only retirement kind for a commitment. Cancelling a commitment SHALL NOT retire its intention; the intention's placement SHALL be cleared so it may be re-resolved.

#### Scenario: Cancel and re-resolve
- **WHEN** a commitment created from int_A is cancelled
- **THEN** int_A loses its placement, keeps its window, and is eligible for resolution again

#### Scenario: Cancellation carries a reason
- **WHEN** a commitment is cancelled with a `reason`
- **THEN** the `retired` record carries the reason, a timestamp, and the source of the cancelling act

### Requirement: External reference only

`external.uid` SHALL be the only link between this specification and an external calendar object. The external object's recurrence, timezone definitions, alarms, and attendee metadata SHALL NOT be copied into the commitment. A recurring external event SHALL be imported as one commitment per occurrence the importer chooses to bring in, each carrying the same `uid` plus the occurrence's placement. On import, a JSCalendar `locations` or `virtualLocations` entry, or an iCalendar `LOCATION`, that carries a URI SHALL become `placement.location`; on export `placement.location` SHALL be written to the corresponding property. On import, an iCalendar `TRANSP:TRANSPARENT` or a JSCalendar `freeBusyStatus` of `free` SHALL become `transparent: true`; on export a transparent commitment SHALL be written with `TRANSP:TRANSPARENT` or `freeBusyStatus: free` and an opaque one with `TRANSP:OPAQUE` or `freeBusyStatus: busy`. On import, an iCalendar `DTSTART` of value type `DATE` or a JSCalendar `showWithoutTime` of true SHALL become an all-day placement whose `start` is that calendar day; on export an all-day placement SHALL be written back in that form. No other metadata SHALL cross the boundary.

#### Scenario: Recurring import
- **WHEN** a weekly iCalendar event is imported for the next four occurrences
- **THEN** four commitments are created sharing one `external.uid` and differing in `placement`

#### Scenario: Virtual location imported
- **WHEN** a JSCalendar event with a `virtualLocations` entry whose `uri` is `https://meet.example.com/x` is imported
- **THEN** the commitment's `placement.location` is that URI

#### Scenario: Free-text location dropped
- **WHEN** an iCalendar event carries `LOCATION:Cafe on the corner` with no URI
- **THEN** the commitment has no `placement.location` and the text is not copied

#### Scenario: Transparent all-day import
- **WHEN** an iCalendar event with `DTSTART;VALUE=DATE:20260921`, `DURATION:P5D`, and `TRANSP:TRANSPARENT` is imported
- **THEN** one commitment is created with `placement: {start: 2026-09-21, duration: P5D}` and `transparent: true`

#### Scenario: Opaque by default
- **WHEN** an iCalendar event with no `TRANSP` property is imported
- **THEN** the commitment has no `transparent` field and is treated as opaque

#### Scenario: Export round-trip
- **WHEN** a commitment with `transparent: true` and an all-day placement is exported to iCalendar
- **THEN** the event carries `TRANSP:TRANSPARENT` and a `DTSTART` of value type `DATE`

### Requirement: Consistency check on create and update

A consistency check (see Consistency) SHALL run whenever a commitment is created or its projection changes, and whenever an availability or intention it rests on changes.

#### Scenario: Availability retracted after commitment
- **WHEN** the availability a resolved commitment rested on is retracted
- **THEN** the next consistency check reports an `expired-ground` flag on the commitment

### Requirement: Transparency arrives only by import

`transparent: true` SHALL be set only on a commitment whose `origin` is `import`. A commitment created by a resolution consumed supply to exist and is opaque by construction; a write that sets `transparent: true` on a commitment whose `origin` is a resolution SHALL be refused, and validation SHALL report it as an error.

#### Scenario: Resolution-born commitment cannot be transparent
- **WHEN** an edit sets `transparent: true` on a commitment with `origin: {resolution: res_A}`
- **THEN** the write is refused and validation reports an error

#### Scenario: Imported commitment may be transparent
- **WHEN** an imported commitment carries `transparent: true`
- **THEN** validation passes
