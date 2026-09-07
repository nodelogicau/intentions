## Context

Resolution requires eligible availability for every party. The object model already anticipated the external case and chose refusal: a party whose availability is held elsewhere yields no supply. Issue #25 reports what that produces once an agent is driving. Faced with a dead end on every external meeting, the agent invented availability for the other person rather than report failure, which is a false assertive about someone else's time written into a workspace whose whole argument is about who authors what.

## Goals / Non-Goals

**Goals:**
- An intention naming someone outside the workspace can be placed, and the record of it contains nothing nobody asserted.
- A party who has declared capacity that does not fit is still a real constraint.
- Whatever the workspace does know about an untracked party's time is used.

**Non-Goals:**
- Federation. Reading another workspace's availability stays deferred; this is about a workspace that will never hold those records at all.
- Any judgement about whether an external party is actually free. The format presumes nothing about their capacity and says so in the record.
- Distinguishing a person from a room by URI. The rules here treat every party alike.

## Decisions

**Unrecorded is unconstrained, and the test is derived.** A workspace tracks a party exactly when it holds at least one availability whose subject is that party, retired and expired included. No roster, no new configuration key, and nothing for a person to maintain. Zero records means the workspace has nothing to say about that party's time; one record means it does, and then absence of eligible supply is that party's own answer.

**Alternative rejected: better refusal.** Option (b) in the issue keeps the refusal and requires the result to say which case it is. It documents the dead end without removing it, so the incentive that produced the fabricated availability survives a clearer error message. The reporting half of (b) is worth keeping and is kept, as `presumed`; the refusal half is what has to go.

**The cliff is real and is stated rather than hidden.** Under this rule, declaring your first availability makes you strictly harder to schedule with than declaring none. That is not perverse: it is the difference between having spoken and not having spoken, and it follows from supply being a positive assertion rather than a default. Stating it in the text keeps a reader from filing it as a defect.

**The subject is never unconstrained.** The demand and supply model collapses if a subject with no records resolves anywhere, and someone who lists themselves in `parties` must not gain that. The rule is about `parties` and never about `subject`.

**Unconstrained is not the same as satisfied, and placements are where the difference bites.** The workspace knows nothing of an external party's capacity, but every commitment it created naming that party is something it has already asked of them. Ignoring those would let resolution place two meetings with the same person at the same hour and report neither, which is a worse failure than the one being fixed, because it is invisible. So an untracked party constrains nothing on the supply side and everything on the occupancy side, which is exactly what "unconstrained rather than silently satisfied" has to mean to be more than a phrase.

**The presumption is written down.** `presumed` lists the parties that contributed no supply, beside `supply`, which lists the availabilities the selection was chosen against. Both are provenance of what the selector saw, both sit outside the projection, and together they let a reader see the whole basis of a placement without recomputing anything. A person who wants to know why a Tuesday was chosen for a meeting with someone at another company reads one line.

**`window-clash` has to say whose.** The definition says a placement overlaps another placement, which was tolerable while occupancy was per commitment. Per-party occupancy made it a per-party question, and untracked parties make it load-bearing, because their placements are the only thing constraining them. Two placements clash when they share a party whom both occupy, where occupancy is by that party's own entry.

## Risks / Trade-offs

- [A placement resting on a presumption looks like one resting on declared capacity] → `presumed` on the record and the result distinguishes them, and the party sits at `tentative` until they answer.
- [An untracked room can be booked at any hour] → Its existing placements still constrain it, which catches the double-booking that matters. A workspace that cares about a room's hours declares them, and then it is tracked.
- [Someone declares one availability and becomes harder to schedule with] → Stated in the text as a consequence of supply being a positive assertion.
- [A party whose only records have expired blocks every meeting] → Correct and deliberate. An expired availability means reconfirm, which is the validity horizon working as designed, not an untracked party.
- [Third normative change to resolution in three days] → Better before the declaration than after it, since the current behaviour is writing false records in the field.
