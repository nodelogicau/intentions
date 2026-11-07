## 1. Specs

- [x] 1.1 `openspec validate import-parties-and-solo-events --strict`: the deltas resolve against `commitment`, `resolution`, `consistency` and `object-model`
- [x] 1.2 Commitment Purpose (not a requirement, so outside the delta): keep "directed at someone" as what a commitment is for, and add that an import may bring one directed at no one, which validation names
- [x] 1.3 Consistency Flag kinds scenario "Kinds are exhaustive" still holds (no new flag kind); confirm nothing else in Consistency implies a commitment clashes with its own intention

## 2. README

- [x] 2.1 COMMITMENT field table: `intention` is set by resolution or by adopting, no longer "absent on imports"
- [x] 2.2 Two origins: parties are mapped by rule; import never names an intention
- [x] 2.3 New paragraph, Parties on import: which entries become parties, URI and `calendar.addresses`, the status table, the subject's entry in the three cases, re-import
- [x] 2.4 External reference only: address and participation status cross, nothing else of attendee metadata
- [x] 2.5 New paragraph, Adopting an imported commitment: the concert example, a selection with `selector: person`, preconditions, the moved-event warning, cancellation
- [x] 2.6 Consistency: a commitment and the intention it fulfils are one occupation
- [x] 2.7 Workspace configuration: `calendar.addresses`
- [x] 2.8 Validation: the four errors, the moved-event warning, the two info findings
- [x] 2.9 Status: re-import may move versions of commitments an earlier importer mapped differently; upgrade every reader before adopting
- [x] 2.10 Reference tool set: an adopt operation (commitment id, intention id), and `calendar.addresses` wherever configuration is shown

## 3. Close out

- [x] 3.1 Commit and push
- [x] 3.2 Open an intentions-cli issue: mapping and `calendar.addresses`, adopt, one-occupation counting, the six findings
- [x] 3.3 Comment on and close issue #35 with a pointer to the change
- [x] 3.4 Archive with sync
