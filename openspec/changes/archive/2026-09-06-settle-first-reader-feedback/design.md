## Context

The README says canonical order "is what makes two implementations produce byte-identical files", and versioning says two files with identical state hash identically. The first implementation found thirteen places where the text does not actually pin that down, or where two passages disagree. Eight are settled exactly as the implementation chose. Four are settled differently, and those are the decisions worth recording.

## Goals / Non-Goals

**Goals:**
- Two conformant writers produce byte-identical files and identical projection hashes for identical state.
- Every act the format reserves to a person or their policy is visible in the file, not only in a command result or in git history.
- One word per kind of intention.

**Non-Goals:**
- Declaring v0.1. That follows this change as its own act.
- Any change to the object kinds, the flag kinds, or the delegation rule.
- Re-deriving the projection field sets. `firmed_under` and `version` are provenance and cache, and stay outside them.

## Decisions

**Durations normalise within the date part and within the time part, never across.** Total-seconds conversion would make `P1D` and `PT24H` agree, which is wrong on a day with a timezone transition; leaving `PT60M` and `PT1H` distinct would break the README's own scenario. So: drop zero components, fold weeks into days, re-express the time part from total seconds as `H`, `M`, `S`, never convert between the date and time parts, never touch months or years. `P0D` is the one form of zero, because after zero components are dropped nothing else is left to write.

**`version` is written always, after `id`.** Optional caching defeats byte-identical files, and a diff that shows the version line changing is the cheapest way a reviewer sees that an edit touched the projection, which is what acknowledgement lapse hinges on. After `id` rather than last so it is the second line of every file.

**`week_start` is dropped rather than redefined.** The implementation's rule, that `W36` spans the seven days starting on the week-start day on or before that ISO week's Monday, contradicts its own deixis rule on a Sunday: "this-week" resolves to the ISO week of today while the shifted bounds ended the day before. A week identifier that lies about the ISO week it names is worse than no preference at all. Weeks are ISO weeks. The one case a Sunday-start person loses, saying "this week" on a Sunday and meaning the coming seven days, is deixis, which the writer resolves in conversation and can ask about.

**Seasons use EDTF's own hemisphere codes first, a resolver setting second.** EDTF level 2 already distinguishes Northern (25 to 28) from Southern (29 to 32) seasons, in the same extended set the format already borrows quarters from. Admitting them costs nothing and makes a season unambiguous in the file. The neutral 21 to 24 stay admitted for people who never think in hemispheres, and resolve through `resolver.hemisphere`, default `north` because that is what every EDTF implementation assumes. A season that begins in December runs into the following year.

**Policy-authorised firming lives on the intention as `firmed_under`.** RESOLUTION has `selector` for the same purpose, but a firming is an edit to `stability`, not a record, and the format's rule is that embedded records are about exactly the object they sit in while an act on one object is a field. `firmed_under` is provenance, like `source`, and is excluded from the projection for the same reason: correcting who authorised something does not change what it clashes with. Validation can then distinguish the authorised case: firm, `source.harness` present, `firmed_under` absent is an error; `firmed_under` naming something that is not an active policy of the subject is an error. Whether the policy's condition was satisfied is checked at write time only, since the intention may legitimately change afterwards.

**Three words for three things, and conditions on termini only.** The README used "standing intention" for the cadenced kind and for the windowless kind. They are different objects: a cadence needs a window to expand within, and a terminus has none. Recurring intention, terminus, and policy. The implementation lets any active intention carry `auto_firm`; this change does not, because a policy is a for-the-sake-of sink, "accept anything under thirty minutes" is exactly a self-understanding the person holds, and admitting conditions on a scheduled intention would let a placement authorise a firming. The terminus rule that a `for-the-sake-of` target has no outbound references already exists, and policies inherit it.

**Booleans equal to their default leave the projection.** The existing rule omits absent optional fields; an explicit `false` is the same state and must hash the same. The writer omits it too, so files agree.

**List style is the implementation's rule.** Block sequences for string lists (`location`, `conditional`, intention `parties`, `displaced`), flow mappings for small records (`serves` entries, ranged durations, `gap`, policy conditions), literal block scalars for multi-line prose. There is nothing to argue about; it only needs stating once.

## Risks / Trade-offs

- [Removing `week_start` breaks an existing `intentions.yaml`] → The only workspace is the implementation's own test fixture; a reader that finds the key ignores it, and validation reports it at info level.
- [`firmed_under` could be forged by a harness] → It can, exactly as `selector` could be; the defence is the same, a diff a person reviews. The field makes the forgery visible, which is all provenance can do.
- [Conditions on termini only is narrower than what the implementation shipped] → The issue thread should say so on close. The narrower rule is the one the design principles already imply, and widening later is cheap; narrowing later is not.
- [Admitting eight more season codes widens the EDTF subset] → They parse with the same grammar as the four already admitted and add no new semantics beyond a fixed month mapping.
