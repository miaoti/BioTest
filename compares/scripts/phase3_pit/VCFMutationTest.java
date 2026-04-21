// VCFMutationTest — the PIT-driven JUnit 4 test that, for each file in
// CORPUS_DIR, asserts the htsjdk parser's outcome matches the pre-
// computed unmutated baseline under BASELINE_JSON. Baseline is the
// flat `{"filename": "<outcome>"}` JSON produced by BaselineBuilder.
//
// Why this shape? PIT's kill rule is "test passed on unmutated code,
// fails on mutated code." If we encode the outcome into a string and
// assert equality per file, any semantic change in htsjdk's VCF parse
// path — different record count, different exception class, new crash
// — flips at least one file's observed outcome, the test fails, and
// PIT counts the mutant as killed.
//
// We batch all N files into ONE @Test method so PIT only pays the JVM
// fork cost once per mutant (N-per-mutant @ParameterizedTest blows up
// the runtime at 1000+ files × thousands of mutants).
//
// Env config (CORPUS_DIR, BASELINE_JSON) is read at @BeforeClass time;
// the test reads it lazily so PIT's forked JVM inherits whatever env
// the outer `pitest-command-line.jar` runner got.

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

import org.junit.*;
import static org.junit.Assert.*;

import htsjdk.variant.vcf.VCFFileReader;
import htsjdk.variant.variantcontext.VariantContext;

public class VCFMutationTest {

    private static Path corpusDir;
    private static Map<String, String> baseline;

    @BeforeClass
    public static void loadBaseline() throws Exception {
        String corpusEnv = System.getenv("CORPUS_DIR");
        String baselineEnv = System.getenv("BASELINE_JSON");
        Assert.assertNotNull("CORPUS_DIR env must be set for PIT run", corpusEnv);
        Assert.assertNotNull("BASELINE_JSON env must be set for PIT run", baselineEnv);
        corpusDir = Paths.get(corpusEnv);
        baseline = parseBaseline(Files.readString(Paths.get(baselineEnv)));
    }

    @Test
    public void allCorpusFilesMatchBaseline() throws Exception {
        List<String> mismatches = new ArrayList<>();
        try (Stream<Path> s = Files.list(corpusDir)) {
            for (Path file : (Iterable<Path>) s.filter(Files::isRegularFile).sorted()::iterator) {
                String observed = computeOutcome(file);
                String expected = baseline.get(file.getFileName().toString());
                if (expected == null) continue;  // new file since baseline — skip
                if (!expected.equals(observed)) {
                    mismatches.add(file.getFileName() + " expected=" + expected
                                   + " observed=" + observed);
                    if (mismatches.size() >= 5) break;  // fail fast
                }
            }
        }
        assertTrue("Outcome diverged from baseline: " + mismatches,
                   mismatches.isEmpty());
    }

    /** Parse one file under *current* htsjdk (mutated or not). Mirrors
     *  BaselineBuilder.computeOutcome exactly — same VCFFileReader
     *  construction + iteration. */
    static String computeOutcome(Path file) {
        try (VCFFileReader reader = new VCFFileReader(file, false)) {
            reader.getFileHeader();
            int count = 0;
            for (VariantContext vc : reader) {
                vc.getAlleles();
                vc.getAttributes();
                vc.getGenotypes();
                vc.getType();
                count++;
            }
            return "ok:" + count;
        } catch (Throwable t) {
            Throwable root = t;
            while (root.getCause() != null && root.getCause() != root) {
                root = root.getCause();
            }
            return "err:" + root.getClass().getName();
        }
    }

    /** Tiny hand-rolled JSON-object parser for the `{"k":"v",...}`
     *  shape BaselineBuilder emits. Not general-purpose — it trusts
     *  the format it parses. Keeps the test classpath free of jackson
     *  / gson. */
    static Map<String, String> parseBaseline(String s) {
        Map<String, String> m = new LinkedHashMap<>();
        int i = s.indexOf('{');
        if (i < 0) throw new IllegalStateException("no JSON object start");
        i++;
        while (i < s.length()) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == '}') break;
            if (s.charAt(i) != '"') throw new IllegalStateException("expected key string at " + i);
            int ke = findCloseQuote(s, i + 1);
            String k = unescape(s.substring(i + 1, ke));
            i = ke + 1;
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (s.charAt(i) != ':') throw new IllegalStateException("expected ':' at " + i);
            i++;
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (s.charAt(i) != '"') throw new IllegalStateException("expected value string at " + i);
            int ve = findCloseQuote(s, i + 1);
            String v = unescape(s.substring(i + 1, ve));
            m.put(k, v);
            i = ve + 1;
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ',') { i++; continue; }
            if (i < s.length() && s.charAt(i) == '}') break;
        }
        return m;
    }

    static int findCloseQuote(String s, int start) {
        int i = start;
        while (i < s.length()) {
            char c = s.charAt(i);
            if (c == '\\') { i += 2; continue; }
            if (c == '"') return i;
            i++;
        }
        throw new IllegalStateException("unterminated string starting at " + start);
    }

    static String unescape(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '\\' && i + 1 < s.length()) {
                char n = s.charAt(++i);
                switch (n) {
                    case '"':  sb.append('"');  break;
                    case '\\': sb.append('\\'); break;
                    case 'n':  sb.append('\n'); break;
                    case 'r':  sb.append('\r'); break;
                    case 't':  sb.append('\t'); break;
                    case 'u':
                        sb.append((char) Integer.parseInt(s.substring(i + 1, i + 5), 16));
                        i += 4;
                        break;
                    default: sb.append(n);
                }
            } else sb.append(c);
        }
        return sb.toString();
    }
}
