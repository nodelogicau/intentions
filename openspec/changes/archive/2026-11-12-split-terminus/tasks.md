## 1. Specs

- [x] 1.1 `openspec validate --changes --strict`: the deltas resolve against `intention`, `object-model` and `harness-tools`

## 2. README

- [x] 2.1 Serves-graph grounding paragraph: at a terminus superseded by a list, the walk continues at each successor and grounds if any does; the revisit rule applies per branch
- [x] 2.2 Terminus paragraph: a terminus may be superseded by several, recording that one self was refined into several. The refusal's alternative becomes "one or more termini, at least one firm". Deepening is recorded as supersession, with the earlier wording in `reason` or a DKF claim
- [x] 2.3 Records / RETIREMENT: the `superseded_by` rule (an id, or on a terminus a sorted list of two or more; never a one-element list) and a short split example
- [x] 2.4 Validation section: the list errors and the info finding for dependents resting on a split terminus
- [x] 2.5 Reference Tool Set: `intention_retire`'s `superseded_by?` row and bullet take an id or a list
- [x] 2.6 Status: readers of a shared workspace must be upgraded before anyone splits a terminus, alongside the `habit` and `external` notes

## 3. Close out

- [x] 3.1 Commit and push
- [x] 3.2 Open an issue on intentions-cli covering list parsing on a terminus's `superseded_by`, the branching walk, the new errors and info finding, a repeatable `--superseded-by` on `intention retire`, and the skill's "A reason changes by supersession" rule gaining the split case and asking the person which successor each dependent is for
- [x] 3.3 Archive with sync
