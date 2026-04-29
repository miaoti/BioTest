import htsjdk.samtools.*;
import htsjdk.samtools.util.CloseableIterator;
import htsjdk.variant.variantcontext.*;
import htsjdk.variant.variantcontext.writer.*;
import htsjdk.variant.vcf.*;

import java.io.*;
import java.lang.reflect.Method;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

/**
 * BioTest Canonical JSON Harness for HTSJDK.
 *
 * Usage:
 *   java -jar biotest-harness.jar VCF|SAM <file_path>
 *     → emits canonical JSON to stdout (default parse mode).
 *
 *   java -jar biotest-harness.jar --mode write_roundtrip VCF|SAM <file_path>
 *     → parses the file, writes it back out via htsjdk's native writer
 *       (VariantContextWriter for VCF, SAMFileWriterFactory for SAM),
 *       and emits the rewritten TEXT to stdout. Used by the generic
 *       `sut_write_roundtrip` transform in the MR arsenal. Writer /
 *       encoder coverage that shows up is the natural consequence of
 *       an MR using this mode — not a coverage hack.
 *
 * Exit code 0 = success, 1 = error.
 */
public class BioTestHarness {

    public static void main(String[] args) {
        if (args.length == 0) {
            System.err.println("Usage: BioTestHarness VCF|SAM <file_path>");
            System.err.println("   or: BioTestHarness --mode write_roundtrip VCF|SAM <file_path>");
            System.exit(1);
        }

        // Parse --mode <name> + optional --writer-variant + --methods +
        // positional args. Keeps backward compat: old two-positional-arg
        // invocations still route to parse mode.
        String mode = "parse";
        String writerVariant = "standard";      // VCF write-roundtrip only
        String methodsArg = "";                  // Rank 5: comma-list of method names
        List<String> positional = new ArrayList<>();
        for (int i = 0; i < args.length; i++) {
            if ("--mode".equals(args[i]) && i + 1 < args.length) {
                mode = args[i + 1];
                i++;
            } else if ("--writer-variant".equals(args[i]) && i + 1 < args.length) {
                writerVariant = args[i + 1];
                i++;
            } else if ("--methods".equals(args[i]) && i + 1 < args.length) {
                methodsArg = args[i + 1];
                i++;
            } else {
                positional.add(args[i]);
            }
        }

        try {
            if ("strict_parse".equals(mode)) {
                // 2026-04-25: bug-bench-only strict-validation mode.
                // The default "parse" mode uses ValidationStringency.SILENT
                // because Phase C runs synthetic / mutated seeds and we
                // don't want every cross-voter test to fail on header
                // pedantry. For real-bug-benchmark cells, however, we
                // WANT strict validation — htsjdk-1561 specifically is
                // "post-fix added strict tag-length validation"; in
                // SILENT mode both pre and post versions silently
                // accept and the bug is invisible.
                //
                // CLI:  --mode strict_parse <VCF|SAM> <file_path>
                // Exits 0 iff the file parses cleanly under STRICT
                // validation, non-zero with the rejection on stderr.
                if (positional.size() < 2) {
                    System.err.println(
                        "--mode strict_parse requires <VCF|SAM> <file_path>");
                    System.exit(1);
                }
                String spFormat = positional.get(0).toUpperCase();
                String spPath = positional.get(1);
                try {
                    if ("VCF".equals(spFormat)) {
                        // VCF strict parse — htsjdk's VCFFileReader has
                        // its own validation handled by the codec; we
                        // iterate every record so any deferred
                        // validation surfaces.
                        try (htsjdk.variant.vcf.VCFFileReader vr =
                                new htsjdk.variant.vcf.VCFFileReader(
                                    java.nio.file.Path.of(spPath), false)) {
                            for (htsjdk.variant.variantcontext.VariantContext _v : vr) { /* iterate */ }
                        }
                    } else if ("SAM".equals(spFormat)) {
                        SamReaderFactory f = SamReaderFactory.makeDefault()
                            .validationStringency(ValidationStringency.STRICT);
                        try (SamReader r = f.open(new java.io.File(spPath))) {
                            r.getFileHeader();
                            for (SAMRecord _x : r) { /* iterate */ }
                        }
                    } else {
                        System.err.println(
                            "--mode strict_parse: unknown format " + spFormat);
                        System.exit(1);
                    }
                    System.exit(0);
                } catch (Throwable t) {
                    System.err.println(
                        "strict_parse rejected: " + t.getClass().getSimpleName()
                        + ": " + t.getMessage());
                    System.exit(2);
                }
                return;
            }

            if ("write_roundtrip".equals(mode)) {
                // CLI grammar:
                //   --mode write_roundtrip <VCF|SAM> <file_path>
                //     [--writer-variant {standard|advanced}]   (VCF only)
                //
                // Legacy single-arg form — <vcf_path> only — is kept for
                // backward compat with older Python callers.
                //
                // writer-variant selects which writer plumbing to exercise
                // on VCF: "standard" is the minimal clearOptions() path;
                // "advanced" keeps default options + .buffered() so
                // AsyncVariantContextWriter and the IndexCreator branches
                // of VariantContextWriterBuilder get covered. See the
                // comment on writeRoundtripVcf() for details.
                if (positional.isEmpty()) {
                    System.err.println(
                        "--mode write_roundtrip requires <VCF|SAM> <file_path>");
                    System.exit(1);
                }
                String rtFormat;
                String rtPath;
                if (positional.size() >= 2) {
                    rtFormat = positional.get(0).toUpperCase();
                    rtPath = positional.get(1);
                } else {
                    // Legacy: single positional → assume VCF
                    rtFormat = "VCF";
                    rtPath = positional.get(0);
                }
                if ("VCF".equals(rtFormat)) {
                    System.out.print(writeRoundtripVcf(rtPath, writerVariant));
                } else if ("SAM".equals(rtFormat)) {
                    System.out.print(writeRoundtripSam(rtPath));
                } else {
                    System.err.println(
                        "--mode write_roundtrip: unknown format " + rtFormat);
                    System.exit(1);
                }
                return;
            }

            if ("discover_methods".equals(mode)) {
                // Rank 5 (Chen-Kuo-Liu-Tse 2018 §3.2; MR-Scout TOSEM 2024).
                // CLI:  --mode discover_methods <VCF|SAM>
                //
                // Emits JSON {"methods": [{"name": str, "returns": str,
                // "args": []}, ...]} listing public scalar-returning,
                // zero-param methods on htsjdk's parsed-record class
                // (VariantContext for VCF, SAMRecord for SAM). Used by
                // HTSJDKRunner.discover_query_methods to feed the
                // Phase B prompt with the LIVE htsjdk API surface.
                if (positional.isEmpty()) {
                    System.err.println(
                        "--mode discover_methods requires <VCF|SAM>");
                    System.exit(1);
                }
                String dFmt = positional.get(0).toUpperCase();
                Class<?> cls;
                if ("VCF".equals(dFmt)) {
                    cls = VariantContext.class;
                } else if ("SAM".equals(dFmt)) {
                    cls = SAMRecord.class;
                } else {
                    System.err.println("Unknown format: " + dFmt);
                    System.exit(1);
                    return;
                }
                System.out.print(discoverMethodsJson(cls));
                return;
            }

            if ("discover_mutators".equals(mode)) {
                // Tier 2b (twinkly-finding-swan plan): mirror of
                // discover_methods that surfaces the MUTATOR surface
                // (set/add/remove/clear/put/reset prefixes; void or
                // fluent return). Catalog is prompt-only — the LLM
                // composes mutator-chain MRs that wrap inside the
                // existing sut_write_roundtrip oracle, so soundness
                // is preserved (no new transform family).
                //
                // CLI:  --mode discover_mutators <VCF|SAM>
                if (positional.isEmpty()) {
                    System.err.println(
                        "--mode discover_mutators requires <VCF|SAM>");
                    System.exit(1);
                }
                String dmFmt = positional.get(0).toUpperCase();
                Class<?> dmCls;
                if ("VCF".equals(dmFmt)) {
                    dmCls = VariantContext.class;
                } else if ("SAM".equals(dmFmt)) {
                    dmCls = SAMRecord.class;
                } else {
                    System.err.println("Unknown format: " + dmFmt);
                    System.exit(1);
                    return;
                }
                System.out.print(discoverMutatorsJson(dmCls));
                return;
            }

            if ("query".equals(mode)) {
                // Rank 5 (Chen-Kuo-Liu-Tse 2018 §3.2; MR-Scout TOSEM 2024).
                // CLI:  --mode query <VCF|SAM> <file_path> --methods name1,name2
                //
                // Parses the file, takes the FIRST record, and invokes each
                // named method via java.lang.reflect.Method.invoke. Emits
                // {"method_results": {name: scalar, ...}}.
                if (positional.size() < 2) {
                    System.err.println(
                        "--mode query requires <VCF|SAM> <file_path>");
                    System.exit(1);
                }
                String qFmt = positional.get(0).toUpperCase();
                String qPath = positional.get(1);
                List<String> methodNames = methodsArg.isEmpty()
                    ? Collections.emptyList()
                    : Arrays.stream(methodsArg.split(","))
                        .map(String::trim).filter(s -> !s.isEmpty())
                        .collect(Collectors.toList());
                if ("VCF".equals(qFmt)) {
                    System.out.print(queryVcf(qPath, methodNames));
                } else if ("SAM".equals(qFmt)) {
                    System.out.print(querySam(qPath, methodNames));
                } else {
                    System.err.println("Unknown format: " + qFmt);
                    System.exit(1);
                }
                return;
            }

            // Default: parse mode. Expects <format> <file_path>.
            if (positional.size() < 2) {
                System.err.println("Usage: BioTestHarness VCF|SAM <file_path>");
                System.exit(1);
            }
            String format = positional.get(0).toUpperCase();
            String filePath = positional.get(1);

            String json;
            if ("VCF".equals(format)) {
                json = parseVcf(filePath);
            } else if ("SAM".equals(format)) {
                json = parseSam(filePath);
            } else {
                System.err.println("Unknown format: " + format);
                System.exit(1);
                return;
            }
            System.out.println(json);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace(System.err);
            System.exit(1);
        }
    }

    // -----------------------------------------------------------------------
    // VCF Write Roundtrip — parse-then-write exercise for the WRITE path.
    //
    // Two flavors are available so `HTSJDKRunner.run_write_roundtrip` can
    // rotate between them and cover *different* subsets of htsjdk's writer
    // plumbing across Phase C. Both return functionally-equivalent VCF text;
    // the harness output is oracle-compared, the coverage difference is the
    // side-effect we care about.
    //
    //   "standard" — the minimal path. clearOptions() + just the two writer
    //                Options we need. Exercises VCFEncoder, VCFWriter,
    //                VariantContextWriterBuilder's simple branches.
    //   "advanced" — the buffered path. .buffered() wraps the writer in
    //                AsyncVariantContextWriter (background IO thread),
    //                INDEX_ON_THE_FLY adds an IndexCreator invocation, and
    //                WRITE_FULL_FORMAT_FIELD + ALLOW_MISSING_FIELDS_IN_HEADER
    //                together hit the full conditional ladder in
    //                VariantContextWriterBuilder.build().
    //
    // These two together reach AsyncVariantContextWriter, IndexCreator
    // branches, and the non-clearOptions default path — all of which sat at
    // 0% coverage before this split.
    // -----------------------------------------------------------------------
    private static String writeRoundtripVcf(String path) throws IOException {
        return writeRoundtripVcf(path, "standard");
    }

    private static String writeRoundtripVcf(String path, String variant) throws IOException {
        File outFile = File.createTempFile("biotest_rt_", ".vcf");
        outFile.deleteOnExit();

        try (VCFFileReader reader = new VCFFileReader(Path.of(path), false)) {
            VCFHeader header = reader.getFileHeader();
            // htsjdk's VCFWriter refuses to serialize v4.3+ headers
            // ("Writing VCF version VCF4_3 is not implemented"). Our
            // canonical JSON comparison is format-agnostic, so force the
            // writeable header down to v4.2 — the VariantContext objects
            // themselves still carry any v4.3 content they contain.
            VCFHeader writableHeader = forceVcfVersionToV42(header);

            VariantContextWriterBuilder builder = new VariantContextWriterBuilder()
                .setOutputFile(outFile);

            if ("advanced".equals(variant)) {
                // Keep the default options (no clearOptions()), add .buffered()
                // so the writer gets wrapped in AsyncVariantContextWriter,
                // and opt into WRITE_FULL_FORMAT_FIELD + ALLOW_MISSING_FIELDS
                // explicitly so they remain even if future htsjdk defaults
                // drop them.
                builder = builder
                    .setBuffer(1 << 14)               // 16 KB buffer
                    .setOption(Options.WRITE_FULL_FORMAT_FIELD)
                    .setOption(Options.ALLOW_MISSING_FIELDS_IN_HEADER);
            } else {
                // Standard: clearOptions() strips index-on-the-fly, MD5, etc.
                // Minimal writer path — matches the original contract.
                builder = builder
                    .clearOptions()
                    .setOption(Options.WRITE_FULL_FORMAT_FIELD)
                    .setOption(Options.ALLOW_MISSING_FIELDS_IN_HEADER);
            }
            if (writableHeader.getSequenceDictionary() != null) {
                builder = builder.setReferenceDictionary(writableHeader.getSequenceDictionary());
            }

            try (VariantContextWriter writer = builder.build()) {
                writer.writeHeader(writableHeader);
                for (VariantContext vc : reader) {
                    writer.add(vc);
                }
            }
        }

        return Files.readString(outFile.toPath());
    }

    // -----------------------------------------------------------------------
    // SAM Write Roundtrip — parse-then-write via SAMFileWriterFactory.
    //
    // Parses the input SAM through SamReaderFactory, re-emits every record
    // via SAMFileWriter (text SAM output via the .sam extension). Exercises
    // SAMFileWriterFactory / SAMTextWriter / SAMRecord serialization — zero
    // coverage from parse-only flows.
    //
    // Returned string is the rewritten SAM text; the caller (Python
    // HTSJDKRunner.run_write_roundtrip) treats it as the transform output.
    // -----------------------------------------------------------------------
    private static String writeRoundtripSam(String path) throws IOException {
        File outFile = File.createTempFile("biotest_rt_", ".sam");
        outFile.deleteOnExit();

        try (SamReader reader = SamReaderFactory.makeDefault()
                .validationStringency(ValidationStringency.SILENT)
                .open(Path.of(path))) {
            SAMFileHeader header = reader.getFileHeader();
            try (SAMFileWriter writer = new SAMFileWriterFactory()
                    .setCreateIndex(false)
                    .setCreateMd5File(false)
                    .makeSAMWriter(header, true, outFile)) {
                for (SAMRecord rec : reader) {
                    writer.addAlignment(rec);
                }
            }
        }

        return Files.readString(outFile.toPath());
    }

    /**
     * Return a clone of `header` with any ##fileformat meta line replaced
     * by VCFv4.2 so htsjdk's VCFWriter will serialize it (v4.3+ headers
     * are rejected by {@code VCFWriter.rejectVCFV43Headers}). All INFO /
     * FORMAT / FILTER / contig lines are preserved verbatim.
     */
    private static VCFHeader forceVcfVersionToV42(VCFHeader header) {
        LinkedHashSet<VCFHeaderLine> lines = new LinkedHashSet<>();
        for (VCFHeaderLine ln : header.getMetaDataInInputOrder()) {
            // Drop any existing fileformat / file-version marker.
            if (VCFHeaderVersion.isFormatString(ln.getKey())) {
                continue;
            }
            lines.add(ln);
        }
        // Inject v4.2 fileformat at the top.
        LinkedHashSet<VCFHeaderLine> withVersion = new LinkedHashSet<>();
        withVersion.add(new VCFHeaderLine(
            VCFHeaderVersion.VCF4_2.getFormatString(),
            VCFHeaderVersion.VCF4_2.getVersionString()));
        withVersion.addAll(lines);

        VCFHeader out = new VCFHeader(withVersion, header.getGenotypeSamples());
        if (header.getSequenceDictionary() != null) {
            out.setSequenceDictionary(header.getSequenceDictionary());
        }
        return out;
    }

    // -----------------------------------------------------------------------
    // VCF
    // -----------------------------------------------------------------------
    private static String parseVcf(String path) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\"format\":\"VCF\",");

        try (VCFFileReader reader = new VCFFileReader(Path.of(path), false)) {
            VCFHeader header = reader.getFileHeader();

            // Header
            sb.append("\"header\":{");
            sb.append("\"fileformat\":").append(jsonStr(header.getVCFHeaderVersion() != null
                ? header.getVCFHeaderVersion().toString() : ""));

            // Meta: INFO, FORMAT, FILTER, contig
            sb.append(",\"meta\":{");
            sb.append("\"INFO\":{");
            sb.append(header.getInfoHeaderLines().stream()
                .map(h -> jsonStr(h.getID()) + ":" + infoHeaderToJson(h))
                .collect(Collectors.joining(",")));
            sb.append("},\"FORMAT\":{");
            sb.append(header.getFormatHeaderLines().stream()
                .map(h -> jsonStr(h.getID()) + ":" + formatHeaderToJson(h))
                .collect(Collectors.joining(",")));
            sb.append("},\"FILTER\":{");
            sb.append(header.getFilterLines().stream()
                .map(h -> jsonStr(h.getID()) + ":{\"ID\":" + jsonStr(h.getID())
                    + ",\"Description\":" + jsonStr(h.getDescription()) + "}")
                .collect(Collectors.joining(",")));
            sb.append("}}");

            // Samples
            sb.append(",\"samples\":[");
            sb.append(header.getGenotypeSamples().stream()
                .map(BioTestHarness::jsonStr)
                .collect(Collectors.joining(",")));
            sb.append("]},");

            // Records
            sb.append("\"records\":[");
            boolean firstRec = true;
            for (VariantContext vc : reader) {
                if (!firstRec) sb.append(",");
                firstRec = false;
                sb.append(vcRecordToJson(vc, header));
            }
            sb.append("]}");
        }
        return sb.toString();
    }

    private static String vcRecordToJson(VariantContext vc, VCFHeader header) {
        StringBuilder sb = new StringBuilder("{");
        sb.append("\"CHROM\":").append(jsonStr(vc.getContig()));
        sb.append(",\"POS\":").append(vc.getStart()); // 1-based
        sb.append(",\"ID\":").append(vc.getID().equals(".") ? "null" : jsonStr(vc.getID()));
        sb.append(",\"REF\":").append(jsonStr(vc.getReference().getBaseString()));

        // ALT — use getDisplayString(), not getBaseString().
        // getBaseString() returns "" for symbolic alleles (<NON_REF>,
        // <DEL>, <DUP>, <*>, etc.); getDisplayString() returns
        // "<NON_REF>" etc. Oracle-validation 2026-04-22 saw 621
        // records in real_world_htslib_index.vcf report ALT=[""]
        // from htsjdk while vcfpy emitted the expected ["*"] — this
        // split consensus on every GVCF/SV input. We also strip the
        // surrounding angle brackets so htsjdk's "<DEL>" agrees with
        // vcfpy's "DEL".
        sb.append(",\"ALT\":[");
        sb.append(vc.getAlternateAlleles().stream()
            .map(a -> {
                String s = a.getDisplayString();
                if (s.length() >= 2 && s.startsWith("<") && s.endsWith(">")) {
                    s = s.substring(1, s.length() - 1);
                }
                return jsonStr(s);
            })
            .collect(Collectors.joining(",")));
        sb.append("]");

        // QUAL
        if (vc.getLog10PError() == VariantContext.NO_LOG10_PERROR) {
            sb.append(",\"QUAL\":null");
        } else {
            sb.append(",\"QUAL\":").append(vc.getPhredScaledQual());
        }

        // FILTER
        sb.append(",\"FILTER\":[");
        sb.append(vc.getFilters().stream().sorted()
            .map(BioTestHarness::jsonStr)
            .collect(Collectors.joining(",")));
        sb.append("]");

        // INFO
        sb.append(",\"INFO\":{");
        Map<String, Object> attrs = new TreeMap<>(vc.getAttributes());
        List<String> infoParts = new ArrayList<>();
        for (Map.Entry<String, Object> entry : attrs.entrySet()) {
            String key = entry.getKey();
            Object val = entry.getValue();
            infoParts.add(jsonStr(key) + ":" + infoValueToJson(val));
        }
        // Add flags
        for (VCFInfoHeaderLine infoLine : header.getInfoHeaderLines()) {
            if (infoLine.getType() == VCFHeaderLineType.Flag
                && vc.hasAttribute(infoLine.getID())
                && !attrs.containsKey(infoLine.getID())) {
                infoParts.add(jsonStr(infoLine.getID()) + ":true");
            }
        }
        sb.append(String.join(",", infoParts));
        sb.append("}");

        // FORMAT + samples
        if (vc.hasGenotypes()) {
            GenotypesContext genotypes = vc.getGenotypes();
            List<String> formatKeys = new ArrayList<>();
            if (!genotypes.isEmpty()) {
                Genotype first = genotypes.get(0);
                if (first.hasGQ()) formatKeys.add("GQ");
                if (first.hasDP()) formatKeys.add("DP");
            }

            sb.append(",\"FORMAT\":[");
            // Get FORMAT keys from the first genotype
            Genotype g0 = genotypes.get(0);
            List<String> fmtKeys = new ArrayList<>();
            fmtKeys.add("GT");
            for (String key : g0.getExtendedAttributes().keySet()) {
                if (!fmtKeys.contains(key)) fmtKeys.add(key);
            }
            if (g0.hasGQ() && !fmtKeys.contains("GQ")) fmtKeys.add("GQ");
            if (g0.hasDP() && !fmtKeys.contains("DP")) fmtKeys.add("DP");
            sb.append(fmtKeys.stream().map(BioTestHarness::jsonStr).collect(Collectors.joining(",")));
            sb.append("]");

            sb.append(",\"samples\":{");
            boolean firstSample = true;
            for (Genotype gt : genotypes) {
                if (!firstSample) sb.append(",");
                firstSample = false;
                sb.append(jsonStr(gt.getSampleName())).append(":{");
                sb.append("\"GT\":").append(jsonStr(gt.getGenotypeString()));
                if (gt.hasGQ()) sb.append(",\"GQ\":").append(gt.getGQ());
                if (gt.hasDP()) sb.append(",\"DP\":").append(gt.getDP());
                for (Map.Entry<String, Object> ext : gt.getExtendedAttributes().entrySet()) {
                    sb.append(",").append(jsonStr(ext.getKey())).append(":")
                      .append(infoValueToJson(ext.getValue()));
                }
                sb.append("}");
            }
            sb.append("}");
        } else {
            sb.append(",\"FORMAT\":null,\"samples\":null");
        }

        sb.append("}");
        return sb.toString();
    }

    // -----------------------------------------------------------------------
    // SAM
    // -----------------------------------------------------------------------
    private static String parseSam(String path) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\"format\":\"SAM\",");

        try (SamReader reader = SamReaderFactory.makeDefault()
                .validationStringency(ValidationStringency.SILENT)
                .open(Path.of(path))) {

            SAMFileHeader header = reader.getFileHeader();

            // Header
            sb.append("\"header\":{");

            // HD
            String version = header.getVersion();
            String sortOrder = header.getSortOrder() != null ? header.getSortOrder().name() : null;
            if (version != null) {
                sb.append("\"HD\":{\"VN\":").append(jsonStr(version));
                if (sortOrder != null) sb.append(",\"SO\":").append(jsonStr(sortOrder.toLowerCase()));
                sb.append("}");
            } else {
                sb.append("\"HD\":null");
            }

            // SQ
            sb.append(",\"SQ\":[");
            sb.append(header.getSequenceDictionary().getSequences().stream()
                .map(sq -> "{\"SN\":" + jsonStr(sq.getSequenceName())
                    + ",\"LN\":\"" + sq.getSequenceLength() + "\"}")
                .collect(Collectors.joining(",")));
            sb.append("]");

            // RG
            sb.append(",\"RG\":[");
            sb.append(header.getReadGroups().stream()
                .map(rg -> readGroupToJson(rg))
                .collect(Collectors.joining(",")));
            sb.append("]");

            // PG
            sb.append(",\"PG\":[");
            sb.append(header.getProgramRecords().stream()
                .map(pg -> programRecordToJson(pg))
                .collect(Collectors.joining(",")));
            sb.append("]");

            // CO
            sb.append(",\"CO\":[");
            sb.append(header.getComments().stream().sorted()
                .map(BioTestHarness::jsonStr)
                .collect(Collectors.joining(",")));
            sb.append("]");

            sb.append("},");

            // Records
            sb.append("\"records\":[");
            boolean first = true;
            for (SAMRecord rec : reader) {
                if (!first) sb.append(",");
                first = false;
                sb.append(samRecordToJson(rec));
            }
            sb.append("]}");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return sb.toString();
    }

    private static String samRecordToJson(SAMRecord rec) {
        StringBuilder sb = new StringBuilder("{");
        sb.append("\"QNAME\":").append(jsonStr(rec.getReadName()));
        sb.append(",\"FLAG\":").append(rec.getFlags());

        // RNAME — null if unmapped
        if (rec.getReadUnmappedFlag()) {
            sb.append(",\"RNAME\":null");
        } else {
            sb.append(",\"RNAME\":").append(jsonStr(rec.getReferenceName()));
        }

        // POS — 1-based, null if unmapped (0)
        int pos = rec.getAlignmentStart();
        sb.append(",\"POS\":").append(pos == 0 ? "null" : pos);

        sb.append(",\"MAPQ\":").append(rec.getMappingQuality());

        // CIGAR
        if (rec.getCigar() == null || rec.getCigar().isEmpty()
            || rec.getCigarString().equals("*")) {
            sb.append(",\"CIGAR\":null");
        } else {
            sb.append(",\"CIGAR\":[");
            sb.append(rec.getCigar().getCigarElements().stream()
                .map(el -> "{\"op\":" + jsonStr(el.getOperator().toString())
                    + ",\"len\":" + el.getLength() + "}")
                .collect(Collectors.joining(",")));
            sb.append("]");
        }

        // RNEXT
        String mateRef = rec.getMateReferenceName();
        sb.append(",\"RNEXT\":").append(
            mateRef == null || mateRef.equals("*") ? "null" : jsonStr(mateRef));

        // PNEXT
        int pnext = rec.getMateAlignmentStart();
        sb.append(",\"PNEXT\":").append(pnext == 0 ? "null" : pnext);

        sb.append(",\"TLEN\":").append(rec.getInferredInsertSize());

        // SEQ
        String seq = rec.getReadString();
        sb.append(",\"SEQ\":").append(seq.equals("*") ? "null" : jsonStr(seq));

        // QUAL
        String qual = rec.getBaseQualityString();
        sb.append(",\"QUAL\":").append(qual.equals("*") ? "null" : jsonStr(qual));

        // Tags — sorted by name
        sb.append(",\"tags\":{");
        List<SAMRecord.SAMTagAndValue> tags = rec.getAttributes();
        tags.sort(Comparator.comparing(t -> t.tag));
        sb.append(tags.stream()
            .map(tv -> jsonStr(tv.tag) + ":{\"type\":" + jsonStr(getTagType(tv.value))
                + ",\"value\":" + tagValueToJson(tv.value) + "}")
            .collect(Collectors.joining(",")));
        sb.append("}");

        sb.append("}");
        return sb.toString();
    }

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------
    private static String jsonStr(String s) {
        if (s == null) return "null";
        return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    private static String infoValueToJson(Object val) {
        if (val == null) return "null";
        if (val instanceof Boolean) return val.toString();
        if (val instanceof Number) return val.toString();
        if (val instanceof List) {
            return "[" + ((List<?>) val).stream()
                .map(v -> infoValueToJson(v))
                .collect(Collectors.joining(",")) + "]";
        }
        if (val.getClass().isArray()) {
            if (val instanceof int[]) {
                return "[" + Arrays.stream((int[]) val)
                    .mapToObj(String::valueOf).collect(Collectors.joining(",")) + "]";
            }
            if (val instanceof double[]) {
                return "[" + Arrays.stream((double[]) val)
                    .mapToObj(String::valueOf).collect(Collectors.joining(",")) + "]";
            }
        }
        return jsonStr(val.toString());
    }

    private static String getTagType(Object val) {
        if (val instanceof Character) return "A";
        if (val instanceof Integer || val instanceof Short || val instanceof Byte) return "i";
        if (val instanceof Float) return "f";
        if (val instanceof String) return "Z";
        if (val instanceof byte[]) return "H";
        if (val instanceof int[] || val instanceof short[] || val instanceof float[]) return "B";
        return "Z";
    }

    private static String tagValueToJson(Object val) {
        if (val instanceof int[]) {
            return "[" + Arrays.stream((int[]) val)
                .mapToObj(String::valueOf).collect(Collectors.joining(",")) + "]";
        }
        if (val instanceof short[]) {
            short[] arr = (short[]) val;
            StringJoiner sj = new StringJoiner(",", "[", "]");
            for (short s : arr) sj.add(String.valueOf(s));
            return sj.toString();
        }
        if (val instanceof float[]) {
            float[] arr = (float[]) val;
            StringJoiner sj = new StringJoiner(",", "[", "]");
            for (float f : arr) sj.add(String.valueOf(f));
            return sj.toString();
        }
        return infoValueToJson(val);
    }

    private static String infoHeaderToJson(VCFInfoHeaderLine h) {
        return "{\"ID\":" + jsonStr(h.getID())
            + ",\"Number\":" + jsonStr(h.getCountType() == VCFHeaderLineCount.INTEGER
                ? String.valueOf(h.getCount()) : h.getCountType().name().substring(0, 1))
            + ",\"Type\":" + jsonStr(h.getType().toString())
            + ",\"Description\":" + jsonStr(h.getDescription()) + "}";
    }

    private static String formatHeaderToJson(VCFFormatHeaderLine h) {
        return "{\"ID\":" + jsonStr(h.getID())
            + ",\"Number\":" + jsonStr(h.getCountType() == VCFHeaderLineCount.INTEGER
                ? String.valueOf(h.getCount()) : h.getCountType().name().substring(0, 1))
            + ",\"Type\":" + jsonStr(h.getType().toString())
            + ",\"Description\":" + jsonStr(h.getDescription()) + "}";
    }

    private static String readGroupToJson(SAMReadGroupRecord rg) {
        StringBuilder sb = new StringBuilder("{");
        sb.append("\"ID\":").append(jsonStr(rg.getId()));
        if (rg.getSample() != null) sb.append(",\"SM\":").append(jsonStr(rg.getSample()));
        if (rg.getPlatform() != null) sb.append(",\"PL\":").append(jsonStr(rg.getPlatform()));
        sb.append("}");
        return sb.toString();
    }

    private static String programRecordToJson(SAMProgramRecord pg) {
        StringBuilder sb = new StringBuilder("{");
        sb.append("\"ID\":").append(jsonStr(pg.getId()));
        if (pg.getProgramName() != null) sb.append(",\"PN\":").append(jsonStr(pg.getProgramName()));
        if (pg.getProgramVersion() != null) sb.append(",\"VN\":").append(jsonStr(pg.getProgramVersion()));
        sb.append("}");
        return sb.toString();
    }

    // ====================================================================
    // Rank 5 — query-method MR support (Java reflection)
    //
    // Reference: Chen, Kuo, Liu, Tse — ACM CSUR 2018 §3.2 (API MRs);
    // MR-Scout — Xu et al., TOSEM 2024, arXiv:2304.07548.
    //
    // The framework's query-consensus oracle compares scalar results of
    // public, zero-arg, getter-style methods on htsjdk's parsed-record
    // classes (VariantContext for VCF, SAMRecord for SAM) across x and
    // T(x). All method enumeration / invocation goes through
    // java.lang.reflect — NO hardcoded method names.
    // ====================================================================

    private static final Set<String> SCALAR_RETURNS = new HashSet<>(Arrays.asList(
        "boolean", "Boolean", "int", "Integer", "long", "Long",
        "float", "Float", "double", "Double", "char", "Character",
        "java.lang.String", "String"
    ));

    private static boolean isScalarReturn(Class<?> rt) {
        if (rt == void.class || rt == Void.class) return false;
        if (rt.isPrimitive()) return true;
        if (rt.isEnum()) return true;
        return SCALAR_RETURNS.contains(rt.getName())
            || SCALAR_RETURNS.contains(rt.getSimpleName());
    }

    private static String discoverMethodsJson(Class<?> cls) {
        // Filter: public, zero-parameter, scalar-returning instance methods
        // whose name doesn't start with `set`, `add`, `remove`, `clear`
        // (mutators / commands — not pure query methods).
        Set<String> mutatorPrefixes = new HashSet<>(Arrays.asList(
            "set", "add", "remove", "clear", "init", "destroy", "close"
        ));
        // Methods inherited from Object/Class are always uninteresting.
        Set<String> objectNoise = new HashSet<>(Arrays.asList(
            "hashCode", "toString", "getClass", "wait", "notify",
            "notifyAll", "equals", "clone"
        ));

        List<String> entries = new ArrayList<>();
        Set<String> seen = new HashSet<>();
        Method[] methods = cls.getMethods();
        Arrays.sort(methods, Comparator.comparing(Method::getName));
        for (Method m : methods) {
            if (m.getParameterCount() != 0) continue;
            int mods = m.getModifiers();
            if ((mods & java.lang.reflect.Modifier.PUBLIC) == 0) continue;
            if ((mods & java.lang.reflect.Modifier.STATIC) != 0) continue;
            String name = m.getName();
            if (objectNoise.contains(name)) continue;
            if (seen.contains(name)) continue;
            // Drop obvious mutators
            String lower = name.toLowerCase(Locale.ROOT);
            boolean isMutator = false;
            for (String pfx : mutatorPrefixes) {
                if (lower.startsWith(pfx)) { isMutator = true; break; }
            }
            if (isMutator) continue;
            Class<?> rt = m.getReturnType();
            if (!isScalarReturn(rt)) continue;
            seen.add(name);
            entries.add(
                "{\"name\":" + jsonStr(name)
                + ",\"returns\":" + jsonStr(rt.getSimpleName())
                + ",\"args\":[]}"
            );
            if (entries.size() >= 50) break;
        }
        return "{\"methods\":[" + String.join(",", entries) + "]}";
    }

    private static String discoverMutatorsJson(Class<?> cls) {
        // Mirror of discoverMethodsJson with INVERSE filter:
        //  - name starts with set/add/remove/clear/put/reset
        //  - return type is void OR the receiver class (fluent setters)
        //  - public, instance (not static), non-Object-noise
        //  - any parameter count (mutators take 1+ args by definition)
        Set<String> mutatorPrefixes = new HashSet<>(Arrays.asList(
            "set", "add", "remove", "clear", "put", "reset"
        ));
        Set<String> objectNoise = new HashSet<>(Arrays.asList(
            "hashCode", "toString", "getClass", "wait", "notify",
            "notifyAll", "equals", "clone"
        ));

        List<String> entries = new ArrayList<>();
        Set<String> seen = new HashSet<>();
        Method[] methods = cls.getMethods();
        Arrays.sort(methods, Comparator.comparing(Method::getName));
        for (Method m : methods) {
            int mods = m.getModifiers();
            if ((mods & java.lang.reflect.Modifier.PUBLIC) == 0) continue;
            if ((mods & java.lang.reflect.Modifier.STATIC) != 0) continue;
            String name = m.getName();
            if (objectNoise.contains(name)) continue;
            String lower = name.toLowerCase(Locale.ROOT);
            boolean isMutator = false;
            for (String pfx : mutatorPrefixes) {
                if (lower.startsWith(pfx)) { isMutator = true; break; }
            }
            if (!isMutator) continue;
            Class<?> rt = m.getReturnType();
            // Accept void or fluent (returns receiver type)
            boolean fluent = rt.equals(void.class)
                || rt.equals(Void.TYPE)
                || rt.equals(cls);
            if (!fluent) continue;
            // Dedupe by name+arg count to keep the catalog compact.
            String key = name + "/" + m.getParameterCount();
            if (seen.contains(key)) continue;
            seen.add(key);
            // Render arg types (Java simple names) to give the LLM a hint.
            StringBuilder argList = new StringBuilder();
            argList.append('[');
            Class<?>[] params = m.getParameterTypes();
            for (int i = 0; i < params.length; i++) {
                if (i > 0) argList.append(',');
                argList.append(jsonStr(params[i].getSimpleName()));
            }
            argList.append(']');
            entries.add(
                "{\"name\":" + jsonStr(name)
                + ",\"returns\":" + jsonStr(rt.equals(cls) ? cls.getSimpleName() : "void")
                + ",\"args\":" + argList.toString() + "}"
            );
            if (entries.size() >= 60) break;
        }
        return "{\"mutators\":[" + String.join(",", entries) + "]}";
    }

    private static String queryVcf(String path, List<String> methodNames) throws IOException {
        try (VCFFileReader reader = new VCFFileReader(Path.of(path), false)) {
            Iterator<VariantContext> it = reader.iterator();
            VariantContext rec = it.hasNext() ? it.next() : null;
            return invokeAndPack(rec, VariantContext.class, methodNames);
        }
    }

    private static String querySam(String path, List<String> methodNames) throws IOException {
        try (SamReader reader = SamReaderFactory.makeDefault()
                .validationStringency(ValidationStringency.SILENT)
                .open(Path.of(path))) {
            Iterator<SAMRecord> it = reader.iterator();
            SAMRecord rec = it.hasNext() ? it.next() : null;
            return invokeAndPack(rec, SAMRecord.class, methodNames);
        }
    }

    private static String invokeAndPack(
        Object rec, Class<?> cls, List<String> methodNames
    ) {
        StringBuilder sb = new StringBuilder("{\"method_results\":{");
        boolean first = true;
        for (String name : methodNames) {
            if (!first) sb.append(",");
            first = false;
            sb.append(jsonStr(name)).append(":");
            if (rec == null) {
                sb.append("null");
                continue;
            }
            try {
                Method m = cls.getMethod(name);
                Object value = m.invoke(rec);
                sb.append(scalarToJson(value));
            } catch (NoSuchMethodException nsme) {
                sb.append("{\"__error__\":")
                  .append(jsonStr("NoSuchMethod: " + name))
                  .append("}");
            } catch (Exception e) {
                sb.append("{\"__error__\":")
                  .append(jsonStr(e.getClass().getSimpleName() + ": "
                                  + (e.getMessage() == null ? "" : e.getMessage())))
                  .append("}");
            }
        }
        sb.append("}}");
        return sb.toString();
    }

    private static String scalarToJson(Object value) {
        if (value == null) return "null";
        if (value instanceof Boolean) return value.toString();
        if (value instanceof Number) return value.toString();
        if (value instanceof Enum<?>) return jsonStr(((Enum<?>) value).name());
        return jsonStr(value.toString());
    }
}
