// BaselineBuilder — single-shot tool that walks a directory of VCF or
// SAM files and records each file's parse OUTCOME under unmutated
// htsjdk. The outcome string is later the expected value that
// MutationTest asserts against; PIT kills a mutant whenever any file's
// observed outcome diverges from the baseline.
//
// Outcome format (one per file):
//     "ok:<recordCount>"            parser succeeded, N records seen
//     "err:<ExceptionClassName>"    parser threw; we record the
//                                   top-level exception class so the
//                                   assertion is exception-class-level
//                                   sensitive (IOException stays
//                                   IOException; mutants that turn an
//                                   expected IOException into an NPE
//                                   flip the outcome string → killed).
//
// Output: a flat JSON map `{"<filename>": "<outcome>", ...}` written
// to the path given as argv[2]. JSON encoding is hand-rolled (one
// dependency less in the classpath we hand to PIT).
//
// CLI:
//     java BaselineBuilder {VCF|SAM} <corpus_dir> <out_json>

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

import htsjdk.variant.vcf.VCFFileReader;
import htsjdk.variant.variantcontext.VariantContext;

import htsjdk.samtools.SAMRecord;
import htsjdk.samtools.SamInputResource;
import htsjdk.samtools.SamReader;
import htsjdk.samtools.SamReaderFactory;
import htsjdk.samtools.ValidationStringency;

public class BaselineBuilder {

    public static void main(String[] args) throws Exception {
        if (args.length < 3) {
            System.err.println("usage: BaselineBuilder {VCF|SAM} <corpus_dir> <out_json>");
            System.exit(2);
        }
        String fmt = args[0].toUpperCase();
        Path corpusDir = Paths.get(args[1]);
        Path outJson = Paths.get(args[2]);

        Map<String, String> outcomes = new LinkedHashMap<>();
        try (Stream<Path> s = Files.list(corpusDir)) {
            s.filter(Files::isRegularFile).sorted().forEach(file -> {
                outcomes.put(file.getFileName().toString(), computeOutcome(fmt, file));
            });
        }

        Files.writeString(outJson, toJson(outcomes));
        System.err.println("[baseline] wrote " + outJson + " (" + outcomes.size() + " files)");
    }

    /** Compute the canonical outcome string for one corpus file.
     *  Same parse invocation as {VCF,SAM}CodecFuzzer but without
     *  FuzzedDataProvider wrapping — feed the raw bytes straight to
     *  the reader. All exceptions (except the ones the real Jazzer
     *  harness catches) are turned into "err:<class>" strings; a
     *  mutant that changes the exception CLASS is killed.
     */
    static String computeOutcome(String fmt, Path file) {
        try {
            if ("VCF".equals(fmt)) {
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
                }
            }
            if ("SAM".equals(fmt)) {
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
            }
            throw new IllegalArgumentException("unknown format " + fmt);
        } catch (Throwable t) {
            // Record the most specific exception class. Include causes
            // so that e.g. a RuntimeIOException wrapping an IOException
            // still distinguishes flips.
            Throwable root = t;
            while (root.getCause() != null && root.getCause() != root) {
                root = root.getCause();
            }
            return "err:" + root.getClass().getName();
        }
    }

    /** Minimal JSON encoder for a flat Map<String,String>. We control
     *  both ends (writer here, reader in MutationTest), so quoting is
     *  restricted to `\\`, `"`, newline; nothing fancier. */
    static String toJson(Map<String, String> m) {
        StringBuilder sb = new StringBuilder("{\n");
        int i = 0, n = m.size();
        for (Map.Entry<String, String> e : m.entrySet()) {
            sb.append("  ").append(quote(e.getKey())).append(": ")
              .append(quote(e.getValue()));
            if (++i < n) sb.append(',');
            sb.append('\n');
        }
        sb.append("}\n");
        return sb.toString();
    }

    static String quote(String s) {
        StringBuilder sb = new StringBuilder("\"");
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': sb.append("\\\\"); break;
                case '"':  sb.append("\\\""); break;
                case '\n': sb.append("\\n");  break;
                case '\r': sb.append("\\r");  break;
                case '\t': sb.append("\\t");  break;
                default:
                    if (c < 0x20) sb.append(String.format("\\u%04x", (int) c));
                    else sb.append(c);
            }
        }
        sb.append("\"");
        return sb.toString();
    }
}
