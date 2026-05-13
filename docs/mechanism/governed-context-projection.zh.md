# CtxVault v0.5.0 机制说明：受治理的上下文投影

Status: v0.5.0 public release artifact.

Governed context projection for AI work.

Boundary phrase for publication review: no target repository writes and no provider/model execution.

这是一份 v0.5.0 的工程机制说明，不是正式论文、benchmark 报告、安全认证、
runtime 声明、adapter compatibility 声明，也不是 provider/model 评测。

## 摘要

CtxVault 把 AI 工具的上下文输入看成一个需要治理的交接过程，而不是自动流入
模型的“记忆”。

核心机制是：

```text
reviewed evidence -> decisions and caveats -> portable context packets -> receipts
```

在上下文进入 AI 工具之前，CtxVault 先把边界说清楚：

- 看过哪些 evidence
- 哪些内容被 selected
- 哪些内容需要 caveat
- 哪些内容被 blocked 或 omitted
- 哪个 receipt 记录了这个决定
- 如何审计和回滚这个 packet

目标不是让 AI 工具更自动，而是让“哪些上下文可以影响下一次 AI 工作”在进入
AI work surface 之前可检查、可审计、可回滚。

## 问题

AI 工具可以读取大量项目上下文，但上下文交接经常缺少治理边界：

- source boundary 不清楚
- private 或无关材料可能混进 prompt
- caveat 在压缩或摘要时丢失
- blocked material 对 reviewer 不可见
- 没有 durable receipt 解释为什么这个 packet 被允许
- 回滚依赖人的记忆，而不是可审计记录

v0.5.0 把问题收窄到一个可测试的控制点：governed context projection。

## 机制

### 1. Evidence

CtxVault 从 source references 和可审阅 evidence 开始。Evidence 可以是本地项目
材料、sanitized examples，或其他被明确选择的上下文输入。

机制要求 evidence 保持 source refs。Packet 不应该只是自由文本摘要，而应该保留
足够 provenance，让人或工具能检查它为什么存在。

### 2. Decisions

Reviewer 或 owner 决定 candidate context 应该如何处理：

- accepted：可以进入 packet
- caveated：有价值，但必须带着可见 caveat
- blocked：不能进入 packet
- omitted：本次 projection 不使用

Decision 是输出契约的一部分，不是隐藏的中间步骤。

### 3. Projection

Projection 把 reviewed evidence 和 decisions 变成 AI tools、agents 和 coding
workflows 可以携带的 context packet。

Projection 比 runtime integration 更窄。它不运行 agent，不调用 provider/model，
不写目标 repo，也不承诺 adapter compatibility。

### 4. Receipts

Receipts 记录发生了什么：

- 使用了哪些 source refs
- 哪些 items 被 selected 或 blocked
- 有哪些 caveats
- quality 和 privacy checks
- target-profile dry-run 状态
- rollback guidance

Receipt 是 audit surface。Reviewer 可以据此追问：这个 AI surface 被允许看到
什么上下文，为什么？

## v0.5.0 证明了什么

v0.5.0 用 public-safe aggregate evidence 和 sanitized example 证明机制形状。

Release 包含一个 private dogfood path 和三个 owner-selected OSS dry-runs 的
aggregate evidence：

| Evidence Set | Runs | Candidates | Caveated | Blocked | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Owner-selected OSS dry-runs | 3 | 121 | 20 | 101 | passed |

Public artifacts 不发布 private dogfood receipts、private local paths、raw source
excerpts、provider/model outputs 或 target repository writes。

建议先看：

- `examples/v0.5.0-governed-context-projection/README.md`
- `release/v0.5.0/RELEASE_NOTES.md`
- `release/v0.5.0/v0.5.0-public-evidence-page-draft.md`

## v0.5.0 不声称什么

这个 release 不声称：

- benchmark 或 leaderboard result
- reliability、accuracy 或 coding-performance improvement
- adapter、runtime、provider/model 或 hardware/cost compatibility
- automatic repository optimization
- stable Memory Governance Protocol
- Memory OS、RAG replacement、hallucination prevention 或 security certification

这些只能作为未来 lanes；只有分别具备 tests、receipts、版本化环境证据、rollback
和 owner approval 后，才能进入公开 claim。

## 为什么它不是 runtime

CtxVault v0.5.0 不运行 agent，不决定 agent 应该做什么任务，也不替模型执行
tools。

它治理的是另一个 AI work surface 使用上下文之前的 context packet。

## 为什么它不是 RAG replacement

RAG 通常关注 retrieval 和 injection。CtxVault 关注的是：哪些上下文被允许影响
AI work surface，以及这个允许过程如何被审阅、记录、审计和回滚。

未来 retrieval 可以成为 candidate context 的上游来源之一，但 v0.5.0 的 claim 是
governed projection。

## 为什么它不是 Memory OS

CtxVault v0.5.0 不是 general long-term memory substrate，不做 automatic
self-learning loop，不做 model weight update，也不声明 universal memory lifecycle。

它记录的是受治理的上下文交接和对应 receipts。

## 公开表达前的检查清单

公开描述这个机制前，先检查：

- 是否把 claim 保持在 governed context projection for AI work？
- 是否明确 no target repository writes and no provider/model execution？
- 是否避免 benchmark、runtime、adapter、model、hardware、cost 和 security claims？
- 是否链接 sanitized example，而不是 private dry-run 材料？
- 是否保留 receipt、audit 和 rollback 边界？

## Public Links

- Main project: `https://github.com/ctxvault/ctxvault`
- v0.5.0 release: `https://github.com/ctxvault/ctxvault/releases/tag/v0.5.0`
- Sanitized example: `https://github.com/ctxvault/ctxvault/tree/main/examples/v0.5.0-governed-context-projection`
