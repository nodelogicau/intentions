## ADDED Requirements

### Requirement: Every intention reaches a terminus
An intention that is not a terminus SHALL reach a firm terminus of its own `subject` through its `serves` graph, by any path of `in-order-to`, `for-the-sake-of` and `instance-of` references. Reachability is the test, not the presence of an entry: a chain that ends on a scheduled intention, or on a tentative terminus, is unserved. Generated instances reach a terminus through the recurring intention they are `instance-of`. In this revision validation SHALL report an unserved intention at warning level, naming the intention and the fix, and a write that would leave an intention unserved SHALL be accepted and SHALL carry the same finding in its result. A later revision that breaks files SHALL raise both to refusal.

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

#### Scenario: Unserved write in this revision
- **WHEN** a harness adds an intention with an empty `serves` in a workspace holding no terminus
- **THEN** the write is accepted and the result carries the unserved warning naming the intention

## MODIFIED Requirements

### Requirement: Terminus

A terminus is an INTENTION with no `serves` entries, no `window`, and no `duration`: a held self-understanding ("being someone who follows through") or a policy. A terminus MAY carry `reference` pointing informally at a DKF claim. A terminus SHALL NOT carry outbound `serves` references; validation SHALL report an error if an intention targeted by a `for-the-sake-of` reference has any `serves` entries. The word "standing intention", where used, means a terminus, never a recurring intention.

A terminus that is a self-understanding SHOULD be titled as who the person is, not as something to do: "being someone who follows through", not "follow through". The test is whether the title names a person or a task. Validation SHALL NOT reject a terminus for its wording.

A terminus is the person's word. A terminus SHALL be `firm` to ground anything, and no policy applies to a terminus, so `firm` on a terminus SHALL come only from an act whose `source` carries no harness. A harness MAY write a terminus with `stability: tentative`; validation SHALL report a tentative terminus at info level as a draft, and it grounds no intention until the person firms it. A terminus grounds only intentions of its own `subject`.

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

### Requirement: Policies are termini

A policy is a terminus carrying `auto_select` or `auto_firm`; each SHALL be a condition over an intention being acted on with terms `max_duration` (ISO 8601 duration) and `stability` (`tentative` or `firm`). A condition is satisfied when every term it states holds for the intention. `auto_select` and `auto_firm` SHALL be admitted on termini only; an intention with a window, a duration, or any `serves` entry SHALL NOT carry them, and validation SHALL report an error if it does. These are the only means by which a harness may select a candidate or set `firm` without a person's direct act. A policy's condition applies only to intentions that are not termini: no policy SHALL firm a terminus or select for one.

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
