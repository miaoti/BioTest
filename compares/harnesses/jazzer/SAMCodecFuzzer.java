// Jazzer harness for htsjdk's SAM parsing path.
//
// Build + run: see VCFCodecFuzzer.java for the build command and the
// reason we use the classic `fuzzerTestOneInput` entry signature
// instead of @FuzzTest.

import com.code_intelligence.jazzer.api.FuzzedDataProvider;

import htsjdk.samtools.SAMRecord;
import htsjdk.samtools.SamInputResource;
import htsjdk.samtools.SamReader;
import htsjdk.samtools.SamReaderFactory;
import htsjdk.samtools.ValidationStringency;
import htsjdk.samtools.util.RuntimeIOException;

import java.io.ByteArrayInputStream;
import java.io.IOException;

public class SAMCodecFuzzer {

    public static void fuzzerTestOneInput(FuzzedDataProvider data) throws IOException {
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
