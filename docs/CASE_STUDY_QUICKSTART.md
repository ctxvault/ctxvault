# CtxVault Case Study Quickstart

Status: public-safe local draft for v0.6.1. This document describes a manual
read-only preview workflow. The future CLI is not implemented.

## Goal

Create a case-study preview that can be audited before anything is published,
run, or written to a target project.

The preview answers four questions:

- What evidence is allowed?
- What claims are blocked?
- What evidence is missing?
- How would we roll back the CtxVault artifacts?

## No Target Mutation

Do not create issues, pull requests, discussions, branches, tags, releases, or
files in the target project. Do not contact maintainers. Do not run target
code. Do not start an MCP server. Do not install target packages. Do not call a
provider/model. Do not promote memory.

## Step 1: Select And Pin The Target

Record:

- repository or docs URL;
- commit, tag, release, or docs version;
- checked_at timestamp;
- license if available;
- volatile facts that must be rechecked before publication.

If the target cannot be pinned, keep the row as docs-only or candidate-only.

## Step 2: Source-Fact Receipt

Create a source-fact receipt with:

- primary source refs;
- verification method;
- selected evidence;
- omitted evidence;
- stale or volatile facts;
- source facts that are missing.

Template:
`templates/case-study-preview/source-fact-receipt.template.json`

## Step 3: Decision Table Template

| State | Decision | Test | Audit | Rollback |
| --- | --- | --- | --- | --- |
| Allowed | Use only source-backed statements. | Every statement has a source ref. | Receipt plus local draft. | Delete or supersede the local draft. |
| Blocked | Quality, security, performance, compatibility, endorsement, stable-protocol, runtime, target-write, and maintainer-intent claims. | Claim lint has no unblocked item in these categories. | Claim-lint receipt. | No target rollback if nothing was published or executed. |
| Missing | Runtime behavior, benchmark, security review, compatibility proof, maintainer intent, release-artifact integrity. | Missing evidence remains explicit. | Missing-evidence table. | Supersede with a later approved receipt. |
| Rollback | Remove or supersede generated CtxVault artifacts. | Artifact paths are listed. | Git diff plus fixture receipt. | Delete/supersede docs, fixtures, tests, and matrix block. |

## Step 4: Claim Lint

Use this rule before writing public copy:

If a claim needs evidence about quality, security, performance,
compatibility, maintainer endorsement, stable protocol behavior, runtime
behavior, target writes, provider/model calls, or memory promotion, block it
until a receipt exists.

Safe wording:

- "The public docs describe..."
- "The local draft maps documented surfaces to CtxVault constraints..."
- "This has not been run or validated for compatibility..."

Blocked wording:

- "CtxVault validates this project."
- "This project is secure, fast, or production-ready."
- "This project is compatible with CtxVault."
- "The maintainers endorse this case study."
- "The MCP behavior was tested by CtxVault."

Template:
`templates/case-study-preview/claim-lint.template.json`

## Step 5: Public-Safe Extract Draft

The extract draft must include:

- source boundary;
- selected evidence;
- omitted evidence;
- blocked claims;
- missing evidence;
- allowed/blocked/missing/rollback decision table;
- local boundary statement.

The draft is not public until the owner approves the exact target and rollback
path.

Template:
`templates/case-study-preview/public-safe-extract.template.md`

## Step 6: Matrix Row

Add or update a row with these columns:

- candidate;
- status;
- source_fact_status;
- pinned_ref;
- allowed_public_artifact;
- blocked_claims;
- leak_scan_status;
- rollback_target;
- side_effect_boundary.

## Future CLI Is Not Implemented

The intended future shape is a read-only preview command:

```text
ctxvault oss-case-study preview \
  --repo-url https://github.com/owner/repo \
  --commit <sha> \
  --output .ctxvault/case-study
```

That command is not implemented by this quickstart. Before implementation, its
dry-run output, receipt schemas, filesystem scope, network scope, and rollback
must be approved.

## Local Template Validator

The current local validator checks only the case-study preview templates:

```bash
python3 scripts/validate-case-study-templates.py
```

It does not fetch, clone, inspect, or run a target project.

## Rollback

Delete or supersede the quickstart, generated local receipts, public-safe draft,
matrix row, and tests. If anything was published later, create a corrective
receipt and verify the public rollback target.
