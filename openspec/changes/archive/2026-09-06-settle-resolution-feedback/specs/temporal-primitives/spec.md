## MODIFIED Requirements

### Requirement: Relational anchor uses RFC 9253 temporal relations

A WINDOW MAY carry a `relative` anchor with fields `target` (the id of another intention or commitment), `relation` (one of `FINISHTOSTART`, `FINISHTOFINISH`, `STARTTOFINISH`, `STARTTOSTART`, as defined in RFC 9253), and an optional `gap` with `min` and `max` ISO 8601 durations. The dependent WINDOW SHALL hold the reference; the target SHALL NOT be modified. This inverts RFC 9253's convention of placing the relation on the predecessor, to match the outbound-reference rule of the object model.

The relation SHALL bound the candidate as follows, where `min` defaults to `P0D` and an absent `max` means unbounded above: `FINISHTOSTART` puts the candidate's start in `[target end + min, target end + max]`; `STARTTOSTART` puts the candidate's start in `[target start + min, target start + max]`; `FINISHTOFINISH` puts the candidate's end in `[target end + min, target end + max]`; `STARTTOFINISH` puts the candidate's end in `[target start + min, target start + max]`.

A `relative` anchor whose target has no placement, or whose target is retired or cancelled, SHALL be treated as a constraint between two unresolved windows and SHALL NOT be reported as an error; resolution reports the dependent intention as blocked.

#### Scenario: After another intention
- **WHEN** a WINDOW is `relative: {target: int_A, relation: FINISHTOSTART, gap: {min: P0D, max: P3D}}`
- **THEN** resolution constrains the placement to start between zero and three days after intention A finishes

#### Scenario: Both anchors
- **WHEN** a WINDOW carries `calendar: 2026-09` and a `relative` anchor on int_A
- **THEN** resolution requires a placement satisfying both

#### Scenario: Unresolved target
- **WHEN** the target of a relative anchor has no placement
- **THEN** resolution reports the dependent intention as blocked on the target and does not place it

#### Scenario: Absent gap
- **WHEN** a WINDOW is `relative: {target: int_A, relation: STARTTOSTART}`
- **THEN** the candidate's start is at or after A's start with no upper bound

#### Scenario: Finish to finish
- **WHEN** a WINDOW is `relative: {target: int_A, relation: FINISHTOFINISH, gap: {max: P1D}}`
- **THEN** the candidate ends between A's end and one day after it

#### Scenario: Cancelled target blocks
- **WHEN** the target of a relative anchor is a commitment carrying `retired: {kind: cancelled, ...}`
- **THEN** resolution reports the dependent intention as blocked
