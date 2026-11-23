## ADDED Requirements

### Requirement: No field requires another format's identifier
The specification SHALL define no field whose value must be an identifier of an object defined by another format. `reference` SHALL be an informal pointer to any record outside this format, written as a URI or other string, and SHALL never be resolved by validation.

#### Scenario: Validating with no sibling workspace
- **WHEN** a validator checks an intentions workspace with no DKF or episodes workspace present
- **THEN** it can decide whether every object is valid without resolving any reference outside the workspace

#### Scenario: A reference to something that is not a DKF claim
- **WHEN** a terminus carries `reference: https://example.com/journal/2026-09-04`
- **THEN** the terminus is valid, and validation neither resolves nor reports the reference

#### Scenario: A DKF claim id
- **WHEN** a terminus carries `reference: clm_01a06d14-7e2c-7b19-a0d3-5c8f2e4a6b91`
- **THEN** the terminus is valid, and validation neither resolves nor reports the reference

### Requirement: Particulars are defined without another format's object model
The specification SHALL define a particular as anything identified by a URI that an object is about or involves, such as a person, a room or a piece of equipment. It SHALL state that a particular need not exist in any registry or workspace, including a DKF workspace, and that resolving its URI is outside the format.

#### Scenario: Reading the definition
- **WHEN** an implementor reads the definitions of `subject` and `parties`
- **THEN** none of them requires knowing what a DKF particular is

#### Scenario: A subject no registry knows
- **WHEN** an intention's `subject` is a URI that resolves to nothing
- **THEN** the intention is valid

### Requirement: No rule constrains another format
The specification SHALL state no requirement on how another format is written, read or used. Where it describes how another format may relate to objects here, the description SHALL be informative.

#### Scenario: How DKF is used
- **WHEN** a reader looks for what this specification requires of a DKF workspace
- **THEN** they find no requirement, only informative description

### Requirement: Text about other formats is informative
The specification SHALL contain a Conformance section stating which sections are normative and that the specification is complete on its own. All text describing DKF, episodes or the family of formats SHALL be informative and SHALL place no requirement on an intentions implementation. A rule SHALL be stated in this format's own terms; a comparison with another format MAY follow it as an informative aside.

#### Scenario: Implementing intentions alone
- **WHEN** an implementor builds a writer, reader, resolver and validator from the normative sections only
- **THEN** the implementation conforms, with no DKF or episodes code, data or workspace

#### Scenario: A sibling format is mentioned in a normative section
- **WHEN** a normative section mentions DKF or episodes
- **THEN** the mention is marked informative, or is an example of a value the section already defines in its own terms

#### Scenario: Relations to episodes
- **WHEN** a reader reads how intentions relates to episodes
- **THEN** nothing in it says that an episode names an object here, or that this format cites episodes
