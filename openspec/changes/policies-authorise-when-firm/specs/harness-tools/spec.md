## MODIFIED Requirements

### Requirement: select is the recorded act; resolve chooses nothing
`resolve` SHALL rank candidates and write nothing. `select` SHALL take exactly one of a person's `candidate` index or a harness's `policy` id, SHALL refuse a call carrying both or neither, and SHALL write the RESOLUTION record, the placement, and a commitment when parties are involved. A `policy` SHALL be honoured only where it names a firm terminus of the subject carrying `auto_select` whose condition the intention satisfies; a tentative policy is refused, and the refusal names it and the act that firms it.

#### Scenario: Both given
- **WHEN** `select` is called with both `candidate` and `policy`
- **THEN** the call is refused as a usage error and nothing is written

#### Scenario: Policy not satisfied
- **WHEN** `select` is called with a `policy` whose `auto_select` condition the intention does not satisfy
- **THEN** the call is refused and nothing is written

#### Scenario: Policy is a draft
- **WHEN** `select` is called with a `policy` whose `stability` is `tentative`
- **THEN** the call is refused, nothing is written, and the error names the draft and the act that firms it

### Requirement: intention_firm refuses a harness without a policy
`intention_firm` SHALL refuse a call whose `source` carries a harness unless `policy` names an active, firm terminus of the subject carrying `auto_firm` whose condition the intention satisfies, and SHALL then write `firmed_under`. A call whose `source` carries no harness SHALL firm by the person's own act and leave `firmed_under` absent. When the intention being firmed is itself a terminus, `intention_firm` SHALL refuse any call that names a `policy` and SHALL refuse any call whose `source` carries a harness, so that a terminus is firmed only by the person.

#### Scenario: Harness without policy
- **WHEN** `intention_firm` is called with `source.harness` set and no `policy`
- **THEN** the call is refused and the intention stays tentative

#### Scenario: Terminus under a policy
- **WHEN** `intention_firm` is called on a terminus with `policy` set
- **THEN** the call is refused, whatever the policy's condition

#### Scenario: Policy is a draft
- **WHEN** `intention_firm` is called with `source.harness` set and `policy` naming a tentative terminus carrying `auto_firm`
- **THEN** the call is refused and the error names the draft policy and the act that firms it
