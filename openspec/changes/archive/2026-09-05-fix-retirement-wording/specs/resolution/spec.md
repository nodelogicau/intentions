## MODIFIED Requirements

### Requirement: Displaced objects are surfaced, never changed

When a selection displaces a tentative intention or commitment, the displaced object SHALL NOT be retired, re-placed, have its stability changed, or have any party status changed. It SHALL be listed in the resolution record and SHALL carry a `window-clash` flag until acknowledged or re-resolved.

#### Scenario: Displacement
- **WHEN** a selected placement overlaps a tentative placed intention
- **THEN** that intention keeps its placement and stability and a window-clash flag is reported on both
