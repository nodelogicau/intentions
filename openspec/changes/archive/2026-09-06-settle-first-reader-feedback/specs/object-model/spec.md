## MODIFIED Requirements

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

### Requirement: Workspace configuration

`intentions.yaml` SHALL declare `format`, `hash`, the resolver context default `resolver.timezone`, `availability.default_horizon`, `generation.horizon`, and `defaults.source.author`. It MAY declare `resolver.hemisphere` (`north` or `south`; absent means `north`) and `defaults.subject`; when `defaults.subject` is absent, every intention SHALL name its `subject` explicitly. `resolver.week_start` SHALL NOT be declared; weeks are ISO weeks. A reader finding an unknown key under `resolver` SHALL ignore it and validation SHALL report it at info level.

#### Scenario: Minimal configuration
- **WHEN** a workspace is initialised for one person
- **THEN** `intentions.yaml` is written with `format`, `hash`, `resolver.timezone`, `availability.default_horizon`, `generation.horizon`, `defaults.subject`, and `defaults.source.author` populated, and no `resolver.week_start`

#### Scenario: Default subject applied
- **WHEN** an intention is written without `subject` in a workspace whose `defaults.subject` is set
- **THEN** the file is written with `subject` equal to the workspace default

#### Scenario: Organisation workspace
- **WHEN** `defaults.subject` is absent and an intention is written without `subject`
- **THEN** the write is refused

#### Scenario: Southern hemisphere
- **WHEN** `intentions.yaml` declares `resolver.hemisphere: south`
- **THEN** a window of `2026-21` resolves to September through November 2026

#### Scenario: Stale week_start key
- **WHEN** an existing `intentions.yaml` still carries `resolver.week_start`
- **THEN** it is ignored and validation reports it at info level

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active policy of the intention's subject, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, and `transparent` on a commitment born of a resolution. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

Where a write operation can determine that the result would fail validation with an error, it SHALL refuse the write. Write-time refusal is a convenience; validation is the invariant, because files may arrive by merge without passing through any write operation.

#### Scenario: Merge introduces error
- **WHEN** two branches each add one valid reference and the merged result contains a cycle
- **THEN** validation on the merged workspace reports the cycle as an error even though neither write was refused

#### Scenario: Unauthorised firming detected after the fact
- **WHEN** a merged intention carries `stability: firm`, a `source.harness`, and no `firmed_under`
- **THEN** validation reports an error naming the intention
