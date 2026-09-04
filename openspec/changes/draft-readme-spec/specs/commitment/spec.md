## MODIFIED Requirements

### Requirement: Commitment fields

A COMMITMENT SHALL carry, in canonical order: `id`; `parties` (a list of `{uri, status}` where `status` is one of `tentative`, `accepted`, `declined`); `placement`; optional `intention` (the id of the intention it fulfils); `origin` (one of `resolution` with the resolution id, or `import`); optional `external` (`{system: icalendar|jscalendar, uid}`); optional `title` and `description`; `source`; `timestamp`; `acknowledgements`; and at most one `retired` record.

The scheduling projection of a COMMITMENT SHALL be: `parties`, `placement`, `intention`, `origin`, `external`, `retired.kind`.

#### Scenario: Commitment from resolution
- **WHEN** a multi-party intention is resolved
- **THEN** a commitment is created with `origin: {resolution: res_...}`, `intention: int_...`, every party at `tentative`, `source` recording who performed the selection, and no `external`

#### Scenario: Imported commitment source
- **WHEN** an iCalendar event is imported by a harness on the workspace owner's behalf
- **THEN** the commitment's `source` carries the owner as `author` and the harness as `harness`, and `origin` is `import`

### Requirement: Cancellation

A commitment SHALL be cancelled by appending a `retired` record with `kind: cancelled`, which is terminal. `cancelled` SHALL be the only retirement kind for a commitment. Cancelling a commitment SHALL NOT retire its intention; the intention's placement SHALL be cleared so it may be re-resolved.

#### Scenario: Cancel and re-resolve
- **WHEN** a commitment created from int_A is cancelled
- **THEN** int_A loses its placement, keeps its window, and is eligible for resolution again

#### Scenario: Cancellation carries a reason
- **WHEN** a commitment is cancelled with a `reason`
- **THEN** the `retired` record carries the reason, a timestamp, and the source of the cancelling act
