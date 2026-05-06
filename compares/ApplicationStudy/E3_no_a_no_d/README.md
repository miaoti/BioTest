# E3 — Phase A + Phase D 双消融（占位）

> **状态**：未实施。

## 协议

* **Phase A**：关闭，naive prompt-stuffing 替代 RAG（同 E1）
* **Phase D**：完整断电（同 E2）

## 实施思路

E3 = E1 的 monkey-patches **并集** E2 的 config overrides。

```python
# E3_no_a_no_d/run_e3.py
# 1. 应用 E1 patches（disable RAG，naive prompt-stuffing）
from compares.ApplicationStudy.E1_no_phase_a.patches import apply_patches
apply_patches(spec_dump_path="compares/ApplicationStudy/shared/raw_spec_dump.txt")

# 2. 应用 E2 config overrides（disable Phase D）
import biotest
from compares.ApplicationStudy.shared.config_helpers import (
    load_main_config, redirect_outputs,
)
cfg = load_main_config()
redirect_outputs(cfg, root="compares/ApplicationStudy/E3_no_a_no_d/results")
# E2 风格的 Phase D 断电（详见 E2_no_phase_d/README.md）

# 3. 跑
biotest.run_pipeline(cfg, phase_filter="B,C")  # A 跳过、D 不跑
```

实施时把 E1 的 patches 拆成单独的 `patches.py` 模块，方便 E3 import 复用。
