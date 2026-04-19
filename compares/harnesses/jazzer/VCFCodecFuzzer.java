// Jazzer harness for htsjdk's VCF parsing path.
//
// Build: bash compares/scripts/build_harnesses.sh jazzer
// Run (from inside biotest-bench):
//   python3.12 compares/scripts/tool_adapters/run_jazzer.py \
//       --sut htsjdk --seed-corpus seeds/vcf \
//       --out-dir /tmp/jz-vcf --time-budget-s 60 --format VCF
//
// Entry point: the classic Jazzer static signature
// `public static void fuzzerTestOneInput(FuzzedDataProvider)`. We do NOT
// use `@FuzzTest` here because that annotation requires JUnit 5 on the
// classpath, which adds unnecessary weight to the harness jar and isn't
// how the standalone `jazzer` CLI discovers targets.
//
// Contract: given fuzzed bytes, write them to a temp file and drive the
// public VCFFileReader / VCFCodec plumbing end-to-end. We catch
// *expected* htsjdk exceptions (TribbleException, IOException,
// IllegalArgumentException) — those signal a legitimately malformed
// input, not a bug. Anything else (NPE, IndexOOB, assertion violation)
// propagates so Jazzer records it as a finding.

import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import htsjdk.tribble.TribbleException;
import htsjdk.variant.vcf.VCFFileReader;
import htsjdk.variant.variantcontext.VariantContext;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class VCFCodecFuzzer {

    public static void fuzzerTestOneInput(FuzzedDataProvider data) throws IOException {
        byte[] bytes = data.consumeRemainingAsBytes();
        if (bytes.length == 0) {
            return;
        }

        // htsjdk's VCFFileReader is file-based; write to temp and let
        // the Codec + Tribble plumbing drive the full parse.
        Path tmp = Files.createTempFile("jazzer-vcf-", ".vcf");
        try {
            Files.write(tmp, bytes,
                    StandardOpenOption.TRUNCATE_EXISTING,
                    StandardOpenOption.WRITE);

            // requireIndex=false: Tribble's in-memory codec pathway.
            try (VCFFileReader reader = new VCFFileReader(tmp, false)) {
                reader.getFileHeader();
                for (VariantContext vc : reader) {
                    vc.getAlleles();
                    vc.getAttributes();
                    vc.getGenotypes();
                    vc.getType();
                }
            }
        } catch (TribbleException | IOException | IllegalArgumentException expected) {
            // Expected: malformed input. Not a bug.
        } finally {
            try {
                Files.deleteIfExists(tmp);
            } catch (IOException ignored) {
                // Best-effort temp cleanup.
            }
        }
    }
}
