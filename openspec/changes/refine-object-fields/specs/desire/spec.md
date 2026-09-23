## MODIFIED Requirements

### Requirement: DESIRE is the rung below intention
A DESIRE is a want the person has expressed and not yet committed to: a world-to-mind pro-attitude, not a commissive act. A workspace MAY hold desires in `/desires/`, one per file, with ids prefixed `des_`. A DESIRE SHALL carry, in canonical order: `id`; `version`; `subject` (the URI of the particular whose desire this is, applied from `defaults.subject` as for an intention); `title` (prose); `description` (prose, optional); `activity` (optional, a term from the workspace's activity vocabulary); `location` (optional, URIs); `parties` (optional, URIs of other particulars the want involves, kept as a hint); `serves` (possibly empty); `reference` (optional, an informal pointer to a DKF claim); `source`; `timestamp`; and `retired` when retired. A DESIRE SHALL NOT carry `duration`, `window`, `stability`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, or `acknowledgements`, and validation SHALL report an error if it does. A DESIRE SHALL NOT carry a strength, priority, or ranking field.

#### Scenario: A passing remark
- **WHEN** a harness records "call the accountant" as a DESIRE with a title, the workspace's default subject, and an empty `serves`
- **THEN** the write is accepted and validation reports nothing about it

#### Scenario: A desire with a window
- **WHEN** a DESIRE file carries `window`
- **THEN** validation reports an error naming the field

### Requirement: Adoption writes the intention and then retires the desire
Adopting a DESIRE SHALL create a new INTENTION carrying the desire's `subject`, `title`, `description`, `serves`, `reference`, `activity`, `location` and `parties`, the `duration` and `window` the adopting act supplies, `stability: tentative`, and the act's `source`; and SHALL then append `retired: {kind: adopted, adopted_as: <the new intention's id>}` to the desire. The intention is the record of the adoption; no other record SHALL be written. Adoption of a retired desire SHALL be refused. Adoption SHALL be refused where the intention it would write is a terminus, that is where the desire's `serves` is empty and the act supplies neither `duration` nor `window`; the refusal SHALL name what is missing, a why or a when. An adopted want is a plan; a self is declared, not adopted. This refusal is not subsumed by the rule that every intention reaches a terminus, because a terminus is exempt from that rule, so it SHALL stand in every revision. A harness MAY still draft a terminus through the ordinary intention write, which is a different act with a different meaning. A harness MAY adopt, since adopting is drafting an intention. The new intention is subject to every rule an intention is subject to, including the grounding warning where its terminus is tentative.

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

### Requirement: Projection of a DESIRE
The scheduling projection of a DESIRE SHALL be `subject`, `serves`, and `retired.kind`. `title`, `description`, `activity`, `location`, `parties`, `reference`, `source` and `timestamp` SHALL be excluded.

#### Scenario: Prose edit
- **WHEN** a desire's `description` is edited
- **THEN** its version is unchanged

#### Scenario: Terminus changed
- **WHEN** a desire's `serves` gains a `for-the-sake-of` entry
- **THEN** its version changes
