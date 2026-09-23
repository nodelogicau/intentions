## MODIFIED Requirements

### Requirement: Timestamps

Every object and record SHALL carry a `timestamp`: the assertion time as an RFC 3339 UTC datetime with seconds. On a record it is the time of the act. On an object it is the time of the object's last write: each edit is a new assertion, and the history is git's. Creation time is carried by the id. The timestamp MAY precede the minting instant embedded in the id, and consumers MUST NOT require the two to agree. `timestamp` SHALL be excluded from every scheduling projection.

#### Scenario: Backdated availability
- **WHEN** an availability learned from a conversation last week is recorded today with last week's `timestamp`
- **THEN** the file is valid and its default validity horizon is measured from last week

#### Scenario: Timestamp correction does not change version
- **WHEN** only an object's `timestamp` is corrected
- **THEN** its version is unchanged

#### Scenario: Edit updates the timestamp
- **WHEN** an intention's window is edited
- **THEN** its `timestamp` is the time of that edit and its version changes for the window, not for the timestamp

### Requirement: Source attribution

Every object and record SHALL carry a `source` block with fields `author` (a URI or name identifying the person on whose behalf the object was written), `harness` (the agent harness that wrote it, if any), and `model` (the model identifier, if any). `author` SHALL be required on INTENTION and AVAILABILITY. `harness` alone SHALL be sufficient on RESOLUTION, ACKNOWLEDGEMENT, and retirement records only when `author` is also present on the object they concern. A writer SHALL apply the workspace default `source.author` from `intentions.yaml` when the caller omits it. `source` SHALL be excluded from every scheduling projection.

#### Scenario: Harness drafts an intention
- **WHEN** a harness writes an intention on a person's behalf with the workspace default author
- **THEN** the file carries `source.author` set to that person and `source.harness` set to the harness, and both are visible in the diff

#### Scenario: Intention without author
- **WHEN** an intention is written with `source.harness` but no `source.author` and no workspace default
- **THEN** the write is refused and validation reports an error

#### Scenario: Attribution correction does not lapse acknowledgements
- **WHEN** an object's `source.author` is corrected after a counterpart acknowledged a flag against it
- **THEN** its version is unchanged and the acknowledgement remains in force

The person's own act is recorded by two conventions, one per kind of file. On a live object, the absence of an authorising policy means the person acted: `firmed_under` is absent when the person firmed. On a record, the actor SHALL always be written, `selector: person` when the person selected, because a record is read on its own and absence there would be silence.

#### Scenario: Person's act on an object and on a record
- **WHEN** a person firms an intention and then selects a candidate for it
- **THEN** the intention carries no `firmed_under` and the resolution record carries `selector: person`
