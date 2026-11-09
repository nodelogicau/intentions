## Why

A placement's `start` is an RFC 3339 datetime with an offset (issue #37). An offset fixes the instant but not the zone whose clock it was read on. Yet the format reads every window, clock anchor and deictic term in `resolver.timezone`, so the zone is lost at the one point where the format touches clock time. As a result:

- `+10:00` could mean Melbourne in winter or Brisbane all year, so a person who changes `resolver.timezone` keeps placements that no longer say what local time they meant.
- A daylight-saving rule change by a government silently turns "10:00 Melbourne" into a different local time, and nothing notices.
- A hold or commitment exported from an offset has no `TZID` to carry.
- The episodes format stores when something happened as a local time plus an IANA zone, so comparing a placement with what happened needs the zone on both sides.

[RFC 9557](https://www.rfc-editor.org/rfc/rfc9557) extends RFC 3339 with a bracketed zone suffix, `2026-09-15T10:00:00+10:00[Australia/Melbourne]`, and keeps both.

## What Changes

- **A placement's datetime `start` may carry an RFC 9557 time-zone suffix.**
  - The suffix is an IANA zone name and nothing else: no offset-form suffix (`[+10:00]`), no other suffix tags such as `[u-ca=…]`, and no critical flag (`!`).
  - It is admitted only on a datetime `start`. A calendar-day (all-day) `start` carries none, and no other datetime field in the format admits one.
  - The same rules apply to the placement in a RESOLUTION record.
- **Writers keep the zone where they know it.**
  - Resolution writes the zone it resolved in: `resolver.timezone`, or the override on the call.
  - Import writes the event's zone when it is an IANA name: iCalendar `DTSTART;TZID=…`, or JSCalendar `timeZone`. A UTC start, or a `TZID` that isn't an IANA name, imports as an offset only, as now.
  - Existing placements without a suffix stay valid, and nothing back-fills them.
- **Export carries the zone.** A commitment or hold whose `start` has a zone is exported as a local time in that zone: iCalendar `DTSTART;TZID=`, JSCalendar `start` with `timeZone`. Zone definitions (`VTIMEZONE`) remain the exporter's concern; the format stores only the name.
- **The offset fixes the instant.** Where the offset disagrees with the zone at that instant, as after a daylight-saving rule change, the placement stays where its offset puts it. Validation warns, naming the placement, both offsets and the fix: re-select to restore the local time it was placed at.
- **No version changes.** Normalisation already writes datetimes as RFC 3339 UTC, and it now drops the suffix too. Adding, changing or removing a zone never changes a version. Comparisons between placements (re-import, an adopted commitment against its intention) compare instants, so a difference only in zone is no difference.
- **Windows and consistency are unchanged.** Clock anchors, all-day spans and deixis are still read in the resolver context. The zone records what the placement meant; it doesn't change how anything is computed.
- **New validation findings.**
  - Error: a suffix that is not a bare zone name, a suffix on an all-day `start` or on any field other than a placement's `start`, and a critical flag.
  - Warning: an offset that disagrees with its zone at that instant, and a zone name the reader's time-zone database does not know.

### Non-goals

- Reading windows or clock anchors in a placement's zone rather than the resolver's.
- Floating times (iCalendar times with no `TZID` and no `Z`, JSCalendar `timeZone: null`) on import, which stay as they are today.
- Mapping non-IANA `TZID`s (Windows names, custom `VTIMEZONE`s) to IANA names.
- Storing zone definitions, or a tz database version, in the workspace.
- Zones on any datetime other than a placement's start.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `temporal-primitives`: Placement is the collapse to clock time admits the zone suffix, says who writes it, and says that the offset fixes the instant.
- `object-model`:
  - Versioning by projection hash: normalisation drops the suffix.
  - Validation: three errors and two warnings.
  - Composition with iCalendar and JSCalendar: a zone name is a reference to the IANA database, not a copied zone definition.
- `commitment`: External reference only imports and exports the zone.
- `intention`: Calendar hold exports a placement's zone.

## Impact

- README:
  - PLACEMENT section;
  - External reference only, under COMMITMENT;
  - Calendar hold, under INTENTION;
  - Versioning, Normalisation;
  - Validation;
  - Status;
  - References (Standards borrowed as grammars: RFC 9557).
- Lands within `intentions/0.2` and applies under 0.1, since no projection changes.
- A reader older than this change rejects a suffixed `start` as unparseable. So, as with `habit` and an intention's `external`, every reader of a shared workspace must be upgraded before any writer emits a zone. Status says so.
- intentions-cli needs:
  - parse and emit RFC 9557 on placements;
  - normalise by dropping the suffix;
  - write the zone on resolution and import;
  - carry it on export;
  - the five findings.
- Closes issue #37.
