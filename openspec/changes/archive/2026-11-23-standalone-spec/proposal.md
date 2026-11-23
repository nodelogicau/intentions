## Why

Intentions should be implementable, and usable, without DKF or episodes, so that people can choose which formats they adopt. It already is in substance: it defines its own ids, field order, `source`, projection and validation, and nothing in it resolves a reference to another format. But the text doesn't say so, and in places it reads as if a sibling were needed:

- **It contradicts episodes.** Five passages say an episode may name an object here as its `occasion`. Episodes dropped `occasion` in its own `standalone-spec` change: an episode cites nothing, and an `occasion` key is now an unknown field.
- **`reference` is defined as a pointer to a DKF claim,** and the object-model spec admits "a URI or DKF id". It is the only field whose meaning names a sibling, and what it accepts leans on DKF's id grammar.
- **"Particular" is never defined here.** Fields say "URI of the particular whose intention this is", a term a reader can only learn from DKF.
- **Several rules are explained only by analogy with DKF** ("as DKF refuses a claim with no particular"), which a reader without DKF can't follow.
- **References calls DKF's conventions ones "this specification adopts"** and suggests reading DKF's README first, though every convention is restated here.
- **One requirement binds another format:** "Live prospective state SHALL never be represented as DKF claims".
- **There is no Conformance section** saying which text is normative.

Episodes settled the same question with a Conformance section and a `standalone-conformance` capability. This change does the same for intentions.

## What Changes

- **A Conformance section** after The Approach: BCP 14 keywords; which sections are normative (Core Object Types, Object Model except *Composition by reference*, Consistency, Versioning, File Layout; Reference Tool Set only for an implementation exposing a listed name); that the specification is complete on its own; and that text naming DKF or episodes is informative.
- **The `occasion` passages are corrected** in The Approach, the *Composition by reference* diagram and text, Design Principles, Status and References. Episodes and DKF point at objects here; this format points at neither; an episode names nothing.
- **`reference` becomes an informal pointer to any record outside this format,** as a URI or other string, never resolved. A DKF claim id is an example, not the definition. Every existing value stays valid.
- **"Particular" is defined in Core Object Types** as anything identified by a URI that an object is about or involves (a person, a room, a piece of equipment), with no registry required. The word is shared with DKF, but the definition here is this format's own.
- **The DKF analogies are restated in this format's own terms,** and kept as informative asides where they help a reader who knows DKF.
- **References describes DKF's conventions as copied by agreement and restated here in full.**
- **The rule about DKF claims is removed.** How DKF is used is DKF's business.
- **No format version.** No file is read differently and no file stops validating.

## Capabilities

### New Capabilities
- `standalone-conformance`: intentions is implementable from its own text: no field's value must be another format's identifier, subjects and parties need no registry, no rule constrains another format, and text about other formats is informative.

### Modified Capabilities
- `object-model`: *Composition with DKF by reference only* is generalised: `reference` is any URI or string, and the rule about representing state as DKF claims is removed.
- `intention`: *Intention fields* and *Terminus* define `reference` without naming DKF.
- `desire`: *DESIRE is the rung below intention* defines `reference` the same way.
- `consistency`: *Acknowledgement as retrospective seed* says a later record, such as a DKF claim, can be written from an acknowledgement, without requiring that record's format.

## Impact

- `README.md`: The Approach, a new Conformance section, Core Object Types (*particular*), the DESIRE and INTENTION field tables, the serves-graph prose and diagram, ACKNOWLEDGEMENT, *Composition by reference*, Design Principles, Status, References.
- `openspec/specs`: four requirements modified, one capability added.
- `intentions-cli`: no behaviour change. It never resolves `reference`. Help text that calls `reference` a DKF claim pointer may be reworded.
- `intentions.fyi`: no change required. Its composition diagram shows informative relations only.
