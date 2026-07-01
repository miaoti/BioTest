"""Audit citation hygiene for the BioTest paper."""
import re
import pathlib

cited = set()
for p in pathlib.Path("documents/paper").rglob("*.tex"):
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\\cite[a-zA-Z]*\{([^}]+)\}", text):
        for k in m.group(1).split(","):
            cited.add(k.strip())

defined = set()
bib = pathlib.Path("documents/paper/biotest.bib").read_text(encoding="utf-8", errors="replace")
for m in re.finditer(r"@[a-zA-Z]+\{([^,]+),", bib):
    defined.add(m.group(1).strip())

print(f"cited: {len(cited)}, defined: {len(defined)}")
print()
orphans = cited - defined
unused = defined - cited
print(f"ORPHANED: {len(orphans)}")
for k in sorted(orphans):
    print("  " + k)
print()
print(f"UNUSED: {len(unused)}")
for k in sorted(unused):
    print("  " + k)
