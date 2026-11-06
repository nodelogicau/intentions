## 1. Specs

- [x] 1.1 `openspec validate hold-imported-before-recognised --strict`: the deltas resolve against `object-model` and `intention`

## 2. README

- [x] 2.1 Validation: add the warning to the warning-level list (an intention, retired or not, and an unretired commitment sharing an `external` `system` and `uid`, naming both and the two fixes)
- [x] 2.2 Calendar hold under INTENTION: after import recognition, say it prevents the case only from then on, that validation finds earlier cases, and that a write setting such a link is accepted with the warning
- [x] 2.3 Status: note that a workspace whose harness wrote holds before #34 should run `validate` once the CLI reports the warning

## 3. Close out

- [x] 3.1 Commit and push
- [x] 3.2 Open an intentions-cli issue: the warning in `validate` (with both fixes in its detail), and the same warning in the result of a write that sets `external`
- [x] 3.3 Comment on and close issue #36 with a pointer to the change
- [x] 3.4 Archive with sync
