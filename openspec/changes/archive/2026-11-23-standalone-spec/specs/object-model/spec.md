## MODIFIED Requirements

### Requirement: Composition with DKF by reference only

This specification SHALL NOT depend on any DKF object, schema, or tool to exist or validate. Any record outside this format, a DKF claim among them, MAY cite an object here by id, optionally with its version; nothing here changes when it does. Objects in this specification MAY carry an informal `reference` (a URI or other string) pointing at any record outside this format, with no resolvability contract. This specification SHALL state no requirement on how DKF or any other format is written or used.

#### Scenario: Terminus points at a claim the person holds
- **WHEN** an intention's terminus carries `reference: clm_...`
- **THEN** validation does not attempt to resolve it and does not report it if the target is absent

#### Scenario: A reference that is a URI
- **WHEN** a desire carries `reference: https://example.com/notes/why-i-run`
- **THEN** validation does not attempt to resolve it and does not report it
