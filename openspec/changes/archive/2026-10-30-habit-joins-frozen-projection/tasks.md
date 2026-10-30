## 1. Specs

- [x] 1.1 `openspec validate habit-joins-frozen-projection --strict`: the deltas resolve against `object-model` and `intention`

## 2. README

- [x] 2.1 Versioning: replace "while 0.2 was unreleased" with the actual ground (optional, omitted at its default, no existing hash moves), state the freeze rule's single named exception and that any further projection change is a new format version, and qualify `counterpart_version` comparability by agreement on admitted fields
- [x] 2.2 INTENTION projection and the Habit paragraph: `habit` is in the projection and admitted only under `intentions/0.2`; a write setting it in a 0.1 workspace is refused naming `migrate`, and a 0.1 object carrying it is hashed and treated as if it were absent
- [x] 2.3 Validation: `habit` in a 0.1 workspace is an error naming `migrate`
- [x] 2.4 Status: a reader that predates `habit` must be upgraded before anyone sharing the workspace sets it

## 3. Close out

- [x] 3.1 Commit and push
- [x] 3.2 Comment on intentions-cli#10: the 0.1 refusal, the validation error, hashing `habit` under 0.2 only
- [x] 3.3 Comment on and close issue #32 with a pointer to the change
- [x] 3.4 Archive with sync
