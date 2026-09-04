## MODIFIED Requirements

### Requirement: Demand and supply

Resolution SHALL take one unretired, unplaced intention with both `duration` and `window` as demand. Supply SHALL be the intersection of eligible availability whose `subject` equals the intention's `subject` and, for every URI in the intention's `parties`, eligible availability whose `subject` equals that URI. Availability is eligible only if it carries no `retired` record, its validity horizon has not passed, its `conditional` (if any) includes the intention's `activity`, and its scope is visible to the resolver.

#### Scenario: Multi-party intersection
- **WHEN** an intention lists a counterparty and a room in `parties`
- **THEN** candidates are placements inside the intersection of the subject's, the counterparty's, and the room's eligible availability

#### Scenario: No supply
- **WHEN** no eligible availability overlaps the intention's window for every required party
- **THEN** resolution returns an empty candidate set and names which party had no supply

#### Scenario: Retired availability ignored
- **WHEN** the only availability matching the intention's subject carries a `retired` record
- **THEN** resolution reports no supply for the subject

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields: `id`; `source`; `intention` (id); `placement`; `selector` (either `person` or the id of the self-governing policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces); and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection. On selection the intention gains the `placement` and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`.

The scheduling projection of a RESOLUTION SHALL be: `intention`, `placement`, `selector`, `displaced`.

#### Scenario: Person selects
- **WHEN** a person selects the second candidate
- **THEN** a resolution record is written with `selector: person`, `source.author` set to that person, the intention gains the placement, and the record lists anything displaced

#### Scenario: Harness selects under policy
- **WHEN** a harness auto-selects under a policy the person holds
- **THEN** the record carries the policy id as `selector` and the harness in `source.harness`

#### Scenario: Multi-party selection
- **WHEN** an intention with one counterparty is resolved
- **THEN** a commitment is created with the subject and the counterparty both at `tentative` and the resolution record references it
