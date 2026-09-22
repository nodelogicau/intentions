## MODIFIED Requirements

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
