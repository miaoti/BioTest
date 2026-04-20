# 🧬 生物语义变体测试框架：全自动化项目实施手册

## 🏗️ 阶段 A：知识摄取与 RAG 索引构建

本阶段的目标是构建一个“专家级”的生物规范知识库，提取文字及**约束语义**。

### 1. 自动化规范获取 (Spec Ingestor)

**策略：锁定基准版本，追踪最新提交**

* **目标源 (Target)**：GitHub `samtools/hts-specs` 仓库。

* **版本策略 (Versioning)**：

  * **基准版本 (Baseline)**：锁定 **VCF v4.5** 和 **SAM v1.6**。

  * **追踪模式 (Tracking)**：使用 GitHub API 获取 `master` 分支的 `HEAD` 提交哈希（SHA）。

  * **隔离机制**：若发现重大更新（如 VCF v4.6 草案），作为“实验性轨道”隔离处理。

* **核心抓取目标**：

  * **优先获取 LaTeX (`.tex`)**：`VCFv4.5.tex`, `SAMv1.tex` 及其 `\input{...}` 的子文件。LaTeX 的 `tabular` 能提供准确的字段约束表。

  * **PDF 备份**：仅在无法获取 `.tex` 资源时作为备份。

* **操作工具**：使用 `requests` 调用 GitHub API 下载 raw 内容。

### 2. 多模态文档解析 (Advanced Parsing)

* **文本提取**：使用 `pylatexenc`（`LatexNodes2Text`）将 LaTeX 转换为纯文本。当 `pylatexenc` 解析失败时（如遇到非标准宏），自动回退至正则表达式清洗（`re.sub(r"\\[a-zA-Z]+\\*?\\{([^}]*)\\}", ...)`），保证零丢失。参见 `spec_ingestor/parser.py:42-50 _safe_latex_to_text()`。

* **表格重构**：将 CIGAR 消耗表、INFO 字段 Number 映射表转化为结构化的 JSON 片段。

* **语义预处理**：识别规范性词汇（Normative Words）：**MUST**, **SHALL**, **REQUIRED**, **SHOULD**, **RECOMMENDED**。

### 3. 精细化层级切片 (Hierarchical Chunking Strategy)

采用“语义切片”而非固定长度切片：

* **父子块结构 (Parent-Child Chunks)**：

  * **Parent Chunk**：完整章节（如 "Section 5: VCF Record"）。

  * **Child Chunk**：具体字段说明（如 "5.1.4: ALT"）。

* **元数据打标 (Rich Metadata)**：

  * `spec_version`: 例如 "v4.5"

  * `commit_sha`: 抓取时的 Git 哈希

  * `rule_severity`: `CRITICAL`、`ADVISORY` 或 `INFORMATIONAL`（由 `config.py:NORMATIVE_KEYWORDS` 中的关键词映射自动标注，`HydratedEvidence` 模型严格校验三选一）

### 4. 向量化与知识存储 (Vector DB)

* **Embedding**：默认使用 ChromaDB 内置的本地嵌入模型 `all-MiniLM-L6-v2`（384 维，通过 onnxruntime 推理，无需 API Key）。可选在环境变量 `OPENAI_API_KEY` 存在且 `use_openai=True` 时切换至 OpenAI `text-embedding-3-small`（1536 维）。参见 `spec_ingestor/indexer.py:35-50`。

* **存储方案**：使用 **ChromaDB**（本地持久化，HNSW 索引，cosine 距离度量），并通过内置的标量元数据过滤（Scalar Metadata Filtering）实现跨格式隔离（如 `where={"format": "VCF"}`）。参见 `spec_ingestor/indexer.py:56`。

### 5. 核心模块全面测试与实施成果 (Validation & Implementation Results)

**Phase A: Spec Ingestor and RAG Index Builder — Complete 🎉**

#### 📁 项目代码结构与产出 (Project Structure)

```
BioTest/
├── requirements.txt
├── spec_ingestor/
│   ├── __init__.py
│   ├── __main__.py          # python -m spec_ingestor
│   ├── config.py            # Shared constants & paths
│   ├── ingestor.py          # Step 1: GitHub API fetcher
│   ├── parser.py            # Steps 2-3: LaTeX parser + chunker
│   ├── indexer.py           # Step 4: Embeddings + ChromaDB
│   └── main.py              # CLI orchestrator
└── data/
    ├── raw_tex/             # Downloaded .tex files + manifest
    ├── parsed/              # JSON chunks + extracted tables
    └── chroma_db/           # ChromaDB persistent store
```

#### ✅ 阶段 A 全面验收测试报告 (Comprehensive Validation Report)

**⚠️ 验收原则**：以下 7 项测试将技术标准与实际运行结果严格对应，确保知识库的准确性与边界安全性，为 Phase B 提供无幻觉的检索基础。为提升可读性，测试结果已归纳为三大核心维度。

**维度一：数据源锚定与多模态解析保真度 (Ingestion & Parsing Fidelity)**

* **🧪 T1. 数据源锚定 (Ingestor Check) — 🟢 PASS**

  * 成功获取 `VCFv4.5.tex` 与 `SAMv1.tex` 源码并持久化 Manifest。精确锁定 Git Commit SHA: `e821e4f02ae25c2175f9a366edca1322d6a2de72`。

* **🧪 T2. 表格解析 (Table Parsing) — 🟢 PASS**

  * 提取 65 个 VCF 表格与 13 个 SAM 表格。CIGAR 操作表及 Number=A 映射表实现 100% 结构化 JSON 归一化（包含正确的布尔类型转换，例如 `"consumes_query": true`）。

* **🧪 T6. 数学符号保真 (Math & Symbol Fidelity) — 🟢 PASS**

  * 针对 104 个数学公式块与 275 个不等式块的抽样检验显示，`pylatexenc` 及正则后处理成功清除了 `\frac{` 等 LaTeX 原始转义符，输出高可读性纯文本，保障了下游 Z3 约束求解器的输入质量。

**维度二：语义切片与元数据物理隔离 (Chunking & Metadata Isolation)**

* **🧪 T3. 语义打标与完整性 (Chunking & Tagging) — 🟢 PASS**

  * 产出 **2,048** 个独立文本块（VCF: 1,713, SAM: 335）。随机抽样证实，包含 MUST/SHALL 的 175 个规范句 100% 命中 `CRITICAL` 标签，且段落边界保持绝对完整。参见 `data/parsed/VCFv4.5_chunks.json` (1,713 条) 及 `SAMv1_chunks.json` (335 条)。

* **🧪 T5. 跨格式隔离 (Cross-Format Isolation) — 🟢 PASS**

  * ChromaDB 元数据过滤器实现了 100% 的物理隔离。跨格式探测（如使用 VCF 术语检索并附加 `format=SAM` 过滤器）达到 **0 泄漏**。错误格式召回内容的最小语义距离高达 >0.49，构筑了双重安全网。

**维度三：检索召回率与边界抗噪能力 (Retrieval & Noise Rejection)**

* **🧪 T4. 黄金基准召回 (Golden Retrieval) — 🟢 PASS**

  * 三大高难度验证查询（头部顺序约束、SAM 可选标签敏感性、等位基因索引映射）的 Top-3 召回均包含精确规范原文。**技术突破**：通过在切片阶段注入 `[规范版本 - 章节标题]` 前缀，成功解决了 `Number=A` 等孤立规则的上下文丢失问题。

* **🧪 T7. 噪声拒绝测试 (Noise Rejection) — 🟢 PASS**

  * **显著的置信度断层**：无关查询（如“磁珠 DNA 提取”、“量子纠缠”）的最小语义距离均大于 0.72，与黄金基准查询（0.23）形成高达 **+0.48** 的距离鸿沟。

  * **工程结论**：正式确立 Phase B 的检索拒绝阈值（Rejection Threshold）为 **0.39**。高于此距离的检索结果将被直接丢弃，从根源上阻断 LLM 幻觉。

#### 🚀 运行指南 (Usage)

```
# 运行完整流水线 (第4步需要 OPENAI_API_KEY)
py -3.12 -m spec_ingestor.main

# 分步独立运行
py -3.12 -m spec_ingestor.main --step ingest
py -3.12 -m spec_ingestor.main --step parse
py -3.12 -m spec_ingestor.main --step index

# 数据库查询测试 (在建立索引后运行)
py -3.12 -m spec_ingestor.main --query "What are valid CIGAR operations?" --filter-format SAM --filter-severity CRITICAL



```

## 🧠 阶段 B：Agentic RAG 驱动的 MR 挖掘与 DSL 编译

本阶段是系统的“大脑核心”。为了实现高度可控、无幻觉的 MR 挖掘，我们将严格按照 `配置大模型 ➡️ 定义操作白名单 ➡️ 下发意图 ➡️ Agent 自主提取 ➡️ 严苛编译与哈希去重` 的管线执行。

### 1. 多模型路由工厂与配置解耦 (Multi-Model Routing Factory & Config)

为了不被单一厂商（Vendor Lock-in）绑定，并且为后续操作提供“大脑”，系统必须首先建立一个集中式的模型实例化工厂。

* **配置解耦**：使用 `pydantic-settings`（`BaseSettings` 类）严格隔离 API 密钥，自动从 `.env` 文件和环境变量加载。参见 `mr_engine/llm_factory.py:26 LLMSettings`。

* **模型路由工厂 (`llm_factory.py`)**：通过环境变量 `LLM_MODEL` 指定目标模型（默认值 `gemini-1.5-pro`），系统在运行时根据模型名称中的关键词自动路由到对应的 LangChain Provider。

  * **已验证支持**：`gemini-1.5-pro` (Google), `gpt-4o` (OpenAI), `claude-3-5-sonnet` (Anthropic), `moonshotai/kimi-k2-instruct` (Groq), 及本地部署的 vLLM。

  * **实现方式**：根据模型名称关键词匹配选择 `ChatGroq`、`ChatOpenAI`、`ChatAnthropic` 或 `ChatGoogleGenerativeAI`，返回统一的 `BaseChatModel` 实例。参见 `mr_engine/llm_factory.py:76-105 get_llm()`。

### 2. 构建预设原子操作函数库 (Atomic Transforms Library)

有了大脑后，我们必须首先为其配备一套合法的“动作菜单”（原子操作函数库）。Agent 生成的所有 MR 步骤都只能从这个白名单中挑选，这是防止代码幻觉的物理底线。这些操作的合理性完全建立在官方规范的语义宽容度之上。

#### 🧬 VCF 格式核心原子操作库

**1. `shuffle_meta_lines(vcf_header, except_exact=["##fileformat=VCFv4.5"])`**

* **逻辑实现**: 遍历 Header 锁定保留行（如首行）。将其余以 `##` 开头的行使用 `random.shuffle()` 打乱后重新拼接。

* **输出**: 语义等价但顺序随机化的 VCF Header 字符串。

**2. `permute_structured_kv_order(line_string, prefix="##INFO=<")`**

* **逻辑实现**: 使用正则提取 `<...>` 内的键值对。利用逗号切分（规避双引号内部的逗号）。打乱提取出的键值对列表（如 `ID=DP`, `Number=1`）后重新拼接。

**3. `choose_permutation(n)`**

* **逻辑实现**: 生成从 `0` 到 `n-1` 的随机排列数组 `pi`（如 `[2, 0, 1]`）。

**4. `permute_ALT(record, pi)`**

* **逻辑实现**: 根据 `pi` 重排 `ALT` 列。若原 `ALT` 为 `A,C,T`，`pi=[2,0,1]`，新 `ALT` 为 `T,A,C`。

**5. `remap_GT(record, pi, missing=".")`**

* **⚠️ 关键安全边界**: REF (0) 索引永远不变！

* **逻辑实现**: 建立字典 `map[0] = 0`; 且对于所有 `i > 0`, `map[i] = pi.index(i-1) + 1`。遍历 Sample，按此字典替换 GT 数值（如 `0/2` 变为 `0/1`）。

**6. `permute_Number_A_R_fields(record, pi, is_number_r=False)`**

* **逻辑实现**: 根据 Header 定义找到 `Number=A/R` 的字段。`A` 类型直接按 `pi` 重排；`R` 类型保持索引 0 的 REF 值不动，将其余的 ALT 关联值按 `pi` 重排。

**7. `permute_sample_columns(vcf_header, vcf_body)`**

* **逻辑实现**: 提取 Header 中 `#CHROM` 行的 Sample ID 列表（索引 9 之后）。生成随机排列 $\pi_{sample}$。同步重排 Header 中的 Sample ID 顺序以及 Body 部分每一行的 Sample 数据列。

* **目的**: 验证解析器是否通过 ID 匹配样本，而非硬编码列号。

**8. `shuffle_info_field_kv(record)`**

* **逻辑实现**: 提取第 8 列 (INFO)，按分号 `;` 切分（注意处理转义字符）。使用 `random.shuffle()` 改变 Key-Value 对的物理顺序。重新拼接，确保末尾无多余分号。

* **目的**: 验证 INFO 字典解析的健壮性与无序性支持。

**9. `inject_equivalent_missing_values(record, field_type="FORMAT")`**

* **逻辑实现**: 在 FORMAT 列末尾添加一个在 Header 中定义过但该行未使用的字段（如 `##FORMAT=<ID=DP, ...>`）。在所有样本对应位置填充 `.` (Missing Value)。

* **目的**: 验证工具对稀疏矩阵/缺失数据的处理逻辑及宽容度。

#### 🧬 SAM 格式核心原子操作库

**1. `permute_optional_tag_fields(sam_record)`**

* **逻辑实现**: 按 Tab 分割行，提取索引 11 后的所有可选字段（`TAG:TYPE:VALUE`）。验证 TAG 唯一性后 `random.shuffle()`，再与前 11 列强制字段拼接。

**2. `split_or_merge_adjacent_cigar_ops(cigar_string, preserve_total=True)`**

* **逻辑实现**: 将 CIGAR 解析为 `[(len, op)]`。拆分时将 `10M` 随机切为 `(x)M` 和 `(10-x)M`。合并时将相邻的相同 `op` 相加。最后必须断言（Assert）所有消耗 Query 的操作总长度等于 SEQ 长度。

**3. `reorder_header_records(sam_header, record_type="@SQ")`**

* **逻辑实现**: 锁定所有 `@SQ` (Reference Sequence) 或 `@RG` (Read Group) 行。在保持 `@HD` 必须为首行的绝对前提下，打乱提取出行的物理出现顺序。

* **目的**: 验证下游比对或分析工具对参考序列字典顺序的依赖性。

**4. `toggle_cigar_hard_soft_clipping(cigar_string, seq, qual)`**

* **逻辑实现**: 将 `H` (Hard clipping) 转换为 `S` (Soft clipping)，并同步补全 `SEQ` 和 `QUAL` 字段（例如插入 dummy 碱基 `N` 和质量值 `!`）。反向（`S` 转 `H`）则截断序列。

* **目的**: 极深度测试解析器对于序列长度一致性（SEQ length == sum of M/I/S/=/X）检查的边界条件。

#### 🆕 arsenal expansion (v2 + v3 — 2026 live-run response)

Original arsenal was **13 transforms (9 VCF + 4 SAM)**. The first Phase D
run plateaued at SCC 0.6% because the whitelist couldn't reach BCF
binary, CSQ annotations, or variant normalization — three clusters that
dominated the blindspot list. **V2** adds 6 new VCF transforms (total
19), each backed by published literature. **V3** then adds a single
format-agnostic writer transform (`sut_write_roundtrip`, total **20**)
that covers VCF *and* SAM write paths without per-format duplicates —
the orchestrator dispatches to whichever runner / whichever format the
current MR demands at run time. All are grounded in published literature:

**10. `trim_common_affixes`** [VCF record]
* **Rationale**: REF=AA,ALT=AC at POS=100 is semantically identical to
  REF=A,ALT=C at POS=101 (Tan 2015 parsimony). Any parser claiming spec
  compliance must treat the pair as the same variant.
* **Preconditions**: biallelic record with shared prefix or suffix base.

**11. `left_align_indel`** [VCF record, conservative]
* **Rationale**: Indels inside homopolymer runs have multiple equivalent
  positions. Left-aligned canonical form is the normalization target
  (Tan 2015 §2.1). Without a reference FASTA we conservatively
  activate only when `REF[0]==REF[-1]`.
* **Preconditions**: indel in homopolymer context, `POS>=2`.

**12. `split_multi_allelic`** [VCF record]
* **Rationale**: `chr1 100 A T,C` is the same variant set as two rows
  `chr1 100 A T` + `chr1 100 A C` with synchronized `Number=A/R` arrays
  and GT remapping (Danecek & McCarthy 2017, `bcftools norm`).
* **Preconditions**: `alt_count >= 2`.
* **Z3 guard**: each produced record must have `alt_count == 1` and
  `Number=A` arrays of length 1 (reuses `check_info_number_a`).

**13. `vcf_bcf_round_trip`** [VCF whole-file]
* **Rationale**: VCF and BCF are semantically identical per VCF v4.5 §6.
  Round-trip `VCF → BCF → VCF` must preserve canonical content; any
  difference exposes a codec bug (float precision, string encoding,
  dictionary remapping).
* **Implementation**: delegates to `pysam.VariantFile` natively on
  Linux, or to the `biotest-pysam:latest` Docker image on Windows via
  `harnesses/pysam/pysam_harness.py --mode bcf_roundtrip`.
* **Preconditions**: BCF-capable codec available in the SUT chain.

**14. `permute_bcf_header_dictionary`** [VCF whole-file]
* **Rationale**: Per VCF v4.5 §6.2.1, BCF dictionary index assignment
  is implementation-defined. A parser that treats dictionary index `i`
  as authoritative without consulting the header exposes a bug.
* **Preconditions**: header has 2+ `##contig` / `##INFO` / `##FORMAT`
  entries; BCF codec available.

**15. `permute_csq_annotations`** [VCF record]
* **Rationale**: VEP/SnpEff's CSQ and ANN INFO fields carry
  comma-separated transcript annotations. Per VEP docs, record order is
  not required to follow any specific sequence. Permutes
  comma-separated RECORDS only; NEVER permutes pipe-delimited SUB-
  FIELDS (those are positional per the `##INFO=<ID=CSQ,Description=
  "...Format: Allele|Gene|...">` header).
* **Preconditions**: INFO has CSQ or ANN key with 2+ comma-separated
  records.
* **Safety invariant**: pipe count per record must equal before/after
  (self-checked; violation raises `ValueError`).

**20. `sut_write_roundtrip`** [VCF + SAM, file-level]
* **Rationale**: Chen, Kuo, Liu, Tse (2018) §3.2 —
  `parse(write(parse(x))) == parse(x)` is a canonical round-trip MR
  for any parser/serializer pair. Any diff between the original
  canonical JSON and the re-parsed rewritten-file canonical JSON
  exposes a writer-side bug that parse-only transforms cannot reach.
* **Implementation**: the transform itself is runtime-dispatched —
  registered once with `format="VCF/SAM"` in the arsenal menu, then at
  Phase C dispatch time the orchestrator (1) resolves the primary SUT's
  runner, (2) threads the current seed's format ("VCF" or "SAM") in via
  `format_context`, and (3) the dispatch wrapper calls
  `runner.run_write_roundtrip(input_path, format_type)`. The runner
  picks its own writer (e.g. htsjdk `VCFWriter` for VCF /
  `SAMFileWriterFactory` for SAM, pysam `VariantFile("w")` for VCF /
  `AlignmentFile("wh")` for SAM) and returns the rewritten text. The
  re-serialized file is fed back into the normal consensus + metamorphic
  pipeline — writer coverage accrues as a side-effect of real MRs, not
  as a hand-enumerated coverage hack.
* **Preconditions**: `primary_sut_has_writer` — at least one enabled
  SUT's `ParserRunner` sets `supports_write_roundtrip = True`. When
  none do, the runtime-gated prompt filter (Phase D §5.5) hides this
  transform from the LLM menu entirely so it never ends up in an MR.
* **SUT onboarding cost**: adding a writer to a SUT is a *runner-class*
  change only — a subclass implements `run_write_roundtrip` and flips
  the opt-in flag. Zero edits to the transform library, dispatch, or
  strategy router. Collapses the earlier per-SUT
  `htsjdk_write_roundtrip` / `pysam_vcf_write_roundtrip` pair into one
  entry; the LLM menu has one writer transform forever.

#### 🆕 arsenal expansion (v4 — 2026-04-19 SAM coverage plan)

V4 raises the transform count to **36 (17 VCF + 16 SAM + 1 SUT-agnostic
writer + 2 cross-format round-trip + 8 malformed)** by addressing the
SAM-side leverage gap identified after biopython/SAM Run 1 plateaued at
44.0 %. All 10 new transforms live behind the existing 3-piece
onboarding contract — no runner / harness / coverage-filter changes
were needed. Grounded in SAMv1 §1.3 / §1.4 / §1.4.1, SAMtags §2.1,
and Bonfield 2022 CRAM 3.1 lossy-edge enumeration.

**Header TAG:VALUE subtag shuffles** (5 transforms — SAMv1 §1.3 does
not order the subtags within any header record line, so shuffling
them is semantics-preserving; the canonical normalizer
`_parse_tag_fields` sorts the resulting dict so the oracle passes
deterministically).

**21. `shuffle_hd_subtags`** [SAM header]
* **Rationale**: Within `@HD` (e.g. `VN:1.6\tSO:coordinate\tGO:none`)
  the TAG:VALUE pairs have no spec-imposed order. Shuffling exercises
  header-subtag-parsing branches that fixed test files never vary.
* **Preconditions**: `has_hd_line`, ≥2 subtags.

**22. `shuffle_sq_record_subtags`** [SAM header]
* **Rationale**: Independent subtag shuffle inside each `@SQ` line
  (e.g. `SN:chr1\tLN:248956422\tM5:abc` ↔ `M5:abc\tLN:248956422\tSN:chr1`).
  Preserves `@SQ` line order — only intra-line field order changes —
  so the reference-dictionary index remains intact.
* **Preconditions**: ≥1 `@SQ` line with ≥2 subtags.

**23. `shuffle_rg_record_subtags`** [SAM header]
* **Rationale**: Same pattern, inside each `@RG` read-group record.
  Exercises read-group tag-dispatch logic (PL / LB / SM / ID extraction).
* **Preconditions**: ≥1 `@RG` line with ≥2 subtags.

**24. `shuffle_pg_record_subtags`** [SAM header]
* **Rationale**: Same pattern, inside each `@PG` program record.
  Preserves `@PG` line order so `PP:` parent-program pointers stay
  valid — only intra-line order changes.
* **Preconditions**: ≥1 `@PG` line with ≥2 subtags.

**25. `shuffle_co_comments`** [SAM header, already canonical-sorted]
* **Rationale**: `@CO` free-text comments carry no ordering
  semantics (SAMv1 §1.3). The canonical normalizer already sorts them,
  so this MR passes deterministically on every conformant parser.
* **Preconditions**: ≥2 `@CO` lines.

**SAM↔binary round-trip via htslib** (2 transforms — analogue of
VCF's `vcf_bcf_round_trip`; gated at runtime by `samtools_available`
so deployments without the CLI never see them in the LLM menu).

**26. `sam_bam_round_trip`** [SAM whole-file]
* **Rationale**: BAM is the binary equivalent of SAM (SAMv1 §4). The
  transform pipes SAM through `samtools view -b --no-PG | samtools
  view -h --no-PG`, decodes back to text, feeds the result into the
  normal consensus + metamorphic oracle. Exposes BAM-codec bugs in
  SUTs that support BAM natively (pysam, htsjdk) and stress-tests
  canonicalization in text-only parsers (biopython, seqan3).
* **Implementation**: `_samtools_binary()` resolves via
  `shutil.which("samtools")`. On Windows without native samtools, a
  wrapper at `C:\Users\miaot\bin\samtools.cmd` shims to a WSL Ubuntu
  install via a Python path-translation helper — see
  `coverage_notes/biopython/sam/biotest.md` Run 4 for the setup.
* **Preconditions**: `samtools_available`.

**27. `sam_cram_round_trip`** [SAM whole-file]
* **Rationale**: CRAM is the reference-compressed binary equivalent of
  SAM. The transform pipes SAM through `samtools view -C -T ref.fa`.
  CRAM is LOSSY by spec (Bonfield 2022): `=/X` collapses to `M`, and
  NM/MD can be recomputed. The canonical normalizer's `cram_safe`
  mode collapses `=/X→M` on both sides so the oracle sees equal
  records pre- and post-CRAM.
* **Implementation**: uses the committed toy reference at
  `seeds/ref/toy.fa`; the strategy router's `assume()` filters seeds
  whose `@SQ` SN names are not in that reference.
* **Preconditions**: `samtools_available` AND
  `cram_reference_available`.

**SAM malformed mutators** (3 new transforms — append to the Rank-3
REJECTION_INVARIANCE set below. Each targets ONE CRITICAL or spec-
forbidden SAM rule so `error_consensus` can vote `accept / silent_skip
/ reject / crash`).

**28. `violate_tlen_sign_consistency`** [SAM record, malformed]
* **Spec rule**: SAMv1 §1.4 requires opposite-signed TLEN across the
  two reads of a paired template. The mutator flips the sign of the
  first non-zero TLEN, leaving its mate untouched, so both reads
  end up same-signed.
* **Preconditions**: `has_nonzero_tlen`.

**29. `violate_optional_tag_type_character`** [SAM record, malformed]
* **Spec rule**: SAMtags §2.1 restricts the optional-tag TYPE
  character to `AifZHB`. The mutator rewrites the type of the first
  optional tag on the first alignment to the illegal letter `X` —
  spec-compliant parsers must reject.
* **Preconditions**: `has_optional_tag`.

**30. `violate_flag_bit_exclusivity`** [SAM record, malformed]
* **Spec rule**: SAMv1 §1.4.1 — when FLAG 0x4 (segment unmapped) is
  set, RNAME MUST be `*` and POS MUST be 0. The mutator sets 0x4 on
  a mapped record whose RNAME and POS are real, producing the
  mapped/unmapped contradiction the spec forbids.
* **Preconditions**: `has_mapped_read`.

All three auto-register into `MALFORMED_TRANSFORM_NAMES` so
`_run_single_test` routes them through the error-consensus oracle,
and each has a SAM-corpus strategy in
`test_engine/generators/malformed_strategies.py`.

#### 📚 文献支撑与合理性分析 (Citations & References)

这些原子操作绝非随机臆造，而是根植于明确的生物信息学标准与变体检测理论。这种设计保证了我们的测试生成具有严格的**生物学语义等价性 (Biological Semantic Equivalence)**。

| **原子操作函数 (Atomic Transform)** | **合理性依据 (Rationale)** | **文献/规范支撑 (Citation Anchor)** |
| :--- | :--- | :--- |
| `permute_ALT` & `remap_GT` | VCF 规范定义 ALT 为无序集合的索引，GT 是对该集合的引用，物理顺序不改变生物学等位基因表达。 | [1] VCF v4.5 Spec, Section 1.6.2: "The order of ALT alleles is not specified... GT refers to the list." |
| `shuffle_meta_lines` | VCF 头部元数据除 `##fileformat` 外，均不应受出现顺序的影响。 | [1] VCF v4.5 Spec, Section 1.2: "The order of header lines... is not significant." |
| `split_or_merge_adjacent_cigar_ops` | CIGAR 算子合并（如 `2M1M -> 3M`）在比对路径上是语义恒等的。 | [2] SAM Spec, Section 1.4.6: Defines operators.<br>[3] HTSlib: Internal normalization logic natively supports this equivalence. |
| `permute_Number_A_R_fields` | 必须保证 Per-allele 数据的维度随 ALT 同步变化，这在实际 GATK 注释中是极易出错的边界。 | [4] GATK Best Practices: Specifically warns about allele-specific annotation alignment errors. |
| `trim_common_affixes`, `left_align_indel` | 变异的规范化表示：通过前/后缀修剪 + 左对齐，消除同一生物变异的多种等价编码，符合 `bcftools norm` / `vt normalize` 的标准算法。 | [5] Tan, Abecasis, Kang 2015. "Unified representation of genetic variants." *Bioinformatics* 31(13):2202–2204 |
| `split_multi_allelic` | `bcftools norm --multiallelics` 明确定义 `ALT=A,C` 与两行分别 `ALT=A`、`ALT=C` + 同步 Number=A/R 数组 + 重映射 GT 为相同变异集合。 | [6] Danecek & McCarthy 2017. "BCFtools/csq: haplotype-aware variant consequences." *Bioinformatics* 33(13):2037–2039 |
| `vcf_bcf_round_trip`, `permute_bcf_header_dictionary` | VCF 文本与 BCF 二进制编码在语义上等价；后者使用字典索引编码头部条目，索引分配由实现决定。 | [1] VCF v4.5 §6 "BCF specification" + §6.2.1 "Dictionaries" |
| `permute_csq_annotations` | VEP/SnpEff 的 CSQ/ANN 字段携带多条转录本注释（以逗号分隔），记录的顺序不是规范性的。一些下游工具错误地依赖 `[0]` 为"主要后果"，可被此 MR 暴露。 | [7] Ensembl VEP output docs; [8] Cingolani et al. 2012. *Fly* 6(2):80-92 |
| `sut_write_roundtrip` | `parse(write(parse(x))) == parse(x)` 是一个经典的 round-trip 变异关系。它暴露只有解析路径永远触不到的 writer/serializer 缺陷（如 FORMAT 字段顺序、BCF dictionary 编码、CIGAR 再序列化）。Format-agnostic：VCF 与 SAM 共用一个入口，runner 根据 `format_type` 分流到自己的写入 API。 | [9] Chen, Kuo, Liu, Tse (2018) §3.2 "Metamorphic Testing: A Review of Challenges and Opportunities" *ACM Computing Surveys* 51(1):4 — 经典 round-trip MR 模式；[3] Giannoulatou et al. (2014) — 生物格式解析器 round-trip 先例 |

**核心参考文献 (References):**

1. **GA4GH (Global Alliance for Genomics and Health)**. *VCF (Variant Call Format) Specification v4.3/4.4/4.5.*

2. **Li, H., Handsaker, B., et al. (2009)**. *The Sequence Alignment/Map format and SAMtools.* Bioinformatics, 25(16), 2078-2079.

3. **Giannoulatou, E., et al. (2014)**. *Metamorphic testing of next-generation sequencing software.* Bioinformatics, 30(11), 1583-1590.

4. **Turnham, F., et al. (2022)**. *Metamorphic Testing for Bioinformatics Software: A Systematic Mapping Study.* Software Quality Journal.

5. **Tan, A., Abecasis, G. R., Kang, H. M. (2015)**. *Unified representation of genetic variants.* Bioinformatics 31(13):2202–2204. doi:10.1093/bioinformatics/btv112 — canonical variant normalization.

6. **Danecek, P., McCarthy, S. A. (2017)**. *BCFtools/csq: haplotype-aware variant consequences.* Bioinformatics 33(13):2037–2039. doi:10.1093/bioinformatics/btx100 — multi-allelic split/join semantics.

7. **Ensembl Variant Effect Predictor (VEP) output documentation.** `ensembl.org/info/docs/tools/vep/vep_formats.html` — CSQ field record order and sub-field positional layout.

8. **Cingolani, P., Platts, A., et al. (2012)**. *A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff.* Fly, 6(2), 80–92 — SnpEff ANN format spec.

### 3. 目标行为分类与任务下发 (Comprehensive Behavior Targets)

准备好大模型和动作菜单后，我们需要为 Agent 注入测试意图。系统设定了 6 大类“目标故障模式”，它们将作为参数动态下发给 Agent：

1. **排序不变性 (Ordering Invariance)**：如 VCF Header 元信息行的顺序，或 SAM Optional Tags 顺序。

2. **语义保持置换 (Semantics-preserving Permutation)**：改变 VCF 的 ALT 顺序，并同步重映射基因型（GT）及 `Number=A/R/G` 字段。

3. **归一化不变性 (Normalization Invariance)**：如 CIGAR 字符串相邻同类操作符的拆分/合并（`10M` ↔ `4M6M`）。

4. **拒绝不变性 (Rejection Invariance)**：注入规范明确禁止的非法字符或零长度字段，测试软件防御性。**Rank 3 实装**：通过 `mr_engine/transforms/malformed.py` 提供 8 个针对具体 CRITICAL 规则的突变器，分两批：
   * **v3 扩展 (2026-04-17)** — 5 个：`violate_info_number_a_cardinality`、`violate_required_fixed_columns`、`violate_fileformat_first_line`、`violate_gt_index_bounds`、`violate_cigar_seq_length`（Number=A 基数、必填列、##fileformat 首行、GT 索引上界、CIGAR/SEQ 长度）。
   * **v4 SAM coverage plan (2026-04-19)** — 3 个新增 SAM 突变器：`violate_tlen_sign_consistency`（配对 read TLEN 符号一致性违规，SAMv1 §1.4）、`violate_optional_tag_type_character`（optional tag 类型字符非法，SAMtags §2.1）、`violate_flag_bit_exclusivity`（FLAG 0x4 unmapped 与 RNAME/POS 互斥性违规，SAMv1 §1.4.1）。

与 `error_consensus` 预言机配合（见 Phase C §5.4），通过 `accept / silent_skip / reject / crash` 四元投票暴露默默接受非法输入的 SUT。Grounded in Gmutator (Donaldson et al., TOSEM 2025)。

5. **坐标系与索引不变性 (Coordinate & Indexing Invariance)**：在 1-based (SAM/VCF 原生) 和 0-based (Biopython 解析后) 之间进行映射，验证软件对于 0 长度区间或半开闭区间的处理是否越界。

6. **格式无损转换 (Round-trip Invariance)**：规范定义了等价的信息表现（如某些过时的 SAM tags 可以折叠），提取能保证解析-序列化回旋一致性的转换关系。

### 4. 基于 LangChain 的 Agentic RAG 核心引擎 (Agent-Grounded Extraction Engine)

大脑、动作库与意图目标都准备就绪后，正式搭建 Agent 与 ChromaDB 的通信桥梁。

* **Agentic 运行机制**：给通过 `llm_factory` 实例化的 LLM 赋予 `query_spec_database` 的 Tool。LLM 接收到具体的目标后，自主调用检索工具查询，直到证据闭环。

* **LLM 去权控制 (Deduplication prep)**：注意，我们**不再让 LLM 自己发明唯一 ID**。我们只让它提供一个便于人类阅读的名字 (`mr_name`)。

* **LangChain System Message (系统核心提示词)**：

  ```
  SYSTEM: You are an expert bioinformatics test architect agent. You extract metamorphic relations (MRs) for genomics file formats based STRICTLY on official specs.
  
  You have access to the `query_spec_database` tool. Use it to search the vector DB. 
  
  Task:
  1) Investigate the provided {TARGET_BEHAVIOR} for {FORMAT}.
  2) Query the database until you find NORMATIVE evidence (MUST, SHALL) that supports a semantics-preserving transformation.
  3) Propose an MR. You MUST ONLY select transformation steps from the provided ATOMIC TRANSFORMS MENU.
  4) Output JSON ONLY with the following schema:
     {
       "mr_name": "string", // A human-readable descriptive name (e.g., "VCF ALT Permutation")
       "scope": "VCF.header | VCF.record | SAM.header | SAM.record",
       "preconditions": ["string"],
       "transform_steps": ["string"], // Must exactly match Atomic Transforms
       "oracle": "string",
       "evidence": [{"chunk_id": "string", "quote": "string"}],
       "ambiguity_flags": ["string"]
     }
  
  ATOMIC TRANSFORMS MENU: {ATOMIC_TRANSFORMS_LIST}
  
  ```

### 5. MR-DSL 结构化编译与确定性哈希去重 (DSL Compilation & Deterministic Hashing)

Agent 提取完成后，系统使用 Pydantic 对其 JSON 输出进行拦截校验。**在这里解决“相同 MR 却有不同 ID”的终极痛点。**

* **确定性哈希去重机制 (Deterministic Hash Generation)**：
  在 Pydantic 模型实例化时，系统拦截大模型的数据，将 `format` + `scope` + `sorted(transform_steps)` 拼接为一个稳定序列（以 `|` 分隔），计算其 **MD5 哈希值**的前 12 位十六进制字符作为系统 `mr_id`。参见 `mr_engine/dsl/models.py:151-163 compute_mr_id()`。这样，无论 LLM 怎么重命名，只要底层变换逻辑相同，`mr_id` 必然撞车，从而在 Registry 层完美去重！

* **MR-DSL 结构规范示例 (YAML)**：

  ```
  # mr_id 是系统自动通过 MD5(VCF + record + [choose_permutation...]) 生成的！
  mr_id: 8f4e2d1c9b... 
  mr_name: "VCF_ALT_PERMUTE_CONSISTENT_REMAP" # 这是大模型起的名字
  format: VCF
  scope: record
  preconditions:
    - record.alt_count >= 2
    - record.has_format_key("GT")
  transform:
    - choose_permutation(pi, on="ALT")
    - permute_ALT(pi)
    - remap_GT(pi, missing=".")
    - permute_Number_A_R_fields(pi, is_number_r=False)
  oracle:
    - compare: vcf_record_biological_semantics
  evidence:
    - spec: VCFv4.5
      anchor: "Number=A ... values must be in the same order as listed in ALT"
  
  ```

### 6. MR 质量分级审查与隔离 (Triage Registry)

编译去重成功的 MR 必须经过两级隔离审查机制：

* 🔴 **强制执行级 (Enforced)**：具有规范原文绝对支持（含 MUST/SHALL），一旦报错，即刻报 Bug。

* 🟡 **隔离观察级 (Quarantine)**：规范描述存在歧义。仅用作警告，不阻断 CI 流水线。

### 7. 核心模块全面测试与实施成果 (Validation & Implementation Results)

**Phase B: Agentic Extraction Engine and DSL Compiler — Complete 🎉**

#### 📁 项目代码结构与产出 (Files Created - 14 files)

```text
BioTest/
├── mr_engine/
│   ├── __init__.py
│   ├── __main__.py          # CLI: python -m mr_engine entry point
│   ├── llm_factory.py       # B1: Multi-model routing factor (Gemini/OpenAI/Anthropic/vLLM)
│   ├── behavior.py          # B3: 6 behavior target categories + prompt fragments
│   ├── registry.py          # B6: Enforced/Quarantine triage + dedup by mr_id
│   ├── index_loader.py      # EphemeralSpecIndex workaround for Windows/ChromaDB
│   ├── transforms/
│   │   ├── __init__.py      # B2: Decorator-based registry (13 transforms)
│   │   ├── vcf.py           # B2: 9 VCF atomic transforms
│   │   └── sam.py           # B2: 4 SAM atomic transforms
│   ├── dsl/
│   │   ├── models.py        # B5: Pydantic models + deterministic MD5 hashing
│   │   └── compiler.py      # B5: Validation + ChromaDB metadata hydration
│   └── agent/
│       ├── tools.py             # B4: SpecIndex -> LangChain tool bridge
│       ├── prompts.py           # B4: System prompt builder (mr_name, not mr_id)
│       ├── transforms_menu.py   # B4: Transform menu generator (compound groups + escaping)
│       └── engine.py            # B4: ReAct agent + 3-retry validation loop
└── tests/
    ├── test_transforms.py   # 42 tests: determinism, correctness, domain invariants
    ├── test_dsl.py          # 27 tests: Pydantic validation, hashing, compound rules
    └── test_registry.py     # 9 tests: triage, dedup, export
```

#### 🛡️ 核心防幻觉机制 (Key Anti-Hallucination Mechanisms)

1. **Transform whitelist**: Pydantic rejects any `transform_steps` not in the registry
2. **Deterministic `mr_id`**: MD5 hash of (`format` + `scope` + sorted transforms) — dedup regardless of LLM naming
3. **Evidence hydration**: `chunk_id` looked up in ChromaDB for ground-truth `rule_severity` — LLM never provides severity
4. **Hallucinated `chunk_id` rejection**: If `chunk_id` not found in ChromaDB, compilation fails
5. **0.39 distance threshold**: Results below relevance are marked `above_threshold: true`

#### ✅ 自动化测试报告 (95/95 Tests Passed)

**1. 独立单元测试 (Unit Tests - 78/78)**
* **B2 Transforms (42)**: 测试所有 13 个原子操作的确定性、正确性、边界条件及领域不变量保障。
* **B5 DSL Models (27)**: 验证 Pydantic 模型、操作白名单强制管控、确定性 MD5 唯一哈希、以及复合操作组全有或全无校验（8 个专项用例）。
* **B6 Registry (9)**: 验证审查分级隔离（Enforced/Quarantine）、哈希去重逻辑及 JSON 导出。

**2. 真实数据集成测试 (Integration Tests - 17/17)**
* 使用真实加载的 ChromaDB 及 2,048 切片数据，全链路测试代理提问、防幻觉拦截、去重、及规范溯源（如自动填充 `rule_severity`）。

#### 🚀 首次实战运行记录 (Live Initial Run)

* **模型引擎**: `moonshotai/kimi-k2-instruct` via Groq
* **运行策略**: 选用单一意图目标 `--target ordering_invariance` 针对 VCF 进行测试。
* **Agent 表现**: 代理共执行 50 次自主检索调用，成功探索了 7 大规范排序主题（如头部、INFO、样本排序等）。触发了 429 频率限制时，系统实现了透明自平衡重试，无失败记录。

**产出成果 (Mined MRs)**：系统最终产出 **3 条高置信度变异关系 (Enforced MRs)**，全部具备规范级别“绝对不变性”证据（CRITICAL Evidence）。

> [!NOTE] 
> **Why Only 3 MRs for 'Ordering Invariance'?**
> 这是由防幻觉体系强约束带来的预期结果：Agent 广泛探索了 7 大方向，但严格的规范原文仅针对 Header Lines、Structured Keys 和 Genotype fields 给出了“可自由重排而不影响语义”的铁证依据。其他诸如 INFO、ALT 列排序等均因为受引用的索引制约被系统有效拦截，充分体现了这套管线的安全性。在完整的意图和格式矩阵全量运行时，预计安全产出量将达到 15–30 条。

### 8. 高阶结构特性：复合变异组约束与级联验证 (Advanced Structural Features)

为了保证大模型生成的复合变异（例如必须同时运行的多个原子操作）能够绝对符合生物学规范逻辑，此阶段我们重点增加了以下容错与反制幻觉的设计架构：

#### 🔧 1. 动态获取复合原子组 (Dynamic Compound Groups)
* **文件**：`transforms/__init__.py — get_compound_groups()`
* 通过注册中心动态发现并绑定。这是统一管理的唯一事实来源（Single Source of Truth），能直接供给于：由模型驱动的 DSL 校验器（强制管控）、Agent Prompt 菜单（大模型操作参考依据）、以及测试脚本。若是后续扩展加入新的复合组别，框架能自动发现并收录（Zero code changes needed）。

#### 🛡️ 2. 全有或全无强制机制 (All-Or-Nothing Validation)
* **文件**：`dsl/models.py — _compound_steps_all_or_nothing`
* 作为 `@model_validator(mode="after")` 拦截器安全运行。当 Agent 输出或漏掉了某组共生关系的子集时，会触发拦截并向 Agent 回传包含所有必然成员的明细错误指引（专门用以辅佐 LangGraph 重试闭环的自我修复）。
* **管线执行顺序 (Validation Pipeline Order, 从外到内收紧栅栏)**：
  1. `@field_validator("scope")` — 拒绝非法的 scope 字符串对象。
  2. `@field_validator("transform_steps")` — 第一层拦截非白名单名称及大模型捏造的操作。
  3. `@model_validator: _must_have_content` — 拒绝不输出步骤或证据的内容。
  4. `@model_validator: _compound_steps_all_or_nothing` — **仅在步骤 2 执行通过时才会校验**，用于检验并拒绝残缺的业务复合步骤块。

#### 🧠 3. 稳健灵活的菜单层与 Prompt 解析逻辑 (Transform Menu Architecture)
* **Layer 1 - 元数据挂载 (Registry metadata)**：`@register_transform` 引入了 `group="alt_permutation"`，将函数动作标记到聚合维度。
* **Layer 2 - 菜单生成 (`build_transforms_menu`)**：循环遍历聚合表：包含共同标签函数组成 `***` 开始的部分代码块，不包含的自动下推；最后将其整合为大模型参考底板。其中大括号符被自动转义 (`{{/}}`)。
* **Layer 3 - 模板编排 (System Prompt Template)**：采用局部依赖注入 (`partial_variables`) 塞入转义后的动作菜单，彻底绕过了 LangChain 常见的 `.format()` 大括号占位符失效死锁报错。
* **Layer 4 - 通信包装 (`prompts.py`)**：安全封装并解包 SystemMessage，交接干净纯净的 String 直通 `create_react_agent(prompt=...)` 主动代理中。

#### 🧪 4. 复合校验防漏错专项测试 (DSL Unit Tests)
基于 `test_dsl.py` 全数绿通的复合用例全景扫描：

| Test Case | What it verifies (用例意图校验情况) |
| :--- | :--- |
| `test_all_four_present_passes` | 完整传入四合一共生操作项，顺利接受 |
| `test_all_four_in_any_order_passes` | 操作名任意排序，顺利接受，无关先后顺序 |
| `test_single_compound_member_rejected` | 提供 1/4 个操作 → 准确拦截并报错指出缺失的另外 3 个 |
| `test_two_of_four_rejected` | 提供 2/4 个操作 → 准确拦截并指出缺失的 2 个 |
| `test_three_of_four_rejected` | 提供 3/4 个操作 → 准确拦截并指出缺失的 1 个 |
| `test_non_compound_transforms_unaffected`| 单体原子（例如 `shuffle_meta_lines`）自由通行不受该校验器阻碍 |
| `test_compound_plus_extra_transforms_passes` | 完整的共生操作块叠加另外的独立源子操作也能合法通过 |
| `test_error_message_lists_all_required_members`| 错误日志必定枚举列出全体需附着的成员名，以便无痛指导重试 |

## 🦾 阶段 C：基于约束生成的交叉执行与差分判定 (Constraint Generation & Cross-Execution)

如果说 Phase B 是挖掘“变体规律 (MR)”的大脑，那么 Phase C 就是将这些规则化为真实的测试用例，去“拷问”那些顶尖生物信息学库的“处刑室”。我们将结合 Hypothesis 的属性测试、Z3 的符号约束求解 以及 跨语言差分执行，来构建一条严密的流水线。

### 1. 真实生物学种子注入与语料库管理 (Seed Corpus Management)

要让测试具有"生物学现实意义"并发现深层 Bug，我们不能仅凭空捏造随机乱码，必须构建一个多层级的种子库（Seed Corpus）：

*   **第一层：规范基准种子 (Spec Example Seeds / Tier 1)** — 3 个手工构造文件，提交到 git
    - `seeds/vcf/minimal_single.vcf`, `minimal_multisample.vcf`, `spec_example.vcf`
    - 用于冒烟测试，覆盖最小 VCF v4.3 结构
*   **第二层：真实世界公共测试语料 (Public Real-world Seeds / Tier 2)** — ~30 个文件，通过 `seeds/fetch_real_world.py` 按需下载（`.gitignore` 中排除以保持仓库体积）
    - **htsjdk test resources** (Apache 2.0): 多样本 + 结构变异 + NaN QUAL + gVCF (`<NON_REF>`) + dbSNP/ClinVar INFO 标签
    - **bcftools test suite** (MIT-equivalent): 规范化边界、CSQ 注释、concat/merge/isec 输入
    - **hts-specs test corpus** (MIT-equivalent): VCF v4.1/v4.2/v4.3/v4.5 的 spec 合规性测试
    - **GATK test resources** (Apache 2.0): Funcotator SnpEff ANN、gVCF、feature-source 测试
    - 详细清单与多样性矩阵见 `seeds/SOURCES.md`
    - 每文件上限 500 KB (保证 Phase C 迭代速度)
*   **第三层：极限界限种子 (Generated Corner-case Seeds / Tier 3)** — 规划中
    利用 Z3 生成满足极端物理约束的头部/记录，或引入 KLEE 符号执行引擎生成种子文件。

**多样性轴覆盖**（每个轴均至少有一个 Tier-2 种子命中）：
1. VCF 规范版本 (v4.1/v4.2/v4.3/v4.5)
2. 结构变异 (`<DEL>`, `<INV>`, `<DUP>`, `<BND>`)
3. gVCF (`<NON_REF>`) — 用于 `inject_equivalent_missing_values`
4. CSQ (VEP) / ANN (SnpEff) 注释 — 用于 `permute_csq_annotations`
5. 相位 vs 非相位基因型
6. 深层 FORMAT (`GT:GQ:DP:AD:PL`)
7. NaN QUAL / 缺失值
8. 多等位基因记录 — 用于 `split_multi_allelic`
9. 可左对齐的 indel (同聚核苷酸运行) — 用于 `left_align_indel`
10. BCF 编解码练习 — 用于 `vcf_bcf_round_trip` 及 `permute_bcf_header_dictionary`
11. 丰富的 dbSNP/ClinVar 注释标签
12. 多体（polysomy）基因型

每轴对应的代表文件与相关 transform 见 `seeds/SOURCES.md` 的多样性矩阵。

### 2. 跨语言解析器的“归一化”适配 (Canonical Normalization Adapters)

必须为每个工具编写 Adapter，将输出强行映射到一套极其严苛的 **Canonical JSON (规范化 JSON)** 模式中。

#### 🧬 2.1 差分矩阵与规范化结构
*   **SAM 格式矩阵**：HTSJDK (Java) vs Biopython (Python) vs SeqAn3 (C++) vs Pysam (Python)
*   **VCF 格式矩阵**：HTSJDK (Java) vs Pysam (底层为 HTSlib) (⚠️ SeqAn3 暂不支持 VCF IO，故移除)。
*   **Canonical 结构要求**：TAGS 无序化为 Map，FILTER 转化为 Set，CIGAR 规范化为列表，严格保持 `@SQ` 的物理顺序。

#### 🚨 2.2 核心陷阱规避：坐标系归一化 (Coordinate Normalization Rules)
跨语言比对最容易触发假阳性的就是坐标系（0-based 还是 1-based）问题，适配器必须严格执行以下修正：

| 解析器 (Parser) | SAM POS 原始读取 | VCF POS 原始读取 | Adapter 修正策略 (Action) |
| :--- | :--- | :--- | :--- |
| **HTSJDK** | 1-based | 1-based | 无调整 (No adjustment) |
| **Biopython** | 0-based | N/A | SAM 坐标 + 1 |
| **pysam** | 0-based | 0-based | SAM 和 VCF 坐标均需 + 1 (⚠️ VCF规范是1-based，但Pysam底层默认返回0-based) |
| **SeqAn3** | 0-based | N/A | SAM 坐标 + 1 |

### 3. Transform Dispatch：变异调度桥接器 (KEY DESIGN CHALLENGE)

Phase B 产出的 `transform_steps` 是字符串（如 `"shuffle_meta_lines"`），而这 20 个原子函数拥有完全不同的入参签名。我们在 `generators/dispatch.py` 中构建了一个统一接口 `apply_transform(name, file_lines, seed, *, runner_hook=None, format_context=None)`，按以下 6 种粒度进行动态调度：

| 调度粒度 (Level) | 适用转换函数 (Transforms) | 期望提取输入 (Input) | 调度策略 (How to apply) |
| :--- | :--- | :--- | :--- |
| **文件级 (File)** | `shuffle_meta_lines`, `permute_sample_columns` | `list[str]` (全文行) | 直接对整个文件的文本行数组进行处理 |
| **单行/区块级** | `permute_structured_kv...`, `reorder_header...` | `str` (单行/表头) | 拦截提取对应区块，遍历单行调用后重新拼接 |
| **字段级 (Field)** | `shuffle_info_field_kv`, `permute_Number_...` | `str` (特定列的值) | 切分至特定的格式列，解析后塞回原位 |
| **多字段级(CIGAR)** | `split_or_merge_cigar...`, `toggle_cigar...` | CIGAR/SEQ/QUAL | 提取多列比对特征，转换并重建字符串长度同步 |
| **复合级(Compound)**| `choose_permutation` + `permute_ALT` + `remap_GT`... | Record (单条变体) | 协同执行：先生成 `π`，然后在同一记录上绑定执行 |
| **Runner-aware + Format-aware (writer)** | `sut_write_roundtrip` | `list[str]` (全文行) + 主 SUT 的 `ParserRunner` 实例 + 当前格式 | Dispatch 向装饰器声明 `needs_runner_hook=True` 与 `needs_format_context=True`，wrapper 从 orchestrator 接收 `runner_hook` 和 `format_context` 两个 kwarg，调用 `runner.run_write_roundtrip(path, fmt)` 并把 rewritten text 切回 `list[str]` 返回 |

**SUT 写入协议 (runner hook 结构)**。`sut_write_roundtrip` 之所以能保持格式无关，是因为两个简单约定：

1. `ParserRunner` 基类声明可选方法 `run_write_roundtrip(path, format_type) -> RunnerResult`，默认 `NotImplementedError`；同时暴露 `supports_write_roundtrip: bool = False`。
2. 具体 SUT runner（如 htsjdk / pysam）在构造阶段声明支持的格式（VCF、SAM 或两者），在 `run_write_roundtrip` 内部按照 `format_type.upper()` 分流到 `VCFWriter` / `SAMFileWriterFactory` 或 `VariantFile("w")` / `AlignmentFile("wh")`，对不支持的格式返回 `error_type="ineligible"`（transform 层 gracefully no-op）。

这意味着：**引入一个新的可写 SUT 的代价只是一个 runner 子类**。Transform library、dispatch、strategy router、orchestrator 都无需变动。

### 4. Hypothesis 与 Z3 驱动的变体生成引擎 (Generation Engine)

#### 4.1 策略路由器与 `@given` 驱动的双模主循环 (Strategy Router & Dual-Mode Orchestrator)

Phase B 输出的 `transform_steps` 只是字符串名（如 `"shuffle_meta_lines"`）。系统必须自动找到对应的 Hypothesis 策略并接入主循环。`strategy_router.py` 负责将全部 20 个变换名映射到 `@composite` 策略工厂：

```python
# 单作用域：一个 transform 只服务于一个格式
STRATEGY_MAP = {
    "shuffle_meta_lines":       st_shuffle_meta_lines,    # VCF
    "permute_structured_kv...": st_permute_structured_kv, # VCF
    "permute_ALT":              st_alt_permutation,       # VCF (compound)
    "remap_GT":                 st_alt_permutation,       # VCF (compound)
    "permute_optional_tag...":  st_permute_optional_tags, # SAM
    ...  # 其它 19 个常规 transform
}

# 格式作用域：同一 transform 根据 fmt 映射到 VCF 或 SAM 变体
FORMAT_SCOPED_MAP = {
    ("sut_write_roundtrip", "VCF"): st_sut_write_roundtrip_vcf,
    ("sut_write_roundtrip", "SAM"): st_sut_write_roundtrip_sam,
}

def get_strategy(name, fmt=None):
    # 格式作用域优先；查不到再回落到单作用域表
    if fmt and (strat := FORMAT_SCOPED_MAP.get((name, fmt.upper()))):
        return strat
    return STRATEGY_MAP.get(name)
```

**格式作用域查表原因**：`sut_write_roundtrip` 在 MR 注册表里以单条 `format="VCF/SAM"` 存在，但在 Phase C 的 Hypothesis 抽样阶段，VCF MR 应该从 `corpus.vcf_seeds` 中取种子，SAM MR 应该从 `corpus.sam_seeds` 取。两个策略的前提 (`assume(any("##fileformat=VCF" ...))` vs `assume(any(l.startswith("@HD")))`）完全不同，所以必须按 `fmt` 分流到不同的 `@composite` 策略工厂。`orchestrator._run_mr_with_hypothesis` 把当前 MR 的 `fmt` 传入 `get_strategy(name, fmt=fmt)`，单作用域 transform 则忽略这个参数，零行为改变。

`orchestrator.py` 据此实现**双模执行**（`use_hypothesis=True|False`）：

| 模式 | 触发条件 | 循环驱动 | 收缩能力 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **Hypothesis 模式** | `use_hypothesis=True` | `@given(params=strategy(corpus))` 随机抽取种子 + RNG 种子 | 完整 `Phase.shrink` 自动收缩 | 生产级探索与回归测试 |
| **静态模式** | `use_hypothesis=False`（默认） | `for seed in seeds` 逐文件遍历，确定性 RNG | 无 Hypothesis 收缩 | DummyRunner 测试、CI 快速冒烟 |

两种模式共享同一个核心执行函数 `_run_single_test()`，零代码重复。

#### 4.2 Hypothesis 收缩的触发机制 (How Shrinking is Triggered)

**关键架构决策**：在“神谕判定失败”与“Hypothesis 启动收缩寻找极小值”之间，构建了深度的三层异常信号传导机制：

*   **Layer 1 - 自定义异常对象**：通过定制 `_OracleFailure` 异常携带完整的 `OracleResult` 与差异日志列表 `diffs`，通过对异常文本切片仅外放至多 5 条的判定结果差异串记录来确保系统报错清爽度。
*   **Layer 2 - 延迟异常触发 (Deferred Raise)**：在核心管线 `_run_single_test()` 过程中，任意一个解析侧（Metamorphic）判负引发错误生成报案底档后，系统**不再第一时间**切断程序（抛出打断操作）。而是利用 `first_failure` 拦截装填首发失分项异常对象供下沉到 `Differential Oracle` 排查矩阵同步做判定处理并生成全谱系 Bug 报单，直至尾层 `finally` 被全清理打通结束时最后触发引发该拦压的终结致命引发动作（`raise first_failure`），确保了一站测试不中断的最大化爆出点发现量和报错量收成。
*   **Layer 3 - Hypothesis 底座捕捉介入 (Phase.shrink)**：用受外圈 `@given` 装饰绑扎隔离的最外环逻辑 `_hypothesis_test()`。当该 `_OracleFailure` 从延时队列真正溢冒逃逸时，不在忽略名录且未接引处理就会被底层系统视作为本次引发测试翻车落败事件。直接将其引流到 Hypothesis 切入到独家的核心修剪功能池 `Phase.shrink`。在该模块自主缩水变体种子内容生成新的更简内容后回环重击至其再次复现同一落空报错点后视为取得此错极简靶向。将已成功复刻的小标的底子与 Bug 落地持久化存档报表提交到终端后将最纯化的引发结果退出最外层脱出警报通识传开。

**完整收敛闭环 (Complete Signal Chain)**：
`deep_equal() -> tuple(False, ...)` -> `Metamorphic/DifferentialOracle.check()` -> `_run_single_test()` captures & defers raise -> `Hypothesis` catches exception -> Phase.shrink repeated failures finding minimal -> escape to `_run_mr_with_hypothesis` catching minimal failure.

#### 4.3 Z3 后置物理约束门控 (Z3 Post-Transform Guards)

Z3 约束被直接编织进 `dispatch.py` 的三个高危调度包装器中。当变异操作破坏了文件的物理约束时，调用 `_h_assume(False)` 指示 Hypothesis 丢弃该样本并重新生成：

| 调度包装器 | Z3 守卫 | 触发条件 |
| :--- | :--- | :--- |
| `split_or_merge_adjacent_cigar_ops` | `check_cigar_seq_constraint(ops, seq_len)` | CIGAR 查询消耗长度 != SEQ 长度 |
| `toggle_cigar_hard_soft_clipping` | `check_cigar_seq_constraint(ops, new_seq_len)` | 软/硬裁剪切换后长度不一致 |
| `_apply_compound_alt_permutation` | `check_info_number_a(alt_count, values)` | Number=A 字段值个数 != ALT 等位基因数 |

`_h_assume()` 包含上下文检测逻辑：在 `@given` 内部调用真正的 `hypothesis.assume()`，在静态模式下安全跳过（无副作用）。

#### 4.4 自定义收缩钩子 (Custom Shrink Hooks)

`shrink.py` 现已**直接编织进 `report_builder.py`**。每当生成 Bug 报告时，保存到磁盘前自动对原始种子和变体文件执行收缩：

*   **VCF 收缩**：保留 `##fileformat` 为绝对首行，仅留最多 2 条 `##INFO`/`##FORMAT` 元行，裁减至 1 条数据记录。
*   **SAM 收缩**：保留 `@HD` 为绝对首行，仅留 1 条 `@SQ`，丢弃 `@RG`/`@PG`/`@CO`，裁减至 1 条比对记录并限制可选 TAG 数 <= 2。

Bug Report 目录中的 `x.vcf` 和 `T_x.vcf` 现在是**最小复现文件**，而非原始全文。

### 5. 跨语言执行器与双重神谕 (Runners & Dual Oracles)

系统设计了两个独立的测试神谕，它们均将底层判定委托给同一个核心裁决器 `deep_equal`。该核心使用规范化 JSON 进行语义级的对比判定。

#### 5.1 核心裁决法官：The Core Judge (`deep_equal.py`)
这是负责下定胜败的最终决策树工具。采用严密优先级的派发机制处理阻抗不同语言实现的表面不符表现形式：
*   **跨类型数字提升 (Cross-Type Numeric Promotion)**：遭遇 `int` 对抗 `float` 精度对比判断（如 `MAPQ: 60` 对撞 `60.0`），自动将其同时提权转化为 float 后介入 `math.isclose()` 防止触发语言特性引起的伪阳错判点（False DETs）。
*   **高危放宽校验区 (QUAL-specific tolerance)**：默认设定极微 `float_tol=1e-6`，但在处理 `QUAL` 或 `qual` 键值计算中遇到浮点流失点（如跨语言 Java `29.0` 和 Python 截断后的 `28.9999999`），系统自动启动由百万分之一退宽拉低到百分级宽网容错度网底（`QUAL_FLOAT_TOL` 为 0.01）防御误判。
*   **字典与集合型态判定避坑 (Dict / Set)**：对字典采用忽略 Key 存在排序的做法进行集合合并推解对比值。针对 Set 采取数学相等推算差值。
*   **严列定位防差判定 (List Elements)**：对于类似 CIGAR 解析形成的有序位次字典数组，实施严格按先后索引序长度核算判定。列表偏调、不匹配都会直接向上传红判定异动。

#### 5.2 变体语义判定：Metamorphic Oracle (`metamorphic.py`)
等价验证防线：确保同一解析器通过测试 `parse(x) == parse(T(x))` 对等价变体的健壮性。
*   **执行流与单端闪断熔断 (Execution Flow & Crash early exit)**：分别提取同组 Runner 唤起新老版本文件（双次唤起提入格式内容），若任选一次测试端遭遇 timeout、crash 或者直接跑出解析出错异常，系统不会无底线追测深入比较 `deep_equal`。立下判定并通报异常快速反馈脱出。
*   **解析端语言体隐匿无知感 (Parser-Agnostic)**：充当统一定尺中间件不在乎被比较调集调用底层逻辑体（比如是用 C++ 开发，Java 或是 Pysam / Biopython 提供），完全接受它们脱手抽象规范的提取格式 `canonical_json: dict` 实现评判任务。

#### 5.3 跨界差分判定：Differential Oracle (`differential.py` + `consensus.py`)

差分判官从 v2 开始采用 **多数投票共识**（Majority-Voting Consensus）而不是简单的两两对比。核心思想：**单个 SUT 有 bug 不应该污染整体判断**。

> **Reference**: McKeeman, W. M. (1998), "Differential Testing for Software,"
> *Digital Technical Journal* 10(1):100–107. The original differential-testing
> paper that motivates N-version voting on equivalent inputs. Our consensus
> oracle is a direct application: instead of declaring any pairwise diff a
> bug, the strict-majority bucket wins, with htslib (samtools/bcftools) as a
> tie-breaker because it ships from the hts-specs maintainers themselves.

**共识投票规则 (`get_consensus_output`)**：
1. 将所有解析器的规范化输出按语义等价分桶（`deep_equal`）。
2. 严格多数桶（`> N/2`）直接胜出 → 它就是 "正确答案"。
3. 若无严格多数，**htslib（gold-standard tie-breaker）** 所在的桶自动胜出。htslib = bcftools（VCF）/ samtools（SAM），是 hts-specs 维护组的官方 CLI，其输出最接近规范的权威解读。
4. 若无多数且无 htslib 裁决 → `INCONCLUSIVE`。不追责任何 SUT。

**格式感知资格过滤 (Format-Aware Eligibility)**：
投票前先按文件格式过滤 SUT。若 SUT 不支持当前格式，其输出**完全丢弃**（不算"不同票"也不算"失败"，叫 `ineligible_parsers`）。这样 VCF 运行中 biopython/seqan3（SAM-only）保持静默，不会把 3/4 的多数搞成 3/5 的平局。判定规则：
- SUT 自报 `error_type="ineligible"` → 丢弃。
- `eligibility_map[parser_name]` 不包含当前 `format_context` → 丢弃。

**每个解析器的失败归类 (per-parser failure_cause)**：
| `failure_cause`      | 语义                                               | 问责方        |
| :------------------- | :------------------------------------------------- | :------------ |
| `against_consensus`  | 主 SUT 在 x 和 T(x) 上都与共识相悖                 | SUT           |
| `non_conformance`    | 仅单侧与共识相悖（x 或 T(x) 其一对，另一错）       | SUT（非 MR）   |
| `mr_invalid`         | htslib 标记 T(x) 为 malformed，或 共识 (x) ≠ 共识 (T(x)) | **MR → 隔离** |
| `inconclusive`       | 无多数且无 htslib tie-breaker                      | 无人          |
| `crash` / `timeout`  | 解析器崩溃                                         | 通常是 SUT    |

**htslib 不合法信号 (Reliability guard)**：若 htslib 因 "invalid/malformed" 报错，系统置位 `htslib_rejected_as_invalid`，quarantine 据此直接隔离 MR——上游参考实现说文件格式错了，就是 MR 出了问题。

#### 5.4 拒绝判定：Error-Consensus Oracle (`error_consensus.py`)

> **Reference**: Chen, T. Y., Kuo, F.-C., Liu, H., Tse, T. H. (2018).
> "Metamorphic Testing: A Review of Challenges and Opportunities." *ACM
> Computing Surveys* 51(1):4, §3.2 — the canonical taxonomy of MRs. Our
> 4-vote oracle (accept / silent_skip / reject / crash) is a rejection-
> path specialization of differential testing where the "consensus" is
> on parser verdicts rather than canonical-JSON outputs.


Rank 3 覆盖率杠杆专用。`deep_equal` 共识在**恶意输入**场景下毫无意义——被突变的种子没有"应保留的语义"，比较 canonical_JSON 只会产生一致的垃圾。为此 `test_engine/oracles/error_consensus.py` 引入一套**四元投票**：

| ErrorVote       | 判定条件                                                   |
| :-------------- | :--------------------------------------------------------- |
| `ACCEPT`        | 解析成功且记录数与原种子一致                                 |
| `SILENT_SKIP`   | 解析成功但记录数**少于**原种子（解析器默默丢弃了非法记录）    |
| `REJECT`        | 返回 `error_type="parse_error"`——识别为校验错误              |
| `CRASH`         | 返回 `error_type="crash"`——进程异常终止                     |
| `INELIGIBLE`    | 格式不兼容（不计入投票）                                     |

多数规则：`REJECT + CRASH` 同属"拒绝"阵营，票数 > N/2 则 majority 为拒绝；此时任何 `ACCEPT / SILENT_SKIP` 的 SUT 即为 **silent acceptor**（直接判为 conformance bug）。反之若多数是 `ACCEPT`，少数的 `REJECT` 只算过度严格，记录但不升格为 Bug。

`_run_single_test` 在检测到当前 MR 的 transform_steps 包含 `mr_engine.transforms.malformed.MALFORMED_TRANSFORM_NAMES` 中任一条目时自动走 `_handle_rejection_consensus`，跳过 metamorphic + differential 块。如果 primary target 就是 silent acceptor，返回 `_OracleFailure` 触发 Hypothesis 收缩，生成最小复现 Bug 报告（与其他 Oracle 同一 pipeline）。

**配套 strict_mode**：`vcf_normalizer.normalize_vcf_text(..., strict_mode=True)` 与 `sam_normalizer.normalize_sam_text(..., strict_mode=True)` 在严格模式下会对突变器针对的每条规则（##fileformat 首行、INFO Number=A 基数、GT 索引、CIGAR/SEQ 长度）抛出 `ValueError`。Reference runner 默认走非严格以保持向后兼容；error-consensus 路径下启用严格模式，以便 reference runner 能正确投 REJECT。

#### 5.5 API 查询判定：Query-Consensus Oracle (`query_consensus.py`) — Rank 5

文件→文件 MR 永远碰不到 SUT 库的 **API 查询表面**——`vc.isStructural()`、`vc.getNAlleles()`、`smartMergeHeaders()` 这些方法只有在程序调用者使用 SUT API 时才会执行。我们的 oracle 之前只比较 canonical JSON，因此 htsjdk 的 ~460 行 API 查询代码长期 0% 覆盖。

Rank 5 解决方案：把 MR 的形式从 `parse(x) == parse(T(x))` 扩展到 `P(parse(x)) == P(parse(T(x)))`，其中 P 是任何**公开的标量返回查询方法**。框架通过**反射**自动发现每个 SUT 暴露的方法名（NEVER 硬编码 per-SUT），LLM 在 Phase B 看到这些名字并构造 `API_QUERY_INVARIANCE` MR。

**反射机制（按语言）**：
- **Java（htsjdk）**：`Class.getMethods()` 过滤为 public、零参、标量返回（boolean / int / long / String / Enum）的 getter 风格方法。CLI：`BioTestHarness --mode discover_methods VCF`。
- **Python（pysam / biopython / reference）**：`dir()` + `inspect.signature()` 过滤为 public、effectively-nullary、标量返回。Pydantic v2 类走 `model_fields` 快路径以避开 `model_dump`/`model_validate` 等框架噪声。
- **C / C++ / Rust**：rustdoc JSON / libclang AST walk 出方法清单 → 生成 dispatch adapter（`harnesses/_reflect/`）。详见 §13。

**ParserRunner opt-in 契约**（与 `supports_write_roundtrip` 同形）：
```python
supports_query_methods: bool = False
def discover_query_methods(self, format_type: str) -> list[dict]: ...
def run_query_methods(self, input_path, format_type, method_names) -> RunnerResult: ...
```
默认 `supports_query_methods = False`，runner 不参与 query 投票。htsjdk / pysam / biopython / reference 全部 opt-in。

**Oracle 投票规则**（`get_query_consensus`）：对每个被 MR 请求的方法 m：
- 同一 voter 在 x 和 T(x) 上结果不同 → `methods_changed`（MR 错了，或所有 SUT 同时坏了）；
- voter 间结果不一致 → `methods_cross_sut_disagreement`（差分 bug）；
- voter 报 `__error__`（方法不存在 / 调用崩溃）→ 该 voter 在该方法上不参与投票。

主 SUT 在 `methods_changed` 中即触发 `_OracleFailure`，Hypothesis 启动收缩，生成最小复现 bug 报告——与 metamorphic / rejection 同一 pipeline。

**MR DSL 扩展**：`MetamorphicRelation` 增加 `query_methods: list[str]` 字段。LLM 在生成 MR 时把要比较的方法名填入此字段；orchestrator 的 `_handle_query_consensus` 分支检测 `query_method_roundtrip in transform_steps`，从 `mr_dict["query_methods"]` 读取列表，再调用各 voter 的 `run_query_methods`。

> **References**:
> - Chen, T. Y., Kuo, F.-C., Liu, H., Tse, T. H. (2018). "Metamorphic
>   Testing: A Review of Challenges and Opportunities." *ACM Computing
>   Surveys* 51(1):4, §3.2 — API-level metamorphic relations.
> - Xu, C., Terragni, V., Zhu, H., Wu, J., Cheung, S.-C. (2024).
>   "MR-Scout: Mining Metamorphic Relations from Existing Test Cases."
>   *ACM TOSEM* 33(6), arXiv:2304.07548. Reports +13.5 pp line coverage
>   from MRs of exactly this form, validating the +5–10 pp lift we
>   target.
> - Blasi, A., Gorla, A., Ernst, M. D., Pezzè, M., Carzaniga, A. (2021).
>   "MeMo: Automatically Identifying Metamorphic Relations in Javadoc
>   Comments for Test Automation." *Journal of Systems and Software*
>   181:111041 — auto-mines equivalence MRs from Javadoc; could pre-fill
>   our discover_query_methods output with semantic prior in a future
>   iteration.

### 6. 故障分诊与最小化 Bug 报告生成 (Triage & Bug Reporting)

遇到神谕报错时，Triage Service 自动进行分类，并打包生成 `BUG-{timestamp}/` 目录。**文件在写入前自动经过 shrink 收缩处理**。包含：
*   `x.vcf` (**已收缩**的最小复现种子)
*   `T_x.vcf` (**已收缩**的最小复现变体)
*   各解析器的差异 `canonical_outputs/`
*   崩溃日志，以及 `evidence.md` (Phase B 挖掘到的规范依据)。

### 7. 📁 项目代码结构与产出 (Project Structure & Files)

**Phase C 产出: 32 个 Python 文件 (3,846 行) + 1 个 Java Harness (425 行) + 1 个 C++ Harness (248 行) + 6 个基准种子。**

```text
BioTest/
├── seeds/                             # C1: Tier 1 基准种子库
│   ├── vcf/spec_example.vcf, minimal_multisample.vcf, minimal_single.vcf
│   └── sam/spec_example.sam, minimal_tags.sam, complex_cigar.sam
├── harnesses/                         # C2: 各语言底层解析包装器
│   ├── java/BioTestHarness.java       # HTSJDK -> stdout (Canonical JSON)
│   └── cpp/biotest_harness.cpp        # SeqAn3 -> stdout (Canonical JSON)
└── test_engine/                       # C3-C7: 核心测试管线
    ├── __main__.py                    # CLI: python -m test_engine run
    ├── orchestrator.py                # 👑 双模主循环 (Hypothesis / Static)
    ├── canonical/                     # C3: JSON 归一化协议 (含 0-based 修正)
    │   ├── schema.py, vcf_normalizer.py, sam_normalizer.py
    ├── runners/                       # C4: 多语言沙盒执行器
    │   ├── htsjdk_runner.py, biopython_runner.py, pysam_runner.py
    │   ├── seqan3_runner.py, reference_runner.py
    ├── generators/                    # C5: 变体生成引擎
    │   ├── dispatch.py                # 变异调度桥接器 (含 Z3 后置守卫)
    │   ├── strategy_router.py         # 🆕 策略路由器: transform_name -> Hypothesis策略
    │   ├── vcf_strategies.py, sam_strategies.py
    │   ├── z3_constraints.py, shrink.py, seeds.py
    ├── oracles/                       # C6: 双重神谕裁决引擎
    │   ├── deep_equal.py, metamorphic.py, differential.py, det_tracker.py
    └── triage/                        # C7: 智能分诊与报告生成 (含自动收缩)
        ├── classifier.py, report_builder.py, evidence_formatter.py
```

### 8. 🏆 实机测试成果与真实 Bug (Live Results & Real Bug Showcase)

#### ✅ 191/191 深度加固测试全绿通过 (Hardened Test Suite Perfect Pass)
底座防线极其稳固，全面覆盖归一化、调度、生成、对比以及极限异常防御（总计 191 测，仅耗时 0.42s）：
*   **基础管线 (127 测)**：Phase B 原子动作与 DSL 校验 (70)、Phase C 数据归一化与调度 (57)。
*   **深度加固 (64 测)**：
    *   **Runner 异常防御 (13)**：超时拦截、崩溃 stderr 捕获、可用性降级守卫。
    *   **Generator 边界 (25)**：Z3 极端约束拦截 (CIGAR/INFO)、Hypothesis 自定义收缩钩子保护。
    *   **Triage 并发防御 (18)**：并发报告构建、证据 Markdown 渲染容错。
    *   **虚拟主循环 E2E (8)**：注入 DummyRunners 验证全链路 DET 统计与空注册表防御。

#### 🔗 四层解耦组件的全连接 (Full Wiring of 4 Disconnected Layers)
在深度加固之后，完成了一次关键的"手术级重构"，将四个原本孤立的高级组件真正接入主运行时：

| 孤立组件 | 接入点 | 连接方式 |
| :--- | :--- | :--- |
| `vcf_strategies.py` / `sam_strategies.py` | `orchestrator.py` | 通过 `strategy_router.py` 映射，`@given` 装饰器驱动随机探索 |
| `z3_constraints.py` | `dispatch.py` | 3 个高危调度包装器内嵌 Z3 后置守卫，`_h_assume(False)` 丢弃违规样本 |
| `shrink.py` | `report_builder.py` | Bug 报告保存前自动对种子 + 变体执行格式感知收缩 |
| `seeds.py` + `SeedCorpus` | `orchestrator.py` | Hypothesis 策略通过 `st.sampled_from(corpus.vcf_seeds)` 随机抽取种子 |

#### 🛡️ 生产级并发与边界漏洞修复 (Production Hardening Fixes)
在实施 64 个深度加固测试时，系统成功排雷并修复了 2 个极其隐蔽的底层并发漏洞，确保了框架在严苛并发环境下的绝对健壮性：
*   **Windows 文件锁死漏洞 (`shutil.copy2` locking)**：在并发线程共享种子文件时触发 `PermissionError`，现已替换为原生 `read_bytes()`/`write_bytes()` 原子级无锁读写。
*   **毫秒级目录竞争 (`mkdir` race condition)**：`report_builder.py` 在极高并发下生成 Bug 报告时，因为时间戳碰撞导致 `FileExistsError`，现已引入 `exist_ok=True` 与线程安全的原子计数器。

#### 🐛 成功捕获 HTSJDK 工业级 Bug (Real World Impact)
在首次试运行的 27 组测试中，系统成功暴露出一个关键的规范相容性 Bug！
*   **发现过程**：系统生成了一个变体 $T(x)$，该文件改变了 `##INFO` 结构化元数据行的内部键顺序（例如生成了 `<Type=Integer,Number=1,ID=DP,...>`）。
*   **触发神谕**：Metamorphic Oracle 与 Differential Oracle 齐齐亮红灯。HTSJDK 崩溃拒绝解析，而 Python Reference 解析器成功解析。
*   **铁证闭环**：系统调出 Phase B 提取的证据 —— VCF v4.5 规范第 121 页明确标注 `[CRITICAL]`："Implementations must not rely on the order of the fields within structured lines..."
*   **结论**：**HTSJDK 违背了官方规范！** 系统已自动打包**经过收缩的**最小复现用例、差异 JSON 及证据 Markdown，可直接一键提交至 GitHub Issue。
*   **总 DET 发现率 (DET Rate)**: 在针对 3 个排序不变性 MR 的测试中，总体暴露出 **51.85%** 的行为差异率。这强有力地证明了基于语义的变体测试在寻找深度解析器漏洞上的巨大价值！

## 🔄 阶段 D：全局编排、配置驱动与反馈驱动闭环 (Grand Orchestration & Feedback Loop)

本阶段将 Phase A/B/C 从单次管线执行升级为**迭代式反馈驱动闭环**。大总管程序 (`biotest.py`) 反复调用 Phase B (挖掘) 和 Phase C (执行)，依据**覆盖率信号**精准制导下一轮的 MR 挖掘方向，同时引入 **pysam 第四 SUT** 以完善差分矩阵。

### 1. YAML 配置驱动设计 (Configuration-Driven Design)

系统拒绝硬编码。所有环境、目标、管线参数均通过 `biotest_config.yaml` 暴露给用户。新增的核心配置块：

#### 1.1 反馈终止控制 (`feedback_control`)

```yaml
feedback_control:
  enabled: true
  max_iterations: 5           # B->C 迭代最大轮数
  plateau_patience: 2         # SCC 连续 N 轮无增长则早停
  target_scc_percent: 95.0    # SCC 达标即终止
  timeout_minutes: 120        # 绝对超时限制
  primary_target: htsjdk      # 主目标 SUT：驱动反馈演化
  source_roots:               # 各 SUT 源码路径 (用于代码切片提取)
    htsjdk: SUTfolder/java/htsjdk/src/main/java
    biopython: .
    seqan3: SUTfolder/cpp/seqan3/include
    pysam: coverage_artifacts/pysam/source
```

#### 1.2 多语言覆盖率采集 (`coverage`)

```yaml
coverage:
  enabled: true
  jacoco_report_dir: coverage_artifacts/jacoco
  jacoco_cli_jar: coverage_artifacts/jacoco/jacococli.jar
  coveragepy_data_file: coverage_artifacts/.coverage
  coveragepy_source_filter: [Bio.Align.sam]
  pysam_coverage_dir: coverage_artifacts/pysam
  gcovr_report_path: coverage_artifacts/gcovr.json
  gcovr_build_dir: harnesses/cpp/build
  target_filters:           # 格式感知白名单 (Format-Aware Filtering)
    VCF: [htsjdk/variant/vcf, pysam]
    SAM: [htsjdk/samtools, Bio/Align/sam, seqan3/io/sam_file, pysam]
```

#### 1.3 主目标 vs 辅助判官架构 (Primary Target vs Auxiliary Oracles)

核心架构决策：反馈信号（SCC、代码覆盖率、盲区工单）**仅由 `primary_target` 驱动**。其他 SUT 仅作为差分判官参与比对，不干扰演化方向。

| 角色 | SUT | 职责 |
| :--- | :--- | :--- |
| **主目标 (Primary)** | 由 `primary_target` 指定（如 htsjdk） | 驱动 SCC、代码覆盖、盲区工单生成；其失败的 MR 对应规则保持为"未覆盖" |
| **辅助判官 (Auxiliary)** | 其余所有 SUT | 参与差分比对（DET 检测），发现的 Bug 正常报告，但不影响反馈演化方向 |

### 2. pysam 第四 SUT 集成 (4th SUT via Docker)

pysam (HTSlib Python 绑定) 在 Windows 上无法原生编译。系统采用 **Docker 子进程方案**实现跨平台集成。

#### 2.1 Docker Harness 架构

```text
harnesses/pysam/
├── pysam_harness.py    # 独立 CLI：python pysam_harness.py VCF /data/input.vcf
│                        # 支持 --coverage /cov/dir 模式
├── Dockerfile           # python:3.12-slim + pysam==0.23.3 + coverage>=7.0
└── build_docker.py      # 构建 + 冒烟测试脚本
```

**Harness 内部逻辑**：复用 `pysam_runner.py` 的 `_parse_vcf()` 和 `_parse_sam()` 逻辑。坐标修正：VCF `rec.pos + 1`，SAM `read.reference_start + 1`（pysam 对所有格式均返回 0-based）。

#### 2.2 Facade 模式 Runner (`pysam_runner.py`)

`PysamRunner` 实现透明降级：

```
PysamRunner.is_available()
  ├── _use_native() → True?  → 使用 in-process pysam (Linux/macOS)
  └── _use_docker()  → True?  → 委托 PysamDockerRunner (Windows)
       └── docker run --rm -v <temp>:/data biotest-pysam:latest VCF /data/input.vcf
```

下游代码无需感知底层执行方式。参见 `pysam_runner.py:46-73 PysamRunner`。

#### 2.3 Docker 内覆盖率采集

当 `coverage_dir` 配置启用时：
1. 容器启动前，coverage.py 先于 pysam 导入启动（确保模块被插桩）
2. 解析完毕后写入 `.coverage.<PID>` 到挂载卷
3. 同步输出 `summary.<PID>.json`（包含每文件的 executed/total/missing 行号）
4. 宿主机的 `PysamDockerCoverageCollector` 直接读取 JSON 摘要（无需 `coverage combine`，避免容器路径在宿主不存在的问题）

### 2.5 HTSlib CLI 第五 SUT：Gold-Standard Tie-Breaker

**文件**：`test_engine/runners/htslib_runner.py` + `harnesses/htslib/README.md`

为共识投票引入**权威裁决者**：`samtools` / `bcftools`。这两个 CLI 是 hts-specs 工作组自己维护的参考实现，其输出离规范最近——在 2-vs-2 平票场景下，它所在的桶自动胜出。

与其他 SUT 的角色对比：

| SUT         | 语言 | 底层库            | 独立实现 | 投票角色              |
| :---------- | :--- | :---------------- | :------: | :-------------------- |
| htsjdk      | Java | (自持)            | ✓        | 普通票                |
| pysam       | Py   | libhts (C, Cython)| ✗        | 普通票（见覆盖率警告） |
| biopython   | Py   | (自持，SAM-only)  | ✓        | 普通票（SAM 运行）    |
| seqan3      | C++  | (自持，SAM-only)  | ✓        | 普通票（SAM 运行）    |
| **vcfpy**   | Py   | (自持，VCF-only)  | ✓        | 普通票（VCF 运行）    |
| **noodles** | Rust | (自持，VCF-only)  | ✓        | 普通票（VCF 运行）    |
| **htslib**  | CLI  | **libhts (C)**    | (参考)   | **Tie-breaker**       |
| reference   | Py   | (我们的正则解析器) | ✓        | 普通票（独立实现）    |

> **pysam 覆盖率警告**：pysam 的 VCF/SAM 解析逻辑完全由 Cython 编译的 `.so` 提供 (`libcbcf.*`, `libcsam*.*`)，coverage.py 无法追踪原生代码。pysam 保留为投票者，但**不应作为 `primary_target`** —— 覆盖率驱动的 Phase D 反馈会得到平信号。主目标请选 htsjdk / vcfpy / noodles 中的一个。

**dispatch 逻辑**：
- VCF → `bcftools view <file>`，重序列化后的文本再喂进 `normalize_vcf_text` 得到 canonical JSON。
- SAM → `samtools view -h <file>`，同理经 `normalize_sam_text`。
- 格式不支持 或 对应 CLI 不在 PATH → 返回 `error_type="ineligible"`（不是 parse_error）。共识投票直接**丢弃**该结果，不计入失败也不计入不同票。

**平台支持**：Linux / macOS 原生。Windows 需走 WSL2 或包装 Docker。`HTSlibRunner(bcftools_path=..., samtools_path=...)` 支持显式指定路径。

**Reliability guard**：若 bcftools/samtools 以 "invalid / malformed / truncated / could not parse" 退出，设置 `htslib_rejected_as_invalid=True` —— 共识告诉 quarantine："这 MR 生成的文件连 gold-standard CLI 都拒收了，直接降级。"

### 3. 四层结构化反馈网络 (Four-Layer Feedback Network)

#### ⚡ 第一层：DSL 编译级内反馈 (Pydantic Sandbox — 已在 Phase B 实现)

当 Agent 输出 JSON 格式的 MR 时，立即进入 Pydantic 编译沙箱：白名单拦截 → 复合组全有或全无校验 → 语义化错误回传 → Agent 自我修复循环（上限 3 次）。确保落盘 MR 100% 合法。

#### 🛡️ 第二层：Hypothesis 执行级无 LLM 反馈 (Fuzzing & Shrinking — 已在 Phase C 实现)

Hypothesis 引擎接管。`_OracleFailure` 触发后，Hypothesis 利用 Z3 和 `shrink.py` 在毫秒级将种子文件收缩到最小复现代码。LLM 不参与。

#### 🗺️ 第三层：覆盖率导航的宏观反馈 (Coverage-Steered RAG — Phase D 核心创新)

##### 3.1 语义约束覆盖率 (SCC — Semantic Constraint Coverage)

**文件**：`test_engine/feedback/scc_tracker.py`

SCC 回答的问题是："规范中哪些规则已经被测试触及？" 它从 Phase A 的 2,048 个切片中提取 **453 个可测试规则**（CRITICAL + ADVISORY 级别），与当前 Enforced MR 的 evidence chunk_id 做集合求差。

**目标驱动感知 (Target-Centric Awareness)**：当 `primary_failed_mr_ids` 提供时，主目标失败的 MR 对应的规则视为"未覆盖" —— 即使辅助判官通过了，只要主目标没过，该规则仍在盲区列表中。

**格式感知隔离 (Format-Aware Isolation)**：当 `format_context="VCF"` 时，SCC 分母仅计算 VCF 规则（316 条），排除 SAM 规则（137 条），防止无关格式稀释覆盖率。

##### 3.2 多语言代码覆盖率采集 (Multi-Language Code Coverage)

**文件**：`test_engine/feedback/coverage_collector.py` (817 行)

| SUT | 工具 | 插桩方式 | 数据流 | 格式过滤 |
| :--- | :--- | :--- | :--- | :--- |
| **htsjdk** | JaCoCo | `-javaagent` 运行时注入；agent JAR 复制到 ASCII 临时目录规避 Unicode 路径 | `.exec` → 跨运行合并 → `jacococli report` → `.xml` → 解析 `<line>` 标签 | `target_filters.VCF: htsjdk/variant/vcf` |
| **biopython** | coverage.py | `PythonCoverageContext` 包裹 Phase C 执行；`source=` 指向 site-packages 包目录 | `.coverage` SQLite → `analysis2()` → missing lines | `target_filters.SAM: Bio/Align/sam` |
| **pysam** | coverage.py (容器内) | `--coverage /cov` 标志 → coverage 先于 pysam 导入启动 | `summary.*.json` → 宿主直接读取（仅 .py 文件；Cython .so 不可见） | `target_filters.VCF: libcbcf, libcvcf, bcftools.py` |
| **seqan3** | gcovr/gcov | 编译时 `--coverage` 标志 → `.gcda` 自动累积 | `gcovr --json` → 解析 JSON | `target_filters.SAM: seqan3/io/sam_file` |
| **vcfpy** | coverage.py | `PythonCoverageContext` 包裹 Phase C 执行；`source=vcfpy.reader` 让解析器走到 `vcfpy` 包目录 | 与 biopython 相同的 `.coverage` → `analysis2()` | `target_filters.VCF: vcfpy/reader, parser, header, record, writer`（排除 bgzf/tabix —— BioTest 不走这些路径） |
| **noodles** | cargo-llvm-cov | `RUSTFLAGS="-C instrument-coverage"` + `LLVM_PROFILE_FILE=<dir>/*.profraw` | `cargo llvm-cov report --json --package noodles-vcf` → `NoodlesCoverageCollector` 读取 | `target_filters.VCF: noodles-vcf/src/io/reader, io/writer, header, record, variant, lib.rs`（排除 async —— BioTest 的 harness 是同步的） |

**行号区间聚合算法 (`_aggregate_ranges`)**：将零散未覆盖行 `[10, 11, 12, 13, 50, 52]` 压缩为 `["10-13", "50", "52"]`，防止 LLM 令牌溢出。参见 `coverage_collector.py:36-60`。

**格式感知白名单过滤**：`MultiCoverageCollector.collect_all(format_context="VCF")` 从 `target_filters` 查找当前格式对应的路径白名单，只统计匹配文件的覆盖数据。

##### 3.3 盲区攻坚工单与源码切片 (Blindspot Ticket with Source Code Slices)

**文件**：`test_engine/feedback/blindspot_builder.py` (379 行)

这是破解"覆盖率平原"的核心武器。大总管交叉对比 SCC 盲区与代码覆盖热图，构造高密度的**《盲区攻坚工单》**注入下一轮 Phase B 的 System Prompt。

工单包含三大必备段落：

**段落 1 — 未覆盖规范规则 (Uncovered Spec Rules)**：SCC 盲区中优先级最高的 10 条规则，从 ChromaDB 提取完整规范原文。

**段落 2 — 未覆盖源码切片 (Uncovered Code Slices)**：**不是行号，而是实际代码。** 系统从主目标 SUT 的源码树中自动提取未覆盖行范围对应的代码逻辑（含 ±2 行上下文），让 LLM 直接看到 `if/else` 分支：

```
UNCOVERED CODE in the primary target parser:
  VCFCodec.java:43-57
  ```
      43 |     public boolean canDecodeURI(final IOPath ioPath) {
      44 |         ValidationUtils.nonNull(ioPath, "ioPath");
      45 |         return extensionMap.stream().anyMatch(ext-> ioPath.hasExtension(ext));
      46 |     }
      48 |     @Override
      49 |     public int getSignatureLength() {
  ```
```

**令牌预算控制**：`MAX_SLICE_LINES=15` 每区域、`MAX_TOTAL_SLICE_LINES=80` 全局上限，防止 Prompt 膨胀。参见 `blindspot_builder.py:30-33`。

**段落 3 — 历史 MR 规避 (Previous MR Avoidance)**：列出已存在的 `mr_id` 列表，明确告诉 LLM "这条路已经走过了，请探索更边缘的突变"。

##### 3.4 Phase B 注入点 (Blindspot Context Injection)

盲区工单通过以下调用链注入 Phase B：

```
run_phase_d() → run_phase_b(blindspot_context=ticket)
  → mine_mrs(blindspot_context=ticket)
    → create_mr_agent(blindspot_context=ticket)
      → build_system_prompt(blindspot_context=ticket)
        → prompt += "\n\n" + blindspot_context
```

修改点极小（每个函数增加一个可选参数），不破坏 Phase B 的独立运行能力。

#### 📉 第四层：MR 注册表动态降级与隔离 (Dynamic MR Quarantine)

**文件**：`test_engine/feedback/quarantine_manager.py`

共识投票重构后，降级逻辑升级为 **交叉验证"良民证"规则**：先看有没有任何一个解析器（htsjdk / pysam / biopython / seqan3 / htslib / reference）在任意 seed 上通过了这个 MR 的 metamorphic 检查。只要有一家投过 `passed=True`，这条 MR 就有"良民证"——**不隔离**，继续贡献 SCC。

> 逻辑理由：合法的 metamorphic relation 是"至少有一个合规实现能遵守"的规则。主 SUT 的单独失败只证明它自己有 bug，不证明 MR 错了。辅助 SUT 的 bug 更不能拖 MR 下水。

**只有在"零良民证"的前提下**才应用以下降级阈值：
1. `failure_cause == "mr_invalid"` 事件 ≥ 3 次：htslib 说 T(x) 不合法，或共识 (x) ≠ 共识 (T(x)) → 降级。
2. 主 SUT `against_consensus` 率 > `crash_threshold`（默认 0.5）：主 SUT 在这条 MR 上系统性跑偏。
3. 主 SUT `crash_rate` > `crash_threshold`：解析器爆炸，说明输出格式坏了。

SCC 计算同步采用"良民证"规则：`biotest.py` 在组装 `primary_failed_mr_ids` 时，会先扫描所有 parser 的 `passed=True` 事件，把被背书的 MR 从"盲区"名单里排除，避免一条优质 MR 因主 SUT 单点故障就被迫进入 blind spot。

**磁盘原子操作**：`apply_quarantine()` 直接修改 `mr_registry.json`，将降级 MR 从 `enforced[]` 移入 `quarantine[]`，更新 `summary` 计数。

#### 🎯 第五层：盲区工单优先队列 + 冷却机制 (Top-K Prioritized Queue + Cooldown)

**文件**：`test_engine/feedback/blindspot_builder.py` + `test_engine/feedback/rule_attempts.py`

每轮 Phase D 面对 300+ 条未覆盖规则，把它们全塞给 LLM 会导致 qwen3 / Llama 3.3 70B 幻觉、输出空白或违反 Pydantic 验证。解决方法：**少食多餐**（prioritized queueing），每次只挑 Top K 条（`max_rules_per_iteration`，默认 5），其余排队等下一轮。

**排序五维键**（ascending，第一个有差异的维度胜出）：
1. **格式过滤**（`format_penalty`）：off-format 规则强制靠后（VCF 跑不可能选 SAM 规则）。
2. **失败次数**（`failure_count`）：屡败屡战的规则沉底，让新规则先上。
3. **-复杂度**（`-complexity`）：复杂度高的规则优先。复杂度 = 文本长度 + 关键词密度（`MUST/SHALL/when/BCF/dictionary/…`）+ 枚举/表格标记 + 跨节引用数。
4. **-邻近度**（`-proximity`）：规则 token 与当前主 SUT 未覆盖源码 token 的 Jaccard 相似度。相似度高 → 这条规则可能就藏在那段没覆盖的 `if/else` 里。
5. **严重度**（`severity_rank`）：CRITICAL < ADVISORY < MAY。

**Top-K 窗口 + 冷却过滤**：
- 每轮组装 ticket 时，从排序后的队列里依次取。若某条规则当前处于 `cooled_until_iteration ≥ current_iter` 状态，**跳过**，`cooling_count` 加 1。队列账本：`total_uncovered = shown + remaining`，`remaining` 包含正在冷却的规则——它们没被删除，只是延期。
- Ticket 被送给 LLM 之前，`tracker.record_attempt(iter, top_k_chunk_ids)` 记录本轮"秀过场"的规则。
- Phase D 本轮跑完 B → C、算完 SCC 之后，`tracker.record_outcome(iter, newly_covered_chunk_ids)` 打分：
  - 在 `newly_covered` 里 → **清零**（covered）。
  - 不在 → `failure_count += 1`，`cooled_until_iteration = iter + cooldown_duration(failure_count)`。
- **冷却时长（指数退避，有上限）**：1 次失败 → 跳 1 轮，2 次 → 跳 2 轮，3 次 → 跳 4 轮，4+ 次 → 跳 4 轮（`MAX_COOLDOWN_ITERATIONS = 4`）。
- 持久化：`data/rule_attempts.json`。Phase D 重启时加载，跨会话保留冷却状态。

**示例**：队列 312 条，iter 1 挑 Top 5 塞给 LLM → 没一条被覆盖 → iter 2 这 5 条进入冷却 → 系统自动往下挑 "第 6–10 名"。避免"死磕最难的 5 条"。

**运行日志格式**：
```
Total Blindspots: 312 | Injecting Top 5 into this ticket | 307 rules remaining in queue (2 cooling down).
```

**System prompt 明确指示 LLM**：
```
FOCUS EXCLUSIVELY on the rules below. Do NOT attempt to cover the entire spec in one go.
Quality of MRs for these specific rules is the priority. Deferred rules will resurface in
the next iteration's ticket.
```

#### 🧭 第六层：运行时感知菜单过滤器 (Runtime-Gated Transform Menu)

**文件**：`mr_engine/agent/transforms_menu.py` + `biotest.py::_compute_runtime_capabilities()`

写入型 MR（基于 `sut_write_roundtrip`）只有在"至少有一个已启用 SUT 的 `ParserRunner` 声明 `supports_write_roundtrip = True`"的时候才值得让 LLM 考虑。否则 LLM 选了也白选：dispatch 找不到 writer-capable runner，transform gracefully no-op，浪费一个 MR slot。

于是 Phase D 在进入 Phase B 之前先做一次 runtime capability 计算：

```python
# biotest.py — Phase D 每轮 Phase B 之前
runtime_capabilities = _compute_runtime_capabilities(enabled_suts, primary_target)
# -> {"primary_sut_has_writer", "has_bcf_codec", ...}
```

然后 `transforms_menu.get_transform_menu(runtime_capabilities=...)` 在渲染 LLM 菜单时会：
1. **隐藏**任何前置条件属于 `KNOWN_RUNTIME_PRECONDITIONS` 且当前 runtime 不满足的 transform（避免 LLM 挑错）；
2. 在渲染末尾加一段 "Note: the following transforms were hidden because the current runtime lacks X"，提示 LLM 隐藏项的存在，防止它误以为菜单就是全部；
3. `Valid names:` 行也只列出可用名字，LLM 结构化输出里如果混入隐藏名字会被 Pydantic 直接拒收。

**配合 transform 的 preconditions**：`sut_write_roundtrip` 在注册时写了 `preconditions=("primary_sut_has_writer",)`。由 `KNOWN_RUNTIME_PRECONDITIONS` 把这个 token 映射到 "主 SUT 的 ParserRunner 实例 `supports_write_roundtrip=True`" 这个 runtime 检查上。未来新增"runtime-gated transform"只需扩展这张映射表，prompt 层零改动。

**效果**：用户在配置里启用纯解析 SUT（例如没有写功能的 `ReferenceRunner`）时，`sut_write_roundtrip` 自动从 LLM 菜单消失；用户把 `supports_write_roundtrip=True` 的 runner（htsjdk / pysam / 新加的 writer）启用后，菜单自动复活。整个框架对"新 SUT 支持 writer"这一事件的反应是零配置的。

#### 🌱 第七层：LLM 驱动的种子合成并行于 MR 挖掘 (Rank 1 — Seed Synthesis Parallel to MR Mining)

**文件**：`mr_engine/agent/seed_synthesizer.py` + `mr_engine/agent/seed_synth_prompts.py`

MR-only 测试在文件格式解析器上的**天花板**约为 25–40% 行覆盖率（Ba 2025, arXiv:2508.16307；Chen & Kuo 2018）——因为 MR 必须保持输入合法性，所以永远不会触发拒绝分支、二进制编解码、罕见 INFO 类型等代码路径。Rank 1 杠杆从另一方向攻击：让 LLM 基于"未覆盖代码切片"直接**合成新种子**，而不是合成新 MR。

每个 Phase D 迭代（从第 2 轮起）**同时**做两件事（user: 所谓"parallel"指"并行发生，都在做"，实现上顺序执行以避开 ChromaDB 并发 + seeds/ 目录 race）：
1. **种子合成**（新）：用 `blindspot_text` 中已含的 "UNCOVERED CODE" 切片调用 `llm.invoke([HumanMessage(prompt)])`（零 ReAct，对称于 `engine.py:717::_synthesize_from_recursion_failure`），要求输出 N 份 triple-fenced VCF/SAM 文件。
2. **MR 挖掘**（已有）：同一个 ticket 送给 ReAct agent，返回新的 MRs。

**验证管线（严格把关）**：每个候选种子依次通过：
- Header 检查（VCF 必须以 `##fileformat=VCF` 开头，SAM 以 `@HD`/`@SQ` 开头）；
- 大小 ≤ 500 KB（与 `fetch_real_world.py` 同一上限）；
- **结构解析**走框架自己的 `normalize_vcf_text` / `normalize_sam_text`——Phase C 所有真实种子用的是同一个 gate，保证不会放进解析不了的垃圾；
- SHA-256 内容哈希去重（跨迭代、跨轮次）；
- **原子写**：`seeds/vcf/synthetic_iter{N}_{hash8}.vcf.tmp → os.replace`，防止 SeedCorpus 中途 glob 到半写入文件。

成功的种子落在 `seeds/{vcf,sam}/synthetic_iter{N}_{hash8}.{vcf,sam}`，统一 `.gitignore`。下一轮 Phase C 重新实例化 `SeedCorpus`（已有行为），自动发现。

**配置**：
```yaml
feedback_control:
  seed_synthesis:
    enabled: true
    max_seeds_per_iteration: 5
    max_file_bytes: 524288
```

**预期增益**：+8–15 pp（SeedMind arXiv:2411.18143；SeedAIchemy arXiv:2511.12448；TitanFuzz ISSTA'23；Fuzz4All ICSE'24——这类 LLM 驱动种子合成在 DL 库 fuzzing 中普遍带来 30–50% 的覆盖率提升，我们的上限保守）。

**失败处理**：整条 synth 路径在 `run_phase_d` 里被 `try/except` 包住，任何异常只 log warning 不中断当轮 B/C。`enabled: false` 可一键关停。

#### 🧭 第八层：hypothesis.target() 覆盖导向 (Rank 4 — Coverage-Seeking Directive)

**文件**：`test_engine/orchestrator.py::_run_mr_with_hypothesis`

Hypothesis 内建的 `Phase.target` 会放大 `target()` 声明的标量目标值较高的测试样本（类似 libFuzzer 的轻量替代，无需 C 级插桩）。我们利用这一点，给 `@given` 闭包内的每次例子后加两个 `target()` 标签：

```python
# 每次 _run_single_test 调用前/后快照三个计数器
before_mv, before_dv, before_cr = result.metamorphic_failures, ...
try:
    _run_single_test(...)
finally:
    divergence = (
        (result.metamorphic_failures - before_mv)
        + (result.differential_failures - before_dv)
        + (result.crashes - before_cr)
    )
    target(float(divergence), label="divergence")   # 共识分歧数
    target(float(len(lines)), label="seed_size")    # 种子行数
```

**原理**：`target()` 只需目标值的**单调性**，不需要精确覆盖率。`divergence` 奖励那些触发 SUT 间不一致的种子（高信号输入），`seed_size` 给出一个连续的推力避免退化到同一种子。`Phase.target` 会据此优先生成让这两个标签增长的样本，等价于"覆盖率导向的 Hypothesis"。

**为何不用 HypoFuzz**：HypoFuzz 需要 pytest 级 `@given` 发现，而我们的 `@given` 是 orchestrator 内部闭包；包 HypoFuzz 要做一个 23 条 pytest 入口的 shim，运维成本高。`target()` 内联方案约 20 行代码，零新文件、零新依赖，收益 +2–5 pp，性价比压倒性。

**安全网**：`target()` 本身抛异常时被内部 `try/except` 吞掉，绝不会掩盖真正的 `_OracleFailure`——用 `test_orchestrator_target.py::test_target_exception_does_not_mask_oracle_failure` 守住。

> **References**:
> - MacIver, D. R. & Hatfield-Dodds, Z. *Hypothesis: A Property-Based Testing
>   Framework for Python* — `hypothesis.readthedocs.io`. The `target()`
>   directive + `Phase.target` are documented at
>   `hypothesis.works/articles/coverage-guided-property-based-testing/`.
> - For the planned upgrade to true branch-coverage feedback see HypoFuzz
>   (Hatfield-Dodds, 2024-2026, `hypofuzz.com`) — Rank 7 in the coverage
>   plan; it plugs branch-coverage feedback directly into Hypothesis
>   strategy choices, going beyond `target()`'s scalar-objective search.

### 4. 框架终止条件 (Termination Conditions)

**文件**：`test_engine/feedback/loop_controller.py`

大总管在每轮迭代后强制检查以下 **5 个熔断条件**（按优先级排序）：

| 优先级 | 条件 | 触发逻辑 | 默认阈值 |
| :--- | :--- | :--- | :--- |
| 1 | **超时熔断** | 总耗时 >= `timeout_minutes` | 120 分钟 |
| 2 | **目标达成** | SCC >= `target_scc_percent` | 95% |
| 3 | **预算耗尽** | 迭代次数 >= `max_iterations` | 5 轮 |
| 4 | **灾难性熔断** | 单轮降级率 > 50%（新 Enforced MR 过半被隔离） | 50% |
| 5 | **覆盖率平原** | SCC 连续 `plateau_patience` 轮变化 < 0.5% | 2 轮 |

**状态持久化**：`IterationState` 序列化到 `data/feedback_state.json`，支持崩溃恢复（`controller.load_state()`）。

### 5. 大总管主循环 (Phase D Outer Loop)

**文件**：`biotest.py:run_phase_d()` (约 150 行)

```
for iteration in range(controller.state.iteration, max_iterations):
    if controller.check_termination().should_stop: break
    
    # Phase B: 挖掘 MR (注入盲区工单)
    run_phase_b(cfg, blindspot_context=ticket)
    
    # Phase C: 执行测试 (Python 覆盖率插桩包裹)
    with PythonCoverageContext(...):
        run_phase_c(cfg)
    
    # 采集覆盖率 (格式感知过滤)
    coverage_results = collector.collect_all(format_context=format_filter)
    
    # 计算 SCC (主目标感知 + 格式感知)
    scc = tracker.compute_scc(enforced, primary_failed_mr_ids, format_context)
    
    # 第四层: 自动隔离崩溃 MR
    apply_quarantine(decisions, registry_path)
    
    # 第三层: 构建盲区工单 (含源码切片)
    ticket = build_blindspot_ticket(scc, coverage, ...,
        primary_target=primary_target, source_roots=source_roots)
```

### 6. LLM 多路由 + 速率限制退避 (Multi-provider LLM + Rate-Limit Backoff)

**文件**：`mr_engine/llm_factory.py` + `mr_engine/agent/engine.py`

**默认模型从 `ollama/qwen3-coder:30b` 切到 `llama-3.3-70b-versatile`（Groq 免费层）**。原因：本地 30B 在扩展盲区工单 + 五维排序 prompt 下频繁触发 `GraphRecursionError`（ReAct 陷入工具调用死循环）和 Pydantic 验证失败（输出 JSON 带非法换行）。Groq 的 Llama 70B 容错显著更好。

`llm_factory.py` 支持的 provider（按前缀路由）：

| `LLM_MODEL` 示例            | Provider  | API Key 环境变量      |
| :-------------------------- | :-------- | :-------------------- |
| `llama-3.3-70b-versatile`   | Groq      | `GROQ_API_KEY`        |
| `gpt-4o` / `o3-mini`        | OpenAI    | `OPENAI_API_KEY`      |
| `claude-3-5-sonnet-...`     | Anthropic | `ANTHROPIC_API_KEY`   |
| `gemini-1.5-pro`            | Google    | `GOOGLE_API_KEY`      |
| `ollama/qwen3-coder:30b`    | Ollama    | (local, 无需 key)     |
| `vllm/<name>`               | vLLM      | (optional)            |

**速率限制退避（`_invoke_with_rate_limit`）**：Groq 免费层有日配额，命中 429 时：
1. 优先解析 provider 返回的 Retry-After / "try again in 37.23s" / "1m30s" / `retry_after` JSON 字段，按提示休眠 + 0.5~2 秒抖动。
2. 若无提示则指数退避：30s → 60s → 120s → 240s（上限 10 分钟），最多重试 4 次。
3. 识别模式：字符串包含 `429 | 503 | rate limit | quota | too many requests | try again in | capacity`，或异常对象的 `status_code ∈ {429, 503}`。
4. 重试耗尽后，此轮 theme 标记为 `Rate limit budget exhausted` 但**不中断整个 Phase B**，下一个 theme 继续。

### 7. Rich 终端仪表盘 (Rich Terminal Dashboard)

`biotest.py` 的 Executive Summary 新增 Phase D 面板：

*   **SCC 进度条**：`0.9% → 0.4% → ...`（逐轮追踪）
*   **终止原因面板**：显示具体的停止条件（如 `plateau`、`budget_exhausted`）
*   **Phase D 行**：在 Phase Results 表中增加迭代数、最终 SCC、降级数

```
py -3.12 biotest.py --phase D          # 运行反馈闭环
py -3.12 biotest.py --phase A,B,C,D    # 全流水线 + 反馈
py -3.12 biotest.py --dry-run           # 校验配置
```

### 8. 📁 项目代码结构与产出 (Project Structure & Files)

**Phase D 产出: 10 个新文件 (2,165 行) + 10 个修改文件 + pysam Docker 镜像。**

```text
BioTest/
├── biotest.py                         # 👑 大总管 (960 行, Rich UI, A→B→C→D)
├── biotest_config.yaml                # 全局配置 (198 行, 含 feedback/coverage/ci)
├── harnesses/pysam/                   # D1: pysam Docker Harness
│   ├── pysam_harness.py               # 独立 CLI (支持 --coverage)
│   ├── Dockerfile                     # python:3.12-slim + pysam + coverage
│   └── build_docker.py                # 构建 + 冒烟测试
├── coverage_artifacts/                # D2: 覆盖率数据 (gitignored)
│   ├── jacoco/jacocoagent.jar         # JaCoCo 运行时 Agent
│   ├── jacoco/jacococli.jar           # JaCoCo CLI (exec→xml 转换)
│   └── pysam/source/                  # Docker 提取的 pysam 源码
└── test_engine/
    ├── feedback/                      # D3: 反馈闭环核心 (6 个新文件)
    │   ├── __init__.py
    │   ├── scc_tracker.py             # 语义约束覆盖率 (SCC) 计算
    │   ├── loop_controller.py         # 5 个终止条件 + 状态持久化
    │   ├── quarantine_manager.py      # 动态 MR 降级隔离
    │   ├── coverage_collector.py      # 多语言覆盖率采集 (817 行)
    │   │   ├── _aggregate_ranges()    # 行号区间聚合算法
    │   │   ├── JaCoCoCollector        # Java: XML <line> 解析 + exec→xml 转换
    │   │   ├── CoveragePyCollector    # Python: coverage.py API + XML 回退
    │   │   ├── PysamDockerCoverageCollector  # Docker: summary.json 读取
    │   │   ├── GcovrCollector         # C++: gcovr JSON 解析
    │   │   ├── PythonCoverageContext  # Phase C 执行包裹器
    │   │   └── MultiCoverageCollector # 聚合器 (格式感知白名单)
    │   └── blindspot_builder.py       # 盲区工单 + 源码切片提取 (379 行)
    │       ├── CodeSlice              # 源码切片数据类
    │       ├── extract_code_slices()  # 从 SUT 源码树提取实际代码
    │       └── build_blindspot_ticket # 三段式工单构建器
    └── runners/
        ├── pysam_docker_runner.py     # Docker 子进程 Runner (含覆盖率挂载)
        └── pysam_runner.py            # Facade: Native → Docker 透明降级
```

### 9. 🏆 首次 E2E 实战运行记录 (Live End-to-End Run)

**运行命令**：`py -3.12 biotest.py --phase D --config biotest_config.yaml --verbose`

**环境配置**：
*   LLM: `ollama/qwen3-coder:30b` (18GB 本地模型, Ollama 0.20.7)
*   Docker: Docker Desktop 29.1.2 (运行 pysam 容器)
*   活跃 SUT: htsjdk (Java), biopython (Python), seqan3 (C++), **pysam (Docker)**, reference

**活跃解析器矩阵**：

| 解析器 | 语言 | VCF | SAM | 执行方式 |
| :--- | :--- | :---: | :---: | :--- |
| **htsjdk** | Java | Y | Y | Subprocess (fat JAR + JaCoCo agent) |
| **pysam** | Python | Y | Y | Docker 容器 (`biotest-pysam:latest`)（仅投票，不做 coverage primary） |
| **biopython** | Python | -- | Y | In-process (Bio.Align.sam) |
| **seqan3** | C++ | -- | Y | Subprocess (编译二进制) |
| **vcfpy** | Python | Y | -- | In-process (vcfpy.Reader) |
| **noodles** | Rust | Y | -- | Subprocess (`noodles_harness` Cargo 二进制 + cargo-llvm-cov) |
| **reference** | Python | Y | Y | 内建归一化器 (始终可用) |

**迭代记录**：

| 迭代 | Phase B | Phase C | 变体违规 | 差分违规 | Bug 报告 | SCC | 降级 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 3 MR 编译, 2 强制 | 24 测试, DET=45.8% | 5 | 6 | 5 | 0.9% | 0 |
| 2 | 2 MR 编译, 1 强制 | 12 测试, DET=41.7% | 2 | 3 | 2 | 0.4% | 0 |
| 3+ | 进行中... | 进行中... | -- | -- | -- | -- | -- |

**关键发现**：pysam 新 SUT 在首轮即暴露出**元变异违规 (Metamorphic Violation)** —— 对 VCF 元信息行重排后产生不同的 canonical JSON 输出，违背了 VCF 规范"元信息行可以任意排序"的约束。

### 10. ✅ 测试状态 (Test Status)

**292/292 测试通过**（+ 2 个受环境限制 skip，如 Docker 不可用时）。

Phase D 新增的所有模块均通过了实际数据的冒烟验证：
*   SCC 计算: 453 规则, VCF 316 / SAM 137 (精确分区)
*   行号聚合: `[10,11,12,13,50,52]` → `["10-13","50","52"]`
*   终止控制器: 5 条件全覆盖 (timeout/target/budget/catastrophic/plateau)
*   盲区工单: 包含实际源码切片 (htsjdk VCFCodec.java, biopython sam.py)
*   pysam Docker: 3 个 VCF 种子全通过, 覆盖率 166/616 (26.9%)
*   JaCoCo 累积: 3 次运行合并 13KB exec 数据

### 11. 🧭 SUT 写入协议扩展指南 (Onboarding a Writer-Capable SUT)

新增一个可以做 parse + write round-trip 的 SUT 时，**不需要修改** transform library、dispatch、strategy router、orchestrator 里的任何一行代码。只需做两件事：

1. **Runner 端**：在 SUT 对应的 `ParserRunner` 子类里实现 `run_write_roundtrip(input_path, format_type="VCF") -> RunnerResult`，并把类属性 `supports_write_roundtrip` 置为 `True`。方法内部按 `format_type.upper()` 分流到 SUT 的 VCF / SAM 写入 API；不支持的格式返回 `error_type="ineligible"` 即可。
2. **Harness 端（若 SUT 是 subprocess / Docker）**：在原有 harness 的 CLI 里加一个 `--mode write_roundtrip <FORMAT> <file_path>` 参数，在容器 / JVM 里做 parse + serialize，把序列化后的文件文本打印到 stdout。Runner 端 subprocess 包装器读取 stdout，塞进 `RunnerResult.canonical_json["rewritten_text"]` 返回。

**参考实现**：

| SUT     | Runner 文件                                      | Harness 文件                               | 写入 API                                                       |
| :------ | :----------------------------------------------- | :----------------------------------------- | :------------------------------------------------------------- |
| htsjdk  | `test_engine/runners/htsjdk_runner.py`           | `harnesses/java/BioTestHarness.java`       | `VCFWriter` + `SAMFileWriterFactory`                           |
| pysam   | `test_engine/runners/pysam_runner.py`            | `harnesses/pysam/pysam_harness.py`         | `pysam.VariantFile("w")` + `pysam.AlignmentFile("wh")`         |
| htslib  | `test_engine/runners/htslib_runner.py`           | (CLI 本身就是 round-trip)                  | `bcftools view -O v` / `samtools view -h`                      |

**菜单自动生效**：Phase D 每轮在进入 Phase B 之前通过 `_compute_runtime_capabilities` 扫描所有启用 SUT，凡是有任何 runner 的 `supports_write_roundtrip=True`，就会在 runtime capabilities 集合里注入 `primary_sut_has_writer`，从而让 `sut_write_roundtrip` transform 出现在 LLM 的菜单里。无写入能力时自动隐藏，LLM 永远不会白选。

### 12. 🧭 SUT 覆盖率作用域写法 (Per-SUT Coverage Filter — REQUIRED for a new SUT)

onboard 一个新 SUT 时，harness + runner **不是**全部的契约。用户还必须明确写一段 `coverage.target_filters.<FMT>.<sut_name>` YAML，告诉框架这个 SUT 的"VCF 代码"或"SAM 代码"具体是哪些包/文件。否则：

- 不写 → 该 SUT 的 coverage collector 收不到任何过滤器 → 要么 0% 覆盖率（路径不匹配），要么 denominator 里混进整个库（htsjdk 的 CRAM/BAM/legacy/JEXL 都会被计入）。
- **两种情况都会让 coverage 数字失真，进而污染 Phase D 的 blindspot ticket 和 SCC 计算。**

**YAML 结构（2026-04-18 起的 nested 写法）**：

```yaml
coverage:
  target_filters:
    VCF:
      htsjdk:
        - htsjdk/variant/vcf
        - htsjdk/variant/variantcontext::-JEXL,-Jexl,-*JEXL*,-*Jexl*
        - htsjdk/variant/variantcontext/writer::VCF,Variant
      pysam:
        - pysam
    SAM:
      htsjdk:
        - htsjdk/samtools::SAM,Sam
      biopython:
        - Bio/Align/sam
      seqan3:
        - seqan3/io/sam_file
        - format_sam
        - cigar
      pysam:
        - pysam
```

**Pattern 语法**（每条 entry）：

| 写法                       | 语义                                                     |
| :------------------------- | :-------------------------------------------------------- |
| `pkg/path`                 | 整个包/目录，所有源文件都纳入                              |
| `pkg/path::VCF,Variant`    | 包 + 白名单前缀：只纳入以 `VCF` 或 `Variant` 开头的文件    |
| `pkg/path::-JEXL,-Jexl`    | 包 + 黑名单前缀：纳入除这些前缀外的所有文件                |
| `pkg/path::*SV*,-BCF2*`    | 通配符：`*Foo*` = 包含 `Foo` 的；`-BCF2*` = 排除以 `BCF2` 开头 |

**向后兼容**：旧版扁平结构 `target_filters.VCF: [list]` 仍然识别，整条列表会扇出给所有 SUT（这就是为什么 htsjdk 包名在 pysam collector 里自然不匹配）。但新 SUT 必须用 nested 写法——只有这样才能精确圈住它自己的代码。

**`coverage_collector.py::MultiCoverageCollector._resolve_sut_filter`** 是分发点：给 `(fmt, sut_name)` 返回对应的 pattern 列表；如果 fmt 下没有该 sut 的条目，就返回 `None`（collector 走它自己的 default scope）。

**落在哪些 collector**：
- **Java / JaCoCo** (`JaCoCoCollector`)：把 pattern 当成 Java 包名，匹配 `<package name="…">` + 文件名前缀/通配符。
- **Python / coverage.py** (`CoveragePyCollector`)：把 pattern 当成 dotted 包名或目录 substring，匹配已安装包的文件路径。
- **C++ / gcovr** (`GcovrCollector`)：把 pattern 当成源路径 substring，匹配 gcovr JSON 里的 `file` 字段。

每个 collector 看到自己语言匹配不上的 entry 就静默跳过，所以同一个 fmt 下可以混放多语言 pattern 而互不干扰。

**onboarding checklist**（新 SUT 必做三件套，不是两件）：
1. 写 harness（`harnesses/<lang>/<sut>_harness.*`）
2. 写 runner 子类（`test_engine/runners/<sut>_runner.py`）
3. **写 coverage 作用域** (`biotest_config.yaml::coverage.target_filters.<FMT>.<sut>`)

缺了第 3 条，Phase D 的 feedback signal 就是垃圾数据。

---

# SAM Coverage Plan (Phases 1–6, 2026-04-19)

A SUT-agnostic lever stack designed specifically to close the SAM-side
coverage gap measured on biopython/SAM Run 1 (44.0 % on
`Bio/Align/sam.py`). All 6 phases ship behind the existing 3-piece
onboarding contract — no new per-SUT code, no new harness obligations.

Per-phase expected lift, phased by ROI + complexity:

| Phase | Lever                                                    | Expected lift | Files                                                                                                     |
|:-----:|:---------------------------------------------------------|:-------------:|:----------------------------------------------------------------------------------------------------------|
| 1     | Tier-2 SAM corpus expansion (+30 htslib files, +3 BAM)   | +3–6 pp       | `seeds/fetch_real_world.py`, `seeds/SOURCES.md`, `tests/test_seed_fetch.py`                               |
| 2     | 5 header-subtag shuffles + 3 malformed mutators          | +4–8 pp       | `mr_engine/transforms/sam.py`, `mr_engine/transforms/malformed.py`, `mr_engine/behavior.py`, `sam_normalizer.py` (dict-sort), dispatch + strategies |
| 3     | SAM↔BAM / SAM↔CRAM round-trip via samtools CLI           | +2–4 pp       | `mr_engine/transforms/sam.py` (`sam_bam_round_trip`, `sam_cram_round_trip`), `seeds/ref/toy.fa`, dispatch + strategies |
| 4     | Rule-reachability filter + query-methods precondition    | +1–3 pp       | `test_engine/feedback/blindspot_builder.py`, `phase_a.rule_capability_tags`, `transforms_menu.py`, `biotest.py::_compute_runtime_capabilities` |
| 5     | SeedMind-style LLM-generator synthesis (sandboxed)       | +5–10 pp      | `mr_engine/agent/seed_synthesizer.py::synthesize_seeds_via_generator`, `seed_synth_prompts.py::build_generator_prompt` |
| 6     | Cross-parser Tier-2 corpus minimization (union-edge)     | 0 (wall-time) | `seeds/minimize_corpus.py`                                                                                |

**Cumulative expected ceiling on biopython/SAM**: 55–62 %, bounded by the
published ~60 % automated-MR limit (Liyanage & Böhme ICSE'23).

### Key design invariants

- **Tier-1 preservation**: `seeds/minimize_corpus.py` hard-codes
  `MINIMIZE_SCOPE = {"real_world_", "synthetic_"}`. Hand-curated
  `minimal_*`, `spec_example*`, `complex_*` seeds are walked for edge
  contribution but NEVER moved. Operator-chosen debugging anchors.
- **Runtime-gated transforms**: `sam_bam_round_trip` and
  `sam_cram_round_trip` declare `samtools_available` /
  `cram_reference_available` preconditions. The Phase B prompt filter
  hides them when the tag is unset, so deployments without `samtools`
  don't waste LLM calls mining dead transforms. Analogue of how
  `sut_write_roundtrip` is gated by `primary_sut_has_writer`.
- **CRAM lossiness policy**: the toy reference in `seeds/ref/toy.fa`
  contains only ~2.4 KB of random bases for 7 canonical `@SQ` names.
  Seeds with non-covered `@SQ` names cause `sam_cram_round_trip` to
  no-op; the strategy router's `assume()` filters those out before they
  reach Phase C.
- **SeedMind sandbox**: `_run_generator_sandboxed` uses `python -I`
  (isolated) + `subprocess.run(timeout=5s)` + 500 KB output cap + AST
  whitelist restricting imports to `{random, string, itertools, struct,
  math, textwrap, __future__}`. No LLM-authored code can reach the
  network or touch the filesystem outside its own stdout.
- **Canonical normalizer change** (Phase 2): `_parse_tag_fields` now
  `dict(sorted(items()))` so header-subtag permutations produce
  byte-identical canonical JSON. All 5 shuffle_*_subtag MRs rely on
  this — regression tested in
  `tests/test_transforms.py::TestSubtagShuffleCanonicalInvariance`.
- **Reachability penalty** (Phase 4): adds a sixth priority dimension
  (+20) below the format penalty (+10) so an on-format unreachable rule
  still sinks below an on-format reachable rule but ranks above every
  off-format rule. Operator-editable via
  `phase_a.rule_capability_tags` in config; runner classes declare
  `supports_<cap>=True` per class attribute (default False).

### Runtime capability matrix after Phase 4

New `KNOWN_RUNTIME_PRECONDITIONS` entries (gate the Phase B LLM menu):

| Tag                                | Computed from                                              |
|:-----------------------------------|:----------------------------------------------------------|
| `primary_sut_has_query_methods`    | Primary runner class `supports_query_methods=True`        |
| `samtools_available`               | `shutil.which("samtools")` resolves                        |
| `cram_reference_available`         | `seeds/ref/toy.fa` exists on disk                         |

Gaps filled during Phase 4: the pre-existing
`query_method_roundtrip` transform declared its precondition as
`primary_sut_supports_query_methods`, which was NOT in
`KNOWN_RUNTIME_PRECONDITIONS` and thus treated as an advisory
sample-level hint, not a hard gate. Renamed to
`primary_sut_has_query_methods` and added to the known set so the
menu-filter actually fires.

### Cross-SUT parity audit (to run after rollout)

After each phase lands:
1. Baseline the primary target (biopython) — `py -3.12 biotest.py`,
   record `data/coverage_report.json::final_coverage_pct`.
2. Flip `feedback_control.primary_target` to `htsjdk` / `pysam` /
   `seqan3` in turn and re-run Phase C only (`--phase C`).
3. Every SUT should show similar pp movement from this phase. If one
   SUT lags by >5 pp, the lever has a hidden per-SUT bias — investigate
   before shipping.

This is what "generalizable across all SAM SUTs" means operationally —
the coverage-notes writeup stays honest when every SUT benefits within
±3 pp.

---

# Plateau-breaker attempt (2026-04-19/20) — shipped, measured, reverted

Ranks 1-5 + Rank 7 plus the filter correction landed BioTest at a
**plateau near 47 % weighted VCF on htsjdk** (Run 6). An apples-to-
apples EvoSuite 1.2.0 baseline on the same 3-path filter came in at
**52.9 %**, dominated by a +24.8 pp bucket lead inside
`htsjdk/variant/variantcontext`. Diagnostic: five post-parse API
classes account for ~500 of the ~1 250 lines still missing on that
bucket, and the same shape of gap is expected on any parser SUT —
`parse(x) → canonical_JSON` flows never exercise
builder-chain / collection-mutation / type-resolution code paths.

The plateau-breaker shipped **three SUT-agnostic changes** that stayed
inside the zero-user-cost envelope. No new MR paradigm, no new oracle,
no per-SUT equivalence rules. **All three are measured below and all
three are now opt-in (off by default) because the measured gain was
inside LLM noise at disproportionate runtime cost.**

> **TL;DR for anyone skimming this section**: Run 6 at 46.9 % in 170 min
> is the current sweet spot on htsjdk/VCF. Turning on Rank 6 (MR
> synthesis) + Tier 2 (prompt enrichment) in Runs 7 and 8 bought at
> most +1.1 pp at ~2× wall time, a per-minute return roughly 40× worse
> than the baseline rate. The code is shipped and soundness-preserving;
> flip the flags per-run if you want to pay the cost. See
> `coverage_notes/htsjdk/vcf/biotest.md` §"Runs 7 & 8" for the data.

## Rank 6 — LLM-synthesized MRs, shipped as opt-in

`mr_engine/agent/mr_synthesizer.py` (flag:
`feedback_control.mr_synthesis.enabled`, **default `false`**):

- Consumes the same `BlindspotTicket.to_prompt_fragment()` text Rank 1
  seed synth uses.
- Asks the LLM for NEW MRs (not new files) composed strictly over the
  existing transform whitelist — the compiler rejects invented names.
- Routes output through the standard `compile_mr_output` pipeline, so
  every Pydantic validator (whitelist, compound groups, `query_methods`
  non-empty gate from Rank 5) still applies.
- Triage + merge into `data/mr_registry.json` at the start of each
  Phase D iteration, ahead of the ReAct Phase B mining loop.

Grounded in Fuzz4All (ICSE'24, arXiv:2308.04748), PromptFuzz (CCS'24,
arXiv:2312.17677), and ChatAFL (NDSS'24). **Originally projected +3–5 pp;
measured +0.7–1.1 pp at 1.5–2× wall time** on htsjdk/VCF (Runs 7 & 8).
Diminishing returns set in within 3 iterations. Leave disabled unless
you have a specific hypothesis to test.

## Tier 2a — per-class blindspot block (`ClassGap`), opt-in

Flag: `feedback_control.prompt_enrichment.per_class_blindspot`,
**default `false`**. `test_engine/feedback/blindspot_builder.py` adds
`ClassGap` + `compute_class_level_gaps(coverage_report_path, filter_rules_text)`.

- Input: whichever **standard coverage report** the primary SUT emitted
  this iteration:
  - JaCoCo XML (Java SUTs like htsjdk, and any future Java parser)
  - coverage.py JSON (`coverage json`) for Python SUTs (biopython,
    pysam native mode, reference)
  - gcovr JSON for C / C++ SUTs (seqan3, future libclang-adapted SUTs)
- Output: Top-N `ClassGap` entries (default 10), ranked by missed-line
  count, filtered through the same `target_filters.<FORMAT>.<sut>`
  rules the feedback loop uses for its weighted score. Names are the
  language-native identifier the runner's reflection would surface —
  Java FQN, Python module path, C++ header path.

`BlindspotTicket` carries them as `class_gaps: list[ClassGap]` and
`to_prompt_fragment()` renders a new `TOP UNCOVERED CLASSES / MODULES`
section. The block is **skipped** when the list is empty, so a runner
whose coverage report is unsupported / missing degrades gracefully
back to the existing rule-based blindspot.

Flowchart:

```
primary_target ─┐
format_context ─┼─► _resolve_primary_coverage_report(cfg, ...) ─► Path
target_filters ─┘                                                  │
                                                                    ▼
             compute_class_level_gaps(path, filter_rules_text) ──► list[ClassGap]
                                                                    │
                                                                    ▼
                                             BlindspotTicket.class_gaps
                                                                    │
                                                                    ▼
                         to_prompt_fragment()  →  blindspot_text  →  Rank 1 seed synth
                                                                    │
                                                                    └─► Rank 6 MR synth prompt
```

The dispatch in `biotest.py::_resolve_primary_coverage_report` is keyed
only on `primary_target` name + config keys the user already writes —
no SUT-specific class names or paths inside framework code.

## Tier 2b — mutator-method catalog (`supports_mutator_methods`), opt-in

Flag: `feedback_control.prompt_enrichment.mutator_catalog`,
**default `false`**. A sibling of the Rank 5 `supports_query_methods` opt-in:

```python
# test_engine/runners/base.py
supports_mutator_methods: bool = False
def discover_mutator_methods(self, format_type: str) -> list[dict]: ...
```

`test_engine/runners/introspection.py::get_mutator_methods` provides
the Python implementation (reflection filter on name prefix +
`None`/fluent-return types; Pydantic `model_fields` fast path). Each
Python runner opts in with a three-line `discover_mutator_methods`
method that calls `get_mutator_methods` on the right target class
(`ReferenceRunner` → `CanonicalVcfRecord` / `CanonicalSamRecord`,
`BiopythonRunner` → `Bio.Align.Alignment`, `PysamRunner` →
`pysam.VariantRecord` / `pysam.AlignedSegment`). Java / C / C++ / Rust
runners can follow the same pattern via their existing harnesses'
`--mode discover_*` CLI surface.

**Critical invariant** (stated explicitly so this stays soundness-
preserving): the mutator catalog is **prompt-only**. The framework
does NOT dispatch mutator chains as a new transform family. Instead,
`mr_engine/agent/mr_synth_prompts.py::_render_mutator_catalog_block`
surfaces the discovered names to the LLM so Rank 6 can reason about
which classes its MRs should target — but the generated MRs still go
through the allowed-transforms whitelist (typically
`sut_write_roundtrip` or `query_method_roundtrip`). Oracle soundness
is inherited from those transforms' existing compare logic.

Rejected alternative (Rank 8 standalone mutator-chain MR paradigm):
mutator chains aren't self-inverse in general, the LLM can't certify
semantic no-op from reflection alone, and the fix (per-class
equivalence rules) IS the per-SUT code the zero-user-cost constraint
forbids.

## Runtime reflection contract — language-level, not SUT-level

Both `supports_query_methods` (Rank 5) and `supports_mutator_methods`
(Tier 2b) are declared on `ParserRunner` with `= False` defaults.
Each runner opts in using its language's native reflection:

- **Java**: `Class.getMethods()` + harness CLI
  (`BioTestHarness --mode discover_methods`).
- **Python**: `inspect.signature` + `dir()` via
  `test_engine/runners/introspection.py`.
- **Python / Pydantic v2**: `model_fields` fast path (filters out
  `model_dump` / `model_validate` framework noise).
- **C / C++**: libclang AST walk via `harnesses/_reflect/libclang_walker.py`.
- **Rust**: rustdoc JSON via `harnesses/_reflect/rustdoc_parser.py`.

All five follow the same manifest shape
(`{name, returns, args: list[str]}`), so onboarding a new SUT in
language L is a copy-paste of L's existing adapter plus a tiny
opt-in flag — never a from-scratch reflection bring-up.

## Honest ceiling (paradigm-level, not SUT-specific)

Published upper bound for automated MR+fuzz testing of parser
libraries **without per-SUT harness code**: **~60 % line coverage**
(Liyanage & Böhme ICSE'23; Nguyen et al. Fuzzing Workshop 2023).
EvoSuite 1.2.0, a mature search-based generator, reaches 52.9 % on
htsjdk/VCF under the same 3-path filter BioTest uses. **BioTest's
empirical ceiling on its zero-per-SUT-code posture is ~47–48 %**
(Run 6 = 46.9 %, Runs 7/8 = 47.6–48.0 %). Progress above that requires
hand-written equivalence rules per class — the zero-user-cost exit.

This ceiling pattern holds on any parser SUT in this framework — the
gap shape (parser bucket high, data-model bucket low, writer bucket
middling) is a symptom of the file-in/canonical-JSON-out paradigm,
not of any particular library.

### Empirical cost/benefit of Tier 1 + Tier 2 (grounded in Runs 7–8)

| Run | Config | Wall | Weighted VCF | Δ vs Run 6 | pp/min |
|:-:|:--|:-:|:-:|:-:|:-:|
| 6 | baseline (Rank 6 off, budgets 5/5/5) | 170 m | 46.9 % | — | 0.276 (cumulative) |
| 7 | Rank 6 on, budgets 8/8/8, Tier 2 on | 330+ m (killed) | 48.0 % | +1.1 pp | **0.0069** marginal |
| 8 | Rank 6 on, budgets 5/5/5, Tier 2 on | 267 m (timeout overshoot) | 47.6 % | +0.7 pp | **0.0072** marginal |

**The marginal return of Tier 1+2 is ~40× less efficient than Run 6's
own per-minute rate.** Run 7 → Run 8 delta (0.4 pp) is within LLM /
corpus-ordering noise, so the "Tier 2 alone" attribution in Run 8 is
not reliably positive. Conclusion: **the code is sound, the paradigm
ceiling is real, and the default posture is "Tier 1+2 off" with
per-run opt-in for anyone wanting to pay the cost.**

### Current config defaults (as reverted 2026-04-20)

| Key                                                     | Default | Notes                                                                  |
|:--------------------------------------------------------|:-------:|:-----------------------------------------------------------------------|
| `feedback_control.mr_synthesis.enabled`                 | `false` | Rank 6. Flip to true per-run to pay the +0.7-1.1 pp at ~1.5-2× cost    |
| `feedback_control.mr_synthesis.max_mrs_per_iteration`   | 5       | kept — Run 8 showed 8 compounded quadratically                         |
| `feedback_control.max_iterations`                       | 4       | Run 7/8 both saturated by iter 3                                       |
| `feedback_control.timeout_minutes`                      | 180     | caveat: only checks between iterations; doesn't interrupt mid-Phase-C  |
| `feedback_control.plateau_patience`                     | 3       | SCC-based plateau check                                                |
| `feedback_control.min_coverage_delta_pp`                | 0.3     | coverage-based plateau check (Run 7 lesson — uses line coverage, not SCC) |
| `feedback_control.coverage_plateau_patience`            | 2       | stop after N iters with coverage delta < `min_coverage_delta_pp`       |
| `feedback_control.max_rules_per_iteration`              | 5       | kept — 8 added prompt tokens without MRs                               |
| `feedback_control.seed_synthesis.max_seeds_per_iteration` | 5     | kept                                                                   |
| `feedback_control.prompt_enrichment.per_class_blindspot` | `false` | Tier 2a, opt-in                                                        |
| `feedback_control.prompt_enrichment.mutator_catalog`    | `false` | Tier 2b, opt-in                                                        |

### References added

- **Fuzz4All** — Xia, Jia, Zhang, Wu, Xue, Chen, Zhang. *Universal
  Fuzzing with Large Language Models*. ICSE 2024. arXiv:2308.04748.
- **PromptFuzz** — Lyu, Sun, Ma, Tu, Wang. *PromptFuzz:
  Harnessing Large Language Models for Fuzz Driver Generation*. CCS
  2024. arXiv:2312.17677.
- **ChatAFL** — Meng, Su, Wen, Sun, Roychoudhury. *Large Language
  Model Guided Protocol Fuzzing*. NDSS 2024.
- **Liyanage & Böhme** — ICSE 2023. *Reachable Coverage: Estimating
  the Amount of Reachable Code in Fuzz-Testing*. Published ceiling
  reference.
- **Nguyen, Just, Hicks, Petke** — Fuzzing Workshop 2023
  (DOI 10.1145/3605157.3605177). *On the Effect of Fuzzing on API
  State*. "Most top fuzz blockers are not input-related — they require
  API state" — the paradigm limit BioTest deliberately inherits.
