## MODIFIED Requirements

### Requirement: Auto-selection only under a self-governing policy

Automatic selection SHALL be permitted only when a firm policy of the subject, that is a terminus carrying `auto_select` with a condition (for example `max_duration: PT30M`, `stability: tentative`), is satisfied by the intention. A tentative policy authorises nothing: selection under it SHALL be refused, naming the draft and the act that firms it. The resolution record SHALL then carry that policy's id as `selector`. No workspace-level or tool-level default SHALL auto-select.

#### Scenario: Policy authorises
- **WHEN** a policy declares `auto_select: {max_duration: PT30M}` and a fifteen-minute intention resolves with at least one rank-1 candidate
- **THEN** the top candidate is selected and the record carries the policy id

#### Scenario: Policy does not cover
- **WHEN** the same policy exists and a two-hour intention resolves
- **THEN** no selection occurs and the candidate set is returned for the person

#### Scenario: Policy is a draft
- **WHEN** a harness attempts to select under a policy whose `stability` is `tentative`, whatever its condition
- **THEN** the selection is refused and no record is written
