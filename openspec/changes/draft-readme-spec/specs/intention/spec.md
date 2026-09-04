## ADDED Requirements

### Requirement: Activity vocabulary

`activity` on an intention and each term in `conditional` on an availability SHALL be a lowercase kebab-case term. The specification SHALL NOT fix the vocabulary; terms are documented in the workspace conventions file. Matching between `activity` and `conditional` SHALL be by exact string equality. An unknown term SHALL NOT be a validation error; validation SHALL report at info level any term used by exactly one object.

#### Scenario: Unknown term accepted
- **WHEN** an intention carries `activity: piano-practice` and no other object uses that term
- **THEN** validation passes and reports the term at info level

#### Scenario: Malformed term
- **WHEN** an intention carries `activity: Deep Work`
- **THEN** the write is refused and validation reports an error

### Requirement: Instance generation

Instances of a standing intention SHALL be materialised by a `generate` operation over a horizon window, which resolution SHALL also run over its own horizon. Generated instances SHALL be written to disk immediately as INTENTION objects. Each instance SHALL carry `occurrence`, the EDTF granule the cadence produced, and generation SHALL be idempotent over that key: generating again over an overlapping horizon SHALL create no second active instance for the same standing intention and occurrence, and validation SHALL report such a duplicate as an error. The horizon defaults to `generation.horizon` in `intentions.yaml`; the recommended default is four weeks (`P4W`). No background generation SHALL occur.

#### Scenario: Idempotent generation
- **WHEN** `generate` runs twice over horizons that both include 2026-09-15 for a weekly Tuesday standing intention
- **THEN** exactly one active instance with `occurrence: 2026-09-15` exists

#### Scenario: Skipped then regenerated
- **WHEN** the instance for 2026-09-15 is retired as `abandoned` and `generate` runs again over that week
- **THEN** no new instance for 2026-09-15 is created

#### Scenario: Resolution generates
- **WHEN** resolution runs for an intention whose window lies in the next two weeks
- **THEN** instances of every standing intention with occurrences in that horizon exist on disk before candidates are ranked

### Requirement: Standing intention policies

A standing intention MAY carry `auto_select` and `auto_firm`; each SHALL be a condition over an intention being acted on with terms `max_duration` (ISO 8601 duration) and `stability` (`tentative` or `firm`). A condition is satisfied when every term it states holds for the intention. These are the only means by which a harness may select a candidate or set `firm` without a person's direct act.

#### Scenario: Policy condition met
- **WHEN** a standing intention carries `auto_firm: {max_duration: PT30M}` and a harness firms a twenty-minute intention citing that policy
- **THEN** the write is accepted and the act records the policy id

#### Scenario: Policy condition not met
- **WHEN** the same policy exists and a harness attempts to firm a two-hour intention citing it
- **THEN** the write is refused

## MODIFIED Requirements

### Requirement: Intention fields

An INTENTION SHALL carry, in canonical order: `id`; `subject` (a URI identifying the particular whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); optional `activity`; optional `parties` (URIs of other required particulars, whose availability resolution must satisfy); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `occurrence` (on generated instances only); optional `placement`; optional `preference` (see Resolution); optional `auto_select` and `auto_firm` (standing intentions only); optional `reference` (informal pointer to a DKF claim); `source`; `timestamp`; `acknowledgements` (see Consistency); and at most one `retired` record.

The scheduling projection of an INTENTION SHALL be: `subject`, `duration`, `window`, `stability`, `activity`, `parties`, `serves`, `cadence`, `occurrence`, `placement`, `retired.kind`.

#### Scenario: Minimal intention
- **WHEN** an intention is written with only `title` and `stability: tentative` in a workspace with default `subject` and `source.author`
- **THEN** it is valid, the file carries the default `subject`, `source.author`, and a `timestamp`, it carries no window or duration, and it cannot be resolved until it has both

#### Scenario: Subject without default
- **WHEN** an intention is written without `subject` in a workspace with no `defaults.subject`
- **THEN** the write is refused

#### Scenario: Own supply is by subject
- **WHEN** an intention with `subject: https://example.org/people/ben` is resolved
- **THEN** its own supply is the eligible availability whose `subject` is that URI

### Requirement: Stability

`stability` SHALL be `tentative` or `firm`. A firm intention SHALL be treated by resolution as costly to reconsider; a tentative one as cheap. Changing stability SHALL be an explicit edit and SHALL change the version. `firm` SHALL be set only by an act whose `source` carries no `harness`, or by a harness acting under a standing intention of the subject whose `auto_firm` condition the intention satisfies, in which case the act SHALL name that policy's id.

#### Scenario: Firming
- **WHEN** a person marks an intention `firm`
- **THEN** subsequent resolutions of other intentions rank placements that would displace it below placements that would not

#### Scenario: Harness firms without policy
- **WHEN** a write whose `source.harness` is set changes `stability` to `firm` and names no policy
- **THEN** the write is refused and validation reports an error

#### Scenario: Harness drafts tentative
- **WHEN** a harness writes a new intention with `stability: tentative`
- **THEN** the write is accepted

### Requirement: Retirement kinds

An intention's `retired.kind` SHALL be one of `fulfilled` (discharged, a positive terminal state), `abandoned` (no longer held, no replacement), or `superseded` (replaced by a specific other intention, in which case `superseded_by` SHALL carry that intention's id). Each kind is final; a retired intention SHALL NOT be edited further except to append acknowledgements.

#### Scenario: Superseded
- **WHEN** an intention is retired with `retired: {kind: superseded, superseded_by: int_C, ...}`
- **THEN** validation requires int_C to exist and reports an error if it does not

#### Scenario: Superseded without target
- **WHEN** an intention is retired with `kind: superseded` and no `superseded_by`
- **THEN** the write is refused

#### Scenario: Fulfilled with reason
- **WHEN** an intention is retired with `kind: fulfilled` and a `reason`
- **THEN** the record carries the reason, a timestamp, and the source of the retiring act, and the intention's version changes

### Requirement: Standing intentions and generated instances

An INTENTION carrying `cadence` is a standing intention. Instances SHALL be new INTENTION objects, each carrying `serves: [{id: <standing>, role: instance-of}]`, `occurrence` (the EDTF granule the cadence produced), a `window` derived from that occurrence, and the standing intention's `subject`, `duration`, `activity`, and `parties` unless overridden. Each instance has its own stability, resolution lifecycle, and retirement. Recurrence SHALL NOT be an attribute of WINDOW.

#### Scenario: Instance generation
- **WHEN** a standing intention has `cadence: FREQ=WEEKLY;BYDAY=TU` and an instance is generated for week 2026-W37
- **THEN** a new intention is created with `occurrence: 2026-09-15`, `window.calendar: 2026-09-15`, the standing intention's `subject`, and `serves: [{id: <standing>, role: instance-of}]`

#### Scenario: Skip one occurrence
- **WHEN** a generated instance is retired with `kind: abandoned`
- **THEN** the standing intention is unchanged and later instances continue to generate

#### Scenario: End the arrangement
- **WHEN** a standing intention is retired
- **THEN** no further instances are generated and existing active instances are unaffected until retired individually
