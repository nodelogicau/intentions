# Harness Tools

## Purpose

Defines the reference tool set through which a harness reaches an implementation: one tool per operation, named after the verb, with the standing DKF gives its names. The names are a reference and an implementation may use others; one that exposes a listed name keeps its semantics, so that a skill written against one implementation works against another. The four semantics stated here are where the format's rules (resolution ranks and never chooses, a harness may draft but not firm without a policy, a party's status is theirs alone) meet a tool call.

## Requirements

### Requirement: The reference tool set and its standing
The specification SHALL name a reference set of tools, one per operation, grouped by the object acted on and named after the verb: `intention_add`, `intention_edit`, `intention_firm`, `intention_retire`, `intention_show`, `intention_list`; `availability_add`, `availability_renew`, `availability_supersede`, `availability_retire`, `availability_list`; `commitment_accept`, `commitment_decline`, `commitment_cancel`, `commitment_show`, `commitment_list`; `generate`, `resolve`, `select`, `unresolved`, `check`, `acknowledge`, `bounds`, `validate`, `workspace_status`. These names are a reference, not a requirement: an implementation MAY expose its operations under other names. An implementation that exposes a listed name SHALL keep that tool's semantics and accept its parameters as the specification states them, so that a skill or prompt written against one implementation works against another.

#### Scenario: Names differ, nothing is bound
- **WHEN** an implementation exposes a tool called `add_intention` with different parameters
- **THEN** nothing in this capability applies to it

#### Scenario: A listed name is exposed
- **WHEN** an implementation exposes a tool called `select`
- **THEN** it SHALL behave as the `select` requirement below states, whatever else it does

### Requirement: Parameters are typed after the format's structures
Tool parameters SHALL use the format's own structures: a window is `{calendar, clock, relative: {target, relation, gap: {min, max}}}` with every part optional, a duration is an ISO 8601 string or `{nominal, min, max}`, `serves` is a list of `{id, role}`, `source` is `{author, harness, model}`, and identifiers are the prefixed ids the format defines. A tool's result SHALL be the same as the implementation's non-interactive output for the corresponding verb.

#### Scenario: A window passed to a tool
- **WHEN** `intention_add` receives `window: {calendar: "2026-W39", clock: "09:00/12:00"}`
- **THEN** the written object's `window` is exactly that, and the result equals what the verb would print with `--json`

### Requirement: select is the recorded act; resolve chooses nothing
`resolve` SHALL rank candidates and write nothing. `select` SHALL take exactly one of a person's `candidate` index or a harness's `policy` id, SHALL refuse a call carrying both or neither, and SHALL write the RESOLUTION record, the placement, and a commitment when parties are involved. A `policy` SHALL be honoured only where it names a terminus of the subject carrying `auto_select` whose condition the intention satisfies.

#### Scenario: Both given
- **WHEN** `select` is called with both `candidate` and `policy`
- **THEN** the call is refused as a usage error and nothing is written

#### Scenario: Policy not satisfied
- **WHEN** `select` is called with a `policy` whose `auto_select` condition the intention does not satisfy
- **THEN** the call is refused and nothing is written

### Requirement: intention_firm refuses a harness without a policy
`intention_firm` SHALL refuse a call whose `source` carries a harness unless `policy` names an active terminus of the subject carrying `auto_firm` whose condition the intention satisfies, and SHALL then write `firmed_under`. A call whose `source` carries no harness SHALL firm by the person's own act and leave `firmed_under` absent.

#### Scenario: Harness without policy
- **WHEN** `intention_firm` is called with `source.harness` set and no `policy`
- **THEN** the call is refused and the intention stays tentative

### Requirement: Party status tools take no policy
`commitment_accept` and `commitment_decline` SHALL take no `policy` parameter and SHALL set only the named party's own status. A party SHALL default to the workspace's subject; a workspace with no default subject SHALL require `party`. Nothing SHALL infer a status: the tools record what the person said.

#### Scenario: Declining as the subject
- **WHEN** `commitment_decline` is called with only `id` in a workspace with a default subject
- **THEN** the subject's own entry becomes `declined` and every other entry is unchanged

### Requirement: unresolved lists what still awaits a placement, and why
`unresolved` SHALL list every unretired intention that has no placement and could take one: not a terminus and not a recurring intention. Each entry SHALL carry a status derived from a dry resolution: `ready` with the candidate count and best rank, `blocked` on a relational target without a placement, `no_candidates` with the resolver's reason, `incomplete` when duration or window is missing, or `unresolvable` when the serves graph or the object prevents resolution. It SHALL write nothing.

#### Scenario: A blocked intention
- **WHEN** an intention's window carries a relational anchor whose target has no placement
- **THEN** `unresolved` reports it as `blocked` and names the target

#### Scenario: Nothing carried
- **WHEN** every placeable intention has a placement
- **THEN** `unresolved` returns an empty list and a count of zero
