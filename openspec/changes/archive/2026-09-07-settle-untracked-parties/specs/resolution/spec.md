## ADDED Requirements

### Requirement: A party the workspace does not track is unconstrained

A workspace tracks a party exactly when it holds at least one AVAILABILITY whose `subject` is that party's URI, whether or not that availability is retired, expired, or eligible. A party in an intention's `parties` that the workspace does not track SHALL contribute no supply constraint: resolution SHALL place against the subject's own supply and the supply of every tracked party, and SHALL NOT report no supply on that party's account. A party the workspace does track, whose eligible availability does not fit, SHALL still yield an empty candidate set naming that party.

The intention's `subject` SHALL NEVER be unconstrained by this rule, whatever their records, including where the subject also appears in `parties`.

An untracked party is unconstrained, not satisfied: the format presumes nothing about their capacity, and the commitment created from the placement carries them at `tentative` as any party would be, which is the state an invitation is sent from.

#### Scenario: External party has no records
- **WHEN** an intention lists `mailto:someone@another-company.example` in `parties` and the workspace holds no availability for that URI
- **THEN** candidates are computed from the subject's own supply and that party is not reported as having no supply

#### Scenario: Tracked party with nothing eligible
- **WHEN** an intention lists a party the workspace tracks, whose eligible availability does not overlap the window
- **THEN** resolution returns an empty candidate set naming that party

#### Scenario: A retired record still counts as tracked
- **WHEN** the only availability for a party carries a `retired` record
- **THEN** that party is tracked, contributes no eligible supply, and resolution reports no supply for them

#### Scenario: Subject with no records
- **WHEN** an intention's subject has no eligible availability for the window
- **THEN** resolution returns an empty candidate set naming the subject, whether or not the subject also appears in `parties`

### Requirement: An untracked party's placements still constrain

Every unretired placement in the workspace that names an untracked party, and that occupies them by their own party entry, SHALL constrain candidates for that party exactly as a tracked party's placements do. A candidate that would place a second commitment on an untracked party at an overlapping time SHALL be treated as displacing that commitment and ranked accordingly.

#### Scenario: No double-booking an external party
- **WHEN** a commitment already places an untracked party at an hour and a candidate for another intention would place the same party at an overlapping hour
- **THEN** the candidate is ranked as displacing that commitment rather than as displacing nothing

#### Scenario: Untracked room
- **WHEN** an intention lists a room the workspace holds no availability for, and another commitment already places that room at the same hour
- **THEN** the overlap is surfaced rather than ignored

#### Scenario: Declined untracked party frees the hour
- **WHEN** the untracked party's entry on the earlier commitment is `declined`
- **THEN** that commitment does not occupy them and a candidate at the same hour displaces nothing on their account

## MODIFIED Requirements

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields, in canonical order: `id`; `version`; `intention` (id); `placement`; `selector` (either `person` or the id of the policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces, sorted); `supply` (ids of the availabilities the placement was chosen against, sorted); `presumed` (URIs of the parties that contributed no supply because the workspace does not track them, sorted); `source`; and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection; `supply` records what the selector saw and is not what the placement rests on now, which consistency recomputes; `presumed` records whose time the placement assumes without evidence. On selection the intention gains the `placement`, including `location` where the intention or supply constrained it, and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`.

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
