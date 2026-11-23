## 1. Spec

- [x] 1.1 Add `standalone-conformance`: no field requires another format's identifier; particulars defined without another format's object model; no rule constrains another format; text about other formats is informative
- [x] 1.2 Modify *Composition with DKF by reference only* in `object-model`: `reference` is any URI or string, and the rule about DKF claims is removed
- [x] 1.3 Modify *Intention fields* and *Terminus* in `intention`, *DESIRE is the rung below intention* in `desire`, and *Acknowledgement as retrospective seed* in `consistency`

## 2. README

- [x] 2.1 Add a Conformance section after The Approach
- [x] 2.2 Define *particular* in Core Object Types
- [x] 2.3 Generalise `reference` in the DESIRE and INTENTION tables, the serves-graph prose and diagram
- [x] 2.4 Remove the `occasion` passages from The Approach, *Composition by reference*, Design Principles, Status and References, and mark *Composition by reference* informative
- [x] 2.5 Restate the DKF analogies in this format's own terms, keeping them as informative asides
- [x] 2.6 Reword the DKF References entry: conventions copied by agreement and restated in full
- [x] 2.7 Add a Status note: no file or behaviour changes

## 3. Verify and follow up

- [x] 3.1 Run `openspec validate standalone-spec --strict` and fix any findings
- [ ] 3.2 Check intentions-cli help text for `reference` described as a DKF claim pointer, and open an issue there if it is
