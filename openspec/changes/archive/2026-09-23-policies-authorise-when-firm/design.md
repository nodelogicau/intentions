## Context

#26 made a terminus the person's word by requiring it to be firm before it grounds anything, using the existing rule that only an act with no harness firms a terminus. A policy is a terminus with a condition, and the settlement said nothing about the condition, so the same tentative object that grounds nothing still authorises a harness to firm or select alone. The spec already holds that a policy's condition is checked at write time only, because the intention may change afterwards, and that `firmed_under` must name an *active* policy, a current-state check. Those two stances have to be reconciled when firmness joins activeness as something validation checks after the fact.

## Goals / Non-Goals

**Goals:**
- A harness cannot author its own authorisation. Only a policy the person has firmed by their own act authorises anything.
- The rule is stated once and cannot drift between grounding and authorising.
- Withdrawal has a defined meaning for the live objects and the records that rested on the policy.

**Non-Goals:**
- Recording history in the spec. Validation still reads current state; the distinction between a live object and a record is what carries the difference.
- Changing what a person may do with their own policies. Every correct use today is unchanged.

## Decisions

**One sentence on the terminus.** "A terminus is inert until it is `firm`: it grounds nothing and authorises nothing." Policies says "only while the policy is firm" and Auto-selection says "a firm policy", both pointing back. The Design Principles sentence changes by two words.

**Refuse at write time, and error on the live object.** `intention_firm` and `select` refuse a tentative policy, naming it and the act that firms it, so a harness sees exactly what is missing. `firmed_under` naming a tentative policy is a validation error, matching the existing error for naming a retired one: a live intention's firmness rests on the policy now, and if the policy is withdrawn the firmness rests on nothing. The finding names the two ways out, re-firm by the person's own act or set tentative.

**Warn on the record.** A RESOLUTION record is append-only history. Its `selector` names the policy that authorised the act when it happened, and the text already checks a policy's condition at write time only because things change afterwards. A record whose policy has since been set tentative or retired is therefore a warning, "selected under a policy since withdrawn", not an error, and the placement it produced stands: it is on the intention, and the person may keep it or re-resolve. The retired case was unstated before and is settled the same way, so withdrawal means one thing.

**Suspend and end are both withdrawal.** Setting a firm policy tentative suspends it, and the person can firm it again; retiring it ends it. Both withdraw what rested on it, in the same way. One sentence in Policies.

**Error from the first revision.** #26 warned during transition because every real workspace would have failed. No workspace known to us holds a tentative policy, and the failure mode is a harness acting on authority nobody gave, so there is nothing to transition and a reason not to wait.

**The refusal message is part of the rule.** The spec says the refusal names the draft and the act that firms it. A harness that hits the refusal should be able to hand the person one command.

## Risks / Trade-offs

- [A person un-firms a policy and is surprised by errors on intentions they did not touch] → The finding says why and names the two ways out. Withdrawing an authorisation withdrawing what rested on it is the point.
- [Warnings accumulate on old records after a policy is retired] → Records are history; a warning on history is information, not a fault, and the placement is the person's to re-resolve if they care.
- [Two checks on `firmed_under`, active and firm, drift apart] → Stated together in one clause in both Stability and Validation.

## Migration Plan

Prose and four deltas; archive with sync. Issue on intentions-cli. Close #27. One claim and a synthesis in the knowledge workspace.

## Open Questions

- Whether validation should also warn on a *firm* policy that a harness wrote and the person then firmed without changing the title, as a nudge to read what one is authorising. Lean no: firming is the person's act and the file shows it.
