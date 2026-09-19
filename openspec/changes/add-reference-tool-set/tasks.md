## 1. Verify the set against the binary

- [x] 1.1 Call `tools/list` on `intentions serve --mcp` over stdio and record the names and parameter schemas the v0.11.0 binary exposes
- [x] 1.2 Diff against `docs/mcp.md` and the proposed list; settle whether `index` and `show` are in the reference set; report any discrepancy upstream on intentions-cli

## 2. README

- [x] 2.1 Add `## Reference Tool Set` between Status and References: the standing sentence, the parameter-typing paragraph, the grouped table, and the four semantics stated with SHALL
- [x] 2.2 Object Model, resolution lifecycle: one sentence naming `unresolved` as the inventory of intentions still carried without a plan
- [x] 2.3 Status: the open-issue clause becomes settled, counts to twenty-five settled and none open

## 3. Specs and site

- [x] 3.1 `openspec validate --changes` passes
- [x] 3.2 Site proof lead: counts follow the feedback file; edit only once the CLI's row for #23 is no longer open, per the `landing-site` requirement

## 4. Close out

- [x] 4.1 Commit and push
- [x] 4.2 Close #23 with a comment naming the commit and where the answer differs from the proposal
- [ ] 4.3 Archive with sync so `harness-tools` lands in the main specs
- [ ] 4.4 Knowledge workspace: a claim for the reference set's standing and a qualification synthesis on the spine; commit and push
