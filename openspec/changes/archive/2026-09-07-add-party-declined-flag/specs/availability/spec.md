## MODIFIED Requirements

### Requirement: Capacity is consumed per occasion

Each occasion of an availability SHALL offer its `duration` (the `max` when ranged). The opaque, unretired placements resting on an occasion SHALL consume it: a candidate SHALL fit within the offered duration less what is already resting there. A commitment SHALL consume the capacity of a party only where that party's own entry is `tentative` or `accepted`; a party at `declined` SHALL have none of their capacity consumed by it. An intention's placement and the commitment created from it SHALL count once against the subject's capacity, and that placement consumes it whatever the subject's party entry says. Transparent commitments consume nothing.

#### Scenario: Two into three
- **WHEN** a three-hour Tuesday-morning occasion already holds a two-hour placement
- **THEN** a second two-hour intention has no candidate there and a one-hour one does

#### Scenario: Commitment does not double-count
- **WHEN** a one-hour intention is placed on an occasion and a commitment is created from it
- **THEN** the occasion's remaining capacity is reduced by one hour, not two

#### Scenario: Transparent import does not consume
- **WHEN** an imported commitment with `transparent: true` overlaps an occasion
- **THEN** the occasion's remaining capacity is unchanged

#### Scenario: Declined import does not consume
- **WHEN** the subject declines an imported one-hour commitment resting on a three-hour occasion
- **THEN** the occasion's remaining capacity returns to three hours for them

#### Scenario: Declining does not free a placed intention's hour
- **WHEN** the subject declines a commitment created from their own intention, which is still placed
- **THEN** the occasion's remaining capacity is unchanged, because the intention's placement consumes it
