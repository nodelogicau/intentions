## Why

The knowledge workspace's current synthesis records three conclusions from the launch of intentions.fyi that the specification and the site do not yet say: a terminus is phrased as who the person is, not what they do; the format forbids losing a window's meaning, not taking a placement early, so the *firm* slot is what comes last; and the relationship with DKF is a loop, because retrospective claims are what make a terminus's self-claim held. The README's Design Principles and the site's hero caption currently overstate the second point ("The slot comes last"), and the psychology that supports the first (Bryan et al., Oyserman, Fujita et al.) and second (Masicampo and Baumeister, Gollwitzer) is uncited. This closes the gap before v0.1 is declared.

## What Changes

- **Termini are nouns.** A Design Principles paragraph stating the convention; the same convention recommended for the workspace's `intentions.md`; the `intention` spec's Terminus requirement gains a SHOULD on the noun form and a scenario. Three psychological sources join References.
- **Place early, firm late.** The Design Principle "The window is the person's, not the clock's" is reworded: what the format forbids is losing what was said and why, not placing early; placement is relief, stability is commitment, a tentative placement is a legal and expected state. The Approach sentence is made consistent. The site's hero caption becomes "The firm slot comes last." Two sources join References. No requirement changes: WINDOW is still stored as written and placement is still the single collapse to clock time.
- **The DKF return arrow.** The README's composition diagram and prose gain the return path: retrospective DKF claims citing fulfilled intentions are the evidence that makes a terminus's referenced self-claim held rather than aspirational. The site's composition diagram gains the same arrow, and the `landing-site` spec requires it.
- One upstream issue on intentions-cli, so that `init` writes the terminus convention into the `intentions.md` it generates. Not part of this change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: the Terminus requirement recommends the noun form and adds a scenario.
- `landing-site`: the composition diagram requirement gains the return arrow from DKF to the intentions box.

## Impact

- README: Approach, Design Principles (one paragraph reworded, one added), the serves-graph diagram's terminus note, Composition by reference (diagram and prose), the `intentions.md` section, References.
- `docs/index.html`: the hero figcaption, the composition SVG (one arrow, one label, the desc, the figcaption). The page still names no field, value or flag kind. The figure script is untouched.
- Two spec deltas; all eight specs must validate after sync.
- The knowledge workspace's current synthesis lists these three edits as unresolved; a short follow-up synthesis after archive closes that item.
