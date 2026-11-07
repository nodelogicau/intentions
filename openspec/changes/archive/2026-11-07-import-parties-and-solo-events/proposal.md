## Why

Import is the only way a commitment arrives from outside, and two things about it are unspecified (issue #35).

First, how an event's participants become `parties`. Two origins says an imported commitment is created "with all parties as the import states them", and External reference only says attendee metadata doesn't cross. Neither says which properties become `parties`, how `PARTSTAT` becomes `status`, or how the person's own entry is found. Two importers can produce different `parties`, and so different versions, from the same event.

Second, the solo event. An event with no other attendee, such as a concert ticket, a gym block, or a dentist appointment entered by hand, imports as a commitment whose only party is the subject. A commitment is meant to be directed at someone. When the person also plans that occasion as an intention, the two clash, and #34's hold link can't join them: a harness treats an intention's `external` as a hold it wrote, so it would rewrite or release the venue's event.

## What Changes

- **Parties on import are mapped by rule.**
  - Each iCalendar `ATTENDEE` and the `ORGANIZER`, or each JSCalendar participant with a calendar address, becomes one party. Its URI is the calendar address, or the subject's URI where the address is one of the subject's.
  - `PARTSTAT` / `participationStatus` becomes `status`: `ACCEPTED` → `accepted`, `DECLINED` and `DELEGATED` → `declined`, `TENTATIVE`, `NEEDS-ACTION` or absent → `tentative`.
  - Non-participants (`ROLE=NON-PARTICIPANT`, JSCalendar `informational` only) don't become parties.
  - Only the address and the status cross; the rest of the attendee metadata still doesn't.
- **The subject's own entry comes from the event.**
  - If the subject is an attendee, their `PARTSTAT` is used.
  - If they are the organizer with no attendee entry, or the event names no one, their status is `accepted`: the event is in their own calendar by their own act.
  - If the event names others but not the subject, their status is `tentative`.
  - The subject is always a party.
- **Calendar addresses are declared.** `intentions.yaml` may declare `calendar.addresses`, mapping a subject URI to the calendar addresses that identify that particular in imported events, so every importer finds the same entry.
- **Re-import applies the same mapping.** A changed `PARTSTAT` is that party's act as it reached the calendar.
- **A one-party import is reported at info level.** An unretired imported commitment whose only party is the subject is reported as a commitment directed at no one, which may be better recorded as an intention. It is still imported as now, and nothing moves.
- **An imported commitment may fulfil an intention.** A person may *adopt* an unretired imported commitment for an intention of its subject that has no `parties`. Adopting is a selection: it writes a RESOLUTION record with `selector: person`, gives the intention the commitment's placement, and sets the commitment's `intention`. The calendar event stays the venue's, and the link survives re-import. Afterwards:
  - If the event later moves, validation warns that the placements differ.
  - Cancelling the commitment clears the intention's placement, as for any commitment.
- **A commitment and the intention it fulfils are one occupation.** They are never reported as clashing with each other, and they consume the subject's capacity once. This is already true of a resolution's commitment but was never stated, and adopting relies on it.
- **New validation findings.**
  - Errors:
    - an imported commitment naming an intention whose subject is not one of its parties;
    - an imported commitment naming an intention with `parties`;
    - an imported commitment naming an intention that carries `external`;
    - two unretired commitments naming one intention.
  - Warning: an imported commitment whose `placement` differs from its intention's.
  - Info: the one-party import, and a workspace with imported commitments but no `calendar.addresses`.

### Non-goals

- Importing a solo event as an intention. Import still never creates an intention or an availability.
- Making "directed at another party" a requirement on every commitment. The info finding names the case; it doesn't forbid it.
- iTIP negotiation, delegation chains, and `SENT-BY`, which stay in the external system.
- Adopting automatically or under a policy. Saying an event fulfils an intention is the person's judgement.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `commitment`:
  - Two origins states the party mapping.
  - New requirements: Parties on import, and Adopting an imported commitment.
  - External reference only says that address and status cross.
- `resolution`: Selection is a recorded act gains adopting as a kind of selection.
- `consistency`: new requirement, A commitment and the intention it fulfils are one occupation.
- `object-model`:
  - Workspace configuration gains `calendar.addresses`.
  - Validation gains four errors, a warning, and two info findings.

## Impact

- README: the COMMITMENT field table (`intention` is no longer "absent on imports"), Two origins, External reference only, a new paragraph on adopting, Consistency, Workspace configuration, Validation, and Status.
- Lands within `intentions/0.2` (and applies under 0.1). No projection changes, so no format version is needed. A re-import under the stated mapping may give an existing imported commitment different `parties`, and so a new version, where an importer had guessed differently. That lapses acknowledgements on it, as any re-import change does.
- intentions-cli needs:
  - the mapping and `calendar.addresses`;
  - an adopt operation;
  - capacity counted once for a commitment and its intention;
  - the six new findings.
- Closes issue #35.
