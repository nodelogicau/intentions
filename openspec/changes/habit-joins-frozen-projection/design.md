## Context

Issue #32 points out that the precedent sentence in Versioning contradicts the rule it sits beside. The rule freezes a projection when the version string is first written to a file. CLI v0.15.0 wrote `intentions/0.2` on 2026-09-23, so "unreleased" can't be the ground for adding `habit`. The issue offers two options. (a) Keep `habit` in 0.2 and state the exception honestly. (b) Hold `habit` for `intentions/0.3`. This change takes (a), the option the issue leans to: the field is additive, no file carries it yet, and the harm needs one workspace shared by binaries from both sides of the change.

The two earlier precedents, `window.clock` and `transparent`, joined 0.1 before any file carried the string, so they were within the rule. Only `habit` needs the exception.

## Goals / Non-Goals

**Goals:**
- The freeze rule and its precedent agree. Where the text bends the rule, it says so and names the cost.
- `habit` behaves in exactly one way per format version: hashed and honoured under 0.2, and absent under 0.1.
- A person sharing a workspace across binaries knows to upgrade before setting `habit`.

**Non-Goals:**
- A general mechanism for adding fields to frozen projections. The exception is a closed list, not a policy.
- Making old readers detect a field they don't know. They keep an unknown key unhashed, as they already do.
- Any change to the 0.1 projection, or to migration. No 0.1 object can carry `habit`, so migration has nothing to carry across.

## Decisions

**The exception is named, not general.** One option was a general clause: "an optional field omitted at its default may join a frozen projection." That would quietly turn the freeze into a rule that applies only to breaking changes, and every later addition would reopen the same trade with nobody looking at it. A closed list keeps the rule a rule. The text states the condition that makes the exception tolerable (an optional field omitted at its default moves no existing hash), names `habit` as the one field admitted that way, and requires a new format version for every other projection change, including a further field of the same kind.

**The cost is stated where the guarantee was.** The paragraph currently ends by saying a stored `counterpart_version` "stays comparable for as long as its format version is known". That is no longer quite true. The text now says comparability holds between readers that agree on the admitted fields, and that a reader older than `habit` computes a different version for an object carrying `habit: true`.

**`habit` is refused under 0.1, not ignored on write.** In a 0.1 workspace, the 0.1 projection has no place for `habit`. If a write were allowed to carry it, the field would change generation and resolution without changing the version, which is exactly the mismatch the projection exists to prevent. Refusing the write and naming `migrate` gives the person the one path that works. The Migration requirement already says the 0.1 rules apply "where 0.2 changed a projection", and this change makes clear that `habit` is such a case.

**A 0.1 file that carries `habit` anyway is an error.** Files can arrive by merge or a hand edit. Validation reports `habit` in a 0.1 workspace as an error naming `migrate`. Until then a 0.2 reader hashes the object under the 0.1 projection and gives the field no effect, so the object behaves the same way under every reader of that workspace.

**Status carries the operational warning.** The upgrade note is about deployment, not about any object's semantics, so it belongs in Status next to the description of 0.2 as a draft. It is not a normative requirement.

## Risks / Trade-offs

- [A shared workspace mixes a v0.15.0 binary with a newer one, and someone sets `habit`] → Status says to upgrade first. The divergence shows up as `stale_version` and an `index --check` failure, not as silent corruption.
- [The named exception invites more of the same] → The text says that any further projection change, including another default-omitted field, needs a new format version.
- [Option (b) would have kept the rule unbent] → It would also hold the habit semantics back for a whole format version, when no file carries the field yet. The issue and the maintainer both prefer (a).

## Migration Plan

None. No hash moves, and no 0.1 object can carry `habit`. intentions-cli#10 implements the 0.1 refusal and the validation error together with the field.

## Open Questions

None.
