## MODIFIED Requirements

### Requirement: intention_firm refuses a harness without a policy
`intention_firm` SHALL refuse a call whose `source` carries a harness unless `policy` names an active terminus of the subject carrying `auto_firm` whose condition the intention satisfies, and SHALL then write `firmed_under`. A call whose `source` carries no harness SHALL firm by the person's own act and leave `firmed_under` absent. When the intention being firmed is itself a terminus, `intention_firm` SHALL refuse any call that names a `policy` and SHALL refuse any call whose `source` carries a harness, so that a terminus is firmed only by the person.

#### Scenario: Harness without policy
- **WHEN** `intention_firm` is called with `source.harness` set and no `policy`
- **THEN** the call is refused and the intention stays tentative

#### Scenario: Terminus under a policy
- **WHEN** `intention_firm` is called on a terminus with `policy` set
- **THEN** the call is refused, whatever the policy's condition
