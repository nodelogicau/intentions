## 1. Validate the change

- [x] 1.1 Run `openspec validate --changes`; confirm every MODIFIED header resolves against the main specs
- [x] 1.2 Confirm the subject exemption, the tracked-but-ineligible case, and the untracked-placement case each have a scenario that fails under the current rule

## 2. README

- [x] 2.1 INTENTION `parties` row: whose availability must be satisfied where the workspace tracks it
- [x] 2.2 Resolution lifecycle diagram: untracked parties contribute no supply and still contribute their placements
- [x] 2.3 Resolution prose: the tracking test, the subject exemption, unconstrained rather than satisfied, and the cliff stated as a consequence of supply being a positive assertion
- [x] 2.4 RESOLUTION record: add `presumed` to the example and the prose beside `supply`
- [x] 2.5 Consistency flag table: `window-clash` says two placements sharing a party whom both occupy
- [x] 2.6 AVAILABILITY or Design Principles: a line that a workspace does not write availability for a party to make a resolution succeed

## 3. Archive and close out

- [x] 3.1 Archive with sync so the three deltas land in the main specs
- [x] 3.2 Commit and push the intentions repo, one close keyword for #25
- [x] 3.3 Close #25 with a comment naming the commit, saying (a) was taken with the three refinements and why the reporting half of (b) was kept
- [x] 3.4 Knowledge workspace: claims for the tracking test and for untracked placements; one synthesis; open list carried forward; commit and push
