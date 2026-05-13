# CtxVault v0.5.0 Mechanism Note: Governed Context Projection

Status: v0.5.0 public release artifact.

Governed context projection for AI work.

Boundary phrase for publication review: no target repository writes and no provider/model execution.

This note explains the mechanism behind CtxVault v0.5.0. It is an engineering
mechanism note, not a formal paper, benchmark report, security certification,
runtime claim, adapter compatibility claim, or provider/model evaluation.

## Summary

CtxVault treats AI tool context as a governed handoff, not as an automatic
memory stream.

The core mechanism is:

```text
reviewed evidence -> decisions and caveats -> portable context packets -> receipts
```

Before context reaches an AI tool, CtxVault makes the context boundary explicit:

- what evidence was considered
- what was selected
- what was caveated
- what was blocked or omitted
- which receipt records the decision
- how to audit and roll back the packet

The goal is not to make an AI tool more autonomous. The goal is to make context
influence inspectable before it reaches an AI work surface.

## Problem

AI tools can consume large amounts of project context, but the handoff often has
weak governance:

- the source boundary is unclear
- private or irrelevant material can be mixed into the prompt
- caveats are lost when context is compressed
- blocked material may be invisible to the reviewer
- there is no durable receipt for why a packet was allowed
- rollback can become a manual memory exercise

CtxVault v0.5.0 narrows the problem to a smaller and testable control point:
governed context projection.

## Mechanism

### 1. Evidence

CtxVault starts from source references and reviewable evidence. Evidence can be
local project material, sanitized examples, or other explicitly selected
context inputs.

The mechanism requires evidence to stay connected to source references. A
packet should not be just a free-form summary; it should retain enough
provenance for a human or tool to inspect why it exists.

### 2. Decisions

The reviewer or owner decides how candidate context should be handled:

- accepted: safe enough to include
- caveated: useful, but only with a visible warning or limitation
- blocked: should not be included
- omitted: not part of this projection

The decision is part of the output contract. It is not an invisible
intermediate step.

### 3. Projection

Projection turns reviewed evidence and decisions into a portable context packet
for AI tools, agents, and coding workflows.

Projection is intentionally narrower than runtime integration. It does not
execute an agent, call a provider/model, write to a target repository, or
promise adapter compatibility.

### 4. Receipts

Receipts record what happened:

- source references used
- selected and blocked items
- caveats
- quality and privacy checks
- target-profile dry-run status
- rollback guidance

The receipt is the audit surface. It lets a reviewer ask: what context was this
AI surface allowed to see, and why?

## What v0.5.0 Demonstrates

v0.5.0 demonstrates the mechanism with public-safe aggregate evidence and a
sanitized example.

The release includes aggregate evidence from one private dogfood path and three
owner-selected OSS dry-runs:

| Evidence Set | Runs | Candidates | Caveated | Blocked | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Owner-selected OSS dry-runs | 3 | 121 | 20 | 101 | passed |

The public artifacts intentionally do not publish private dogfood receipts,
private local paths, raw source excerpts, provider/model outputs, or target
repository writes.

Start with:

- `examples/v0.5.0-governed-context-projection/README.md`
- `release/v0.5.0/RELEASE_NOTES.md`
- `release/v0.5.0/v0.5.0-public-evidence-page-draft.md`

## What v0.5.0 Does Not Claim

This release does not claim:

- benchmark or leaderboard results
- reliability, accuracy, or coding-performance improvement
- adapter, runtime, provider/model, or hardware/cost compatibility
- automatic repository optimization
- stable Memory Governance Protocol
- Memory OS, RAG replacement, hallucination prevention, or security certification

These are future lanes only if they receive their own tests, receipts, versioned
environment evidence, rollback plan, and owner approval.

## Why This Is Not a Runtime

CtxVault v0.5.0 does not run an agent. It does not decide which task an agent
should perform. It does not execute tools on behalf of a model.

It governs the context packet before another AI work surface consumes it.

## Why This Is Not a RAG Replacement

RAG systems usually focus on retrieval and injection. CtxVault focuses on the
governance boundary around what is allowed to influence an AI work surface.

Retrieval can be one upstream source of candidate context in the future, but
governed projection is the release claim here.

## Why This Is Not a Memory OS

CtxVault v0.5.0 does not claim a general long-term memory substrate, automatic
self-learning loop, model weight update path, or universal memory lifecycle.

It records governed context handoffs and their receipts.

## Review Checklist

Use this checklist before describing the mechanism publicly:

- Does the wording keep the claim to governed context projection for AI work?
- Does it mention no target repository writes and no provider/model execution?
- Does it avoid benchmark, runtime, adapter, model, hardware, cost, and security
  claims?
- Does it point to the sanitized example rather than private dry-run material?
- Does it preserve the receipt, audit, and rollback boundary?

## Public Links

- Main project: `https://github.com/ctxvault/ctxvault`
- v0.5.0 release: `https://github.com/ctxvault/ctxvault/releases/tag/v0.5.0`
- Sanitized example: `https://github.com/ctxvault/ctxvault/tree/main/examples/v0.5.0-governed-context-projection`
