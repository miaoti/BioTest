# Mutation Score 与 Bug Detection 的计算/判定细节（中文版）

本文回答两个具体问题：

1. **Mutation Score 究竟怎么算？** 我们有 5 个 SUT、4 种不同的 mutation 工具，分母分子的来源是什么？
2. **怎么判断一个 bug 是否被 detected？** 不同 testing tool（BioTest / Jazzer / Atheris / libFuzzer / cargo-fuzz / Pure Random / EvoSuite）的判定路径有何不同？

参考：`compares/DESIGN.md` §3.3、§4.3、§5.3.1、§5.3.2；以及实际代码 `compares/scripts/mutation_driver.py` 与 `compares/scripts/bug_bench_driver.py`。

---

## 一、Mutation Score 计算

### 1.1 一句话公式

```
score = killed / reachable
```

- `killed`：mutant 被某个 corpus 输入"杀掉"了（mutated SUT 的可观测输出 ≠ baseline）。
- `reachable`：corpus 实际执行到的那些 mutant；corpus 完全没碰到的代码区域里的 mutant **不进分母**（DESIGN §3.3 第 4 条："reachable = mutants in code the corpus actually executed. This avoids penalising coverage gaps twice"）。

> **为什么不用 `killed / total_mutants`？** 如果一个 corpus 只跑到了一半源代码，剩下那一半的 mutant 谁都杀不掉——把它们算进分母会让"corpus 杀伤力"和"corpus 触达面"两个指标搅在一起。先用 coverage 反映触达面，再用 mutation 反映"已触达代码里的判别能力"，两个指标各司其职。

### 1.2 "killed" 的统一判据

DESIGN §3.3 给出的是跨 SUT 通用判据：

> 把 mutant `m` 应用到 SUT，把工具的 corpus 跑过 mutated SUT。
> 只要某个 input `I` 的可观测输出（**parse-success flip**、**canonical-JSON diff**、**crash flip** 三者任一）与 unmutated baseline **不同**，`m` 就算被 killed。

举个具体例子（Atheris × vcfpy 那条 cell）：

- pristine vcfpy：`reader.parse(file_42.vcf)` → 成功，输出 `{open_ok=True, n_records=3, Σ POS=12345, ...}`
- 把 mutant `parser.py:line 88: a + b → a - b` 应用上去，再跑 `file_42.vcf`：
  - 如果输出变成 `{open_ok=True, n_records=3, Σ POS=12299, ...}` → fingerprint 不同 → killed。
  - 如果直接抛 `IndexError` → "crash flip" → killed。
  - 如果输出和 baseline 一模一样 → survived。

代码上 `mutation_driver.py:691-705` 写得很直白：fingerprint 是一个整数元组 `{open_ok, n_header_lines, n_records, Σ POS, Σ len(REF), Σ ord(CHROM), INFO/FORMAT/ALT/calls/FILTER cardinality, mid-iteration exception class}`，逐文件比对。

### 1.3 五个 SUT 用五种不同工具——但概念是一样的

| SUT | 语言 | Mutation 工具 | mutator 来源 |
| :--- | :--- | :--- | :--- |
| htsjdk | Java | **PIT** 1.15+ | DEFAULT_GROUP（条件翻转、算术替换、return 值改写、null check 删除…） |
| vcfpy | Python | **mutmut** 3.x | AST 改写（算术、比较、布尔翻转、`not` 删除、常量改写） |
| biopython | Python | **mutmut** 3.x | 同上 |
| noodles-vcf | Rust | **cargo-mutants** 25.x | 源码级（替换函数返回值、改 match arm、删除条件） |
| seqan3 | C++ | **mull** 0.33 (LLVM 18) | LLVM-IR 级（IR 指令替换） |

**每种工具都把自己的"mutant 状态"映射到 killed/reachable 两个桶**。具体映射：

#### mutmut（vcfpy / biopython）

`mutation_driver.py:489-502`：

```python
killed     = status_counts["killed"]
survived   = status_counts["survived"]
timeout    = status_counts["timeout"]      # 超时 → 行为变化 → 算 killed*
suspicious = status_counts["suspicious"]
no_tests   = status_counts["no tests"]     # 没被 corpus 触达 → unreachable
not_checked= status_counts["not checked"]
skipped    = status_counts["skipped"]

reachable  = killed + survived + timeout + suspicious
total      = reachable + skipped + no_tests + not_checked
score      = killed / reachable
```

注意 `no_tests` 桶 = "mutant 那条语句根本没被 corpus 触发执行"，对应 DESIGN §3.3 的"unreachable"，不进分母。这是 mutmut 自带的能力——它知道每个 mutant 在哪一行、corpus 是否进了那一行。

#### cargo-mutants（noodles-vcf）

`mutation_driver.py:544-553` 的映射表：

```
Caught   → killed     （oracle 检测到 divergence）
Missed   → survived   （corpus 没区分出来）
Timeout  → killed*    （--timeout 超时算行为变化，按 killed 计）
Unviable → skipped    （mutant 编不过；不进分母）
Success  → baseline   （未变异的 control run；不进分子分母）
```

实际数据（`compares/results/mutation/cargo_fuzz/noodles/`）：

```
483 mutants 总共
- Caught:    21
- Timeout:    7   → killed = 21 + 7 = 28
- Missed:   271
- Unviable: 184  → 不进分母

reachable = 28 + 271 = 299
score     = 28 / 299 = 9.36 %
```

#### PIT（htsjdk）

PIT 自己输出 `{killed, survived, no_coverage, timed_out, memory_error}`：

```
killed_total = killed + timed_out
reachable    = killed_total + survived
score        = killed_total / reachable
```

`no_coverage` 桶就是"corpus 没执行到这条 mutant 所在行"，不进分母。

#### mull（seqan3）

mull 输出 LLVM-IR 级 mutant 的 `{killed, survived, skipped}`，逻辑同上。

### 1.4 对比：cargo-fuzz 的 9.36 % vs Jazzer 的 89.59 %

DESIGN §3.3 的标题就是"coverage saturates before defect-detection"——这个落差正好印证了这一点：

| Cell | Phase-2 line coverage | Phase-3 mutation score | 差距说明 |
| :--- | :---: | :---: | :--- |
| Jazzer × htsjdk | ~高 | **89.59 %** | crash-fuzzer 的 corpus 撞遍了 parser 主路径，且 PIT 的 mutator 多在 if 边界里，corpus 一旦经过都会触发输出差异 |
| Atheris × vcfpy | 55.0 % | **89.59 %** ± 4 runs 88.10 % | Python 解析路径短、可观测性强 |
| cargo_fuzz × noodles | 22.7 % | **9.36 %** | corpus 大量 mutant 落在 field-accessor（`record.info().get(key)`），read-only oracle 不调那些 method → coverage 低 + score 低，**双低** |

> 这里有个常见误解：cargo-fuzz 的 9.36 % **不是**因为 cargo-fuzz "弱"，而是因为我们给它的 oracle（`tests/biotest_corpus_oracle.rs`）只 read + fingerprint，没碰 writer / accessor 路径。换一个 oracle，分数会显著上升。这就是 DESIGN §3.3 强调"oracle quality 与 input quality 是两件事"的原因。

### 1.5 一个完整的端到端例子：Atheris × vcfpy

1. **Phase 2** Atheris 跑 7200 s，产生 corpus（accepted inputs）→ 比如 1025 个 `.vcf` 文件。
2. **Phase 3 准备**：
   - 把 vcfpy 源码复制一份到 `<out>/vcfpy/`（pristine）。
   - 在 `<out>/tests/` 放 `test_vcfpy_corpus.py`：每个测试用例就是把 corpus 里的某个 .vcf 喂给 vcfpy.Reader，记录 fingerprint。
   - 用 `mutmut --create-mutants` 把 vcfpy 改写成 2338 个 mutant 副本。
3. **Phase 3 baseline**：以 `MUTANT_UNDER_TEST=''` 跑一次 baseline，记下每个 corpus 文件的 fingerprint → 写入 `baseline.json`。
4. **Phase 3 主跑**：mutmut 逐个 mutant 切换 `MUTANT_UNDER_TEST=<id>`，跑 `test_vcfpy_corpus.py`：
   - 任何一个 corpus 文件的 fingerprint 与 baseline 不同（或抛了 baseline 没抛的异常）→ test fail → mutant killed。
   - 全 1025 个 corpus 文件都 fingerprint 一致 → mutant survived。
   - 那条 mutant 所在的 .py 文件 corpus 根本没 import → mutmut 标 `no_tests` → 不进分母。
5. **结果**：
   ```
   killed     = 852
   survived   = 99
   timeout    = 0
   reachable  = 951
   no_tests   = 1387   （bgzf.py / tabix.py / writer.py — read-only harness 没碰）
   total      = 2338
   score      = 852 / 951 = 89.59 %
   ```

输出落到 `compares/results/mutation/atheris/vcfpy/summary.json`。

---

## 二、Bug Detection 判定

### 2.1 形式化定义（DESIGN §5.3.1）

```
detects(T, B) := ∃ I produced by T during its run on V_pre such that
                  signal_T(I, V_pre) = true   AND   signal_T(I, V_post) = false
```

**为什么不直接用"找到 crash"算 detected？** DESIGN §5.3.1 引用了 Klees CCS'18：

- (i) 一个 bug 经常产生几十个不同的 crash input（hash bucket 散开）→ raw crash count 严重高估。
- (ii) crash 可能是 spec-ambiguous input，所有实现都拒绝，根本不是 SUT 的 bug。
- (iii) coverage-driven fuzzer 还会撞到依赖库里跟 target bug 完全无关的 crash。

所以我们要求"在 V_pre 触发 + 在 V_post 静默"两个条件同时成立，强制建立"input ↔ 目标 bug"的因果链。

### 2.2 §5.3.2 的双向 predicate（accept-when-should-reject）

只用 forward（pre 抛 / post 干净）会漏掉一类 bug：**pre 错误地接受了 spec-invalid 的输入，post 才正确拒绝**。典型代表是 `htsjdk-1238`（RNAME 正则收紧，pre-fix 把 `chr@1` 这种非法名字接受了）。

所以 driver 实际跑的是双向版：

```
detects(T, B) := ∃ I such that
   ( signal(I, V_pre)=true  AND signal(I, V_post)=false )    ← forward
 OR
   ( signal(I, V_pre)=false AND signal(I, V_post)=true )     ← reverse
```

代码里 `bug_bench_driver.py:1237-1278` 的 PoV reverse fallback 就是这条 reverse 路径。

### 2.3 三个 boolean 字段（每个 cell 都要写齐）

`bug_bench_driver.py:91-101` 的 `BugResult` dataclass：

| 字段 | 类型 | 含义 |
| :--- | :--- | :--- |
| `detected` | bool | `signal_T(I, V_pre) = true` 是否在该工具的产出里至少出现一次 |
| `trigger_input` | str \| null | 触发该 signal 的代表性 input I 的路径 |
| `confirmed_fix_silences_signal` | bool \| null | `signal_T(I, V_post) = false` 是否被验证 |

**算"工具 T 找到 bug B"的条件（DESIGN §5.3.1）**：

```
detected == true  AND  trigger_input != null  AND  confirmed_fix_silences_signal == true
```

任何一个不满足都不算。例如 `detected==true` 但 `confirmed_fix_silences_signal==false` → 这是个跟目标 bug 无关的 crash → 进 `null_silences` 桶，由 chat 6 post-run review 手工裁断（DESIGN §5.3.1 末段）。

`compares/scripts/post_run_review.py` 在第 85-92 行做的就是这个裁定：

```python
if pre_failed and post_silenced:
    per_cell[(tool, sut)]["FOUND"] += 1
else:
    null_silences.append(r)
```

### 2.4 不同 tool class 的 signal_T(I, V) 定义

DESIGN §4.3 + §5.3.1 给出 5 种工具的 signal 各自怎么算：

| 工具 | signal_T(I, V) 是什么？ | adapter 怎么知道这个 signal 触发了？ |
| :--- | :--- | :--- |
| **Jazzer / Atheris / libFuzzer / cargo-fuzz** | "用 V 编译/链接的 fuzzer 把 I 写进了 `crashes/` 目录" | adapter 数 `crashes/*` 文件数。例如 `run_jazzer.py:106`：`crash_count=count_files(crashes_dir)`。Crash artifact 命名是 libFuzzer 约定（`crash-*`、`timeout-*`、`leak-*`、`slow-unit-*`），Atheris/Jazzer/cargo-fuzz 全部继承 |
| **Pure Random** | "V 的 `ParserRunner.run(I)` 抛了未捕获异常" | post-hoc replay：把 `pure_random/<bug>/corpus/*.vcf` 一个个跑，任何 exception 算 crash（Miller CACM'90 范式） |
| **EvoSuite**（仅 htsjdk anchor） | "EvoSuite 生成的 JUnit case `T_I` 在 V 上 FAIL" | 解析 `junit.xml` |
| **BioTest** | "V 的 canonical-JSON 与 ≥1 个其他 voter 的 canonical-JSON 不一致"（differential 路径）OR "`data/mr_registry.json` 里至少一条 metamorphic relation 在 I 上被违反"（metamorphic 路径） | adapter 数 `bug_reports/<id>/` 子目录数。`run_biotest.py:691-693`：`crash_count = sum(1 for _ in crashes_dir.iterdir())`——注意 BioTest 的 "crashes" 项是子目录（包含 JSON + seed + diff），不是 .crash 文件 |

### 2.5 Silence 验证机制（关键的"post-fix 不再触发"那一步）

代码在 `bug_bench_driver.py:1497`，函数叫 `_replay_trigger_silenced(sut, trig_path, fmt) → bool | None`：

- **True** → post-fix 把 trigger 干净地 parse 通过了 → signal silenced → 这是 §5.3.1 的真 detection。
- **False** → post-fix 还是失败 → 不是目标 bug，可能是另一个还没修的 bug → 不算 detection。
- **None** → 重放本身不可能（缺 runner、缺 binary、平台不匹配）→ 进 `null_silences` 桶等手工 triage。

每个 SUT 的"重放 + 判 silence"逻辑不一样，因为它们的可观测面不一样：

#### htsjdk（`bug_bench_driver.py:1597-1649`）

不只是"调 parser 看抛不抛"，而是 **deep predicate**：
1. parse → 必须 success
2. write_roundtrip → 必须 success
3. 重新 parse 改写后的文件 → 必须 success
4. 比对前后 canonical_json 的 `{CHROM, POS, REF, ALT}` → 必须相等

任何一步失败都返回 False。这样 writer bug（如 `htsjdk-1389` 把多值 missing field 写成 `.,.,.`）才能在 silence 验证里暴露出来。

外加 STRICT-stringency 网关（`bug_bench_driver.py:1516-1524`）：先用 `ValidationStringency.STRICT` 跑一遍，STRICT 拒绝就直接 short-circuit 到 `not silenced`。这样 `htsjdk-1360`（STRICT 才拒绝零长度 read）在默认 SILENT 下看不到的差异也能被捕获。

#### vcfpy（`bug_bench_driver.py:1544-1596`）

子进程跑一段 inline 的 Python：
1. `vcfpy.Reader.from_path(I)` 打开
2. 遍历 header lines、每条 record 的 `(CHROM, POS, ID, REF, ALT, QUAL, FILTER)`
3. 遍历每条 INFO key、每个 sample 的 FORMAT field（**deep iteration** 而不是 shallow——因为 vcfpy 大量是 lazy eval，`__iter__` 不触碰的话有些 KeyError 永远不会抛）
4. write_roundtrip → 重新 parse → 比对 record 数和 INFO key 内容

任何一步抛异常或对不齐 → False。

#### noodles（`bug_bench_driver.py:1668-1700+`）

调 Rust 写的 `noodles_harness`（一个独立 binary）：
1. `noodles_harness VCF I` → 返回 stdout 是 canonical JSON
2. 同 binary `--mode write_roundtrip` → 写一遍 + 重读 → 输出 canonical JSON
3. 字节级比对两个 canonical JSON

这是为了捕获 noodles 的 writer 系列 bug（259 / 268 / 300 / 339）——它们只在 "写出来再读回来" 时才暴露差异。

#### seqan3 / biopython

简化版：直接调 `Runner.run(I, fmt)`，看 `result.success` 是否为 True。

### 2.6 完整决策流程（这是真正的"逻辑判断"）

前面 2.1–2.5 都是组件级的解释，这一节把组件拼起来：**给定 (tool, bug)，driver 实际按什么顺序、走哪几条 if/else 来判定？** 全部对应 `bug_bench_driver.py:1025-1390` 的代码逻辑。

#### 阶段 A：装 pre-fix，跑 tool，建候选 trigger 列表

```
1. install_sut(sut, anchor, "pre_fix")
2. adapter_json = invoke_adapter(tool, bug, ...)        # 跑 2 小时
3. detected, ttfb, trig, sig = detection_from_adapter(adapter_json, bug)
   #  detection_from_adapter 的逻辑很简单（line 900-923）：
   #    if adapter_json["crash_count"] > 0:
   #        return True, mid_point, first_file_in_crashes_dir, signal_type
   #    else:
   #        return False, None, None, None
```

**到这里 detected 只反映"adapter 有没有报 crash"，跟"目标 bug 有没有被找到"还差好几道关。**

```
4. 建候选列表 candidates:
   a. PoV 优先 — compares/bug_bench/triggers/<bug_id>/original.{vcf,sam}（如果存在）
   b. adapter 自己挖的 crashes/ 目录里前 30 个文件
```

#### 阶段 A 的候选循环（line 1090-1125）— 这是核心判定

```python
picked_fail = None    # 用来支持 forward §5.3.1（pre 抛 → 后续验 post 不抛）
picked_ok   = None    # 用来支持 reverse §5.3.1（pre 接受 → 后续验 post 拒）

for cand in candidates:
    silenced_here = _replay_trigger_silenced(sut, cand, fmt)
    #   ↑ 注意：这一步是把 cand 喂给 PRE-FIX SUT 跑一遍，
    #     函数名虽然是 "silenced"，但语义是 "pre-fix 是否干净接受"
    #     - True   → pre-fix 接受 → 候选 reverse §5.3.1
    #     - False  → pre-fix 拒绝/抛 → 候选 forward §5.3.1
    #     - None   → 重放本身失败 → 跳过

    if silenced_here is False:
        picked_fail = cand
        break                  # 一旦找到 forward 候选，停止循环
    if silenced_here is True and picked_ok is None:
        picked_ok = cand       # 只记第一个 reverse 候选
```

**循环出来后做三向分流（line 1108-1125）**：

```python
if picked_fail:
    selected_trig    = picked_fail
    pre_fix_succeeds = False        # 标记: pre-fix 在这条 trigger 上失败
    # detected 保持原样（adapter 报 True 就是 True）

elif picked_ok:
    selected_trig    = picked_ok
    pre_fix_succeeds = True         # 标记: pre-fix 干净接受
    detected = False                # 临时降级 — 等阶段 B 才能确认

else:
    # 所有候选 replay 都返回 None → pre_fix_succeeds 留 None，沿用 adapter verdict
```

并且额外记一条 `pov_alt`（line 1136-1141）：**当 picked_fail 是 adapter 挖的 trigger、而 PoV 是 picked_ok 时**，把 PoV 缓存为"备用 reverse 候选"——这是 htsjdk-1238 走 reverse PoV-fallback 的关键。

#### 阶段 B：装 post-fix，按优先级走 4 条 promotion 路径

每个 cell 在阶段 B 走下面这 4 条 if（**顺序很重要——每条满足都会改写 detected/confirmed**）：

##### 路径 1：**默认 forward replay**（line 1211-1233）

```python
if detected and trig and replay_available:
    if tool in UNIT_ANCHOR_TOOLS:           # EvoSuite/Randoop 走自己的 JUnit 比对
        confirmed = True if (post_pass_count != None and pre_pass_count != None) else None
    else:
        confirmed = _replay_trigger_silenced(sut, trig, fmt)   # 这次喂给 POST-FIX
        # confirmed=True  → post-fix 接受 trigger → forward §5.3.1 命中
        # confirmed=False → post-fix 还失败       → false+
        # confirmed=None  → 重放不可能            → null_silences
```

##### 路径 2：**PoV reverse fallback**（line 1252-1276）

```python
if not confirmed and pov_alt and replay_available:
    alt_silenced = _replay_trigger_silenced(sut, pov_alt, fmt)   # POST-FIX 上 replay PoV
    if alt_silenced is False:
        # PoV 在 pre-fix 被接受、在 post-fix 被拒 → reverse §5.3.1
        detected   = True
        confirmed  = True
        trig       = pov_alt
        notes      = "reverse §5.3.1 via PoV fallback"
```

> **`htsjdk-1238` jazzer/pure_random 都靠这条 promote 成 FOUND**——adapter 挖的 synthetic trigger 验证不过（post-fix 还抛），但 canonical PoV 在 pre 接受 / post STRICT 拒，这是真目标 bug。

##### 路径 3：**STRICT-gate forward fallback**（line 1287-1309）

```python
if pre_fix_succeeds is False and not detected and replay_available and trig:
    post_silenced_strict = _replay_trigger_silenced(sut, trig, fmt)
    # _replay_trigger_silenced 内部先走 STRICT-gate prelude（line 1516-1524）：
    #     if runner.supports_strict_parse:
    #         sp = runner.run_strict_parse(trig, fmt)
    #         if not sp.success:
    #             return False    # short-circuit
    if post_silenced_strict is True:
        detected   = True
        confirmed  = True
        notes      = "forward §5.3.1 via STRICT gate"
```

> **`htsjdk-1360` / `htsjdk-1410` 都靠这条**——pre-fix STRICT 拒（EMPTY_READ / TLEN cap），post-fix 移除了那个验证 → STRICT 也接受。

##### 路径 4：**Reverse §5.3.1 主路径**（line 1317-1340）

```python
if pre_fix_succeeds is True and replay_available and trig:
    post_silenced = _replay_trigger_silenced(sut, trig, fmt)
    if post_silenced is False:
        # pre 接受 / post 拒 → reverse
        detected   = True
        confirmed  = True
        notes      = "reverse §5.3.1: pre-fix accepted, post-fix rejects"
```

##### 路径 5：**Method-signature diff (Rank 5)**（line 1350-1372）

```python
if pre_method_sig and post_method_sig and post_method_sig != pre_method_sig:
    detected   = True
    confirmed  = True
    notes      = "method-signature diff across versions"
```

> **`htsjdk-1544` 靠这条**——`getType()` 在两个版本上对同一 PoV 返回不同 scalar。`pre_method_sig` 是阶段 A 末尾对 PoV 做的 API 调用快照。

##### 终态降级（line 1373-1377）

如果以上 4 条都没 fire 但 `pre_fix_succeeds == True`：
```python
notes = "pre_fix SUT parses cleanly — detection demoted to False"
# detected = False, confirmed = None, → miss
```

#### 把 5 条路径压成一张分类表

阶段 A/B 走完后，driver 写出 `BugResult(detected, trigger_input, confirmed_fix_silences_signal)`，下游 `post_run_review.py` 按这个三元组分类：

| `detected` | `trigger` | `confirmed_fix_silences_signal` | → 分类 |
| :---: | :---: | :---: | :--- |
| True | not None | **True** | **FOUND** ✅ |
| True | not None | False | false+ ❌（真 bug 但不是目标） |
| True | not None | None | crash?（重放失败，进 null_silences） |
| False | — | — | miss |
| — | — | — (有 install_error) | skip |

#### 一个完整 trace 例子：jazzer × htsjdk-1238 走完整条 5 路径

```
阶段 A:
  install pre-fix htsjdk 2.18.1.jar
  jazzer 跑 2h → crashes/ 写了 12 个文件 → adapter 报 detected=True
  candidates = [PoV original.sam, crash-aaa, crash-bbb, ..., crash-lll]

  候选循环:
    cand=PoV          → _replay_trigger_silenced(htsjdk, PoV, SAM) on PRE-FIX
                        → htsjdk 2.18.1 接受这条 SN:gi|123|chr,1
                        → 返回 True
                        → picked_ok = PoV
    cand=crash-aaa    → 返回 False (pre-fix 抛 some other exception)
                        → picked_fail = crash-aaa, BREAK

  分流:
    picked_fail 存在 → selected_trig=crash-aaa, pre_fix_succeeds=False
    pov_alt=PoV (因为 picked_fail 是 harvested + picked_ok==PoV)

阶段 B:
  install post-fix htsjdk 2.18.2.jar

  路径 1 (默认 forward replay):
    confirmed = _replay_trigger_silenced(htsjdk, crash-aaa, SAM) on POST-FIX
              = False (post-fix 还抛同一个 exception)

  路径 2 (PoV reverse fallback):
    not confirmed AND pov_alt 存在 → 触发
    alt_silenced = _replay_trigger_silenced(htsjdk, PoV, SAM) on POST-FIX
                 = False (post-fix 抛 SAMException: Invalid RNAME)
    → detected=True, confirmed=True, trig=PoV
    → notes="reverse §5.3.1 via PoV fallback"

  路径 3-5: 已 confirmed，跳过

最终 BugResult:
  detected = True
  trigger_input = .../triggers/htsjdk-1238/original.sam
  confirmed_fix_silences_signal = True
  → 分类: FOUND ✅
```

如果**没有阶段 B 的路径 2 那个 fallback**，这个 cell 会卡在路径 1 的 `confirmed=False` → 被算成 false+ → htsjdk-1238 在 jazzer 这条 row 上就完全不算找到。这就是为什么 §5.3.2 双向 predicate + PoV fallback 不是花哨设计、而是必需逻辑。

---

### 2.7 完整端到端例子

#### 例 1：Jazzer × htsjdk-1238（reverse §5.3.1）

- **Phase A**：装 htsjdk 2.18.1.jar（pre-fix），跑 Jazzer 2 小时。
- Jazzer 把若干 `crash-*` 写到 `compares/results/bug_bench/jazzer/htsjdk-1238/crashes/`，比如 `crash-deadbeef`。
- adapter 报 `crash_count=12, crashes_dir=...`，driver `detection_from_adapter` 算出 `detected=True, trigger_input=crash-deadbeef, signal=crash`。
- **Phase A 候选循环**（`bug_bench_driver.py:1071-1126`）：以 PoV `triggers/htsjdk-1238/original.sam` 为首选 candidate，对每个 candidate 调 `_replay_trigger_silenced("htsjdk", cand, "SAM")`。
  - PoV 在 pre-fix 上跑了一遍，**返回 True**（pre-fix 接受这条 spec-invalid SN）→ 标 `picked_ok = PoV`。
- 候选循环 fall-through 到 reverse §5.3.1 路径。
- **Phase B**：装 htsjdk 2.18.2.jar（post-fix），调 `_replay_trigger_silenced("htsjdk", PoV, "SAM")`。
  - post-fix 抛 `SAMException: Invalid RNAME` → 返回 False（"silenced" = False）。
- 因此这是 reverse 命中：`detected=True (in V_pre signal=False but accepted)`、`trigger_input=PoV`、`confirmed_fix_silences=True (because reverse-direction post fail)`，notes 标 `"reverse §5.3.1 via PoV fallback"`。
- post_run_review 把它计入 `FOUND`。

#### 例 2：Atheris × vcfpy-176（forward §5.3.1）

- **Phase A**：`pip install vcfpy==0.13.8`，跑 Atheris 2 小时。
- Atheris fuzz target 调 `vcfpy.Reader.from_path` 时把 GT="0|0"（header 里没声明 GT）的输入塞进去 → vcfpy 内部 `ValueError: invalid literal for int() with base 10: "['0"`。
- libFuzzer runtime 把这个 input 写到 `crashes/crash-cafef00d`。
- **Phase B**：`pip install vcfpy==0.14.0`，调 `_replay_trigger_silenced("vcfpy", crash-cafef00d, "VCF")`。
  - 内部 inline Python 跑了一遍 deep predicate，没抛异常 + write_roundtrip 一致 → 返回 True。
- 计入 `FOUND`，`confirmed_fix_silences=True`，forward §5.3.1。

#### 例 3：cargo-fuzz × noodles-300（写回检测）

- **Phase A**：`Cargo.toml` pin `noodles-vcf = "0.63"`，重 build harness，跑 cargo-fuzz 2 小时。
- cargo-fuzz 没找到 crash → `detected=False`。
- 但 PoV 存在（`triggers/noodles-300/original.vcf`）→ 候选循环依然进入。
- 把 PoV 在 V_pre 上喂 `noodles_harness VCF original.vcf` → 返回 success（pre-fix 能 parse）。但 `--mode write_roundtrip` 写出来的文件再 parse → INFO 字段里的 `;` 被吞了 → canonical JSON 不一致 → 返回 False（pre-fix 没 silence）。
- **Phase B**：pin `noodles-vcf = "0.64"`，重新跑 write_roundtrip → canonical JSON 一致 → 返回 True。
- 这是个 forward §5.3.1 的"silent-accept-then-corrupt"型 bug：`detected=True (because pre-fix's write_roundtrip mismatches)`、`confirmed_fix_silences=True`，计入 `FOUND`。

#### 例 4：Pure Random × biopython（post-hoc replay）

- **Phase A**：直接用 `os.urandom` 生成 corpus 2 小时。
- Phase A 不 hook 任何 crash 信号（Pure Random 不是 in-process fuzzer），只是把 corpus 文件写出来。
- **Post-hoc replay**：在 `chat 6 post_run_review` 阶段，逐个把 `pure_random/<bug>/corpus/*.sam` 喂给 V_pre 的 `BiopythonRunner.run` →
  - 如果某个 `random_xxx.sam` 抛了异常（match Miller 1990 范式）→ `detected=True`，trigger 就是该文件。
- 然后调 `_replay_trigger_silenced("biopython", random_xxx.sam, "SAM")`：装 V_post 后再跑一次。
  - 抛 → False（不算 target bug detection）。
  - 不抛 → True，计入 FOUND。

---

## 三、汇总速查表

### Mutation score 速查

| Cell | 工具 | 分子 (`killed`) 来源 | 分母 (`reachable`) 来源 | "不算分母"的桶 |
| :--- | :--- | :--- | :--- | :--- |
| Atheris × vcfpy | mutmut | killed + timeout + suspicious | killed + survived + timeout + suspicious | no_tests, not_checked, skipped |
| Atheris × biopython | mutmut | 同上 | 同上 | 同上 |
| cargo-fuzz × noodles | cargo-mutants | Caught + Timeout | Caught + Missed + Timeout | Unviable, Success, Failure |
| Jazzer × htsjdk | PIT | killed + timed_out | killed + timed_out + survived | no_coverage, memory_error |
| libFuzzer × seqan3 | mull | killed | killed + survived | skipped (IR-unreachable) |

### Bug detection 速查

| 工具 | "在 V_pre 触发" 的 signal | adapter 怎么数 | "在 V_post silence" 怎么验 |
| :--- | :--- | :--- | :--- |
| Jazzer / Atheris / libFuzzer / cargo-fuzz | crashes/ 目录里出现 artifact | `count_files(crashes_dir)` | `_replay_trigger_silenced` 跑 deep parser predicate |
| BioTest | bug_reports/<id>/ 子目录出现 | `sum(1 for _ in crashes_dir.iterdir())` | 同上 |
| Pure Random | corpus 文件 post-hoc replay 抛异常 | post-run review 里 replay | 同上 |
| EvoSuite | junit.xml 里的 testcase failure | 解析 junit XML | EvoSuite 在 V_post 上重跑同 testcase 看是否 PASS |

### "FOUND" 的最终判定

```
FOUND ⇔ detected==True  AND  trigger_input!=None  AND  confirmed_fix_silences==True
```

否则进 `null_silences` 桶等手工 triage。

---

## 四、实际 bench 里每个 bug 的判定路径

数据来自 `compares/results/bug_bench/post_run_review.md`（74 cells）和 `DETECTION_RATIONALE.md`（BioTest 13/32 confirmed）。下面按 cell（tool, sut）逐 bug 列出实际分类结果。

### 4.1 全局总览

| 分类 | 数量 | 含义 |
| :--- | ---: | :--- |
| **FOUND** | **9** | 真正命中目标 bug（detected ∧ trigger ∧ post-fix silenced） |
| false+ | 11 | adapter 报 crash 了，但 post-fix 还是 crash → **真 bug，但不是目标 bug** |
| miss | 47 | adapter 没报 crash → 没动静 |
| skip | 7 | install 失败或 adapter 不可用（这 7 个全是 evosuite_anchor/htsjdk 的 ClassLoader 问题） |

### 4.2 每个 cell 的 FOUND 数（来自 `post_run_review.md` 第 22-32 行）

| cell | total | FOUND | false+ | miss | skip |
| :--- | ---: | ---: | ---: | ---: | ---: |
| evosuite_anchor/htsjdk | 12 | **4** | 0 | 1 | 7 |
| jazzer/htsjdk | 12 | **2** | 10 | 0 | 0 |
| pure_random/htsjdk | 12 | **3** | 0 | 9 | 0 |
| libfuzzer/seqan3 | 6 | 0 | 1 | 5 | 0 |
| atheris/vcfpy | 7 | 0 | 0 | 7 | 0 |
| cargo_fuzz/noodles | 6 | 0 | 0 | 6 | 0 |
| pure_random/{noodles,vcfpy,seqan3} | 6+7+6 | 0 | 0 | all miss | 0 |

> BioTest 的 cell 不在这张表里——它走自己的 oracle，结果在 `DETECTION_RATIONALE.md`：**13 / 32 confirmed (40.6 %)**，VCF 10/23 + SAM 3/9。

### 4.3 EvoSuite 找到的 4 个（全是 htsjdk VCF）

| bug | 判定路径 | 具体怎么判的 |
| :--- | :--- | :--- |
| `htsjdk-1403` | adapter 内部 JUnit 比对 | EvoSuite 生成的 `test02` 在 pre-fix 2.20.0 抛 `NPE at VariantContextBuilder.filters:405`，在 post-fix 2.20.1 通过 |
| `htsjdk-1418` | adapter 内部 JUnit 比对 | 生成的 `test06` 在 pre-fix 2.20.1 抛 `TribbleException: Contig ID does not have a length field`，post-fix 2.21.0 通过 |
| `htsjdk-1389` | pre-compile drift | EvoSuite 用 post-fix 2.20.0 生成的 21 个测试，在 pre-fix 2.19.0 上 21 个全编不过——`VCFEncoder` API 在小版本间被改了 → 视为"编不过=测试失败"算 FOUND |
| `htsjdk-1401` | pre-compile drift | 同样 shape，43/47 个 method 编不过 |

> EvoSuite 完全走自己的 `.java` 测试比对路径，不进 `_replay_trigger_silenced`（`bug_bench_driver.py:188` 显式 short-circuit）。

### 4.4 Jazzer 找到的 2 个（**都是通过 PoV reverse-fallback**，不是 jazzer 自己挖的）

| bug | 判定路径 | 触发文件来源 | 具体 |
| :--- | :--- | :--- | :--- |
| `htsjdk-1238` | **reverse §5.3.1 via PoV fallback** | `compares/bug_bench/triggers/htsjdk-1238/original.sam` | jazzer 自己挖的 crash 不算数；canonical PoV (`@SQ SN:gi\|123\|chr,1`，RNAME 含逗号) 在 pre-fix 2.18.1 被静默接受，在 post-fix 2.18.2 被 `SAMSequenceRecord` 收紧的正则 STRICT-reject |
| `htsjdk-1410` | **forward §5.3.1 via STRICT gate** | canonical PoV | pre-fix 2.20.2 STRICT 抛 `\|TLEN\| > 2^29` 拒绝；post-fix 2.20.3 把上限提到 `Integer.MAX_VALUE` 接受 |

> 也就是说：**jazzer 的 12 个 SAM/VCF cell 里，jazzer 本身一个目标 bug 都没挖到**。这 2 个 FOUND 是 driver 在候选循环里把 PoV 当 fallback 喂进去触发的——任何工具理论上都能拿这 2 分（pure_random 拿了 3 分就是证据）。

### 4.5 Jazzer 的 10 个 false+（**真 bug，但不是目标**）

9 个 VCF cell（1364/1372/1389/1401/1403/1418/1544/1554/1637）全部因为同一条 latent bug：

```
java.lang.IndexOutOfBoundsException: Index <N> out of bounds for length <M>
    at htsjdk.variant.vcf.AbstractVCFCodec.oneAllele(AbstractVCFCodec.java:582)
    at VCFCodecFuzzer.fuzzerTestOneInput(VCFCodecFuzzer.java:52)
```

- libFuzzer 的 `DEDUP_TOKEN` 把 9 个 cell 总共 ~735 个 crashes 收敛到 **2 个 unique signature**，全在 `oneAllele:582`。
- driver 把 jazzer 写出来的 `crashes/crash-*` 喂给 post-fix runner → **9 个 cell 全部还抛**同一个异常 → `confirmed_fix_silences=False` → false+。
- `htsjdk-1418` 这个理论上 crash-finder 能找的 bug（`expected_signal.type == uncaught_exception`），把 jazzer 挖的 **164 个 crash 全部** replay 到 post-fix htsjdk 2.21.0 → **0/164 silence** → 确认 jazzer 真的没找到 1418，只是反复在 oneAllele:582 那条 latent bug 上撞。

剩下 1 个 SAM false+ 是 `htsjdk-1360`：jazzer 挖到一个 synthetic SAM trigger 让 pre-fix STRICT 抛 EMPTY_READ，但同一个 synthetic 在 post-fix 还抛（多了别的 spec 违反）。这个 cell 的候选循环里 jazzer 的 harvested trigger 优先级**抢在 PoV 前面**，结果落到 false+；PoV 本来能让它变 FOUND（pure_random 那边就是这样拿到 1360 的）。

### 4.6 Pure Random 找到的 3 个（**全靠 PoV**）

`run_pure_random.py` 里 `crash_count` 硬编码 0——adapter 本身根本不调 SUT，只生成 `os.urandom` 字节。这 3 个 FOUND 全是 driver 把 PoV 当候选喂进 `_replay_trigger_silenced` 拿到的：

| bug | 判定路径 | 关键差异 |
| :--- | :--- | :--- |
| `htsjdk-1238` | reverse §5.3.1 | 同 jazzer-1238，pre 接受 / post STRICT 拒 |
| `htsjdk-1360` | forward §5.3.1 via STRICT gate | pre-fix STRICT 抛 EMPTY_READ；post-fix 接受（jazzer 在这个 cell 输给了 candidate ordering） |
| `htsjdk-1410` | forward §5.3.1 via STRICT gate | 同 jazzer-1410 |

> jazzer (2 SAM FOUND) vs pure_random (3 SAM FOUND) 的差异**不是 fuzzer 强弱**，而是 candidate 优先级——jazzer 有 harvested triggers 抢先；pure_random 没 harvested triggers，PoV 永远赢。

### 4.7 libFuzzer 的 1 个 false+（seqan3-3269）

- libfuzzer 跑了 7200 s，在 `-ignore_crashes=1` 下记录了 **~20,400 个 deadly signal** 事件，第 1 个被存为 `trigger_input`。
- 实际是 seqan3 SAM/BAM 或 BGZF 路径里一个反复触发的 latent crash，pre-fix `ca4d668` 和 post-fix `11564cb` **两边都还在**。
- driver replay → post-fix 也 crash → `confirmed_fix_silences=False` → false+。
- 真实的 seqan3-3269 是 banded alignment 返回**相对位置而不是绝对位置**——一个 wrong-result bug，crash-only fuzzer **结构性地无法观察**（没 oracle 比 output value）。

### 4.8 Atheris / cargo_fuzz / pure_random（除 htsjdk）全部 miss 的原因

| cell | 为什么没 FOUND |
| :--- | :--- |
| atheris/vcfpy（7 cells） | vcfpy.Reader 把内部异常 catch 在 fuzz harness 里 → `crashes/` 永远空 → 没 trigger 可 replay → miss |
| cargo_fuzz/noodles（6 cells） | noodles-vcf 设计上返回 `Result<>` 而不是 panic → 不产生 deadly signal → miss |
| pure_random/{noodles,vcfpy,seqan3}（19 cells） | 这些 SUT 的 PoV 主要是 differential_disagreement 或 API mutator → single-shot parse 看不到 → miss |

### 4.9 BioTest 找到的 13 个（来自 `DETECTION_RATIONALE.md`）

| # | bug | SUT | 判定路径 | 关键机制 |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `htsjdk-1554` | htsjdk VCF | reverse §5.3.1 | 2-sample VCF `GT:FT`，pre 静默接受 / post 改正 counter 后拒绝 |
| 2 | `htsjdk-1364` | htsjdk VCF | forward §5.3.1 via STRICT | 混合大小写 `NaN/Inf`，pre STRICT 抛 NumberFormatException；htslib+pysam 都接受 |
| 3 | `htsjdk-1389` | htsjdk VCF | forward §5.3.1 via STRICT + write-roundtrip | pre 写出 `.,.,.`，reparse-canonical-compare 飙差异 |
| 4 | `htsjdk-1372` | htsjdk VCF | forward §5.3.1 via STRICT | `GL=.,.,.` pre STRICT 拒 / post 当 missing 接受 |
| 5 | `htsjdk-1418` | htsjdk VCF | forward §5.3.1 via STRICT | `##contig=<ID=X>` 不带 length pre 拒 / post 接 |
| 6 | `htsjdk-1544` | htsjdk VCF | reverse §5.3.1 | `getType()` 误分类 `<NON_REF>`，PoV 双向扫到 |
| 7 | `vcfpy-176` | vcfpy | forward §5.3.1 via STRICT | vcfpy deep traversal 触发 lazy `_genotype_updated` 抛 ValueError |
| 8 | `vcfpy-146` | vcfpy | forward §5.3.1 via STRICT | INFO Flag 强转 String → `TypeError: 'bool' is not iterable` |
| 9 | `vcfpy-127` | vcfpy | forward §5.3.1 via STRICT | `call.data.get(fmt_k)` 触 `KeyError: 'GQ'`（shallow iter 触不到） |
| 10 | `noodles-268` | noodles | forward §5.3.1 via STRICT + write-roundtrip | IUPAC 模糊码污染 writer，reparse 不一致 |
| 11 | `htsjdk-1238` | htsjdk SAM | reverse §5.3.1 | 同上面 1238，PoV `picked_ok` + post replay False |
| 12 | `htsjdk-1360` | htsjdk SAM | forward §5.3.1 via STRICT | EMPTY_READ block |
| 13 | `htsjdk-1410` | htsjdk SAM | forward §5.3.1 via STRICT | TLEN cap |

### 4.10 BioTest 的 21 个 miss 分桶（同样来自 `DETECTION_RATIONALE.md`）

| 桶 | 数量 | 代表 bug | 为什么没找到 |
| :--- | ---: | :--- | :--- |
| install / build 失败（基建问题，非 paradigm） | 4 | `noodles-{223,224,ob1-0.23}`, `seqan3-2418` | `cargo build --release` 对 pin 版本失败、harness CMake build-rot |
| pre/post 都干净 parse（PoV richness 不足） | 4 | `vcfpy-171`（%3D 转义只在 write 路径丢失，dict 强转掩盖了差异）、`noodles-{300,339,259}` | 需要字节级 write-roundtrip diff 或更精细 PoV |
| anchor 或 PoV 富度问题（无诊断） | 4 | `htsjdk-1401`、`vcfpy-145`、`noodles-{241,inforay-0.64}` | `.bgz` 后缀被 subprocess wrapper normalize 掉、anchor 太窄等 |
| paradigm-out（**不能**通过文件级 differential 检测） | 7 | `htsjdk-1637`（multi-file VCF merge）、`htsjdk-1403`（VariantContextBuilder mutator 链）、`seqan3-3081`（zero-record writer）、`seqan3-{3269,3098}`（alignment-internal score 计算）、`seqan3-2869`（实际是 FASTA bug，不在 SAM 范围）、`seqan3-3406`（BGZF 并发数据竞争） | 这些 bug **本质上**不是 file-input → parse → output 这条线能观测到的；DESIGN §5.1.1 honesty audit 故意保留它们作为"已知零分"，不作弊 |
| 其他 PoV 富度 | 2 | 略 | 同上 |

---

### 4.11 一个常见疑问

> "为什么 jazzer 跑出来一堆 crash 却只算 2 个 FOUND，pure_random 啥都没跑反而算 3 个 FOUND？"

短答：**因为我们**不**把"找到任意 crash"算 detection**——必须满足"在 V_pre 触发 + 在 V_post silenced + 这条 trigger 跟目标 bug 在因果上对得上"三条。jazzer 那 ~735 个 crash 全集中在一条 oneAllele:582 的 latent bug 上，post-fix 还抛 → false+。pure_random 没自己挖 crash，但 driver 把 PoV 当候选喂进去触发 §5.3.1 双向扫描，PoV 直接对得上目标 bug → FOUND。这恰恰是 DESIGN §5.3.1 引用 Klees CCS'18 的目的：raw crash count 严重高估真实 detection。

---

## 五、相关代码定位

| 内容 | 文件:行 |
| :--- | :--- |
| Mutation score 公式（mutmut） | `compares/scripts/mutation_driver.py:489-515` |
| Mutation score 公式（cargo-mutants） | `compares/scripts/mutation_driver.py:723-770` |
| BugResult dataclass | `compares/scripts/bug_bench_driver.py:91-101` |
| 候选循环 + reverse §5.3.1 | `compares/scripts/bug_bench_driver.py:1071-1278` |
| `_replay_trigger_silenced` | `compares/scripts/bug_bench_driver.py:1497` |
| FOUND/null_silence 裁定 | `compares/scripts/post_run_review.py:80-95` |
| crash_count 在各 adapter 的算法 | `compares/scripts/tool_adapters/run_jazzer.py:106` ↔ `run_biotest.py:691` |
