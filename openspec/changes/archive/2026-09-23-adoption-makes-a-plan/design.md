## Context

`add-desire` defined adoption as writing an intention from the desire plus "the duration and window the adopting act supplies", both optional, and left `serves` on a desire optional. Together those admit an adoption whose result has none of `serves`, `window` or `duration`, which is the definition of a terminus. #26 made a terminus the person's word and exempted it from the grounding rule; #27 made it inert until firm. Neither rule reaches an intention that is a terminus by shape, so the errand-terminus is reported only as a draft.

## Goals / Non-Goals

**Goals:**
- Adoption can only produce a plan, never a self.
- No new restriction on what a plan may lack: a why without a when is still admitted.
- The rule survives future editing, by saying why it cannot be subsumed.

**Non-Goals:**
- Requiring a duration or window on adoption. That would make `desire_adopt` stricter than `intention_add`.
- Stopping a harness from drafting a terminus through `intention_add`. That is #26's deliberate path.

## Decisions

**Refuse on the result's shape, not on the inputs.** The condition is stated as "where the intention it would write is a terminus", then spelled out: empty `serves` and neither `duration` nor `window` supplied. Stating it by shape keeps it correct if a terminus's definition ever gains a clause, and it names the thing the format actually objects to.

**The refusal names what is missing.** A harness that hits it should be able to ask the person one of two questions: what is this for, or when. The message lists both.

**Say it is permanent.** One sentence: a terminus is exempt from the grounding rule because it is the ground, so no later refusal of unserved intentions closes this path. Without it the rule looks like a transitional duplicate of #26 and gets deleted.

**Name the asymmetry.** `intention_add` with a bare title drafts a self, visible and inert, by design. `desire_adopt` says a want is now a plan. Same shape, different act. One sentence in the adoption paragraph.

**`adopted` is written only by adoption.** `desire_retire` refuses `kind: adopted` because the retirement's pointer must name an intention that adoption wrote; a hand-written `adopted_as` is a forgery of the trail. The same requirement gains the `superseded_by` finding, since it was stated and not enumerated.

## Risks / Trade-offs

- [A harness works around the refusal by adopting with a throwaway window] → The result is then a plan with a when and no why, unserved, and the person is asked for the why. That is the intended path, not a workaround.
- [The refusal message is chatty] → Two short options; the alternative is a harness guessing which to ask.

## Migration Plan

Prose and three deltas; nothing to migrate. Archive with sync, comment on intentions-cli #7, close #28, one claim and a synthesis in the knowledge workspace.

## Open Questions

None.
