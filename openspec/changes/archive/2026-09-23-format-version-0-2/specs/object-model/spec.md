## ADDED Requirements

### Requirement: Migration from intentions/0.1

A workspace SHALL move from `intentions/0.1` to `intentions/0.2` only by an explicit `migrate` operation, the person's act. Migration SHALL: rewrite each commitment's `origin` from the 0.1 union shape to `origin: resolution` with a sibling `resolution`, or `origin: import`; rename `duration` to `capacity` and `conditional` to `activities` on every availability; recompute every version under 0.2; rewrite `counterpart_version` on every acknowledgement whose counterpart's version changed only because of the migration, so that no acknowledgement lapses for a change in shape; regenerate the index; and rewrite `format` in `intentions.yaml`. Nothing else SHALL change: no id, no field a person wrote, no `source`, no `timestamp`, no `retired` record. Migration SHALL refuse to rewrite `format` while any intention is unserved under the 0.2 rule, naming them, so that the walk-up to termini happens before the refusal applies.

#### Scenario: Acknowledgement carried across
- **WHEN** an intention carries an acknowledgement whose counterpart is a resolution-born commitment and the workspace is migrated
- **THEN** the acknowledgement's `counterpart_version` is the commitment's new version and the acknowledgement has not lapsed

#### Scenario: Migration refused while unserved
- **WHEN** a 0.1 workspace holding an unserved intention is migrated
- **THEN** `format` is not rewritten and the refusal names the intention

#### Scenario: Nothing else moves
- **WHEN** a 0.1 workspace with no commitments, no availability and no acknowledgements is migrated
- **THEN** only `format`, the index, and the recomputed `version` lines change

## MODIFIED Requirements

### Requirement: Versioning by projection hash

Every object SHALL have a version, defined as the hash of a canonical serialisation of that object's *scheduling projection*: the subset of its fields that bear on consistency checking, as enumerated in each object type's specification and frozen per format version. A projection SHALL be frozen from the moment any implementation writes the format version string into a file, not from any declaration; a change to any projection SHALL be a new format version. Prose fields (title, description, notes), `source`, `timestamp`, `version`, `firmed_under`, acknowledgement records, and the `reason`, `timestamp`, and `source` of a `retired` record SHALL be excluded from the projection. `retired.kind` SHALL be included.

The version SHALL be derived, never declared. The projection SHALL be expressed as a JSON object with values normalised first, serialised with the JSON Canonicalization Scheme (RFC 8785), and hashed with the algorithm named by `hash` in `intentions.yaml`. Normalisation SHALL be: EDTF expressions in shortest admitted form; ISO 8601 durations with zero components dropped, weeks folded into days (`P1W` becomes `P7D`), the time part re-expressed from its total seconds as hours, minutes and seconds (`PT90M` becomes `PT1H30M`, `PT60M` becomes `PT1H`), no conversion between the date part and the time part (`P1D` and `PT24H` stay distinct), and no conversion of months or years, with a zero duration written `P0D`; datetimes as RFC 3339 UTC with seconds; every set-valued list sorted, namely references by id then role, commitment `parties` by `uri`, and string lists (`location`, `activities`, intention `parties`, `displaced`) lexically; absent optional fields omitted; and a boolean equal to its documented default omitted, so that an explicit `transparent: false` hashes as absent. The version SHALL be written as `<algorithm>:<lowercase hex>`. This version of the format admits only `sha256`.

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

### Requirement: Format name and type names

The format SHALL be named the Intentions Format, with slug `intentions` and format version string `intentions/0.2` in the workspace marker. Object types SHALL be named DESIRE, INTENTION, AVAILABILITY, and COMMITMENT; record types RESOLUTION, ACKNOWLEDGEMENT, and RETIREMENT; embedded values WINDOW, DURATION, and PLACEMENT. No type name SHALL carry a `D` prefix or any other marker of a DKF relationship.

#### Scenario: Format version declared
- **WHEN** a workspace is initialised
- **THEN** `intentions.yaml` carries `format: intentions/0.2`

#### Scenario: Newer format refused
- **WHEN** a reader implementing `intentions/0.2` opens a workspace whose `format` is `intentions/0.3`
- **THEN** it refuses to read or write, naming both versions

#### Scenario: Older format accepted
- **WHEN** a reader implementing `intentions/0.2` opens a workspace whose `format` is `intentions/0.1`
- **THEN** it reads and writes it under the 0.1 rules and shapes until the workspace is migrated

### Requirement: Canonical field order

Each object type's specification lists its fields in canonical order, with `version` immediately after `id`. Writers SHALL emit fields in that order; readers MUST accept any order and MUST NOT reject a file for its field arrangement. Fields an implementation adds beyond this specification SHALL be written after all specified fields. Writers SHALL use one style per kind of value: lists of strings (`location`, `activities`, intention `parties`, `displaced`) as block sequences, sorted as in the projection; small records (`serves` entries, ranged durations, `gap`, policy conditions) as flow mappings; multi-line prose as a literal block scalar; everything else in block style. A boolean equal to its documented default SHALL be omitted.

#### Scenario: Reordered file accepted
- **WHEN** a file lists `window` before `title`
- **THEN** it is read correctly and validation does not report it

#### Scenario: Two writers agree
- **WHEN** two implementations write the same intention
- **THEN** the files are byte-identical

#### Scenario: List style
- **WHEN** a writer emits an availability with two `activities` terms and one serves entry
- **THEN** `activities` is a block sequence of two lines and the serves entry is a one-line flow mapping

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active, firm policy of the intention's subject, `firmed_under` on a terminus, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, a DESIRE carrying any field of an intention's temporal or deontic kind (`duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, `acknowledgements`), a DESIRE `serves` entry with any role but `for-the-sake-of`, `adopted` without `adopted_as` or `adopted_as` naming anything but an intention, `superseded_by` on a desire naming anything but a desire, and `transparent` on a commitment born of a resolution. Under `intentions/0.2` errors SHALL also include an intention that reaches no firm terminus of its own subject, named with the fix; under `intentions/0.1` that finding is a warning. Warnings SHALL include a RESOLUTION record whose `selector` names a policy that is no longer firm or no longer active, as an act authorised when it happened under a policy since withdrawn; the placement it produced stands and is the person's to keep or re-resolve. Info SHALL include a tentative terminus, as a draft. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

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
