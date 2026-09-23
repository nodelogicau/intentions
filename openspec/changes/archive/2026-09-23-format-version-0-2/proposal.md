## Why

`refine-object-fields` changed the COMMITMENT projection under an unchanged `intentions/0.1`, against the text's own rule that a change to any projection is a new format version (nodelogicau/intentions #29). The rule had a loophole the change leaned on: that a projection costs nothing to change "while v0.1 was still undeclared". Readers key on the version string in the file, not on a declaration, and files carrying `intentions/0.1` have existed since the first CLI release. The text has also twice deferred the refusal of an unserved intention to "the next revision that breaks files", and two renames were held back for the same revision. That revision is now.

## What Changes

- **v0.1 is declared**, as the text the second reader implemented: the commit before the `origin` change, `54c9a83`, tagged `v0.1`. Its stated condition has been met for weeks.
- **The current text is `intentions/0.2`.** The workspace marker, the object-model spec and every example say so. **BREAKING**: a 0.2 workspace is not readable by a 0.1 reader, and says so by its `format` key.
- **The freeze rule is fixed.** A projection is frozen from the moment any implementation writes the version string, not from the declaration. The loophole sentence is replaced.
- **0.2 carries every deferred break, so there is one migration, not several:**
  - the COMMITMENT `origin` and `resolution` shape, already in the text;
  - an unserved intention is a validation **error** and a write that would leave one unserved is **refused**, as #26 deferred;
  - AVAILABILITY `duration` is renamed **`capacity`**, so supply reads as supply, DURATION remaining its value type;
  - AVAILABILITY `conditional` is renamed **`activities`**, one vocabulary under one name on both sides of the match.
- **Migration is an explicit act.** A 0.2 reader accepts a 0.1 workspace under 0.1 rules until `format` is rewritten. A `migrate` operation rewrites the `origin` shape and the two renamed fields, recomputes every version, regenerates the index, rewrites `format`, and **carries acknowledgements across**: `counterpart_version` on any acknowledgement whose counterpart changed only by the migration is rewritten to the new version, because a mechanical rewrite is not a change in what the counterpart says. A 0.1 workspace with unserved intentions is walked up to its termini before its owner flips the key, since 0.2 refuses what 0.1 warned about.
- **A reader refuses a workspace whose `format` is newer than it knows**, naming the version.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `object-model`: the format string; the freeze rule; migration and the newer-format refusal; Validation's unserved finding becomes an error; list names.
- `intention`: the reachability requirement refuses under 0.2; the activity vocabulary names `activities`.
- `availability`: `capacity` and `activities` throughout.
- `consistency`: the two flag descriptions that name the renamed field.
- `resolution`: eligibility names `activities` and `capacity`.

## Impact

- README: Status (v0.1 declared, this text is 0.2, the transition note becomes the migration note), Versioning (the rule), a new Migration subsection, the AVAILABILITY section and every mention of `duration` as capacity and of `conditional`, the Validation section, the Reference Tool Set rows for availability, `intentions.yaml`. Five deltas.
- The site's example workspace stays a 0.1 workspace, written by a 0.1 binary, until the CLI can migrate it; its README says so, and the figure script keeps running against it because a 0.2 reader accepts 0.1.
- intentions-cli: read 0.1 and write 0.2, `migrate`, the newer-format refusal, the renames, the unserved refusal under 0.2. #8 is superseded by a 0.2 issue.
- Knowledge workspace: one claim and a synthesis on the spine.
