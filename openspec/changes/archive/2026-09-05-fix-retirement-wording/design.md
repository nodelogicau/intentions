## Context

A wording-only correction left over from syncing draft-readme-spec. The MODIFIED delta kept the original requirement header, which OpenSpec requires for matching, and two untouched scenarios in other specs still used "status" loosely.

## Goals / Non-Goals

**Goals:**
- Every requirement header and scenario in the main specs uses the format's own vocabulary: retired, placement, stability, party status.

**Non-Goals:**
- Any change to behaviour, fields, or projections.

## Decisions

**RENAMED for the header, MODIFIED for the scenarios.** The header change is a rename with no body change, which is exactly what RENAMED is for. The two scenario rewordings need MODIFIED with the full block, because the archive sync replaces whole requirements.

**No synthesis.** The knowledge workspace already holds the decision this text should reflect. Recording a synthesis for a typo-grade fix would be noise for a reviewer.

## Risks / Trade-offs

- [The RENAMED FROM line must match the current header exactly] → Copied verbatim from the synced spec.
