## MODIFIED Requirements

### Requirement: Terminus

A terminus is an INTENTION with no `serves` entries, no `window`, and no `duration`: a practice the person holds ("following through") or a policy. A terminus MAY carry `reference` pointing informally at a DKF claim. A terminus SHALL NOT carry outbound `serves` references; validation SHALL report an error if an intention targeted by a `for-the-sake-of` reference has any `serves` entries. The word "standing intention", where used, means a terminus, never a recurring intention.

A terminus that is a practice SHOULD be titled as something the person chooses to keep doing, not as who they are and not as something that can be finished: "following through", not "being someone who follows through" and not "follow through on the board pack". The test is whether the title could ever be done. A terminus has no window and no duration and is never finished, so a title that could be finished names a task, and a title that names a property of the person names an identity rather than a choice. Validation SHALL NOT reject a terminus for its wording.

A terminus is the person's word. A terminus is inert until it is `firm`: it grounds nothing and authorises nothing. No policy applies to a terminus, so `firm` on a terminus SHALL come only from an act whose `source` carries no harness. A harness MAY write a terminus with `stability: tentative`; validation SHALL report a tentative terminus at info level as a draft, and it grounds no intention until the person firms it. A terminus grounds only intentions of its own `subject`.

#### Scenario: Chain closes on a terminus
- **WHEN** intention A serves B `in-order-to` and B serves T `for-the-sake-of`, and T has no `serves`
- **THEN** validation passes and T is reported as the terminus of A

#### Scenario: Terminus with outbound reference
- **WHEN** an intention targeted by `for-the-sake-of` itself carries a `serves` entry
- **THEN** validation reports an error on the terminus

#### Scenario: Terminus titled as a task
- **WHEN** a terminus is titled "follow through on the board pack" rather than "following through"
- **THEN** validation passes, and a conforming conventions file or skill MAY advise the practice form

#### Scenario: Terminus titled as an identity
- **WHEN** a terminus is titled "being someone who follows through" rather than "following through"
- **THEN** validation passes, and a conforming conventions file or skill MAY advise the practice form

#### Scenario: Harness drafts a terminus
- **WHEN** a write whose `source.harness` is set creates a terminus with `stability: tentative`
- **THEN** the write is accepted, validation reports the terminus as a draft at info level, and intentions reaching only it are unserved

#### Scenario: Harness firms a terminus under a policy
- **WHEN** a write whose `source.harness` is set attempts to firm a terminus citing a policy
- **THEN** the write is refused, because no policy applies to a terminus

#### Scenario: Person firms a terminus
- **WHEN** an act whose `source` carries no harness sets a terminus `firm`
- **THEN** the write is accepted and every intention reaching it is served

### Requirement: Retirement kinds

An intention's `retired.kind` SHALL be one of `fulfilled` (discharged, a positive terminal state), `abandoned` (no longer held, no replacement), or `superseded` (replaced by a specific other intention, in which case `superseded_by` SHALL carry that intention's id). A terminus SHALL admit `abandoned` and `superseded` only, since a practice is never finished, and its `superseded_by` SHALL name a terminus of the same `subject`, or SHALL be a list of two or more distinct termini of the same `subject`, each firm or tentative, sorted by id, recording that one practice was refined into several. A single successor SHALL be written as an id, never as a one-element list. `superseded_by` on an intention that is not a terminus SHALL be a single id. Each kind is final; a retired intention SHALL NOT be edited further except to append acknowledgements.

#### Scenario: Superseded
- **WHEN** an intention is retired with `retired: {kind: superseded, superseded_by: int_C, ...}`
- **THEN** validation requires int_C to exist and reports an error if it does not

#### Scenario: Superseded without target
- **WHEN** an intention is retired with `kind: superseded` and no `superseded_by`
- **THEN** the write is refused

#### Scenario: Fulfilled with reason
- **WHEN** an intention is retired with `kind: fulfilled` and a `reason`
- **THEN** the record carries the reason, a timestamp, and the source of the retiring act, and the intention's version changes

#### Scenario: Fulfilled terminus
- **WHEN** a terminus carries `retired: {kind: fulfilled}`
- **THEN** validation reports an error, and a retirement act naming that kind on a terminus is refused

#### Scenario: Terminus superseded by a scheduled intention
- **WHEN** a terminus is retired as `superseded` with `superseded_by` naming an intention that has a window
- **THEN** the write is refused and validation reports an error

#### Scenario: Terminus split
- **WHEN** a terminus is retired with `retired: {kind: superseded, superseded_by: [int_U, int_V], ...}` and int_U and int_V are termini of its subject
- **THEN** the record is valid, and the terminus's version changes only by `retired.kind`

#### Scenario: List on a plan
- **WHEN** an intention with a window is retired as `superseded` with `superseded_by` a list
- **THEN** the write is refused and validation reports an error

#### Scenario: One-element list
- **WHEN** a terminus carries `superseded_by: [int_U]`
- **THEN** validation reports an error naming the single id as the form
