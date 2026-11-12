## Context

A terminus is a sink in the serves graph: no window, no duration, no `serves`. It is what the person's intentions are ultimately for. Since ground-through-retirement, supersession is the way a reason evolves: retiring a terminus as `superseded` hands its dependents to `superseded_by` without editing them. That covers rewording (one self, truer words) and merging (several termini superseded by one). It doesn't cover splitting, because `superseded_by` names one object. Splitting is how self-understanding most often grows: one self is found to be two. Today the person has two options. Retiring the old terminus as `abandoned` says it was dropped. Superseding it by one successor is half true and loses the other link. The retirement record is the format's history of who the person has been trying to be, and both options record that history wrongly.

`superseded_by` is outside every projection, so its shape can change without a version changing. The text is the `intentions/0.2` draft. Readers already in use expect a single id there.

## Goals / Non-Goals

**Goals:**
- A terminus can be recorded as refined into several, and the retirement record says so.
- Dependents stay grounded through a split exactly as they do through a one-to-one supersession, with no edits needed at the moment of the act.
- The ambiguity a split leaves behind (which successor is a given dependent for?) is visible, and resolving it is the person's act.

**Non-Goals:**
- **Deepening.** That's where a terminus turns out to serve a deeper self. A terminus stays a sink. Admitting a mediate end, valid as a `for-the-sake-of` target while itself reaching a terminus, would change the terminus definition at the root of grounding and pull the format toward a structure of the self that it leaves to the person. Deepening is recorded as supersession, with the earlier wording kept in the retirement `reason` or in a DKF claim.
- **Splits of anything but a terminus.** A plan that becomes two plans is two new intentions, each with its own `serves`. A desire that becomes two is two desires. Neither has dependents that need a ground passed on, so neither needs a list.
- **An inquiry or exploratory kind of terminus.** An early, uncertain self is an ordinary terminus, refined by supersession like any other.

## Decisions

**A list on a terminus only, of two or more.** On a terminus, `superseded_by` is either one id or a list of two or more distinct ids. One successor is always written as a single id, never as a one-element list, so each state has one spelling and existing files are untouched. Writers sort the list by id, as other lists of strings are sorted. That gives byte-identical files, and no successor reads as the primary one. Each entry must be a terminus of the same subject, firm or tentative, the same rule a single successor follows now. Validation reports a list anywhere but on a terminus, a list of fewer than two, a repeated entry, and any entry that is not a terminus of the subject, each as an error.

**The walk follows every branch, and any branch grounds.** At a link to a terminus superseded by a list, the walk continues at each successor in turn and grounds if any of them grounds. The existing rule (a walk that revisits an intention through `superseded_by` ends without grounding) applies per branch. Supersession can therefore form a DAG (split, then merge) without any new cycle rule. The alternative was to require every successor to ground. That was rejected: it would make a split with one draft successor unground everything, and it would penalise the honest act of naming a self the person hasn't yet firmed.

**The retirement refusal follows from the walk, unchanged in kind.** "Retiring a terminus" is already computed by the walk, so a split with at least one firm successor is accepted, and a split whose successors are all tentative is refused when something rests on the terminus. Only the alternatives the refusal names change their wording: supersede it with one or more termini, at least one firm.

**Info, not warning, for what a split leaves undecided.** A dependent grounded through a split is grounded honestly, but the record no longer says which successor it is for. Validation reports, at info level, each unretired intention with a `serves` entry whose supersession chain from its target passes through a terminus superseded by a list. The finding names the intention, the split terminus and its successors, with re-pointing as the fix. It is info because a dependent may truly serve both successors. A warning would pressure a harness to choose for the person, and choosing what an intention is for is the person's act. A one-to-one supersession raises no finding, because there's nothing to choose. Desires serving a split terminus raise no finding: nothing is checked against a desire, and adoption carries its `serves` onto an intention, which then gets the finding.

**The list is the trail.** Once every dependent is re-pointed, the list still records that the old self became these. Nothing is ever removed from a retired record, and the info finding goes quiet by itself.

**Readers are named in Status.** A reader that predates this change and expects a single id may fail to parse a list or misread it. The README's Status paragraph already lists upgrade-before-use notes for `habit` and `external`, and gets one more: every reader of a shared workspace must be upgraded before anyone splits a terminus.

## Risks / Trade-offs

- [A split grounds a dependent through a successor it isn't really for] → That's the leniency of "any branch grounds", made visible by the info finding, with the fix named. Grounding stays honest at the level the format checks (some firm self of the person's), and the rest is the person's to say.
- [A harness re-points dependents on its own] → The skill treats re-pointing as asking what each dependent is for, as it does when walking unserved intentions. The finding is info, so nothing pushes a harness to act.
- [Older readers in a shared workspace] → Named in Status. No file changes until someone splits.
- [Scope creep toward lists elsewhere] → The decision states why only termini need one: only a terminus hands a ground to dependents that it cannot edit.

## Migration Plan

Prose and three deltas, archived with sync. No projection change and no file change to existing workspaces. `docs/example` holds no retired termini and stays as it is. An issue on intentions-cli covers list parsing, the branching walk, the errors and the info finding, a repeatable `--superseded-by` on `intention retire`, and the skill's supersession rule gaining the split case.

## Open Questions

- Whether `intention_retire` should offer, in its result, the dependents that the split leaves undecided, so a harness can ask about them at once rather than waiting for `validate`. Lean yes, as the same info finding carried in the result, the way write results already carry warnings.
