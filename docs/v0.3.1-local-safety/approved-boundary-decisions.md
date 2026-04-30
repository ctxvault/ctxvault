# CtxVault v0.3.1 Approved Boundary Decisions

Last updated: 2026-04-30

This file records owner-approved v0.3.1 boundary decisions for local safety,
model use, and connector expansion. These decisions preserve the deterministic
baseline and do not authorize a public release by themselves.

## Privacy Deletion Semantics

Approved:

- implement explicit, reviewed logical purge for derived data
- purge slice rows, slice FTS rows, redacted previews, optional embedding rows,
  and selected generated projection files
- retain governed source objects by default
- emit a logical purge receipt with reviewer, policy decision, purged refs, and
  a clear `secure_deletion_claim: none`

Not approved:

- automatic deletion or rewriting of source governed objects
- claiming app-level physical secure deletion from SSDs, APFS snapshots,
  backups, or filesystem caches
- silent purge without a review gate

## Model Adapter And External Send Policy

Approved:

- deterministic baseline remains model-free
- optional local model paths may be added later only with usage receipts
- remote model or embedding providers require explicit external-send consent,
  redaction mode, input refs, provider class, output contract, and receipt

Not approved:

- model adapters as baseline correctness
- silent remote reranking, embedding, enrichment, or durable truth promotion
- background model enrichment that bypasses review

## Markdown, Plugin, And Connector Expansion

Approved:

- continue Markdown-vault import/export as an adoption bridge
- treat Markdown and Obsidian-compatible files as source/projection surfaces,
  not canonical truth
- defer live connector expansion until slice selection, privacy preflight, and
  receipts are stable

Not approved:

- official Obsidian plugin claims
- broad Codex, Claude Code, Cursor, shell, or AI-chat live connectors before
  connector receipts, failure states, and review gates are stable
- direct note mutation that bypasses candidate review, provenance, privacy
  preflight, receipts, or rollback visibility
