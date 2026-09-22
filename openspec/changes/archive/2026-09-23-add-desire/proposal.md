## Why

Since `ground-every-intention` an intention costs a why: it must reach a firm terminus or validation says so, and the next revision that breaks files will refuse it. That is right for an intention, and it leaves a passing remark with nowhere to go. "Call the accountant" is not yet a plan, has no why, may conflict with other things the person half-wants, and should not be held with the standing of an intention the person has thought through to who they are trying to be. The knowledge workspace settled the shape of the answer on 2026-09-06 and its relationship to the terminus on 2026-09-23: a DESIRE is the rung below intention, a world-to-mind pro-attitude in Bratman's sense, not commissive, free to conflict, exempt from resolution, consistency and grounding, and adoptable into an intention. It is the inbox the grounding rule now needs.

## What Changes

- **A fourth object type, DESIRE.** Prefix `des_`, directory `/desires/`. Fields in canonical order: `id`, `version`, `subject`, `title`, `description`, `activity`, `location`, `serves`, `reference`, `source`, `timestamp`, `retired`. No duration, no window, no stability, no parties, no acknowledgements, no strength or priority. `serves` admits `for-the-sake-of` only, possibly empty, and its target may be any terminus, tentative or firm: a draft want may point at a draft self, since nothing rests on either.
- **Exempt from everything an intention is subject to.** Resolution never sees a desire; consistency checks nothing against one; `unresolved` does not list one; the grounding rule does not apply. A desire is not conduct-controlling and the format treats it so.
- **Adoption is a retirement with a pointer.** Retirement kinds `abandoned`, `superseded`, and `adopted`, the last carrying `adopted_as`, required when and only when the kind is `adopted`, naming the intention it became. Adoption writes a new INTENTION from the desire, carrying its subject, title, description, serves, reference, and `activity` and `location` as the person's own hints, plus the duration and window the act supplies, and then retires the desire. The intention is the record of the adoption; no separate record.
- **A harness may write a desire freely.** Expressing a desire is not a commissive act, so a harness records one on the person's word as it records a decline, and adopting is drafting an intention, which a harness may do. The result is tentative and grounded or not like any other intention.
- **Projection**: `subject`, `serves`, `retired.kind`. Everything else is prose or provenance.
- Object model, identifiers, retirement kinds, type names, file layout, index, validation, and the reference tool set are extended; six tools join the set: `desire_add`, `desire_edit`, `desire_adopt`, `desire_retire`, `desire_show`, `desire_list`.

## Capabilities

### New Capabilities

- `desire`: the DESIRE object, its fields and projection, its exemptions, its retirement kinds, and adoption.

### Modified Capabilities

- `object-model`: identifiers gain `des`; retirement kinds per type gain desire's three and `adopted_as`; type names gain DESIRE; validation gains the desire errors.
- `harness-tools`: the reference set gains the six desire tools, and `desire_adopt`'s semantics are stated.

## Impact

- README: a `DESIRE` section under Core Object Types before `INTENTION`, the identifier and retirement-kind tables, the object-model diagram and the serves-graph paragraph, File Layout, Validation, the Reference Tool Set, and a sentence in Design Principles under "The why is the price of entry" saying where a remark goes instead.
- One new spec and two deltas. Ten capabilities after sync.
- Not file-breaking: no existing object changes, a new directory and prefix are additive, and `index.yaml` gains a type. Whether it lands before or after the v0.1 declaration is the maintainer's call; the knowledge workspace deferred it past v0.1 when v0.1 seemed nearer than it is.
- intentions-cli: the object, the six verbs and tools, `unresolved` and `resolve` ignoring desires, and the skill's advice that a passing remark is `desire add`, not `intention add`.
- The site is unaffected; the page names no object beyond the three it explains. Whether it should name the inbox is a later question.
- Knowledge workspace: the Desire particular's synthesis is qualified to "built", and its open shape questions close.
