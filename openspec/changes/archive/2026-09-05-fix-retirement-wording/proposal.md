## Why

The draft-readme-spec sync replaced the body of the retirement requirement with the appended-record design but kept its original header, so the object-model spec now has a requirement titled "terminal status" that forbids a status field. Two scenarios still say "its status is not changed" for the same reason. A reader implementing from the specs would find a term the format no longer uses.

## What Changes

- Rename the object-model requirement "Retirement is a terminal status, never deletion" to "Retirement is an appended record, never deletion".
- Reword one scenario in intention and one requirement plus scenario in resolution to say what is actually preserved: the displaced object's placement, stability, and retirement state, rather than "its status".
- No normative behaviour changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `object-model`: requirement renamed; body unchanged.
- `intention`: wording of the reconsideration scenario.
- `resolution`: wording of the displaced-objects requirement and its scenario.

## Impact

- Three spec files. README is already consistent and does not change.
- No knowledge-workspace record is needed: this corrects the text to match a decision already recorded (retirement as an appended record), it does not make a new one.
