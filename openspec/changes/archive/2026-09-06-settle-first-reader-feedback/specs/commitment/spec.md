## MODIFIED Requirements

### Requirement: Commitment fields

A COMMITMENT SHALL carry, in canonical order: `id`; `version`; `parties` (a list of `{uri, status}` where `status` is one of `tentative`, `accepted`, `declined`, sorted by `uri`); `placement`; optional `intention` (the id of the intention it fulfils); `origin` (one of `resolution` with the resolution id, or `import`); optional `transparent` (a boolean; absent means false; true means the commitment occupies none of the subject's time; a writer SHALL omit it when false); optional `external` (`{system: icalendar|jscalendar, uid}`); optional `title` and `description`; `source`; `timestamp`; `acknowledgements`; and at most one `retired` record.

The scheduling projection of a COMMITMENT SHALL be: `parties`, `placement`, `intention`, `origin`, `transparent`, `external`, `retired.kind`, with `transparent` present only when true.

#### Scenario: Commitment from resolution
- **WHEN** a multi-party intention is resolved
- **THEN** a commitment is created with `version` after `id`, `origin: {resolution: res_...}`, `intention: int_...`, every party at `tentative`, `source` recording who performed the selection, no `transparent`, and no `external`

#### Scenario: Imported commitment source
- **WHEN** an iCalendar event is imported by a harness on the workspace owner's behalf
- **THEN** the commitment's `source` carries the owner as `author` and the harness as `harness`, and `origin` is `import`

#### Scenario: Transparency changes the version
- **WHEN** an imported commitment's `transparent` changes from absent to true on re-import
- **THEN** its projection hash changes and any acknowledgement naming it as counterpart lapses

#### Scenario: Explicit false is absent
- **WHEN** a file arrives carrying `transparent: false`
- **THEN** it hashes identically to the same file without the field, and a writer touching it drops the field
