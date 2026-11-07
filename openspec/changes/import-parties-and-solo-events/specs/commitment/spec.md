## MODIFIED Requirements

### Requirement: Two origins

A commitment SHALL arise either endogenously from a RESOLUTION, in which case consistency with availability and intention holds by construction at creation, or exogenously by import from an external calendar, in which case consistency SHALL be checked at creation and any clash flagged. An imported commitment SHALL NOT create an intention or availability. Its `parties` SHALL be mapped from the event as Parties on import states, and it SHALL be created without `intention`; a person MAY later adopt it for an intention (see Adopting an imported commitment).

#### Scenario: Import clashes with availability
- **WHEN** an iCalendar event is imported whose placement falls outside the person's declared availability
- **THEN** the commitment is created with all parties as the import states them and carries a `window-clash` flag

#### Scenario: Import names no intention
- **WHEN** any event is imported
- **THEN** the commitment carries no `intention`, whatever the event's title or time

### Requirement: External reference only

A commitment's `external.uid` SHALL be the only link between it and an external calendar object; a placed intention with no `parties` MAY carry its own link to a hold (see Calendar hold in Intention), and every other object type SHALL carry none. The external object's recurrence, timezone definitions, alarms, and attendee metadata SHALL NOT be copied into the commitment, except each participant's calendar address and participation status, which become `parties` as Parties on import states. A recurring external event SHALL be imported as one commitment per occurrence the importer chooses to bring in, each carrying the same `uid` plus the occurrence's placement. On import, a JSCalendar `locations` or `virtualLocations` entry, or an iCalendar `LOCATION`, that carries a URI SHALL become `placement.location`; on export `placement.location` SHALL be written to the corresponding property. On import, an iCalendar `TRANSP:TRANSPARENT` or a JSCalendar `freeBusyStatus` of `free` SHALL become `transparent: true`; on export a transparent commitment SHALL be written with `TRANSP:TRANSPARENT` or `freeBusyStatus: free` and an opaque one with `TRANSP:OPAQUE` or `freeBusyStatus: busy`. On import, an iCalendar `DTSTART` of value type `DATE` or a JSCalendar `showWithoutTime` of true SHALL become an all-day placement whose `start` is that calendar day; on export an all-day placement SHALL be written back in that form. No other metadata SHALL cross the boundary.

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

## ADDED Requirements

### Requirement: Parties on import

An import SHALL be made on behalf of one subject: the workspace's `defaults.subject` unless the import names another. Each iCalendar `ATTENDEE` and the `ORGANIZER`, and each JSCalendar `participants` entry with a calendar address in `sendTo` (`imip` if present, otherwise the first method in key order), SHALL become one party, except an entry whose iCalendar `ROLE` is `NON-PARTICIPANT` or whose JSCalendar `roles` hold only `informational`, and an entry with no calendar address. A party's `uri` SHALL be the subject URI under which `calendar.addresses` lists that address (see Workspace configuration in Object model), or else the address itself, a `mailto:` address lowercased in full. Entries mapping to one `uri` SHALL give one party, taking an attendee entry's status over an organizer's.

A party's `status` SHALL be mapped from iCalendar `PARTSTAT` or JSCalendar `participationStatus`: `ACCEPTED` to `accepted`; `TENTATIVE`, `NEEDS-ACTION`, or absent to `tentative`; `DECLINED` and `DELEGATED` to `declined`. An organizer with no attendee entry SHALL be `accepted`.

The subject SHALL always be a party. Where the event names the subject, their status SHALL be mapped as above; where the event names no organizer and no attendee, the subject SHALL be `accepted`; where it names others but not the subject, the subject SHALL be `tentative`. No other attendee or participant property SHALL cross.

Each import of an event SHALL apply this mapping. A status changed on re-import SHALL be taken as that party's act as it reached the calendar: for another party, their reply; for the subject, their own act in their calendar.

#### Scenario: Meeting with attendees
- **WHEN** an event is imported whose `ORGANIZER` is `mailto:Alex@Example.com` with no attendee entry and whose attendees are `mailto:ben@example.org` (`PARTSTAT=ACCEPTED`) and `mailto:sam@example.com` (`PARTSTAT=NEEDS-ACTION`), and `calendar.addresses` lists `mailto:ben@example.org` under `https://example.org/people/ben`
- **THEN** the commitment's `parties` are `https://example.org/people/ben` at `accepted`, `mailto:alex@example.com` at `accepted`, and `mailto:sam@example.com` at `tentative`, sorted by `uri`

#### Scenario: Ticket with no attendees
- **WHEN** an event naming no organizer and no attendee is imported for subject `https://example.org/people/ben`
- **THEN** the commitment's only party is `https://example.org/people/ben` at `accepted`

#### Scenario: Non-participant not a party
- **WHEN** an imported event carries an attendee with `ROLE=NON-PARTICIPANT`
- **THEN** that attendee is not among the commitment's `parties`

#### Scenario: Delegated attendee
- **WHEN** an imported attendee carries `PARTSTAT=DELEGATED` and the delegate is also an attendee at `NEEDS-ACTION`
- **THEN** the delegator is `declined` and the delegate is `tentative`

#### Scenario: Reply arrives by re-import
- **WHEN** an event is re-imported and another party's `PARTSTAT` has changed from `NEEDS-ACTION` to `ACCEPTED`
- **THEN** that party's entry becomes `accepted`, the commitment's version changes, and `intention` is unchanged

#### Scenario: Two importers agree
- **WHEN** two conforming importers import the same event into workspaces with the same configuration
- **THEN** the two commitments carry the same `parties` and the same version

### Requirement: Adopting an imported commitment

A person MAY adopt an unretired commitment whose `origin` is `import` for an unretired INTENTION, declaring that the event is that intention's occasion. Adopting SHALL be a selection (see Selection is a recorded act in Resolution): it SHALL write a RESOLUTION record with `selector: person` and the commitment's placement, give the intention that placement, and set the commitment's `intention` to the intention's id, in one act. The commitment's `origin` SHALL stay `import`, and it SHALL NOT gain `resolution`. A harness MAY perform the act on the person's instruction, recorded in `source.harness`, and SHALL NOT adopt under a policy.

Adopting SHALL be refused unless the intention's `subject` is one of the commitment's parties, the intention has no `parties`, the intention carries no `external`, and no other unretired commitment names the intention. Validation SHALL report each of these as an error where a merged workspace contains it. A re-import SHALL NOT clear or change a commitment's `intention`.

Where an adopted commitment's placement and its intention's placement differ, validation SHALL report a warning naming both, with adopting again as the fix. Cancelling an adopted commitment SHALL clear the intention's placement, as Cancellation states for any commitment.

#### Scenario: Concert planned and ticketed
- **WHEN** the person adopts the imported commitment for a concert, whose only party is the subject at `accepted`, for an unplaced intention of that subject with no `parties`
- **THEN** a resolution record with `selector: person` and the commitment's placement is written, the intention gains that placement, the commitment carries `intention`, keeps `origin: import`, and changes version, and no `window-clash` arises between them

#### Scenario: Intention with a hold
- **WHEN** the person adopts an imported commitment for an intention carrying `external`
- **THEN** the act is refused, naming `external` as the field to clear first

#### Scenario: Intention with parties
- **WHEN** the person adopts an imported commitment for an intention with `parties`
- **THEN** the act is refused, since that intention gets its commitment by resolution

#### Scenario: Event moved
- **WHEN** an adopted commitment is re-imported with a later start
- **THEN** it keeps `intention`, the intention keeps its placement, and validation warns that the two placements differ

#### Scenario: Venue cancels
- **WHEN** the person cancels an adopted commitment
- **THEN** the intention's placement is cleared and the intention may be resolved again
