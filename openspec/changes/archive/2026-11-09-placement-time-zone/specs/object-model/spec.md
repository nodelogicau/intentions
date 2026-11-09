## MODIFIED Requirements

### Requirement: Versioning by projection hash

Every object SHALL have a version, defined as the hash of a canonical serialisation of that object's *scheduling projection*: the subset of its fields that bear on consistency checking, as enumerated in each object type's specification and frozen per format version. A projection SHALL be frozen from the moment any implementation writes the format version string into a file, not from any declaration; a change to any projection SHALL be a new format version, with one named exception. `habit` joined the INTENTION projection of `intentions/0.2` after files carried that string. It was admitted because it is optional and omitted at its documented default, so no existing hash moved. No other field SHALL be admitted this way: every further change to any projection, including another field omitted at its default, SHALL be a new format version. A reader older than an admitted field computes a different version for any object carrying it at a non-default value and does not apply its semantics, so a stored `counterpart_version` stays comparable only between readers that agree on the admitted fields. Prose fields (title, description, notes), `source`, `timestamp`, `version`, `firmed_under`, an intention's `external`, acknowledgement records, and the `reason`, `timestamp`, and `source` of a `retired` record SHALL be excluded from the projection. `retired.kind` SHALL be included.

The version SHALL be derived, never declared. The projection SHALL be expressed as a JSON object with values normalised first, serialised with the JSON Canonicalization Scheme (RFC 8785), and hashed with the algorithm named by `hash` in `intentions.yaml`. Normalisation SHALL be: EDTF expressions in shortest admitted form; ISO 8601 durations with zero components dropped, weeks folded into days (`P1W` becomes `P7D`), the time part re-expressed from its total seconds as hours, minutes and seconds (`PT90M` becomes `PT1H30M`, `PT60M` becomes `PT1H`), no conversion between the date part and the time part (`P1D` and `PT24H` stay distinct), and no conversion of months or years, with a zero duration written `P0D`; datetimes as RFC 3339 UTC with seconds, any RFC 9557 time-zone suffix dropped; every set-valued list sorted, namely references by id then role, commitment `parties` by `uri`, and string lists (`location`, `activities`, intention `parties`, `displaced`) lexically; absent optional fields omitted; and a boolean equal to its documented default omitted, so that an explicit `transparent: false` hashes as absent. The version SHALL be written as `<algorithm>:<lowercase hex>`. This version of the format admits only `sha256`.

Every object and every RESOLUTION record SHALL carry its computed version in the file under `version`, immediately after `id` in canonical order. The computed value is authoritative; validation SHALL report a warning when the written value disagrees, and tools SHALL use the computed value.

#### Scenario: Prose edit does not change version
- **WHEN** only an intention's description is edited
- **THEN** its version is unchanged

#### Scenario: Window edit changes version
- **WHEN** an intention's window is edited
- **THEN** its version changes and the `version` line in the file changes with it

#### Scenario: Stale cached version
- **WHEN** a file carries a `version` that differs from the computed value
- **THEN** validation reports a warning and tools use the computed value

#### Scenario: Source edit does not change version
- **WHEN** only an object's `source.model` is edited
- **THEN** its version is unchanged

#### Scenario: Normalisation before hashing
- **WHEN** two files carry `duration: PT1H` and `duration: PT60M`
- **THEN** their projections hash identically

#### Scenario: Date and time parts stay distinct
- **WHEN** two files carry `duration: P1D` and `duration: PT24H`
- **THEN** their projections hash differently

#### Scenario: Set order does not matter
- **WHEN** two files carry `location: [home, office]` and `location: [office, home]`
- **THEN** their projections hash identically

#### Scenario: Explicit default boolean
- **WHEN** one commitment file carries `transparent: false` and another omits `transparent`, all else equal
- **THEN** their projections hash identically

#### Scenario: Version missing
- **WHEN** an object file carries no `version`
- **THEN** validation reports a warning and a writer touching the file adds it

#### Scenario: Admitted field at its default
- **WHEN** a 0.2 reader that knows `habit` and one that predates it each hash a recurring intention that omits `habit`
- **THEN** they compute the same version

#### Scenario: Admitted field set
- **WHEN** a 0.2 reader that knows `habit` and one that predates it each hash a recurring intention carrying `habit: true`
- **THEN** they compute different versions, and the older reader reports the written version as stale

#### Scenario: No further admission
- **WHEN** a later revision of this text adds another optional field, omitted at its default, to a projection
- **THEN** that revision names a new format version

#### Scenario: Hold link is outside the projection
- **WHEN** a harness sets or replaces `external` on an intention
- **THEN** the intention's version is unchanged, its acknowledgements do not lapse, and no format version is involved

#### Scenario: Zone suffix outside the projection
- **WHEN** a placement's `start` gains, changes, or loses an RFC 9557 time-zone suffix and nothing else changes
- **THEN** the object's version is unchanged and no acknowledgement naming it lapses

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active, firm policy of the intention's subject, `firmed_under` on a terminus, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, `habit` on an intention without `cadence`, `habit` in a workspace whose `format` is `intentions/0.1` (named with `migrate` as the fix), a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, a DESIRE carrying any field of an intention's temporal or deontic kind (`duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, `acknowledgements`), a DESIRE `serves` entry with any role but `for-the-sake-of`, `adopted` without `adopted_as` or `adopted_as` naming anything but an intention, `superseded_by` on a desire naming anything but a desire, `fulfilled` on a terminus, `superseded_by` on a terminus naming anything but a terminus of its subject, `transparent` on a commitment born of a resolution, `external` on an intention with no `placement`, `external` on an intention with `parties`, two intentions carrying the same `external` `system` and `uid`, an imported commitment naming an intention whose `subject` is not one of its parties, an imported commitment naming an intention with `parties`, an imported commitment naming an intention that carries `external`, two unretired commitments naming one intention, an RFC 9557 suffix on a placement `start` that is not a bare IANA zone name (an offset-form suffix or any other suffix tag), the critical flag `!` on such a suffix, and a time-zone suffix on a calendar-day `start` or on any datetime other than a placement's `start`. Under `intentions/0.2` errors SHALL also include an intention that reaches no firm terminus of its own subject, named with the fix; under `intentions/0.1` that finding is a warning. Warnings SHALL include an unretired intention with an `in-order-to` or `instance-of` link to an intention retired as `abandoned`, naming the abandoned end; and a RESOLUTION record whose `selector` names a policy that is no longer firm or no longer active, as an act authorised when it happened under a policy since withdrawn; the placement it produced stands and is the person's to keep or re-resolve; and an intention, retired or not, whose `external` `system` and `uid` match an unretired commitment's `external`, naming both and the two fixes: if the commitment is the intention's own hold imported before it was recognised, retire the commitment as `cancelled`; if it is a real event that shares the UID, clear the intention's `external`; and an unretired imported commitment naming an intention whose placement differs from its own, naming both, with adopting again as the fix; a placement whose `start` carries an offset that differs from the offset its time-zone suffix gives at that instant in the reader's time-zone database, naming the object, both offsets, and a replacing selection as the fix that restores the local time it was placed at; and a placement whose time-zone suffix names a zone the reader's time-zone database does not know, naming the zone. Info SHALL include a tentative terminus, as a draft; an unretired imported commitment whose only party is one particular and which names no intention and shares no `external` with an intention, as a commitment directed at no one that may be better recorded as an intention and adopted; and a workspace holding imported commitments whose `intentions.yaml` declares no `calendar.addresses`. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

Where a write operation can determine that the result would fail validation with an error, it SHALL refuse the write. Where it can determine that the result would carry a warning, it SHALL accept the write and report the warning in its result. Write-time refusal is a convenience; validation is the invariant, because files may arrive by merge without passing through any write operation.

#### Scenario: Merge introduces error
- **WHEN** two branches each add one valid reference and the merged result contains a cycle
- **THEN** validation on the merged workspace reports the cycle as an error even though neither write was refused

#### Scenario: Unauthorised firming detected after the fact
- **WHEN** a merged intention carries `stability: firm`, a `source.harness`, and no `firmed_under`
- **THEN** validation reports an error naming the intention

#### Scenario: Workspace without termini under 0.1
- **WHEN** a workspace whose `format` is `intentions/0.1` holds intentions and no terminus
- **THEN** validation reports every non-terminus intention as unserved at warning level and exits zero

#### Scenario: Workspace without termini under 0.2
- **WHEN** a workspace whose `format` is `intentions/0.2` holds intentions and no terminus
- **THEN** validation reports every non-terminus intention as unserved at error level and exits non-zero

#### Scenario: Firmed under a draft
- **WHEN** an intention carries `firmed_under` naming a policy whose `stability` is `tentative`
- **THEN** validation reports an error naming the intention and the policy

#### Scenario: Selected under a policy since withdrawn
- **WHEN** a RESOLUTION record's `selector` names a policy that has since been set tentative or retired
- **THEN** validation reports a warning on the record and does not exit non-zero for it

#### Scenario: Habit on an instance
- **WHEN** a generated instance carries `habit: true`
- **THEN** validation reports an error naming the instance and the field

#### Scenario: Abandoned end
- **WHEN** an unretired intention serves `in-order-to` an intention retired as `abandoned`
- **THEN** validation reports a warning naming both and does not exit non-zero for it

#### Scenario: Habit in a 0.1 workspace
- **WHEN** a merged recurring intention in a workspace whose `format` is `intentions/0.1` carries `habit: true`
- **THEN** validation reports an error naming the intention, the field and `migrate`, and the intention's version is computed under the 0.1 projection, without `habit`

#### Scenario: Hold link on an intention with parties
- **WHEN** a merged intention with `parties` carries `external`
- **THEN** validation reports an error naming the intention and the commitment as the place for the link

#### Scenario: Hold imported before it was recognised
- **WHEN** an intention carries `external: {system: icalendar, uid: U}` and an unretired commitment with `origin: import` carries `external: {system: icalendar, uid: U}`
- **THEN** validation reports a warning naming the intention, the commitment and both fixes, and does not exit non-zero for it

#### Scenario: Cancelled duplicate is quiet
- **WHEN** the commitment sharing the intention's `external` is retired as `cancelled`
- **THEN** validation reports no warning for the pair

#### Scenario: Ticket directed at no one
- **WHEN** an unretired imported commitment's only party is the subject and it names no intention
- **THEN** validation reports it at info level, suggesting an intention that adopts it, and does not exit non-zero for it

#### Scenario: Two commitments for one intention
- **WHEN** a merged workspace holds two unretired commitments naming the same intention
- **THEN** validation reports an error naming both and the intention

#### Scenario: Offset-form zone suffix
- **WHEN** a merged placement carries `start: 2026-09-15T10:00:00+10:00[+10:00]`
- **THEN** validation reports an error naming the object and the field, and exits non-zero

#### Scenario: Critical flag
- **WHEN** a merged placement carries `start: 2026-09-15T10:00:00+10:00[!Australia/Melbourne]`
- **THEN** validation reports an error naming the object and the flag

#### Scenario: Offset and zone disagree
- **WHEN** a placement carries `start: 2026-09-15T10:00:00+11:00[Australia/Melbourne]`, and Melbourne's offset at that instant is `+10:00`
- **THEN** validation reports a warning naming the object, both offsets, and re-selection as the fix, and does not exit non-zero for it

#### Scenario: Zone unknown to the reader
- **WHEN** a placement's suffix names a zone that the reader's time-zone database does not contain
- **THEN** validation reports a warning naming the zone, the placement's instant is taken from its offset, and validation does not exit non-zero for it

### Requirement: Composition with iCalendar and JSCalendar by reference only

This specification SHALL NOT embed iCalendar or JSCalendar grammar beyond three deliberate reuses: ISO 8601 durations, RRULE-shaped cadence expressions, and the RFC 9253 temporal relation vocabulary. A COMMITMENT MAY carry an external calendar UID, and a placed INTENTION with no `parties` MAY carry the UID of the hold written for its placement; no other object type SHALL reference an external calendar object. Recurrence exception handling, timezone definitions, alarms, attendee delegation, and iTIP negotiation SHALL remain entirely in the external system. A placement's RFC 9557 time-zone suffix names a zone in the IANA time zone database and carries none of its rules; it is a reference, as a location URI is, and not a timezone definition.

#### Scenario: Imported event
- **WHEN** an iCalendar event is imported
- **THEN** exactly one COMMITMENT is created carrying the event's UID, and no WINDOW, INTENTION, or AVAILABILITY is created from it, unless the UID is an intention's hold, in which case nothing is created

#### Scenario: Zone name, not definition
- **WHEN** an iCalendar event with `DTSTART;TZID=Australia/Melbourne` and a `VTIMEZONE` for that zone is imported
- **THEN** the commitment's `placement.start` carries `[Australia/Melbourne]` and nothing of the `VTIMEZONE` is stored
