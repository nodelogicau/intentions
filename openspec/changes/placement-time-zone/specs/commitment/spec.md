## MODIFIED Requirements

### Requirement: External reference only

A commitment's `external.uid` SHALL be the only link between it and an external calendar object; a placed intention with no `parties` MAY carry its own link to a hold (see Calendar hold in Intention), and every other object type SHALL carry none. The external object's recurrence, timezone definitions, alarms, and attendee metadata SHALL NOT be copied into the commitment, except each participant's calendar address and participation status, which become `parties` as Parties on import states. A recurring external event SHALL be imported as one commitment per occurrence the importer chooses to bring in, each carrying the same `uid` plus the occurrence's placement. On import, a JSCalendar `locations` or `virtualLocations` entry, or an iCalendar `LOCATION`, that carries a URI SHALL become `placement.location`; on export `placement.location` SHALL be written to the corresponding property. On import, an iCalendar `TRANSP:TRANSPARENT` or a JSCalendar `freeBusyStatus` of `free` SHALL become `transparent: true`; on export a transparent commitment SHALL be written with `TRANSP:TRANSPARENT` or `freeBusyStatus: free` and an opaque one with `TRANSP:OPAQUE` or `freeBusyStatus: busy`. On import, an iCalendar `DTSTART` of value type `DATE` or a JSCalendar `showWithoutTime` of true SHALL become an all-day placement whose `start` is that calendar day; on export an all-day placement SHALL be written back in that form. On import, an iCalendar `DTSTART` whose `TZID` is an IANA time zone name, or a JSCalendar event whose `timeZone` is one, SHALL give a datetime placement `start` carrying that name as its RFC 9557 time-zone suffix, with the offset the event gives at that instant; a UTC start, or a `TZID` that is not an IANA name, SHALL give a `start` with an offset and no suffix. On export, a `start` carrying a suffix SHALL be written as a local time in that zone, as iCalendar `DTSTART;TZID=` or JSCalendar `start` with `timeZone`, and a `start` without one as today; the exporter supplies whatever zone definition the external format requires. No other metadata SHALL cross the boundary.

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

#### Scenario: Hold is not a commitment
- **WHEN** an imported event's `uid` matches an intention's `external`
- **THEN** no commitment is created for it

#### Scenario: Attendee metadata beyond address and status dropped
- **WHEN** an imported event's attendee carries `CN`, `RSVP`, `CUTYPE` and `DELEGATED-TO`
- **THEN** the commitment's party entry for that attendee carries only its `uri` and `status`

#### Scenario: Zone imported
- **WHEN** an iCalendar event with `DTSTART;TZID=Australia/Melbourne:20260915T100000` is imported
- **THEN** the commitment's `placement.start` is `2026-09-15T10:00:00+10:00[Australia/Melbourne]`

#### Scenario: Non-IANA TZID
- **WHEN** an iCalendar event with `DTSTART;TZID=AUS Eastern Standard Time:20260915T100000` is imported
- **THEN** the commitment's `placement.start` carries the offset its `VTIMEZONE` gives and no suffix

#### Scenario: Zone exported
- **WHEN** a commitment whose `placement.start` is `2026-09-15T10:00:00+10:00[Australia/Melbourne]` is exported to JSCalendar
- **THEN** the event carries `start: 2026-09-15T10:00:00` and `timeZone: Australia/Melbourne`

#### Scenario: Re-import with only a zone change
- **WHEN** a commitment imported with an offset-only start is re-imported and the event now names the same instant with an IANA `TZID`
- **THEN** the commitment's `start` gains the suffix and its version is unchanged
