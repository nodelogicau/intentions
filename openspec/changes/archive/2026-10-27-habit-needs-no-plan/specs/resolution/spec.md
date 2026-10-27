## MODIFIED Requirements

### Requirement: Preconditions

Resolution SHALL refuse an intention that lacks `duration` or `window`, is retired, carries a `cycle` flag, has a relative anchor whose target is unplaced, or is a dormant instance of a habit (see Intention). It SHALL report the reason.

#### Scenario: Blocked on anchor
- **WHEN** an intention's window is relative to an unplaced intention
- **THEN** resolution reports it as blocked and places nothing

#### Scenario: Dormant instance
- **WHEN** resolution is asked for an unplaced instance whose recurring intention carries `habit`
- **THEN** resolution refuses it, reporting that the recurring intention is held as habit, and places nothing
