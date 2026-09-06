## Why

The first implementation, intentions-cli v0.1.0, has been written from the README and raised thirteen issues (nodelogicau/intentions #1 to #13) where the text was ambiguous, contradictory, or silent on something a writer must decide to produce byte-identical files and stable hashes. That is exactly the condition the Status section set for declaring v0.1. This change settles all thirteen so that declaring v0.1 can follow as a separate, deliberate act.

## What Changes

- **Projection normalisation is fully specified** (#1, #2, #12): durations drop zero components, fold weeks into days, re-express the time part as hours, minutes and seconds from total seconds, and never convert between the date and time parts; `P0D` is the one form of zero; every set-valued list is sorted, and the lists are named.
- **Booleans equal to their default leave the projection** (#7). `transparent: false` hashes the same as absent, and a writer omits it. The commitment example is corrected.
- **`version` is always written, immediately after `id`** (#3), on every object and on RESOLUTION records.
- **Cadence has a seed** (#4): the first local day of the calendar anchor's lower bound, or the expansion horizon's start when that bound is open. An object with `cadence` must carry a calendar anchor.
- **`week_start` is removed** (#5). Weeks are ISO weeks. A writer resolving deixis on a Sunday for someone whose week starts then may ask; the format does not carry the preference. **BREAKING** for `intentions.yaml`, which loses a key.
- **Seasons get a hemisphere** (#6): EDTF's hemisphere-specific season codes 25 to 32 are admitted alongside the neutral 21 to 24, and the neutral ones resolve through an optional `resolver.hemisphere`, default `north`.
- **Policy-authorised firming is recorded on the intention** (#8, #11): a `firmed_under` field names the policy, sits outside the projection, is required whenever a firm intention's `source` carries a harness, and lets validation tell an authorised firming from an unauthorised one.
- **"Standing intention" is split** (#9): an intention with `cadence` is a *recurring intention*; a *terminus* is an intention with no window, duration, or outbound references; a *policy* is a terminus carrying `auto_select` or `auto_firm`. Conditions are admitted on termini only, which is narrower than the implementation's reading.
- **Deictic vocabulary is fixed** (#10): a writer that accepts deixis recognises at least `today`, `tomorrow`, `this-week`, `next-week`, `this-month`, `next-month`, `this-quarter`, `next-quarter`, and `this-year`, resolved at the current instant in the resolver's timezone.
- **List style is fixed** (#13): string lists are block sequences, small records are flow mappings, multi-line prose is a literal block scalar. The examples are aligned.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `object-model`: versioning normalisation rules, boolean defaults, `version` as a written field, canonical list style, workspace configuration without `week_start` and with optional `resolver.hemisphere`, and the validation list.
- `temporal-primitives`: resolver context without week start, hemisphere season codes, the deictic vocabulary, the cadence seed and calendar-anchor requirement, and `P0D`.
- `intention`: `version` and `firmed_under` in the field list, the stability rule naming `firmed_under`, recurring-intention and terminus terminology, and policies as termini.
- `availability`: `version` in the field list.
- `commitment`: `version` in the field list and the boolean-default rule for `transparent`.
- `resolution`: `version` on the record and terminus wording in auto-selection.

## Impact

- Six spec files and most README sections: Field order, Source, INTENTION (fields, stability, serves graph, instances, policies), AVAILABILITY and COMMITMENT examples, RESOLUTION, Values (DURATION, WINDOW, Cadence), Versioning, `intentions.yaml`, Validation, Design Principles, and Status. The object-model diagram's "standing" labels change.
- The only implementation is the one that raised the issues, and each issue records what it did; where this change agrees, nothing moves, and where it differs (#5, #6, #8, #9) the issue thread should say so when closed.
- v0.1 is not declared here. The Status entry is updated to say its condition is met and this change is what stood between the text and the declaration.
- The knowledge workspace needs one synthesis after archive, recording which issues were taken as proposed and which were answered differently, and why.
