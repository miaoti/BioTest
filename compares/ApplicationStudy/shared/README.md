# shared/ — 跨变体共用资源

## `build_spec_dump.py`

把 `data/raw_tex/VCFv4.5.tex` 与 `SAMv1.tex` 经 `pylatexenc` 转纯文本，
截前 32k tokens，写到 `shared/raw_spec_dump.txt`。

**用途**：E1（−A）与 E3（−A−D）的 wrapper 脚本会读取该文件并通过
monkey-patch 把内容追加到 LLM 的 system prompt 里——naive prompt-
stuffing 替代 RAG retrieval。

**何时跑**：

* 第一次跑 E1 / E3 之前；
* `data/raw_tex/` 里的 `.tex` 更新后（spec 升级到 v4.6 等）。

**命令**：

```bash
py -3.12 compares/ApplicationStudy/shared/build_spec_dump.py
```

输出 `shared/raw_spec_dump.txt`（gitignored；regenerable）。
