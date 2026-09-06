## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Demand and supply

Resolution SHALL take one unretired intention with both `duration` and `window` as demand. Supply SHALL be the intersection of eligible availability whose `subject` equals the intention's `subject` and, for every URI in the intention's `parties`, eligible availability whose `subject` equals that URI. Availability is eligible only if it carries no `retired` record, its validity horizon has not passed, its `conditional` (if any) includes the intention's `activity`, its `location` (if any) shares a URI with the intention's `location` or the intention has none, and it is visible: `personal` availability only when its `subject` is the intention's `subject` or one of its `parties`, and `organisation` or `public` availability when its scope is at or wider than `resolver.scope`. Where the intention's window or a supplying availability's window carries a `clock` anchor, a candidate placement SHALL lie wholly within every such clock interval on the local day concerned. An occasion's remaining capacity is its offered duration less the opaque, unretired placements already resting on it (see Availability); a candidate SHALL fit within the remaining capacity of every occasion it rests on.

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
- **WHEN** an organisation workspace holds Rob's `personal` availability and Ada's intention does not list Rob in `parties`
- **THEN** Rob's availability is not supply for Ada's intention

#### Scenario: Capacity already consumed
- **WHEN** a three-hour occasion already has a two-hour opaque placement resting on it
- **THEN** a two-hour intention has no candidate on that occasion and a one-hour intention does

### Requirement: Selection is a recorded act

Resolution SHALL NOT write a placement by itself. Selecting a candidate SHALL create a RESOLUTION record with fields, in canonical order: `id`; `version`; `intention` (id); `placement`; `selector` (either `person` or the id of the policy that authorised auto-selection); `candidates_considered` (count); `displaced` (ids of intentions or commitments the placement displaces, sorted); `supply` (ids of the availabilities the placement was chosen against, sorted); `source`; and `timestamp`. `selector` records whose will chose; `source` records which hand performed the selection; `supply` records what the selector saw and is not what the placement rests on now, which consistency recomputes. On selection the intention gains the `placement`, including `location` where the intention or supply constrained it, and, if it has `parties`, a COMMITMENT is created with status `tentative` for every party, including the intention's `subject`.

The scheduling projection of a RESOLUTION SHALL be: `intention`, `placement`, `selector`, `displaced`. `supply` is not in it.

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
