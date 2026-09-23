## MODIFIED Requirements

### Requirement: Activity vocabulary

`activity` on an intention and each term in `activities` on an availability SHALL be a lowercase kebab-case term. The specification SHALL NOT fix the vocabulary; terms are documented in the workspace conventions file. Matching between `activity` and `activities` SHALL be by exact string equality. An unknown term SHALL NOT be a validation error; validation SHALL report at info level any term used by exactly one object.

#### Scenario: Unknown term accepted
- **WHEN** an intention carries `activity: piano-practice` and no other object uses that term
- **THEN** validation passes and reports the term at info level

#### Scenario: Malformed term
- **WHEN** an intention carries `activity: Deep Work`
- **THEN** the write is refused and validation reports an error

### Requirement: Every intention reaches a terminus
An intention that is not a terminus SHALL reach a firm terminus of its own `subject` through its `serves` graph, by any path of `in-order-to`, `for-the-sake-of` and `instance-of` references. Reachability is the test, not the presence of an entry: a chain that ends on a scheduled intention, or on a tentative terminus, is unserved. Generated instances reach a terminus through the recurring intention they are `instance-of`. Under `intentions/0.1` validation reports an unserved intention at warning level, naming the intention and the fix, and a write that would leave an intention unserved is accepted and carries the same finding in its result. Under `intentions/0.2` validation SHALL report an unserved intention as an error, naming the intention and the fix, and a write that would leave an intention unserved SHALL be refused. A 0.2 reader applies the 0.1 rule to a workspace whose `format` is still `intentions/0.1`.

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
