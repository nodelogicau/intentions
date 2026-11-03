## Context

Issue #34: a harness with write access to the person's calendar writes a busy hold when a placement is selected. For an intention with `parties`, resolution creates a COMMITMENT, and the commitment's `external` records the event. A placed intention with no `parties` creates no commitment, and object-model forbids any other object from referencing an external calendar object. So the hold has nowhere to be recorded. The issue offers three options: (1) optional `external` on a placed intention, (2) a one-party commitment for every placed solo intention, (3) a private harness mapping. It prefers (1), and the review on the issue agreed, rejecting (2) because a commitment is commissive towards another party and (3) because it is not portable.

The issue's case for timing ("v0.1 is undeclared") is out of date: `intentions/0.2` is frozen, and the freeze rule's one named exception is `habit`. This design keeps the field out of the projection, so the freeze rule is not engaged.

## Goals / Non-Goals

**Goals:**
- A harness finds, moves and releases its own hold for a solo intention across runs, and never duplicates it.
- A hold read back from the calendar never becomes a commitment that clashes with its own intention.
- One link shape and one meaning (`{system, uid}`, the only link) for both object types that may carry it.
- No hash moves and no format version.

**Non-Goals:**
- iTIP replies. Party status changes only by that party's own act; this change adds no path to it.
- Writing availability as busy time, or publishing it for booking (federation).
- Harness mechanics: when to write, which calendar, credentials, retries.
- Recurring holds. Each generated instance is its own intention with its own placement and its own hold, never one event with an RRULE.

## Decisions

**Option 1, with `external` outside the projection.** The projection holds the fields that bear on consistency checking. The hold is downstream of `placement`, which is already hashed, and says nothing new about the person's time. Hashing it would change the version on every hold write, lapse acknowledgements and break stored `counterpart_version` values for an act that changed nothing in the plan. It is excluded alongside `source`, `timestamp` and `firmed_under`. The asymmetry with a commitment is deliberate: an imported commitment's UID is its identity and the thread that ties a recurring event's occurrences together, so it stays in that projection.

Alternative considered: hash it and name `intentions/0.3`. Rejected: a version bump buys nothing a consistency check can use.

**Only an intention with no `parties`.** Any intention with `parties` gets a commitment on selection, including for untracked parties, so its hold belongs on the commitment. Allowing both would give one placement two links and two holds. `external` on an intention with `parties` is a validation error, and a write adding `parties` to an intention that carries `external` is refused unless the same write clears it; the harness moves the link to the commitment when one is created.

**Only on a placed intention.** A hold is of a placement. `external` with no `placement` is an error. A replacing selection clears and writes the placement in one act, so the intention is never unplaced in between, and `external` survives it: the harness updates the same event to the new placement rather than creating a second.

**Unique per intention.** Imported commitments share a UID across occurrences of one recurring event. Holds do not: two intentions carrying the same `system` and `uid` is an error, because each hold is a separate event the harness wrote.

**Export shape is fixed and minimal.** Start and duration, all-day form for an all-day placement; `placement.location` where it is a URI; the `title` as `SUMMARY` / `title`, since the calendar is the person's own and an untitled busy block is unreadable to them; always opaque, since intentions are never transparent (where the person will be, as their own statement, is presence); `STATUS:TENTATIVE` for `stability: tentative` and `STATUS:CONFIRMED` for `firm` (JSCalendar `status: tentative` / `confirmed`). Nothing else crosses: no `description`, `serves`, `activity`, `parties`, policy, `source` or `reference`. This extends the boundary list in External reference only, which today ends "No other metadata SHALL cross the boundary".

**Import recognises holds.** Before creating a commitment, an importer checks whether the event's `system` and `uid` match any intention's `external`, retired or not. A match is that intention's hold and creates nothing. This closes the duplicate loop the issue describes and prevents a self-inflicted `window-clash`.

**Retirement keeps the link; the harness acts on the kind.** A retired intention is not edited except to append acknowledgements, so `external` stays. For `abandoned` or `superseded` the harness releases the hold, since nothing will happen then. For `fulfilled` it leaves it, since the event happened and the calendar keeps its record. Releasing a hold needs no write to the workspace.

**Harness writes are allowed.** Setting or clearing `external` is a bookkeeping write a harness may make with `source.harness` set; it confers no stability and needs no policy. It does not touch the version.

## Risks / Trade-offs

- [An older reader keeps `external` on an intention as an unknown key and ignores it] → It neither hashes it nor validates it, and its importer would import the hold as a commitment. Status says to upgrade every reader of a shared workspace before a harness writes holds.
- [A person edits the hold directly in their calendar] → The calendar is not authoritative for the placement. The harness rewrites the hold from the placement on its next run, or, if the person moved it on purpose, they re-select in the workspace. Importing the edit is out of scope.
- [The hold is deleted in the calendar] → The link dangles. The harness may write a new event and replace `external`; this is a non-projected write, so nothing else moves. Validation does not check external resolvability, as it never has for commitments.
- [The calendar already holds someone else's event for the same occasion, such as a venue's ticket invite for a concert the person planned as an intention] → Import recognises only the intention's own hold, so the venue's event still imports, as a commitment whose only party is the subject, and clashes with the intention. That is an import question, not a hold one, and is tracked in #35.
- [`title` crossing the boundary leaks prose to a shared calendar] → The calendar is the person's own; a harness writing to a shared one is the person's configuration. Description and the serves graph never cross.

## Migration Plan

None. The field is optional and unhashed; no hash moves and no workspace migrates. intentions-cli implements the field, the three validation errors, the import check and the export shape.

## Open Questions

None.
