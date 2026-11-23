## MODIFIED Requirements

### Requirement: Intention fields

An INTENTION SHALL carry, in canonical order: `id`; `version`; `subject` (a URI identifying the particular, as Core Object Types defines it, whose intention this is; required on disk, applied from the workspace default when omitted by the caller); `title` (prose); optional `description` (prose); optional `duration`; optional `window`; `stability` (one of `tentative`, `firm`); optional `firmed_under` (the id of the policy under which a harness set `firm`); optional `activity`; optional `location` (a list of absolute URIs at one of which the intention must happen; absent means anywhere); optional `parties` (bare URIs of other required particulars, whose availability resolution must satisfy; a different shape from a commitment's `parties`, which carry a status); `serves` (a list of outbound references, possibly empty); optional `cadence`; optional `habit` (boolean, default false; recurring intentions only, see Habit); optional `occurrence` (on generated instances only); optional `placement`; optional `external` (`{system: icalendar|jscalendar, uid}`, the link to the calendar hold written for the placement; see Calendar hold); optional `preference` (see Resolution); optional `auto_select` and `auto_firm` (termini only); optional `reference` (an informal pointer to any record outside this format, as a URI or other string; never resolved); `source`; `timestamp`; `acknowledgements` (see Consistency); and at most one `retired` record.

The scheduling projection of an INTENTION SHALL be: `subject`, `duration`, `window`, `stability`, `activity`, `location`, `parties`, `serves`, `cadence`, `habit`, `occurrence`, `placement`, `retired.kind`. `version`, `firmed_under` and `external` are not in it. `habit` is in the projection only under `intentions/0.2`, which admitted it after files carried that string (see Versioning by projection hash in Object model). The `intentions/0.1` projection is the same list without `habit`.

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

#### Scenario: Hold link does not change the version
- **WHEN** a harness sets `external` on a placed intention with no `parties`
- **THEN** the file carries `external` immediately after `placement` and the intention's version is unchanged

### Requirement: Terminus

A terminus is an INTENTION with no `serves` entries, no `window`, and no `duration`: a practice the person holds ("following through") or a policy. A terminus MAY carry `reference` pointing informally at a record of what the person holds about the practice, such as a claim in a knowledge store; it is never resolved. A terminus SHALL NOT carry outbound `serves` references; validation SHALL report an error if an intention targeted by a `for-the-sake-of` reference has any `serves` entries. The word "standing intention", where used, means a terminus, never a recurring intention.

A terminus that is a practice SHOULD be titled as something the person chooses to keep doing, not as who they are and not as something that can be finished: "following through", not "being someone who follows through" and not "follow through on the board pack". The test is whether the title could ever be done. A terminus has no window and no duration and is never finished, so a title that could be finished names a task, and a title that names a property of the person names an identity rather than a choice. Validation SHALL NOT reject a terminus for its wording.

A terminus is the person's word. A terminus is inert until it is `firm`: it grounds nothing and authorises nothing. No policy applies to a terminus, so `firm` on a terminus SHALL come only from an act whose `source` carries no harness. A harness MAY write a terminus with `stability: tentative`; validation SHALL report a tentative terminus at info level as a draft, and it grounds no intention until the person firms it. A terminus grounds only intentions of its own `subject`.

#### Scenario: Chain closes on a terminus
- **WHEN** intention A serves B `in-order-to` and B serves T `for-the-sake-of`, and T has no `serves`
- **THEN** validation passes and T is reported as the terminus of A

#### Scenario: Terminus with outbound reference
- **WHEN** an intention targeted by `for-the-sake-of` itself carries a `serves` entry
- **THEN** validation reports an error on the terminus

#### Scenario: Terminus titled as a task
- **WHEN** a terminus is titled "follow through on the board pack" rather than "following through"
- **THEN** validation passes, and a conforming conventions file or skill MAY advise the practice form

#### Scenario: Terminus titled as an identity
- **WHEN** a terminus is titled "being someone who follows through" rather than "following through"
- **THEN** validation passes, and a conforming conventions file or skill MAY advise the practice form

#### Scenario: Harness drafts a terminus
- **WHEN** a write whose `source.harness` is set creates a terminus with `stability: tentative`
- **THEN** the write is accepted, validation reports the terminus as a draft at info level, and intentions reaching only it are unserved

#### Scenario: Harness firms a terminus under a policy
- **WHEN** a write whose `source.harness` is set attempts to firm a terminus citing a policy
- **THEN** the write is refused, because no policy applies to a terminus

#### Scenario: Person firms a terminus
- **WHEN** an act whose `source` carries no harness sets a terminus `firm`
- **THEN** the write is accepted and every intention reaching it is served
