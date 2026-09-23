## Why

A side-by-side reading of every object's fields found five things a second implementer would trip on or have to guess at. COMMITMENT's `origin` is a union type, a mapping for one value and a bare string for the other. `parties` names a list of URIs on an intention and a list of `{uri, status}` on a commitment, and nothing says so. The person's own act is recorded by absence on a live object (`firmed_under`) and by an explicit sentinel on a record (`selector: person`), with no stated reason. A DESIRE keeps `activity` and `location` as the person's own hints but not `parties`, though "lunch with Priya" is the hint most likely to be said. And `timestamp` on an object that is edited in place is defined as assertion time without saying whether an edit updates it. None changes what the format means; all are cheaper now than after v0.1.

## What Changes

- **`origin` becomes a plain value.** `origin` is `resolution` or `import`. A sibling `resolution` field carries the record id, present when and only when `origin` is `resolution`. Both are in the projection, as `origin` was. **BREAKING** for commitment files born of a resolution, which change shape; nothing else in the file moves.
- **`parties` is named as two shapes.** The INTENTION row says its `parties` are URIs and that a commitment's are entries with a status; the COMMITMENT row says the reverse, and notes that `tentative` on a party is iCalendar's sense, tentatively accepted, not the intention's sense, cheap to reconsider.
- **The convention for the person's own act is stated, not changed.** On a live object, the absence of an authorising policy means the person acted; on a record, the actor is always written, because a record is read on its own and absence there is silence. One sentence under Source and timestamp, and the same sentence in the object-model spec.
- **DESIRE gains `parties`** as a hint, URIs, outside the projection, carried onto the intention on adoption alongside `activity` and `location`.
- **`timestamp` on an object is the time of its last write.** Each edit is a new assertion; git holds the history. On a record it remains the time of the act.
- The `version` and `subject` rows are worded the same way in every table.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `commitment`: fields and projection for `origin` and `resolution`; the `parties` sentence.
- `intention`: the `parties` sentence.
- `desire`: `parties` as a hint; adoption carries it.
- `object-model`: Timestamps (last write on an object); Source attribution (the person's-act convention).

## Impact

- README: the COMMITMENT example, fields table, projection line and object-model diagram; the INTENTION and COMMITMENT `parties` rows; the DESIRE example, table, adoption paragraph and the two tool rows; Source and timestamp; every `version` and `subject` row. Four deltas.
- File-breaking for one object type. The example workspace's commitment was written by the CLI with the old shape and stays as it is until the CLI writes the new one; the proof figure does not read `origin`.
- intentions-cli: `origin` and `resolution` on write and read, `parties` on `desire add` and `desire adopt`, and `timestamp` updated on edit. One issue.
- Knowledge workspace: one claim and a qualification synthesis on the spine.
