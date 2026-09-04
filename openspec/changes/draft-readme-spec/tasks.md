## 1. Settle remaining design questions in the knowledge workspace

- [ ] 1.1 Decide the format name and object prefix convention; record as a synthesis, add an object-model delta if prefixes change
- [ ] 1.2 Decide where the activity-type vocabulary lives; record as a synthesis, add deltas to intention and availability
- [ ] 1.3 Decide the instance-generation trigger and whether instances are persisted before resolution; record as a synthesis, add an intention delta
- [ ] 1.4 Define canonical field order and canonical serialisation for the projection hash; record as a synthesis, add an object-model delta
- [ ] 1.5 Decide whether objects carry an assertion `timestamp` distinct from id minting time; record as a synthesis, add deltas to object-model and availability (horizon origin)
- [ ] 1.6 Specify `index.yaml` as a derived cache; record as a synthesis, add an object-model delta
- [ ] 1.7 Decide whether one workspace may hold several subjects or that is federation; record as a synthesis, add an object-model delta or a Status deferral note
- [ ] 1.8 Decide whether availability renewal is an edit or a supersession; record as a synthesis, add an availability delta
- [ ] 1.9 Decide whether harness-drafted intentions need a confirmation act before becoming firm; record as a synthesis, add an intention delta if so
- [ ] 1.10 Run `particulars validate` and `particulars conflicts` on the knowledge workspace and commit it

## 2. Draft README.md

- [ ] 2.1 Write the Problem section: clock time, slot scheduling, and what iCalendar cannot say
- [ ] 2.2 Write the Approach section: duration, window, intention; availability as supply; commitment as hand-off; DKF as the retrospective layer
- [ ] 2.3 Write Core Object Types: identifiers, field order, source, then INTENTION with a complete YAML example
- [ ] 2.4 Write AVAILABILITY and COMMITMENT with complete YAML examples
- [ ] 2.5 Write the records: RESOLUTION, ACKNOWLEDGEMENT, and retirement, each with a YAML example
- [ ] 2.6 Write WINDOW and DURATION: EDTF calendar anchors, RFC 9253 relational anchors, cadence, placement
- [ ] 2.7 Write the Object Model section with the objects-and-records diagram, the serves graph, and the resolution lifecycle
- [ ] 2.8 Write Consistency: flag kinds, computation, acknowledgement suppression and lapse
- [ ] 2.9 Write File Layout and `intentions.yaml`
- [ ] 2.10 Write Design Principles and Status, including explicit deferrals (federation, v0.1)

## 3. Reconcile and verify

- [ ] 3.1 Check every field named in README.md against the main specs plus this change's delta specs; fix whichever is wrong and record any new decision as a synthesis
- [ ] 3.2 Check every YAML example in README.md validates against the rules the specs state (required fields, admitted values, projection membership)
- [ ] 3.3 Run `openspec validate --changes` and `openspec validate --specs`
- [ ] 3.4 Commit README.md and the change directory
