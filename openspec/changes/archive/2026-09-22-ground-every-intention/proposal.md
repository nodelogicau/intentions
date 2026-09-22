## Why

An intention with no chain is admitted, placed, firmed and committed without anyone having said what it is for, and nothing reports it (nodelogicau/intentions #26). The Design Principles now argue that the chain up to a terminus is what makes an intention resist reconsideration, and the only normative trace of that argument is a SHOULD on how a terminus is titled. DKF settles the same question at its root: a claim cannot exist without a particular, because the particular is what the claim is about, and `claim_assert` refuses one without it. A terminus grounds an intention in exactly that sense, what it is ultimately for, the self it is a claim about. An intention with no terminus is a duration floating free. The first implementation has asked the format to settle this rather than diverge on the one rule that decides what the format is for.

## What Changes

- **Every intention reaches a terminus.** An intention that is not a terminus SHALL reach a terminus of its own subject through its `serves` graph, by any path of `in-order-to`, `for-the-sake-of` and `instance-of`. Reachability, not presence: an `in-order-to` chain ending on a scheduled intention is unserved all the way down. In this revision an unserved intention is a validation **warning**, and a write that would produce one is accepted and warns; the next revision that breaks files raises both to refusal, as DKF refuses a claim with no particular.
- **A terminus is the person's word.** A terminus SHALL be `firm`, and no policy applies to a terminus, so only the person's own act firms one. A harness may draft a terminus, tentative, as it drafts anything. A terminus that is not firm grounds nothing: intentions reaching only a tentative terminus are unserved until the person firms it. This is the issue's softer form built from rules the spec already has, and it keeps a terminus writable over MCP, where every write carries a harness.
- **The terminus is the subject's own.** An intention reaching another subject's self-understanding is a category error; an organisation workspace holds termini per subject.
- **The principle, stated.** A Design Principles paragraph, "The why is the price of entry", beside "A terminus is a person, not a task": a workspace's first act is a terminus, a harness's first question is who the person is trying to be, and the format does not hold an intention the person cannot say the point of.
- The site's example workspace gains the chain its one-to-one lacks, and the CLI is asked to implement the check and to walk an existing workspace up to its termini.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: a new requirement that every intention reaches a terminus; the Terminus requirement gains firmness, the person's word, and the subject match; the Policies requirement excludes termini from policy conditions.
- `object-model`: Validation gains the unserved warning and the write-time warning rule for this revision.
- `harness-tools`: `intention_firm` refuses a policy on a terminus.

## Impact

- README: the serves-graph paragraph, the Policies paragraph, the Validation section, the Design Principles, the Status paragraph's transition note, and the Reference Tool Set bullet for `intention_firm`. Three spec deltas.
- Every existing workspace written without termini goes to warning on every intention. The maintainer's personal workspace has forty-six active intentions and no terminus; the site's example has one unserved intention of four. The transition is explicit: warning now, a skill that walks a workspace up to its termini, refusal later.
- `docs/example`: the one-to-one gains a `for-the-sake-of` reference; the proof figure is regenerated and its candidate set is unchanged, since `serves` is outside the scheduling projection.
- intentions-cli: one issue for the check, the terminus rules, and the walk-up skill.
- Knowledge workspace: claims and a synthesis on the spine after archive.
