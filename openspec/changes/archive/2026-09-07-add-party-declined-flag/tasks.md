## 1. Validate the change

- [x] 1.1 Run `openspec validate --changes`; confirm every MODIFIED header resolves against the main specs
- [x] 1.2 Confirm the flag fires for a resolution-born commitment and not for an import, and that no scenario has a flag changing state

## 2. README

- [x] 2.1 COMMITMENT party-status paragraph: a status decides occupancy per party; a decline frees that party alone; the subject's decline frees nothing while the placement stands
- [x] 2.2 AVAILABILITY capacity paragraph: a commitment consumes a party's capacity only where that party is tentative or accepted
- [x] 2.3 Consistency flag table: add the `party-declined` row
- [x] 2.4 Consistency prose: a paragraph on the two origins, why an import raises nothing, and what the person does about the flag
- [x] 2.5 Resolution lifecycle diagram and ranking: the rungs read the subject's own entry, and a declined commitment is not displaced

## 3. Archive and close out

- [x] 3.1 Archive with sync so the four deltas land in the main specs
- [x] 3.2 Commit and push the intentions repo, one close keyword for #24
- [x] 3.3 Close #24 with a comment naming the commit and saying the answer is (a) refined per party, plus the flag, and how that differs from what v0.8.0 shipped
- [x] 3.4 Knowledge workspace: claims for per-party occupancy and the flag; one synthesis; open list carried forward; commit and push
