## Why

A reviewer noticed that every firm terminus of one subject has the same version. A firm terminus's projection is just `subject` and `stability`, and its title is prose. That's intended: a version detects change within one object and is always compared together with an id, as an acknowledgement's `counterpart` and `counterpart_version` are. But the text never says a version isn't an identity, so a reader can reasonably worry that two objects could be confused by it. The same review surfaced a real gap, that a policy's condition is outside the projection. That's tracked separately in nodelogicau/intentions#43 because it needs a format version.

## What Changes

- The object-model spec's Versioning requirement says that a version identifies a state of one object, not the object. Two objects with equal projections have equal versions, and a version is compared only together with the id it was read from. A scenario shows two termini sharing a version.
- The README's Versioning section says the same in a sentence.
- No field, projection, hash or behaviour changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `object-model`: Versioning by projection hash states that a version is not an identity, with one scenario.

## Impact

README Versioning section; `object-model` spec. Implementations already compare versions only alongside ids.
