# CtxVault v0.5.0 机制说明：受治理的上下文投影

Status: v0.5.0 public release artifact.

Governed context projection for AI work.

Boundary phrase for publication review: no target repository writes and no provider/model execution.

这是 governed context projection 机制说明的 v0.5.0 release-bound copy。长期维护的
项目版本在 `docs/mechanism/governed-context-projection.zh.md`。

## 机制

CtxVault v0.5.0 把 AI 工具上下文看成一个受治理的交接过程：

```text
reviewed evidence -> decisions and caveats -> portable context packets -> receipts
```

机制记录：

- 看过哪些 evidence
- candidate context 的 review decision
- 哪些内容被 accepted、caveated、blocked 或 omitted
- projection output 的边界
- 用于 audit 和 rollback 的 receipts

这个 release 的 claim 很窄：governed context projection for AI work。v0.5.0 不运行
agent，不调用 provider/model，不写目标 repository，不训练模型，不更新模型权重，也
不声明 benchmark result。

## v0.5.0 的证据边界

Public v0.5.0 release 包含一个 private dogfood path 和三个 owner-selected OSS
dry-runs 的 aggregate evidence：

| Evidence Set | Runs | Candidates | Caveated | Blocked | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Owner-selected OSS dry-runs | 3 | 121 | 20 | 101 | passed |

Public artifacts 不发布 private dogfood receipts、private local paths、raw source
excerpts、provider/model outputs 或 target repository writes。

## 不声称什么

v0.5.0 不声称：

- benchmark 或 leaderboard results
- reliability、accuracy 或 coding-performance improvement
- adapter、runtime、provider/model 或 hardware/cost compatibility
- automatic repository optimization
- stable Memory Governance Protocol
- Memory OS、RAG replacement、hallucination prevention 或 security certification

## Review Path

建议先看：

- `docs/mechanism/governed-context-projection.zh.md`
- `release/v0.5.0/RELEASE_NOTES.md`
- `release/v0.5.0/v0.5.0-public-evidence-page-draft.md`
- `examples/v0.5.0-governed-context-projection/README.md`
