## Context

Issue #31, after review, asks two questions. Does the grounding walk pass through retired intentions? And when may a terminus be retired? The maintainer settled four choices before this change:

- the refusal is by grounding, not by pointing
- termini admit `abandoned` and `superseded` only
- only the person retires a firm terminus, and a harness may retire its own drafts
- `superseded_by` stays outside the projection

## Goals / Non-Goals

**Goals:**
- Grounding is defined at every retired link, and ending an arrangement doesn't put its instances in error.
- A reason can evolve by supersession without editing what rests on it.
- A terminus can't be retired out from under live intentions, but can always be withdrawn by setting it tentative.

**Non-Goals:**
- Retiring or re-pointing dependents automatically. Nothing here writes to an object other than the one acted on.
- Any change to policies' `firmed_under` withdrawal rule.
- Detecting reasons reworded in place. Supersession is the visible path, and rewording stays invisible to the projection.

## Decisions

**The walk.** From an intention, follow each `serves` link. At an unretired target, continue as now. At a retired target that is `superseded`, continue at `superseded_by`. At any other retired target, continue through that target's own `serves`. A terminus grounds the walk only when it is firm and unretired. A walk that revisits an intention through `superseded_by` ends there. `serves` cycles are already refused and flagged.

**A retired terminus grounds nothing.** The issue considered letting dependents walk "through" a retired terminus. That would make a retired terminus ground its dependents forever, silently, and it would need a separate merge-time error. Treating a retired terminus like a tentative one, a top that grounds nothing, gives the right answer from the existing unserved check. A terminus retired by a merge shows up as unserved dependents, with no new finding.

**Supersession passes the ground on.** A superseded terminus grounds through its successor, which must be a terminus of the same subject. If the successor is firm, the dependents stay grounded. If it is tentative, they are unserved, so the refusal below applies to supersession too. That is the right outcome, because a draft successor isn't yet a reason.

**`superseded_by` stays outside the projection.** The projection is what bears on consistency, and grounding is a validation concern, like `firmed_under`. Supersession already changes the version through `retired.kind`, and once an object is retired its target can't be edited.

**Abandoned ends warn, and fulfilled ends are silent.** When a means outlives an end that was dropped, the person should hear about it, and a warning names the dependent and the abandoned end. A means outliving an end that was reached is usually just completion out of order. Reporting it would add the kind of noise the format exists to keep away. This applies to `in-order-to` and `instance-of` links. Pending instances of an abandoned recurring intention are therefore warned, which prompts the person to retire them. A `for-the-sake-of` link to an abandoned terminus needs no warning, because it is already handled as unserved unless another ground exists.

**The refusal is by grounding.** Retiring a terminus is refused when some unretired intention that is served now would be unserved afterwards. A pointer rule would refuse two harmless cases: an intention with a second firm ground, and the dependents of a tentative draft. The refusal is computed with the walk above. It applies under 0.1 too, as a refusal rather than a warning, because it protects structure, not severity. A 0.2 reader applies the 0.1 rules only where 0.2 changed a projection or refusal, and this is a new refusal in both versions.

**Kinds.** A terminus admits `abandoned` and `superseded`, and a terminus retired as `fulfilled` is a validation error. Policies are termini and follow the same rule. "Retiring it ends it" continues to mean abandonment.

**Who.** A firm terminus is retired only by an act whose `source` carries no harness. A tentative terminus may be retired by a harness when its own `source` carries a harness. The `source` records the last write, so a draft the person has since edited is theirs. This mirrors firming: a terminus is the person's word, and a harness may withdraw only what it wrote.

**The scope of the 0.2 refusal.** "A write that would leave an intention unserved" means the intention being written. Read more broadly, it would refuse setting a firm terminus tentative whenever something rests on it alone, and a reason could never be withdrawn. Withdrawal stays accepted, and its dependents become validation errors, which is the prompt to re-ground or retire them. Terminus retirement has its own refusal and isn't covered by this one.

## Risks / Trade-offs

- [Withdrawal by setting a terminus tentative fails CI under 0.2 until dependents are re-grounded] → That is intended: withdrawal is the person saying something no longer stands, and CI shows what rested on it. The person can supersede instead if they are replacing the reason rather than dropping it.
- [The abandoned-end warning is noisy for ended arrangements with many pending instances] → Bounded by the horizon, and each warning is resolved by retiring the instance, which the existing rule already asks the person to do.
- [Supersession chains get long] → The walk follows them. Retired objects are never edited, so a chain only grows by new acts.

## Migration Plan

This is additive within unreleased 0.2. No file needs rewriting, because `docs/example` holds no retired terminus. A 0.1 workspace with a terminus retired as `fulfilled` will report an error the moment a 0.2 implementation validates it. Archive with sync, open an issue on intentions-cli, and close #31.

## Open Questions

None blocking.
