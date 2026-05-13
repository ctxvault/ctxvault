# CtxVault v0.5.0 Mechanism Note: Governed Context Projection

Status: v0.5.0 public release artifact.

Governed context projection for AI work.

Boundary phrase for publication review: no target repository writes and no provider/model execution.

This is the v0.5.0 release-bound copy of the governed context projection
mechanism note. The evergreen project copy lives at
`docs/mechanism/governed-context-projection.md`.

## Mechanism

CtxVault v0.5.0 treats AI tool context as a governed handoff:

```text
reviewed evidence -> decisions and caveats -> portable context packets -> receipts
```

The mechanism records:

- the evidence considered
- the review decision for candidate context
- accepted, caveated, blocked, and omitted material
- projection output boundaries
- receipts for audit and rollback

The release claim is intentionally narrow: governed context projection for AI
work. v0.5.0 does not run an agent, call a provider/model, write to a target
repository, train a model, update model weights, or claim benchmark results.

## v0.5.0 Evidence Boundary

The public v0.5.0 release includes aggregate evidence from one private dogfood
path and three owner-selected OSS dry-runs:

| Evidence Set | Runs | Candidates | Caveated | Blocked | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Owner-selected OSS dry-runs | 3 | 121 | 20 | 101 | passed |

The public artifacts do not publish private dogfood receipts, private local
paths, raw source excerpts, provider/model outputs, or target repository
writes.

## Not Claimed

v0.5.0 does not claim:

- benchmark or leaderboard results
- reliability, accuracy, or coding-performance improvement
- adapter, runtime, provider/model, or hardware/cost compatibility
- automatic repository optimization
- stable Memory Governance Protocol
- Memory OS, RAG replacement, hallucination prevention, or security certification

## Review Path

Start with:

- `docs/mechanism/governed-context-projection.md`
- `release/v0.5.0/RELEASE_NOTES.md`
- `release/v0.5.0/v0.5.0-public-evidence-page-draft.md`
- `examples/v0.5.0-governed-context-projection/README.md`
