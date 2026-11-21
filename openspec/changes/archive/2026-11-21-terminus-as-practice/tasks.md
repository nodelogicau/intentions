## 1. Specs

- [x] 1.1 Confirm the delta files resolve against the main specs with `openspec validate terminus-as-practice --strict`
- [x] 1.2 Extend the deltas to the other places where "self" means a terminus: `intention` Retirement kinds and the two `desire` requirements

## 2. README

- [x] 2.1 Approach (:65): the chain ends in a practice the person holds, not "a standing self-understanding about who the person is"
- [x] 2.2 Serves graph (:346) and its diagram (:1150): terminus example becomes *following through*; the diagram note's DKF claim is one Ada holds about what she keeps doing
- [x] 2.3 Split-terminus passage (:408-420): "one self is found to be two" becomes "one practice is found to be two", with the retitled examples from design.md
- [x] 2.4 DKF loop (:1270-1278): "makes the self-claim held" and "infers who they are" reworded to a claim about what the person keeps choosing
- [x] 2.5 `intentions.md` section (:1519-1522): the Termini convention says a terminus is titled as a practice the person chooses to keep doing, with the "could this ever be done?" test
- [x] 2.6 Design Principles (:1610-1619): "A terminus is a person, not a task" becomes "A terminus is a practice, not a task": the test, why identity wording is bad faith, and how firming, supersession and splitting keep a terminus chosen; drop the claim that identity framing is acted on more reliably
- [x] 2.7 Design Principles (:1621-1625): the harness's first question becomes what the person means to keep doing, for its own sake
- [x] 2.8 References: remove Bryan et al. and Oyserman; add Sartre (*Being and Nothingness*, bad faith and the fundamental project; *Existentialism Is a Humanism*) and Aristotle (*Metaphysics* Θ.6) to Philosophical sources; reword Bem; keep Fujita et al.
- [x] 2.9 Search the README for any remaining "who the person is", "who they are", "being someone" and "self" meaning a terminus, and fix each one

## 3. Site and example

- [x] 3.1 `docs/index.html` hero SVG: the terminus label becomes "keeping my word to the board" and the `desc` matches; check it fits the 260px box in both colour schemes and at phone width
- [x] 3.2 `docs/README.md` script and `docs/example` terminus YAML: retitle to "Keeping my word to the board"; confirm the projection hash and version are unchanged
- [x] 3.3 Read every changed sentence on the page against the README

## 4. Close out

- [x] 4.1 `openspec validate --all --strict` passes after sync
- [x] 4.2 Commit and push; confirm Pages rebuilds and the hero label changed
- [x] 4.3 Open an issue on intentions-cli: `init` writes the practice convention into the generated `intentions.md`
- [x] 4.4 Update the `intentions` skill's terminus guidance to the practice form and the new test
- [x] 4.5 Knowledge workspace: record an antithesis against the 2026-09-19/20 terminus-as-noun conclusion, citing this change
- [x] 4.6 Archive with sync so the `intention`, `desire` and `object-model` deltas land
