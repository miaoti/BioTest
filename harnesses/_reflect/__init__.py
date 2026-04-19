"""
Shared reflection scaffolding for languages WITHOUT native runtime
reflection (C, C++, Rust). Framework-level code-gen pipeline that takes
the SUT's public headers (or rustdoc JSON) and emits a uniform
`methods_manifest.json` plus a per-SUT dispatch adapter.

Pipeline:

    SUT public headers (.h / .hpp)         rustdoc JSON output
            │                                       │
            └──► libclang AST walk ◄────────────────┘
                           │
                           ▼
           methods_manifest.json   (uniform Pydantic shape)
                           │
                           ▼
            adapter source (generated)
                           │
                           ▼
              compiled query binary
                           │
                           ▼
         biotest harness `--mode query` CLI

The walker / parser is shared across SUTs. A user onboarding a Rust SUT
points the generator at their crate; the framework produces the adapter.
No hand-written reflection logic per method.

References:
- Java + Python use native reflection (no codegen needed).
- C / C++: libclang (https://clang.llvm.org/docs/LibClang.html) — Python
  binding `pip install libclang`.
- Rust: `cargo rustdoc -- -Z unstable-options --output-format json`,
  RFC #2963 (rustdoc-json), tracked at
  https://github.com/rust-lang/rust/issues/76578.
"""
