## Why

`declined` appears twice in the specification, both times in a field enumeration, and has no consequence anywhere (nodelogicau/intentions #24). A party who has refused a commitment still has that hour consumed from their capacity and still pays a displacement cost in every later resolution, which is the format charging a person for a claim they rejected. Occupancy is also written as though a commitment had one status, so the ranking ladder is undefined when three parties hold three different ones. This change gives `declined` its meaning, makes occupancy per-party, and adds the seventh flag kind that the resolution-born case needs.

## What Changes

- **Occupancy is per-party.** A commitment consumes a party's capacity, and is displaceable by that party's resolution, only where that party's own status is `tentative` or `accepted`. A `declined` party is not occupied by it. Nothing changes for the other parties, whose commitment still stands and still occupies their time.
- **The ranking ladder names whose status it means.** `accepted` and `tentative` in the ranking are the resolving subject's own party entry, and a commitment that does not occupy the subject's time is not displaced by their candidates.
- **A seventh flag kind, `party-declined`**: an intention is still placed while a party to the commitment fulfilling it has declined. Reported on both objects, with the declining party named in `detail`.
- **The two origins differ, and the flag says which case needs a person.** An imported commitment has no intention, so declining one frees the decliner's time and raises nothing. A commitment from a resolution leaves the intention placed and still occupying, so a decline alone leaves the subject saying they will not attend something they still intend at that hour. That contradiction is flagged, and the person cancels, replaces, or acknowledges.
- No new field, no projection change, and no change to what any act may do. Party status still changes only by that party's act, and no flag decides anything.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `consistency`: the `party-declined` kind, and what it is reported on.
- `commitment`: what `declined` entails for occupancy, stated where party status is defined.
- `availability`: capacity consumed per occasion becomes per-party.
- `resolution`: eligibility and ranking read a party's own status.

## Impact

- Four spec files. README sections: AVAILABILITY capacity paragraph, COMMITMENT party-status paragraph, the Consistency flag table and the paragraph after it, and the ranking rung in the resolution lifecycle diagram.
- The flag table grows from six kinds to seven, days before v0.1 is declared. Nothing already written changes meaning: a workspace whose commitments carry no `declined` party behaves exactly as before.
- The implementation shipped the conservative reading in v0.8.0, where a declined commitment still occupies and only cancellation frees anything. Issue #24 should say what changed and why.
- The knowledge workspace needs one synthesis after archive.
