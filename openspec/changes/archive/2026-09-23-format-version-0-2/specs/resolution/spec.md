## MODIFIED Requirements

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
