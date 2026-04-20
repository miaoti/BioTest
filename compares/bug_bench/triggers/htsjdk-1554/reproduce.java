// Minimal reproducer for htsjdk-1554.
//
// Build against htsjdk 2.24.1 (pre-fix) to observe wrong AC; against
// 3.0.0 (post-fix) to observe the fix. The bug surfaces in the cohort
// allele-count utility that ignores genotype-level FT.
//
// Expected behaviour:
//   pre-fix  : getCalledChrCount(Allele.T) == 1  (WRONG — FT-filtered GT counted)
//   post-fix : getCalledChrCount(Allele.T) == 0  (correct — FT excluded)

import htsjdk.variant.variantcontext.*;
import htsjdk.variant.vcf.*;
import java.io.File;

public class Reproduce_1554 {
    public static void main(String[] args) throws Exception {
        File vcf = new File("original.vcf");
        try (VCFFileReader r = new VCFFileReader(vcf, /*requireIndex*/ false)) {
            for (VariantContext vc : r) {
                Allele t = Allele.create("T", false);
                int calledT = vc.getCalledChrCount(t);
                System.out.println("calledChrCount(T) = " + calledT +
                                   "  (expected 0 after FT respect)");
            }
        }
    }
}
