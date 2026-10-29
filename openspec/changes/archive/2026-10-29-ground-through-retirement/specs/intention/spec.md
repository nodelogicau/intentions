## MODIFIED Requirements

### Requirement: Every intention reaches a terminus
An intention that is not a terminus SHALL reach a firm terminus of its own `subject` through its `serves` graph, by any path of `in-order-to`, `for-the-sake-of` and `instance-of` references. Reachability is the test, not the presence of an entry: a chain that ends on a scheduled intention, or on a tentative terminus, is unserved. Generated instances reach a terminus through the recurring intention they are `instance-of`.

The walk SHALL pass through retired intentions. At a link whose target is retired as `superseded`, the walk SHALL continue at the target's `superseded_by`. At a link whose target is retired as any other kind, the walk SHALL continue through the target's own `serves`. A terminus SHALL ground the walk only when it is firm and unretired, so a retired terminus grounds nothing, while a superseded terminus grounds through its successor. A walk that reaches an intention it has already visited through `superseded_by` SHALL end there without grounding.

An unretired intention with an `in-order-to` or `instance-of` link to an intention retired as `abandoned` SHALL be reported at warning level, naming the intention and the abandoned end. A link to an intention retired as `fulfilled` SHALL raise no finding.

Under `intentions/0.1` validation reports an unserved intention at warning level, naming the intention and the fix, and a write that would leave the intention it writes unserved is accepted and carries the same finding in its result. Under `intentions/0.2` validation SHALL report an unserved intention as an error, naming the intention and the fix, and a write that would leave the intention it writes unserved SHALL be refused. This refusal SHALL cover only the intention being written. A write to a terminus that leaves its dependents unserved, such as setting it tentative, is not refused by it, and retiring a terminus is governed by Retiring a terminus. A 0.2 reader applies the 0.1 rule to a workspace whose `format` is still `intentions/0.1`.

#### Scenario: Chain ends on a scheduled intention
- **WHEN** A serves B `in-order-to`, B has a window and a duration, and B has no `serves`
- **THEN** validation reports A and B as unserved at warning level

#### Scenario: Chain ends on a tentative terminus
- **WHEN** A serves T `for-the-sake-of`, T has no window, duration or serves, and T is `tentative`
- **THEN** validation reports A as unserved and T as a draft terminus

#### Scenario: Instance reaches through the recurring intention
- **WHEN** an instance carries only `instance-of` to a recurring intention that serves a firm terminus
- **THEN** the instance is served and validation reports nothing

#### Scenario: Another subject's terminus
- **WHEN** Ada's intention serves Priya's terminus `for-the-sake-of` and no terminus of Ada's
- **THEN** validation reports Ada's intention as unserved

#### Scenario: Unserved write under 0.1
- **WHEN** a harness adds an intention with an empty `serves` in a workspace whose `format` is `intentions/0.1` and which holds no terminus
- **THEN** the write is accepted and the result carries the unserved warning naming the intention

#### Scenario: Unserved write under 0.2
- **WHEN** a harness adds an intention with an empty `serves` in a workspace whose `format` is `intentions/0.2` and which holds no terminus
- **THEN** the write is refused, naming the intention and the fix

#### Scenario: Ended arrangement
- **WHEN** a recurring intention serving a firm terminus is retired as `abandoned` and two of its instances are still unretired
- **THEN** both instances are served through it, and each carries a warning naming the abandoned recurring intention

#### Scenario: Fulfilled end
- **WHEN** A serves B `in-order-to`, B serves a firm terminus, and B is retired as `fulfilled` while A is unretired
- **THEN** A is served and validation reports nothing about it

#### Scenario: Superseded reason
- **WHEN** A serves terminus T `for-the-sake-of`, and T is retired as `superseded` with `superseded_by` naming a firm terminus U of the same subject
- **THEN** A is served through U and validation reports nothing about it

#### Scenario: Withdrawal is accepted
- **WHEN** in a workspace whose `format` is `intentions/0.2` the person sets tentative the only firm terminus that A reaches
- **THEN** the write is accepted, and validation reports A as unserved at error level

### Requirement: Retirement kinds

An intention's `retired.kind` SHALL be one of `fulfilled` (discharged, a positive terminal state), `abandoned` (no longer held, no replacement), or `superseded` (replaced by a specific other intention, in which case `superseded_by` SHALL carry that intention's id). A terminus SHALL admit `abandoned` and `superseded` only, since a self-understanding is never discharged, and its `superseded_by` SHALL name a terminus of the same `subject`. Each kind is final; a retired intention SHALL NOT be edited further except to append acknowledgements.

#### Scenario: Superseded
- **WHEN** an intention is retired with `retired: {kind: superseded, superseded_by: int_C, ...}`
- **THEN** validation requires int_C to exist and reports an error if it does not

#### Scenario: Superseded without target
- **WHEN** an intention is retired with `kind: superseded` and no `superseded_by`
- **THEN** the write is refused

#### Scenario: Fulfilled with reason
- **WHEN** an intention is retired with `kind: fulfilled` and a `reason`
- **THEN** the record carries the reason, a timestamp, and the source of the retiring act, and the intention's version changes

#### Scenario: Fulfilled terminus
- **WHEN** a terminus carries `retired: {kind: fulfilled}`
- **THEN** validation reports an error, and a retirement act naming that kind on a terminus is refused

#### Scenario: Terminus superseded by a scheduled intention
- **WHEN** a terminus is retired as `superseded` with `superseded_by` naming an intention that has a window
- **THEN** the write is refused and validation reports an error

## ADDED Requirements

### Requirement: Retiring a terminus
Retiring a terminus SHALL be refused when some unretired intention that reaches a firm terminus before the act would reach none after it, computed by the walk in Every intention reaches a terminus. The refusal SHALL name those intentions and the alternatives: set the terminus tentative to withdraw it, or supersede it with a firm terminus to replace it. An intention with another firm ground, the dependents of a tentative terminus, desires serving the terminus, and intentions carrying `firmed_under` naming it SHALL NOT block the act. This refusal SHALL apply under `intentions/0.1` and `intentions/0.2` alike.

A firm terminus SHALL be retired only by an act whose `source` carries no harness. A tentative terminus MAY be retired by an act whose `source` carries a harness only when the terminus's own `source` carries a harness.

#### Scenario: Sole ground
- **WHEN** the person retires as `abandoned` the only firm terminus that an unretired intention A reaches
- **THEN** the act is refused, naming A and the alternatives

#### Scenario: Another ground remains
- **WHEN** A serves firm termini T and U `for-the-sake-of`, and the person retires T as `abandoned`
- **THEN** the act is accepted and A is served through U

#### Scenario: Nothing rests on it
- **WHEN** the person retires a firm terminus that no unretired intention reaches
- **THEN** the act is accepted

#### Scenario: Superseded by a firm terminus
- **WHEN** the person retires the sole ground of A as `superseded` with `superseded_by` naming a firm terminus of the same subject
- **THEN** the act is accepted and A is served through the successor

#### Scenario: Superseded by a draft
- **WHEN** the person retires the sole ground of A as `superseded` with `superseded_by` naming a tentative terminus
- **THEN** the act is refused, naming A

#### Scenario: Harness withdraws its draft
- **WHEN** a harness retires a tentative terminus whose `source` carries a harness
- **THEN** the act is accepted

#### Scenario: Harness retires a firm terminus
- **WHEN** an act whose `source` carries a harness retires a firm terminus
- **THEN** the act is refused, naming the act as the person's
