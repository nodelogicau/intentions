## MODIFIED Requirements

### Requirement: Placement is the collapse to clock time

A `placement` is a concrete `start` datetime with timezone, a DURATION, and an optional `location` (one absolute URI), and SHALL exist only on a resolved intention or a COMMITMENT. It is the single point where this specification touches clock time and fixed place, and it is written only as the result of a RESOLUTION or an import. When the intention or the supplying availability carries `location`, resolution SHALL set `placement.location` to one URI from their intersection; otherwise `placement.location` MAY be absent.

#### Scenario: Placement written by resolution
- **WHEN** a resolution is selected for an intention
- **THEN** the intention gains a `placement` and its `window` is preserved unchanged

#### Scenario: Placement location chosen
- **WHEN** an intention with `location: [home, office]` is resolved against availability with `location: [office]`
- **THEN** the placement carries `location: office` and the intention's `location` list is unchanged
