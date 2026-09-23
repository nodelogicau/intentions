## 1. Declare v0.1

- [x] 1.1 Tag `v0.1` at `54c9a83` and push the tag; confirm it is the last commit whose projections the CLI implements

## 2. Specs

- [x] 2.1 `openspec validate --changes`: the ADDED requirement and every MODIFIED header resolve

## 3. README

- [x] 3.1 `intentions.yaml`: `format: intentions/0.2`; the Format name paragraph wherever the string appears
- [x] 3.2 Versioning: replace the "last moment such a change costs nothing" sentence with the freeze-from-first-file rule, keeping the clock and transparent history
- [x] 3.3 Status: v0.1 declared at the tag; this text is the 0.2 draft; what 0.2 breaks and why; the transition sentence becomes the migration note
- [x] 3.4 A Migration subsection under Versioning: the steps, the acknowledgement carry-across, the unserved check, and that a 0.2 reader accepts a 0.1 workspace under 0.1 rules and refuses anything newer
- [x] 3.5 AVAILABILITY: `capacity` and `activities` in the example, the table, the prose on capacity, validity and clock, and the object-model diagram
- [x] 3.6 Every other mention of `conditional` (INTENTION `activity` row, the Consistency flag table, Resolution eligibility, `intentions.md`, the docs example README if it names the field) and of availability `duration` as capacity
- [x] 3.7 Validation section: unserved is an error under 0.2 and a warning under 0.1
- [x] 3.8 Reference Tool Set: `availability_add` and `availability_supersede` rows use `capacity` and `activities`; a `migrate` row under Workspace
- [x] 3.9 Design Principles: "The why is the price of entry" sentence names 0.2 instead of "the next that breaks files"

## 4. Site and example

- [x] 4.1 `docs/README.md`: the example is a 0.1 workspace read by a 0.2 reader until the CLI can migrate it; the figure script is unaffected
- [x] 4.2 Read the page against the README; nothing on the page names a field or version

## 5. Close out

- [x] 5.1 Commit and push
- [ ] 5.2 Open an issue on intentions-cli for 0.2: read 0.1 and write 0.2, `migrate` with the acknowledgement carry-across and the unserved check, the newer-format refusal, the two renames, the unserved refusal under 0.2; note it supersedes #8
- [ ] 5.3 Close #29 with a comment naming the commit and the tag
- [ ] 5.4 Archive with sync
- [ ] 5.5 Knowledge workspace: one claim and a qualification synthesis on the spine; commit and push
