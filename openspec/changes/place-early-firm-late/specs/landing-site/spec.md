## MODIFIED Requirements

### Requirement: The page carries the seven beats in order
After the hero, the page SHALL present, in this order: "One plan, two fates"; "Whose calendar is it?"; "It ranks. It flags. It never chooses." including a before / the moment / after composition diagram that links to particulars.fyi and shows the return path from DKF to intentions; a proof section; "Start in your terminal"; and a footer.

#### Scenario: The headings are listed
- **WHEN** the `<h2>` elements are read in document order
- **THEN** they match the five section titles above in that order

#### Scenario: The composition diagram is followed
- **WHEN** the DKF element of the composition diagram or its caption link is activated
- **THEN** the browser lands on particulars.fyi

#### Scenario: The composition diagram shows the loop
- **WHEN** the composition diagram is read
- **THEN** an arrow runs from the DKF box back to the intentions box, labelled to say that the retrospective record is what makes a terminus held
