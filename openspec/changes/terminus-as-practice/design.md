## Context

`place-early-firm-late` (archived 2026-09-20) added the noun convention for termini. The spec made it a SHOULD, the README made it a Design Principle, and the `intentions.md` section made it a convention, citing Bryan et al. (2011) and Oyserman (2009). The convention is prose only: validation has never read a terminus's wording. This change replaces the convention and its rationale. It changes no field, projection, act or finding.

## Goals / Non-Goals

**Goals:**
- Every place that tells a reader or a harness how to title a terminus says the same thing: a practice the person chooses to keep up.
- A test a harness can apply mechanically: could this ever be done?
- A rationale that rests on sources that hold.

**Non-Goals:**
- Validation of wording, at any level. The SHALL NOT stays.
- Renaming anything structural. "Terminus", "standing intention" and `for-the-sake-of` are unchanged.
- Rewriting existing user workspaces. Old identity-form titles stay valid, and retitling is the person's choice.
- Reopening the policy half of the terminus definition. A policy's title is unaffected.

## Decisions

**The test is whether the thing can be finished, not whether the title is a noun or a verb.** Simply flipping to "verbs, not nouns" would let *follow through* (an imperative, a task) pass. The structural fact is that a terminus has no window and no duration, so nothing about it can be finished. Aristotle's split between activity that is never done and movement that ends when it is done (*Metaphysics* Θ.6) names exactly that. A gerund practice ("following through", "keeping my word to the board") passes the test. A task ("follow through on the pack") and an outcome ("a finished thesis") fail it. Alternative considered: keep the self and call it a project ("becoming someone who…"). Rejected because it is clunky, still reads as a property one will have, and doesn't give a sharper test.

**Identity form is advised against explicitly, not only by omission.** Most existing termini, including the example workspace's, use "being someone who…", so the spec names that form in its own scenario. Then a skill or conventions file can recognise it and suggest the practice form, the same way it treated the task form before.

**Sartre is cited for the reason, not for the mechanism.** Bad faith (*Being and Nothingness*, Part One, ch. 2) is why the old wording is wrong. The fundamental project (Part Four) and "man is nothing else but what he makes of himself" (*Existentialism Is a Humanism*) are why a practice is right. The README also notes that firming by the person's own act, supersession and splitting already treat a terminus as chosen and re-choosable. The wording now matches the machinery.

**Heidegger stays.** The for-the-sake-of-which is a possibility of Dasein's being, a way of going on rather than a fixed property, so a practice reads it at least as faithfully as the noun form did. The Purpose sections and the serves-graph vocabulary are untouched.

**Psychology is trimmed, not replaced.** Bryan et al. and Oyserman are removed. The README no longer claims that wording makes action more reliable, so nothing needs a new experimental citation. Fujita et al. still supports reading the chain at the level of what it is for. Bem still supports the DKF return path, rephrased from "infers who they are" to "sees what they keep choosing from what they did". Before the README mentions the failed replication, check the source (Gerber, Huber, Biggers and Hendry, *PNAS* 2016). Otherwise just drop the claim without commentary.

**The DKF loop survives the reframe.** A referenced claim becomes "I keep my word", which is a claim about a practice, and episodes are still its evidence. Only the object-model scenario name carried "identity".

**Example wording.**

| Was | Becomes |
|---|---|
| being someone who follows through | following through |
| being someone the board can rely on | keeping my word to the board |
| being someone who looks after their health | looking after my health |
| being someone who is strong in old age | staying strong into old age |
| being someone with a calm mind | keeping a calm mind |

The person writes their own termini in their own voice, so the examples use first person where a person is implied.

**Sequence.** Specs first, then the README, then the site, then the example and its script, then validation.

## Risks / Trade-offs

- [A practice-form terminus is mistaken for a recurring intention] → The README says the difference: a recurring intention has a cadence and generates instances, and a terminus has neither and is never placed. "Following through" isn't something you do on Tuesdays.
- [The reversal reads as churn two months after the convention was set] → The proposal records why. The knowledge workspace gets an antithesis, so the trail shows the earlier conclusion and its supersession.
- [Philosophy cited more heavily than before] → One principle paragraph and two References entries. That's the same weight Heidegger, Bratman and Searle already carry.
- [Existing workspaces carry identity-form titles] → They stay valid. A skill may suggest a retitle, and that is the person's act.

## Migration Plan

Prose only. Merge, push, let Pages rebuild. Archive with sync so both deltas land. Then: an issue on intentions-cli for the `init` template, an update to the `intentions` skill's terminus guidance, and an antithesis in the knowledge workspace.

## Open Questions

- Should the split-terminus prose ("one self is often found to be two") become "one practice is often found to be two"? Proposed: yes. "Self" goes wherever it means a terminus.
