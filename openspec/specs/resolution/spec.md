# Resolution

## Purpose

Defines RESOLUTION, the operation that matches an intention's demand (duration, window, activity, required parties) against the availability of every required particular and produces an ordered set of candidate placements. Resolution is the moment a partial plan becomes definite and the one place this specification collapses a window to clock time.

Resolution never chooses on the person's behalf. Its output is a ranked candidate set; selecting one is a recorded act, by the person or by a self-governing policy the person authored.

## Requirements

### Requirement: Demand and supply

Resolution SHALL take one unretired, unplaced intention with both `duration` and `window` as demand. Supply SHALL be the intersection of eligible availability whose `subject` equals the intention's `subject` and, for every URI in the intention's `parties`, eligible availability whose `subject` equals that URI. Availability is eligible only if it carries no `retired` record, its validity horizon has not passed, its `conditional` (if any) includes the intention's `activity`, its `location` (if any) shares a URI with the intention's `location` or the intention has none, and its scope is visible to the resolver.

#### Scenario: Multi-party intersection
- **WHEN** an intention lists a counterparty and a room in `parties`
- **THEN** candidates are placements inside the intersection of the subject's, the counterparty's, and the room's eligible availability

#### Scenario: No supply
- **WHEN** no eligible availability overlaps the intention's window for every required party
- **THEN** resolution returns an empty candidate set and names which party had no supply

#### Scenario: Location excludes supply
- **WHEN** an intention requires `location: [home]` and the subject's only availability for the window carries `location: [office]`
- **THEN** resolution reports no supply for the subject

#### Scenario: Retired availability ignored
- **WHEN** the only availability matching the intention's subject carries a `retired` record
- **THEN** resolution reports no supply for the subject

### Requirement: Preconditions

Resolution SHALL refuse an intention that lacks `duration` or `window`, is retired, carries a `cycle` flag, or has a relative anchor whose target is unplaced. It SHALL report the reason.

#### Scenario: Blocked on anchor
- **WHEN** an intention's window is relative to an unplaced intention
- **THEN** resolution reports it as blocked and places nothing

### Requirement: Candidate ranking by reconsideration cost

Candidates SHALL be ordered first by reconsideration cost, from lowest to highest:

1. Displaces no existing placed firm intention and no accepted commitment.
2. Displaces only tentative placed intentions or tentative commitments.
3. Requires retiring a firm intention or cancelling an accepted commitment.

Within a rank, candidates SHALL be ordered by the intention's declared `preference` if present, otherwise by that of the nearest standing intention it is an instance of, otherwise by earliest start.

#### Scenario: Firm outranks tentative
- **WHEN** candidate X overlaps a tentative placed intention and candidate Y overlaps nothing
- **THEN** Y is ranked above X

#### Scenario: Declared preference breaks ties
- **WHEN** two candidates displace nothing and the intention declares `preference: latest`
- **THEN** the later candidate is ranked first

### Requirement: Preference vocabulary

`preference` SHALL be one of `earliest`, `latest`, `adjacent` (next to an existing placement with the same `activity`), or `spread` (farthest from any placement with the same `activity`). Unknown values SHALL be a validation error.

#### Scenario: Adjacent
- **WHEN** an intention with `activity: deep-work` declares `preference: adjacent` and a deep-work placement exists on Tuesday morning
- **THEN** a candidate abutting it ranks above an isolated candidate of the same reconsideration cost

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields: `id`; `source`; `intention` (id); `placement`; `selector` (either `person` or the id of the self-governing policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces); and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection. On selection the intention gains the `placement`, including `location` where the intention or supply constrained it, and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`.

The scheduling projection of a RESOLUTION SHALL be: `intention`, `placement`, `selector`, `displaced`.

#### Scenario: Person selects
- **WHEN** a person selects the second candidate
- **THEN** a resolution record is written with `selector: person`, `source.author` set to that person, the intention gains the placement, and the record lists anything displaced

#### Scenario: Harness selects under policy
- **WHEN** a harness auto-selects under a policy the person holds
- **THEN** the record carries the policy id as `selector` and the harness in `source.harness`

#### Scenario: Multi-party selection
- **WHEN** an intention with one counterparty is resolved
- **THEN** a commitment is created with the subject and the counterparty both at `tentative` and the resolution record references it

### Requirement: Auto-selection only under a self-governing policy

Automatic selection SHALL be permitted only when a standing intention (a terminus or policy) carries `auto_select` with a condition (for example `max_duration: PT30M`, `stability: tentative`) that the intention satisfies. The resolution record SHALL then carry that policy's id as `selector`. No workspace-level or tool-level default SHALL auto-select.

#### Scenario: Policy authorises
- **WHEN** a policy declares `auto_select: {max_duration: PT30M}` and a fifteen-minute intention resolves with at least one rank-1 candidate
- **THEN** the top candidate is selected and the record carries the policy id

#### Scenario: Policy does not cover
- **WHEN** the same policy exists and a two-hour intention resolves
- **THEN** no selection occurs and the candidate set is returned for the person

### Requirement: Displaced objects are surfaced, never changed

When a selection displaces a tentative intention or commitment, the displaced object SHALL NOT be retired, re-placed, or have its status changed. It SHALL be listed in the resolution record and SHALL carry a `window-clash` flag until acknowledged or re-resolved.

#### Scenario: Displacement
- **WHEN** a selected placement overlaps a tentative placed intention
- **THEN** that intention keeps its placement and status and a window-clash flag is reported on both
