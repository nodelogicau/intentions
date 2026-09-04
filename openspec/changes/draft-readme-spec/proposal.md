## Why

The seven capability specs settle the object model, but the format has no document a reader can pick up and implement from, and drafting one exposed three holes that every YAML example would hit: an intention does not say whose it is, no object says who wrote it, and retirement is a bare status field while every other event on an object is an append-only record. Those three are now settled in the knowledge workspace, so the README can be written the way the DKF README was: as the normative specification, with OpenSpec keeping it honest change by change.

## What Changes

- Write `README.md` as the normative specification for the intentions format, mirroring the DKF README's structure: Problem, Approach, Core Object Types with a complete YAML example per object and record, Object Model, File Layout, Design Principles, Status.
- **BREAKING** Add `subject` to INTENTION, required on disk, defaulting from a workspace-level subject URI at write time. Resolution's "own supply" is defined against it.
- **BREAKING** Add a `source` block (`author`, `harness`, `model`) to every object and record. `author` is required on INTENTION and AVAILABILITY. Source is excluded from the scheduling projection.
- **BREAKING** Replace the `status` field on INTENTION, AVAILABILITY, and COMMITMENT with an appended `retired` record (`kind`, `reason`, `superseded_by`, `timestamp`, `source`). "Active" is the absence of the record. `retired.kind` joins the projection.
- Add `source` to RESOLUTION records and to ACKNOWLEDGEMENT entries.
- Add `location`, a list of URIs, to INTENTION and AVAILABILITY as a second filter dimension beside activity; add `location` to PLACEMENT; add the `location-mismatch` flag kind; map location to and from JSCalendar and iCalendar on the commitment boundary.
- Settle, during drafting, the remaining gaps the README cannot leave open: the format's name and object prefixes, the activity-type vocabulary's home, the instance-generation trigger, canonical field order and serialisation (which the projection hash already depends on), an assertion `timestamp` on objects, `index.yaml` as a derived cache, and an explicit deferral of federation. Each is recorded in the knowledge workspace as it is decided and lands here as a further delta spec.

## Capabilities

### New Capabilities

None. The README is a document, not a capability; it is the rendering of the capabilities below.

### Modified Capabilities

- `object-model`: add source attribution; replace status-based retirement with the appended `retired` record; extend the projection rules to include `retired.kind` and exclude `source`; add the workspace subject default to configuration.
- `intention`: add `subject` and `source` to fields and projection; remove `status`; restate retirement kinds and standing-intention scenarios in terms of the `retired` record.
- `availability`: add `source`; remove `status`; add retirement kinds `retracted` and `superseded`.
- `commitment`: add `source`; remove object-level `status`; restate cancellation as a `retired` record with kind `cancelled`. Party status is unchanged.
- `resolution`: eligibility is "not retired" rather than `status: active`; location must intersect; RESOLUTION records carry `source`.
- `temporal-primitives`: PLACEMENT gains an optional `location`.
- `consistency`: ACKNOWLEDGEMENT entries carry `source`; the no-state-change rule names retirement rather than status.

## Impact

- `README.md` is created; it becomes the document the capability specs are derived from and must stay consistent with.
- All seven capability specs change.
- No implementation exists yet, so there is no migration of stored objects. The three breaking changes are breaking to the specification text only.
- The knowledge workspace at `~/IdeaProjects/intentions-knowledge` gains one claim or synthesis per gap settled during drafting; the change is not complete until each gap has both a workspace record and a delta spec.
