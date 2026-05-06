# E2 — Phase D 反馈闭环消融（占位）

> **状态**：未实施。先实施 E1，E2/E3 在 E1 验证完毕后再做。

## 协议（详见 `compares/APPLICATION_STUDY.md` §3.2）

* **Phase A**：保留（RAG retrieval 启用）
* **Phase D**：完整断电——不只是 `max_iterations: 1`，还要：
  - `feedback_control.enabled: false`
  - `phase_c.corpus_keeper.enabled: false`
  - `phase_e.enabled: false`
  - `feedback_control.seed_synthesis.enabled: false`
  - `feedback_control.mr_synthesis.enabled: false`
  - 环境变量 `BIOTEST_NO_TARGET=1`（Rank 4 `hypothesis.target()`）

## 实施思路

E2 不需要 monkey-patch —— 全部通过 config override 完成。

照搬 E1 的 wrapper 骨架：

```python
# E2_no_phase_d/run_e2.py
import biotest
from compares.ApplicationStudy.shared.config_helpers import (
    load_main_config, redirect_outputs,
)

cfg = load_main_config()
redirect_outputs(cfg, root="compares/ApplicationStudy/E2_no_phase_d/results")

# Phase D 完整断电
cfg["feedback_control"]["enabled"] = False
cfg["feedback_control"]["max_iterations"] = 1
cfg["feedback_control"]["seed_synthesis"]["enabled"] = False
cfg["feedback_control"]["mr_synthesis"]["enabled"] = False
cfg["phase_c"]["corpus_keeper"]["enabled"] = False
cfg["phase_e"]["enabled"] = False

import os; os.environ["BIOTEST_NO_TARGET"] = "1"

biotest.run_pipeline(cfg, phase_filter="A,B,C")  # 不跑 D 也不跑 E
```

⚠️ `BIOTEST_NO_TARGET` 这个 flag 在当前源码里**还不存在**——
`orchestrator.py::_run_mr_with_hypothesis` 里的两个 `target()` 调用是
hardcoded。E2 实施前要么：

1. 用 monkey-patch 把 `hypothesis.target` 替换成 no-op；
2. 或接受 Rank 4 残留（论文里说明 "Rank 4 contribution measured at < 5 pp,
   acceptable noise"）。

E2 实施时再决定。
