## MODIFIED Requirements

### Requirement: unresolved lists what still awaits a placement, and why
`unresolved` SHALL list every unretired intention that has no placement and could take one: not a terminus, not a recurring intention, and not a dormant instance of a habit. Each entry SHALL carry a status derived from a dry resolution: `ready` with the candidate count and best rank, `blocked` on a relational target without a placement, `no_candidates` with the resolver's reason, `incomplete` when duration or window is missing, or `unresolvable` when the serves graph or the object prevents resolution. It SHALL write nothing.

#### Scenario: A blocked intention
- **WHEN** an intention's window carries a relational anchor whose target has no placement
- **THEN** `unresolved` reports it as `blocked` and names the target

#### Scenario: Nothing carried
- **WHEN** every placeable intention has a placement
- **THEN** `unresolved` returns an empty list and a count of zero

#### Scenario: A habit asks nothing
- **WHEN** the only unplaced intentions in a workspace are instances of a recurring intention carrying `habit`
- **THEN** `unresolved` returns an empty list and a count of zero

## ADDED Requirements

### Requirement: intention_edit sets habit only by the person's act
`intention_edit` SHALL refuse a call that sets `habit` to true when its `source` carries a harness, whatever `policy` it names, and SHALL name the act as the person's. It SHALL accept a call that clears `habit` from any source.

#### Scenario: Harness habituates
- **WHEN** `intention_edit` is called with `source.harness` set and `habit: true` on a recurring intention
- **THEN** the call is refused and the intention is unchanged

#### Scenario: Harness reverts
- **WHEN** `intention_edit` is called with `source.harness` set and clears `habit`
- **THEN** the call is accepted and the intention's version changes
