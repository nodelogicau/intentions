## MODIFIED Requirements

### Requirement: Versioning by projection hash

Every object SHALL have a version, defined as the hash of a canonical serialisation of that object's *scheduling projection*: the subset of its fields that bear on consistency checking, as enumerated in each object type's specification and frozen per format version. A projection SHALL be frozen from the moment any implementation writes the format version string into a file, not from any declaration; a change to any projection SHALL be a new format version, with one named exception. `habit` joined the INTENTION projection of `intentions/0.2` after files carried that string. It was admitted because it is optional and omitted at its documented default, so no existing hash moved. No other field SHALL be admitted this way: every further change to any projection, including another field omitted at its default, SHALL be a new format version. A reader older than an admitted field computes a different version for any object carrying it at a non-default value and does not apply its semantics, so a stored `counterpart_version` stays comparable only between readers that agree on the admitted fields. Prose fields (title, description, notes), `source`, `timestamp`, `version`, `firmed_under`, an intention's `external`, acknowledgement records, and the `reason`, `timestamp`, and `source` of a `retired` record SHALL be excluded from the projection. `retired.kind` SHALL be included.

A version identifies a state of one object, not the object: two objects whose projections are equal SHALL have equal versions, as every firm terminus of one subject that carries nothing else in its projection does, and a version SHALL be compared only together with the id of the object it was read from, as an acknowledgement's `counterpart_version` is with its `counterpart`.

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

#### Scenario: Two termini share a version
- **WHEN** two firm, unretired termini of one subject differ only in `title`
- **THEN** they carry the same version, validation reports nothing, and an acknowledgement or citation naming one by id and version does not match the other
