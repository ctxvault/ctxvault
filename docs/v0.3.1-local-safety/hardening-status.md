# CtxVault v0.3.1 Hardening Status

## What Works

- `ctxvault.context-slice/v1` is an experimental rebuildable read model.
- Markdown knowledge, session turns, episodes, and compiled workstream state can
  be sliced into local deterministic context slices.
- `context-slice-rebuild` rebuilds `context_slices`, `context_slice_links`, and
  `context_slice_fts`.
- `context-search` works through Surface, CLI, and MCP without any model,
  embedding, remote service, or hosted API dependency.
- slice privacy classes control indexing:
  - `searchable_plain` is indexed as plain local text
  - `searchable_redacted` is indexed with deterministic redaction markers
  - `metadata_only` keeps body text out of FTS
  - `withheld` is not inserted into FTS
- selected-slice projection is preflight-gated. If projection commands receive
  `selected_slice_refs`, CtxVault writes a
  `ctxvault.privacy-preflight-receipt/v1` receipt before projection and blocks
  `block` decisions before writing output.
- projection receipts now carry `selected_slice_refs` and an embedded
  `privacy_preflight` section when slices are selected.
- `logical-purge-apply` removes derived slice rows, FTS rows, links, optional
  embedding rows, and optionally safe generated projection files. It keeps
  governed source objects and records tombstones for projection receipts that
  referenced purged slices.
- `doctor` reports slice-index health, stale slice sources, and projection
  receipts that reference slice refs absent from the current slice index.

## Intentional Non-Goals

- No vector search baseline.
- No graph product claim.
- No local model or remote model dependency for baseline correctness.
- No silent remote reranking, embedding, enrichment, or durable truth promotion.
- No automatic source-material clearing.
- No SSD, APFS snapshot, backup, or physical secure-wipe claim.
- No official Obsidian plugin.
- No Codex, Claude Code, Cursor, shell, or live connector expansion.
- No public release authorization from this hardening step alone.

## Operator Notes

- Use `context-slice-rebuild` after source objects change or after a logical
  purge when you want to rebuild derived slice indexes.
- Use `logical-purge-plan --include-projections` before clearing generated
  outputs that may reference purged selected slices.
- Treat projection receipts as audit evidence. Logical purge tombstones mark
  receipts as referencing purged derived data; they do not rewrite old receipts.
