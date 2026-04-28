// PerFileCoverageProbe — measures per-file line coverage of the SUT's
// parse path, so corpus_coverage_select.py can greedy-pick a coverage-
// maximal subset before PIT runs.
//
// SUT-agnostic within Java: any Java SUT that has a one-argument
// computeOutcome(Path) static method in a JUnit harness class can be
// probed. Currently points at VCFMutationTest / SAMMutationTest for
// htsjdk, but the same mechanism extends to any JaCoCo-instrumented
// Java project by compiling a sibling harness class with the same
// computeOutcome(Path) contract and passing its classname as the
// --harness argument.
//
// Invocation (via phase3_jazzer_pit.sh integration):
//
//     java -javaagent:jacocoagent.jar=destfile=/dev/null,dumponexit=false \
//          -cp <classpath> PerFileCoverageProbe \
//          --format SAM \
//          --harness SAMMutationTest \
//          --corpus <dir>/ \
//          --classes <dir>/ \
//          --out <out>/perfile_coverage.json
//
// Output: a JSON object {filename: [list of "classname:lineNumber"]}
// that corpus_coverage_select.py consumes as per-file coverage.

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

import org.jacoco.agent.rt.RT;
import org.jacoco.agent.rt.IAgent;
import org.jacoco.core.analysis.Analyzer;
import org.jacoco.core.analysis.CoverageBuilder;
import org.jacoco.core.analysis.IClassCoverage;
import org.jacoco.core.analysis.ICounter;
import org.jacoco.core.data.ExecutionDataReader;
import org.jacoco.core.data.ExecutionDataStore;
import org.jacoco.core.data.SessionInfoStore;

public class PerFileCoverageProbe {

    public static void main(String[] args) throws Exception {
        String format = null;
        String harnessClass = null;
        Path corpusDir = null;
        Path classesDir = null;
        Path outPath = null;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--format":  format = args[++i]; break;
                case "--harness": harnessClass = args[++i]; break;
                case "--corpus":  corpusDir = Paths.get(args[++i]); break;
                case "--classes": classesDir = Paths.get(args[++i]); break;
                case "--out":     outPath = Paths.get(args[++i]); break;
                default:
                    throw new IllegalArgumentException("unknown arg: " + args[i]);
            }
        }
        if (format == null || harnessClass == null || corpusDir == null
                || classesDir == null || outPath == null) {
            System.err.println(
                "usage: PerFileCoverageProbe --format <VCF|SAM> --harness "
                + "<ClassName> --corpus <dir> --classes <dir> --out <file>");
            System.exit(2);
        }

        Class<?> harness = Class.forName(harnessClass);
        Method computeOutcome = harness.getDeclaredMethod("computeOutcome", Path.class);
        computeOutcome.setAccessible(true);

        IAgent agent;
        try {
            agent = RT.getAgent();
        } catch (Throwable t) {
            System.err.println("JaCoCo agent not attached; start JVM with "
                    + "-javaagent:jacocoagent.jar=output=none");
            throw new RuntimeException(t);
        }

        List<Path> files = new ArrayList<>();
        try (DirectoryStream<Path> ds = Files.newDirectoryStream(corpusDir)) {
            for (Path p : ds) {
                if (Files.isRegularFile(p)) files.add(p);
            }
        }
        Collections.sort(files);

        // Snapshot compiled class bytes once so per-file analysis is fast.
        List<byte[]> classBytes = new ArrayList<>();
        List<String> classPaths = new ArrayList<>();
        Files.walk(classesDir)
             .filter(p -> p.toString().endsWith(".class"))
             .forEach(p -> {
                 try {
                     classBytes.add(Files.readAllBytes(p));
                     classPaths.add(p.toString());
                 } catch (IOException ignored) {}
             });
        System.err.println("probe: " + files.size() + " corpus files, "
                + classBytes.size() + " classes to analyse");

        // Prime the JVM once so first-file coverage doesn't include class
        // loading of harness + htsjdk — we only want parse-path lines.
        if (!files.isEmpty()) {
            try { computeOutcome.invoke(null, files.get(0)); } catch (Throwable ignored) {}
        }

        try (Writer w = new OutputStreamWriter(
                Files.newOutputStream(outPath), StandardCharsets.UTF_8)) {
            w.write("{\n");
            boolean firstFile = true;
            int idx = 0;
            for (Path f : files) {
                idx++;
                agent.reset();
                try { computeOutcome.invoke(null, f); }
                catch (Throwable t) { /* parse error → count as reach for JaCoCo */ }

                byte[] execData = agent.getExecutionData(false);
                ExecutionDataStore eds = new ExecutionDataStore();
                SessionInfoStore sis = new SessionInfoStore();
                try (ByteArrayInputStream bis = new ByteArrayInputStream(execData)) {
                    ExecutionDataReader r = new ExecutionDataReader(bis);
                    r.setSessionInfoVisitor(sis);
                    r.setExecutionDataVisitor(eds);
                    r.read();
                }
                CoverageBuilder cb = new CoverageBuilder();
                Analyzer a = new Analyzer(eds, cb);
                for (int i = 0; i < classBytes.size(); i++) {
                    try { a.analyzeClass(classBytes.get(i), classPaths.get(i)); }
                    catch (IOException ignored) {}
                }

                List<String> hits = new ArrayList<>();
                for (IClassCoverage cc : cb.getClasses()) {
                    int first = cc.getFirstLine();
                    int last = cc.getLastLine();
                    if (first < 0) continue;
                    for (int line = first; line <= last; line++) {
                        int status = cc.getLine(line).getStatus();
                        if (status == ICounter.FULLY_COVERED
                                || status == ICounter.PARTLY_COVERED) {
                            hits.add(cc.getName() + ":" + line);
                        }
                    }
                }

                if (!firstFile) w.write(",\n");
                firstFile = false;
                w.write("  \"" + f.getFileName() + "\": [");
                for (int i = 0; i < hits.size(); i++) {
                    if (i > 0) w.write(",");
                    w.write("\"" + hits.get(i) + "\"");
                }
                w.write("]");

                if (idx % 25 == 0) {
                    System.err.println("  probed " + idx + "/" + files.size()
                            + " (last file " + hits.size() + " lines)");
                }
            }
            w.write("\n}\n");
        }
        System.err.println("probe done: " + files.size() + " files → " + outPath);
    }
}
