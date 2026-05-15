# Public-Safe Case-Study Matrix

Status: public-safe artifact for v0.6.1 evidence hardening. Published as
GitHub issue 15 comment:
`https://github.com/ctxvault/ctxvault/issues/15#issuecomment-4464512768`.

This matrix compares candidate OSS case studies only by governance dimensions.
It does not rank project quality, security, performance, adoption,
compatibility, maintainer endorsement, or stable protocol support.

## Matrix

| Candidate | Status | Source-Fact Status | Pinned Ref | Allowed Public Artifact | Blocked Claims | Leak Scan | Rollback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mem0 | historical v0.6.0 case-study reference | pinned evaluation exists; volatile repo metadata requires recheck before reuse | v0.6.0 receipt-bound commit/evidence refs | sanitized extract and governance deep dive already bounded by v0.6.0 receipts | quality, performance, security, compatibility, endorsement, stable protocol, target-write claims | required before any new public copy | remove or supersede v0.6.0 public extract/copy through corrective receipt |
| Context Harness | next candidate intake only | official GitHub/docs refs checked; no CtxVault evaluation run | `f691f13ebf816e2f0f89c1fcaf8d4841c63e6a0d` from GitHub API on 2026-05-15 | future public-safe extract draft after owner approval | project-quality, benchmark, compatibility, endorsement, MCP-support-by-CtxVault, target-write claims | not run; required before publication | delete candidate receipt or supersede with updated source-fact receipt |
| Letta | second-wave candidate | official repo/docs refs require recheck before use | not pinned in v0.6.1 | candidate note only | memory-quality, agent-quality, benchmark, compatibility, endorsement, stable memory-runtime claims | not run | leave parked or create future candidate receipt |
| LangGraph memory | conformance-profile candidate | official memory docs require recheck before use | docs URL only; no repo deep-dive pin | taxonomy/conformance profile only | ecosystem-quality, runtime compatibility, benchmark, adoption, endorsement claims | not run | leave parked or supersede with a profile receipt |
| Future owner-selected OSS | planned row template | must record primary source URL, checked_at, pinned commit/tag/release/doc version | required before extraction | public-safe extract draft, claim-lint result, omitted-evidence table, rollback instructions | all unsupported quality, security, performance, compatibility, endorsement, stable protocol, target-write claims | required before publication | delete/supersede local draft; if published, corrective receipt and public verification |

## Required Columns For New Rows

- `candidate`
- `status`
- `source_fact_status`
- `pinned_ref`
- `allowed_public_artifact`
- `blocked_claims`
- `leak_scan_status`
- `rollback_target`
- `side_effect_boundary`

## Publication Gate

A row may become public only when all of these are true:

- primary source refs are recorded;
- `checked_at_utc` is present;
- pinned ref is present or the row is explicitly docs-only;
- claim-lint has no unblocked quality, performance, security, compatibility,
  endorsement, stable-protocol, or target-write claims;
- leak scan names every public artifact;
- rollback target is written before publication;
- owner approves the exact public target.

## Local Boundary

This file is the local source copy for the published issue 15 comment. It does
not push repository code, publish Pages, change a release, run a target
project, call a provider/model, execute an MCP server, install a package,
promote memory, or authorize target writes.
