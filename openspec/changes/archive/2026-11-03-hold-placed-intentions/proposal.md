## Why

Only a COMMITMENT may carry `external` (`{system, uid}`), and object-model says no other object type references an external calendar object. A placed intention with no `parties` has no commitment, so a harness that writes a busy hold for it has nowhere to record the hold's UID. On later runs it cannot find, move or release its own hold, cannot tell it from an unrelated event, and creates duplicates. If it imports from the same calendar, its hold comes back as an opaque imported commitment that clashes with the intention that produced it (issue #34).

## What Changes

- **A placed intention with no `parties` may carry `external`.** It has the same shape as a commitment's, `{system: icalendar|jscalendar, uid}`, and is the only link to the hold written for its placement. An intention with `parties` never carries it: its hold is its commitment's.
- **`external` on an intention is outside the scheduling projection.** The hold mirrors `placement`, which is already hashed. Writing or rewriting a hold leaves the version unchanged, so acknowledgements and `counterpart_version` do not move. The field lands in `intentions/0.1` and `intentions/0.2` without touching the freeze rule, and no hash moves. A commitment's `external` stays in its projection.
- **Holds are exported with a fixed, minimal shape.** The placement's start and duration (all-day placements in all-day form), `placement.location` where it is a URI, and the title, always opaque (`TRANSP:OPAQUE` / `freeBusyStatus: busy`), with `STATUS:TENTATIVE` for a tentative intention and `STATUS:CONFIRMED` for a firm one. Nothing else crosses: no description, serves graph, activity, policy or source.
- **A hold is never imported back.** An external event whose `system` and `uid` match an intention's `external` is recognised as that intention's hold and creates no commitment.
- **Lifecycle.** A replacing selection keeps `external`, so the harness moves the same event. Retirement keeps the record; the harness releases the hold for an intention retired as `abandoned` or `superseded` and leaves it for one retired as `fulfilled`.
- **Validation errors.** `external` on an intention with no `placement`; `external` on an intention with `parties`; two intentions carrying the same `system` and `uid`.
- **Text that said "only a commitment" is corrected.** Object-model's composition requirement, the commitment Purpose, and the README.

### Non-goals

- Replying to invitations. An iTIP REPLY changes a party's status and stays the party's own act, as it already is.
- Writing availability to a calendar as blocked time. Availability is supply, not occupation. Publishing it for others to book is federation, which the specification defers.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: Intention fields gains optional `external`, outside the projection. A new requirement, Calendar hold, covers who may carry it, the export shape, import recognition, and lifecycle.
- `commitment`: the Purpose no longer calls a commitment the only object that references an external calendar. External reference only keeps its rules for commitments and defers to Calendar hold for intentions.
- `object-model`: Composition with iCalendar and JSCalendar admits an intention's hold link. Versioning by projection hash lists an intention's `external` among the excluded fields. Validation gains three errors.

## Impact

- README: the INTENTION field table and projection note, the COMMITMENT section and its "only link" wording, the two diagrams that show `external.uid` on COMMITMENT alone, Versioning, Validation, and Status.
- Lands within `intentions/0.2` (and is admitted under 0.1). No hash moves and no workspace needs migrating.
- intentions-cli needs the field, the three validation errors, the import check, and hold export.
- Closes issue #34.
