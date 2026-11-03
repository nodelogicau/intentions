## MODIFIED Requirements

### Requirement: Intention fields

An INTENTION SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); optional `firmed_under` (the id of the policy under which a harness set `firm`); optional `activity`; optional `location` (a list of absolute URIs at one of which the intention must happen; absent means anywhere); optional `parties` (bare URIs of other required particulars, whose availability resolution must satisfy; a different shape from a commitment's `parties`, which carry a status); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `habit` (boolean, default false; recurring intentions only, see Habit); optional `occurrence` (on generated instances only); optional `placement`; optional `external` (`{system: icalendar|jscalendar, uid}`, the link to the calendar hold written for the placement; see Calendar hold); optional `preference` (see Resolution); optional `auto_select` and `auto_firm` (termini only); optional `reference` (informal pointer to a DKF claim); `source`; `timestamp`; `acknowledgements` (see Consistency); and at most one `retired` record.

The scheduling projection of an INTENTION SHALL be: `subject`, `duration`, `window`, `stability`, `activity`, `location`, `parties`, `serves`, `cadence`, `habit`, `occurrence`, `placement`, `retired.kind`. `version`, `firmed_under` and `external` are not in it. `habit` is in the projection only under `intentions/0.2`, which admitted it after files carried that string (see Versioning by projection hash in Object model). The `intentions/0.1` projection is the same list without `habit`.

#### Scenario: Minimal intention
- **WHEN** an intention is written with only `title` and `stability: tentative` in a workspace with default `subject` and `source.author`
- **THEN** it is valid, the file carries `version` after `id`, the default `subject`, `source.author`, and a `timestamp`, it carries no window or duration, and it cannot be resolved until it has both

#### Scenario: Subject without default
- **WHEN** an intention is written without `subject` in a workspace with no `defaults.subject`
- **THEN** the write is refused

#### Scenario: Own supply is by subject
- **WHEN** an intention with `subject: https://example.org/people/ben` is resolved
- **THEN** its own supply is the eligible availability whose `subject` is that URI

#### Scenario: Habit changes the version
- **WHEN** the person sets `habit: true` on a recurring intention
- **THEN** the file carries `habit` immediately after `cadence` and the intention's version changes

#### Scenario: Hold link does not change the version
- **WHEN** a harness sets `external` on a placed intention with no `parties`
- **THEN** the file carries `external` immediately after `placement` and the intention's version is unchanged

## ADDED Requirements

### Requirement: Calendar hold

A placed INTENTION with no `parties` MAY carry `external` (`{system: icalendar|jscalendar, uid}`), recording the event written to the person's calendar as a busy hold for its placement. It SHALL be the only link between the intention and that event, with the same shape and meaning as a commitment's `external`. An intention with `parties` SHALL NOT carry `external`: on selection it gets a COMMITMENT, and its hold is the commitment's. `external` SHALL NOT be present without `placement`, and no two intentions SHALL carry the same `system` and `uid`. A write that adds `parties` to an intention carrying `external` SHALL be refused unless the same write clears `external`. A write setting or clearing `external` MAY carry a harness and needs no policy.

A hold SHALL be exported with only: the placement's start and duration, in all-day form for an all-day placement; `placement.location` where it is a URI, written to the location property as for a commitment; the intention's `title` as iCalendar `SUMMARY` or JSCalendar `title`; `TRANSP:OPAQUE` or `freeBusyStatus: busy`, always, since an intention is never transparent; and `STATUS:TENTATIVE` or JSCalendar `status: tentative` for `stability: tentative`, `STATUS:CONFIRMED` or `status: confirmed` for `firm`. No other field SHALL cross the boundary.

On import, an external event whose `system` and `uid` match any intention's `external`, retired or not, SHALL be recognised as that intention's hold and SHALL NOT create a commitment.

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
