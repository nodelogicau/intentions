## MODIFIED Requirements

### Requirement: Multiple subjects per workspace

A workspace MAY hold objects for several subjects, and validation SHALL NOT require that every object share one subject. Reading another workspace's objects (federation) is deferred from this version: scope visibility is defined within one workspace, and a resolver has no supply for a party whose availability is held elsewhere. A party the workspace holds no availability for at all is untracked rather than unavailable, and resolution treats them as unconstrained (see Resolution); a workspace SHALL NOT write an availability for a party in order to make a resolution succeed, because an availability is an assertion about that particular's capacity and inventing one records a fact nobody asserted.

#### Scenario: Room in a personal workspace
- **WHEN** a personal workspace holds an availability whose `subject` is a room URI
- **THEN** it is valid and resolution uses it for intentions listing that room in `parties`

#### Scenario: Party held elsewhere
- **WHEN** an intention lists a party for which no availability exists in this workspace
- **THEN** that party is untracked, contributes no supply constraint, and resolution places against the tracked parties' supply

#### Scenario: No manufactured supply
- **WHEN** a harness cannot place an intention naming an external party
- **THEN** it reports what stands in the way and does not write an availability whose subject is that party
