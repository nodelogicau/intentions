## ADDED Requirements

### Requirement: Source attribution

Every object and record SHALL carry a `source` block with fields `author` (a URI or name identifying the person on whose behalf the object was written), `harness` (the agent harness that wrote it, if any), and `model` (the model identifier, if any). `author` SHALL be required on INTENTION and AVAILABILITY. `harness` alone SHALL be sufficient on RESOLUTION, ACKNOWLEDGEMENT, and retirement records only when `author` is also present on the object they concern. A writer SHALL apply the workspace default `source.author` from `intentions.yaml` when the caller omits it. `source` SHALL be excluded from every scheduling projection.

#### Scenario: Harness drafts an intention
- **WHEN** a harness writes an intention on a person's behalf with the workspace default author
- **THEN** the file carries `source.author` set to that person and `source.harness` set to the harness, and both are visible in the diff

#### Scenario: Intention without author
- **WHEN** an intention is written with `source.harness` but no `source.author` and no workspace default
- **THEN** the write is refused and validation reports an error

#### Scenario: Attribution correction does not lapse acknowledgements
- **WHEN** an object's `source.author` is corrected after a counterpart acknowledged a flag against it
- **THEN** its version is unchanged and the acknowledgement remains in force

## MODIFIED Requirements

### Requirement: Retirement is a terminal status, never deletion

An object SHALL be retired by appending a single `retired` record to it, never by deleting its file and never by a status field. The record SHALL carry `kind` (per object type), optional `reason` (prose), `superseded_by` (required when and only when `kind` is `superseded`), `timestamp`, and `source`. An object with no `retired` record is active; no `status` field SHALL exist on any object. A retired object SHALL NOT be edited further, except that acknowledgement records MAY still be appended to it. `retired.kind` SHALL be part of the object's scheduling projection; `reason`, `timestamp`, and `source` SHALL NOT.

#### Scenario: Deletion attempted
- **WHEN** a tool is asked to remove an intention
- **THEN** it appends a `retired` record and refuses to delete the file

#### Scenario: Second retirement refused
- **WHEN** an object already carrying a `retired` record is retired again
- **THEN** the write is refused

#### Scenario: Retirement changes version
- **WHEN** a `retired` record is appended to an active intention
- **THEN** its version changes and it no longer participates in any flag as a live counterpart

### Requirement: Versioning by projection hash

Every object SHALL have a version, defined as the hash of a canonical serialisation of that object's *scheduling projection*: the subset of its fields that bear on consistency checking, as enumerated in each object type's specification. Prose fields (title, description, notes), `source`, acknowledgement records, and the `reason`, `timestamp`, and `source` of a `retired` record SHALL be excluded from the projection. `retired.kind` SHALL be included.

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

#### Scenario: Source edit does not change version
- **WHEN** only an object's `source.model` is edited
- **THEN** its version is unchanged

### Requirement: Workspace configuration

`intentions.yaml` SHALL declare the format version, the hash algorithm used for versioning, the resolver context defaults (timezone, week start), the default availability validity horizon, and defaults for `subject` (the URI of the particular whose workspace this is) and `source.author`.

#### Scenario: Minimal configuration
- **WHEN** a workspace is initialised
- **THEN** `intentions.yaml` is written with `format`, `hash`, `resolver.timezone`, `resolver.week_start`, `availability.default_horizon`, `defaults.subject`, and `defaults.source.author` populated

#### Scenario: Default subject applied
- **WHEN** an intention is written without `subject` in a workspace whose `defaults.subject` is set
- **THEN** the file is written with `subject` equal to the workspace default
