# Resolution

## Purpose

Defines RESOLUTION, the operation that matches an intention's demand (duration, window, activity, required parties) against the availability of every required particular and produces an ordered set of candidate placements. Resolution is the moment a partial plan becomes definite and the one place this specification collapses a window to clock time.

Resolution never chooses on the person's behalf. Its output is a ranked candidate set; selecting one is a recorded act, by the person or by a self-governing policy the person authored.

## Requirements

### Requirement: Demand and supply

Resolution SHALL take one unretired intention with both `duration` and `window` as demand. Supply SHALL be the intersection of eligible availability whose `subject` equals the intention's `subject` and, for every URI in the intention's `parties`, eligible availability whose `subject` equals that URI. Availability is eligible only if it carries no `retired` record, its validity horizon has not passed, its `activities` (if any) include the intention's `activity`, its `location` (if any) shares a URI with the intention's `location` or the intention has none, and it is visible: `personal` availability only when its `subject` is the intention's `subject` or one of its `parties`, and `organisation` or `public` availability when its scope is at or wider than `resolver.scope`. Where the intention's window or a supplying availability's window carries a `clock` anchor, a candidate placement SHALL lie wholly within every such clock interval on the local day concerned. An occasion's remaining capacity is its offered `capacity` less the opaque, unretired placements already resting on it (see Availability); a candidate SHALL fit within the remaining capacity of every occasion it rests on.

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

#### Scenario: Clock bounds intersect
- **WHEN** an intention has `window: {calendar: 2026-W38, clock: 08:00/12:00}` and `duration: PT2H`, and the subject's availability for that week has `clock: 10:00/16:00`
- **THEN** every candidate starts at or after 10:00 and ends at or before 12:00 on a day of that week

#### Scenario: Clock bounds disjoint
- **WHEN** an intention has `clock: 18:00/21:00` and the subject's only availability for the window has `clock: 09:00/17:00`
- **THEN** resolution reports no supply for the subject

#### Scenario: Another person's personal availability is invisible
- **WHEN** an organisation workspace holds Priya's `personal` availability and Ada's intention does not list Priya in `parties`
- **THEN** Priya's availability is not supply for Ada's intention

#### Scenario: Capacity already consumed
- **WHEN** a three-hour occasion already has a two-hour opaque placement resting on it
- **THEN** a two-hour intention has no candidate on that occasion and a one-hour intention does

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

Where a rung names a commitment's status it means the resolving subject's own party entry, never another party's. A commitment that does not occupy the subject's time, because their entry is `declined` or because it is transparent, SHALL NOT be treated as displaced by any candidate and SHALL NOT raise a candidate's rank.

Within a rank, candidates SHALL be ordered by the intention's declared `preference` if present, otherwise by that of the nearest standing intention it is an instance of, otherwise by earliest start.

#### Scenario: Firm outranks tentative
- **WHEN** candidate X overlaps a tentative placed intention and candidate Y overlaps nothing
- **THEN** Y is ranked above X

#### Scenario: Declared preference breaks ties
- **WHEN** two candidates displace nothing and the intention declares `preference: latest`
- **THEN** the later candidate is ranked first

#### Scenario: The subject's own entry decides the rung
- **WHEN** a candidate overlaps a commitment on which the subject is `tentative` and a counterparty is `accepted`
- **THEN** the candidate is ranked as displacing a tentative commitment

#### Scenario: A declined commitment is not displaced
- **WHEN** a candidate overlaps an imported commitment the subject has declined and nothing else
- **THEN** the candidate is ranked as displacing nothing, and the commitment is not listed in `displaced`

### Requirement: Preference vocabulary

`preference` SHALL be one of `earliest`, `latest`, `adjacent` (next to an existing placement with the same `activity`), or `spread` (farthest from any placement with the same `activity`). Unknown values SHALL be a validation error.

#### Scenario: Adjacent
- **WHEN** an intention with `activity: deep-work` declares `preference: adjacent` and a deep-work placement exists on Tuesday morning
- **THEN** a candidate abutting it ranks above an isolated candidate of the same reconsideration cost

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields, in canonical order: `id`; `version`; `intention` (id); `placement`; `selector` (either `person` or the id of the policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces, sorted); `supply` (ids of the availabilities the placement was chosen against, sorted); `presumed` (URIs of the parties that contributed no supply because the workspace does not track them, sorted); `source`; and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection; `supply` records what the selector saw and is not what the placement rests on now, which consistency recomputes; `presumed` records whose time the placement assumes without evidence. On selection the intention gains the `placement`, including `location` where the intention or supply constrained it, and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`.

The scheduling projection of a RESOLUTION SHALL be: `intention`, `placement`, `selector`, `displaced`. Neither `supply` nor `presumed` is in it.

#### Scenario: Person selects
- **WHEN** a person selects the second candidate
- **THEN** a resolution record is written with `version` after `id`, `selector: person`, `source.author` set to that person, `supply` naming the availabilities used, the intention gains the placement, and the record lists anything displaced

#### Scenario: Harness selects under policy
- **WHEN** a harness auto-selects under a policy the person holds
- **THEN** the record carries the policy id as `selector` and the harness in `source.harness`

#### Scenario: Multi-party selection
- **WHEN** an intention with one counterparty is resolved
- **THEN** a commitment is created with the subject and the counterparty both at `tentative` and the resolution record references it

#### Scenario: Supply edit does not change the record's version
- **WHEN** a resolution record's `supply` list is corrected
- **THEN** its version is unchanged

#### Scenario: The presumption is on the record
- **WHEN** a placement is selected for an intention naming an untracked external party
- **THEN** the record's `presumed` names that party's URI and `supply` names only the availabilities that were actually used

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

### Requirement: Displaced objects are surfaced, never changed

When a selection displaces a tentative intention or commitment, the displaced object SHALL NOT be retired, re-placed, have its stability changed, or have any party status changed. It SHALL be listed in the resolution record and SHALL carry a `window-clash` flag until acknowledged or re-resolved.

#### Scenario: Displacement
- **WHEN** a selected placement overlaps a tentative placed intention
- **THEN** that intention keeps its placement and stability and a window-clash flag is reported on both

### Requirement: Transparent commitments are never displaced

A candidate placement that overlaps a commitment with `transparent: true` SHALL NOT be treated as displacing it: the overlap SHALL NOT raise the candidate's reconsideration cost, the commitment SHALL NOT be listed in the resolution record's `displaced`, and no flag SHALL result from the overlap.

#### Scenario: Overlap with a transparent commitment is free
- **WHEN** candidate X overlaps an accepted commitment with `transparent: true` and candidate Y overlaps nothing
- **THEN** X and Y have the same reconsideration cost and are ordered by preference or earliest start

#### Scenario: Not recorded as displaced
- **WHEN** a selected placement overlaps a transparent commitment
- **THEN** the resolution record's `displaced` list does not include it

### Requirement: Resolution is a function of workspace, configuration, and now

Given the workspace, `intentions.yaml`, and a `now` instant, the candidate set and its order SHALL be fully determined; two conformant implementations SHALL produce the same ranked set. `now` SHALL be taken from the clock unless overridden on the call.

#### Scenario: Two resolvers agree
- **WHEN** two implementations resolve the same intention against the same workspace with the same `now`
- **THEN** they produce the same candidates in the same order

### Requirement: Resolution range

Candidates SHALL lie within a range whose start is the later of the window's computed start and `now`, and whose end is the earlier of the window's computed end and `now` plus `resolver.horizon`. An open side of the window contributes nothing to the range. A window that has entirely passed, or that starts beyond the horizon, SHALL yield no candidates and a reason. A candidate starting before `now` SHALL never be offered.

#### Scenario: Deadline window
- **WHEN** an intention has `window.calendar: ../2026-12`, `now` is 2026-09-06, and `resolver.horizon` is `P4W`
- **THEN** candidates lie between 2026-09-06 and 2026-10-04

#### Scenario: Window has passed
- **WHEN** an intention's window ended before `now`
- **THEN** resolution returns no candidates and reports the window as past

#### Scenario: Window beyond horizon
- **WHEN** an intention's window starts after `now` plus `resolver.horizon`
- **THEN** resolution returns no candidates and reports the window as beyond the horizon

### Requirement: Candidate grid

Candidate starts SHALL lie on a grid of `resolver.step` (default `PT15M`) aligned to the start of each supply interval, and each candidate SHALL span the intention's nominal duration. When the duration is ranged and the nominal yields no candidate, resolution SHALL try successively shorter durations on the grid, down to `min`, and offer the longest that yields any. The full ranked set SHALL be computed; `candidates_considered` records its size, and a caller MAY limit what it displays.

#### Scenario: Grid aligned to supply
- **WHEN** a supply interval starts at 09:10 and `resolver.step` is `PT15M`
- **THEN** candidate starts are 09:10, 09:25, 09:40, and so on within the interval

#### Scenario: Ranged duration falls back
- **WHEN** an intention has `duration: {nominal: PT2H, min: PT1H, max: PT2H}` and the only supply interval is ninety minutes long
- **THEN** resolution offers ninety-minute candidates and none at two hours

#### Scenario: Determinism
- **WHEN** resolution runs twice on an unchanged workspace with the same `now`
- **THEN** the candidate sets are identical

### Requirement: Re-selection replaces the placement

Selecting a candidate for an intention that already has a placement SHALL be refused unless the caller explicitly asks to replace. A replacing selection SHALL clear the previous placement and write the new one in the same act, and SHALL create a new RESOLUTION record; the previous record SHALL be left unchanged. If a live commitment rests on the previous placement, the replacing selection SHALL cancel it with the new resolution's id as `reason` and create a fresh commitment with every party at `tentative`, because a placement its parties accepted cannot change under them.

#### Scenario: Replace refused by default
- **WHEN** a selection is attempted for a placed intention without asking to replace
- **THEN** the write is refused and the existing placement is unchanged

#### Scenario: Replace
- **WHEN** a replacing selection is made for a placed intention with no commitment
- **THEN** the intention carries the new placement, a second RESOLUTION record exists, and the first is unchanged

#### Scenario: Replace with a live commitment
- **WHEN** a replacing selection is made for an intention whose commitment has one party at `accepted`
- **THEN** that commitment gains `retired: {kind: cancelled, reason: <new resolution id>, ...}` and a new commitment exists with every party at `tentative`

### Requirement: A party the workspace does not track is unconstrained

A workspace tracks a party exactly when it holds at least one AVAILABILITY whose `subject` is that party's URI, whether or not that availability is retired, expired, or eligible. A party in an intention's `parties` that the workspace does not track SHALL contribute no supply constraint: resolution SHALL place against the subject's own supply and the supply of every tracked party, and SHALL NOT report no supply on that party's account. A party the workspace does track, whose eligible availability does not fit, SHALL still yield an empty candidate set naming that party.

The intention's `subject` SHALL NEVER be unconstrained by this rule, whatever their records, including where the subject also appears in `parties`.

An untracked party is unconstrained, not satisfied: the format presumes nothing about their capacity, and the commitment created from the placement carries them at `tentative` as any party would be, which is the state an invitation is sent from.

#### Scenario: External party has no records
- **WHEN** an intention lists `mailto:someone@another-company.example` in `parties` and the workspace holds no availability for that URI
- **THEN** candidates are computed from the subject's own supply and that party is not reported as having no supply

#### Scenario: Tracked party with nothing eligible
- **WHEN** an intention lists a party the workspace tracks, whose eligible availability does not overlap the window
- **THEN** resolution returns an empty candidate set naming that party

#### Scenario: A retired record still counts as tracked
- **WHEN** the only availability for a party carries a `retired` record
- **THEN** that party is tracked, contributes no eligible supply, and resolution reports no supply for them

#### Scenario: Subject with no records
- **WHEN** an intention's subject has no eligible availability for the window
- **THEN** resolution returns an empty candidate set naming the subject, whether or not the subject also appears in `parties`

### Requirement: An untracked party's placements still constrain

Every unretired placement in the workspace that names an untracked party, and that occupies them by their own party entry, SHALL constrain candidates for that party exactly as a tracked party's placements do. A candidate that would place a second commitment on an untracked party at an overlapping time SHALL be treated as displacing that commitment and ranked accordingly.

#### Scenario: No double-booking an external party
- **WHEN** a commitment already places an untracked party at an hour and a candidate for another intention would place the same party at an overlapping hour
- **THEN** the candidate is ranked as displacing that commitment rather than as displacing nothing

#### Scenario: Untracked room
- **WHEN** an intention lists a room the workspace holds no availability for, and another commitment already places that room at the same hour
- **THEN** the overlap is surfaced rather than ignored

#### Scenario: Declined untracked party frees the hour
- **WHEN** the untracked party's entry on the earlier commitment is `declined`
- **THEN** that commitment does not occupy them and a candidate at the same hour displaces nothing on their account
