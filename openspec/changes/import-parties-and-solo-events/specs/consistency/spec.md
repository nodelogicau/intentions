## MODIFIED Requirements

### Requirement: A decline against a standing plan is flagged

A `party-declined` flag SHALL be reported when a commitment has any party at `declined` and the intention it fulfils still carries a placement. It SHALL be reported on both the commitment and that intention, each naming the other as counterpart, and its `detail` SHALL name the declining party and whether that party is the intention's subject. A commitment with no `intention`, which is every imported commitment not adopted (see Adopting an imported commitment in Commitment), SHALL NOT raise it, because there is no plan for the decline to disagree with. A commitment whose intention's placement has been cleared SHALL NOT raise it.

The flag SHALL NOT change any party status, clear any placement, or retire anything. It is acknowledgeable like any other flag, and because a party status is in the commitment's projection, a later change to it lapses the acknowledgement and the flag is recomputed.

#### Scenario: Subject declines their own arrangement
- **WHEN** the subject sets their own party entry to `declined` on a commitment created from their placed intention
- **THEN** a `party-declined` flag is reported on the commitment and on the intention, the placement is unchanged, and the detail says the declining party is the subject

#### Scenario: Counterparty declines
- **WHEN** a counterparty declines a commitment whose intention is still placed
- **THEN** the same flag is reported on both objects and the detail names that party as not the subject

#### Scenario: Imported commitment declined
- **WHEN** the subject declines an imported commitment that has not been adopted, and so has no `intention`
- **THEN** no `party-declined` flag is reported and the hour is no longer occupied for them

#### Scenario: Cancelled, not declined
- **WHEN** the commitment is cancelled, clearing the intention's placement
- **THEN** no `party-declined` flag is reported

#### Scenario: Acknowledged and carried on
- **WHEN** a person acknowledges a `party-declined` flag naming a counterparty
- **THEN** the flag is suppressed, the placement stands, and no status changes

#### Scenario: Acknowledgement lapses on a reversal
- **WHEN** an acknowledged declining party later sets their status to `accepted`
- **THEN** the commitment's projection changes, the acknowledgement lapses, and the flag is not reported because no party is declined

#### Scenario: Adopted import declined
- **WHEN** the subject declines an imported commitment that has been adopted for their placed intention
- **THEN** a `party-declined` flag is reported on the commitment and on the intention, and the hour stays occupied by the intention's placement

## ADDED Requirements

### Requirement: A commitment and the intention it fulfils are one occupation

A commitment and the intention named by its `intention` SHALL NOT be reported as a `window-clash` with each other, whatever the commitment's `origin`. Where both occupy the intention's subject over the same interval, that interval SHALL consume the subject's capacity once and SHALL count once as an existing placement in resolution. Each SHALL still be checked against every other object as usual.

#### Scenario: Resolution's commitment
- **WHEN** a multi-party intention is resolved and its commitment created at the same placement
- **THEN** no `window-clash` is reported between the intention and its commitment, and the subject's capacity for that interval is consumed once

#### Scenario: Adopted import
- **WHEN** an imported commitment has been adopted for an intention at the same placement
- **THEN** no `window-clash` is reported between them, and another intention's candidates treat that interval as occupied once
