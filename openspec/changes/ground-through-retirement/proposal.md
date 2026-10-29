## Why

The grounding rule says an intention reaches a firm terminus "by any path" of `serves` references, but never says what happens at a retired link (issue #31). The spec already depends on an answer without stating it. Ending a recurring intention leaves its pending instances "to be retired individually", which only works if the walk passes through the retired recurring intention. Otherwise, under 0.2, every pending instance becomes an error the moment the arrangement ends.

Termini need their own rule. A terminus is structural more than assertive: it is what the serves graph hangs from. Retiring one that nothing rests on is harmless, but retiring one that active intentions rest on pulls the ground out from under them. Today any terminus may be retired as any kind, by anyone, and the 0.2 write refusal is ambiguous about whether that is refused. Read broadly, the refusal would also stop a person withdrawing a reason by setting its terminus tentative.

## What Changes

- **The walk passes through retired intentions.** At a link to a retired intention, the walk continues through that intention's own `serves`. If the intention is `superseded`, the walk continues at its `superseded_by` target instead. A terminus grounds only when it is firm and unretired, so a retired terminus grounds nothing. Where `superseded_by` targets loop back on themselves, the walk ends.
- **Abandoned ends are reported.** An unretired intention whose `in-order-to` or `instance-of` target is retired as `abandoned` gets a validation warning naming the abandoned end. A fulfilled end gets no finding, because completion happening in a different order is routine.
- **Supersession keeps a reason's dependents grounded.** Superseding a terminus with a firm one keeps everything that rested on it grounded, with no edits to the dependents. That makes supersession, not rewording in place, the natural way for a reason to evolve, and a superseded reason is visible in `retired.kind`. `superseded_by` stays outside the projection.
- **Termini admit `abandoned` and `superseded` only.** A self-understanding is never discharged. A terminus retired as `fulfilled` is a validation error. On a terminus, `superseded_by` must name a terminus of the same subject.
- **Retiring a terminus is refused when it would unground something.** Retiring a terminus is refused if some unretired intention that was served would become unserved. The refusal names those intentions and the alternatives: set the terminus tentative to withdraw it, or supersede it with a firm terminus to replace it. An intention with another firm ground doesn't block, and neither do the dependents of a tentative terminus, because a tentative terminus grounds nothing. Desires and `firmed_under` dependents never block.
- **Only the person retires a firm terminus.** A harness may retire a tentative terminus whose `source` carries a harness, which lets it withdraw a self it drafted.
- **The 0.2 unserved refusal covers only the intention being written.** Setting a terminus tentative is accepted, and its dependents become validation errors until they are re-grounded. Terminus retirement has its own refusal, described above.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: the grounding requirement (the walk through retired links, the scope of the refusal, the abandoned-end warning) and retirement kinds (termini restricted, `superseded_by` on a terminus). A new requirement covers retiring a terminus.
- `object-model`: retirement kinds per type note the terminus restriction; validation gains the new errors and warning.
- `harness-tools`: `intention_retire` carries the terminus refusal and the harness rule.

## Impact

- README: the serves-graph and grounding paragraphs, the retirement-kinds table, Records/RETIREMENT, Validation, and a Reference Tool Set bullet for `intention_retire`.
- Lands within `intentions/0.2`, which is unreleased. No projection changes. `docs/example` holds no retired termini, so it needs no changes.
- The habit change (#30) is unaffected. Its scenario withdraws a reason by setting the terminus tentative, which this change keeps accepted.
- intentions-cli: the walk, the warning, the refusal, the harness rule and the new validation errors.
- Issue #31: closed by this change.
