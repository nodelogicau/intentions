## 1. Specs

- [x] 1.1 `openspec validate hold-placed-intentions --strict`: the deltas resolve against `intention`, `commitment` and `object-model`
- [x] 1.2 Commitment Purpose (not a requirement, so outside the delta): replace "the only object that references an external calendar" with wording that keeps the commitment as the hand-off point for interchange and names an intention's hold link as the one other reference

## 2. README

- [x] 2.1 INTENTION field table: add `external` after `placement`, placed intentions with no `parties` only, pointing at the hold rules; projection note says `external` is not in it
- [x] 2.2 New Calendar hold paragraph under INTENTION: who may carry it, export shape (start and duration, location URI, title, always opaque, `STATUS` from stability, nothing else), import recognition, re-selection and retirement
- [x] 2.3 COMMITMENT section: the intro line ("the only one that touches an external calendar"), the `external` row ("The only link…"), and External reference only, so they speak for commitments and point at the intention's hold link
- [x] 2.4 The two diagrams showing `external.uid` on COMMITMENT alone: add the intention's hold link
- [x] 2.5 Versioning: an intention's `external` joins the excluded fields
- [x] 2.6 Validation: the three new errors (`external` without `placement`, with `parties`, duplicate `system` and `uid`)
- [x] 2.7 Status: upgrade every reader of a shared workspace before a harness writes holds, since an older importer would import a hold as a commitment
- [x] 2.8 Non-goals stated where the README discusses calendar interchange: iTIP replies stay the party's own act; availability is never written as busy time
- [x] 2.9 Reference tool set: `intention_edit` accepts `external?`, so a harness can record and clear a hold (found during apply; without it the field has no reference write path)

## 3. Close out

- [ ] 3.1 Commit and push
- [ ] 3.2 Open an intentions-cli issue: the field, the three validation errors, the write refusals, import recognition, hold export shape
- [ ] 3.3 Comment on and close issue #34 with a pointer to the change
- [ ] 3.4 Archive with sync
