# BioTest Application Study — Phase A / Phase D 贡献消融实验设计

> 配套文档：`compares/DESIGN.md`（vs baselines 比较协议）。本文件正交
> 于 DESIGN.md：DESIGN.md 回答 *"BioTest vs 其它工具谁更强"*；本文件
> 回答 *"BioTest 内部 Phase A 与 Phase D 各自贡献多少"*。两份文档共
> 用 §3 度量、运行预算、Phase-3 mutation 工具链。
>
> 状态：deferred — 协议先冻结，等主线 Phase A–D 评估完成后再执行。

---

## 1. 动机 (Motivation)

BioTest 的论文叙事建立在两根支柱上：

* **支柱一（spec-grounded）**：Phase A 通过 RAG 把 VCF/SAM 规范文本（2,048 切片、453 条可测试规则）显式接入 MR 挖掘，让 LLM 输出可追溯到规范原句、杜绝幻觉。
* **支柱二（feedback-driven）**：Phase D 的迭代闭环（SCC + 覆盖率 + 盲区工单 + 9 层 Rank 杠杆）在 MR-only 工具的 25–40 % 行覆盖率天花板（Liyanage & Böhme ICSE'23；Ba 2025）之上继续推进。

任何评审者都会问：**"砍掉哪根支柱后，工具还能产出有意义的 bug？反过来，是不是其中一根支柱就足够撑起所有收益？"** 本研究用经典 2×2 析因消融（fractional factorial DOE）回答这个问题。

---

## 2. 配置矩阵 (Configurations)

完整 2×2 析因，**3 个待跑配置 + 1 个 implicit baseline**（E0 已在主线评估里产出，不需要额外运行）：

| ID | Phase A | Phase D | 描述 | 状态 |
| :--- | :---: | :---: | :--- | :--- |
| **E0** | ✓ | ✓ | Full BioTest | implicit（主线产出复用）|
| **E1** | ✗ | ✓ | spec-blind LLM + 反馈闭环 | **跑** |
| **E2** | ✓ | ✗ | spec-grounded + 单轮 B+C | **跑** |
| **E3** | ✗ | ✗ | spec-blind + 单轮 | **跑** |

从这 4 个 cell 可解出三组关键统计量：

* **Phase A 主效应** $= \tfrac{1}{2}\big[(E0-E1) + (E2-E3)\big]$
* **Phase D 主效应** $= \tfrac{1}{2}\big[(E0-E2) + (E1-E3)\big]$
* **A×D 交互效应** $= (E0-E1) - (E2-E3)$

只有 E3 那一格能给出交互项；任何抛弃 E3 的"3 配置替代方案"都会损失这一信息。

---

## 3. 关键实现细节 (Implementation Specification)

> ⚠️ "去掉 Phase A" 与 "去掉 Phase D" 各有强弱两种语义。下面的选择直接决
> 定结论的解读，必须在跑实验之前一次性钉死。

### 3.1 Phase A 关闭语义：选择 *naive prompt-stuffing* 而非 *zero-shot*

**两种候选**：

| 语义 | 实现 | 测什么 |
| :--- | :--- | :--- |
| zero-shot（最严格）| LLM 完全无 spec 上下文，仅给"你是 VCF/SAM 测试架构师"+ schema | 测 *spec 接入是否必要* |
| naive prompt-stuffing（推荐）| 把 `data/raw_tex/VCFv4.5.tex` + `SAMv1.tex` pylatexenc 转换后的纯文本截前 32k tokens 整段塞进 system message，**不启用 `query_spec_database` Tool** | 测 *retrieval 架构是否必要*（已经把 spec 给 LLM 了） |

**采用 naive prompt-stuffing**。理由：

1. zero-shot 是极弱基线，LLM 只能依靠训练数据里的 VCF/SAM 知识，结果几乎肯定大幅退步——但那只能证明 *"spec 内容必须到达 LLM"*，无法证明 *"必须用 RAG"*。
2. naive prompt-stuffing 是 Fuzz4All（ICSE'24）"raw-prompt" 变体的同构对照——RAG 综述 2025 也以此为标准 baseline。如果 RAG 仍能击败 naive prompt-stuffing，结论就强很多：*"不是有 spec 就行，retrieval 架构本身贡献显著"*。
3. 它把 prompt token 数量与 E0/E2 控制在同一量级（±10%），消除"prompt 长度"作为 confounder。

**落地清单**：

* `mr_engine/agent/engine.py::create_mr_agent` 在 `--no-rag-tool` flag 下不绑定 `query_spec_database` 工具；
* `mr_engine/agent/prompts.py::build_system_prompt` 切到 `prompts/raw_spec_dump.txt` 模板（含整段 spec 文本）；
* `mr_engine/dsl/compiler.py` 的 evidence hydration 跳过 chunk_id 校验，因为 LLM 没有 chunk_id 可引；
* `feedback/scc_tracker.py` 在该模式下输出 `n/a`（SCC 无意义——盲区不是用规则索引定位的）。

### 3.2 Phase D 关闭语义：完整断电，不只关闭外层循环

**两种候选**：

| 语义 | 实现 | 测什么 |
| :--- | :--- | :--- |
| 仅关循环（弱）| `max_iterations: 1`，所有 Rank 1/4/6/8/9–13 杠杆**保留** | 测 *是否有第 2 轮+ 才有用* |
| 完整断电（推荐）| `max_iterations: 1` + `feedback_control.enabled: false` + `phase_c.corpus_keeper.enabled: false` + `phase_e.enabled: false` + `BIOTEST_NO_TARGET=1` 关闭 `hypothesis.target()` + 所有 `mr_synthesis` / `seed_synthesis` flags 全 false | 测 *Phase D 整套机制是否必要* |

**采用完整断电**。理由：

1. Rank 1 (seed synthesis)、Rank 8 (corpus keeper)、Rank 4 (`hypothesis.target()`) 这些杠杆即使在单轮内也会激活——只关外循环并不能真正测出"无反馈"的下界。
2. 论文叙事里 Phase D 不只是"多跑几轮"——它是 SCC + 覆盖率 + 盲区 + 9 层 lever 的整体设计。E2 / E3 必须真正关掉所有这些机制，结论才指向"整套 Phase D 设计有用"，而不是"多迭代有用"（后者过于平庸）。
3. corpus_keeper 与 Phase E 的 augment 输出会被下游 Phase-3 mutation harness 显式 union 进 corpus（详见 `compares/scripts/phase3_jazzer_pit.sh`）。E2/E3 必须关闭这两路，否则 mutation 度量被污染。

**落地清单**（4 行 yaml override + 1 个环境变量）：

```yaml
feedback_control:
  enabled: false
  max_iterations: 1
phase_c:
  corpus_keeper:
    enabled: false
phase_e:
  enabled: false
```

加 `BIOTEST_NO_TARGET=1`（`orchestrator.py::_run_mr_with_hypothesis` 在该 env 下跳过两个 `target()` 调用）。

### 3.3 −A 与 −D 的随机性控制

* `global.seed_rng=42` 固定；Hypothesis `derandomize=True`；每 rep 用不同子种子（42/43/44）。
* **同一 cell 同一变体共用同一份起始种子**（`seeds/<fmt>/`），把 corpus 起点钉死。
* **关闭 LLM 的随机性**：所有变体强制 `temperature=0.0`、固定模型版本 `deepseek-chat-v3.0` 的 snapshot id。
* 同一 rep 里所有变体（E1/E2/E3）按相同 wall-clock 顺序启动，避免 Groq/DeepSeek 当日配额影响导致跨 rep 偏置。

---

## 4. 度量 (Metrics)

完全沿用 `compares/DESIGN.md §3` 的五大度量；新增两个 BioTest-内部度量以使 ablation 信号更敏锐：

1. **Validity Ratio**（DESIGN §3.1）—— 生成文件的合规率
2. **Structural Coverage Growth**（DESIGN §3.2）—— 行/分支覆盖随时间
3. **Mutation Score**（DESIGN §3.3）—— PIT / mutmut / cargo-mutants / mull
4. **Real-Bug Detection Rate**（DESIGN §3.4）—— `compares/bug_bench`
5. **TTFB**（DESIGN §3.5）—— 首发 bug 的中位 wall-time
6. **🆕 MR Yield**（per-iteration）—— Phase B 编译通过的 MR 数 ÷ LLM 调用数；衡量 LLM "产出效率"
7. **🆕 Hallucinated-MR Rate**（仅 −A 变体有意义）—— 被 Pydantic / 白名单 / chunk_id 验证拦截的 MR 占总输出的比例；这是 Phase A 主效应最直接的证据

---

## 5. 实验协议 (Protocol)

**SUT 集合**（与 DESIGN.md §4.1 对齐）：6 个 cell——`htsjdk(VCF)`, `htsjdk(SAM)`, `vcfpy(VCF)`, `noodles-vcf(VCF)`, `biopython(SAM)`, `seqan3(SAM)`。

**时间预算**：每 cell 2 h × 3 reps，对应 DESIGN.md 主预算同档（满足 Klees CCS'18 ≥3 reps + ≥6 h 累计的下限要求）。覆盖率/SCC 在 `{1, 10, 60, 300, 1800, 7200}` s 对数节拍采样。

**Cell 矩阵与总预算**：

| | htsjdk-VCF | htsjdk-SAM | vcfpy | noodles | biopython | seqan3 | 单变体 cell-时 |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: | --: |
| E1 (−A) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 × 2 h × 3 reps = 36 h |
| E2 (−D) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 36 h |
| E3 (−A,−D) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 36 h |
| **合计** | | | | | | | **108 wall-hours** |

E0 复用主线评估结果，不重跑。4-way 并行 ≈ 27 h ≈ 1.5 天。

**统计检验**：成对 Mann-Whitney U（α=0.05），效应量 Vargha-Delaney $\hat{A}_{12}$（large 阈值 0.71）。每个度量在每个 SUT 上单独检验，全工具汇报用 sign test 整合。pp 差异 < 1 pp 时显式标注 *not statistically distinguishable*。

---

## 6. 假设与预期结果 (Hypotheses)

| 假设 | 预期 | 推理依据 |
| :--- | :--- | :--- |
| **H1（A 主效应）**| E1 / E3 的 hallucinated-MR rate 从 0 % 上升到 30–60 %；MR yield 下降 ≥ 50 %；line coverage 比对应 (A=on) 配置低 4–10 pp | LLM 没有规范 anchor 时倾向发明非法 transform 名；naive prompt-stuffing 不能完全替代 retrieval 的"语义靠近"信号 |
| **H2（D 主效应）**| E2 / E3 的 final line coverage 比对应 (D=on) 配置低 8–18 pp；mutation score 低 5–12 pp | MR-only 在我们 Run 1 数据是 ~36 % vs 完整 Phase D 的 Run 6 是 ~47 %（htsjdk-VCF）|
| **H3（A×D 交互）**| 交互效应 ≤ 2 pp，统计上不显著 | A 主管 *MR 质量*，D 主管 *探索深度*；两者机制基本正交 |
| **H4（floor 验证）**| E3（−A−D）退化到接近 DESIGN.md 的 Pure Random + structure-aware 起点（约 25–35 % 行覆盖、几乎无 real-bug 检出） | 两个支柱同时拿掉后，框架退化为"白名单 transform 的单轮 fuzzing"，其覆盖能力应接近 Pure Random + 模板 |

* H1 + H2 都成立 → 论文最希望的"两根支柱都必要"叙事。
* H3 成立 → 加分项："A 与 D 是模块化的、各自独立可替换"。
* H3 不成立（交互显著）→ 也是有意思的发现："A 与 D 之间有协同放大效应"。

---

## 7. 实施细节 (Implementation Layout)

```
compares/scripts/application_study/
├── README.md                           # 矩阵 + 复现命令
├── configs/
│   ├── E1_no_phase_a.yaml              # naive prompt-stuffing + Phase D on
│   ├── E2_no_phase_d.yaml              # RAG on + 完整断电 Phase D
│   └── E3_no_a_no_d.yaml               # 两者皆关
├── prompts/
│   └── raw_spec_dump.txt               # E1 / E3 用：整段 spec 直塞 system msg
├── run_application_study.sh            # 3 cfg × 6 SUT × 3 rep
└── aggregate_application_study.py      # Mann-Whitney + Â12 + 渲染 §6 表格
```

**E1 / E3 共用同一个 `raw_spec_dump.txt`**：把 `data/raw_tex/VCFv4.5.tex` + `SAMv1.tex` 经 `pylatexenc` 转纯文本后截前 32k tokens 拼接。三个变体的 prompt 总 token 数控制在 ±10 % 以内（必要时 padding/truncate），消除"prompt 长度"作为 confounder。

**复现命令**：

```bash
# 1.5 天，4-way 并行
bash compares/scripts/application_study/run_application_study.sh \
    --suts htsjdk_vcf,htsjdk_sam,vcfpy,noodles,biopython,seqan3 \
    --reps 3 --budget 7200

# 聚合 + 渲染最终表
py -3.12 compares/scripts/application_study/aggregate_application_study.py \
    --runs results/application_study/ \
    --baseline results/main_run/ \
    --out documents/paper/application_study_tables.md
```

---

## 8. 限制与威胁 (Limitations & Threats to Validity)

| 威胁 | 缓解 |
| :--- | :--- |
| LLM 单一选型（DeepSeek-V3）| 在 *Limitations* 章节明确写出；后续可在 htsjdk-VCF 单 cell 上加做 LLM-provider 敏感性，但不在本研究的 3 配置范围内 |
| 2 h × 3 reps 不及 Magma 24 h × 5 reps 的标准 | 沿用 DESIGN.md §3.2 的 "short-budget regime, defensible for ranking stability" 措辞；H4 的 floor 验证只读取 short-budget 下的相对差距，不依赖绝对峰值 |
| naive prompt-stuffing 选 32k tokens 截断作为单一 baseline | 在附录中列出 16k / 64k 截断的烟雾测试结果（仅 1 cell × 1 rep），证明截断阈值不是关键 |
| E1/E3 的 LLM 在 spec 极长时可能拒答或截断输出 | 提前用 `compares/scripts/application_study/probe_llm_capacity.py` 验证 DeepSeek-V3 在 32k spec + 6k blindspot ticket 输入下不触发截断 |

---

## 9. 参考文献 (References)

* **Klees, G., Ruef, A., Cooper, B., Wei, S., Hicks, M.** (2018). *Evaluating Fuzz Testing.* CCS'18 — 协议（reps、time budget、Mann-Whitney U）权威参考。
* **Hazimeh, A., Herrera, A., Payer, M.** (2020). *Magma: A Ground-Truth Fuzzing Benchmark.* SIGMETRICS'20 — Real-bug bench 协议。
* **Xia, C. S., et al.** (2024). *Fuzz4All: Universal Fuzzing with Large Language Models.* ICSE'24 — naive prompt-stuffing ("raw-prompt") 作为强 baseline 的范式。
* **Meng, R., et al.** (2024). *Large Language Model Guided Protocol Fuzzing (ChatAFL).* NDSS'24 — 增量 ablation 范式参考。
* **Gu, T., Sun, C., Ma, X., Lü, J., Su, Z.** (2022). *Feedback-Directed Metamorphic Testing.* ACM TOSEM 31(4):63 — RQ "反馈闭环必要性" 的直接背书。
* **Liyanage, S., Böhme, M.** (2023). *On the Limits of Automated Metamorphic Testing.* ICSE'23 — H2 中 MR-only 25–40 % 上限的来源。
* **Ba, K., et al.** (2025). *Metamorphic Coverage.* arXiv:2508.16307 — 同 H2 的辅助论据。
* **Vargha, A., Delaney, H. D.** (2000). *A Critique and Improvement of the CL Common Language Effect Size Statistics.* J. Educ. Behav. Statist. 25(2):101–132 — $\hat{A}_{12}$ 效应量。
* **RAG Surveys 2025**：arXiv:2506.00054 + arXiv:2508.06401 — RAG ablation 的标准做法（zero-shot vs raw-prompt vs full-RAG 三档）。
