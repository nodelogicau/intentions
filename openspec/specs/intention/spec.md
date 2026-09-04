# Intention

## Purpose

Defines INTENTION, the third leg of the duration/window/intention triad and the object that carries what a person means to do. The design draws on Heidegger's account of projection (Entwurf) and the referential totality of in-order-to relations terminating in a for-the-sake-of-which, and on Bratman's planning theory: intentions are future-directed, conduct-controlling, resistant to casual reconsideration, mutually consistent, filled in incrementally, and terminate in self-governing policies.

An intention involves no other party. When it must interlock with someone else it crystallises into a COMMITMENT.

## Requirements

### Requirement: Intention fields

An INTENTION SHALL carry: `id`; `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `activity` (a term from the workspace activity-type vocabulary, matched against availability conditionals); optional `parties` (URIs of other required particulars, whose availability resolution must satisfy); `status`; optional `placement`; optional `reference` (informal pointer to a DKF claim); optional `preference` (see Resolution); and `acknowledgements` (see Consistency).

The scheduling projection of an INTENTION SHALL be: `duration`, `window`, `stability`, `serves`, `cadence`, `activity`, `parties`, `status`, `placement`.

#### Scenario: Minimal intention
- **WHEN** an intention is written with only `title`, `stability: tentative`, and `status: active`
- **THEN** it is valid, carries no window or duration, and cannot be resolved until it has both

### Requirement: Stability

`stability` SHALL be `tentative` or `firm`. A firm intention SHALL be treated by resolution as costly to reconsider; a tentative one as cheap. Changing stability SHALL be an explicit edit and SHALL change the version.

#### Scenario: Firming
- **WHEN** a person marks an intention `firm`
- **THEN** subsequent resolutions of other intentions rank placements that would displace it below placements that would not

### Requirement: The serves graph has two teleological roles

Each entry in `serves` SHALL be `{id, role}` where `role` is one of `in-order-to` (this intention is a means to the target intention), `for-the-sake-of` (the target is this intention's terminus), or `instance-of` (this intention is a generated instance of the target standing intention). No other role SHALL be admitted on `serves`. RFC 9253 relation types SHALL NOT be used on `serves`; temporal relations belong to WINDOW.

The serves graph is a directed acyclic graph, not a tree: an intention MAY serve several targets and several intentions MAY converge on one target.

#### Scenario: Multiple ends
- **WHEN** an intention lists two `in-order-to` targets
- **THEN** both are valid and the intention appears under both when the graph is walked inward

#### Scenario: Unknown role
- **WHEN** `serves` contains `{id: int_B, role: PARENT}`
- **THEN** the write is refused and validation reports an error

### Requirement: Terminus

A terminus is an INTENTION with no `serves` entries, no `window`, and no `duration`: a self-governing policy or a held self-understanding ("being someone who follows through"). A terminus MAY carry `reference` pointing informally at a DKF claim. A terminus SHALL NOT carry outbound `serves` references; validation SHALL report an error if an intention targeted by a `for-the-sake-of` reference has any `serves` entries.

#### Scenario: Chain closes on a terminus
- **WHEN** intention A serves B `in-order-to` and B serves T `for-the-sake-of`, and T has no `serves`
- **THEN** validation passes and T is reported as the terminus of A

#### Scenario: Terminus with outbound reference
- **WHEN** an intention targeted by `for-the-sake-of` itself carries a `serves` entry
- **THEN** validation reports an error on the terminus

### Requirement: Standing intentions and generated instances

An INTENTION carrying `cadence` is a standing intention. Instances SHALL be generated on demand as new INTENTION objects, each carrying `serves: [{id: <standing>, role: instance-of}]`, a `window` derived from the cadence occurrence at the granule the cadence implies, and the standing intention's `duration`, `activity`, and `parties` unless overridden. Each instance has its own stability, resolution lifecycle, and retirement. Recurrence SHALL NOT be an attribute of WINDOW.

#### Scenario: Instance generation
- **WHEN** a standing intention has `cadence: FREQ=WEEKLY;BYDAY=TU` and an instance is requested for week 2026-W37
- **THEN** a new intention is created with `window.calendar: 2026-09-15` and `serves: [{id: <standing>, role: instance-of}]`

#### Scenario: Skip one occurrence
- **WHEN** a generated instance is retired as `abandoned`
- **THEN** the standing intention is unchanged and later instances continue to generate

#### Scenario: End the arrangement
- **WHEN** a standing intention is retired
- **THEN** no further instances are generated and existing active instances are unaffected until retired individually

### Requirement: Retirement kinds

`status` SHALL be one of `active`, `fulfilled` (discharged, a positive terminal state), `abandoned` (no longer held, no replacement), or `superseded` (replaced by a specific other intention, in which case `superseded_by` SHALL carry that intention's id). Each terminal status is final; a retired intention SHALL NOT be edited further.

#### Scenario: Superseded
- **WHEN** an intention is retired as `superseded` with `superseded_by: int_C`
- **THEN** validation requires int_C to exist and reports an error if it does not

#### Scenario: Superseded without target
- **WHEN** an intention is retired as `superseded` without `superseded_by`
- **THEN** the write is refused

### Requirement: Cycle prevention

A write that would add a `serves` reference closing a cycle SHALL be refused. Validation SHALL detect cycles in the serves graph, regardless of how they arose, and report each strongly-connected component as an error. Every intention in a detected cycle SHALL be treated as unresolvable and SHALL carry a `cycle` flag; intentions outside the cycle SHALL continue to function.

#### Scenario: Write-time refusal
- **WHEN** A serves B and a write attempts to make B serve A
- **THEN** the write is refused with a message naming the cycle

#### Scenario: Cycle by merge
- **WHEN** a merge produces a cycle A → B → A
- **THEN** validation reports an error naming A and B, resolution refuses both, and unrelated intention C still resolves

### Requirement: Reconsideration is triggered by conflict, not by sweep

Whether an existing intention should be reconsidered SHALL be surfaced when a new or changed intention conflicts with it (see Consistency), not by any background expiry mechanism. Intentions have no validity horizon.

#### Scenario: Conflict surfaces reconsideration
- **WHEN** a new firm intention cannot be placed without displacing an existing tentative one
- **THEN** the existing intention is surfaced for reconsideration in the resolution output and its status is not changed automatically
