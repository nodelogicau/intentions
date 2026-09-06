## MODIFIED Requirements

### Requirement: Flag kinds

A flag SHALL have exactly one `kind` from: `window-clash` (a placement overlaps another placement or falls in a window with no eligible supply), `condition-mismatch` (the availability supplying a placement has a conditional that does not include the intention's activity), `location-mismatch` (the availability supplying a placement has a location list that does not include the placement's location, or the placement's location is not in the intention's location list), `expired-ground` (an availability the placement rests on has passed its horizon or been retired), `intention-inconsistency` (two active unplaced intentions of one subject, each with duration and window and with intersecting resolution ranges, each have candidates alone but no pair of non-overlapping candidates exists; the check is pairwise and never global), `party-declined` (a commitment has a party at `declined` while the intention it fulfils is still placed), and `cycle` (the intention is in a strongly-connected component of the serves graph). Flags SHALL NOT carry a numeric severity.

#### Scenario: Kinds are exhaustive
- **WHEN** a consistency check finds a problem
- **THEN** it is reported under exactly one of the seven kinds

#### Scenario: Imported meeting elsewhere
- **WHEN** an imported commitment carries `placement.location: office` and the subject's availability for that window carries `location: [home]`
- **THEN** the commitment carries a `location-mismatch` flag and its party statuses are unchanged

#### Scenario: Pairwise inconsistency
- **WHEN** two unplaced intentions of one subject each fit the subject's single three-hour occasion alone but not together
- **THEN** both carry an `intention-inconsistency` flag naming the other, with `detail` saying the check is pairwise

#### Scenario: Three-way infeasibility not reported
- **WHEN** three unplaced intentions each fit an occasion in pairs but not all three together
- **THEN** no `intention-inconsistency` flag is reported

## ADDED Requirements

### Requirement: A decline against a standing plan is flagged

A `party-declined` flag SHALL be reported when a commitment has any party at `declined` and the intention it fulfils still carries a placement. It SHALL be reported on both the commitment and that intention, each naming the other as counterpart, and its `detail` SHALL name the declining party and whether that party is the intention's subject. A commitment with no `intention`, which is every imported commitment, SHALL NOT raise it, because there is no plan for the decline to disagree with. A commitment whose intention's placement has been cleared SHALL NOT raise it.

The flag SHALL NOT change any party status, clear any placement, or retire anything. It is acknowledgeable like any other flag, and because a party status is in the commitment's projection, a later change to it lapses the acknowledgement and the flag is recomputed.

#### Scenario: Subject declines their own arrangement
- **WHEN** the subject sets their own party entry to `declined` on a commitment created from their placed intention
- **THEN** a `party-declined` flag is reported on the commitment and on the intention, the placement is unchanged, and the detail says the declining party is the subject

#### Scenario: Counterparty declines
- **WHEN** a counterparty declines a commitment whose intention is still placed
- **THEN** the same flag is reported on both objects and the detail names that party as not the subject

#### Scenario: Imported commitment declined
- **WHEN** the subject declines an imported commitment, which has no `intention`
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
