## MODIFIED Requirements

### Requirement: Identifiers

Every object SHALL have an `id` composed of a type prefix, an underscore, and a UUIDv7. The prefix SHALL be `int` for intentions, `avl` for availability, `res` for resolutions, `cmt` for commitments, `des` for desires. WINDOW and DURATION are values embedded in their carrying object and SHALL NOT have ids of their own. Ids SHALL be immutable and SHALL remain resolvable for the life of the workspace, including after retirement.

#### Scenario: Reference to a retired object
- **WHEN** an object references an intention whose status is `abandoned`
- **THEN** the reference still resolves and validation does not report it as dangling

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

### Requirement: Format name and type names

The format SHALL be named the Intentions Format, with slug `intentions` and format version string `intentions/0.1` in the workspace marker. Object types SHALL be named DESIRE, INTENTION, AVAILABILITY, and COMMITMENT; record types RESOLUTION, ACKNOWLEDGEMENT, and RETIREMENT; embedded values WINDOW, DURATION, and PLACEMENT. No type name SHALL carry a `D` prefix or any other marker of a DKF relationship.

#### Scenario: Format version declared
- **WHEN** a workspace is initialised
- **THEN** `intentions.yaml` carries `format: intentions/0.1`

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active, firm policy of the intention's subject, `firmed_under` on a terminus, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, a DESIRE carrying any field of an intention's temporal or deontic kind (`duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, `acknowledgements`), a DESIRE `serves` entry with any role but `for-the-sake-of`, `adopted` without `adopted_as` or `adopted_as` naming anything but an intention, and `transparent` on a commitment born of a resolution. Warnings SHALL include an intention that reaches no firm terminus of its own subject, named with the fix, and a RESOLUTION record whose `selector` names a policy that is no longer firm or no longer active, as an act authorised when it happened under a policy since withdrawn; the placement it produced stands and is the person's to keep or re-resolve. Info SHALL include a tentative terminus, as a draft. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

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
