# `compares/docker/` — Benchmark container

A single Docker image carries every tool the comparative evaluation
needs (DESIGN.md §13.1). One `docker build` replaces the full WSL2
install sequence.

Why Docker instead of raw WSL2? Docker Desktop on Windows already uses
WSL2 as its backend, so you pay the same VM cost either way. Docker
adds:

- **Reproducibility** — the Dockerfile is the spec.
- **Isolation** — no tool conflicts with host or other projects.
- **Alignment** — the existing `harnesses/pysam/` setup already uses
  Docker; this is the same pattern.

## Quick start

```bash
# 1. Build (~7 GB download; takes 15–25 minutes on first build)
bash compares/docker/build.sh

# 2. Drop into an interactive shell with the repo mounted at /work
bash compares/docker/run.sh

# 3. From inside the container — or via `run.sh -- …` from Windows —
#    run the one-shot smoke test
bash compares/docker/verify.sh
```

All the benchmark scripts (`compares/scripts/*.py`,
`compares/scripts/tool_adapters/*.py`, `biotest.py`) work unchanged
inside the container because the repo is mounted at `/work`.

## What's inside

| Layer | Tool | Version | Purpose |
| :---- | :--- | :------ | :------ |
| Base | Ubuntu | 22.04 | host OS |
| JVM | Temurin JDK | 17 | Jazzer + EvoSuite + PIT |
| Python | CPython | 3.12 | BioTest + Atheris + pysam + biopython |
| C++ | Clang / LLVM | 18 | libFuzzer + AddressSanitizer + mull |
| C++ | libseqan3-dev | distro | seqan3 C++23 SAM/BAM library |
| Fuzzer | Jazzer | 0.22.1 | Java coverage-guided fuzzer |
| Fuzzer | Atheris | 2.3.0 | Python coverage-guided fuzzer |
| Fuzzer | libFuzzer | Clang 18 built-in | C++ coverage-guided fuzzer |
| Unit-test gen | EvoSuite | 1.2.0 | white-box Java anchor |
| Mutation | PIT | 1.15.3 | Java mutation scoring |
| Mutation | mutmut | 3.0.0 | Python mutation scoring |
| Mutation | mull | 0.18.0 | C++ mutation scoring |
| Coverage | JaCoCo agent | bundled via htsjdk build | Java coverage |
| Coverage | coverage.py | 7.6.0 | Python coverage |
| Coverage | gcovr, lcov | distro | C++ coverage |
| Build | Gradle | 8.5 | Jazzer harness build |
| Build | Maven | distro | PIT integration |

## Volumes and paths

`run.sh` mounts the repo root at `/work` inside the container. Outputs
written to `/work/compares/results/` are visible on the host. This is
symmetric with the `pysam` Docker harness.

The image keeps tools under `/opt/`:
- `/opt/jazzer/` — Jazzer CLI + agent
- `/opt/evosuite/evosuite.jar` — EvoSuite runner JAR
- `/opt/pit/pitest-command-line.jar` — PIT runner JAR
- `/opt/mull/bin/` — mull binaries (also on PATH)

## Windows-specific notes

- **Docker Desktop** must be running with the WSL2 backend enabled
  (default on Windows 10+/11).
- Git-Bash / MSYS mount-path quirks are handled in `run.sh` via the
  `//` prefix idiom.
- First-time builds pull ~7 GB and compile Atheris against Clang 18.
  Budget 15–25 minutes on broadband.

## Troubleshooting

| Symptom | Likely cause | Fix |
| :------ | :----------- | :-- |
| `Error response from daemon: Dockerfile parse error` | Windows CRLF line endings in Dockerfile | `git config core.autocrlf input` and re-checkout |
| `ld.lld: not found` during libFuzzer smoke test | lld package missed | rebuild the image; apt has `lld-18` pinned |
| Atheris `ImportError` on `import atheris` | wheel built against a different Clang | `CC=clang-18 pip install --no-binary :all: atheris==2.3.0` inside the image |
| seqan3 include fails | libseqan3-dev apt pin drifted | rebuild the image; Dockerfile re-pulls latest distro package |
| mull-runner-18 not found | distro package name varies by release | check `dpkg -L` for the mull package; alias in `~/.bashrc` |

## Rebuilding partially

Docker's layer cache preserves all steps that precede the one you
change. To bust only the Python layer (e.g., to update `atheris`):

```bash
docker build --no-cache-filter=atheris ...  # Docker 24+
```

Or bump the pin in the Dockerfile and rebuild normally — the intervening
cache layers are reused.
