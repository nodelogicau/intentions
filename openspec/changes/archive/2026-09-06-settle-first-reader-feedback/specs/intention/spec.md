## RENAMED Requirements

- FROM: `### Requirement: Standing intentions and generated instances`
- TO: `### Requirement: Recurring intentions and generated instances`

- FROM: `### Requirement: Standing intention policies`
- TO: `### Requirement: Policies are termini`

## MODIFIED Requirements

### Requirement: Intention fields

An INTENTION SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); optional `firmed_under` (the id of the policy under which a harness set `firm`); optional `activity`; optional `location` (a list of absolute URIs at one of which the intention must happen; absent means anywhere); optional `parties` (URIs of other required particulars, whose availability resolution must satisfy); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `occurrence` (on generated instances only); optional `placement`; optional `preference` (see Resolution); optional `auto_select` and `auto_firm` (termini only); optional `reference` (informal pointer to a DKF claim); `source`; `timestamp`; `acknowledgements` (see Consistency); and at most one `retired` record.

The scheduling projection of an INTENTION SHALL be: `subject`, `duration`, `window`, `stability`, `activity`, `location`, `parties`, `serves`, `cadence`, `occurrence`, `placement`, `retired.kind`. `version` and `firmed_under` are not in it.

#### Scenario: Minimal intention
- **WHEN** an intention is written with only `title` and `stability: tentative` in a workspace with default `subject` and `source.author`
- **THEN** it is valid, the file carries `version` after `id`, the default `subject`, `source.author`, and a `timestamp`, it carries no window or duration, and it cannot be resolved until it has both

#### Scenario: Subject without default
- **WHEN** an intention is written without `subject` in a workspace with no `defaults.subject`
- **THEN** the write is refused

#### Scenario: Own supply is by subject
- **WHEN** an intention with `subject: https://example.org/people/ben` is resolved
- **THEN** its own supply is the eligible availability whose `subject` is that URI

### Requirement: Stability

`stability` SHALL be `tentative` or `firm`. A firm intention SHALL be treated by resolution as costly to reconsider; a tentative one as cheap. Changing stability SHALL be an explicit edit and SHALL change the version. `firm` SHALL be set only by an act whose `source` carries no `harness`, or by a harness acting under a policy of the subject whose `auto_firm` condition the intention satisfies, in which case the write SHALL set `firmed_under` to that policy's id. `firmed_under` SHALL be required on any intention whose `stability` is `firm` and whose `source` carries a harness, and SHALL name an active terminus of the same subject carrying `auto_firm`. A person firming by their own act SHALL leave `firmed_under` absent. Whether the condition was satisfied is checked at write time; validation checks that the named policy exists and is a policy.

#### Scenario: Firming
- **WHEN** a person marks an intention `firm`
- **THEN** subsequent resolutions of other intentions rank placements that would displace it below placements that would not, and the file carries no `firmed_under`

#### Scenario: Harness firms without policy
- **WHEN** a write whose `source.harness` is set changes `stability` to `firm` and names no policy
- **THEN** the write is refused and validation reports an error

#### Scenario: Harness firms under policy
- **WHEN** a harness firms a twenty-minute intention citing a terminus of the subject carrying `auto_firm: {max_duration: PT30M}`
- **THEN** the write is accepted, the file carries `firmed_under: <policy id>`, and the version changes only for the stability edit

#### Scenario: Policy named is not a policy
- **WHEN** an intention carries `firmed_under` naming an intention with a window or without `auto_firm`
- **THEN** validation reports an error

#### Scenario: Harness drafts tentative
- **WHEN** a harness writes a new intention with `stability: tentative`
- **THEN** the write is accepted

### Requirement: The serves graph has two teleological roles

Each entry in `serves` SHALL be `{id, role}` where `role` is one of `in-order-to` (this intention is a means to the target intention), `for-the-sake-of` (the target is this intention's terminus), or `instance-of` (this intention is a generated instance of the target recurring intention). No other role SHALL be admitted on `serves`. RFC 9253 relation types SHALL NOT be used on `serves`; temporal relations belong to WINDOW.

The serves graph is a directed acyclic graph, not a tree: an intention MAY serve several targets and several intentions MAY converge on one target.

#### Scenario: Multiple ends
- **WHEN** an intention lists two `in-order-to` targets
- **THEN** both are valid and the intention appears under both when the graph is walked inward

#### Scenario: Unknown role
- **WHEN** `serves` contains `{id: int_B, role: PARENT}`
- **THEN** the write is refused and validation reports an error

### Requirement: Terminus

A terminus is an INTENTION with no `serves` entries, no `window`, and no `duration`: a held self-understanding ("being someone who follows through") or a policy. A terminus MAY carry `reference` pointing informally at a DKF claim. A terminus SHALL NOT carry outbound `serves` references; validation SHALL report an error if an intention targeted by a `for-the-sake-of` reference has any `serves` entries. The word "standing intention", where used, means a terminus, never a recurring intention.

#### Scenario: Chain closes on a terminus
- **WHEN** intention A serves B `in-order-to` and B serves T `for-the-sake-of`, and T has no `serves`
- **THEN** validation passes and T is reported as the terminus of A

#### Scenario: Terminus with outbound reference
- **WHEN** an intention targeted by `for-the-sake-of` itself carries a `serves` entry
- **THEN** validation reports an error on the terminus

### Requirement: Recurring intentions and generated instances

An INTENTION carrying `cadence` is a recurring intention, and its window SHALL carry a calendar anchor for the cadence to expand within. Instances SHALL be new INTENTION objects, each carrying `serves: [{id: <recurring>, role: instance-of}]`, `occurrence` (the EDTF granule the cadence produced), a `window` derived from that occurrence, and the recurring intention's `subject`, `duration`, `activity`, and `parties` unless overridden. Each instance has its own stability, resolution lifecycle, and retirement. Recurrence SHALL NOT be an attribute of WINDOW. A recurring intention is not a terminus and SHALL NOT carry `auto_select` or `auto_firm`.

#### Scenario: Instance generation
- **WHEN** a recurring intention has `cadence: FREQ=WEEKLY;BYDAY=TU` and an instance is generated for week 2026-W37
- **THEN** a new intention is created with `occurrence: 2026-09-15`, `window.calendar: 2026-09-15`, the recurring intention's `subject`, and `serves: [{id: <recurring>, role: instance-of}]`

#### Scenario: Skip one occurrence
- **WHEN** a generated instance is retired with `kind: abandoned`
- **THEN** the recurring intention is unchanged and later instances continue to generate

#### Scenario: End the arrangement
- **WHEN** a recurring intention is retired
- **THEN** no further instances are generated and existing active instances are unaffected until retired individually

#### Scenario: Recurring intention with a condition
- **WHEN** an intention with `cadence` is written with `auto_firm`
- **THEN** the write is refused and validation reports an error

### Requirement: Policies are termini

A policy is a terminus carrying `auto_select` or `auto_firm`; each SHALL be a condition over an intention being acted on with terms `max_duration` (ISO 8601 duration) and `stability` (`tentative` or `firm`). A condition is satisfied when every term it states holds for the intention. `auto_select` and `auto_firm` SHALL be admitted on termini only; an intention with a window, a duration, or any `serves` entry SHALL NOT carry them, and validation SHALL report an error if it does. These are the only means by which a harness may select a candidate or set `firm` without a person's direct act.

#### Scenario: Policy condition met
- **WHEN** a terminus carries `auto_firm: {max_duration: PT30M}` and a harness firms a twenty-minute intention citing it
- **THEN** the write is accepted and the intention carries `firmed_under` naming the terminus

#### Scenario: Policy condition not met
- **WHEN** the same policy exists and a harness attempts to firm a two-hour intention citing it
- **THEN** the write is refused

#### Scenario: Condition on a scheduled intention
- **WHEN** an intention with a `window` is written with `auto_select`
- **THEN** the write is refused and validation reports an error
