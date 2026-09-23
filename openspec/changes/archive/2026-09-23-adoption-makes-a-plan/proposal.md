## Why

Adopting a bare desire bare produces a terminus (nodelogicau/intentions #28). A desire's `serves` may be empty and `desire_adopt` takes `duration` and `window` as optional, so `desire_adopt{id}` on "call the accountant" writes an intention with no `serves`, no `window` and no `duration`, which the format defines as a terminus: a self titled as an errand, reported only as a draft, that the person is then asked to firm. Adoption is the rung from want to plan; this path steps sideways from a want to a self. The grounding rule will never catch it, because a terminus is exempt from grounding, so the only thing that ever closes the path is a refusal on adoption itself.

## What Changes

- **Adoption is refused where it would write a terminus**: where the desire's `serves` is empty and the act supplies neither `duration` nor `window`. The refusal names what is missing. An adopted want is a plan; a self is declared, not adopted. `duration` and `window` stay optional on `desire_adopt`, since a desire that already serves a terminus may be adopted with either alone or with neither, into an intention with a why and not yet a when, which `unresolved` reports as incomplete.
- **The rule is stated as permanent.** A terminus is exempt from the grounding rule, so no later revision subsumes this refusal.
- **The asymmetry with `intention_add` is named as intended.** A harness may still draft a terminus through `intention_add` with a bare title, #26's draft self, because that act means "here is a self I am drafting" where `desire_adopt` means "this want is now a plan".
- **`desire_retire` refuses `kind: adopted`.** Only `desire_adopt` writes the intention the pointer must name.
- **`superseded_by` on a desire naming anything but a desire is a validation error.** The `desire` spec already requires it; the finding is now enumerated.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `desire`: the adoption requirement gains the refusal and its permanence; the retirement requirement says `adopted` is written only by adoption.
- `object-model`: Validation enumerates the `superseded_by` finding on a desire.
- `harness-tools`: `desire_adopt` refuses a bare adoption by name; `desire_retire` refuses `kind: adopted`.

## Impact

- README: the DESIRE section's adoption paragraph, the Validation section, the `desire_adopt` and `desire_retire` rows and the `desire_adopt` bullet in the Reference Tool Set. Three spec deltas.
- No workspace holds a desire yet; DESIRE is unimplemented in intentions-cli (#7 there), which is why this is settled now.
- intentions-cli #7 gains a comment with the three refinements; #28 closes.
- Knowledge workspace: one claim on the Desire particular and a qualification synthesis.
