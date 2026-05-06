# ApplicationStudy — Phase A / Phase D 消融实验

> 协议规范：`compares/APPLICATION_STUDY.md`
> （本目录是该协议的实施代码；不重复设计内容）

## 目录矩阵

| 配置 | Phase A | Phase D | 状态 | 入口 |
| :--- | :---: | :---: | :--- | :--- |
| **E0** | ✓ | ✓ | implicit baseline | `biotest.py`（主线评估，复用结果）|
| **E1** | ✗ | ✓ | **implemented** | `E1_no_phase_a/run_e1.py` |
| E2 | ✓ | ✗ | placeholder | `E2_no_phase_d/` |
| E3 | ✗ | ✗ | placeholder | `E3_no_a_no_d/` |

E0 不在本目录运行——它就是 `biotest.py` 默认全开的主线评估。

## 设计约束（关键）

**所有变体必须做到**：

1. **零源码改动**：不修改 `mr_engine/`、`test_engine/`、`biotest.py`、
   `spec_ingestor/` 下任何文件。差异通过 wrapper 脚本里的 module-level
   monkey-patch 实现。
2. **输出隔离**：每个变体把所有输出（`bug_reports/`、coverage、registry、
   feedback state）重定向到 `<variant>/results/`，不污染主线评估的目录。
3. **下游度量同形**：每个变体的 `results/` 必须与 `biotest.py` 默认输出
   结构一致，这样 `compares/scripts/` 下的 mutation / bugbench / coverage
   driver 不需要改动就能对它运行。
4. **Corpus 与 seed 严格分离**：
   * 起始 corpus 来自主 `seeds/{vcf,sam,ref}/`，但**只取合法输入种子**——
     凡是名字以 `kept_`、`synthetic_`、`.kept_`、`.synthetic_` 开头的文件
     都跳过（前两者是 Rank 8 / Rank 1 的运行产物；后两者是审计日志）。
     `seeds/{vcf,sam}_{struct,rawfuzz,diverse,bytefuzz}/` 兄弟目录整体跳过
     （那些是 Phase E + 手工 CLI 工具的产物）。
   * 起始 corpus 拷贝到 `<variant>/results/corpus/`，**故意不叫 `seeds/`**——
     避免与主 `seeds/` 概念混淆。
   * 运行中产出（kept_、synthetic_、Phase E 的 `_struct/_rawfuzz`）都落在
     `<variant>/results/corpus/` 内，**不写主 `seeds/`**。Phase E 因为源码
     里硬编码了路径，需要靠 monkey-patch 强制隔离（详见 E1 README）。
   * `<variant>/results/input_manifest.json` 记录每个起始 corpus 文件的
     SHA-256 + 跳过的 BioTest 产物清单——审计用。

## 主 `seeds/` 目录污染审计（2026-05-01 截止）

| 目录 | 状态 | 说明 |
| :--- | :--- | :--- |
| `seeds/vcf/` | ✓ 干净 | 33 个文件全部为合法 input seed（real_world_*, htsjdk_*, minimal_*, spec_example*, bcftools_test*）；无 kept_*/synthetic_* |
| `seeds/sam/` | ✓ 干净 | 75 个文件全部为合法 input seed（real_world_*, jazzer_* 30 条用户确认有意放入, literals_*, spec_*, minimal_*, htsjdk_*, complex_*）；无 kept_*/synthetic_* |
| `seeds/ref/` | ✓ 干净 | CRAM toy reference，read-only |
| `seeds/vcf/.kept_manifest.jsonl` | ⚠ 历史产物 | Rank 8 audit log（hidden 文件，不被 SeedCorpus glob 捕获）。E1 setup 自动跳过 |
| `seeds/sam/.kept_manifest.jsonl` | ⚠ 历史产物 | 同上 |
| `seeds/vcf_struct/` | ⚠ 历史产物 | Phase E Rank 12 之前 run 的输出。E1 不读、不写它（兄弟目录整体跳过 + Phase E patch 重定向） |
| `seeds/vcf_rawfuzz/` | ⚠ 历史产物 | Phase E Rank 13 之前 run 的输出。同上 |

**结论**：主 `seeds/` 的 *常规 seed 文件*（`vcf/*.vcf`、`sam/*.sam`）从未被
BioTest 工具自身产出污染——`jazzer_*` 是用户有意添加，所有 `real_world_*`
来自 `fetch_real_world.py`，所有 `minimal_*`/`spec_*` 是 Tier-1 手工种子。
唯一的"污染"是 hidden manifest 与兄弟目录，E1 setup 已经全部排除在 input
之外、并隔离 output 路径。

## 运行流程

```bash
# 一次性：从 data/raw_tex/ 生成 spec 全文（E1/E3 共用）
py -3.12 compares/ApplicationStudy/shared/build_spec_dump.py

# 跑 E1
py -3.12 compares/ApplicationStudy/E1_no_phase_a/run_e1.py
```

详细命令见每个变体目录下的 README。

## 共享资源

`shared/` 目录存放跨变体共用资源：

* `build_spec_dump.py` — 把 `data/raw_tex/VCFv4.5.tex + SAMv1.tex` 经
  `pylatexenc` 转纯文本，截前 ~32k tokens，写到 `shared/raw_spec_dump.txt`。
  E1（−A 单跑）和 E3（−A−D 联跑）都通过 monkey-patch 把这个文件注入
  system prompt。

## 度量

每个变体 `results/` 跑完后，复用 `compares/scripts/` 既有 driver：

```bash
# Coverage growth
py -3.12 compares/scripts/coverage_rollup.py \
    --runs compares/ApplicationStudy/E1_no_phase_a/results

# Mutation score（PIT / mutmut / cargo-mutants / mull）
bash compares/scripts/phase3_jazzer_pit.sh \
    TOOL=biotest_E1 \
    CORPUS_DIR=compares/ApplicationStudy/E1_no_phase_a/results/seeds_kept

# Bug bench
py -3.12 compares/scripts/bug_bench_driver.py \
    --tool biotest_E1 \
    --corpus compares/ApplicationStudy/E1_no_phase_a/results/seeds_kept
```

确切参数取决于主线评估在 `compares/results/` 下落地的格式；保持一致即可。
