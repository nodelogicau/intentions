## Why

The README's Status paragraph says the first implementation was intentions-cli v0.1.0 and raised thirteen issues, all settled, four differently. That was true on 2026-09-06. The CLI's own record, `SPEC-FEEDBACK.md`, now lists twenty-five issues: twenty-four settled, five decided differently from what the implementation chose, one still open (#23, a reference tool set), and the CLI is at v0.11.0. The site's proof section repeats the thirteen, and the `landing-site` spec requires the page to say nothing the README does not, so the site's central proof claim is wrong in the same way. The paragraph is the sentence a reader uses to judge whether the spec has been tested, and it undercounts by half.

## What Changes

- The README Status paragraph states the current counts and version, names the one open issue, and points at the CLI's feedback file as the record so the numbers have a source.
- The site's proof lead states the same counts in the same words, and gains a link to the feedback file.
- The `landing-site` spec gains a requirement that the proof section's account of the second reader match the feedback file at publication, so the next drift is caught by the page-against-README read rather than by accident.
- No change to any format requirement.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `landing-site`: a new requirement that the second-reader counts on the page agree with intentions-cli's `SPEC-FEEDBACK.md`.

## Impact

- README: the Status paragraph only.
- `docs/index.html`: the proof section's lead paragraph.
- One spec delta. All eight specs must validate after sync.
- The counts will drift again as issues are raised; the requirement makes the check part of every site edit, and the design records the one-line tally command.
