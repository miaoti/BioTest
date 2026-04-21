// SAMMutationTest — SAM sibling of VCFMutationTest. Same baseline-
// compare shape, but parses via SamReaderFactory so PIT mutations
// inside `htsjdk.samtools::SAM,Sam` are reachable from the test.
//
// Mirrors BaselineBuilder.computeOutcome for fmt="SAM".

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

import org.junit.*;
import static org.junit.Assert.*;

import htsjdk.samtools.SAMRecord;
import htsjdk.samtools.SamInputResource;
import htsjdk.samtools.SamReader;
import htsjdk.samtools.SamReaderFactory;
import htsjdk.samtools.ValidationStringency;

public class SAMMutationTest {

    private static Path corpusDir;
    private static Map<String, String> baseline;

    @BeforeClass
    public static void loadBaseline() throws Exception {
        String corpusEnv = System.getenv("CORPUS_DIR");
        String baselineEnv = System.getenv("BASELINE_JSON");
        Assert.assertNotNull("CORPUS_DIR env must be set for PIT run", corpusEnv);
        Assert.assertNotNull("BASELINE_JSON env must be set for PIT run", baselineEnv);
        corpusDir = Paths.get(corpusEnv);
        baseline = VCFMutationTest.parseBaseline(Files.readString(Paths.get(baselineEnv)));
    }

    @Test
    public void allCorpusFilesMatchBaseline() throws Exception {
        List<String> mismatches = new ArrayList<>();
        try (Stream<Path> s = Files.list(corpusDir)) {
            for (Path file : (Iterable<Path>) s.filter(Files::isRegularFile).sorted()::iterator) {
                String observed = computeOutcome(file);
                String expected = baseline.get(file.getFileName().toString());
                if (expected == null) continue;
                if (!expected.equals(observed)) {
                    mismatches.add(file.getFileName() + " expected=" + expected
                                   + " observed=" + observed);
                    if (mismatches.size() >= 5) break;
                }
            }
        }
        assertTrue("Outcome diverged from baseline: " + mismatches,
                   mismatches.isEmpty());
    }

    static String computeOutcome(Path file) {
        try {
            byte[] bytes = Files.readAllBytes(file);
            SamReaderFactory factory = SamReaderFactory.makeDefault()
                    .validationStringency(ValidationStringency.LENIENT);
            try (SamReader reader = factory.open(
                    SamInputResource.of(new ByteArrayInputStream(bytes)))) {
                reader.getFileHeader();
                int count = 0;
                for (SAMRecord rec : reader) {
                    rec.getReadName();
                    rec.getCigar();
                    rec.getAlignmentStart();
                    rec.getReadBases();
                    rec.getBaseQualities();
                    rec.getAttributes();
                    count++;
                }
                return "ok:" + count;
            }
        } catch (Throwable t) {
            Throwable root = t;
            while (root.getCause() != null && root.getCause() != root) {
                root = root.getCause();
            }
            return "err:" + root.getClass().getName();
        }
    }
}
