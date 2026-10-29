## ADDED Requirements

### Requirement: intention_retire guards termini
`intention_retire` SHALL refuse, on a terminus, the kind `fulfilled`; `superseded` with a `superseded_by` that is not a terminus of the same subject; any retirement that would leave a served intention with no firm terminus, naming those intentions and the alternatives of setting the terminus tentative or superseding it with a firm terminus; and a call whose `source` carries a harness, unless the terminus is tentative and its own `source` carries a harness.

#### Scenario: Refusal names what rests on it
- **WHEN** `intention_retire` is called on the sole firm terminus of two unretired intentions with `kind: abandoned`
- **THEN** the call is refused, naming both intentions, `intention_edit` to set the terminus tentative, and supersession

#### Scenario: Harness and a person's draft
- **WHEN** `intention_retire` is called with `source.harness` set on a tentative terminus whose own `source` carries no harness
- **THEN** the call is refused
