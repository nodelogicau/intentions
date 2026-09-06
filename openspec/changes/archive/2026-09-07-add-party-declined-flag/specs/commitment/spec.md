## MODIFIED Requirements

### Requirement: Party status is set only by that party's explicit act

A party's `status` SHALL change only through an explicit act attributed to that party: a local action by the workspace owner for their own entry, or an imported iTIP reply for another party. No resolution, consistency check, flag, or policy SHALL change a party status.

A status is also what decides whether the commitment occupies that party's time. A commitment SHALL occupy a party's time, consuming their capacity and standing to be displaced by their resolutions, exactly where that party's own entry is `tentative` or `accepted`. A party at `declined` SHALL NOT be occupied by it. This is per party: one party's decline SHALL NOT change what the commitment occupies for any other party, whose commitment still stands. Where the commitment fulfils an intention, that intention's placement occupies its subject's time on its own, so a decline by the subject frees nothing while the placement stands and is reported as a `party-declined` flag (see Consistency).

#### Scenario: Flag does not decline
- **WHEN** a consistency check finds a commitment clashing with a firm intention
- **THEN** the commitment's party statuses are unchanged and a flag is reported

#### Scenario: Owner accepts
- **WHEN** the workspace owner accepts a tentative commitment
- **THEN** their party entry becomes `accepted` and the version changes

#### Scenario: Decline frees the decliner only
- **WHEN** a counterparty declines a commitment
- **THEN** that hour no longer consumes their capacity, and it still consumes the capacity of every party at `tentative` or `accepted`

#### Scenario: Declining an import frees the hour
- **WHEN** the subject declines an imported commitment
- **THEN** the hour no longer consumes their capacity and no later candidate is ranked as displacing it
