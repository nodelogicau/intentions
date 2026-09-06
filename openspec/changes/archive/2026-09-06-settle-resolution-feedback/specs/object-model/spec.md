## MODIFIED Requirements

### Requirement: Workspace configuration

`intentions.yaml` SHALL declare `format`, `hash`, the resolver context default `resolver.timezone`, `resolver.horizon` (the planning horizon shared by resolution and instance generation; recommended `P4W`), `availability.default_horizon`, and `defaults.source.author`. It MAY declare `resolver.hemisphere` (`north` or `south`; absent means `north`), `resolver.step` (the candidate grid; absent means `PT15M`), `resolver.scope` (`personal`, `organisation`, or `public`; absent means `personal`), and `defaults.subject`; when `defaults.subject` is absent, every intention SHALL name its `subject` explicitly. `resolver.week_start` and `generation.horizon` SHALL NOT be declared. A reader finding an unknown key under `resolver` or `generation` SHALL ignore it and validation SHALL report it at info level.

#### Scenario: Minimal configuration
- **WHEN** a workspace is initialised for one person
- **THEN** `intentions.yaml` is written with `format`, `hash`, `resolver.timezone`, `resolver.horizon`, `availability.default_horizon`, `defaults.subject`, and `defaults.source.author` populated, and no `generation` section

#### Scenario: Default subject applied
- **WHEN** an intention is written without `subject` in a workspace whose `defaults.subject` is set
- **THEN** the file is written with `subject` equal to the workspace default

#### Scenario: Organisation workspace
- **WHEN** `defaults.subject` is absent and an intention is written without `subject`
- **THEN** the write is refused

#### Scenario: Southern hemisphere
- **WHEN** `intentions.yaml` declares `resolver.hemisphere: south`
- **THEN** a window of `2026-21` resolves to September through November 2026

#### Scenario: Stale keys
- **WHEN** an existing `intentions.yaml` still carries `resolver.week_start` or `generation.horizon`
- **THEN** they are ignored and validation reports them at info level

#### Scenario: Step and scope defaults
- **WHEN** `intentions.yaml` declares neither `resolver.step` nor `resolver.scope`
- **THEN** resolution uses a fifteen-minute grid and a `personal` scope ceiling
