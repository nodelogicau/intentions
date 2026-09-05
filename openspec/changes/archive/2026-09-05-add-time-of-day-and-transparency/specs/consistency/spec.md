## ADDED Requirements

### Requirement: Transparent commitments occupy no time and rest on no supply

A commitment with `transparent: true` SHALL NOT be the subject or the counterpart of a `window-clash` flag, because it occupies none of the subject's time, and SHALL NOT be the subject of a `condition-mismatch`, `location-mismatch`, or `expired-ground` flag, because it rests on no availability. A transparent commitment SHALL NOT count as eligible supply for anything and SHALL NOT remove supply from anything. Its party statuses, acknowledgements, and retirement behave as for any commitment.

#### Scenario: Conference week does not clash
- **WHEN** an imported commitment with `transparent: true` spans 21 to 25 September and a firm intention is placed on 23 September
- **THEN** no `window-clash` is reported on either object

#### Scenario: Transparent import outside availability
- **WHEN** an imported commitment with `transparent: true` falls in a window where the subject has no eligible availability
- **THEN** no `window-clash` and no `expired-ground` is reported on it

#### Scenario: Opaque import still clashes
- **WHEN** an imported commitment with no `transparent` field overlaps a placed intention
- **THEN** a `window-clash` is reported on both
