# Phase 4 post-run review

- records_total: 76
- detected_total: 17
- null_silences_total: 0

## Per-cell (tool/sut) detection counts

| cell | total | detected |
| :--- | ---: | ---: |
| atheris/biopython | 1 | 0 |
| atheris/vcfpy | 7 | 0 |
| cargo_fuzz/noodles | 6 | 0 |
| evosuite_anchor/htsjdk | 12 | 4 |
| jazzer/htsjdk | 12 | 12 |
| libfuzzer/seqan3 | 6 | 1 |
| pure_random/biopython | 1 | 0 |
| pure_random/htsjdk | 12 | 0 |
| pure_random/noodles | 6 | 0 |
| pure_random/seqan3 | 6 | 0 |
| pure_random/vcfpy | 7 | 0 |

## Spot-check replays

| tool | bug | sut | post_fix_success |
| :--- | :--- | :--- | :--- |
| evosuite_anchor | htsjdk-1389 | htsjdk | None |
| jazzer | htsjdk-1401 | htsjdk | None |
| libfuzzer | seqan3-3269 | seqan3 | None |
