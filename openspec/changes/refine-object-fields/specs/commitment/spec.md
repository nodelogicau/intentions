## MODIFIED Requirements

### Requirement: Commitment fields

A COMMITMENT SHALL carry, in canonical order: `id`; `version`; `parties` (a list of `{uri, status}` where `status` is one of `tentative`, `accepted`, `declined`, sorted by `uri`; a different shape from an intention's `parties`, which are bare URIs; `tentative` here is a party's answer in iCalendar's sense, tentatively accepted, not an intention's stability); `placement`; optional `intention` (the id of the intention it fulfils); `origin` (one of `resolution` or `import`); `resolution` (the id of the RESOLUTION record, present when and only when `origin` is `resolution`); optional `transparent` (a boolean; absent means false; true means the commitment occupies none of the subject's time; a writer SHALL omit it when false); optional `external` (`{system: icalendar|jscalendar, uid}`); optional `title` and `description`; `source`; `timestamp`; `acknowledgements`; and at most one `retired` record.

The scheduling projection of a COMMITMENT SHALL be: `parties`, `placement`, `intention`, `origin`, `resolution`, `transparent`, `external`, `retired.kind`, with `transparent` present only when true.

#### Scenario: Commitment from resolution
- **WHEN** a multi-party intention is resolved
- **THEN** a commitment is created with `version` after `id`, `origin: resolution`, `resolution: res_...`, `intention: int_...`, every party at `tentative`, `source` recording who performed the selection, no `transparent`, and no `external`

#### Scenario: Imported commitment source
- **WHEN** an iCalendar event is imported by a harness on the workspace owner's behalf
- **THEN** the commitment's `source` carries the owner as `author` and the harness as `harness`, and `origin` is `import`

#### Scenario: Transparency changes the version
- **WHEN** an imported commitment's `transparent` changes from absent to true on re-import
- **THEN** its projection hash changes and any acknowledgement naming it as counterpart lapses

#### Scenario: Explicit false is absent
- **WHEN** a file arrives carrying `transparent: false`
- **THEN** it hashes identically to the same file without the field, and a writer touching it drops the field

#### Scenario: Resolution id without origin
- **WHEN** a commitment carries `resolution` while `origin` is `import`, or `origin: resolution` with no `resolution`
- **THEN** validation reports an error

### Requirement: Transparency arrives only by import

`transparent: true` SHALL be set only on a commitment whose `origin` is `import`. A commitment created by a resolution consumed supply to exist and is opaque by construction; a write that sets `transparent: true` on a commitment whose `origin` is a resolution SHALL be refused, and validation SHALL report it as an error.

#### Scenario: Resolution-born commitment cannot be transparent
- **WHEN** an edit sets `transparent: true` on a commitment with `origin: resolution`
- **THEN** the write is refused and validation reports an error

#### Scenario: Imported commitment may be transparent
- **WHEN** an imported commitment carries `transparent: true`
- **THEN** validation passes
