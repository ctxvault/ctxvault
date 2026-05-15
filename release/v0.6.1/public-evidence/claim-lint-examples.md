# Claim-Lint Examples For Public OSS Case Studies

Status: public-safe artifact for v0.6.1 evidence hardening. Published as
GitHub issue 14 comment:
`https://github.com/ctxvault/ctxvault/issues/14#issuecomment-4464512485`.

Use these examples before publishing any CtxVault public OSS case study,
quickstart, demo caption, release note, social post, or issue comment.

## Rule Format

Each example has:

- blocked claim;
- why it is blocked;
- safe rewrite;
- required receipt field;
- rollback if the claim escapes.

## Examples

### 1. Quality Judgment

Blocked claim:
`CtxVault proves this project has strong memory architecture.`

Why blocked:
This is a project-quality judgment. A read-only CtxVault case study can show
evidence paths and governance decisions, not certify architecture quality.

Safe rewrite:
`CtxVault inspected a pinned source snapshot and classified selected, omitted,
stale, blocked, and rollbackable evidence paths for this project.`

Required receipt field:
`claim_boundary.blocked` must include `quality_judgment`.

Rollback:
Remove or supersede the sentence anywhere it was published and verify the
public target no longer contains the quality claim.

### 2. Benchmark Or Performance Claim

Blocked claim:
`This case study shows the project improves agent accuracy and reduces tokens.`

Why blocked:
No benchmark or reproduced measurement exists in the case-study receipt.
Project-reported metrics, paper metrics, or README claims are source facts, not
CtxVault results.

Safe rewrite:
`Any benchmark or token-efficiency statement remains a source-reported claim and
is excluded from CtxVault's public conclusion unless a separate evaluation
receipt reproduces it.`

Required receipt field:
`facts_excluded` must name the metric and `claim_boundary.blocked` must include
`benchmark_or_performance_claim`.

Rollback:
Delete or correct the benchmark wording and add a corrective receipt if the
claim was public.

### 3. Compatibility Claim

Blocked claim:
`CtxVault is compatible with this memory/runtime/MCP system.`

Why blocked:
A read-only evidence pass does not execute adapters, start runtimes, call MCP
servers, install packages, or mutate target projects.

Safe rewrite:
`This case study treats the system as a source of evidence only; no runtime,
adapter, MCP, package, or target-write compatibility was tested.`

Required receipt field:
`boundary.runtime_or_adapter_executed=false`.

Rollback:
Remove compatibility wording across README, Pages, release notes, and social
copy; verify public surfaces after correction.

### 4. Maintainer Endorsement

Blocked claim:
`The maintainer agrees with CtxVault's findings.`

Why blocked:
Maintainer agreement requires explicit owner-supplied text or public comment.
An issue, repo, or project page is not an endorsement.

Safe rewrite:
`No maintainer endorsement is claimed. The case study uses public source refs
and CtxVault-local receipts only.`

Required receipt field:
`claim_boundary.blocked` must include `maintainer_endorsement`.

Rollback:
Remove endorsement wording and, if needed, publish a correction from the owner
account.

### 5. Security Or Privacy Claim

Blocked claim:
`This project is safe/private because CtxVault reviewed it.`

Why blocked:
CtxVault's leak scan and claim lint protect its own public artifacts. They do
not certify the target project's security, privacy, or compliance.

Safe rewrite:
`CtxVault leak-scanned the named public artifacts for this case-study draft; it
does not certify the target project's security or privacy.`

Required receipt field:
`leak_scan.files` and `leak_scan.result`.

Rollback:
Remove the security/privacy claim and rerun leak scan over the affected public
artifacts.

### 6. Stable Protocol Claim

Blocked claim:
`This demonstrates stable MGP support.`

Why blocked:
The current MGP work is fixture/read-model planning and private design. It is
not a stable protocol, SDK, adapter contract, or conformance suite.

Safe rewrite:
`This draft uses MGP-style read-model vocabulary as planning evidence; it does
not claim stable protocol support.`

Required receipt field:
`boundary.stable_mgp_or_protocol_claim=false`.

Rollback:
Replace stable-protocol language with fixture/read-model language and verify
all public surfaces.

### 7. Target Write Or Action Claim

Blocked claim:
`CtxVault can safely update the target repo based on this evidence.`

Why blocked:
The public case-study path is read-only. Target writes require a separate lane,
owner approval, before/after digests, verification, and rollback.

Safe rewrite:
`This case-study draft is read-only and does not authorize target writes.`

Required receipt field:
`boundary.target_file_written=false`.

Rollback:
Remove target-write wording; if any target mutation happened, open a corrective
receipt with before/after digests and revert or supersede the mutation.

## Minimal Lint Checklist

Before public copy ships, check for:

- quality, correctness, architecture, security, privacy, performance, adoption,
  benchmark, token-efficiency, compatibility, endorsement, stable protocol, and
  target-write claims;
- volatile facts without `checked_at_utc`;
- source-reported metrics phrased as CtxVault results;
- missing rollback;
- missing leak-scan file list;
- missing public/private boundary.

This file is the local source copy for the published issue 14 comment. It does
not push repository code, publish Pages, change a release, run a target
project, call a provider/model, or authorize target writes.
