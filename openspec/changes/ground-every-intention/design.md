## Context

`serves` is required on every intention but may be empty. A terminus is an intention with no `serves`, no `window` and no `duration`, and the only rule about it is a SHOULD on its wording. Validation checks cycles and that a terminus has no outbound references, nothing else about the chain. Over MCP every write carries a harness, since the server sets it from the client's name, so any rule that refuses harness-sourced termini outright makes a terminus impossible to create from a harness. `firm` is already the person's act or a policy they hold, and a policy is a terminus of the subject. The review on #26 proposed building the second rule from that.

## Goals / Non-Goals

**Goals:**
- Grounding is a condition of admission, not a quality: no intention stands without saying what it is for, and what it is for bottoms out in the person's own word.
- A harness can still do its job over MCP: draft the terminus, then the intentions, and hand the person one act, firming.
- Existing workspaces keep validating during the transition, and the transition has an end.

**Non-Goals:**
- A flag. An unserved intention is a structural finding about one object, not a way the prospective graph fails to hang together between two. It is validation's job.
- Refusing tentative termini or intentions reaching them. Drafts are drafts.
- A DESIRE object. The issue strengthens that proposal; it does not decide it.

## Decisions

**Reachability, by any role, to a terminus of the same subject.** The check walks `serves` outward through `in-order-to`, `for-the-sake-of` and `instance-of` and succeeds on reaching a firm terminus whose `subject` equals the intention's. Instances reach one through the recurring intention and need nothing new. A cycle is already an error and is not walked twice.

**Warning now, refusal later, and the write matches validation.** The issue refused the write and warned on validation; that is the refusal regime with a warning label. In this revision both warn: `validate` reports `unserved` at warning level, and a write that would produce an unserved intention is accepted and its result carries the finding. The Status paragraph records that the next file-breaking revision raises both to refusal, which is DKF's level for a claim with no particular. A warning that names what to do ("serves nothing; add `--serves <terminus>:for-the-sake-of`") is part of the requirement.

**A terminus is firm, and only the person firms it.** A terminus SHALL be `firm`. A policy's condition applies to intentions that are not termini, so no `auto_firm` can firm a terminus and no `auto_select` can act on one. `firm` on a terminus therefore comes only from an act whose `source` carries no harness. A harness may write a tentative terminus; validation reports it at info level as a draft, and every intention that reaches only tentative termini is unserved. This answers the issue's fear, a fabricated self at the top of the graph, with visibility rather than refusal: the draft exists, grounds nothing, and waits for the person.

**The subject match is stated, not inferred.** Policies already require a terminus of the subject. The same clause on reachability keeps a personal workspace simple and gives an organisation workspace a terminus per subject.

**The principle goes in the text's own voice.** "The why is the price of entry" follows "A terminus is a person, not a task" in Design Principles. It says three things: a workspace's first act is a terminus, a harness's first question is who the person is trying to be, and the cost of capture is the point.

**The site's example gains the chain rather than a warning.** The one-to-one with Priya serves the terminus `for-the-sake-of`. `serves` is part of the projection, so the object's version changes, but no candidate depends on it: the resolve output and every candidate bar in the figure are unchanged, and the figure is regenerated to prove it.

**The CLI is asked, not told.** One issue on intentions-cli: the warning in `validate` and on write, the terminus firmness rules, `intention_firm` refusing a policy on a terminus, and a skill that walks an existing workspace up to its termini one at a time, asking rather than inventing.

## Risks / Trade-offs

- [Every real workspace warns on day one] → That is the transition's purpose. The warning names the fix, the skill walks the person through it, and nothing stops validating.
- [A harness invents termini to silence warnings] → Its termini are tentative and ground nothing until the person firms them, so inventing them silences nothing. The skill says to ask, not to invent.
- [A person firms a terminus without thought to silence a warning] → Visible in the file as their act, which is the format's answer everywhere else.
- [Refusal later breaks files] → Announced now in Status, with the level and the trigger.

## Migration Plan

Prose and three deltas; archive with sync. `docs/example` edited in place with `intention edit --serves`, figure regenerated, byte-identical candidates confirmed. Issue on intentions-cli; close #26 with a comment. Knowledge workspace: two claims (grounding as admission; a terminus is firm and the person's) and a synthesis on the spine.

## Open Questions

- Whether a tentative terminus should be reported at info or not at all. Lean info: a draft self is worth seeing in `validate` output.
