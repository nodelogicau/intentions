## MODIFIED Requirements

### Requirement: Composition with DKF by reference only

This specification SHALL NOT depend on any DKF object, schema, or tool to exist or validate. A DKF claim MAY cite any object in this specification by id, optionally with a projection hash, exactly as a DKF claim cites an external document. Objects in this specification MAY carry an informal `reference` (a URI or DKF id) pointing at a DKF claim, with no resolvability contract. Live prospective state SHALL never be represented as DKF claims.

#### Scenario: Terminus points at a claim the person holds
- **WHEN** an intention's terminus carries `reference: clm_...`
- **THEN** validation does not attempt to resolve it and does not report it if the target is absent
