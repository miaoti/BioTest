// Jazzer harness for htsjdk's VCF parsing path.
//
// Build: ./gradlew :harnesses:jazzer:jazzerHarness
// Run:   jazzer --cp=build/libs/biotest-jazzer.jar:... \
//              --target_class=VCFCodecFuzzer \
//              --instrumentation_includes=htsjdk.variant.vcf.*,htsjdk.variant.variantcontext.* \
//              -seed_corpus=../../../seeds/vcf \
//              -max_total_time=7200 \
//              results_dir/
//
// Contract: given a byte stream, write it to a temp file and drive the
// SUT's public file-level entry points end-to-end. We catch *expected*
// htsjdk exceptions (TribbleException, IOException) — those signal a
// legitimately malformed input, not a bug. Anything else (NPE,
// IndexOOB, ClassCast, assertion violation) propagates and Jazzer
// records it as a finding.

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;

import htsjdk.tribble.TribbleException;
import htsjdk.variant.vcf.VCFFileReader;
import htsjdk.variant.vcf.VCFCodec;
import htsjdk.variant.variantcontext.VariantContext;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class VCFCodecFuzzer {

    @FuzzTest(maxDuration = "0")
    public static void fuzzVcfParse(FuzzedDataProvider data) throws IOException {
        byte[] bytes = data.consumeRemainingAsBytes();
        if (bytes.length == 0) {
            return;
        }

        // htsjdk's VCFFileReader is file-based; write to temp and let
        // the Codec+Tribble plumbing drive the full parse.
        Path tmp = Files.createTempFile("jazzer-vcf-", ".vcf");
        try {
            Files.write(tmp, bytes,
                    StandardOpenOption.TRUNCATE_EXISTING,
                    StandardOpenOption.WRITE);

            // requireIndex=false: Tribble's in-memory codec pathway.
            try (VCFFileReader reader = new VCFFileReader(tmp, false)) {
                // Force full read of header + every record.
                reader.getFileHeader();
                for (VariantContext vc : reader) {
                    // Drain side-effects that trigger lazy parsing.
                    vc.getAlleles();
                    vc.getAttributes();
                    vc.getGenotypes();
                    vc.getType();
                }
            }
        } catch (TribbleException | IOException expected) {
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
