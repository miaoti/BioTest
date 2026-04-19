// Jazzer harness for htsjdk's SAM parsing path.
//
// Build: ./gradlew :harnesses:jazzer:jazzerHarness
// Run:   jazzer --cp=build/libs/biotest-jazzer.jar:... \
//              --target_class=SAMCodecFuzzer \
//              --instrumentation_includes=htsjdk.samtools.* \
//              -seed_corpus=../../../seeds/sam \
//              -max_total_time=7200 \
//              results_dir/
//
// Contract: same as VCFCodecFuzzer — expected SAM-parse exceptions are
// caught; everything else propagates as a Jazzer finding.

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;

import htsjdk.samtools.SAMRecord;
import htsjdk.samtools.SamInputResource;
import htsjdk.samtools.SamReader;
import htsjdk.samtools.SamReaderFactory;
import htsjdk.samtools.ValidationStringency;
import htsjdk.samtools.util.RuntimeIOException;

import java.io.ByteArrayInputStream;
import java.io.IOException;

public class SAMCodecFuzzer {

    @FuzzTest(maxDuration = "0")
    public static void fuzzSamParse(FuzzedDataProvider data) throws IOException {
        byte[] bytes = data.consumeRemainingAsBytes();
        if (bytes.length == 0) {
            return;
        }

        // SamReaderFactory handles both SAM and BAM; leave detection to htsjdk.
        SamReaderFactory factory = SamReaderFactory.makeDefault()
                .validationStringency(ValidationStringency.LENIENT);

        try (SamReader reader = factory.open(
                SamInputResource.of(new ByteArrayInputStream(bytes)))) {
            reader.getFileHeader();
            for (SAMRecord rec : reader) {
                // Force lazy field resolution.
                rec.getReadName();
                rec.getCigar();
                rec.getAlignmentStart();
                rec.getReadBases();
                rec.getBaseQualities();
                rec.getAttributes();
            }
        } catch (RuntimeIOException | IOException | IllegalArgumentException expected) {
            // Expected: malformed SAM / BAM input. Not a bug.
        }
    }
}
