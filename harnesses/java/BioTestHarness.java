import htsjdk.samtools.*;
import htsjdk.samtools.util.CloseableIterator;
import htsjdk.variant.variantcontext.*;
import htsjdk.variant.vcf.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

/**
 * BioTest Canonical JSON Harness for HTSJDK.
 *
 * Usage: java -cp biotest-harness.jar BioTestHarness VCF|SAM <file_path>
 *
 * Outputs canonical JSON to stdout. Exit code 0 = success, 1 = error.
 */
public class BioTestHarness {

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: BioTestHarness VCF|SAM <file_path>");
            System.exit(1);
        }

        String format = args[0].toUpperCase();
        String filePath = args[1];

        try {
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

        // ALT
        sb.append(",\"ALT\":[");
        sb.append(vc.getAlternateAlleles().stream()
            .map(a -> jsonStr(a.getBaseString()))
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
}
