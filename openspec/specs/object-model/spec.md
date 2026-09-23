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

Every object SHALL have an `id` composed of a type prefix, an underscore, and a UUIDv7. The prefix SHALL be `int` for intentions, `avl` for availability, `res` for resolutions, `cmt` for commitments, `des` for desires. WINDOW and DURATION are values embedded in their carrying object and SHALL NOT have ids of their own. Ids SHALL be immutable and SHALL remain resolvable for the life of the workspace, including after retirement.

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

### Requirement: Retirement is an appended record, never deletion

An object SHALL be retired by appending a single `retired` record to it, never by deleting its file and never by a status field. The record SHALL carry `kind` (per object type), optional `reason` (prose), `superseded_by` (required when and only when `kind` is `superseded`), `adopted_as` (on a DESIRE, required when and only when `kind` is `adopted`, naming the INTENTION it became), `timestamp`, and `source`. Kinds are per type: intention `fulfilled`, `abandoned`, `superseded`; availability `retracted`, `superseded`; commitment `cancelled`; desire `abandoned`, `superseded`, `adopted`. An object with no `retired` record is active; no `status` field SHALL exist on any object. A retired object SHALL NOT be edited further, except that acknowledgement records MAY still be appended to it. `retired.kind` SHALL be part of the object's scheduling projection; `reason`, `superseded_by`, `adopted_as`, `timestamp`, and `source` SHALL NOT.

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

### Requirement: Versioning by projection hash

Every object SHALL have a version, defined as the hash of a canonical serialisation of that object's *scheduling projection*: the subset of its fields that bear on consistency checking, as enumerated in each object type's specification and frozen per format version. Prose fields (title, description, notes), `source`, `timestamp`, `version`, `firmed_under`, acknowledgement records, and the `reason`, `timestamp`, and `source` of a `retired` record SHALL be excluded from the projection. `retired.kind` SHALL be included.

The version SHALL be derived, never declared. The projection SHALL be expressed as a JSON object with values normalised first, serialised with the JSON Canonicalization Scheme (RFC 8785), and hashed with the algorithm named by `hash` in `intentions.yaml`. Normalisation SHALL be: EDTF expressions in shortest admitted form; ISO 8601 durations with zero components dropped, weeks folded into days (`P1W` becomes `P7D`), the time part re-expressed from its total seconds as hours, minutes and seconds (`PT90M` becomes `PT1H30M`, `PT60M` becomes `PT1H`), no conversion between the date part and the time part (`P1D` and `PT24H` stay distinct), and no conversion of months or years, with a zero duration written `P0D`; datetimes as RFC 3339 UTC with seconds; every set-valued list sorted, namely references by id then role, commitment `parties` by `uri`, and string lists (`location`, `conditional`, intention `parties`, `displaced`) lexically; absent optional fields omitted; and a boolean equal to its documented default omitted, so that an explicit `transparent: false` hashes as absent. The version SHALL be written as `<algorithm>:<lowercase hex>`. This version of the format admits only `sha256`.

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

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active, firm policy of the intention's subject, `firmed_under` on a terminus, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, a DESIRE carrying any field of an intention's temporal or deontic kind (`duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, `acknowledgements`), a DESIRE `serves` entry with any role but `for-the-sake-of`, `adopted` without `adopted_as` or `adopted_as` naming anything but an intention, `superseded_by` on a desire naming anything but a desire, and `transparent` on a commitment born of a resolution. Warnings SHALL include an intention that reaches no firm terminus of its own subject, named with the fix, and a RESOLUTION record whose `selector` names a policy that is no longer firm or no longer active, as an act authorised when it happened under a policy since withdrawn; the placement it produced stands and is the person's to keep or re-resolve. Info SHALL include a tentative terminus, as a draft. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

Where a write operation can determine that the result would fail validation with an error, it SHALL refuse the write. Where it can determine that the result would carry a warning, it SHALL accept the write and report the warning in its result. Write-time refusal is a convenience; validation is the invariant, because files may arrive by merge without passing through any write operation.

#### Scenario: Merge introduces error
- **WHEN** two branches each add one valid reference and the merged result contains a cycle
- **THEN** validation on the merged workspace reports the cycle as an error even though neither write was refused

#### Scenario: Unauthorised firming detected after the fact
- **WHEN** a merged intention carries `stability: firm`, a `source.harness`, and no `firmed_under`
- **THEN** validation reports an error naming the intention

#### Scenario: Workspace without termini
- **WHEN** a workspace holds intentions and no terminus
- **THEN** validation reports every non-terminus intention as unserved at warning level and exits zero

#### Scenario: Firmed under a draft
- **WHEN** an intention carries `firmed_under` naming a policy whose `stability` is `tentative`
- **THEN** validation reports an error naming the intention and the policy

#### Scenario: Selected under a policy since withdrawn
- **WHEN** a RESOLUTION record's `selector` names a policy that has since been set tentative or retired
- **THEN** validation reports a warning on the record and does not exit non-zero for it

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

`intentions.yaml` SHALL declare `format`, `hash`, the resolver context default `resolver.timezone`, `resolver.horizon` (the planning horizon shared by resolution and instance generation; recommended `P4W`), `availability.default_horizon`, and `defaults.source.author`. It MAY declare `resolver.hemisphere` (`north` or `south`; absent means `north`), `resolver.step` (the candidate grid; absent means `PT15M`), `resolver.scope` (`personal`, `organisation`, or `public`; absent means `personal`), and `defaults.subject`; when `defaults.subject` is absent, every intention SHALL name its `subject` explicitly. `resolver.week_start` and `generation.horizon` SHALL NOT be declared. A reader finding an unknown key under `resolver` or `generation` SHALL ignore it and validation SHALL report it at info level.

#### Scenario: Minimal configuration
- **WHEN** a workspace is initialised for one person
- **THEN** `intentions.yaml` is written with `format`, `hash`, `resolver.timezone`, `resolver.horizon`, `availability.default_horizon`, `defaults.subject`, and `defaults.source.author` populated, and no `generation` section

#### Scenario: Default subject applied
- **WHEN** an intention is written without `subject` in a workspace whose `defaults.subject` is set
- **THEN** the file is written with `subject` equal to the workspace default

#### Scenario: Organisation workspace
- **WHEN** `defaults.subject` is absent and an intention is written without `subject`
- **THEN** the write is refused

#### Scenario: Southern hemisphere
- **WHEN** `intentions.yaml` declares `resolver.hemisphere: south`
- **THEN** a window of `2026-21` resolves to September through November 2026

#### Scenario: Stale keys
- **WHEN** an existing `intentions.yaml` still carries `resolver.week_start` or `generation.horizon`
- **THEN** they are ignored and validation reports them at info level

#### Scenario: Step and scope defaults
- **WHEN** `intentions.yaml` declares neither `resolver.step` nor `resolver.scope`
- **THEN** resolution uses a fifteen-minute grid and a `personal` scope ceiling

### Requirement: Format name and type names

The format SHALL be named the Intentions Format, with slug `intentions` and format version string `intentions/0.1` in the workspace marker. Object types SHALL be named DESIRE, INTENTION, AVAILABILITY, and COMMITMENT; record types RESOLUTION, ACKNOWLEDGEMENT, and RETIREMENT; embedded values WINDOW, DURATION, and PLACEMENT. No type name SHALL carry a `D` prefix or any other marker of a DKF relationship.

#### Scenario: Format version declared
- **WHEN** a workspace is initialised
- **THEN** `intentions.yaml` carries `format: intentions/0.1`

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

### Requirement: Timestamps

Every object and record SHALL carry a `timestamp`: the assertion time as an RFC 3339 UTC datetime with seconds. On a record it is the time of the act. The timestamp MAY precede the minting instant embedded in the id, and consumers MUST NOT require the two to agree. `timestamp` SHALL be excluded from every scheduling projection.

#### Scenario: Backdated availability
- **WHEN** an availability learned from a conversation last week is recorded today with last week's `timestamp`
- **THEN** the file is valid and its default validity horizon is measured from last week

#### Scenario: Timestamp correction does not change version
- **WHEN** only an object's `timestamp` is corrected
- **THEN** its version is unchanged

### Requirement: Canonical field order

Each object type's specification lists its fields in canonical order, with `version` immediately after `id`. Writers SHALL emit fields in that order; readers MUST accept any order and MUST NOT reject a file for its field arrangement. Fields an implementation adds beyond this specification SHALL be written after all specified fields. Writers SHALL use one style per kind of value: lists of strings (`location`, `conditional`, intention `parties`, `displaced`) as block sequences, sorted as in the projection; small records (`serves` entries, ranged durations, `gap`, policy conditions) as flow mappings; multi-line prose as a literal block scalar; everything else in block style. A boolean equal to its documented default SHALL be omitted.

#### Scenario: Reordered file accepted
- **WHEN** a file lists `window` before `title`
- **THEN** it is read correctly and validation does not report it

#### Scenario: Two writers agree
- **WHEN** two implementations write the same intention
- **THEN** the files are byte-identical

#### Scenario: List style
- **WHEN** a writer emits an availability with two conditional terms and one serves entry
- **THEN** `conditional` is a block sequence of two lines and the serves entry is a one-line flow mapping

### Requirement: Derived index

`index.yaml` SHALL be a derived cache of the object files, regenerated by an `index` operation and verified by `index --check`. Each entry SHALL carry the object's `id`, type, `subject`, file path, projection version, `retired.kind` if any, and the ids of its outbound references, and nothing not derivable from the file. Readers MUST treat any disagreement between the index and a file as an index defect and use the file; validation SHALL report such drift as a warning. The index SHALL be committed alongside the objects and a merge conflict in it SHALL be resolved by regeneration.

#### Scenario: Index drift
- **WHEN** an object file's window is edited without re-running `index`
- **THEN** validation reports a warning naming the entry and tools use the file's value

#### Scenario: Merge conflict
- **WHEN** two branches both regenerate `index.yaml`
- **THEN** the merged index is produced by running `index` again, not by hand-merging

### Requirement: Workspace conventions file

A workspace MAY carry `intentions.md`, a prose conventions file for agents and people, recording among other things the activity-type terms in use. It SHALL have no schema and SHALL NOT be read by validation.

#### Scenario: Conventions present
- **WHEN** `intentions.md` lists the term `deep-work`
- **THEN** validation behaviour is unchanged and an agent reads the file for guidance

### Requirement: Multiple subjects per workspace

A workspace MAY hold objects for several subjects, and validation SHALL NOT require that every object share one subject. Reading another workspace's objects (federation) is deferred from this version: scope visibility is defined within one workspace, and a resolver has no supply for a party whose availability is held elsewhere. A party the workspace holds no availability for at all is untracked rather than unavailable, and resolution treats them as unconstrained (see Resolution); a workspace SHALL NOT write an availability for a party in order to make a resolution succeed, because an availability is an assertion about that particular's capacity and inventing one records a fact nobody asserted.

#### Scenario: Room in a personal workspace
- **WHEN** a personal workspace holds an availability whose `subject` is a room URI
- **THEN** it is valid and resolution uses it for intentions listing that room in `parties`

#### Scenario: Party held elsewhere
- **WHEN** an intention lists a party for which no availability exists in this workspace
- **THEN** that party is untracked, contributes no supply constraint, and resolution places against the tracked parties' supply

#### Scenario: No manufactured supply
- **WHEN** a harness cannot place an intention naming an external party
- **THEN** it reports what stands in the way and does not write an availability whose subject is that party

### Requirement: Workspace discovery

Tools SHALL locate the workspace by, in order of precedence: a `--workspace` argument; the `INTENTIONS_WORKSPACE` environment variable; the nearest ancestor directory containing `intentions.yaml` or a `.intentions` pointer file whose content is the workspace path. An environment variable naming a directory with no `intentions.yaml` SHALL be an error, not a fallback to the search.

#### Scenario: Pointer file
- **WHEN** a tool runs in a directory whose ancestor holds `.intentions` containing `/home/ada/planning`
- **THEN** the workspace at `/home/ada/planning` is used

#### Scenario: Bad environment variable
- **WHEN** `INTENTIONS_WORKSPACE` names a directory with no `intentions.yaml`
- **THEN** the tool exits with the no-workspace code rather than searching ancestors
