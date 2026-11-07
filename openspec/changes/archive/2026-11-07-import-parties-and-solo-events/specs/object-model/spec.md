## MODIFIED Requirements

### Requirement: Workspace configuration

`intentions.yaml` SHALL declare `format`, `hash`, the resolver context default `resolver.timezone`, `resolver.horizon` (the planning horizon shared by resolution and instance generation; recommended `P4W`), `availability.default_horizon`, and `defaults.source.author`. It MAY declare `resolver.hemisphere` (`north` or `south`; absent means `north`), `resolver.step` (the candidate grid; absent means `PT15M`), `resolver.scope` (`personal`, `organisation`, or `public`; absent means `personal`), `defaults.subject`, and `calendar.addresses` (a map from a subject URI to a list of calendar addresses, such as `mailto:` URIs, that identify that particular in imported events; see Parties on import in Commitment); when `defaults.subject` is absent, every intention SHALL name its `subject` explicitly. `resolver.week_start` and `generation.horizon` SHALL NOT be declared. A reader finding an unknown key under `resolver` or `generation` SHALL ignore it and validation SHALL report it at info level.

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

#### Scenario: Calendar addresses
- **WHEN** `intentions.yaml` declares `calendar.addresses` mapping `https://example.org/people/ben` to `[mailto:ben@example.org, mailto:ben@work.example]`
- **THEN** an imported attendee at either address becomes a party with `uri: https://example.org/people/ben`, and no hash of any object depends on the key

### Requirement: Validation

A `validate` operation SHALL check the whole workspace and report findings with severity `error`, `warning`, or `info`. Errors SHALL include: dangling references, unknown reference roles, cycles in the intention serves graph, unparseable EDTF or ISO 8601 values, unknown retirement kinds, `superseded` without `superseded_by`, duplicate active instances for one occurrence, an intention or availability with no author, `firm` on an intention whose `source` carries a harness and which has no `firmed_under`, `firmed_under` naming anything other than an active, firm policy of the intention's subject, `firmed_under` on a terminus, `auto_select` or `auto_firm` on an intention that is not a terminus, `cadence` on an object whose window has no calendar anchor, `habit` on an intention without `cadence`, `habit` in a workspace whose `format` is `intentions/0.1` (named with `migrate` as the fix), a sub-day RRULE part in `cadence`, a fractional duration on an all-day placement, a DESIRE carrying any field of an intention's temporal or deontic kind (`duration`, `window`, `stability`, `parties`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, `acknowledgements`), a DESIRE `serves` entry with any role but `for-the-sake-of`, `adopted` without `adopted_as` or `adopted_as` naming anything but an intention, `superseded_by` on a desire naming anything but a desire, `fulfilled` on a terminus, `superseded_by` on a terminus naming anything but a terminus of its subject, `transparent` on a commitment born of a resolution, `external` on an intention with no `placement`, `external` on an intention with `parties`, two intentions carrying the same `external` `system` and `uid`, an imported commitment naming an intention whose `subject` is not one of its parties, an imported commitment naming an intention with `parties`, an imported commitment naming an intention that carries `external`, and two unretired commitments naming one intention. Under `intentions/0.2` errors SHALL also include an intention that reaches no firm terminus of its own subject, named with the fix; under `intentions/0.1` that finding is a warning. Warnings SHALL include an unretired intention with an `in-order-to` or `instance-of` link to an intention retired as `abandoned`, naming the abandoned end; and a RESOLUTION record whose `selector` names a policy that is no longer firm or no longer active, as an act authorised when it happened under a policy since withdrawn; the placement it produced stands and is the person's to keep or re-resolve; and an intention, retired or not, whose `external` `system` and `uid` match an unretired commitment's `external`, naming both and the two fixes: if the commitment is the intention's own hold imported before it was recognised, retire the commitment as `cancelled`; if it is a real event that shares the UID, clear the intention's `external`; and an unretired imported commitment naming an intention whose placement differs from its own, naming both, with adopting again as the fix. Info SHALL include a tentative terminus, as a draft; an unretired imported commitment whose only party is one particular and which names no intention and shares no `external` with an intention, as a commitment directed at no one that may be better recorded as an intention and adopted; and a workspace holding imported commitments whose `intentions.yaml` declares no `calendar.addresses`. Validation SHALL be runnable in continuous integration and SHALL exit non-zero on any error.

Where a write operation can determine that the result would fail validation with an error, it SHALL refuse the write. Where it can determine that the result would carry a warning, it SHALL accept the write and report the warning in its result. Write-time refusal is a convenience; validation is the invariant, because files may arrive by merge without passing through any write operation.

#### Scenario: Merge introduces error
- **WHEN** two branches each add one valid reference and the merged result contains a cycle
- **THEN** validation on the merged workspace reports the cycle as an error even though neither write was refused

#### Scenario: Unauthorised firming detected after the fact
- **WHEN** a merged intention carries `stability: firm`, a `source.harness`, and no `firmed_under`
- **THEN** validation reports an error naming the intention

#### Scenario: Workspace without termini under 0.1
- **WHEN** a workspace whose `format` is `intentions/0.1` holds intentions and no terminus
- **THEN** validation reports every non-terminus intention as unserved at warning level and exits zero

#### Scenario: Workspace without termini under 0.2
- **WHEN** a workspace whose `format` is `intentions/0.2` holds intentions and no terminus
- **THEN** validation reports every non-terminus intention as unserved at error level and exits non-zero

#### Scenario: Firmed under a draft
- **WHEN** an intention carries `firmed_under` naming a policy whose `stability` is `tentative`
- **THEN** validation reports an error naming the intention and the policy

#### Scenario: Selected under a policy since withdrawn
- **WHEN** a RESOLUTION record's `selector` names a policy that has since been set tentative or retired
- **THEN** validation reports a warning on the record and does not exit non-zero for it

#### Scenario: Habit on an instance
- **WHEN** a generated instance carries `habit: true`
- **THEN** validation reports an error naming the instance and the field

#### Scenario: Abandoned end
- **WHEN** an unretired intention serves `in-order-to` an intention retired as `abandoned`
- **THEN** validation reports a warning naming both and does not exit non-zero for it

#### Scenario: Habit in a 0.1 workspace
- **WHEN** a merged recurring intention in a workspace whose `format` is `intentions/0.1` carries `habit: true`
- **THEN** validation reports an error naming the intention, the field and `migrate`, and the intention's version is computed under the 0.1 projection, without `habit`

#### Scenario: Hold link on an intention with parties
- **WHEN** a merged intention with `parties` carries `external`
- **THEN** validation reports an error naming the intention and the commitment as the place for the link

#### Scenario: Hold imported before it was recognised
- **WHEN** an intention carries `external: {system: icalendar, uid: U}` and an unretired commitment with `origin: import` carries `external: {system: icalendar, uid: U}`
- **THEN** validation reports a warning naming the intention, the commitment and both fixes, and does not exit non-zero for it

#### Scenario: Cancelled duplicate is quiet
- **WHEN** the commitment sharing the intention's `external` is retired as `cancelled`
- **THEN** validation reports no warning for the pair

#### Scenario: Ticket directed at no one
- **WHEN** an unretired imported commitment's only party is the subject and it names no intention
- **THEN** validation reports it at info level, suggesting an intention that adopts it, and does not exit non-zero for it

#### Scenario: Two commitments for one intention
- **WHEN** a merged workspace holds two unretired commitments naming the same intention
- **THEN** validation reports an error naming both and the intention
