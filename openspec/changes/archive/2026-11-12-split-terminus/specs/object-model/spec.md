## MODIFIED Requirements

### Requirement: Retirement is an appended record, never deletion

An object SHALL be retired by appending a single `retired` record to it, never by deleting its file and never by a status field. The record SHALL carry `kind` (per object type), optional `reason` (prose), `superseded_by` (required when and only when `kind` is `superseded`; an id, or on a terminus a list of two or more ids, see Retirement kinds in Intention), `adopted_as` (on a DESIRE, required when and only when `kind` is `adopted`, naming the INTENTION it became), `timestamp`, and `source`. Kinds are per type: intention `fulfilled`, `abandoned`, `superseded`, of which a terminus admits only `abandoned` and `superseded`; availability `retracted`, `superseded`; commitment `cancelled`; desire `abandoned`, `superseded`, `adopted`. An object with no `retired` record is active; no `status` field SHALL exist on any object. A retired object SHALL NOT be edited further, except that acknowledgement records MAY still be appended to it. `retired.kind` SHALL be part of the object's scheduling projection; `reason`, `superseded_by`, `adopted_as`, `timestamp`, and `source` SHALL NOT.

#### Scenario: Deletion attempted
- **WHEN** a tool is asked to remove an intention
- **THEN** it appends a `retired` record and refuses to delete the file

#### Scenario: Second retirement refused
- **WHEN** an object already carrying a `retired` record is retired again
- **THEN** the write is refused

#### Scenario: Retirement changes version
- **WHEN** a `retired` record is appended to an active intention
- **THEN** its version changes and it no longer participates in any flag as a live counterpart

#### Scenario: Adopted names an intention
- **WHEN** a DESIRE is retired with `kind: adopted` and `adopted_as` naming an availability
- **THEN** validation reports an error

#### Scenario: Terminus kinds
- **WHEN** a terminus is retired with `kind: fulfilled`
- **THEN** the write is refused

#### Scenario: List on a desire
- **WHEN** a DESIRE is retired with `kind: superseded` and `superseded_by` a list
- **THEN** validation reports an error

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active, firm policy of the intention's subject, `firmed_under` on a terminus, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, `habit` on an intention without `cadence`, `habit` in a workspace whose `format` is `intentions/0.1` (named with `migrate` as the fix), a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, a DESIRE carrying any field of an intention's temporal or deontic kind (`duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, `acknowledgements`), a DESIRE `serves` entry with any role but `for-the-sake-of`, `adopted` without `adopted_as` or `adopted_as` naming anything but an intention, `superseded_by` on a desire naming anything but a desire, `fulfilled` on a terminus, `superseded_by` on a terminus naming or listing anything but a terminus of its subject, a list-valued `superseded_by` on any object but a terminus, a list-valued `superseded_by` with fewer than two entries or a repeated entry, `transparent` on a commitment born of a resolution, `external` on an intention with no `placement`, `external` on an intention with `parties`, two intentions carrying the same `external` `system` and `uid`, an imported commitment naming an intention whose `subject` is not one of its parties, an imported commitment naming an intention with `parties`, an imported commitment naming an intention that carries `external`, two unretired commitments naming one intention, an RFC 9557 suffix on a placement `start` that is not a bare IANA zone name (an offset-form suffix or any other suffix tag), the critical flag `!` on such a suffix, and a time-zone suffix on a calendar-day `start` or on any datetime other than a placement's `start`. Under `intentions/0.2` errors SHALL also include an intention that reaches no firm terminus of its own subject, named with the fix; under `intentions/0.1` that finding is a warning. Warnings SHALL include an unretired intention with an `in-order-to` or `instance-of` link to an intention retired as `abandoned`, naming the abandoned end; and a RESOLUTION record whose `selector` names a policy that is no longer firm or no longer active, as an act authorised when it happened under a policy since withdrawn; the placement it produced stands and is the person's to keep or re-resolve; and an intention, retired or not, whose `external` `system` and `uid` match an unretired commitment's `external`, naming both and the two fixes: if the commitment is the intention's own hold imported before it was recognised, retire the commitment as `cancelled`; if it is a real event that shares the UID, clear the intention's `external`; and an unretired imported commitment naming an intention whose placement differs from its own, naming both, with adopting again as the fix; a placement whose `start` carries an offset that differs from the offset its time-zone suffix gives at that instant in the reader's time-zone database, naming the object, both offsets, and a replacing selection as the fix that restores the local time it was placed at; and a placement whose time-zone suffix names a zone the reader's time-zone database does not know, naming the zone. Info SHALL include a tentative terminus, as a draft; an unretired intention with a `serves` entry whose supersession chain from its target passes through a terminus superseded by a list, naming the intention, that terminus and its successors, with re-pointing the entry to the successor or successors it is for as the fix; an unretired imported commitment whose only party is one particular and which names no intention and shares no `external` with an intention, as a commitment directed at no one that may be better recorded as an intention and adopted; and a workspace holding imported commitments whose `intentions.yaml` declares no `calendar.addresses`. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

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

#### Scenario: Dependent of a split
- **WHEN** A serves T `for-the-sake-of`, and T is superseded by `[U, V]`, both firm
- **THEN** validation reports A at info level, naming T, U and V and re-pointing as the fix, and does not exit non-zero for it

#### Scenario: Re-pointed dependent
- **WHEN** A, which served a split terminus T, is edited to serve U `for-the-sake-of` and no longer names T
- **THEN** validation reports nothing about A, and T's record still lists U and V

#### Scenario: One-to-one supersession is quiet
- **WHEN** A serves T `for-the-sake-of`, and T is superseded by the single firm terminus U
- **THEN** validation reports nothing about A
