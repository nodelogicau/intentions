## MODIFIED Requirements

### Requirement: Intention fields

An INTENTION SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); optional `firmed_under` (the id of the policy under which a harness set `firm`); optional `activity`; optional `location` (a list of absolute URIs at one of which the intention must happen; absent means anywhere); optional `parties` (bare URIs of other required particulars, whose availability resolution must satisfy; a different shape from a commitment's `parties`, which carry a status); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `habit` (boolean, default false; recurring intentions only, see Habit); optional `occurrence` (on generated instances only); optional `placement`; optional `preference` (see Resolution); optional `auto_select` and `auto_firm` (termini only); optional `reference` (informal pointer to a DKF claim); `source`; `timestamp`; `acknowledgements` (see Consistency); and at most one `retired` record.

The scheduling projection of an INTENTION SHALL be: `subject`, `duration`, `window`, `stability`, `activity`, `location`, `parties`, `serves`, `cadence`, `habit`, `occurrence`, `placement`, `retired.kind`. `version` and `firmed_under` are not in it.

#### Scenario: Minimal intention
- **WHEN** an intention is written with only `title` and `stability: tentative` in a workspace with default `subject` and `source.author`
- **THEN** it is valid, the file carries `version` after `id`, the default `subject`, `source.author`, and a `timestamp`, it carries no window or duration, and it cannot be resolved until it has both

#### Scenario: Subject without default
- **WHEN** an intention is written without `subject` in a workspace with no `defaults.subject`
- **THEN** the write is refused

#### Scenario: Own supply is by subject
- **WHEN** an intention with `subject: https://example.org/people/ben` is resolved
- **THEN** its own supply is the eligible availability whose `subject` is that URI

#### Scenario: Habit changes the version
- **WHEN** the person sets `habit: true` on a recurring intention
- **THEN** the file carries `habit` immediately after `cadence` and the intention's version changes

### Requirement: Instance generation

Instances of a recurring intention SHALL be materialised by a `generate` operation over a horizon window, which resolution SHALL also run over its own horizon. Generated instances SHALL be written to disk immediately as INTENTION objects. Each instance SHALL carry `occurrence`, the EDTF granule the cadence produced, and generation SHALL be idempotent over that key: generating again over an overlapping horizon SHALL create no second active instance for the same recurring intention and occurrence, and validation SHALL report such a duplicate as an error. `generate` SHALL create no instance for a recurring intention carrying `habit`. The horizon is `resolver.horizon` in `intentions.yaml`, the one planning horizon shared with resolution; the recommended default is four weeks (`P4W`). No background generation SHALL occur.

#### Scenario: Idempotent generation
- **WHEN** `generate` runs twice over horizons that both include 2026-09-15 for a weekly Tuesday recurring intention
- **THEN** exactly one active instance with `occurrence: 2026-09-15` exists

#### Scenario: Skipped then regenerated
- **WHEN** the instance for 2026-09-15 is retired as `abandoned` and `generate` runs again over that week
- **THEN** no new instance for 2026-09-15 is created

#### Scenario: Resolution generates
- **WHEN** resolution runs for an intention whose window lies in the next two weeks
- **THEN** instances of every recurring intention with occurrences within `resolver.horizon` exist on disk before candidates are ranked

#### Scenario: A habit generates nothing
- **WHEN** `generate` runs over a horizon containing occurrences of a recurring intention carrying `habit`
- **THEN** no instance is created for it

## ADDED Requirements

### Requirement: Habit

A recurring intention MAY carry `habit: true`, meaning the person holds it as habit: its context cues it and it needs no plan. `habit` SHALL be admitted only on an intention carrying `cadence`. A write that sets `habit` to true SHALL be refused when its `source` carries a harness, and no policy SHALL authorise it. A write that clears `habit` MAY carry a harness. Because `source` records the last write, whether the person set `habit` is checked at write time only.

Habit SHALL change nothing about the intention's own standing. It stays unretired, keeps its `stability`, and remains subject to the grounding rule. Its `serves` chain is walked like any other.

An instance is *dormant* when it is unplaced and unretired and its `instance-of` target carries `habit`. Habituation SHALL write nothing to existing instances. A dormant instance is refused by resolution (see Resolution), omitted by `unresolved` (see Harness tools), and not counted by `intention-inconsistency` (see Consistency). A placed instance of a habit is not dormant. Clearing `habit` ends dormancy, and `generate` resumes over the horizon.

#### Scenario: The person habituates
- **WHEN** a write whose `source` carries no harness sets `habit: true` on a recurring intention
- **THEN** the write is accepted, no instance is created, retired or edited, and the recurring intention stays active

#### Scenario: A harness habituates
- **WHEN** a write whose `source.harness` is set sets `habit: true` on a recurring intention
- **THEN** the write is refused, naming the act as the person's

#### Scenario: Habit on a one-off
- **WHEN** an intention without `cadence` carries `habit: true`
- **THEN** validation reports an error naming the field

#### Scenario: Dormant instances
- **WHEN** a recurring intention with three unplaced instances and one placed instance in the horizon is habituated
- **THEN** the three unplaced instances are dormant and the placed instance keeps its placement and is checked as before

#### Scenario: Revert
- **WHEN** a harness clears `habit` on a recurring intention whose unplaced instances were dormant
- **THEN** the write is accepted, those instances are no longer dormant, and the next `generate` creates instances for occurrences in the horizon that have none

#### Scenario: A habit outlives its reason
- **WHEN** the firm terminus a habit serves `for-the-sake-of` is set tentative by the person
- **THEN** validation reports the habit as unserved at the format's level for unserved intentions, naming it and the fix
