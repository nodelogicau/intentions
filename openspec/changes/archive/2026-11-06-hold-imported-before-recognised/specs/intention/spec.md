## MODIFIED Requirements

### Requirement: Calendar hold

A placed INTENTION with no `parties` MAY carry `external` (`{system: icalendar|jscalendar, uid}`), recording the event written to the person's calendar as a busy hold for its placement. It SHALL be the only link between the intention and that event, with the same shape and meaning as a commitment's `external`. An intention with `parties` SHALL NOT carry `external`: on selection it gets a COMMITMENT, and its hold is the commitment's. `external` SHALL NOT be present without `placement`, and no two intentions SHALL carry the same `system` and `uid`. A write that adds `parties` to an intention carrying `external` SHALL be refused unless the same write clears `external`. A write setting or clearing `external` MAY carry a harness and needs no policy.

A hold SHALL be exported with only: the placement's start and duration, in all-day form for an all-day placement; `placement.location` where it is a URI, written to the location property as for a commitment; the intention's `title` as iCalendar `SUMMARY` or JSCalendar `title`; `TRANSP:OPAQUE` or `freeBusyStatus: busy`, always, since an intention is never transparent; and `STATUS:TENTATIVE` or JSCalendar `status: tentative` for `stability: tentative`, `STATUS:CONFIRMED` or `status: confirmed` for `firm`. No other field SHALL cross the boundary.

On import, an external event whose `system` and `uid` match any intention's `external`, retired or not, SHALL be recognised as that intention's hold and SHALL NOT create a commitment. Recognition prevents the case only from then on: a hold imported as a commitment before it was recognised, by an older importer, or by a merge, leaves an intention and an unretired commitment sharing one `system` and `uid`, which validation SHALL report as a warning (see Validation in Object model). A write that sets `external` to a `system` and `uid` an unretired commitment already carries SHALL be accepted and SHALL report that warning.

A replacing selection SHALL keep `external`, so the same event is moved to the new placement. Retirement SHALL keep `external`. A harness SHOULD release the hold of an intention retired as `abandoned` or `superseded`, and SHOULD leave the hold of one retired as `fulfilled`.

#### Scenario: Hold for a solo placement
- **WHEN** a placement is selected for an intention with no `parties` and a harness writes a busy hold for it to iCalendar
- **THEN** no commitment is created, the intention carries `external: {system: icalendar, uid: <the event's UID>}`, and its version is unchanged

#### Scenario: Hold export shape
- **WHEN** a tentative intention with an all-day placement on 2026-11-10 and `placement.location` of `https://example.org/places/office` is exported as a hold to iCalendar
- **THEN** the event carries `DTSTART;VALUE=DATE:20261110`, a `LOCATION` with that URI, `SUMMARY` set to the title, `TRANSP:OPAQUE` and `STATUS:TENTATIVE`, and no description

#### Scenario: Own hold not imported
- **WHEN** a harness imports from the calendar it wrote a hold to, and the hold's UID matches an intention's `external`
- **THEN** no commitment is created for that event and no `window-clash` arises

#### Scenario: Hold imported before it was recognised
- **WHEN** a harness records `external` on an intention whose hold was imported as a commitment before the import check existed
- **THEN** the write is accepted, the result reports the warning naming the commitment, and the person may retire the commitment as `cancelled` without touching the intention

#### Scenario: Re-selection moves the hold
- **WHEN** a replacing selection is made for a placed intention carrying `external`
- **THEN** the intention carries the new placement and the same `external`

#### Scenario: Intention with parties
- **WHEN** a write sets `external` on an intention with `parties`
- **THEN** the write is refused, naming the commitment as the place for the link

#### Scenario: Gaining parties
- **WHEN** a write adds `parties` to an intention carrying `external` without clearing it
- **THEN** the write is refused

#### Scenario: Abandoned with a hold
- **WHEN** an intention carrying `external` is retired as `abandoned`
- **THEN** it keeps `external`, and the harness releases the hold without writing to the workspace
