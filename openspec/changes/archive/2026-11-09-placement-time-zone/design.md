## Context

Issue #37. A `PLACEMENT.start` is an RFC 3339 datetime with offset, or an EDTF calendar day for an all-day placement. Everything else that touches local time is read in the resolver context, `resolver.timezone`, which `intentions.yaml` declares and a call may override:

- window bounds;
- clock anchors;
- deictic terms;
- the local days an all-day placement spans.

Normalisation hashes datetimes as RFC 3339 UTC with seconds, so the offset is already outside every version.

External reference only keeps "timezone definitions" in the external system. Neither import nor export says what happens to an event's `TZID` or JSCalendar `timeZone`.

The review on #37 chose RFC 9557's in-string suffix over a separate `zone` key. The suffix is the standard grammar, and the format borrows grammars rather than inventing fields. The cost is that readers older than this change must be upgraded first.

## Goals / Non-Goals

**Goals:**
- A placement says which zone's clock it was placed on, wherever the writer knows it.
- A zone round-trips through import and export.
- A daylight-saving rule change that moves a placement's local time is reported, never silently absorbed.
- No version changes, and no format version.

**Non-Goals:**
- Changing how windows, clock anchors or all-day spans are computed. They stay in the resolver context.
- Floating times on import, and mapping non-IANA `TZID`s.
- Zones anywhere but a placement's datetime `start`.
- Storing zone definitions or a tz database version.

## Decisions

**The suffix grammar admitted.** RFC 9557 allows a time-zone suffix (an IANA name or an offset), any number of other suffix tags, and a critical flag `!` on any of them. The format admits exactly one suffix, a bare IANA zone name, after an RFC 3339 datetime that has an offset:

- **An offset-form suffix** (`[+10:00]`) adds nothing to the offset already there, so it is an error.
- **Other suffix tags** (`u-ca=` for calendar system, experimental tags) have no meaning here, so they are errors, like EDTF qualifiers with no resolution semantics.
- **The critical flag** asks a reader to refuse a value whose offset and zone disagree. The format's answer to disagreement is a warning (below), so the flag would demand a refusal the format doesn't make. It is an error.
- **A suffix with `Z`** (`…Z[Australia/Melbourne]`) is legal RFC 9557. It says the local time is unknown and only the instant is meant. Resolution and import never write it, since they always know the offset. It is admitted, with no finding.

**Where it is admitted.** Only on a datetime `start` of a PLACEMENT, on an intention, a commitment or a RESOLUTION record. An all-day `start` is a calendar day spanning local days in the resolver's zone, and has no instant to annotate. `timestamp`, `valid_until` and the datetimes in records are instants of recording or horizons, not local times anyone chose. A suffix anywhere else is an error naming the field.

**Who writes it.**
- **Resolution** writes the zone it resolved in: `resolver.timezone`, or the call's override. It is the zone whose clock the window and clock anchors were read on to produce the candidate, so it is exactly what was meant.
- **Import** writes the zone when the event's start names an IANA zone: iCalendar `DTSTART;TZID=` where the `TZID` is an IANA name, or JSCalendar `timeZone`. A UTC start (`Z`, or JSCalendar `timeZone: "Etc/UTC"`) imports as an offset of `Z` with no suffix, since an event pinned to UTC chose no local clock. A non-IANA `TZID` imports as the offset its `VTIMEZONE` gives, with no suffix. Guessing a mapping would assert a zone the event never named.
- **Adopting** copies the commitment's placement, zone included.
- **Nothing back-fills.** A placement written before this change keeps its plain offset. Adding `resolver.timezone` to it would claim a zone that may not have been the one used.

Alternative considered: requiring a zone on every new datetime placement. Rejected, because an import from a non-IANA or UTC source has none to give, and making it optional for import but required for resolution adds a rule for little gain. Resolution writes it whenever it can.

**The offset fixes the instant.** A placement is a selected instant. The candidate was chosen against supply and displaced objects at that instant, and a commitment's parties answered for that instant. If tz rules change after selection, so that the zone now gives a different offset at that local time, moving the placement to keep its local time would change what was agreed without anyone's act. So the instant stands. Validation warns that the offset disagrees with what the zone gives at that instant, naming:

- the placement and its object;
- the written offset, and the zone's offset at that instant now;
- the fix: re-select, a replacing selection, to restore the local time the placement was made at.

This follows RFC 9557's default for a suffix without the critical flag, where the offset governs. Alternative considered: the zone governs, and the instant follows the rules. Rejected for the reason above. It would also make a placement's instant depend on the reader's tz database version.

**An unknown zone name** is a warning, not an error. Zone names are added to the tz database over time, and an older database not knowing a newer name says nothing about the file. The offset still fixes the instant, so nothing is ambiguous.

**Normalisation drops the suffix.** Datetimes are already normalised to RFC 3339 UTC, and the suffix is now removed in the same step. So:

- adding, changing or removing a zone never changes a version;
- an acknowledgement never lapses because of one;
- a re-import that only gains a zone moves nothing.

The zone is outside the projection for the reason the offset is: consistency is computed on instants and on the resolver context, never on a placement's zone.

**Comparisons are on instants.** Wherever the spec compares two placements, it compares their normalised instants, durations and locations, never their zones. That covers the warning on an adopted commitment whose placement differs from its intention's, the re-import check, and a replacing selection. An adopted commitment re-imported with a different `TZID` but the same instant raises nothing.

**Export.** A commitment or hold whose `start` carries a zone is exported as a local time in that zone: iCalendar `DTSTART;TZID=<zone>:<local time>`, JSCalendar `start` (a local date-time) with `timeZone: <zone>`. iCalendar requires a `VTIMEZONE` for every `TZID` it uses. The exporter supplies it, or relies on time zones by reference (RFC 7809), and the workspace stores no definition. A `start` with no zone exports as today. An all-day placement exports as a date, as today.

**Composition.** "Timezone definitions remain in the external system" still holds. A zone name refers to the IANA database, as a URI location refers to a place. The format stores the name and never its rules. The Composition requirement says so, so the suffix isn't read as embedding iCalendar timezone grammar.

**No format version.** No projection's field list changes, and no hash moves. The change applies under 0.1 and 0.2. Older readers will reject the suffix as an unparseable datetime, which validation already reports as an error. Status tells shared workspaces to upgrade every reader before a writer emits a zone, as it does for `habit` and for an intention's `external`.

## Risks / Trade-offs

- [An older reader in a shared workspace errors on every new placement] → Status says to upgrade every reader first. The finding it raises (unparseable datetime) names the field, so the cause is visible.
- [tz database drift between readers] → Only the disagreement warning and the unknown-name warning depend on the database, and both are warnings. The instant, the version and every consistency result are independent of it.
- [A zone that is wrong for what the person meant (resolver context overridden carelessly)] → The zone is the one the resolution actually ran in, so it is a true record of how candidates were computed. If it isn't what the person meant, that is a resolver-context problem, and re-selecting fixes it.
- [Imports from Windows-zone calendars carry no zone] → They behave exactly as today. Mapping is a deliberate non-goal, since it would assert a zone the event didn't name.
- [Some YAML tools may quote or mangle the bracket] → `[` inside a plain scalar after other characters is valid YAML 1.2, but writers SHOULD emit the value as written. Canonical field order is unchanged.

## Migration Plan

Nothing to migrate. Existing placements stay as they are and stay valid. After every reader of a shared workspace is upgraded, new resolutions and imports start writing zones. Rollback is to stop writing them. Files that already carry a suffix stay valid for upgraded readers.

## Open Questions

- Should `validate` offer, at info level, a placement written by resolution after this change that carries no zone? It would catch a writer that forgot. Left out for now, since an older writer can't be told apart from a forgetful one.
