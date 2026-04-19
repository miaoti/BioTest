"""
libclang AST walker — extracts public scalar-returning, nullary methods
of a named struct/class from a C or C++ public header file. Emits a
`MethodsManifest` JSON suitable for hand-off to the per-SUT dispatch
adapter generator.

Usage:
    py -3.12 -m harnesses._reflect.libclang_walker \
        --header path/to/pub.h \
        --type StructName \
        --sut-name my_c_parser \
        [--language c|cpp] \
        [--out manifest.json]

Reference:
- libclang Python binding: `pip install libclang` (bundles the LLVM .so / .dll
  on Windows / Linux / macOS).
- Clang documentation: https://clang.llvm.org/docs/LibClang.html

Limitations (documented in harnesses/c/README.md and harnesses/cpp/README.md):
- C: macros, static-inline functions, and #defined constants are invisible
  to libclang's pre-preprocessed AST walk.
- C++: templates, overloaded functions, SFINAE-gated members are not admitted —
  only concrete instantiations of zero-arg const member functions.
- ABI / struct layout stability across SUT library versions is the user's
  responsibility (pin a version in the SUT's CMake/Cargo manifest).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .manifest_schema import MethodDescriptor, MethodsManifest


# Scalar return type names the framework's deep_equal can compare cleanly.
# Match libclang's `Type.spelling` strings.
_SCALAR_C = frozenset({
    "void *",  # excluded (handled separately)
    "_Bool", "bool", "char", "signed char", "unsigned char",
    "short", "unsigned short", "int", "unsigned int", "long",
    "unsigned long", "long long", "unsigned long long",
    "float", "double", "long double", "size_t", "ssize_t",
    "int8_t", "uint8_t", "int16_t", "uint16_t",
    "int32_t", "uint32_t", "int64_t", "uint64_t",
    "const char *", "char *",  # C-strings
})


def _is_scalar_c(type_spelling: str) -> bool:
    s = type_spelling.strip()
    if s in ("void", "void *"):
        return False
    return s in _SCALAR_C or s.startswith("enum ")


def walk_c_header(
    header: Path,
    struct_name: str,
    sut_name: str,
    extra_args: Optional[list[str]] = None,
    limit: int = 50,
) -> MethodsManifest:
    """C variant: extract `Scalar fn(const struct StructName *)` functions
    declared in `header`. `extra_args` accepts clang flags (`-I…`, `-D…`)
    for SUTs with non-default include paths."""
    try:
        import clang.cindex  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "libclang Python binding not installed. "
            "Run: py -3.12 -m pip install libclang"
        ) from e

    args = ["-x", "c"] + list(extra_args or [])
    index = clang.cindex.Index.create()
    tu = index.parse(str(header), args=args)
    if tu is None:
        raise RuntimeError(f"libclang failed to parse {header}")

    methods: list[MethodDescriptor] = []
    target_pointer = f"const struct {struct_name} *"
    target_pointer2 = f"struct {struct_name} *"
    for cursor in tu.cursor.walk_preorder():
        if cursor.kind != clang.cindex.CursorKind.FUNCTION_DECL:
            continue
        name = cursor.spelling
        if not name or name.startswith("_"):
            continue
        ret = cursor.result_type.spelling
        if not _is_scalar_c(ret):
            continue
        params = list(cursor.get_arguments())
        if len(params) != 1:
            continue
        ptype = params[0].type.spelling
        if ptype not in (target_pointer, target_pointer2):
            continue
        methods.append(MethodDescriptor(
            name=name, returns=ret, args=[ptype], language="c",
        ))
        if len(methods) >= limit:
            break

    return MethodsManifest(
        sut_name=sut_name,
        record_type=f"struct {struct_name}",
        methods=methods,
    )


def walk_cpp_header(
    header: Path,
    class_name: str,
    sut_name: str,
    extra_args: Optional[list[str]] = None,
    limit: int = 50,
) -> MethodsManifest:
    """C++ variant: extract `public, const, zero-arg, scalar-returning`
    member functions of `class_name`. Templates / overloads are skipped
    by design — see header docstring."""
    try:
        import clang.cindex  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "libclang Python binding not installed. "
            "Run: py -3.12 -m pip install libclang"
        ) from e

    args = ["-x", "c++", "-std=c++20"] + list(extra_args or [])
    index = clang.cindex.Index.create()
    tu = index.parse(str(header), args=args)
    if tu is None:
        raise RuntimeError(f"libclang failed to parse {header}")

    methods: list[MethodDescriptor] = []
    seen: set[str] = set()
    for cursor in tu.cursor.walk_preorder():
        if cursor.kind != clang.cindex.CursorKind.CXX_METHOD:
            continue
        # Find owning class — must match the requested name.
        parent = cursor.semantic_parent
        if parent is None or parent.spelling != class_name:
            continue
        # Public + const + zero-arg + non-templated.
        if cursor.access_specifier != clang.cindex.AccessSpecifier.PUBLIC:
            continue
        if not cursor.is_const_method():
            continue
        if list(cursor.get_arguments()):
            continue
        # Templates surface as TEMPLATE_CXX_METHOD or have parameter list
        # — skip them defensively.
        try:
            num_t = cursor.get_num_template_arguments()
            if num_t > 0:
                continue
        except Exception:
            pass
        ret = cursor.result_type.spelling
        if not _is_scalar_c(ret) and not ret.startswith("std::string"):
            continue
        name = cursor.spelling
        if not name or name.startswith("_") or name in seen:
            continue
        seen.add(name)
        methods.append(MethodDescriptor(
            name=name, returns=ret, args=[], language="cpp",
        ))
        if len(methods) >= limit:
            break

    return MethodsManifest(
        sut_name=sut_name,
        record_type=class_name,
        methods=methods,
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--header", required=True, type=Path)
    parser.add_argument("--type", required=True, dest="type_name")
    parser.add_argument("--sut-name", required=True)
    parser.add_argument("--language", choices=["c", "cpp"], default="c")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output JSON path (default stdout).")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("clang_args", nargs="*",
                        help="Extra clang flags after `--`, e.g. -I…")
    args = parser.parse_args(argv)

    if args.language == "c":
        manifest = walk_c_header(
            args.header, args.type_name, args.sut_name,
            extra_args=args.clang_args, limit=args.limit,
        )
    else:
        manifest = walk_cpp_header(
            args.header, args.type_name, args.sut_name,
            extra_args=args.clang_args, limit=args.limit,
        )

    blob = manifest.model_dump_json(indent=2)
    if args.out:
        args.out.write_text(blob, encoding="utf-8")
    else:
        print(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
