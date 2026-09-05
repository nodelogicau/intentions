## Context

WINDOW has two anchors, a calendar granule (EDTF, day or coarser) and a relational one (RFC 9253), and its bounds are computed at resolution time from the resolver's timezone and week start. Nothing carries a time of day. Cadence is an RRULE that produces day granules. PLACEMENT is a datetime with offset plus a duration. Every commitment has a placement and every placement clashes on overlap.

Two claims in the knowledge workspace record what this cannot say: the availability example titled "Tuesday mornings" is indistinguishable from Tuesday evenings, and an imported non-blocking event flags everything it touches. The README's delegation rule keeps alarms, timezones, and iTIP outside, and that rule is right; these two are prospective facts the resolver and the consistency check need, so they belong inside.

The projection field set is frozen per format version, and `intentions/0.1` has not been declared. Adding fields to the projection now costs nothing; adding them after v0.1 would be a format bump.

## Goals / Non-Goals

**Goals:**
- A window or availability can say which hours of a day it means, in one place, without storing computed bounds.
- An imported event that does not occupy the person can be held as a commitment without raising a clash against everything it overlaps.
- Imported all-day events have a representation, since they are the commonest transparent events.
- Round-trip with iCalendar and JSCalendar for the properties involved: `DTSTART` as `DATE`, `TRANSP`, `freeBusyStatus`.

**Non-Goals:**
- Presence. An own non-blocking whereabouts entry ("in Berlin this week") is the PRESENCE object named under Status, not a transparent intention.
- Floating local times on import, RDATE-style irregular date sets, per-import suppression policies, and any change to the delegation rule for alarms or timezone definitions.
- A format version bump. This lands before v0.1 is declared.

## Decisions

**Time of day is a third WINDOW anchor, `clock`, not an RRULE part and not an EDTF datetime.** `clock` is an ISO 8601 time-of-day interval, `HH:MM/HH:MM`, read in the resolver's timezone and applied to every local day the other anchors admit; end is exclusive; the interval may cross midnight, in which case the day is the local day of its start. Alternatives: `BYHOUR`/`BYMINUTE` in cadence was rejected because a one-off availability with no cadence ("this week, after five") needs hours too, and because RRULE mixes the generating pattern with the bound, which the format keeps apart. An EDTF datetime anchor was rejected because EDTF has no time-only form, and a full datetime is a computed bound, which WINDOW must never store. `clock` sits beside `calendar` and `relative` and combines with both: a placement must satisfy every anchor present. Sub-day RRULE parts are excluded from cadence so that time of day has one home.

**`clock` is stored as written and its bounds are computed like every other anchor.** No offset is stored. This keeps the existing rule that a window means the same thing when the resolver's timezone changes, and it is what makes "mornings" survive a move between zones. Where a clock time does not exist on a given local day (a spring-forward gap), the resolver follows RFC 5545 §3.3.5 for nonexistent local times.

**Transparency is a COMMITMENT field, `transparent`, and only an import may set it.** A commitment from a resolution consumed supply to exist, so it is opaque by construction; `transparent: true` with `origin: {resolution: …}` is a validation error. Alternatives: a field on INTENTION was rejected because a transparent intention would need resolution to place it without supply, which contradicts what resolution is, and because the only own non-blocking thing anyone wants to write is whereabouts, which is presence. A field on PLACEMENT was rejected because placement is a value written by resolution or import, and occupancy is a fact about the engagement, not about the instant. The name borrows iCalendar's term the way cadence borrows RRULE: it maps one-to-one on both boundaries (`TRANSP`, `freeBusyStatus`) and every calendar user already knows it.

**A transparent commitment is exempt from every supply and overlap kind, not only `window-clash`.** It occupies no time, so it is neither subject nor counterpart of `window-clash`; it rests on no supply, so there is no supplying availability for `condition-mismatch`, `location-mismatch`, or `expired-ground` to compare against. Resolution treats it the same way: overlap with it is not displacement, for ranking or for the record. Exempting only `window-clash` would leave the mismatch kinds firing against an availability the commitment never claimed.

**All-day placement is a `start` that is a calendar date.** When `start` is an EDTF day, `duration` is whole days and the placement spans those local days in the resolver's timezone. Alternatives: local midnight with `P1D` was rejected because a DST-transition day is not twenty-four hours and export would write `DATE-TIME` rather than `DATE`, breaking the round-trip; a separate `all_day` flag was rejected as redundant with the value's type. Resolution keeps writing datetimes; only import writes dates in this version.

**`window.clock` and `transparent` enter the projection.** Both change what clashes, so leaving them out would let an edit to either pass without lapsing an acknowledgement of a state it changed.

## Risks / Trade-offs

- [Every stored `counterpart_version` computed under the current field set lapses once] → No implementation exists; the README's versioning section already says a projection change is a format change, and v0.1 is undeclared, so this is the last free moment. Noted in the proposal as breaking.
- [iCalendar defaults all-day events to `OPAQUE` while most clients treat them as free] → Import maps what the source says, never what a client would assume. An opaque all-day import flags overlaps, which is correct under RFC 5545 and is exactly the imposition the flag exists to surface. A standing suppression for such imports is open item 2 in the knowledge workspace and is not decided here.
- [A midnight-crossing `clock` combined with a `BYDAY` cadence is ambiguous about which day it belongs to] → Defined: the local day of the interval's start.
- [`clock` on an intention and `clock` on its supply may not intersect] → That is "no supply", the same outcome as disjoint locations, and resolution already reports it.
