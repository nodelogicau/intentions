## Context

The knowledge workspace holds four claims and two syntheses on desire. Settled: it belongs in this format, not DKF, because it is a world-to-mind pro-attitude and not a belief; it cannot be an intention lacking duration and window, because creating an intention is commissive and expressing a desire is not; it cannot be a third `stability` value, because a tentative intention is already conduct-controlling and already checked for consistency; its lifecycle is the appended retirement the format has, with one new kind; it carries no strength field, for the reason severity is kept off flags; and it is the rung below intention, not a role the terminus plays. Open until now: whether `activity` and `location` survive adoption, and whether a desire may point at a tentative terminus.

## Goals / Non-Goals

**Goals:**
- A place for a want that has not earned a why, with no standing it has not earned.
- One act, adoption, that turns a want into a plan and leaves the trail.
- Nothing about intentions, resolution, consistency or grounding changes.

**Non-Goals:**
- Ranking or aggregating desires. No strength, no priority, no ordering beyond the file listing.
- Consistency between desires. They may conflict; that is what makes them desires.
- Any change to the site in this change.

## Decisions

**Fields.** `id`, `version`, `subject`, `title`, `description`, `activity`, `location`, `serves`, `reference`, `source`, `timestamp`, `retired`. Required: `id`, `version`, `subject` (on disk, from the workspace default as for intentions), `title`, `serves` (possibly empty), `source`, `timestamp`. A desire with a `duration`, `window`, `stability`, `parties`, `cadence`, `auto_select` or `auto_firm` is malformed: those are what make an intention an intention, and validation reports an error.

**`activity` and `location` are hints, and they survive adoption.** They are what the person said ("something with the accountant, at the office"), they cost nothing to keep, and adoption copies them onto the intention where they become the real thing. Neither is in the desire's projection, because nothing checks a desire.

**`serves` is `for-the-sake-of` only, and the terminus may be tentative.** A desire is not a means to anything yet, so `in-order-to` is not admitted; it is not generated, so `instance-of` is not. It may say who it is for the sake of, and that terminus may be a draft: a harness writing "call the accountant" for the sake of "being someone who keeps their affairs in order" has drafted a want and a self, and neither grounds or authorises anything until the person acts. The grounding rule does not apply to desires, so an empty `serves` is fine; a desire that names a terminus is simply better prepared for adoption.

**Exemptions are stated once, in the desire capability.** Resolution, `unresolved`, consistency, and grounding each ignore desires. The other capabilities are not modified to say so; a desire has no field any of them reads.

**Adoption is a retirement plus a write, in that order of meaning.** `desire_adopt` takes the desire's id and the duration and window the plan now has, writes a new INTENTION carrying the desire's `subject`, `title`, `description`, `serves`, `reference`, `activity` and `location`, with `stability: tentative` and the caller's `source`, then appends `retired: {kind: adopted, adopted_as: <intention id>}` to the desire. The intention is the record; no RESOLUTION-like record is written. The new intention is subject to everything an intention is subject to, including the grounding warning if its terminus is a draft, which is the moment the harness asks the person to firm the self.

**`adopted_as` mirrors `superseded_by`.** Required when and only when `kind` is `adopted`, its target must exist and be an intention, and validation reports an error otherwise. It is in the projection only through `retired.kind`, as `superseded_by` is.

**A harness writes desires without a policy.** Expressing a desire has no felicity conditions software cannot meet; the person said they wanted something, and recording that is like recording a decline. Adopting is drafting an intention, which a harness may already do. Retiring a desire as abandoned is the person's word in the same sense as any retirement.

**Projection.** `subject`, `serves`, `retired.kind`. The version changes on adoption and abandonment and on a change of terminus, and on nothing else; a desire is mostly prose, and the hash says so.

**Six tools.** `desire_add`, `desire_edit`, `desire_adopt`, `desire_retire`, `desire_show`, `desire_list`, in the reference set with the standing the set has. `desire_adopt` is the one with semantics to keep: it writes the intention first and the retirement second, and refuses if the desire is already retired.

**Placement in the README.** A `DESIRE` section before `INTENTION` under Core Object Types, opening with the ladder: desire, intention, commitment. The object-model diagram gains a row above INTENTION with `adopted_as` pointing down.

**Not file-breaking.** Nothing existing changes. The format version string stays `intentions/0.1`.

## Risks / Trade-offs

- [The inbox fills and nobody adopts or abandons] → It is a list the person owns; the skill can say to read it each session. No expiry: a desire that is still wanted is still wanted.
- [A harness records every stray sentence as a desire] → Cheap by design, and the person retires as abandoned. The skill says a desire is something the person said they wanted, not something the harness inferred.
- [Duplicate wants] → Same answer as duplicate intentions: list before you add, edit the one that exists.
- [The distinction from a tentative unserved intention blurs] → A desire has no duration and no window, cannot be resolved, and is not warned about. The moment it has a when and a how long, adopt it.

## Migration Plan

Additive: new directory, new prefix, new index type. Archive with sync. Issue on intentions-cli. Knowledge workspace: the Desire particular's synthesis qualified to "built", with the two shape questions closed.

## Open Questions

- Before or after the v0.1 declaration. Additive either way.
- Whether the site's composition section should mention the inbox. Not in this change.
