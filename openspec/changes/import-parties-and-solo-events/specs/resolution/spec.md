## MODIFIED Requirements

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields, in canonical order: `id`; `version`; `intention` (id); `placement`; `selector` (either `person` or the id of the policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces, sorted); `supply` (ids of the availabilities the placement was chosen against, sorted); `presumed` (URIs of the parties that contributed no supply because the workspace does not track them, sorted); `source`; and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection; `supply` records what the selector saw and is not what the placement rests on now, which consistency recomputes; `presumed` records whose time the placement assumes without evidence. On selection the intention gains the `placement`, including `location` where the intention or supply constrained it, and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`. Adopting an imported commitment (see Commitment) SHALL be a selection whose placement is that commitment's: its record carries `selector: person` and `candidates_considered: 1`, the placement need not be among the candidates, `displaced` never lists the adopted commitment, and no commitment is created.

The scheduling projection of a RESOLUTION SHALL be: `intention`, `placement`, `selector`, `displaced`. Neither `supply` nor `presumed` is in it.

#### Scenario: Person selects
- **WHEN** a person selects the second candidate
- **THEN** a resolution record is written with `version` after `id`, `selector: person`, `source.author` set to that person, `supply` naming the availabilities used, the intention gains the placement, and the record lists anything displaced

#### Scenario: Harness selects under policy
- **WHEN** a harness auto-selects under a policy the person holds
- **THEN** the record carries the policy id as `selector` and the harness in `source.harness`

#### Scenario: Multi-party selection
- **WHEN** an intention with one counterparty is resolved
- **THEN** a commitment is created with the subject and the counterparty both at `tentative` and the resolution record references it

#### Scenario: Supply edit does not change the record's version
- **WHEN** a resolution record's `supply` list is corrected
- **THEN** its version is unchanged

#### Scenario: The presumption is on the record
- **WHEN** a placement is selected for an intention naming an untracked external party
- **THEN** the record's `presumed` names that party's URI and `supply` names only the availabilities that were actually used

#### Scenario: Adoption is recorded as a selection
- **WHEN** a person adopts an imported commitment for an intention
- **THEN** a resolution record is written with `selector: person`, `candidates_considered: 1`, the commitment's placement, and a `displaced` list that does not name that commitment
