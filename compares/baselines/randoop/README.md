# Randoop baseline

Feedback-directed random unit-test generation for Java. Used on **htsjdk only**.

## Version

`4.3.3` (2024). Pinned in fetch script.

## Fetch

```
bash compares/scripts/fetch_sources.sh randoop
```

Downloads `randoop-all-4.3.3.jar` into `source/` (the `-all` JAR bundles all transitive deps — single-artifact invocation).

## Invocation (planned)

```
java -cp source/randoop-all-4.3.3.jar:<htsjdk fat JAR> \
  randoop.main.Main gentests \
  --classlist=classlist.txt \
  --time-limit=300 \
  --output-tests=ALL \
  --junit-output-dir=randoop-tests
```

`classlist.txt` contains the same VCF/SAM-relevant htsjdk classes used for EvoSuite (see `../evosuite/README.md`).

Output: JUnit classes in `randoop-tests/`, then routed through JaCoCo + PIT like EvoSuite.

## Notes

- Randoop's feedback loop kills inputs that immediately crash the constructor; this is exactly the behavior we want for validity-ratio measurement — it will naturally produce a higher floor than pure random but (expectation) a lower one than BioTest's spec-grounded generation.
- Same Java-only limitation as EvoSuite: cannot target biopython / seqan3 / pysam.

## References

- https://randoop.github.io/randoop/
- Pacheco & Ernst, *Randoop: Feedback-Directed Random Testing for Java*, OOPSLA 2007 Companion.
