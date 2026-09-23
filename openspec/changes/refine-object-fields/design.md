## Context

The review compared DESIRE, INTENTION, AVAILABILITY, COMMITMENT, the three records, the embedded values and the workspace config. Most asymmetries are deliberate and were left alone: `subject` defaulted on some objects and required on availability, `scope` on availability only, no `subject` on a commitment, required-but-empty lists. Five were not deliberate, or were deliberate but unstated.

## Goals / Non-Goals

**Goals:**
- No field with two shapes under one name goes unstated.
- No union-typed field.
- Every convention a second implementer would have to infer is written down.

**Non-Goals:**
- The two renames the review floated, `duration` to `capacity` on availability and `conditional` to `activity`. Both break files for a naming gain, and they deserve their own decision.
- Consolidating `superseded_by` and `adopted_as`, or `auto_select` and `auto_firm`. Both are fine as they are.

## Decisions

**`origin` is a string and `resolution` is its own field.** The alternative, keeping the mapping and making `import` a mapping too (`{import: {}}`), keeps the union's awkwardness in a different place. A string plus a conditional sibling is the shape every other conditional field in the format already has (`superseded_by` with `superseded`, `adopted_as` with `adopted`). `resolution` joins the projection because `origin` was in it and the record id is what the value carried.

**State the person's-act convention rather than change a field.** Making `firmed_under` explicit (`firmed_under: person`) reads wrongly and adds a sentinel to a provenance field that is deliberately absent when nothing authorised. Making `selector` absent for the person makes a record silent about the one thing it exists to say. The two are right for different reasons, and the reason is the rule: a live object is read in its workspace, where absence means the person; a record is read on its own, so the actor is always written.

**`parties` on a DESIRE is a hint like the other two.** URIs, outside the projection, copied onto the intention on adoption, where they become real. Nothing checks a desire's parties.

**`timestamp` is last write.** The other reading, creation time, is derivable from the id's minting instant, so it would carry nothing. Last write is what a reader wants when asking whether the file reflects a recent conversation. Records are unchanged: the time of the act.

**The `parties` sentence goes on both rows.** A reader of either table should meet it.

## Risks / Trade-offs

- [Breaking commitment files before v0.1] → Nothing is declared yet, no workspace outside the maintainer's holds resolution-born commitments, and the CLI is the only writer.
- [`timestamp` now changes on every edit, so two writers editing the same object produce different files] → They already do, since `timestamp` was never in the projection and the version is what two writers must agree on.

## Migration Plan

Prose and four deltas. Archive with sync. Issue on intentions-cli covering `origin`, `resolution`, `parties` on desires, and `timestamp` on edit. Knowledge workspace: one claim and a synthesis.

## Open Questions

- Whether to take the two renames in a separate change before v0.1. Recommend deciding before the declaration, since they are the only remaining file-breaking naming questions.
