## MODIFIED Requirements

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields, in canonical order: `id`; `version`; `intention` (id); `placement`; `selector` (either `person` or the id of the policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces, sorted); `source`; and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection. On selection the intention gains the `placement`, including `location` where the intention or supply constrained it, and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`.

The scheduling projection of a RESOLUTION SHALL be: `intention`, `placement`, `selector`, `displaced`.

#### Scenario: Person selects
- **WHEN** a person selects the second candidate
- **THEN** a resolution record is written with `version` after `id`, `selector: person`, `source.author` set to that person, the intention gains the placement, and the record lists anything displaced

#### Scenario: Harness selects under policy
- **WHEN** a harness auto-selects under a policy the person holds
- **THEN** the record carries the policy id as `selector` and the harness in `source.harness`

#### Scenario: Multi-party selection
- **WHEN** an intention with one counterparty is resolved
- **THEN** a commitment is created with the subject and the counterparty both at `tentative` and the resolution record references it

### Requirement: Auto-selection only under a self-governing policy

Automatic selection SHALL be permitted only when a policy of the subject, that is a terminus carrying `auto_select` with a condition (for example `max_duration: PT30M`, `stability: tentative`), is satisfied by the intention. The resolution record SHALL then carry that policy's id as `selector`. No workspace-level or tool-level default SHALL auto-select.

#### Scenario: Policy authorises
- **WHEN** a policy declares `auto_select: {max_duration: PT30M}` and a fifteen-minute intention resolves with at least one rank-1 candidate
- **THEN** the top candidate is selected and the record carries the policy id

#### Scenario: Policy does not cover
- **WHEN** the same policy exists and a two-hour intention resolves
- **THEN** no selection occurs and the candidate set is returned for the person
