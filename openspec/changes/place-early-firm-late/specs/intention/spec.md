## MODIFIED Requirements

### Requirement: Terminus

A terminus is an INTENTION with no `serves` entries, no `window`, and no `duration`: a held self-understanding ("being someone who follows through") or a policy. A terminus MAY carry `reference` pointing informally at a DKF claim. A terminus SHALL NOT carry outbound `serves` references; validation SHALL report an error if an intention targeted by a `for-the-sake-of` reference has any `serves` entries. The word "standing intention", where used, means a terminus, never a recurring intention.

A terminus that is a self-understanding SHOULD be titled as who the person is, not as something to do: "being someone who follows through", not "follow through". The test is whether the title names a person or a task. Validation SHALL NOT reject a terminus for its wording.

#### Scenario: Chain closes on a terminus
- **WHEN** intention A serves B `in-order-to` and B serves T `for-the-sake-of`, and T has no `serves`
- **THEN** validation passes and T is reported as the terminus of A

#### Scenario: Terminus with outbound reference
- **WHEN** an intention targeted by `for-the-sake-of` itself carries a `serves` entry
- **THEN** validation reports an error on the terminus

#### Scenario: Terminus titled as a task
- **WHEN** a terminus is titled "follow through" rather than "being someone who follows through"
- **THEN** validation passes, and a conforming conventions file or skill MAY advise the noun form
