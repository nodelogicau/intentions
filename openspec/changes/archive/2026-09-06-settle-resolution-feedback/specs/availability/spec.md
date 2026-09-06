## MODIFIED Requirements

### Requirement: Scope

`scope` SHALL default to `personal`. `personal` availability SHALL be visible to a resolver only when the availability's `subject` is the intention's `subject` or one of its `parties`. `organisation` and `public` availability SHALL be visible to a resolver whose `resolver.scope` is at or narrower than the availability's scope, where `personal` is narrowest and `public` widest. Scope SHALL only ever be widened.

#### Scenario: Shared availability
- **WHEN** a person sets an availability's scope to `organisation`
- **THEN** a resolver acting for another party in the organisation may use it as supply

#### Scenario: Personal stays personal
- **WHEN** an organisation workspace holds Rob's `personal` availability and Ada resolves an intention that does not involve Rob
- **THEN** it is not visible as supply

#### Scenario: Party's personal availability
- **WHEN** Ada's intention lists Rob in `parties` and Rob's availability is `personal`
- **THEN** it is visible as Rob's supply for that intention

## ADDED Requirements

### Requirement: Capacity is consumed per occasion

Each occasion of an availability SHALL offer its `duration` (the `max` when ranged). The opaque, unretired placements resting on an occasion SHALL consume it: a candidate SHALL fit within the offered duration less what is already resting there. An intention's placement and the commitment created from it SHALL count once. Transparent commitments consume nothing.

#### Scenario: Two into three
- **WHEN** a three-hour Tuesday-morning occasion already holds a two-hour placement
- **THEN** a second two-hour intention has no candidate there and a one-hour one does

#### Scenario: Commitment does not double-count
- **WHEN** a one-hour intention is placed on an occasion and a commitment is created from it
- **THEN** the occasion's remaining capacity is reduced by one hour, not two

#### Scenario: Transparent import does not consume
- **WHEN** an imported commitment with `transparent: true` overlaps an occasion
- **THEN** the occasion's remaining capacity is unchanged
