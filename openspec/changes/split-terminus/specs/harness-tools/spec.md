## MODIFIED Requirements

### Requirement: intention_retire guards termini
`intention_retire` SHALL refuse, on a terminus, the kind `fulfilled`; `superseded` with a `superseded_by` that is not a terminus of the same subject, or a list containing anything but two or more distinct termini of the same subject; any retirement that would leave a served intention with no firm terminus, naming those intentions and the alternatives of setting the terminus tentative or superseding it with one or more termini, at least one of them firm; and a call whose `source` carries a harness, unless the terminus is tentative and its own `source` carries a harness. `superseded_by` SHALL accept an id or a list of ids. A list SHALL be refused on anything but a terminus. A result that leaves dependents resting on a split terminus SHALL carry the info finding for each of them.

#### Scenario: Refusal names what rests on it
- **WHEN** `intention_retire` is called on the sole firm terminus of two unretired intentions with `kind: abandoned`
- **THEN** the call is refused, naming both intentions, `intention_edit` to set the terminus tentative, and supersession

#### Scenario: Harness and a person's draft
- **WHEN** `intention_retire` is called with `source.harness` set on a tentative terminus whose own `source` carries no harness
- **THEN** the call is refused

#### Scenario: Split through the tool
- **WHEN** `intention_retire` is called by the person on a terminus with `kind: superseded` and `superseded_by: [int_U, int_V]`, int_U firm
- **THEN** the retirement is written with the list sorted by id, and the result names each dependent left resting on the split

#### Scenario: List on a non-terminus
- **WHEN** `intention_retire` is called on an intention with a window and `superseded_by` a list
- **THEN** the call is refused
