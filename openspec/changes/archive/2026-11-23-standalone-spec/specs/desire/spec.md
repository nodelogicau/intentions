## MODIFIED Requirements

### Requirement: DESIRE is the rung below intention
A DESIRE is a want the person has expressed and not yet committed to: a world-to-mind pro-attitude, not a commissive act. A workspace MAY hold desires in `/desires/`, one per file, with ids prefixed `des_`. A DESIRE SHALL carry, in canonical order: `id`; `version`; `subject` (the URI of the particular whose desire this is, applied from `defaults.subject` as for an intention); `title` (prose); `description` (prose, optional); `activity` (optional, a term from the workspace's activity vocabulary); `location` (optional, URIs); `parties` (optional, URIs of other particulars the want involves, kept as a hint); `serves` (possibly empty); `reference` (optional, an informal pointer to any record outside this format, as a URI or other string; never resolved); `source`; `timestamp`; and `retired` when retired. A DESIRE SHALL NOT carry `duration`, `window`, `stability`, `cadence`, `auto_select`, `auto_firm`, `firmed_under`, `placement`, or `acknowledgements`, and validation SHALL report an error if it does. A DESIRE SHALL NOT carry a strength, priority, or ranking field.

#### Scenario: A passing remark
- **WHEN** a harness records "call the accountant" as a DESIRE with a title, the workspace's default subject, and an empty `serves`
- **THEN** the write is accepted and validation reports nothing about it

#### Scenario: A desire with a window
- **WHEN** a DESIRE file carries `window`
- **THEN** validation reports an error naming the field
