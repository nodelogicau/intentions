# Landing Site

## Purpose

Defines what intentions.fyi is built from and what it asserts. The site is a visual introduction for practitioners, not the specification: the README is the specification, and the page states nothing it does not. Its constraints are those of particulars.fyi, so the two sibling sites are maintained the same way: one hand-written file, no build, no script, no request to another origin, and a proof figure regenerable from real output.

## Requirements

### Requirement: The site is one static file with no build and no external request
The site SHALL consist of a single hand-written `docs/index.html`, served by GitHub Pages from `docs/` on `main`. The file SHALL contain no `<script>` element and SHALL reference no resource on any other origin: no external stylesheet, font, image, or `@import`. All diagrams SHALL be inline SVG.

#### Scenario: The page is loaded
- **WHEN** `index.html` is opened in a browser with the network inspector recording
- **THEN** exactly one request is made, for the document itself, and no script executes

#### Scenario: A reviewer checks the source
- **WHEN** the file is searched for `<script`, `<link rel="stylesheet"`, `src="http`, `href="http` inside `<link>`, and `@import`
- **THEN** none is found

### Requirement: The custom domain is declared in the repository
`docs/CNAME` SHALL contain exactly `intentions.fyi`, and `docs/README.md` SHALL record the Pages settings and the DNS records needed to serve it.

#### Scenario: Pages is configured from the repository
- **WHEN** Pages is set to deploy `main` from `/docs`
- **THEN** GitHub reads the custom domain from `docs/CNAME` without it being typed into settings

### Requirement: The page renders in both colour schemes
Colours SHALL be defined as CSS custom properties on `:root`, redefined under `prefers-color-scheme: dark`, and every SVG SHALL take its fills and strokes from those properties.

#### Scenario: The system theme changes
- **WHEN** the operating system switches between light and dark
- **THEN** the page, including every diagram, re-renders legibly with no hard-coded colour remaining from the other scheme

### Requirement: The hero states the headline and the two calls to action
The hero SHALL carry the eyebrow "Intentions · an open planning format", the headline "Every hour is for something.", a lead paragraph, a primary call to action linking to the start section, and a secondary call to action linking to the specification README on GitHub. A muted line beneath the hero diagram SHALL credit the source of the headline; no heading on the page SHALL name a philosopher.

#### Scenario: A reader arrives
- **WHEN** the page loads at the top
- **THEN** the headline, lead, both calls to action and the slot-against-triad diagram are visible without scrolling on a desktop viewport

#### Scenario: A reader follows the second call to action
- **WHEN** "Read the spec" is activated
- **THEN** the browser lands on the README of `github.com/nodelogicau/intentions`

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

### Requirement: The page says nothing the specification does not
Every claim the page makes about the format SHALL be true of the README on `main` at the time of publication. The page SHALL NOT name a field, a vocabulary value, or a flag kind, so that a rename in the specification cannot falsify it.

#### Scenario: The page is checked against the README
- **WHEN** each sentence of the page's prose is read against the README's Problem, Approach and Status sections
- **THEN** no sentence asserts something those sections do not

#### Scenario: A field is renamed in the specification
- **WHEN** any field or vocabulary value changes name in a later change
- **THEN** no edit to the page is required for it to remain true

### Requirement: The proof figure is drawn from real output and can be regenerated
The proof section SHALL contain a figure rendered from the actual `--json` output of a released intentions-cli binary run against an example workspace committed under `docs/example/`. A script under `docs/` SHALL regenerate the figure's SVG in place between marker comments, and `docs/README.md` SHALL record the exact command. The figure's caption SHALL name the CLI version it was drawn from.

#### Scenario: The figure is regenerated
- **WHEN** the documented command is run against the committed example workspace with the named CLI version
- **THEN** the SVG between the markers is byte-identical to the committed one

#### Scenario: The example workspace changes
- **WHEN** an object in `docs/example/` is edited and the command is re-run
- **THEN** the figure changes to match and nothing outside the markers is touched

### Requirement: The footer's licence statement agrees with the repository
The footer SHALL state that the specification is released under CC0 and the CLI under the MIT License, and this SHALL match the `LICENSE` file in this repository and the `LICENSE` file in intentions-cli.

#### Scenario: The licences are compared
- **WHEN** the footer, this repository's `LICENSE`, and intentions-cli's `LICENSE` are read together
- **THEN** all three agree

### Requirement: The README points at the site and states the licence
`README.md` SHALL carry, near the title, a one-line pointer to intentions.fyi described as a visual introduction, and its License section SHALL state that the specification is released under CC0 1.0 Universal and reference implementations under the MIT License.

#### Scenario: A reader opens the README
- **WHEN** the first screen of the README is read
- **THEN** the pointer to intentions.fyi is visible

#### Scenario: The License section is read
- **WHEN** the License section is read
- **THEN** it no longer says `TBD.` and its wording agrees with the site footer
