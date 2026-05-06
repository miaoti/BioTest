# E1 — Phase A 消融（去 RAG retrieval）

## 这个配置是什么

对应 `compares/APPLICATION_STUDY.md` 的 **E1 cell**：

* Phase A 完全不参与 LLM 的 MR 挖掘——`query_spec_database` Tool 被打成
  no-op，spec 文本通过 *naive prompt-stuffing*（Fuzz4All raw-prompt 同款）
  整段塞进 system prompt。
* Phase D 反馈闭环 **完整保留**（SCC tracker、blindspot ticket、Rank 1
  seed-synth、Rank 4 `target()`、Rank 8 corpus keeper、Phase E 都正常跑）。
* 所有输出隔离在 `results/` 下，不污染主线 `biotest.py` 的 `bug_reports/`、
  `data/`、`seeds/`、`coverage_artifacts/`。

## 不触碰源码的实现

4 处 module-level monkey-patch。前三个在 `import biotest` 之前装配；
第四个（Phase E 隔离）必须在 `import biotest` 之后装配，因为它要拿到
`biotest.PhaseEResult` 类。

| Patch 点 | 替换为 | 作用 |
| :--- | :--- | :--- |
| `mr_engine.agent.tools.get_ephemeral_index` | 返回空 `_StubSpecIndex` | `query_spec_database` Tool 永远返回空；同时 `engine.py:313 spec_index = get_spec_index()` 也拿到 stub，不加载 ChromaDB |
| `mr_engine.agent.engine.build_system_prompt` | 包装函数：在原 prompt 末尾追加 `shared/raw_spec_dump.txt` 全文 | LLM 看到完整 spec 但没有 retrieval 工具 |
| `mr_engine.dsl.compiler._hydrate_evidence` | stub，跳过 chunk_id 校验，severity 默认 `ADVISORY` | LLM 无法引用真实 chunk_id 时仍能产出合规 MR |
| `biotest.run_phase_e` | 复制函数体，把 `seeds_root = repo_root/"seeds"` 改成 `seeds_root = Path(cfg["phase_c"]["seeds_dir"])` | Phase E 的 Rank 12+13 augmentation 输出落到 E1 隔离 corpus 目录，不污染主 `seeds/<fmt>_struct/`、`<fmt>_rawfuzz/` |

`mr_engine/`、`test_engine/`、`biotest.py`、`spec_ingestor/` 下任何文件
都未被修改——可用 `git diff --stat` 验证。

## 运行命令

```bash
# 一次性：构建 spec 全文（E1 与 E3 共用）
py -3.12 compares/ApplicationStudy/shared/build_spec_dump.py

# 仅 patch + 配置 + dump effective config（不实际跑流水线）
py -3.12 compares/ApplicationStudy/E1_no_phase_a/run_e1.py --check

# 完整跑流水线
py -3.12 compares/ApplicationStudy/E1_no_phase_a/run_e1.py
```

`run_e1.py` 调用 `biotest.run_pipeline(cfg, phase_filter="B,C,D,E")`——
跳过 Phase A，B/C/D/E 都跑。

## 输出位置（corpus 与 seed 严格分离）

所有输出落在 `compares/ApplicationStudy/E1_no_phase_a/results/`：

```
results/
├── effective_config.yaml          # 实际生效的合并 config（reproducibility）
├── input_manifest.json            # ✨ 所有起始 corpus 的 SHA-256 + 跳过的 BioTest 产物清单（审计用）
├── mr_registry.json               # Phase B 编译后的 MR 注册表
├── bug_reports/                   # Phase C 触发的 bug 报告（与主线同结构）
├── det_report.json                # DET 统计
├── corpus/                        # ✨ 工作 corpus（== phase_c.seeds_dir）— 不叫 seeds，避免歧义
│   ├── vcf/                       #   起始：从主 seeds/vcf/ 拷贝（已过滤 BioTest 产物）
│   ├── sam/                       #   起始：从主 seeds/sam/ 拷贝（已过滤 BioTest 产物）
│   ├── ref/                       #   起始：从主 seeds/ref/ 拷贝（CRAM 参考）
│   ├── vcf/, sam/                 #   运行中累积：kept_*（Rank 8）+ synthetic_*（Rank 1）
│   ├── vcf_struct/, sam_struct/   #   运行中产出：Phase E Rank 12（隔离 patch 后才落到这里）
│   └── vcf_rawfuzz/, sam_rawfuzz/ #   运行中产出：Phase E Rank 13
├── coverage/                      # JaCoCo / coverage.py / gcovr / cargo-llvm-cov 全套
│   ├── jacoco/, pysam/, noodles/
│   ├── gcovr.json
│   └── .coverage
├── feedback_state.json            # Phase D iteration state
└── rule_attempts.json             # Top-K 冷却账本
```

**Corpus 隔离保证**（这是 E1 设计的硬底线）：

1. **入站**：`_sync_input_corpus` 只拷贝主 `seeds/{vcf,sam,ref}/` 下名字
   *不* 以 `kept_`、`synthetic_`、`.kept_`、`.synthetic_` 开头的常规文件。
   不递归到主 `seeds/{vcf,sam}_{struct,rawfuzz,diverse,bytefuzz}/` 兄弟目录
   （那些全是 BioTest 之前 run 的产物）。每个文件的 SHA-256 写入
   `input_manifest.json`——配合主 `seeds/` 的 git 历史可证明 corpus 来源。
2. **出站**：corpus_keeper、Rank 1 seed-synth、Phase E 的 Rank 12+13 augmentation
   全部写入 `<E1>/results/corpus/`，**绝不**写主 `seeds/`。
   * corpus_keeper / seed-synth 通过 `phase_c.seeds_dir` config 自然路由；
   * Phase E 通过 `biotest.run_phase_e` monkey-patch 强制路由（原函数硬编码
     `repo_root/"seeds"`，不读 config——`biotest.py:1552`）。

下游度量（coverage growth / mutation score / bugbench）直接拿这个
`results/` 目录当输入即可——结构与主线一致。具体命令见
`compares/ApplicationStudy/README.md` 的 §度量。

## Phase A 消融的边界（重要）

Phase A 的 *知识产物*（`data/parsed/*.json`、`data/chroma_db/`）在 E1 里
**不被 LLM 使用**，但 SCC tracker 仍读取 `data/parsed/` 计算 SCC。这是有意为之：
SCC 的分母（453 条规范规则）是 Phase A 已落盘的固定值，分子（被 enforced
MR 引用的 chunk_id）由当前 run 的 LLM 决定。E1 里 LLM 引用的 chunk_id
全是 `spec-blind`，无法匹配真实规则——所以 E1 的 SCC 预期会接近 0%，
这正是消融实验想测出的信号。

如果机器上 `data/parsed/` 不存在（极端情况），SCC tracker 会优雅降级
到 `total_rules=0, scc_percent=0.0`（`scc_tracker.py` 既有行为），
不会 crash。
