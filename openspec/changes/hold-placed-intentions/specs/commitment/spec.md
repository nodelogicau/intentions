## MODIFIED Requirements

### Requirement: External reference only

A commitment's `external.uid` SHALL be the only link between it and an external calendar object; a placed intention with no `parties` MAY carry its own link to a hold (see Calendar hold in Intention), and every other object type SHALL carry none. The external object's recurrence, timezone definitions, alarms, and attendee metadata SHALL NOT be copied into the commitment. A recurring external event SHALL be imported as one commitment per occurrence the importer chooses to bring in, each carrying the same `uid` plus the occurrence's placement. On import, a JSCalendar `locations` or `virtualLocations` entry, or an iCalendar `LOCATION`, that carries a URI SHALL become `placement.location`; on export `placement.location` SHALL be written to the corresponding property. On import, an iCalendar `TRANSP:TRANSPARENT` or a JSCalendar `freeBusyStatus` of `free` SHALL become `transparent: true`; on export a transparent commitment SHALL be written with `TRANSP:TRANSPARENT` or `freeBusyStatus: free` and an opaque one with `TRANSP:OPAQUE` or `freeBusyStatus: busy`. On import, an iCalendar `DTSTART` of value type `DATE` or a JSCalendar `showWithoutTime` of true SHALL become an all-day placement whose `start` is that calendar day; on export an all-day placement SHALL be written back in that form. No other metadata SHALL cross the boundary.

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
