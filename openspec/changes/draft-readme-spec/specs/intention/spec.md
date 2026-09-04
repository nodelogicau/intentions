## MODIFIED Requirements

### Requirement: Intention fields

An INTENTION SHALL carry: `id`; `subject` (a URI identifying the particular whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `source`; `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `activity` (a term from the workspace activity-type vocabulary, matched against availability conditionals); optional `parties` (URIs of other required particulars, whose availability resolution must satisfy); optional `placement`; optional `reference` (informal pointer to a DKF claim); optional `preference` (see Resolution); `acknowledgements` (see Consistency); and at most one `retired` record.

The scheduling projection of an INTENTION SHALL be: `subject`, `duration`, `window`, `stability`, `serves`, `cadence`, `activity`, `parties`, `placement`, `retired.kind`.

#### Scenario: Minimal intention
- **WHEN** an intention is written with only `title` and `stability: tentative` in a workspace with default `subject` and `source.author`
- **THEN** it is valid, the file carries the default `subject` and `source.author`, it carries no window or duration, and it cannot be resolved until it has both

#### Scenario: Subject without default
- **WHEN** an intention is written without `subject` in a workspace with no `defaults.subject`
- **THEN** the write is refused

#### Scenario: Own supply is by subject
- **WHEN** an intention with `subject: https://example.org/people/ben` is resolved
- **THEN** its own supply is the eligible availability whose `subject` is that URI

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

An INTENTION carrying `cadence` is a standing intention. Instances SHALL be generated on demand as new INTENTION objects, each carrying `serves: [{id: <standing>, role: instance-of}]`, a `window` derived from the cadence occurrence at the granule the cadence implies, and the standing intention's `subject`, `duration`, `activity`, and `parties` unless overridden. Each instance has its own stability, resolution lifecycle, and retirement. Recurrence SHALL NOT be an attribute of WINDOW.

#### Scenario: Instance generation
- **WHEN** a standing intention has `cadence: FREQ=WEEKLY;BYDAY=TU` and an instance is requested for week 2026-W37
- **THEN** a new intention is created with `window.calendar: 2026-09-15`, the standing intention's `subject`, and `serves: [{id: <standing>, role: instance-of}]`

#### Scenario: Skip one occurrence
- **WHEN** a generated instance is retired with `kind: abandoned`
- **THEN** the standing intention is unchanged and later instances continue to generate

#### Scenario: End the arrangement
- **WHEN** a standing intention is retired
- **THEN** no further instances are generated and existing active instances are unaffected until retired individually
