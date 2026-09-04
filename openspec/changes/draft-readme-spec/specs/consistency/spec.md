## MODIFIED Requirements

### Requirement: Acknowledgements are stored

An ACKNOWLEDGEMENT SHALL be an entry in the `acknowledgements` list of the intention or commitment it concerns, with fields `kind`, `counterpart` (id, or absent where the flag has none), `counterpart_version`, `reason` (prose), `timestamp`, and `source`. The list SHALL be append-only. Acknowledgements are excluded from the scheduling projection.

#### Scenario: Acknowledge a clash
- **WHEN** a person acknowledges the window-clash between cmt_X and int_Y with a reason
- **THEN** an acknowledgement is appended to cmt_X recording kind, counterpart int_Y, int_Y's current version, the reason, the time, and the person as `source.author`

#### Scenario: Acknowledgement on a retired object
- **WHEN** an acknowledgement is appended to an intention that carries a `retired` record
- **THEN** the append is accepted and no other field of the intention changes

### Requirement: Consistency never changes state

A consistency check SHALL NOT retire any object, nor change any object's stability, placement, or party status. Its only outputs are flags.

#### Scenario: Inconsistent intentions
- **WHEN** two firm intentions cannot both be placed
- **THEN** both carry an `intention-inconsistency` flag and neither gains a `retired` record
