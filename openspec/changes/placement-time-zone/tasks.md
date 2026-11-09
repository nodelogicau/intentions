## 1. Specs

- [x] 1.1 `openspec validate placement-time-zone --strict`: the deltas resolve against `temporal-primitives`, `object-model`, `commitment` and `intention`
- [x] 1.2 Check that every other placement comparison in the main specs (Resolution's replacing selection, Commitment's adopted-commitment warning, re-import) reads as a comparison of instants, and that nothing implies a zone is compared
- [x] 1.3 Confirm no other requirement admits a zone, and that `valid_until`, `timestamp` and record datetimes stay plain RFC 3339

## 2. README

- [x] 2.1 PLACEMENT: the suffix, with the Melbourne example; bare IANA name only; datetime `start` only; who writes it; the offset fixes the instant; no back-fill; windows still read in the resolver context
- [x] 2.2 External reference only (COMMITMENT): import from `TZID` / `timeZone` when it is an IANA name, UTC and non-IANA as offset only; export as a local time in the zone; zone names are references, not definitions
- [x] 2.3 Calendar hold (INTENTION): a hold is exported in its placement's zone
- [x] 2.4 Versioning: normalisation drops the suffix; adding or changing a zone moves no version
- [x] 2.5 Validation: the three errors and the two warnings
- [x] 2.6 Status: lands in 0.2 (and 0.1) with no projection change; every reader of a shared workspace must be upgraded before a writer emits a zone
- [x] 2.7 References, Standards borrowed as grammars: RFC 9557 for the zone suffix
- [x] 2.8 Reference tool set: note where resolution and import results show a zoned `start`

## 3. Close out

- [ ] 3.1 Commit and push
- [ ] 3.2 Open an intentions-cli issue: parse and emit RFC 9557 on placements, normalise by dropping the suffix, write the zone on resolution and import, carry it on export, the five findings
- [ ] 3.3 Comment on issue #37 with a pointer to the change, and close it when archived
- [ ] 3.4 Archive with sync
