# Consistency

## Purpose

Defines the consistency check, its flags, and acknowledgements. The check surfaces every way the prospective graph fails to hang together: overlaps, mismatched conditions, expired grounds, mutually unsatisfiable intentions, and cycles. It never decides; it makes the imposition visible so the person can contest or accept it. Philosophically this is how the specification protects resoluteness against the schedule silently filling with other people's claims on one's time.

Flags are derived and recomputed. What persists is the person's acknowledgement.

## Requirements

### Requirement: Flag kinds

A flag SHALL have exactly one `kind` from: `window-clash` (a placement overlaps another placement or falls in a window with no eligible supply), `condition-mismatch` (the availability supplying a placement has a conditional that does not include the intention's activity), `expired-ground` (an availability the placement rests on has passed its horizon or been retracted), `intention-inconsistency` (two active intentions cannot both be placed within their windows given available supply), and `cycle` (the intention is in a strongly-connected component of the serves graph). Flags SHALL NOT carry a numeric severity.

#### Scenario: Kinds are exhaustive
- **WHEN** a consistency check finds a problem
- **THEN** it is reported under exactly one of the five kinds

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

An ACKNOWLEDGEMENT SHALL be an entry in the `acknowledgements` list of the intention or commitment it concerns, with fields `kind`, `counterpart` (id, or absent where the flag has none), `counterpart_version`, `reason` (prose), and `timestamp`. The list SHALL be append-only. Acknowledgements are excluded from the scheduling projection.

#### Scenario: Acknowledge a clash
- **WHEN** a person acknowledges the window-clash between cmt_X and int_Y with a reason
- **THEN** an acknowledgement is appended to cmt_X recording kind, counterpart int_Y, int_Y's current version, the reason, and the time

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

A consistency check SHALL NOT change any object's status, stability, placement, or party status. Its only outputs are flags.

#### Scenario: Inconsistent intentions
- **WHEN** two firm intentions cannot both be placed
- **THEN** both carry an `intention-inconsistency` flag and neither is retired

### Requirement: Acknowledgement as retrospective seed

An acknowledgement's `reason` and identifiers SHALL be sufficient for a DKF claim to be written about the decision later, citing the acknowledging object by id and version. This specification SHALL NOT write that claim.

#### Scenario: Citable acknowledgement
- **WHEN** a DKF user recalls why a clash was accepted
- **THEN** the acknowledgement entry identifies the objects, their versions at the time, and the stated reason
