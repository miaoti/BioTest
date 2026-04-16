# EvoSuite baseline

Search-based Java unit-test generator. Used here to benchmark against BioTest on **htsjdk only** (Java SUT).

## Version

`1.2.0` (latest stable as of 2023). Pinned in `compares/scripts/fetch_sources.sh`.

## Fetch

```
bash compares/scripts/fetch_sources.sh evosuite
```

This downloads `evosuite-1.2.0.jar` into `source/`. The JAR is a standalone executable — no build needed.

## Invocation (planned, to be scripted)

Target classes: the VCF/SAM I/O entry points of htsjdk, consistent with the coverage/mutation scope in `../../DESIGN.md` §5.

```
java -jar source/evosuite-1.2.0.jar \
  -class htsjdk.variant.vcf.VCFCodec \
  -projectCP <htsjdk fat JAR on classpath> \
  -Dsearch_budget=300 \
  -Dstopping_condition=MaxTime
```

Repeat for each target class. Output: JUnit test suite in `evosuite-tests/`. We then run that suite under JaCoCo for coverage metrics and under PIT for mutation scoring — both already configured in this repo (see `biotest_config.yaml: coverage` and `compares/mutation/pit/`).

## Notes

- EvoSuite generates **in-memory Java objects**, not VCF/SAM **files**. Validity Ratio as defined in DESIGN.md §3.1 is file-level; for EvoSuite we compute it by inspecting whether the generated test's constructed input would parse, i.e., by instrumenting VCFCodec/SAMRecord to dump the byte form and piping that through the reference parser.
- EvoSuite requires Java 11+; the project already uses Java via JaCoCo so the toolchain is in place.

## References

- https://www.evosuite.org/
- Fraser & Arcuri, *EvoSuite: Automatic Test Suite Generation for Object-Oriented Software*, FSE 2011.
