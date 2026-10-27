## Why

A recurring intention practised long enough becomes habit. Its context cues it, not the plan, and the plan is no longer needed for it to happen (issue #30, after the forgetting whitepaper, sections 7 and 8). The format can't say that. Keeping the intention active means `generate` keeps writing instances, and `unresolved` keeps asking the person when to do something they no longer decide about. That is the deliberation the format exists to relieve. Retiring the intention misdescribes it: nothing was fulfilled, abandoned or superseded. Retirement also takes the habit out of the grounding check, and the grounding check is what notices a habit that has outlived its reason.

## What Changes

- **A recurring intention may be held as habit.** A new boolean field, `habit`, sits on the live object after `cadence`. It is admitted only on an intention carrying `cadence`, and it is in the scheduling projection.
- **Only the person's own act sets it.** A write that sets `habit` is refused when its `source` carries a harness. No policy authorises it: `auto_firm` and `auto_select` don't reach it, and no new condition is added. A harness may suggest habituation. Clearing the field to revert may be done by anyone, because reverting only brings the plan back into view, as a harness setting an intention tentative does.
- **A habit has no plan.** `generate` creates no instances for it. Instances that already exist are left on disk untouched. While their recurring intention is a habit, each unplaced instance is dormant: resolution refuses it, `unresolved` omits it, and consistency doesn't count it toward `intention-inconsistency`. Placed instances keep their placements and behave as before until the person retires them. Reverting brings the dormant instances straight back, and `generate` resumes over the horizon.
- **A habit stays a live reason.** It's active, so the grounding rule applies to it unchanged. When the person sets the terminus it serves tentative, the habit is reported unserved. That is the format's way of noticing a habit that has outlived its reason.
- **A habit reserves no time.** If it occupies a fixed hour, the person's AVAILABILITY says so by no longer offering that hour. Reserving capacity from a habit's window is left out of this change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: `habit` joins the fields and the projection. A new requirement defines habit: recurring-only, set by the person's act, reverted by clearing, with dormant instances and grounding unchanged. Instance generation skips a habit.
- `resolution`: the preconditions refuse a dormant instance.
- `consistency`: `intention-inconsistency` doesn't count a dormant instance.
- `harness-tools`: `unresolved` omits dormant instances, and `intention_edit` refuses a harness that sets `habit`.
- `object-model`: validation reports `habit` on an intention without `cadence` as an error.

## Impact

- README: under INTENTION, the fields table, the projection, a short habit subsection after recurrence, and the validation list. The reference tool set gains a bullet on `intention_edit` and `habit`.
- Five deltas, no new capability.
- Lands within `intentions/0.2`, which is unreleased. `habit` joins the 0.2 projection, and the README's Versioning section records it alongside the 0.1 precedent. No existing hash changes.
- intentions-cli: the field, the refusal, `generate` skipping, and dormant instances in `resolve`, `unresolved` and `check`. The skill should say that a harness may suggest habituation after a run of fulfilled instances, but must not set it.
- Issue #30: closed by this change, with a pointer.
