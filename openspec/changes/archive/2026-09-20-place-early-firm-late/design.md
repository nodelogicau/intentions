## Context

Three conclusions were reached in the knowledge workspace on 2026-09-19 and 20 and folded into the spine: the terminus-as-noun convention (Bryan, Walton, Rogers and Dweck 2011; Oyserman's identity-based motivation; Fujita, Trope, Liberman and Levin-Sagi 2006), the place-early-firm-late reconciliation of "the slot comes last" with plan-making (Masicampo and Baumeister 2011; Gollwitzer 1999; Gollwitzer and Sheeran 2006), and the DKF return arrow (Bem 1972). Each is prose, not machinery: the format already has separate placement and stability axes, a `reference` field on termini, and DKF citation by id and version. Nothing here changes a field, a projection, or what any act may do.

## Goals / Non-Goals

**Goals:**
- The README says what the workspace believes, in the three places a reader would look.
- The site's two captions stop overstating.
- The specs carry the one recommendation that is checkable (noun-form termini) and the one page requirement that is checkable (the return arrow).
- Sources cited at the level of trust they deserve.

**Non-Goals:**
- Any schema change. No new field, no validation error for a verb-form terminus.
- A harness nudge toward early placement. Placing remains a recorded act of the person or a policy they hold.
- Changing `unresolved` or any CLI behaviour; the CLI change for `init` is an upstream issue.
- Citing ego depletion. The resource model failed replication and is not relied on.

## Decisions

**Noun-form termini are SHOULD, not SHALL.** The finding is about wording, and a verb-form terminus is not malformed. Validation stays silent. The spec says SHOULD, the README says it as a principle, and the conventions file says it as advice a harness will read. A future info-level validation note is possible but not proposed.

**The Design Principle is reworded, not replaced.** "The window is the person's, not the clock's" is still the principle. Its body changes from *when* the collapse happens to *what is lost* if it happens wrongly: the window's precision and the intention's reason. A sentence is added: placement is relief and may be taken early; stability is commitment and is what comes last. The Approach sentence "never flattened to clock time until it must be" becomes "kept as the person expressed it, and collapsed to a slot without losing it", or equivalent, so the two passages agree.

**The hero caption gains one word.** "The firm slot comes last." keeps the rhythm and is exactly the synthesis. The two-fates diagram and its caption already describe the invented, reasonless block, so they stand.

**The return arrow is drawn on both diagrams the same way.** In the README's ASCII composition diagram, a line from the DKF claim back to `INTENTION.reference`. On the site, a curved edge from the DKF box beneath the row back to the intentions box, labelled "the record makes the terminus held". The SVG desc and figcaption say it in a sentence. The `landing-site` requirement adds one scenario: the diagram shows an arrow from DKF back to intentions.

**References grow by two groups.** "Psychological sources" for the identity and construal findings and for plan-making, kept separate from "Philosophical sources" so a reader can see which claims rest on experiment and which on phenomenology. Each entry names the finding it supports.

**Sequence.** README first, then the specs, then the site, then validate the page against the README as the `landing-site` spec requires.

## Risks / Trade-offs

- [The reworded principle reads as licence to slot everything immediately] → The paragraph says placement is *tentative* relief and that the invented, reasonless block is still the error. The two-fates section on the site still shows that block as the bad case.
- [SHOULD on wording invites bikeshedding of terminus titles] → The spec gives the two-word test: a person, not a task. Nothing enforces it.
- [Citing psychology in a format specification] → Kept to References and one Design Principles sentence each, at the same weight as Bratman and Searle already carry.
- [The site's composition diagram gets busy] → One extra edge below the row, no new box.

## Migration Plan

Prose only. Merge, push, Pages rebuilds. Archive with sync so the two deltas land. Then one follow-up synthesis in the knowledge workspace closing the "three edits are implied but not made" item.

## Open Questions

- Whether `unresolved` should be described in the README as the inventory of intentions still carried without a plan. It is a CLI verb, not a format object, so probably the CLI README's job.
