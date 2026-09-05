## Why

Comparing the format with RFC 5545 found two things the README implies it can express but cannot. WINDOW bottoms out at a day granule, so the README's own example, an availability titled "Tuesday mornings for deep work", carries nothing that distinguishes it from Tuesday evenings; "free after five" and "not before nine" are the commonest availability statements people make. And every placement consumes time: there is no analogue of iCalendar `TRANSP` or JSCalendar `freeBusyStatus`, so an imported conference week or a colleague's leave raises `window-clash` against everything it overlaps. Both are recorded as claims in the knowledge workspace (`clm_01a070c8-73bb…` and `clm_01a070c8-73d0…`) and both need the spec to move before they can be synthesised.

## What Changes

- WINDOW gains an optional `clock` anchor: an ISO 8601 time-of-day interval such as `09:00/12:00`, read in the resolver's timezone and applied to every local day the window's other anchors admit. Absent means whole days, so every existing window keeps its meaning.
- Cadence is restricted to the date-level RRULE parts. `BYHOUR`, `BYMINUTE`, and `BYSECOND` are not admitted; time of day lives in `clock` and nowhere else.
- PLACEMENT `start` may be a calendar date, making an all-day placement whose duration is whole days, so that imported `DATE`-valued events have a representation.
- COMMITMENT gains `transparent`, a boolean in the projection, default false. Only an import may set it true; a commitment from a resolution is opaque by construction and validation errors otherwise. Import maps `TRANSP:TRANSPARENT` and `freeBusyStatus: free` onto it; export writes them back.
- A transparent commitment occupies no time and rests on no supply. Consistency never reports `window-clash`, `condition-mismatch`, `location-mismatch`, or `expired-ground` on it or against it, and resolution neither displaces it nor counts it in reconsideration cost.
- Resolution computes supply and demand within `clock` bounds: a candidate must lie inside the intention window's clock interval and inside the supplying availability's.
- **BREAKING** for the projection: `window.clock` and `transparent` enter the hashed field set, so every stored `counterpart_version` computed under `intentions/0.1` lapses. The format version string is unchanged because v0.1 has not been declared; this is the last moment such a change is free.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `temporal-primitives`: WINDOW admits a `clock` anchor; cadence excludes sub-day RRULE parts; placement admits an all-day form.
- `availability`: the field list and a scenario show time-of-day capacity; `clock` is a change of terms for renewal versus supersession.
- `commitment`: `transparent` field, its import and export mapping, and the rule that only an import may set it.
- `consistency`: transparent commitments are excluded from the supply and overlap kinds.
- `resolution`: supply is computed within clock bounds; transparent commitments are never displaced.

## Impact

- Five spec files and the README sections for WINDOW, cadence, PLACEMENT, COMMITMENT, consistency, resolution, and validation. The README availability example gains `clock: 09:00/12:00` so its title finally says something the object also says.
- No implementation exists yet, so nothing on disk migrates. A workspace written against the current text would see every acknowledgement lapse once, because the projection changed.
- The knowledge workspace needs one synthesis after archive, closing the two gap claims against the new text. Presence is not in scope: an own non-blocking whereabouts entry is the PRESENCE object already named under Status, and `transparent` deliberately arrives only from outside.
