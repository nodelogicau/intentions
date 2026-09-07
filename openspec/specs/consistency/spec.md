# Consistency

## Purpose

Defines the consistency check, its flags, and acknowledgements. The check surfaces every way the prospective graph fails to hang together: overlaps, mismatched conditions, expired grounds, mutually unsatisfiable intentions, and cycles. It never decides; it makes the imposition visible so the person can contest or accept it. Philosophically this is how the specification protects resoluteness against the schedule silently filling with other people's claims on one's time.

Flags are derived and recomputed. What persists is the person's acknowledgement.

## Requirements

### Requirement: Flag kinds

A flag SHALL have exactly one `kind` from: `window-clash` (two placements overlap while sharing a party whom both occupy, occupancy being by each party's own entry, or a placement falls in a window with no eligible supply), `condition-mismatch` (the availability supplying a placement has a conditional that does not include the intention's activity), `location-mismatch` (the availability supplying a placement has a location list that does not include the placement's location, or the placement's location is not in the intention's location list), `expired-ground` (an availability the placement rests on has passed its horizon or been retired), `intention-inconsistency` (two active unplaced intentions of one subject, each with duration and window and with intersecting resolution ranges, each have candidates alone but no pair of non-overlapping candidates exists; the check is pairwise and never global), `party-declined` (a commitment has a party at `declined` while the intention it fulfils is still placed), and `cycle` (the intention is in a strongly-connected component of the serves graph). Flags SHALL NOT carry a numeric severity.

Whether the workspace tracks a party's availability SHALL make no difference to `window-clash`: a party's placements clash whether or not the workspace holds any capacity for them.

#### Scenario: Kinds are exhaustive
- **WHEN** a consistency check finds a problem
- **THEN** it is reported under exactly one of the seven kinds

#### Scenario: Imported meeting elsewhere
- **WHEN** an imported commitment carries `placement.location: office` and the subject's availability for that window carries `location: [home]`
- **THEN** the commitment carries a `location-mismatch` flag and its party statuses are unchanged

#### Scenario: Pairwise inconsistency
- **WHEN** two unplaced intentions of one subject each fit the subject's single three-hour occasion alone but not together
- **THEN** both carry an `intention-inconsistency` flag naming the other, with `detail` saying the check is pairwise

#### Scenario: Three-way infeasibility not reported
- **WHEN** three unplaced intentions each fit an occasion in pairs but not all three together
- **THEN** no `intention-inconsistency` flag is reported

#### Scenario: Overlap without a shared party
- **WHEN** two commitments overlap in time and share no party
- **THEN** no `window-clash` is reported between them

#### Scenario: Overlap on an untracked party
- **WHEN** two commitments overlap and both carry the same untracked external party at `tentative`
- **THEN** a `window-clash` is reported on both, naming the shared party in `detail`

### Requirement: Flag shape

A flag SHALL carry `kind`, `subject` (the id of the object the flag is reported on), `counterpart` (the id of the other object involved, or absent for `cycle` and for `window-clash` against absent supply), `counterpart_version` (the counterpart's projection hash at check time), and a human-readable `detail`.

#### Scenario: Clash between two objects
- **WHEN** commitment cmt_X overlaps intention int_Y
- **THEN** a `window-clash` flag is reported on cmt_X with counterpart int_Y and on int_Y with counterpart cmt_X

### Requirement: Flags are computed, not stored

Flags SHALL be computed by the consistency check from the current workspace and SHALL NOT be written to any object file. A check SHALL run on: creation or projection change of a commitment; projection change of an availability or intention; every resolution; and on demand.

#### Scenario: No flag file
- **WHEN** a consistency check reports flags
- **THEN** no object file is modified and a second run on the unchanged workspace reports the same flags

### Requirement: Acknowledgements are stored

An ACKNOWLEDGEMENT SHALL be an entry in the `acknowledgements` list of the intention or commitment it concerns, with fields `kind`, `counterpart` (id, or absent where the flag has none), `counterpart_version`, `reason` (prose), `timestamp`, and `source`. The list SHALL be append-only. Acknowledgements are excluded from the scheduling projection.

#### Scenario: Acknowledge a clash
- **WHEN** a person acknowledges the window-clash between cmt_X and int_Y with a reason
- **THEN** an acknowledgement is appended to cmt_X recording kind, counterpart int_Y, int_Y's current version, the reason, the time, and the person as `source.author`

#### Scenario: Acknowledgement on a retired object
- **WHEN** an acknowledgement is appended to an intention that carries a `retired` record
- **THEN** the append is accepted and no other field of the intention changes

### Requirement: Suppression and lapse

A computed flag SHALL be suppressed when its subject carries an acknowledgement with the same `kind`, the same `counterpart`, and a `counterpart_version` equal to the counterpart's current projection hash. If the counterpart's projection has changed since, the acknowledgement SHALL be treated as lapsed and the flag SHALL be reported again. Lapsed acknowledgements SHALL remain in the list.

#### Scenario: Suppressed
- **WHEN** an acknowledged clash is rechecked and the counterpart is unchanged
- **THEN** the flag is not reported

#### Scenario: Lapsed
- **WHEN** the counterpart's window is edited after acknowledgement
- **THEN** the flag is reported again and the old acknowledgement is retained

#### Scenario: Prose edit does not lapse
- **WHEN** only the counterpart's description is edited after acknowledgement
- **THEN** the flag remains suppressed

### Requirement: Consistency never changes state

A consistency check SHALL NOT retire any object, nor change any object's stability, placement, or party status. Its only outputs are flags.

#### Scenario: Inconsistent intentions
- **WHEN** two firm intentions cannot both be placed
- **THEN** both carry an `intention-inconsistency` flag and neither gains a `retired` record

### Requirement: Acknowledgement as retrospective seed

An acknowledgement's `reason` and identifiers SHALL be sufficient for a DKF claim to be written about the decision later, citing the acknowledging object by id and version. This specification SHALL NOT write that claim.

#### Scenario: Citable acknowledgement
- **WHEN** a DKF user recalls why a clash was accepted
- **THEN** the acknowledgement entry identifies the objects, their versions at the time, and the stated reason

### Requirement: Transparent commitments occupy no time and rest on no supply

A commitment with `transparent: true` SHALL NOT be the subject or the counterpart of a `window-clash` flag, because it occupies none of the subject's time, and SHALL NOT be the subject of a `condition-mismatch`, `location-mismatch`, or `expired-ground` flag, because it rests on no availability. A transparent commitment SHALL NOT count as eligible supply for anything and SHALL NOT remove supply from anything. Its party statuses, acknowledgements, and retirement behave as for any commitment.

#### Scenario: Conference week does not clash
- **WHEN** an imported commitment with `transparent: true` spans 21 to 25 September and a firm intention is placed on 23 September
- **THEN** no `window-clash` is reported on either object

#### Scenario: Transparent import outside availability
- **WHEN** an imported commitment with `transparent: true` falls in a window where the subject has no eligible availability
- **THEN** no `window-clash` and no `expired-ground` is reported on it

#### Scenario: Opaque import still clashes
- **WHEN** an imported commitment with no `transparent` field overlaps a placed intention
- **THEN** a `window-clash` is reported on both

### Requirement: What a placement rests on is recomputed

At check time a placement SHALL rest on every occasion, of each particular involved in it, that contains the placement. No containing occasion for some involved particular SHALL be reported as `window-clash` without counterpart. Where containing occasions exist but every one fails eligibility, the failure SHALL be reported by its kind: a retired or expired occasion as `expired-ground`, a conditional that excludes the activity as `condition-mismatch`, a location list that excludes the placement's location as `location-mismatch`. Nothing stored on the placement, the intention, or the RESOLUTION record SHALL be used to decide what a placement rests on.

#### Scenario: Availability replaced after selection
- **WHEN** the availability named in a resolution's `supply` is superseded by one that still contains the placement
- **THEN** the next check finds the placement resting on the new availability and reports nothing

#### Scenario: Only containing occasion expired
- **WHEN** the only occasion containing a placement has passed its validity horizon
- **THEN** the placement carries `expired-ground`, not `window-clash`

#### Scenario: No containing occasion
- **WHEN** no occasion of the subject contains a placement
- **THEN** the placement carries `window-clash` with no counterpart

### Requirement: A decline against a standing plan is flagged

A `party-declined` flag SHALL be reported when a commitment has any party at `declined` and the intention it fulfils still carries a placement. It SHALL be reported on both the commitment and that intention, each naming the other as counterpart, and its `detail` SHALL name the declining party and whether that party is the intention's subject. A commitment with no `intention`, which is every imported commitment, SHALL NOT raise it, because there is no plan for the decline to disagree with. A commitment whose intention's placement has been cleared SHALL NOT raise it.

The flag SHALL NOT change any party status, clear any placement, or retire anything. It is acknowledgeable like any other flag, and because a party status is in the commitment's projection, a later change to it lapses the acknowledgement and the flag is recomputed.

#### Scenario: Subject declines their own arrangement
- **WHEN** the subject sets their own party entry to `declined` on a commitment created from their placed intention
- **THEN** a `party-declined` flag is reported on the commitment and on the intention, the placement is unchanged, and the detail says the declining party is the subject

#### Scenario: Counterparty declines
- **WHEN** a counterparty declines a commitment whose intention is still placed
- **THEN** the same flag is reported on both objects and the detail names that party as not the subject

#### Scenario: Imported commitment declined
- **WHEN** the subject declines an imported commitment, which has no `intention`
- **THEN** no `party-declined` flag is reported and the hour is no longer occupied for them

#### Scenario: Cancelled, not declined
- **WHEN** the commitment is cancelled, clearing the intention's placement
- **THEN** no `party-declined` flag is reported

#### Scenario: Acknowledged and carried on
- **WHEN** a person acknowledges a `party-declined` flag naming a counterparty
- **THEN** the flag is suppressed, the placement stands, and no status changes

#### Scenario: Acknowledgement lapses on a reversal
- **WHEN** an acknowledged declining party later sets their status to `accepted`
- **THEN** the commitment's projection changes, the acknowledgement lapses, and the flag is not reported because no party is declined
