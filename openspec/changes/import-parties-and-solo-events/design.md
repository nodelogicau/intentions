## Context

Issue #35. Import always creates a COMMITMENT and never an intention or availability (Two origins). The spec states how place, transparency and all-day form cross from iCalendar and JSCalendar, but not how participants become `parties`. Nothing requires an imported commitment to name anyone besides the subject, so a solo event (a ticket, a gym block, a dentist booked by hand) imports as a one-party commitment. The commitment Purpose calls a commitment "directed at someone", but that is prose, not a requirement.

The review on #35 chose option 3 from the issue: keep importing solo events as commitments and flag them. It also chose to take the subject's status from the event's `PARTSTAT`, and to reconcile an intention with someone else's event by letting the imported commitment name the intention it fulfils. #34's hold link can't do that job. A harness treats an intention's `external` as its own hold, and moves or releases it with the placement, so pointing it at a venue's event would rewrite or delete that event.

#36 already warns when an intention's `external` matches an unretired commitment's.

## Goals / Non-Goals

**Goals:**
- Two conforming importers produce the same `parties`, and so the same version, from the same event.
- The subject's own status comes from what the subject did in their calendar.
- A one-party import is visible as such, without changing what import creates.
- A person can say "this imported event is my intention's occasion", and afterwards nothing clashes or is counted twice.
- No projection changes and no format version.

**Non-Goals:**
- Importing as an intention (option 2), or forbidding one-party commitments.
- iTIP processing, delegation chains, `SENT-BY`, `RSVP`, `CUTYPE`, `ROLE` other than non-participant, and `DELEGATED-TO`/`-FROM`, which stay in the external system.
- Adopting under a policy, or by a harness on its own judgement. A harness may perform the act on the person's instruction, recorded in `source.harness`, as with any selection the person makes.
- Exporting a linked commitment differently from any other commitment.

## Decisions

**Which entries become parties.** In iCalendar, each `ATTENDEE` and the `ORGANIZER`. In JSCalendar, each `participants` entry with a calendar address (`sendTo`; `imip` preferred, then any other method in key order). Entries that only receive information don't become parties: `ROLE=NON-PARTICIPANT`, or JSCalendar `roles` holding only `informational`. They aren't occupied by the event, and occupation is what `parties` is for. Rooms and resources (`CUTYPE=ROOM|RESOURCE`) do become parties, matching an intention's `parties`, where a room that must be booked is a particular. An entry with no address is dropped, since a party needs a URI.

**URI.** It is the calendar address, a `mailto:` address lowercased in full, because addresses are matched without regard to case in practice and the hash must not depend on case. An address listed under a subject in `calendar.addresses` becomes that subject's URI instead. One URI gives one entry. Where an address appears as both organizer and attendee, the attendee entry's status wins, since that is the organizer's own answer.

**Status.** `ACCEPTED` → `accepted`. `TENTATIVE` → `tentative`. `NEEDS-ACTION`, or no `PARTSTAT`, → `tentative`, the same as a resolution's commitment before anyone answers. `DECLINED` → `declined`. `DELEGATED` → `declined`: the delegator won't attend, and the delegate, if the event lists them, is their own entry. JSCalendar `participationStatus` uses the same values in lower case. An organizer with no attendee entry is `accepted`, because organising is their act.

**The subject's entry.** Import runs on behalf of one subject: the workspace's `defaults.subject`, unless the import names another. The subject is always a party:
- **The event names the subject** (by an address in `calendar.addresses`, or by the subject URI itself): their status is mapped as above.
- **The event names no one:** it is in the subject's own calendar by their own act, so the status is `accepted`.
- **The event names others but not the subject:** for example, an event on a shared calendar. The status is `tentative`, since nothing records an answer.

This answers #35's question: the event's `PARTSTAT`, which is the subject's own act in their calendar. It keeps "a status changes only by that party's act" intact.

**`calendar.addresses`.** This is an optional map in `intentions.yaml`, from subject URI to a list of calendar addresses. Without it, two importers would guess differently about which attendee is the person. In a multi-subject workspace it maps each subject, so an event between two of them gives two subject URIs. It sits outside every projection. It is configuration, like `resolver.timezone`. Alternative considered: an import-time parameter. Rejected, because it isn't reproducible from the workspace.

**Re-import.** Each import applies the mapping. Where an event comes back with a changed `PARTSTAT`, that is the party's reply as it reached the calendar, an imported iTIP reply in effect, or the subject's own act in their calendar. The commitment's `parties` follows, and its version changes, as it already does for transparency. A re-import SHALL NOT clear `intention`. The link is the person's, not the calendar's.

**The one-party finding is `info`.** A typical calendar import brings in many personal blocks, so a warning would bury the real warnings. The finding names the commitment and says it is directed at no one and may be better recorded as an intention, which can then adopt it. It is not reported for a commitment that already names an intention, or whose `external` matches an intention's (#36's warning covers that).

**Adopting is a selection.** The intention gains a placement, and placements arrive only by selection (Selection is a recorded act). So adopting writes a RESOLUTION record:
- `selector: person`;
- `placement` equal to the commitment's;
- `candidates_considered: 1`;
- `displaced` listing whatever else the placement displaces, but never the adopted commitment;
- `supply` and `presumed` as for any selection.

In the same act, the commitment's `intention` is set, and its version changes, since `intention` is in its projection. The commitment's `origin` stays `import`, and it gets no `resolution`, because the resolution record belongs to the intention's placement, not to the commitment's creation. The placement need not be a candidate. The person is accepting an occasion that already exists, and consistency reports anything it lacks, such as no eligible supply. Adopting may replace an existing placement, as a re-selection.

Preconditions, each refused at write time and each an error under validation:
- the commitment is unretired and imported;
- the intention is unretired;
- the intention's `subject` is one of the commitment's parties;
- the intention has no `parties`, since one with parties gets its commitment from resolution;
- the intention carries no `external`, since the imported event is its calendar presence and a hold would duplicate it (clear `external` first, and the harness releases its hold);
- no other unretired commitment names the intention.

Alternative considered: setting `intention` on the commitment alone, without a resolution record. Rejected: the intention would be unplaced while its occasion occupies the subject's time, so resolution would place it elsewhere.

**One occupation.** A commitment and the intention it fulfils are never a `window-clash` with each other. Where both occupy the subject over the same interval, the subject's capacity is consumed once. This is what a resolution's commitment has always needed, but no text said it, so it is stated in Consistency for both origins.

**When the event moves.** A re-import that changes the commitment's placement leaves the intention's placement where it was. Validation warns that an imported commitment's placement differs from its intention's, naming both. The fix is to adopt again. The warning is not an error, because the person may be deliberately keeping the old placement while they decide.

**Cancelling an adopted commitment** follows Cancellation: the intention's placement is cleared, and the intention may be re-resolved. This is the right result when the venue cancels and the person records it.

**No format version.** No projection's field list changes. `intention` was already in a commitment's projection. Re-importing may move a commitment's version where an earlier importer mapped parties differently. That is a correction to data the spec never fixed, and acknowledgements lapse as they do for any re-import change. Answering #35's third question: `intentions/0.3` is not needed.

## Risks / Trade-offs

- [Existing imported commitments change version on their next import] → Only where the earlier importer differed from the rule. Status says so; the lapse is the existing behaviour for any re-import change.
- [`calendar.addresses` is absent] → The subject is matched only by their URI, which is rarely a `mailto:`. Their attendee entry then appears as a separate party, and the subject is added as `tentative` alongside it. Validation reports a workspace with `defaults.subject` set and no `calendar.addresses` at info level once imported commitments exist, so the person knows to set it.
- [A dentist booked by hand gets the one-party info] → It is `info`, the person may leave it, and adopting it for an intention silences it.
- [Adopting bypasses the candidate search] → It is always the person's act, recorded with `selector: person`, and consistency still checks it.
- [Older readers don't count a linked pair once] → They may report a clash between an adopted commitment and its intention. Status says to upgrade before adopting.

## Migration Plan

None required. Workspaces may add `calendar.addresses`. intentions-cli needs: the mapping and its configuration; an adopt operation; one-occupation counting; and the findings (four errors, one warning, two info: the one-party import and the missing `calendar.addresses`).

## Open Questions

None.
