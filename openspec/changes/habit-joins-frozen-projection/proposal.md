## Why

`habit` joined the INTENTION scheduling projection under `intentions/0.2` (change `2026-10-27-habit-needs-no-plan`). The Versioning text justifies this by saying 0.2 "was unreleased". The same paragraph freezes a projection "from the moment any implementation writes the version string into a file, not from any declaration". intentions-cli v0.15.0 has written `intentions/0.2` into workspaces since 2026-09-23, so by the rule's own terms the 0.2 projection was already frozen. "Unreleased" is exactly the declaration the rule refuses to count (issue #32).

The harm is real but narrow. No existing hash moves, because `habit` at its default is omitted. But once someone sets `habit: true`, that object has two versions under one format string. A reader older than the field reports it as stale, `index --check` fails until the index is rebuilt, and an acknowledgement on it lapses or holds depending on which binary last wrote the file. The old reader also keeps generating instances for the habit and lists its dormant instances as unresolved. The text is also silent about `habit` in a 0.1 workspace, whose projection is frozen without it.

## What Changes

- **The freeze rule states its exception.** Field sets stay frozen as written. One exception is named in the text: an optional field omitted from the projection at its documented default may join a frozen projection, because no existing hash moves. The text names every field admitted this way, and `habit` under 0.2 is the only one. Any other change to a projection, including a further field of this kind, needs a new format version.
- **The trade is named.** The Versioning text replaces "while 0.2 was unreleased" with the actual ground and the actual cost. A reader older than the field computes a different version for any object carrying it at a non-default value, and doesn't apply its semantics. `counterpart_version` stays comparable only between readers that agree on the admitted fields.
- **`habit` is admitted only under 0.2.**
  - In a workspace whose `format` is `intentions/0.1`, a write setting `habit` is refused, naming `migrate`.
  - Validation reports `habit` in a 0.1 workspace as an error.
  - A 0.2 reader hashes a 0.1 object without `habit` and gives it no effect on generation, resolution, `unresolved` or consistency.
  - The 0.1 projection is unchanged.
- **Status warns about older readers.** A reader that predates `habit` must be upgraded before anyone in a shared workspace sets it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `object-model`: Versioning by projection hash, which states the freeze rule's named exception and its cost. Validation gains the error for `habit` in a 0.1 workspace.
- `intention`: Habit, which admits the field only under `intentions/0.2` and refuses the write in a 0.1 workspace, naming `migrate`.

## Impact

- README: the Versioning paragraph, the Habit paragraph, Validation, and Status.
- Lands within `intentions/0.2`. No hash moves, and no workspace needs migrating.
- Unblocks intentions-cli#10, which needs the refusal in a 0.1 workspace, the validation error, and hashing `habit` under 0.2 only.
- Closes issue #32.
