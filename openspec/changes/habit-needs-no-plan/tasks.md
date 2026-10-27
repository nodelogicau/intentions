## 1. Specs

- [x] 1.1 Settle the format-version open question: lands within `intentions/0.2`
- [ ] 1.2 `openspec validate --changes`: the five MODIFIED and ADDED deltas resolve against `intention`, `resolution`, `consistency`, `harness-tools` and `object-model`

## 2. README

- [ ] 2.1 INTENTION fields table: `habit` after `cadence`, recurring-only, boolean default false
- [ ] 2.2 INTENTION projection: `habit` between `cadence` and `occurrence`
- [ ] 2.3 A short Habit subsection after recurrence: what habit means, that only the person sets it, that reverting is clearing it, dormant instances, that grounding still applies and is how a habit's withdrawn reason surfaces, and that a fixed-hour habit is reflected in availability, not reserved
- [ ] 2.4 Resolution preconditions: a dormant instance is refused
- [ ] 2.5 Consistency: `intention-inconsistency` doesn't count a dormant instance
- [ ] 2.6 Validation section: `habit` without `cadence`
- [ ] 2.7 Reference Tool Set: `unresolved` omits dormant instances; `intention_edit` refuses a harness setting `habit`

## 3. Close out

- [ ] 3.1 Commit and push
- [ ] 3.2 Open an issue on intentions-cli: the field and its order, the write-time refusal, `generate` skipping a habit, dormant instances in `resolve`, `unresolved` and `check`, and the skill's advice that a harness may suggest habituation but not set it
- [ ] 3.3 Comment on and close issue #30 with a pointer to the change
- [ ] 3.4 Archive with sync so the five deltas apply
