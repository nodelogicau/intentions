## ADDED Requirements

### Requirement: The second-reader account agrees with the implementation's record
Where the proof section states how many issues the first implementation raised, how many are settled, how many were decided differently, and how many remain open, those counts SHALL equal the status table in intentions-cli's `SPEC-FEEDBACK.md` at the time of publication, and the section SHALL link to that file.

#### Scenario: The counts are tallied
- **WHEN** the rows of the feedback file's status table are counted by status
- **THEN** the page's counts of raised, settled, decided-differently and open issues match

#### Scenario: A new issue is recorded upstream
- **WHEN** a row is added to the feedback file after publication
- **THEN** the page is out of date until its next edit, and the pre-publication read against the README and the feedback file catches it
