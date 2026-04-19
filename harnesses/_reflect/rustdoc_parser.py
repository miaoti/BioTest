"""
rustdoc-JSON parser — extracts public scalar-returning methods of a
named type from `cargo rustdoc --output-format json` output.

Usage:
    # Step 1: produce the rustdoc JSON for the SUT crate
    cargo +nightly rustdoc -- -Zunstable-options --output-format json
    # Output appears under target/doc/<crate_name>.json

    # Step 2: parse it
    py -3.12 -m harnesses._reflect.rustdoc_parser \
        --rustdoc-json target/doc/my_parser.json \
        --type my_parser::Record \
        --sut-name my_rust_parser \
        [--out manifest.json]

Reference:
- rustdoc JSON format RFC: https://rust-lang.github.io/rfcs/2963-rustdoc-json.html
- Tracking issue: https://github.com/rust-lang/rust/issues/76578
- As of 2025 the format is nightly-only; expected to stabilize in 2026.
  Once stable, drop the `+nightly` requirement.

Method-admission filter:
- `&self` only (no `&mut self`, no associated functions)
- Zero non-self parameters
- Returns one of: `bool`, signed/unsigned int (any width), `f32`, `f64`,
  `String`, `&str`, `Option<T>` for any of those
- Public visibility (rustdoc emits private items only with --document-private-items)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

from .manifest_schema import MethodDescriptor, MethodsManifest


# Type kinds rustdoc emits in `inner.function.decl.output` that we admit.
_RUST_SCALAR_PRIM = frozenset({
    "bool", "char",
    "i8", "i16", "i32", "i64", "i128", "isize",
    "u8", "u16", "u32", "u64", "u128", "usize",
    "f32", "f64", "str",
})


def _type_to_string(t: Any) -> str:
    """Render a rustdoc-json type node to a best-effort display string."""
    if not isinstance(t, dict):
        return repr(t)
    if "primitive" in t:
        return t["primitive"]
    if "resolved_path" in t:
        path = t["resolved_path"].get("name") or t["resolved_path"].get("path", "?")
        return path
    if "borrowed_ref" in t:
        inner = t["borrowed_ref"].get("type", {})
        return f"&{_type_to_string(inner)}"
    if "generic" in t:
        return t["generic"]
    return "Unknown"


def _is_scalar_rust(t: Any) -> bool:
    if not isinstance(t, dict):
        return False
    if "primitive" in t:
        return t["primitive"] in _RUST_SCALAR_PRIM
    if "borrowed_ref" in t:
        return _is_scalar_rust(t["borrowed_ref"].get("type", {}))
    if "resolved_path" in t:
        rp = t["resolved_path"]
        name = rp.get("name", "")
        if name == "String":
            return True
        if name == "Option":
            args = rp.get("args", {}).get("angle_bracketed", {}).get("args", [])
            if args and "type" in args[0]:
                return _is_scalar_rust(args[0]["type"])
        return False
    return False


def parse_rustdoc(
    json_blob: dict,
    type_name: str,
    sut_name: str,
    limit: int = 50,
) -> MethodsManifest:
    """Walk the rustdoc index, find the impl(s) for `type_name`, extract
    matching public methods. `type_name` is the SHORT type name (rustdoc
    JSON identifies items by short name within the crate's namespace)."""
    index = json_blob.get("index", {})

    # 1. Find the type's id.
    target_id: Optional[str] = None
    for item_id, item in index.items():
        if item.get("name") != type_name:
            continue
        kind = item.get("kind") or (item.get("inner", {}).get("kind"))
        if kind in ("struct", "enum"):
            target_id = item_id
            break
    if target_id is None:
        return MethodsManifest(sut_name=sut_name, record_type=type_name, methods=[])

    target = index[target_id]
    impl_ids: list[str] = []
    inner = target.get("inner", {})
    # rustdoc-json shape: struct/enum item has impls list under inner.
    for variant_key in ("struct", "enum"):
        if variant_key in inner:
            impl_ids.extend(inner[variant_key].get("impls", []))

    methods: list[MethodDescriptor] = []
    for impl_id in impl_ids:
        impl_item = index.get(impl_id)
        if impl_item is None:
            continue
        if impl_item.get("inner", {}).get("impl", {}).get("trait") is not None:
            continue  # skip trait impls (Debug, Clone, …)
        for fn_id in impl_item.get("inner", {}).get("impl", {}).get("items", []):
            fn = index.get(fn_id)
            if fn is None or fn.get("name") is None:
                continue
            if fn.get("visibility") not in ("public", None):
                continue
            fn_inner = fn.get("inner", {}).get("function", {})
            if not fn_inner:
                continue
            decl = fn_inner.get("decl", {})
            inputs = decl.get("inputs", [])
            # Must have exactly one input: &self
            if len(inputs) != 1:
                continue
            self_name, self_ty = inputs[0]
            if self_name != "self":
                continue
            # Reject &mut self (would be borrowed_ref with mutable flag)
            if isinstance(self_ty, dict) and "borrowed_ref" in self_ty:
                if self_ty["borrowed_ref"].get("mutable"):
                    continue
            output = decl.get("output")
            if output is None:
                continue
            if not _is_scalar_rust(output):
                continue
            methods.append(MethodDescriptor(
                name=fn["name"],
                returns=_type_to_string(output),
                args=[],
                language="rust",
            ))
            if len(methods) >= limit:
                break
        if len(methods) >= limit:
            break

    return MethodsManifest(
        sut_name=sut_name, record_type=type_name, methods=methods,
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--rustdoc-json", required=True, type=Path)
    parser.add_argument("--type", required=True, dest="type_name")
    parser.add_argument("--sut-name", required=True)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)

    blob = json.loads(args.rustdoc_json.read_text(encoding="utf-8"))
    manifest = parse_rustdoc(
        blob,
        # Use the SHORT type name — rustdoc indexes items by short name
        # within the crate. Strip any "crate::" or "module::" prefix.
        args.type_name.rsplit("::", 1)[-1],
        args.sut_name,
        limit=args.limit,
    )
    out_blob = manifest.model_dump_json(indent=2)
    if args.out:
        args.out.write_text(out_blob, encoding="utf-8")
    else:
        print(out_blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
