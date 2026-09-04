# Object Model

## Purpose

Defines the storage, identity, reference, mutability, versioning, and validation rules shared by every object type in the intentions specification (WINDOW, DURATION, INTENTION, AVAILABILITY, RESOLUTION, COMMITMENT, ACKNOWLEDGEMENT), and the boundaries between this specification and the two systems it composes with: the Dialectical Knowledge Format (DKF) for the retrospective, contested, evidential layer, and iCalendar/JSCalendar for interpersonal calendar interchange.

The specification is standalone. It owns all prospective and temporal structure natively and composes with other systems by external reference only, never by shared object model.

## Requirements

### Requirement: File-per-object YAML storage

Each object SHALL be stored as exactly one YAML file, in a directory named for its object type, under a workspace root identified by an `intentions.yaml` configuration file. A file SHALL contain only the object it names.

#### Scenario: Object written
- **WHEN** an intention is created
- **THEN** one file `intentions/<id>.yaml` is written under the workspace root and no other file is modified except a derived index

#### Scenario: Workspace located
- **WHEN** a tool is invoked in a directory
- **THEN** it uses the nearest ancestor directory containing `intentions.yaml` as the workspace root, and fails with a distinct exit code if none exists

### Requirement: Identifiers

Every object SHALL have an `id` composed of a type prefix, an underscore, and a UUIDv7. The prefix SHALL be `int` for intentions, `avl` for availability, `res` for resolutions, `cmt` for commitments. WINDOW and DURATION are values embedded in their carrying object and SHALL NOT have ids of their own. Ids SHALL be immutable and SHALL remain resolvable for the life of the workspace, including after retirement.

#### Scenario: Reference to a retired object
- **WHEN** an object references an intention whose status is `abandoned`
- **THEN** the reference still resolves and validation does not report it as dangling

### Requirement: Outbound references only

An object SHALL store only its own outbound references, as a list of `{id, role}` entries. No object SHALL store inbound links. Any graph over objects (the intention serves graph, the window anchoring graph, commitment-to-intention links) SHALL be reconstructed by walking outbound references.

#### Scenario: Graph reconstruction
- **WHEN** a tool needs every intention that serves intention X
- **THEN** it derives them by scanning outbound `serves` references that target X, not by reading a stored inbound list on X

#### Scenario: Dangling reference
- **WHEN** an outbound reference targets an id that resolves to no file
- **THEN** validation reports an error naming the referencing object and the missing id

### Requirement: Objects are mutable live state

Objects SHALL be edited in place. A change of state (a window narrowing, a stability change, a status change) SHALL be an edit to the existing object, not the creation of a replacement. This is the opposite of DKF's append-only discipline and is deliberate: DKF records epistemic history, this specification records live prospective state, and a partial plan filled in incrementally remains the same plan.

The exceptions are: a retired object (see Retirement) SHALL NOT be edited further; and a generated instance of a recurring intention SHALL be a new object, not an edit of the standing intention.

#### Scenario: Window narrowed
- **WHEN** an intention with window `2026-09` is resolved to a concrete placement
- **THEN** the same intention file is updated with the placement and its id is unchanged

### Requirement: Retirement is a terminal status, never deletion

An object SHALL be retired by setting a terminal `status`, never by deleting its file. Retirement kinds are defined per object type. A retired object SHALL NOT be edited further, except that acknowledgement records already on it are preserved.

#### Scenario: Deletion attempted
- **WHEN** a tool is asked to remove an intention
- **THEN** it sets a retirement status and refuses to delete the file

### Requirement: Versioning by projection hash

Every object SHALL have a version, defined as the hash of a canonical serialisation of that object's *scheduling projection*: the subset of its fields that bear on consistency checking, as enumerated in each object type's specification. Prose fields (title, description, notes) and acknowledgement records SHALL be excluded from the projection.

The version SHALL be derived, never declared. The canonical serialisation SHALL use sorted keys, normalised EDTF and ISO 8601 duration strings, UTF-8 encoding, and a fixed hash algorithm named in `intentions.yaml`. A tool MAY cache the computed version in the file under `version`; the computed value is authoritative.

#### Scenario: Prose edit does not change version
- **WHEN** only an intention's description is edited
- **THEN** its version is unchanged

#### Scenario: Window edit changes version
- **WHEN** an intention's window is edited
- **THEN** its version changes

#### Scenario: Stale cached version
- **WHEN** a file carries a cached `version` that differs from the computed value
- **THEN** validation reports a warning and tools use the computed value

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, and unknown status values. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

Where a write operation can determine that the result would fail validation with an error, it SHALL refuse the write. Write-time refusal is a convenience; validation is the invariant, because files may arrive by merge without passing through any write operation.

#### Scenario: Merge introduces error
- **WHEN** two branches each add one valid reference and the merged result contains a cycle
- **THEN** validation on the merged workspace reports the cycle as an error even though neither write was refused

### Requirement: Composition with DKF by reference only

This specification SHALL NOT depend on any DKF object, schema, or tool to exist or validate. A DKF claim MAY cite any object in this specification by id, optionally with a projection hash, exactly as a DKF claim cites an external document. Objects in this specification MAY carry an informal `reference` (a URI or DKF id) pointing at a DKF claim, with no resolvability contract. Live prospective state SHALL never be represented as DKF claims.

#### Scenario: Terminus points at a held identity claim
- **WHEN** an intention's terminus carries `reference: clm_...`
- **THEN** validation does not attempt to resolve it and does not report it if the target is absent

### Requirement: Composition with iCalendar and JSCalendar by reference only

This specification SHALL NOT embed iCalendar or JSCalendar grammar beyond three deliberate reuses: ISO 8601 durations, RRULE-shaped cadence expressions, and the RFC 9253 temporal relation vocabulary. A COMMITMENT MAY carry an external calendar UID; no other object type SHALL reference an external calendar object. Recurrence exception handling, timezone definitions, alarms, attendee delegation, and iTIP negotiation SHALL remain entirely in the external system.

#### Scenario: Imported event
- **WHEN** an iCalendar event is imported
- **THEN** exactly one COMMITMENT is created carrying the event's UID, and no WINDOW, INTENTION, or AVAILABILITY is created from it

### Requirement: Workspace configuration

`intentions.yaml` SHALL declare the format version, the hash algorithm used for versioning, the resolver context defaults (timezone, week start), and the default availability validity horizon.

#### Scenario: Minimal configuration
- **WHEN** a workspace is initialised
- **THEN** `intentions.yaml` is written with `format`, `hash`, `resolver.timezone`, `resolver.week_start`, and `availability.default_horizon` populated
