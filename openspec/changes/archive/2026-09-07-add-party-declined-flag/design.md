## Context

A commitment carries a status per party, but occupancy, capacity and ranking were all written as though a commitment had one status. So `declined` had nowhere to take effect, and the ranking ladder ("displaces no accepted commitment", "displaces only tentative commitments") is undefined when three parties disagree. The implementation shipped the conservative reading: a declined commitment occupies everyone's time until someone cancels it.

## Goals / Non-Goals

**Goals:**
- A party who has declined is not charged for the hour they refused.
- The ranking ladder is defined for every combination of party statuses.
- A subject who declines a commitment fulfilling their own intention is told that the plan and their stated will disagree.

**Non-Goals:**
- Any inference from a decline. No act follows automatically, and nothing changes a party status.
- Freeing the intention. Cancellation remains the only act that clears a placement.
- Any new field, and any change to a projection.

## Decisions

**Occupancy is a fact about a party, because status is.** The format already holds that a status is a fact about that party's will and that only their act may set it. Occupancy is a claim on that same party's time. Reading a per-party field into a per-commitment effect is what created the gap, so the effect becomes per-party too: a commitment consumes a party's capacity, and is displaceable by that party's resolution, exactly where that party's entry is `tentative` or `accepted`. This is the format's founding argument applied to its own machinery. A calendar that keeps charging a person for a claim they refused is the imposition the format exists to make visible.

**Freeing the decliner's time hides nothing.** The objection is that a decline would silently free time the other parties still believe is booked. It does not: their commitment still stands and still occupies their own time, and their view is unchanged. The single thing that changed is a fact about this person, which the status field carries and which iTIP transmits, and that negotiation is already delegated to the external system.

**Transparency is the precedent.** A commitment that consumes nobody's capacity already exists. Transparency is a property of the whole commitment and a decline is a property of one party's entry, but both are exemptions from occupancy, so the machinery they need is the same.

**The two origins split, and only one needs a flag.** An imported commitment has no intention behind it, so a decline frees the decliner's time and there is nothing left to disagree with. A commitment from a resolution is different: the intention's own placement occupies the subject's time whatever the commitment says, and "an intention's placement and the commitment created from it count once" means the pair still consumes one hour. So a subject's decline frees nothing while the intention stands, and the subject has said they will not attend something they still intend at that hour. That is a disagreement between two objects, which is exactly what a flag is for, and it is the only mechanism consistent with software never deciding.

**A counterparty's decline is flagged too.** It leaves the subject's intention placed on an arrangement that has lost a required party. The subject's own time is still occupied and their entry is untouched, but they need to know, and the response is theirs: cancel, replace, or acknowledge and go ahead without that person.

**`party-declined` rather than a status on the flag.** The alternative was to widen an existing kind. None fits: the placement overlaps nothing, lacks no supply, and rests on nothing expired. Kinds are how this format distinguishes responses, and the response here is unlike the other six.

**No automatic consequence, and the flag is acknowledgeable like any other.** "Rob cannot come and I am doing it anyway" is precisely the resolute act the acknowledgement mechanism exists for, so it needs no new machinery. A later change to the counterpart's projection lapses it, which is already the rule, and a party status is in the projection, so a second decline or a reversal resurfaces the flag.

## Risks / Trade-offs

- [A seventh kind days before v0.1] → It is additive. A workspace with no declined party behaves exactly as before, and the alternative leaves a field that changes nothing, which the format's own test calls decoration.
- [The implementation shipped the opposite reading in v0.8.0] → One version, one day old, and the issue asked the question rather than assuming the answer. The close comment should say what changed.
- [Per-party occupancy makes capacity depend on who is asking] → It always did: supply is per subject, and a party's capacity was never shared. This makes the consumption side agree with the supply side.
- [A person could acknowledge every party-declined flag and drift into a schedule of refused commitments] → Visible in the file as a list of acknowledgements, which is the format's answer everywhere else.
