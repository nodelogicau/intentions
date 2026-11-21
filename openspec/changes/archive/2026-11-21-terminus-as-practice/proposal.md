## Why

`place-early-firm-late` settled that a terminus is titled as who the person is, not what they do: *being someone who follows through*, never *follow through*. That wording treats the self as something a person is. Sartre calls this bad faith: holding oneself as a fixed thing, the waiter playing at being a waiter. A person is what they keep choosing to do, and they can always choose again. The format's machinery already works that way. A terminus is inert until the person firms it, only the person can firm it, and supersession lets them re-choose it. The wording is the only part that says otherwise. The empirical support is also weaker than the README claims: the noun-framing effect it cites (Bryan et al. 2011) didn't hold up in larger field studies. The convention should now name what the person chooses to keep doing.

## What Changes

- **Termini are practices.** A terminus that is not a policy is titled as an ongoing practice the person chooses to keep up: *following through*, *keeping my word to the board*. It isn't titled as an identity (*being someone who follows through*) or as a task (*follow through on the pack*).
- **A new test.** "Does the title name a person or a task?" becomes "could this ever be done?" A terminus has no window and no duration, so it is never finished. A title that could be finished names a task, and a title that names a property names an identity rather than a choice.
- **Rationale rewritten.** The README principle "A terminus is a person, not a task" becomes "A terminus is a practice, not a task", grounded in Sartre (bad faith, the fundamental project) and Aristotle (an activity that is never finished versus a movement that is finished when it ends). It says that firming, supersession and splitting are how the format keeps a terminus chosen. The harness's first question changes from "who is the person trying to be?" to "what does the person mean to keep doing, for its own sake?"
- **Sources.** Bryan et al. (2011) and Oyserman (2009) are removed from References. Sartre and Aristotle are added to the Philosophical sources. Fujita et al. (2006) and Bem (1972) stay, reworded where they refer to identity.
- **Examples retitled** across the README, site, example workspace and its generating script, including the split-terminus example. *Looking after my health* becomes *staying strong into old age* and *keeping a calm mind*.
- Validation does not change. Wording is never an error, and existing workspaces stay valid without edits. No version bump.
- Outside this change: an issue on intentions-cli so that `init` writes the new convention into `intentions.md`, an update to the `intentions` skill, and an antithesis in the knowledge workspace against the 2026-09-19/20 conclusion.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: the Terminus requirement says a terminus is titled as a practice, changes the test to "could this ever be done?", and replaces the "titled as a task" scenario with task and identity scenarios.
- `intention` (Retirement kinds): a terminus is never `fulfilled` because a practice is never finished; a split records one practice refined into several.
- `desire`: "a self is declared, not adopted" becomes "a terminus is declared, not adopted", and the scenario "Draft want, draft self" becomes "Draft want, draft terminus".
- `object-model`: the DKF composition scenario "Terminus points at a held identity claim" no longer says the referenced claim is about identity.

## Impact

- README: the Approach, the serves-graph prose and diagram, the split-terminus passage, the DKF loop paragraph, the `intentions.md` Termini convention, the Design Principles, and References.
- `docs/index.html`: the hero SVG terminus label and `desc`. The `landing-site` spec doesn't name the terminus wording, so it needs no delta.
- `docs/README.md` script and `docs/example`: the terminus title. A title is not in the projection, so versions and hashes don't move.
- Three spec deltas (`intention`, `desire`, `object-model`). All specs must validate after sync.
