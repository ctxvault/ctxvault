# Claim-Lint Examples For Public Influence Drafts

Status: sanitized public example draft; not published.

Governed context projection for AI work.

Use this file before publishing v0.6.0 public influence copy. It shows how to
turn unsupported public case-study wording into source-bound text, caveats, or
blocked claims.

Public influence drafts keep these boundaries:

- no target repository writes;
- no provider/model execution;
- no runtime or adapter execution;
- no maintainer endorsement unless an explicit public source exists.

## Usage

Run the public draft claim checker against this file:

```bash
python scripts/check_v050_public_drafts.py release/v0.6.0/public-influence/claim-lint-examples.md
```

Expected output:

```text
public draft claim check passed for 1 files
```

## Examples

### 1. Quality Claim

Not allowed input:
`CtxVault proves mem0 has strong memory architecture.`

Why blocked:
That is a target-project quality judgment. The v0.6.0 public influence lane
can describe the pinned source snapshot, evidence categories, and governance
decision, but it does not score the target project.

Safe rewrite:
`CtxVault inspected a pinned public source snapshot and classified selected,
caveated, blocked, omitted, and rollbackable evidence paths.`

Receipt field:
`claim_lint.prohibited_claims_absent` includes
`target_project_quality_judgment`.

### 2. Performance Claim

Not allowed input:
`The case study shows mem0 improves agent accuracy and token efficiency.`

Why blocked:
No reproduced measurement or evaluation receipt exists for that statement.
Source-reported metrics can be recorded as source facts, but not as CtxVault
results.

Safe rewrite:
`No benchmark, leaderboard, accuracy, or token-efficiency result is claimed by
CtxVault in this public influence draft.`

Receipt field:
`evaluation_boundary.benchmark_or_leaderboard_claim=false`.

### 3. Compatibility Claim

Not allowed input:
`mem0 is compatible with CtxVault's runtime and adapters.`

Why blocked:
The public influence lane is read-only. It does not install packages, start a
runtime, execute adapters, call MCP servers, or mutate target files.

Safe rewrite:
`This draft treats mem0 as public evidence only; runtime, adapter, MCP, package,
and target-write compatibility are not evaluated.`

Receipt field:
`evaluation_boundary.runtime_or_adapter_execution=false`.

### 4. Maintainer Endorsement Claim

Not allowed input:
`mem0 maintainers agree with this case study.`

Why blocked:
Maintainer agreement requires an explicit public maintainer statement. Public
repository metadata and source files are evidence, not endorsement.

Safe rewrite:
`No maintainer endorsement is claimed. The draft uses public source refs and
CtxVault-local receipts only.`

Receipt field:
`claim_lint.prohibited_claims_absent` includes `endorsement_by_mem0`.

### 5. Security Or Privacy Claim

Not allowed input:
`CtxVault confirms mem0 is safe and private.`

Why blocked:
Claim lint and leak scan protect CtxVault's own public artifact boundary. They
do not certify the target project's security, privacy, or compliance.

Safe rewrite:
`CtxVault leak-scanned the public influence files for private paths and raw
secret markers; it does not certify the target project's security or privacy.`

Receipt field:
`leak_scan.result=pass_for_public_data_extract`.

### 6. Target Write Claim

Not allowed input:
`CtxVault can update the target repository from this evidence.`

Why blocked:
The v0.6.0 public influence path is read-only. Target writes require a separate
approval lane, before/after digests, verification, and rollback.

Safe rewrite:
`This public influence draft is read-only and does not authorize target writes.`

Receipt field:
`evaluation_boundary.target_files_written=false`.

## Minimal Checklist

Before public copy ships, verify that it:

- says what source evidence was selected, caveated, blocked, and omitted;
- keeps source-reported metrics separate from CtxVault results;
- names missing evidence for quality, performance, compatibility, security,
  privacy, endorsement, runtime, and target-write claims;
- includes rollback or correction language for public artifacts;
- keeps private paths, credentials, target internals, and unpublished receipts
  out of public text.
