## Why

Supply is the intersection of eligible availability for the subject and for every party, so an intention naming someone at another organisation has no candidates on the day it is written and no candidates ever (nodelogicau/intentions #25). A workspace holds the capacity of the people it is for and mostly cannot hold anyone else's, so the rule rules out a large share of what people mean to do. In practice it has done worse than that: an agent driving the reference implementation manufactured an availability for each external party so that resolution would succeed, writing a record of a fact nobody asserted about someone whose time is not the workspace owner's to declare. Guidance cannot fix that, because an agent obeying the guidance cannot schedule an external meeting at all. The format has no way to say the difference between a party who has offered no capacity that fits, which is a real constraint, and a party whose capacity this workspace does not track, which is a statement about the workspace.

## What Changes

- **A party with no availability records at all is unconstrained, not satisfied.** Resolution places against the subject's own supply and the supply of every party the workspace does track, and the commitment is written with the untracked party `tentative`, which is already what the format calls someone who has not yet agreed. This is the state an iTIP invitation is sent from.
- **A party with records but none eligible still yields an empty candidate set**, naming that party. Having spoken and having offered nothing that fits is a real conflict, and the test needs no new configuration: the workspace tracks a party exactly when it holds any availability whose subject is that party.
- **The subject is never unconstrained.** Their own supply is always required, however few records they have.
- **An untracked party still contributes their placements.** The workspace knows nothing of an external party's capacity but knows exactly what it has already asked of them, so a candidate that would place a second commitment on an untracked party at an overlapping hour is refused as it would be for a tracked one. Without this, resolution would double-book the same external person, or an untracked room, and never notice.
- **The presumption is recorded.** The resolution result and the RESOLUTION record name the parties that contributed no supply, in a `presumed` list beside `supply`, outside the projection, so a person reading the file sees that the placement rests on an assumption about someone else's time.
- **`window-clash` says whose placements clash**: two placements clash when they share a party whom both occupy, which is what per-party occupancy already implied and what untracked parties make load-bearing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `resolution`: untracked parties, the subject exemption, placements of untracked parties, and `presumed` on the record.
- `consistency`: `window-clash` states whose placements overlap.
- `object-model`: the federation requirement's scenario, which currently says a party held elsewhere yields no supply.

## Impact

- Three spec files. README sections: the INTENTION `parties` row, the resolution lifecycle diagram, the RESOLUTION record and its prose, and the Consistency flag table row for `window-clash`.
- No new field on any object and no projection changes, so no format version bump. `presumed` joins `supply` on the record, both outside the projection.
- This is normative and changes what resolution does, so it should land before v0.1 is declared. The behaviour as it stands is producing false records in the field, which is the worst kind of thing to freeze into a version.
- The knowledge workspace needs one synthesis after archive.
