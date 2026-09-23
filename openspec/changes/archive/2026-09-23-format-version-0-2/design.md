## Context

The text says a change to any projection is a new format version, and separately that `window.clock` and `transparent` joined the projection "while v0.1 was still undeclared, which is the last moment such a change costs nothing." The second sentence keys the freeze to a ceremony. Files carrying `intentions/0.1` have existed since intentions-cli v0.1.0, and the CLI is at v0.12 implementing that projection. The `origin` change in `refine-object-fields` moved the commitment projection under the same string. #29 lays out the three consequences; the one that matters most is that a 0.1 reader sees `origin: resolution` as malformed. DKF, the sibling format, has already been through a version bump and has a Migration section: move files, regenerate the index, rewrite `format`, nothing else changes.

## Goals / Non-Goals

**Goals:**
- One version bump carrying every deferred break, so a workspace migrates once.
- v0.1 declared as what was implemented, so the version string means what the second reader read.
- A rule that would have caught this.
- A migration that changes no meaning: nothing a person said is un-said.

**Non-Goals:**
- Migrating the site's example workspace in this change. It stays 0.1 until the CLI can migrate it.
- Any change to what the objects mean. Every 0.2 rule was already in the text or deferred by it.

## Decisions

**Declare v0.1 at `54c9a83`.** That is the last commit whose projection the CLI implements. A tag there is the declaration; the Status paragraph names it. Declaring 0.2 without 0.1 would leave the implemented version undeclared forever.

**Freeze from the first file, not the declaration.** The rule becomes: a projection is frozen from the moment any implementation writes the version string; a change to any projection is a new format version. The clock and transparent history is kept as history, with the sentence about cost removed.

**Everything deferred goes in 0.2.** The unserved refusal, the two renames, and the `origin` shape. Each was held for "the next revision that breaks files"; holding any of them past it means a 0.3 migration for a naming change, which is worse than one bump.

**`capacity` and `activities`.** `capacity` because the prose already says capacity every time it means the supply side, and DURATION stays the value type so nothing about ranges changes. `activities` rather than `activity` because an intention's `activity` is one term and an availability's is a list, and one name for two shapes is the thing `refine-object-fields` just had to explain for `parties`. The plural says which side it is.

**Migration is the person's act.** A 0.2 reader accepts a 0.1 workspace and applies 0.1 rules to it: warnings, not refusals, and the old shapes read as written. `migrate` is explicit, rewrites everything a 0.2 writer would, and flips the key. This is also what settles the unserved transition: a workspace with forty-six unserved intentions keeps validating until its owner has walked it up and chooses to migrate. The skill asked for in intentions-cli#5 is the walk-up.

**Acknowledgements carry across.** The migration rewrites `counterpart_version` wherever the counterpart's version changed only because the migration recomputed it. #29 proposed letting them lapse and be re-acknowledged. Lapse exists to catch a change in what the counterpart says; a shape rewrite changes nothing the person acknowledged, so lapsing it would make the workspace say less than the person said. The migration writes the new version into the acknowledgement and touches nothing else on it.

**A reader refuses what is newer than it.** One sentence in the object-model spec: a reader SHALL refuse a workspace whose `format` names a version it does not implement, naming both. #29's third point depends on it.

**Status paragraph.** It says v0.1 was declared at the tag, that this text is the 0.2 draft, what 0.2 breaks and why, and how a 0.1 workspace is read and migrated. The "one rule is in transition" sentence becomes the migration note.

## Risks / Trade-offs

- [Two renames in a version bump look like scope creep] → They are the last file-breaking naming questions, and this is the last cheap moment; the alternative is 0.3.
- [A person migrates a workspace with unserved intentions and is refused] → Migration checks first and refuses to flip the key while any intention is unserved, naming them, so the walk-up happens before the break.
- [The site's example is a 0.1 workspace under a 0.2 spec] → A 0.2 reader accepts it, the docs say so, and it migrates when the CLI can.

## Migration Plan

Tag `v0.1` at `54c9a83` and push the tag. Prose and five deltas; archive with sync. Issue on intentions-cli for 0.2. Knowledge workspace: one claim and a synthesis.

## Open Questions

None. The renames are included; dropping them is a one-line edit to the proposal before apply.
