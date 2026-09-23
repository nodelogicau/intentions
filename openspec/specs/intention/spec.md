# Intention

## Purpose

Defines INTENTION, the third leg of the duration/window/intention triad and the object that carries what a person means to do. The design draws on Heidegger's account of projection (Entwurf) and the referential totality of in-order-to relations terminating in a for-the-sake-of-which, and on Bratman's planning theory: intentions are future-directed, conduct-controlling, resistant to casual reconsideration, mutually consistent, filled in incrementally, and terminate in self-governing policies.

An intention involves no other party. When it must interlock with someone else it crystallises into a COMMITMENT.

## Requirements

### Requirement: Intention fields

An INTENTION SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); optional `firmed_under` (the id of the policy under which a harness set `firm`); optional `activity`; optional `location` (a list of absolute URIs at one of which the intention must happen; absent means anywhere); optional `parties` (bare URIs of other required particulars, whose availability resolution must satisfy; a different shape from a commitment's `parties`, which carry a status); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `occurrence` (on generated instances only); optional `placement`; optional `preference` (see Resolution); optional `auto_select` and `auto_firm` (termini only); optional `reference` (informal pointer to a DKF claim); `source`; `timestamp`; `acknowledgements` (see Consistency); and at most one `retired` record.

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

`stability` SHALL be `tentative` or `firm`. A firm intention SHALL be treated by resolution as costly to reconsider; a tentative one as cheap. Changing stability SHALL be an explicit edit and SHALL change the version. `firm` SHALL be set only by an act whose `source` carries no `harness`, or by a harness acting under a policy of the subject whose `auto_firm` condition the intention satisfies, in which case the write SHALL set `firmed_under` to that policy's id. `firmed_under` SHALL be required on any intention whose `stability` is `firm` and whose `source` carries a harness, and SHALL name an active, firm terminus of the same subject carrying `auto_firm`. A person firming by their own act SHALL leave `firmed_under` absent. Whether the condition was satisfied is checked at write time; validation checks that the named policy exists, is a policy, and is firm. A person withdrawing a policy, by setting it tentative or retiring it, withdraws what rested on it: every intention firmed under it is then in error until the person re-firms it by their own act or sets it tentative.

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

#### Scenario: Policy named is a draft
- **WHEN** an intention carries `firmed_under` naming a policy whose `stability` is `tentative`
- **THEN** validation reports an error naming the intention and the policy to firm

#### Scenario: Policy withdrawn after firming
- **WHEN** a person sets a policy tentative after a harness has firmed an intention under it
- **THEN** validation reports that intention in error, and the finding says to re-firm by the person's own act or set it tentative

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

A terminus that is a self-understanding SHOULD be titled as who the person is, not as something to do: "being someone who follows through", not "follow through". The test is whether the title names a person or a task. Validation SHALL NOT reject a terminus for its wording.

A terminus is the person's word. A terminus is inert until it is `firm`: it grounds nothing and authorises nothing. No policy applies to a terminus, so `firm` on a terminus SHALL come only from an act whose `source` carries no harness. A harness MAY write a terminus with `stability: tentative`; validation SHALL report a tentative terminus at info level as a draft, and it grounds no intention until the person firms it. A terminus grounds only intentions of its own `subject`.

#### Scenario: Chain closes on a terminus
- **WHEN** intention A serves B `in-order-to` and B serves T `for-the-sake-of`, and T has no `serves`
- **THEN** validation passes and T is reported as the terminus of A

#### Scenario: Terminus with outbound reference
- **WHEN** an intention targeted by `for-the-sake-of` itself carries a `serves` entry
- **THEN** validation reports an error on the terminus

#### Scenario: Terminus titled as a task
- **WHEN** a terminus is titled "follow through" rather than "being someone who follows through"
- **THEN** validation passes, and a conforming conventions file or skill MAY advise the noun form

#### Scenario: Harness drafts a terminus
- **WHEN** a write whose `source.harness` is set creates a terminus with `stability: tentative`
- **THEN** the write is accepted, validation reports the terminus as a draft at info level, and intentions reaching only it are unserved

#### Scenario: Harness firms a terminus under a policy
- **WHEN** a write whose `source.harness` is set attempts to firm a terminus citing a policy
- **THEN** the write is refused, because no policy applies to a terminus

#### Scenario: Person firms a terminus
- **WHEN** an act whose `source` carries no harness sets a terminus `firm`
- **THEN** the write is accepted and every intention reaching it is served

### Requirement: Every intention reaches a terminus
An intention that is not a terminus SHALL reach a firm terminus of its own `subject` through its `serves` graph, by any path of `in-order-to`, `for-the-sake-of` and `instance-of` references. Reachability is the test, not the presence of an entry: a chain that ends on a scheduled intention, or on a tentative terminus, is unserved. Generated instances reach a terminus through the recurring intention they are `instance-of`. Under `intentions/0.1` validation reports an unserved intention at warning level, naming the intention and the fix, and a write that would leave an intention unserved is accepted and carries the same finding in its result. Under `intentions/0.2` validation SHALL report an unserved intention as an error, naming the intention and the fix, and a write that would leave an intention unserved SHALL be refused. A 0.2 reader applies the 0.1 rule to a workspace whose `format` is still `intentions/0.1`.

#### Scenario: Chain ends on a scheduled intention
- **WHEN** A serves B `in-order-to`, B has a window and a duration, and B has no `serves`
- **THEN** validation reports A and B as unserved at warning level

#### Scenario: Chain ends on a tentative terminus
- **WHEN** A serves T `for-the-sake-of`, T has no window, duration or serves, and T is `tentative`
- **THEN** validation reports A as unserved and T as a draft terminus

#### Scenario: Instance reaches through the recurring intention
- **WHEN** an instance carries only `instance-of` to a recurring intention that serves a firm terminus
- **THEN** the instance is served and validation reports nothing

#### Scenario: Another subject's terminus
- **WHEN** Ada's intention serves Priya's terminus `for-the-sake-of` and no terminus of Ada's
- **THEN** validation reports Ada's intention as unserved

#### Scenario: Unserved write under 0.1
- **WHEN** a harness adds an intention with an empty `serves` in a workspace whose `format` is `intentions/0.1` and which holds no terminus
- **THEN** the write is accepted and the result carries the unserved warning naming the intention

#### Scenario: Unserved write under 0.2
- **WHEN** a harness adds an intention with an empty `serves` in a workspace whose `format` is `intentions/0.2` and which holds no terminus
- **THEN** the write is refused, naming the intention and the fix

### Requirement: Recurring intentions and generated instances

An INTENTION carrying `cadence` is a recurring intention, and its window SHALL carry a calendar anchor for the cadence to expand within. Instances SHALL be new INTENTION objects, each carrying `serves: [{id: <recurring>, role: instance-of}]`, `occurrence` (the EDTF granule the cadence produced), a `window` whose `calendar` is that occurrence and whose `clock` is the recurring intention's `clock` when it has one, and the recurring intention's `subject`, `duration`, `activity`, `location`, and `parties` unless overridden. Each instance has its own stability, resolution lifecycle, and retirement. Recurrence SHALL NOT be an attribute of WINDOW. A recurring intention is not a terminus and SHALL NOT carry `auto_select` or `auto_firm`.

#### Scenario: Instance generation
- **WHEN** a recurring intention has `cadence: FREQ=WEEKLY;BYDAY=TU` and an instance is generated for week 2026-W37
- **THEN** a new intention is created with `occurrence: 2026-09-15`, `window.calendar: 2026-09-15`, the recurring intention's `subject`, and `serves: [{id: <recurring>, role: instance-of}]`

#### Scenario: Instance keeps place and hours
- **WHEN** a recurring intention has `window: {calendar: 2026-09/2026-12, clock: 09:00/12:00}` and `location: [home]`
- **THEN** each instance carries `window: {calendar: <occurrence>, clock: 09:00/12:00}` and `location: [home]`

#### Scenario: Skip one occurrence
- **WHEN** a generated instance is retired with `kind: abandoned`
- **THEN** the recurring intention is unchanged and later instances continue to generate

#### Scenario: End the arrangement
- **WHEN** a recurring intention is retired
- **THEN** no further instances are generated and existing active instances are unaffected until retired individually

#### Scenario: Recurring intention with a condition
- **WHEN** an intention with `cadence` is written with `auto_firm`
- **THEN** the write is refused and validation reports an error

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
- **THEN** the existing intention is surfaced for reconsideration in the resolution output and is neither retired nor re-placed automatically

### Requirement: Activity vocabulary

`activity` on an intention and each term in `activities` on an availability SHALL be a lowercase kebab-case term. The specification SHALL NOT fix the vocabulary; terms are documented in the workspace conventions file. Matching between `activity` and `activities` SHALL be by exact string equality. An unknown term SHALL NOT be a validation error; validation SHALL report at info level any term used by exactly one object.

#### Scenario: Unknown term accepted
- **WHEN** an intention carries `activity: piano-practice` and no other object uses that term
- **THEN** validation passes and reports the term at info level

#### Scenario: Malformed term
- **WHEN** an intention carries `activity: Deep Work`
- **THEN** the write is refused and validation reports an error

### Requirement: Instance generation

Instances of a recurring intention SHALL be materialised by a `generate` operation over a horizon window, which resolution SHALL also run over its own horizon. Generated instances SHALL be written to disk immediately as INTENTION objects. Each instance SHALL carry `occurrence`, the EDTF granule the cadence produced, and generation SHALL be idempotent over that key: generating again over an overlapping horizon SHALL create no second active instance for the same recurring intention and occurrence, and validation SHALL report such a duplicate as an error. The horizon is `resolver.horizon` in `intentions.yaml`, the one planning horizon shared with resolution; the recommended default is four weeks (`P4W`). No background generation SHALL occur.

#### Scenario: Idempotent generation
- **WHEN** `generate` runs twice over horizons that both include 2026-09-15 for a weekly Tuesday recurring intention
- **THEN** exactly one active instance with `occurrence: 2026-09-15` exists

#### Scenario: Skipped then regenerated
- **WHEN** the instance for 2026-09-15 is retired as `abandoned` and `generate` runs again over that week
- **THEN** no new instance for 2026-09-15 is created

#### Scenario: Resolution generates
- **WHEN** resolution runs for an intention whose window lies in the next two weeks
- **THEN** instances of every recurring intention with occurrences within `resolver.horizon` exist on disk before candidates are ranked

### Requirement: Policies are termini

A policy is a terminus carrying `auto_select` or `auto_firm`; each SHALL be a condition over an intention being acted on with terms `max_duration` (ISO 8601 duration) and `stability` (`tentative` or `firm`). A condition is satisfied when every term it states holds for the intention. `auto_select` and `auto_firm` SHALL be admitted on termini only; an intention with a window, a duration, or any `serves` entry SHALL NOT carry them, and validation SHALL report an error if it does. These are the only means by which a harness may select a candidate or set `firm` without a person's direct act. A policy's condition applies only while the policy is `firm` and only to intentions that are not termini: no policy SHALL firm a terminus or select for one. A tentative policy is a draft: a harness MAY write one, and until the person firms it by their own act, firming and selection SHALL refuse to act under it, naming the draft and the act that makes it the person's. Setting a firm policy tentative suspends it; retiring it ends it.

#### Scenario: Policy condition met
- **WHEN** a terminus carries `auto_firm: {max_duration: PT30M}` and a harness firms a twenty-minute intention citing it
- **THEN** the write is accepted and the intention carries `firmed_under` naming the terminus

#### Scenario: Policy condition not met
- **WHEN** the same policy exists and a harness attempts to firm a two-hour intention citing it
- **THEN** the write is refused

#### Scenario: Condition on a scheduled intention
- **WHEN** an intention with a `window` is written with `auto_select`
- **THEN** the write is refused and validation reports an error

#### Scenario: Policy cited for a terminus
- **WHEN** a harness attempts to firm a terminus citing a policy whose condition would otherwise be satisfied
- **THEN** the write is refused

#### Scenario: Policy is a draft
- **WHEN** a harness writes a terminus carrying `auto_firm` with `stability: tentative` and then attempts to firm an intention citing it
- **THEN** the firming is refused, and the refusal names the draft policy and the act that firms it

#### Scenario: Policy suspended
- **WHEN** a person sets a firm policy to `tentative`
- **THEN** no harness act is authorised under it until the person firms it again, and what was firmed under it is reported by validation
