## Why

The specification describes its operations as verbs (add, edit, firm, retire, resolve, select, acknowledge, check) and says nothing about how a harness reaches an implementation programmatically. DKF names its tools, so a skill written against one implementation works against another. This format does not, so a second MCP server would name and shape its tools differently and every skill and prompt would have to be rewritten. This is the one issue of the twenty-five raised by the first implementation that is still open (nodelogicau/intentions #23), and the last thing standing between the text and a v0.1 declaration that says the second reader has been answered.

## What Changes

- A **Reference Tool Set** section in the README, after Status and before References: one tool per operation, named after the verb and grouped by the object it acts on, with parameters typed after the format's own structures and results equal to the implementation's non-interactive output. The names are stated as a reference set, not the format's: an implementation MAY expose other names, but one that exposes these SHALL keep their semantics, so that skills transfer.
- The four places where the format's discipline meets a tool call are stated as requirements: `select` takes a person's candidate or a harness's policy and never both, while `resolve` chooses nothing; `intention_firm` refuses a harness without a policy the subject holds; `commitment_accept` and `commitment_decline` take no policy because a party's status is a fact about their will; `unresolved` lists what still awaits a placement and why, from a dry resolution.
- `unresolved` is named in the text for the first time, closing the item the knowledge workspace carried about where to describe it.
- Issue #23 is closed with a comment naming the commit and how the answer differs from the proposal, if at all. The feedback file's row is the CLI's to update.

## Capabilities

### New Capabilities

- `harness-tools`: the reference tool set, its normative status, and the semantics an implementation exposing those names must keep.

### Modified Capabilities

None.

## Impact

- README: one new section and one line in Status saying the open issue is settled, which changes the counts the site repeats (twenty-five settled, none open).
- `docs/index.html`: the proof lead's counts, per the `landing-site` requirement that they match the feedback file. The site line changes only once the CLI's feedback file marks #23 settled, so that edit waits on the upstream row.
- A new spec, `openspec/specs/harness-tools/spec.md`, on archive.
- The set is verified against the released binary's actual tool list rather than copied from its documentation, which lists twenty-six names while its source registers `index` and `show` as well.
