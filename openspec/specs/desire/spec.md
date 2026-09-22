# Desire

## Purpose

Defines DESIRE, the rung below intention: a want the person has expressed and not yet committed to. A desire is a world-to-mind pro-attitude, not a commissive act, so it is free to conflict with other desires, is never resolved, is checked against nothing, and is not grounded. It is where a passing remark goes until the person adopts it into an intention, which costs a why, or lets it go. Adoption writes the intention and retires the desire with a pointer to it.

## Requirements

### Requirement: DESIRE is the rung below intention
A DESIRE is a want the person has expressed and not yet committed to: a world-to-mind pro-attitude, not a commissive act. A workspace MAY hold desires in `/desires/`, one per file, with ids prefixed `des_`. A DESIRE SHALL carry, in canonical order: `id`; `version`; `subject` (the URI of the particular whose desire this is, applied from `defaults.subject` as for an intention); `title` (prose); `description` (prose, optional); `activity` (optional, a term from the workspace's activity vocabulary); `location` (optional, URIs); `serves` (possibly empty); `reference` (optional, an informal pointer to a DKF claim); `source`; `timestamp`; and `retired` when retired. A DESIRE SHALL NOT carry `duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, or `acknowledgements`, and validation SHALL report an error if it does. A DESIRE SHALL NOT carry a strength, priority, or ranking field.

#### Scenario: A passing remark
- **WHEN** a harness records "call the accountant" as a DESIRE with a title, the workspace's default subject, and an empty `serves`
- **THEN** the write is accepted and validation reports nothing about it

#### Scenario: A desire with a window
- **WHEN** a DESIRE file carries `window`
- **THEN** validation reports an error naming the field

### Requirement: A desire serves only a terminus, which may be a draft
`serves` on a DESIRE SHALL admit only entries whose `role` is `for-the-sake-of`, and each target SHALL be a terminus of the same `subject`. The terminus MAY be tentative: a desire is not grounded by it and nothing rests on either. An empty `serves` is valid; the grounding rule for intentions SHALL NOT apply to desires.

#### Scenario: Draft want, draft self
- **WHEN** a harness writes a tentative terminus and a DESIRE serving it `for-the-sake-of`
- **THEN** both writes are accepted, the terminus is reported as a draft, and the desire is not reported as unserved

#### Scenario: In-order-to on a desire
- **WHEN** a DESIRE's `serves` carries an entry with role `in-order-to`
- **THEN** the write is refused and validation reports an error

### Requirement: Desires are exempt from resolution, consistency, listing and grounding
Resolution SHALL NOT read desires. Consistency SHALL check nothing against a desire and SHALL report no flag on one. The `unresolved` listing SHALL NOT include desires. The requirement that every intention reaches a terminus SHALL NOT apply to desires. Two desires MAY conflict with each other in any way without any finding.

#### Scenario: Conflicting wants
- **WHEN** a person holds a desire to spend September writing and a desire to spend September travelling
- **THEN** validation and consistency report nothing

#### Scenario: Not in unresolved
- **WHEN** a workspace holds three desires and no unplaced intention
- **THEN** `unresolved` returns an empty list

### Requirement: Retirement kinds and adoption
A DESIRE SHALL be retired by the appended `retired` record with `kind` one of `abandoned`, `superseded`, or `adopted`. `superseded_by` SHALL be required when and only when `kind` is `superseded` and SHALL name a DESIRE. `adopted_as` SHALL be required when and only when `kind` is `adopted` and SHALL name an INTENTION; validation SHALL report an error if the target is absent or is not an intention. `retired.kind` SHALL be in the projection; `adopted_as`, `superseded_by`, `reason`, `timestamp` and `source` SHALL NOT.

#### Scenario: Adopted without pointer
- **WHEN** a DESIRE carries `retired: {kind: adopted}` with no `adopted_as`
- **THEN** validation reports an error

#### Scenario: Abandoned
- **WHEN** a person retires a desire with `kind: abandoned`
- **THEN** the file gains the record, is never edited again, and its version changes

### Requirement: Adoption writes the intention and then retires the desire
Adopting a DESIRE SHALL create a new INTENTION carrying the desire's `subject`, `title`, `description`, `serves`, `reference`, `activity` and `location`, the `duration` and `window` the adopting act supplies, `stability: tentative`, and the act's `source`; and SHALL then append `retired: {kind: adopted, adopted_as: <the new intention's id>}` to the desire. The intention is the record of the adoption; no other record SHALL be written. Adoption of a retired desire SHALL be refused. A harness MAY adopt, since adopting is drafting an intention. The new intention is subject to every rule an intention is subject to, including the grounding warning where its terminus is tentative.

#### Scenario: Harness adopts
- **WHEN** a harness adopts a desire supplying `duration: PT30M` and `window: {calendar: this-week}`
- **THEN** a tentative intention is written with the desire's title, serves, activity and location and the supplied duration and window, the desire is retired as `adopted` naming it, and the result carries both ids

#### Scenario: Adopting a draft-grounded want
- **WHEN** the adopted desire served a tentative terminus
- **THEN** the new intention is reported as unserved at warning level until the person firms the terminus

#### Scenario: Adopting twice
- **WHEN** adoption is attempted on a desire already carrying a `retired` record
- **THEN** the act is refused and nothing is written

### Requirement: Projection of a DESIRE
The scheduling projection of a DESIRE SHALL be `subject`, `serves`, and `retired.kind`. `title`, `description`, `activity`, `location`, `reference`, `source` and `timestamp` SHALL be excluded.

#### Scenario: Prose edit
- **WHEN** a desire's `description` is edited
- **THEN** its version is unchanged

#### Scenario: Terminus changed
- **WHEN** a desire's `serves` gains a `for-the-sake-of` entry
- **THEN** its version changes
