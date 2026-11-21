## MODIFIED Requirements

### Requirement: A desire serves only a terminus, which may be a draft
`serves` on a DESIRE SHALL admit only entries whose `role` is `for-the-sake-of`, and each target SHALL be a terminus of the same `subject`. The terminus MAY be tentative: a desire is not grounded by it and nothing rests on either. An empty `serves` is valid; the grounding rule for intentions SHALL NOT apply to desires.

#### Scenario: Draft want, draft terminus
- **WHEN** a harness writes a tentative terminus and a DESIRE serving it `for-the-sake-of`
- **THEN** both writes are accepted, the terminus is reported as a draft, and the desire is not reported as unserved

#### Scenario: In-order-to on a desire
- **WHEN** a DESIRE's `serves` carries an entry with role `in-order-to`
- **THEN** the write is refused and validation reports an error

### Requirement: Adoption writes the intention and then retires the desire
Adopting a DESIRE SHALL create a new INTENTION carrying the desire's `subject`, `title`, `description`, `serves`, `reference`, `activity`, `location` and `parties`, the `duration` and `window` the adopting act supplies, `stability: tentative`, and the act's `source`; and SHALL then append `retired: {kind: adopted, adopted_as: <the new intention's id>}` to the desire. The intention is the record of the adoption; no other record SHALL be written. Adoption of a retired desire SHALL be refused. Adoption SHALL be refused where the intention it would write is a terminus, that is where the desire's `serves` is empty and the act supplies neither `duration` nor `window`; the refusal SHALL name what is missing, a why or a when. An adopted want is a plan; a terminus is declared, not adopted. This refusal is not subsumed by the rule that every intention reaches a terminus, because a terminus is exempt from that rule, so it SHALL stand in every revision. A harness MAY still draft a terminus through the ordinary intention write, which is a different act with a different meaning. A harness MAY adopt, since adopting is drafting an intention. The new intention is subject to every rule an intention is subject to, including the grounding warning where its terminus is tentative.

#### Scenario: Harness adopts
- **WHEN** a harness adopts a desire supplying `duration: PT30M` and `window: {calendar: this-week}`
- **THEN** a tentative intention is written with the desire's title, serves, activity, location and parties and the supplied duration and window, the desire is retired as `adopted` naming it, and the result carries both ids

#### Scenario: Adopting a draft-grounded want
- **WHEN** the adopted desire served a tentative terminus
- **THEN** the new intention is reported as unserved at warning level until the person firms the terminus

#### Scenario: Adopting twice
- **WHEN** adoption is attempted on a desire already carrying a `retired` record
- **THEN** the act is refused and nothing is written

#### Scenario: Bare adoption refused
- **WHEN** a desire with an empty `serves` is adopted with neither `duration` nor `window`
- **THEN** the act is refused, nothing is written, and the refusal says the want needs a why or a when

#### Scenario: A why and no when
- **WHEN** a desire serving a terminus is adopted with neither `duration` nor `window`
- **THEN** a tentative intention is written with the `serves` and no window, and `unresolved` reports it as incomplete

#### Scenario: A when and no why
- **WHEN** a desire with an empty `serves` is adopted with a `window`
- **THEN** a tentative intention is written and validation reports it as unserved at warning level
