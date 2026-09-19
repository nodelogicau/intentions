## Context

intentions-cli v0.11.0 exposes one MCP tool per CLI operation over stdio, documented in its `docs/mcp.md`: six intention tools, five availability tools, five commitment tools, `generate`, `resolve`, `select`, `unresolved`, `check`, `acknowledge`, `bounds`, `validate` and `workspace_status`. Its source also registers `index` and `show`, which the documentation table omits. Results equal the CLI's `--json` output, errors carry the CLI's codes, and every refusal a verb makes the tool makes. The server tells the model these names are the implementation's, not the format's.

DKF's README carries a "MCP Server Tools" section that describes the reference server's tools in tables, and particulars specs the tool-facing discipline as an `agent-guidance` capability. Skills written for particulars transfer because of that section.

## Goals / Non-Goals

**Goals:**
- A second implementation can expose a tool surface a skill written for the first will work against.
- The four semantics that carry the format's discipline into a tool call are stated as requirements, not left to documentation.
- The appendix is verified against the binary, not transcribed from its docs.

**Non-Goals:**
- Mandating MCP, or any transport. The set is a naming and semantics convention for whatever a harness calls.
- Specifying result shapes field by field. Results are the implementation's non-interactive output; what is fixed is that the tool and the verb return the same thing.
- Changing any verb.

## Decisions

**Reference, not required.** The names are a reference set. An implementation MAY use others; one that exposes a listed name SHALL keep its semantics and accept its parameters. This is the same standing DKF gives its names and it is the weakest rule that still makes skills portable.

**Grouped by object, named by verb.** `intention_add`, `availability_renew`, `commitment_decline`; the operations that act on the workspace as a whole (`generate`, `resolve`, `select`, `unresolved`, `check`, `acknowledge`, `bounds`, `validate`, `workspace_status`) are bare. This is what the implementation already does and there is no reason to differ from it.

**Parameters typed after the format.** A window is `{calendar, clock, relative: {target, relation, gap}}`, a duration is a string or `{nominal, min, max}`, `serves` is a list of `{id, role}`, `source` is `{author, harness, model}`. The appendix says this once at the top rather than per row.

**Four semantics are requirements; the rest is a table.** `select`'s candidate-or-policy, `intention_firm`'s refusal without a policy, the absence of any policy on `commitment_accept` and `commitment_decline`, and `unresolved`'s status vocabulary are where the format's rules (flags never decisions, every object says who wrote it, a party's status is theirs) meet a tool call. They are stated with SHALL. Everything else in the table is descriptive.

**`unresolved` is named in the text.** The verb has no counterpart in the draft. Its statuses (`ready`, `blocked`, `no_candidates`, `incomplete`, `unresolvable`) are derived from a dry resolution and are the vocabulary a harness uses to decide what needs a person. It is described in the appendix and, in one sentence, in the Object Model's resolution lifecycle as the inventory of intentions still carried without a plan.

**Verify against the binary.** The task list has the implementer call `tools/list` on `intentions serve --mcp` over stdio and diff the names against the appendix, so `index` and `show` are settled by what the binary exposes rather than by which document is read.

**Placement and status.** A `## Reference Tool Set` section between Status and References, opening with the sentence that gives it its standing. The Status paragraph's open-issue clause becomes "all twenty-five settled" only in the commit that lands the appendix; the site follows when the CLI's feedback file marks #23.

## Risks / Trade-offs

- [The set drifts as the CLI adds verbs] → The appendix says it reflects v0.11.0 and the feedback file is the record of divergence; the same tally discipline as the second-reader counts.
- [A SHALL on tool semantics in a file format spec] → Scoped to implementations that choose to expose the listed names. An implementation that names nothing the same is bound by nothing here.
- [Two documents disagree about the set today] → Resolved by the binary, and the discrepancy reported upstream.

## Migration Plan

Prose and one new spec. Commit, push, archive with sync. Close #23 with a comment. Knowledge workspace: one claim and a qualification synthesis on the spine.

## Open Questions

- Whether `workspace_status` belongs in the reference set or is an implementation convenience. Lean: include, since a harness's first call in a session is to learn where it is.
