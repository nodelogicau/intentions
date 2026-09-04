## Context

The intentions format has seven capability specs under `openspec/specs` and a reasoning chain of about thirty claims and syntheses in the knowledge workspace at `~/IdeaProjects/intentions-knowledge`. There is no document a reader can implement from. The DKF specification in the particulars repository is the model: its `README.md` is the normative text, its `openspec/specs` are fine-grained capabilities, and every change updates both.

Attempting to sketch a complete YAML example for each object surfaced three structural holes, now settled in the knowledge workspace: an intention had no `subject`, no object carried `source`, and retirement was a status field while every other event on an object was an append-only record. Several smaller holes remain and are listed under Open Questions. Each will be settled the same way, as a workspace synthesis first and a delta spec second, while the README is drafted.

## Goals / Non-Goals

**Goals:**
- A `README.md` that a second implementer could build from without reading the knowledge workspace.
- One complete, validating YAML example per object type and record type.
- The capability specs and the README agreeing on every field, so the specs remain the testable rendering of the README.
- Every decision made during drafting traceable to a claim or synthesis.

**Non-Goals:**
- Any implementation. No CLI, no validator, no resolver.
- Federation across workspaces. The README will name it as deferred, as the DKF README did for public discovery before its v0.1.
- Declaring a v0.1. The README's Status section will say the format is in draft and what is stable.
- Splitting the seven capability specs into finer ones to match the particulars repository's granularity. That can follow when a change needs it.

## Decisions

**README as normative text, specs as its testable rendering.** Alternative: keep the capability specs as the only source of truth and generate a README from them. Rejected because the DKF README earns its readers through prose that explains why, and the philosophy behind this format is the reason it exists; a generated field list would lose that. The specs stay the place where every requirement has a scenario.

**Same section structure as the DKF README.** Problem, Approach, Core Object Types, Object Model, File Layout, Design Principles, Status. Alternative: organise by lifecycle (intend, resolve, commit, reconsider). Rejected for the first draft because a reader who knows DKF should recognise the shape immediately, and the Object Model section can carry the lifecycle as a diagram.

**Subject on intention, required on disk, defaulting from configuration.** Alternative: keep ownership implicit as the workspace owner. Rejected because objects must be portable between workspaces, and this session moved this very workspace's files between two workspaces; implicit ownership would have silently reassigned every intention. The DKF scope rule is the precedent: the writer applies the default, the file always says.

**Source block on every object and record, author required on intention and availability.** Alternative: no provenance, on the grounds that git commit authorship suffices. Rejected because the founding claim of the format is that the same schedule is authentic or imposed depending on who authors it, and a format that cannot tell a harness-drafted intention from a person-written one has lost that axis. The block reuses DKF's shape as a pattern, not a schema dependency. Harness alone is not enough on an intention because a tool cannot intend.

**Retirement as an appended record, no status field.** Alternative: keep `status` and add `reason` and `timestamp` beside it. Rejected because that leaves two places that can disagree about whether an object is live. With a single `retired` block, active is the absence of the block, kinds are per type, `superseded_by` is required exactly when kind is `superseded`, and `retired.kind` alone joins the projection.

**Record taxonomy stated explicitly.** Objects are intention, availability, commitment: mutable live state. Records are events about objects: resolution stands alone because it relates several objects and recurs; acknowledgement and retirement are embedded because each is about exactly the object it sits in. The README's Object Model section will draw this.

**Open questions are settled in the workspace before they land in the README.** Alternative: decide in the README and backfill. Rejected because the chain of reasoning is the format's own justification and the workspace is where a reviewer can see why.

## Risks / Trade-offs

- [The README and the specs drift as the draft evolves] → The final task is a field-by-field reconciliation pass, and the archive step syncs delta specs into main specs so the two are checked against each other at least once.
- [Breaking changes to specs with no implementation invite unbounded churn] → Each change is tied to a workspace synthesis; nothing changes in the specs without a recorded reason.
- [The projection hash depends on canonical serialisation, which is not yet defined] → Listed as an open question that must close before the Versioning section is written; the README cannot show a hash example without it.
- [Source on every record adds weight to small files] → Accepted; DKF carries the same block and reviewers rely on it.
- [Philosophical prose crowds out normative text] → The Approach section carries the philosophy once; object sections say SHALL and show YAML.

## Open Questions

Each is to be settled as a claim or synthesis in the knowledge workspace, then captured as a delta spec in this change.

- Format name and object prefix convention. The syntheses still say DCOMMITMENT from the DKF era; the specs say COMMITMENT and `cmt_`.
- Where the activity-type vocabulary lives. Leaning toward the DKF topics precedent: small, lowercase, in a workspace conventions file, not spec-fixed.
- Instance-generation trigger for standing intentions: who materialises instances, over what horizon, and whether they are written to disk before one is resolved.
- Canonical field order and serialisation, which the projection hash already assumes.
- An assertion `timestamp` on objects, distinct from the id's minting time, so backdating is possible and the availability horizon default has a defined origin.
- `index.yaml` as a derived cache, assumed by validation and resolution but never specified.
- Whether a single workspace may hold intentions for several subjects, or whether that is federation and deferred.
- Whether availability renewal is an edit to `valid_until` or a supersession by a new object, now that supersession is a retirement kind.
- Whether a harness-drafted intention needs a confirmation act before it may become firm.
