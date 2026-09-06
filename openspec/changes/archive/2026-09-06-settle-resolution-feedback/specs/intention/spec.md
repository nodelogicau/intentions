## MODIFIED Requirements

### Requirement: Recurring intentions and generated instances

An INTENTION carrying `cadence` is a recurring intention, and its window SHALL carry a calendar anchor for the cadence to expand within. Instances SHALL be new INTENTION objects, each carrying `serves: [{id: <recurring>, role: instance-of}]`, `occurrence` (the EDTF granule the cadence produced), a `window` whose `calendar` is that occurrence and whose `clock` is the recurring intention's `clock` when it has one, and the recurring intention's `subject`, `duration`, `activity`, `location`, and `parties` unless overridden. Each instance has its own stability, resolution lifecycle, and retirement. Recurrence SHALL NOT be an attribute of WINDOW. A recurring intention is not a terminus and SHALL NOT carry `auto_select` or `auto_firm`.

#### Scenario: Instance generation
- **WHEN** a recurring intention has `cadence: FREQ=WEEKLY;BYDAY=TU` and an instance is generated for week 2026-W37
- **THEN** a new intention is created with `occurrence: 2026-09-15`, `window.calendar: 2026-09-15`, the recurring intention's `subject`, and `serves: [{id: <recurring>, role: instance-of}]`

#### Scenario: Instance keeps place and hours
- **WHEN** a recurring intention has `window: {calendar: 2026-09/2026-12, clock: 09:00/12:00}` and `location: [home]`
- **THEN** each instance carries `window: {calendar: <occurrence>, clock: 09:00/12:00}` and `location: [home]`

#### Scenario: Skip one occurrence
- **WHEN** a generated instance is retired with `kind: abandoned`
- **THEN** the recurring intention is unchanged and later instances continue to generate

#### Scenario: End the arrangement
- **WHEN** a recurring intention is retired
- **THEN** no further instances are generated and existing active instances are unaffected until retired individually

#### Scenario: Recurring intention with a condition
- **WHEN** an intention with `cadence` is written with `auto_firm`
- **THEN** the write is refused and validation reports an error

### Requirement: Instance generation

Instances of a recurring intention SHALL be materialised by a `generate` operation over a horizon window, which resolution SHALL also run over its own horizon. Generated instances SHALL be written to disk immediately as INTENTION objects. Each instance SHALL carry `occurrence`, the EDTF granule the cadence produced, and generation SHALL be idempotent over that key: generating again over an overlapping horizon SHALL create no second active instance for the same recurring intention and occurrence, and validation SHALL report such a duplicate as an error. The horizon is `resolver.horizon` in `intentions.yaml`, the one planning horizon shared with resolution; the recommended default is four weeks (`P4W`). No background generation SHALL occur.

#### Scenario: Idempotent generation
- **WHEN** `generate` runs twice over horizons that both include 2026-09-15 for a weekly Tuesday recurring intention
- **THEN** exactly one active instance with `occurrence: 2026-09-15` exists

#### Scenario: Skipped then regenerated
- **WHEN** the instance for 2026-09-15 is retired as `abandoned` and `generate` runs again over that week
- **THEN** no new instance for 2026-09-15 is created

#### Scenario: Resolution generates
- **WHEN** resolution runs for an intention whose window lies in the next two weeks
- **THEN** instances of every recurring intention with occurrences within `resolver.horizon` exist on disk before candidates are ranked
