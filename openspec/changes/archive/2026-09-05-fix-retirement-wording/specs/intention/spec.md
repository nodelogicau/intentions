## MODIFIED Requirements

### Requirement: Reconsideration is triggered by conflict, not by sweep

Whether an existing intention should be reconsidered SHALL be surfaced when a new or changed intention conflicts with it (see Consistency), not by any background expiry mechanism. Intentions have no validity horizon.

#### Scenario: Conflict surfaces reconsideration
- **WHEN** a new firm intention cannot be placed without displacing an existing tentative one
- **THEN** the existing intention is surfaced for reconsideration in the resolution output and is neither retired nor re-placed automatically
