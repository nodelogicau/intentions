## MODIFIED Requirements

### Requirement: The reference tool set and its standing
The specification SHALL name a reference set of tools, one per operation, grouped by the object acted on and named after the verb: `desire_add`, `desire_edit`, `desire_adopt`, `desire_retire`, `desire_show`, `desire_list`; `intention_add`, `intention_edit`, `intention_firm`, `intention_retire`, `intention_show`, `intention_list`; `availability_add`, `availability_renew`, `availability_supersede`, `availability_retire`, `availability_list`; `commitment_accept`, `commitment_decline`, `commitment_cancel`, `commitment_show`, `commitment_list`; `generate`, `resolve`, `select`, `unresolved`, `check`, `acknowledge`, `bounds`, `validate`, `workspace_status`. These names are a reference, not a requirement: an implementation MAY expose its operations under other names. An implementation that exposes a listed name SHALL keep that tool's semantics and accept its parameters as the specification states them, so that a skill or prompt written against one implementation works against another.

#### Scenario: Names differ, nothing is bound
- **WHEN** an implementation exposes a tool called `add_intention` with different parameters
- **THEN** nothing in this capability applies to it

#### Scenario: A listed name is exposed
- **WHEN** an implementation exposes a tool called `select`
- **THEN** it SHALL behave as the `select` requirement below states, whatever else it does

#### Scenario: desire_adopt is exposed
- **WHEN** an implementation exposes a tool called `desire_adopt`
- **THEN** it SHALL write the intention first and the desire's `adopted` retirement second, return both ids, refuse a desire already retired, and refuse a bare adoption, one whose desire serves nothing and which supplies neither `duration` nor `window`, naming what is missing

#### Scenario: desire_retire is exposed
- **WHEN** an implementation exposes a tool called `desire_retire`
- **THEN** it SHALL accept `abandoned` and `superseded` and SHALL refuse `adopted`
