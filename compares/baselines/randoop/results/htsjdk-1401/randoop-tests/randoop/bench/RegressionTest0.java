package randoop.bench;

import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class RegressionTest0 {

    public static boolean debug = false;

    @Test
    public void test001() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test001");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.REFERENCE_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "reference" + "'", str0, "reference");
    }

    @Test
    public void test002() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test002");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.INTERVALS_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "intervals" + "'", str0, "intervals");
    }

    @Test
    public void test003() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test003");
        long long0 = htsjdk.variant.vcf.VCFHeader.serialVersionUID;
        org.junit.Assert.assertTrue("'" + long0 + "' != '" + 1L + "'", long0 == 1L);
    }

    @Test
    public void test004() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test004");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.INTERVAL_MERGING_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "interval_merging" + "'", str0, "interval_merging");
    }

    @Test
    public void test005() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test005");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot read field \"mMetaData\" because \"toCopy\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test006() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test006");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.ALT;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.ALT + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.ALT));
    }

    @Test
    public void test007() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test007");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator1 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test008() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test008");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.EXCLUDE_INTERVALS_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "excludeIntervals" + "'", str0, "excludeIntervals");
    }

    @Test
    public void test009() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test009");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.CHROM;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.CHROM + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.CHROM));
    }

    @Test
    public void test010() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test010");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader.validateVersionTransition(vCFHeaderVersion0, vCFHeaderVersion1);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test011() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test011");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.hasGenotypingData();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine6 = vCFHeader0.getOtherHeaderLine("interval_merging");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(vCFHeaderLine6);
    }

    @Test
    public void test012() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test012");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.POS;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.POS + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.POS));
    }

    @Test
    public void test013() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test013");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.CONTIG_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "contig" + "'", str0, "contig");
    }

    @Test
    public void test014() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test014");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion4);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
    }

    @Test
    public void test015() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test015");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        boolean boolean11 = vCFHeader7.hasInfoLine("contig");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
    }

    @Test
    public void test016() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test016");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.HEADER_INDICATOR;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "#" + "'", str0, "#");
    }

    @Test
    public void test017() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test017");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.INTERVAL_SET_RULE_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "interval_set_rule" + "'", str0, "interval_set_rule");
    }

    @Test
    public void test018() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test018");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary1 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test019() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test019");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.ID;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.ID + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.ID));
    }

    @Test
    public void test020() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test020");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.INFO;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.INFO + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.INFO));
    }

    @Test
    public void test021() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test021");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator9 = vCFHeader7.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
    }

    @Test
    public void test022() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test022");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        java.lang.Class<?> wildcardClass2 = vCFHeader0.getClass();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNotNull(wildcardClass2);
    }

    @Test
    public void test023() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test023");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.INTERVAL_PADDING_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "interval_padding" + "'", str0, "interval_padding");
    }

    @Test
    public void test024() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test024");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary4 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary4);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
    }

    @Test
    public void test025() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test025");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.METADATA_INDICATOR;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "##" + "'", str0, "##");
    }

    @Test
    public void test026() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test026");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = vCFHeader1.getMetaDataInSortedOrder();
        java.util.Set<java.lang.String> strSet3 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet2, strSet3);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineSet2);
    }

    @Test
    public void test027() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test027");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        java.lang.String[] strArray5 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet6 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean7 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet6, strArray5);
        htsjdk.variant.vcf.VCFHeader vCFHeader8 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet6);
        java.lang.String[] strArray16 = new java.lang.String[] { "#", "reference", "intervals", "hi!", "hi!", "", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet17 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet17, strArray16);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet17);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray5);
        org.junit.Assert.assertArrayEquals(strArray5, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertNotNull(strArray16);
        org.junit.Assert.assertArrayEquals(strArray16, new java.lang.String[] { "#", "reference", "intervals", "hi!", "hi!", "", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
    }

    @Test
    public void test028() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test028");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        java.util.List<java.lang.String> strList2 = vCFHeader0.getGenotypeSamples();
        boolean boolean4 = vCFHeader0.hasFormatLine("#");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(strList2);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test029() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test029");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "interval_merging", "interval_set_rule", "", "interval_set_rule" };
        java.util.ArrayList<java.lang.String> strList10 = new java.util.ArrayList<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList10, strArray9);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.List<java.lang.String>) strList10);
            org.junit.Assert.fail("Expected exception of type htsjdk.tribble.TribbleException.InvalidHeader; message: Your input file has a malformed header: BUG: VCF header has duplicate sample names");
        } catch (htsjdk.tribble.TribbleException.InvalidHeader e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "interval_merging", "interval_set_rule", "", "interval_set_rule" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
    }

    @Test
    public void test030() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test030");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine3 = vCFHeader0.getFormatHeaderLine("#");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNull(vCFFormatHeaderLine3);
    }

    @Test
    public void test031() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test031");
        java.lang.String str0 = htsjdk.variant.vcf.VCFHeader.SOURCE_KEY;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "source" + "'", str0, "source");
    }

    @Test
    public void test032() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test032");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion5 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion5);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
    }

    @Test
    public void test033() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test033");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        java.lang.String[] strArray10 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet11 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet11, strArray10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet11);
        java.lang.String[] strArray24 = new java.lang.String[] { "##", "excludeIntervals", "contig", "hi!", "", "", "##", "interval_padding", "reference", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet25 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean26 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet25, strArray24);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader27 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet25);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(strArray24);
        org.junit.Assert.assertArrayEquals(strArray24, new java.lang.String[] { "##", "excludeIntervals", "contig", "hi!", "", "", "##", "interval_padding", "reference", "##" });
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + true + "'", boolean26 == true);
    }

    @Test
    public void test034() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test034");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        boolean boolean5 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
    }

    @Test
    public void test035() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test035");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        java.util.ArrayList<java.lang.String> strList9 = vCFHeader0.getSampleNamesInOrder();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList10 = vCFHeader0.getIDHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(strList9);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList10);
    }

    @Test
    public void test036() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test036");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion6 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion6);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
    }

    @Test
    public void test037() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test037");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = vCFHeader1.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray3 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet4 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean5 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet4, vCFHeaderLineArray3);
        java.lang.String[] strArray7 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet8 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean9 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet8, strArray7);
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet4, (java.util.Set<java.lang.String>) strSet8);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader11 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet8);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineSet2);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray3);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray3, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(strArray7);
        org.junit.Assert.assertArrayEquals(strArray7, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test038() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test038");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        java.lang.Class<?> wildcardClass6 = vCFHeader0.getClass();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
        org.junit.Assert.assertNotNull(wildcardClass6);
    }

    @Test
    public void test039() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test039");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        vCFHeader4.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion7 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader4.setVCFHeaderVersion(vCFHeaderVersion7);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
    }

    @Test
    public void test040() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test040");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine6 = vCFHeader0.getMetaDataLine("##");
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNull(vCFHeaderLine6);
    }

    @Test
    public void test041() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test041");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("reference");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
    }

    @Test
    public void test042() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test042");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean3 = vCFHeader1.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet4 = vCFHeader1.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet4);
        java.lang.String[] strArray16 = new java.lang.String[] { "", "hi!", "intervals", "interval_padding", "reference", "contig", "hi!", "", "", "interval_padding" };
        java.util.LinkedHashSet<java.lang.String> strSet17 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet17, strArray16);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet4, (java.util.Set<java.lang.String>) strSet17);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet4);
        org.junit.Assert.assertNotNull(strArray16);
        org.junit.Assert.assertArrayEquals(strArray16, new java.lang.String[] { "", "hi!", "intervals", "interval_padding", "reference", "contig", "hi!", "", "", "interval_padding" });
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
    }

    @Test
    public void test043() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test043");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine14 = vCFHeader0.getFilterHeaderLine("reference");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine16 = vCFHeader0.getMetaDataLine("excludeIntervals");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNull(vCFFilterHeaderLine14);
        org.junit.Assert.assertNull(vCFHeaderLine16);
    }

    @Test
    public void test044() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test044");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        java.util.List<java.lang.String> strList8 = vCFHeader0.getGenotypeSamples();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
        org.junit.Assert.assertNotNull(strList8);
    }

    @Test
    public void test045() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test045");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.REF;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.REF + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.REF));
    }

    @Test
    public void test046() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test046");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray5 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet6 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean7 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet6, vCFHeaderLineArray5);
        htsjdk.variant.vcf.VCFHeader vCFHeader8 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet6);
        htsjdk.variant.vcf.VCFHeader vCFHeader9 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet6);
        java.lang.String[] strArray14 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet15 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean16 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet15, strArray14);
        htsjdk.variant.vcf.VCFHeader vCFHeader17 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet6, (java.util.Set<java.lang.String>) strSet15);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader18 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet15);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray5);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray5, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
        org.junit.Assert.assertNotNull(strArray14);
        org.junit.Assert.assertArrayEquals(strArray14, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
    }

    @Test
    public void test047() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test047");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.List<java.lang.String> strList3 = vCFHeader0.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList5 = vCFHeader0.getIDHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strList3);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList5);
    }

    @Test
    public void test048() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test048");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine9 = vCFHeader0.getFormatHeaderLine("##");
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap10 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
        org.junit.Assert.assertNull(vCFFormatHeaderLine9);
        org.junit.Assert.assertNotNull(strMap10);
    }

    @Test
    public void test049() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test049");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.FILTER;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.FILTER + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.FILTER));
    }

    @Test
    public void test050() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test050");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        java.util.ArrayList<java.lang.String> strList9 = vCFHeader0.getSampleNamesInOrder();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary10 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(strList9);
    }

    @Test
    public void test051() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test051");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary2 = vCFHeader0.getSequenceDictionary();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine4 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNull(sAMSequenceDictionary2);
        org.junit.Assert.assertNull(vCFFormatHeaderLine4);
    }

    @Test
    public void test052() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test052");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        java.lang.String str12 = vCFHeader0.toString();
        boolean boolean14 = vCFHeader0.hasFormatLine("[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "[VCFHeader:\n]" + "'", str12, "[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test053() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test053");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine10 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader7.addMetaDataLine(vCFHeaderLine10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
    }

    @Test
    public void test054() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test054");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        vCFHeader4.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader4);
        boolean boolean8 = vCFHeader7.isWriteEngineHeaders();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + true + "'", boolean8 == true);
    }

    @Test
    public void test055() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test055");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
    }

    @Test
    public void test056() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test056");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3);
        boolean boolean5 = vCFHeader4.samplesWereAlreadySorted();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet3);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
    }

    @Test
    public void test057() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test057");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.Class<?> wildcardClass5 = vCFHeaderLineSet1.getClass();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(wildcardClass5);
    }

    @Test
    public void test058() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test058");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList4 = vCFHeader0.getFilterLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList4);
    }

    @Test
    public void test059() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test059");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList2 = vCFHeader0.getContigLines();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection3 = vCFHeader0.getFormatHeaderLines();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList2);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection3);
    }

    @Test
    public void test060() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test060");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList2 = vCFHeader0.getContigLines();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList3 = vCFHeader0.getIDHeaderLines();
        boolean boolean5 = vCFHeader0.hasFormatLine("interval_set_rule");
        int int6 = vCFHeader0.getColumnCount();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList2);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList3);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 8 + "'", int6 == 8);
    }

    @Test
    public void test061() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test061");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection6 = vCFHeader0.getInfoHeaderLines();
        vCFHeader0.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine9 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine9);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection6);
    }

    @Test
    public void test062() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test062");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("");
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList12 = vCFHeader0.getContigLines();
        java.lang.Class<?> wildcardClass13 = vCFContigHeaderLineList12.getClass();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList12);
        org.junit.Assert.assertNotNull(wildcardClass13);
    }

    @Test
    public void test063() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test063");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion2 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFHeaderVersion2);
    }

    @Test
    public void test064() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test064");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.List<java.lang.String> strList3 = vCFHeader0.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        boolean boolean5 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strList3);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
    }

    @Test
    public void test065() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test065");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary1 = vCFHeader0.getSequenceDictionary();
        java.util.ArrayList<java.lang.String> strList2 = vCFHeader0.getSampleNamesInOrder();
        org.junit.Assert.assertNull(sAMSequenceDictionary1);
        org.junit.Assert.assertNotNull(strList2);
    }

    @Test
    public void test066() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test066");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        java.lang.String[] strArray10 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet11 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet11, strArray10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet11);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray14 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet15 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean16 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, vCFHeaderLineArray14);
        htsjdk.variant.vcf.VCFHeader vCFHeader17 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        htsjdk.variant.vcf.VCFHeader vCFHeader18 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        java.lang.String[] strArray23 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet24 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet24, strArray23);
        htsjdk.variant.vcf.VCFHeader vCFHeader26 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, (java.util.Set<java.lang.String>) strSet24);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader27 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet24);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray14);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray14, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(strArray23);
        org.junit.Assert.assertArrayEquals(strArray23, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + true + "'", boolean25 == true);
    }

    @Test
    public void test067() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test067");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine9 = vCFHeader0.getFormatHeaderLine("##");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion10 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion10);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
        org.junit.Assert.assertNull(vCFFormatHeaderLine9);
    }

    @Test
    public void test068() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test068");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        vCFHeader4.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader4);
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection8 = vCFHeader4.getFormatHeaderLines();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection8);
    }

    @Test
    public void test069() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test069");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        vCFHeader4.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader4);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine8 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader7.addMetaDataLine(vCFHeaderLine8);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
    }

    @Test
    public void test070() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test070");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        boolean boolean4 = vCFHeader3.hasGenotypingData();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator5 = vCFHeader3.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test071() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test071");
        htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS hEADER_FIELDS0 = htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.QUAL;
        org.junit.Assert.assertTrue("'" + hEADER_FIELDS0 + "' != '" + htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.QUAL + "'", hEADER_FIELDS0.equals(htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS.QUAL));
    }

    @Test
    public void test072() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test072");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        java.lang.String[] strArray10 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet11 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet11, strArray10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet11);
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet14 = vCFHeader13.getMetaDataInInputOrder();
        java.util.Set<java.lang.String> strSet15 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader16 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet14, strSet15);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet14);
    }

    @Test
    public void test073() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test073");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary8 = vCFHeader7.getSequenceDictionary();
        vCFHeader7.setWriteEngineHeaders(true);
        java.util.ArrayList<java.lang.String> strList11 = vCFHeader7.getSampleNamesInOrder();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNull(sAMSequenceDictionary8);
        org.junit.Assert.assertNotNull(strList11);
    }

    @Test
    public void test074() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test074");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator12 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
    }

    @Test
    public void test075() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test075");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion12 = vCFHeader0.getVCFHeaderVersion();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet13 = vCFHeader0.getHeaderFields();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion12);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet13);
    }

    @Test
    public void test076() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test076");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion7 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion7);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
    }

    @Test
    public void test077() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test077");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList10 = vCFHeader7.getFilterLines();
        boolean boolean12 = vCFHeader7.hasFilterLine("#");
        vCFHeader7.setWriteCommandLine(true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test078() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test078");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion2 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNull(vCFHeaderVersion2);
    }

    @Test
    public void test079() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test079");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary5 = vCFHeader0.getSequenceDictionary();
        boolean boolean7 = vCFHeader0.hasFilterLine("intervals");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(sAMSequenceDictionary5);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test080() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test080");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        int int4 = vCFHeader0.getColumnCount();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
    }

    @Test
    public void test081() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test081");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        java.lang.String str12 = vCFHeader0.toString();
        int int13 = vCFHeader0.getColumnCount();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "[VCFHeader:\n]" + "'", str12, "[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 8 + "'", int13 == 8);
    }

    @Test
    public void test082() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test082");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine11 = vCFHeader0.getFilterHeaderLine("excludeIntervals");
        boolean boolean12 = vCFHeader0.isWriteCommandLine();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNull(vCFFilterHeaderLine11);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test083() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test083");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList10 = vCFHeader7.getFilterLines();
        boolean boolean12 = vCFHeader7.hasFilterLine("#");
        boolean boolean14 = vCFHeader7.hasInfoLine("intervals");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine15 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader7.addMetaDataLine(vCFHeaderLine15);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test084() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test084");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion2 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderVersion2);
    }

    @Test
    public void test085() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test085");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion6 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion6);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
    }

    @Test
    public void test086() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test086");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary5 = vCFHeader0.getSequenceDictionary();
        int int6 = vCFHeader0.getNGenotypeSamples();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(sAMSequenceDictionary5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test087() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test087");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList2 = vCFHeader0.getFilterLines();
        vCFHeader0.setWriteEngineHeaders(false);
        java.util.ArrayList<java.lang.String> strList5 = vCFHeader0.getSampleNamesInOrder();
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList2);
        org.junit.Assert.assertNotNull(strList5);
    }

    @Test
    public void test088() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test088");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        boolean boolean13 = vCFHeader0.hasFilterLine("contig");
        boolean boolean14 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test089() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test089");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        boolean boolean7 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test090() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test090");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        int int10 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion11 = vCFHeader0.getVCFHeaderVersion();
        boolean boolean12 = vCFHeader0.isWriteEngineHeaders();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 0 + "'", int10 == 0);
        org.junit.Assert.assertNull(vCFHeaderVersion11);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test091() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test091");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList4 = vCFHeader0.getContigLines();
        java.lang.String str5 = vCFHeader0.toString();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList4);
        org.junit.Assert.assertEquals("'" + str5 + "' != '" + "[VCFHeader:\n]" + "'", str5, "[VCFHeader:\n]");
    }

    @Test
    public void test092() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test092");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine5 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine5);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
    }

    @Test
    public void test093() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test093");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray2 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean4 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet3, vCFHeaderLineArray2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet3);
        htsjdk.variant.vcf.VCFHeader vCFHeader6 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet3);
        java.lang.String[] strArray11 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet12 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean13 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet12, strArray11);
        htsjdk.variant.vcf.VCFHeader vCFHeader14 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet3, (java.util.Set<java.lang.String>) strSet12);
        htsjdk.variant.vcf.VCFHeader vCFHeader15 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet3);
        java.lang.String[] strArray22 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.vcf.VCFHeader vCFHeader25 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet3, (java.util.Set<java.lang.String>) strSet23);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader26 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet23);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.iterator()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray2);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray2, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(strArray11);
        org.junit.Assert.assertArrayEquals(strArray11, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
    }

    @Test
    public void test094() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test094");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean3 = vCFHeader1.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet4 = vCFHeader1.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet4);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray6 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean8 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7, vCFHeaderLineArray6);
        htsjdk.variant.vcf.VCFHeader vCFHeader9 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7);
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7);
        java.lang.String[] strArray15 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet16 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean17 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet16, strArray15);
        htsjdk.variant.vcf.VCFHeader vCFHeader18 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7, (java.util.Set<java.lang.String>) strSet16);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet4, (java.util.Set<java.lang.String>) strSet16);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet4);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray6);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray6, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(strArray15);
        org.junit.Assert.assertArrayEquals(strArray15, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
    }

    @Test
    public void test095() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test095");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        java.util.ArrayList<java.lang.String> strList13 = vCFHeader12.getSampleNamesInOrder();
        int int14 = vCFHeader12.getColumnCount();
        htsjdk.variant.vcf.VCFHeader vCFHeader15 = new htsjdk.variant.vcf.VCFHeader(vCFHeader12);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strList13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 13 + "'", int14 == 13);
    }

    @Test
    public void test096() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test096");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList2 = vCFHeader0.getFilterLines();
        vCFHeader0.setWriteEngineHeaders(false);
        boolean boolean6 = vCFHeader0.hasFilterLine("#");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList2);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test097() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test097");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection8 = vCFHeader7.getInfoHeaderLines();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine10 = vCFHeader7.getMetaDataLine("");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet11 = vCFHeader7.getMetaDataInInputOrder();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection8);
        org.junit.Assert.assertNull(vCFHeaderLine10);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet11);
    }

    @Test
    public void test098() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test098");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet13 = vCFHeader0.getHeaderFields();
        boolean boolean14 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean15 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet13);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test099() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test099");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection5 = vCFHeader0.getOtherHeaderLines();
        boolean boolean7 = vCFHeader0.hasFormatLine("reference");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection5);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test100() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test100");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        java.util.ArrayList<java.lang.String> strList13 = vCFHeader12.getSampleNamesInOrder();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap14 = vCFHeader12.getSampleNameToOffset();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strList13);
        org.junit.Assert.assertNotNull(strMap14);
    }

    @Test
    public void test101() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test101");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList10 = vCFHeader0.getContigLines();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap11 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList10);
        org.junit.Assert.assertNotNull(strMap11);
    }

    @Test
    public void test102() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test102");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        vCFHeader4.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader4);
        vCFHeader7.setWriteCommandLine(false);
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection10 = vCFHeader7.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList11 = vCFHeader7.getIDHeaderLines();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection10);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList11);
    }

    @Test
    public void test103() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test103");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
    }

    @Test
    public void test104() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test104");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion6 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion6);
    }

    @Test
    public void test105() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test105");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        java.lang.String[] strArray5 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet6 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean7 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet6, strArray5);
        htsjdk.variant.vcf.VCFHeader vCFHeader8 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet6);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray9 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet10 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet10, vCFHeaderLineArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet10);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray14 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet15 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean16 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, vCFHeaderLineArray14);
        htsjdk.variant.vcf.VCFHeader vCFHeader17 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        htsjdk.variant.vcf.VCFHeader vCFHeader18 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        java.lang.String[] strArray23 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet24 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet24, strArray23);
        htsjdk.variant.vcf.VCFHeader vCFHeader26 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, (java.util.Set<java.lang.String>) strSet24);
        htsjdk.variant.vcf.VCFHeader vCFHeader27 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        java.lang.String[] strArray34 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet35 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean36 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet35, strArray34);
        htsjdk.variant.vcf.VCFHeader vCFHeader37 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, (java.util.Set<java.lang.String>) strSet35);
        htsjdk.variant.vcf.VCFHeader vCFHeader38 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet10, (java.util.Set<java.lang.String>) strSet35);
        htsjdk.variant.vcf.VCFHeader vCFHeader39 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet35);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray40 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet41 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean42 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet41, vCFHeaderLineArray40);
        htsjdk.variant.vcf.VCFHeader vCFHeader43 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet41);
        htsjdk.variant.vcf.VCFHeader vCFHeader44 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet41);
        java.lang.String[] strArray49 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet50 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean51 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet50, strArray49);
        htsjdk.variant.vcf.VCFHeader vCFHeader52 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet41, (java.util.Set<java.lang.String>) strSet50);
        htsjdk.variant.vcf.VCFHeader vCFHeader53 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet41);
        java.lang.String[] strArray60 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet61 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean62 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet61, strArray60);
        htsjdk.variant.vcf.VCFHeader vCFHeader63 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet41, (java.util.Set<java.lang.String>) strSet61);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader64 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet61);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray5);
        org.junit.Assert.assertArrayEquals(strArray5, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray9);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray9, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray14);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray14, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(strArray23);
        org.junit.Assert.assertArrayEquals(strArray23, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + true + "'", boolean25 == true);
        org.junit.Assert.assertNotNull(strArray34);
        org.junit.Assert.assertArrayEquals(strArray34, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + true + "'", boolean36 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray40);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray40, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean42 + "' != '" + false + "'", boolean42 == false);
        org.junit.Assert.assertNotNull(strArray49);
        org.junit.Assert.assertArrayEquals(strArray49, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + true + "'", boolean51 == true);
        org.junit.Assert.assertNotNull(strArray60);
        org.junit.Assert.assertArrayEquals(strArray60, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean62 + "' != '" + true + "'", boolean62 == true);
    }

    @Test
    public void test106() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test106");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        int int9 = vCFHeader0.getColumnCount();
        int int10 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion11 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setVCFHeaderVersion(vCFHeaderVersion11);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 8 + "'", int9 == 8);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 0 + "'", int10 == 0);
    }

    @Test
    public void test107() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test107");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection6 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection7 = vCFHeader0.getOtherHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection8 = vCFHeader0.getInfoHeaderLines();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine9 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine9);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection6);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection7);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection8);
    }

    @Test
    public void test108() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test108");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine8 = vCFHeader0.getInfoHeaderLine("intervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNull(vCFInfoHeaderLine8);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
    }

    @Test
    public void test109() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test109");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList2 = vCFHeader0.getContigLines();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList3 = vCFHeader0.getIDHeaderLines();
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary5 = vCFHeader0.getSequenceDictionary();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList2);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNull(sAMSequenceDictionary5);
    }

    @Test
    public void test110() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test110");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        boolean boolean3 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        boolean boolean5 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary6 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary6);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
    }

    @Test
    public void test111() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test111");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        int int9 = vCFHeader0.getColumnCount();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap10 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 8 + "'", int9 == 8);
        org.junit.Assert.assertNotNull(strMap10);
    }

    @Test
    public void test112() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test112");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean3 = vCFHeader1.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet4 = vCFHeader1.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet4);
        htsjdk.variant.vcf.VCFHeader vCFHeader6 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet4);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray7 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet8 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean9 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet8, vCFHeaderLineArray7);
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet8);
        htsjdk.variant.vcf.VCFHeader vCFHeader11 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet8);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray12 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet13 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet13, vCFHeaderLineArray12);
        htsjdk.variant.vcf.VCFHeader vCFHeader15 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet13);
        htsjdk.variant.vcf.VCFHeader vCFHeader16 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet13);
        java.lang.String[] strArray21 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet22 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean23 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet22, strArray21);
        htsjdk.variant.vcf.VCFHeader vCFHeader24 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet13, (java.util.Set<java.lang.String>) strSet22);
        htsjdk.variant.vcf.VCFHeader vCFHeader25 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet13);
        java.lang.String[] strArray32 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet33 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean34 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet33, strArray32);
        htsjdk.variant.vcf.VCFHeader vCFHeader35 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet13, (java.util.Set<java.lang.String>) strSet33);
        htsjdk.variant.vcf.VCFHeader vCFHeader36 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet8, (java.util.Set<java.lang.String>) strSet33);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader37 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet4, (java.util.Set<java.lang.String>) strSet33);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet4);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray7);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray7, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray12);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray12, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray21);
        org.junit.Assert.assertArrayEquals(strArray21, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + true + "'", boolean23 == true);
        org.junit.Assert.assertNotNull(strArray32);
        org.junit.Assert.assertArrayEquals(strArray32, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
    }

    @Test
    public void test113() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test113");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.List<java.lang.String> strList9 = vCFHeader7.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader(vCFHeader7);
        java.util.List<java.lang.String> strList11 = vCFHeader7.getGenotypeSamples();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(strList9);
        org.junit.Assert.assertNotNull(strList11);
    }

    @Test
    public void test114() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test114");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        boolean boolean13 = vCFHeader12.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine15 = vCFHeader12.getOtherHeaderLine("[VCFHeader:\n]");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNull(vCFHeaderLine15);
    }

    @Test
    public void test115() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test115");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet0 = null;
        htsjdk.variant.vcf.VCFHeader vCFHeader1 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader1.isWriteEngineHeaders();
        boolean boolean4 = vCFHeader1.hasFormatLine("");
        java.util.List<java.lang.String> strList5 = vCFHeader1.getGenotypeSamples();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader6 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet0, strList5);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.iterator()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + true + "'", boolean2 == true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(strList5);
    }

    @Test
    public void test116() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test116");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        java.util.List<java.lang.String> strList2 = vCFHeader0.getGenotypeSamples();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine5 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(strList2);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNull(vCFFormatHeaderLine5);
    }

    @Test
    public void test117() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test117");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        boolean boolean13 = vCFHeader0.hasFilterLine("contig");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine14 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine14);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test118() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test118");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteCommandLine(true);
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList4 = vCFHeader0.getContigLines();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("hi!");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine7 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine7);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList4);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
    }

    @Test
    public void test119() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test119");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary2 = vCFHeader0.getSequenceDictionary();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator3 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNull(sAMSequenceDictionary2);
    }

    @Test
    public void test120() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test120");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary10 = vCFHeader0.getSequenceDictionary();
        java.util.ArrayList<java.lang.String> strList11 = vCFHeader0.getSampleNamesInOrder();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine13 = vCFHeader0.getFormatHeaderLine("interval_padding");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNull(sAMSequenceDictionary10);
        org.junit.Assert.assertNotNull(strList11);
        org.junit.Assert.assertNull(vCFFormatHeaderLine13);
    }

    @Test
    public void test121() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test121");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary10 = vCFHeader0.getSequenceDictionary();
        java.lang.String str11 = vCFHeader0.toString();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNull(sAMSequenceDictionary10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "[VCFHeader:\n]" + "'", str11, "[VCFHeader:\n]");
    }

    @Test
    public void test122() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test122");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList10 = vCFHeader7.getFilterLines();
        boolean boolean12 = vCFHeader7.hasFilterLine("#");
        vCFHeader7.setWriteEngineHeaders(true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test123() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test123");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList4 = vCFHeader0.getFilterLines();
        vCFHeader0.setWriteCommandLine(true);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator7 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList4);
    }

    @Test
    public void test124() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test124");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine3 = vCFHeader0.getFormatHeaderLine("");
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection4 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFormatHeaderLine3);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection4);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
    }

    @Test
    public void test125() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test125");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        vCFHeader4.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader4);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator8 = vCFHeader7.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
    }

    @Test
    public void test126() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test126");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        int int10 = vCFHeader0.getNGenotypeSamples();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap11 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 0 + "'", int10 == 0);
        org.junit.Assert.assertNotNull(strMap11);
    }

    @Test
    public void test127() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test127");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection6 = vCFHeader0.getInfoHeaderLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet7 = vCFHeader0.getHeaderFields();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection6);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet7);
    }

    @Test
    public void test128() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test128");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet4 = vCFHeader0.getMetaDataInInputOrder();
        boolean boolean5 = vCFHeader0.isWriteEngineHeaders();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet4);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
    }

    @Test
    public void test129() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test129");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        boolean boolean11 = vCFHeader0.hasFormatLine("intervals");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
    }

    @Test
    public void test130() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test130");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine5 = vCFHeader0.getInfoHeaderLine("excludeIntervals");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean8 = vCFHeader0.samplesWereAlreadySorted();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNull(vCFInfoHeaderLine5);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + true + "'", boolean8 == true);
    }

    @Test
    public void test131() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test131");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteCommandLine(true);
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList7 = vCFHeader0.getContigLines();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList7);
    }

    @Test
    public void test132() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test132");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine3 = vCFHeader0.getFormatHeaderLine("");
        boolean boolean4 = vCFHeader0.hasGenotypingData();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet5 = vCFHeader0.getMetaDataInSortedOrder();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFormatHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet5);
    }

    @Test
    public void test133() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test133");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection6 = vCFHeader0.getInfoHeaderLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInSortedOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
    }

    @Test
    public void test134() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test134");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine5 = vCFHeader0.getFilterHeaderLine("[VCFHeader:\n]");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertNull(vCFFilterHeaderLine5);
    }

    @Test
    public void test135() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test135");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean12 = vCFHeader10.hasFormatLine("reference");
        java.util.List<java.lang.String> strList13 = vCFHeader10.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeader vCFHeader14 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet9, strList13);
        boolean boolean15 = vCFHeader14.hasGenotypingData();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(strList13);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test136() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test136");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        int int6 = vCFHeader0.getNGenotypeSamples();
        boolean boolean8 = vCFHeader0.hasInfoLine("[VCFHeader:\n]");
        boolean boolean9 = vCFHeader0.samplesWereAlreadySorted();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test137() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test137");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        boolean boolean5 = vCFHeader0.hasFormatLine("interval_set_rule");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
    }

    @Test
    public void test138() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test138");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        boolean boolean3 = vCFHeader0.hasFormatLine("interval_set_rule");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
    }

    @Test
    public void test139() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test139");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList2 = vCFHeader0.getContigLines();
        vCFHeader0.setWriteEngineHeaders(false);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList2);
    }

    @Test
    public void test140() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test140");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        java.util.ArrayList<java.lang.String> strList13 = vCFHeader12.getSampleNamesInOrder();
        boolean boolean15 = vCFHeader12.hasFilterLine("hi!");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strList13);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test141() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test141");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine14 = vCFHeader0.getInfoHeaderLine("reference");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNull(vCFInfoHeaderLine14);
    }

    @Test
    public void test142() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test142");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray6 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean8 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7, vCFHeaderLineArray6);
        java.lang.String[] strArray10 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet11 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet11, strArray10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7, (java.util.Set<java.lang.String>) strSet11);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray14 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet15 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean16 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, vCFHeaderLineArray14);
        htsjdk.variant.vcf.VCFHeader vCFHeader17 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        htsjdk.variant.vcf.VCFHeader vCFHeader18 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray19 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet20 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean21 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet20, vCFHeaderLineArray19);
        htsjdk.variant.vcf.VCFHeader vCFHeader22 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet20);
        htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet20);
        java.lang.String[] strArray28 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet29 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean30 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet29, strArray28);
        htsjdk.variant.vcf.VCFHeader vCFHeader31 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet20, (java.util.Set<java.lang.String>) strSet29);
        htsjdk.variant.vcf.VCFHeader vCFHeader32 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet20);
        java.lang.String[] strArray39 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet40 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet40, strArray39);
        htsjdk.variant.vcf.VCFHeader vCFHeader42 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet20, (java.util.Set<java.lang.String>) strSet40);
        htsjdk.variant.vcf.VCFHeader vCFHeader43 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet15, (java.util.Set<java.lang.String>) strSet40);
        htsjdk.variant.vcf.VCFHeader vCFHeader44 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet7, (java.util.Set<java.lang.String>) strSet40);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader45 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet40);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray6);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray6, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray14);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray14, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray19);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray19, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + false + "'", boolean21 == false);
        org.junit.Assert.assertNotNull(strArray28);
        org.junit.Assert.assertArrayEquals(strArray28, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + true + "'", boolean30 == true);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
    }

    @Test
    public void test143() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test143");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary8 = vCFHeader7.getSequenceDictionary();
        vCFHeader7.setWriteEngineHeaders(true);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine12 = vCFHeader7.getOtherHeaderLine("intervals");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine14 = vCFHeader7.getFilterHeaderLine("contig");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNull(sAMSequenceDictionary8);
        org.junit.Assert.assertNull(vCFHeaderLine12);
        org.junit.Assert.assertNull(vCFFilterHeaderLine14);
    }

    @Test
    public void test144() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test144");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine3 = vCFHeader0.getFormatHeaderLine("");
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection4 = vCFHeader0.getInfoHeaderLines();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet7 = vCFHeader0.getHeaderFields();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFormatHeaderLine3);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection4);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet7);
    }

    @Test
    public void test145() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test145");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        java.util.List<java.lang.String> strList2 = vCFHeader0.getGenotypeSamples();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine5 = vCFHeader0.getFilterHeaderLine("contig");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(strList2);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNull(vCFFilterHeaderLine5);
    }

    @Test
    public void test146() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test146");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary1 = vCFHeader0.getSequenceDictionary();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion2 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary3 = vCFHeader0.getSequenceDictionary();
        org.junit.Assert.assertNull(sAMSequenceDictionary1);
        org.junit.Assert.assertNull(vCFHeaderVersion2);
        org.junit.Assert.assertNull(sAMSequenceDictionary3);
    }

    @Test
    public void test147() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test147");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        java.lang.String[] strArray10 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet11 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet11, strArray10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet11);
        htsjdk.variant.vcf.VCFHeader vCFHeader14 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        java.lang.String[] strArray21 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet22 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean23 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet22, strArray21);
        htsjdk.variant.vcf.VCFHeader vCFHeader24 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet22);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray25 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet26 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet26, vCFHeaderLineArray25);
        htsjdk.variant.vcf.VCFHeader vCFHeader28 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet26);
        htsjdk.variant.vcf.VCFHeader vCFHeader29 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet26);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray30 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet31 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean32 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet31, vCFHeaderLineArray30);
        htsjdk.variant.vcf.VCFHeader vCFHeader33 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet31);
        htsjdk.variant.vcf.VCFHeader vCFHeader34 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet31);
        java.lang.String[] strArray39 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet40 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet40, strArray39);
        htsjdk.variant.vcf.VCFHeader vCFHeader42 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet31, (java.util.Set<java.lang.String>) strSet40);
        htsjdk.variant.vcf.VCFHeader vCFHeader43 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet31);
        java.lang.String[] strArray50 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet51 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean52 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet51, strArray50);
        htsjdk.variant.vcf.VCFHeader vCFHeader53 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet31, (java.util.Set<java.lang.String>) strSet51);
        htsjdk.variant.vcf.VCFHeader vCFHeader54 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet26, (java.util.Set<java.lang.String>) strSet51);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader55 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, (java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet51);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(strArray21);
        org.junit.Assert.assertArrayEquals(strArray21, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + true + "'", boolean23 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray25);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray25, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray30);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray30, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(strArray50);
        org.junit.Assert.assertArrayEquals(strArray50, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean52 + "' != '" + true + "'", boolean52 == true);
    }

    @Test
    public void test148() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test148");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getOtherHeaderLine("");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFHeaderLine3);
    }

    @Test
    public void test149() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test149");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine2 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean3 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean5 = vCFHeader0.hasFilterLine("[VCFHeader:\n]");
        org.junit.Assert.assertNull(vCFInfoHeaderLine2);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
    }

    @Test
    public void test150() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test150");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        java.util.List<java.lang.String> strList4 = vCFHeader0.getGenotypeSamples();
        boolean boolean6 = vCFHeader0.hasFilterLine("intervals");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strList4);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test151() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test151");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet4 = vCFHeader0.getHeaderFields();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet4);
    }

    @Test
    public void test152() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test152");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        boolean boolean9 = vCFHeader0.hasInfoLine("interval_padding");
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test153() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test153");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet13 = vCFHeader0.getHeaderFields();
        java.util.ArrayList<java.lang.String> strList14 = vCFHeader0.getSampleNamesInOrder();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection15 = vCFHeader0.getInfoHeaderLines();
        boolean boolean16 = vCFHeader0.isWriteCommandLine();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet13);
        org.junit.Assert.assertNotNull(strList14);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
    }

    @Test
    public void test154() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test154");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet5 = vCFHeader0.getHeaderFields();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine7 = vCFHeader0.getFilterHeaderLine("reference");
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet5);
        org.junit.Assert.assertNull(vCFFilterHeaderLine7);
    }

    @Test
    public void test155() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test155");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList2 = vCFHeader0.getContigLines();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList3 = vCFHeader0.getIDHeaderLines();
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine5 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine5);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList2);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
    }

    @Test
    public void test156() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test156");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean7 = vCFHeader0.samplesWereAlreadySorted();
        int int8 = vCFHeader0.getColumnCount();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 8 + "'", int8 == 8);
    }

    @Test
    public void test157() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test157");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("");
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList12 = vCFHeader0.getContigLines();
        boolean boolean13 = vCFHeader0.isWriteCommandLine();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test158() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test158");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine5 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean6 = vCFHeader0.hasGenotypingData();
        java.util.List<java.lang.String> strList7 = vCFHeader0.getGenotypeSamples();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertNull(vCFInfoHeaderLine5);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(strList7);
    }

    @Test
    public void test159() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test159");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion0 = null;
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray1 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet2 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean3 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, vCFHeaderLineArray1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2);
        java.lang.String[] strArray10 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet11 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet11, strArray10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet2, (java.util.Set<java.lang.String>) strSet11);
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet14 = vCFHeader13.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray15 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet16 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean17 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet16, vCFHeaderLineArray15);
        java.lang.String[] strArray19 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet20 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean21 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet20, strArray19);
        htsjdk.variant.vcf.VCFHeader vCFHeader22 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet16, (java.util.Set<java.lang.String>) strSet20);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderVersion0, vCFHeaderLineSet14, (java.util.Set<java.lang.String>) strSet20);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: object cannot be null.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray1);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray1, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet14);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray15);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray15, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
    }

    @Test
    public void test160() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test160");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean5 = vCFHeader4.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine7 = vCFHeader4.getMetaDataLine("");
        int int8 = vCFHeader4.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine10 = vCFHeader4.getFilterHeaderLine("interval_merging");
        boolean boolean12 = vCFHeader4.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine14 = vCFHeader4.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine16 = vCFHeader4.getFormatHeaderLine("interval_set_rule");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet17 = vCFHeader4.getHeaderFields();
        java.util.ArrayList<java.lang.String> strList18 = vCFHeader4.getSampleNamesInOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3, (java.util.List<java.lang.String>) strList18);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary20 = vCFHeader19.getSequenceDictionary();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet3);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertNull(vCFHeaderLine7);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 8 + "'", int8 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine14);
        org.junit.Assert.assertNull(vCFFormatHeaderLine16);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet17);
        org.junit.Assert.assertNotNull(strList18);
        org.junit.Assert.assertNull(sAMSequenceDictionary20);
    }

    @Test
    public void test161() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test161");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        int int10 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion11 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary12 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary12);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 0 + "'", int10 == 0);
        org.junit.Assert.assertNull(vCFHeaderVersion11);
    }

    @Test
    public void test162() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test162");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet9);
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection11 = vCFHeader10.getFormatHeaderLines();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection11);
    }

    @Test
    public void test163() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test163");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet9);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray11 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet12 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean13 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet12, vCFHeaderLineArray11);
        htsjdk.variant.vcf.VCFHeader vCFHeader14 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet12);
        htsjdk.variant.vcf.VCFHeader vCFHeader15 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet12);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray16 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet17 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17, vCFHeaderLineArray16);
        htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17);
        htsjdk.variant.vcf.VCFHeader vCFHeader20 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17);
        java.lang.String[] strArray25 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet26 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet26, strArray25);
        htsjdk.variant.vcf.VCFHeader vCFHeader28 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17, (java.util.Set<java.lang.String>) strSet26);
        htsjdk.variant.vcf.VCFHeader vCFHeader29 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17);
        java.lang.String[] strArray36 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet37 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean38 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet37, strArray36);
        htsjdk.variant.vcf.VCFHeader vCFHeader39 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17, (java.util.Set<java.lang.String>) strSet37);
        htsjdk.variant.vcf.VCFHeader vCFHeader40 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet12, (java.util.Set<java.lang.String>) strSet37);
        htsjdk.variant.vcf.VCFHeader vCFHeader41 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet9, (java.util.Set<java.lang.String>) strSet37);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray11);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray11, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray16);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray16, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(strArray25);
        org.junit.Assert.assertArrayEquals(strArray25, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + true + "'", boolean27 == true);
        org.junit.Assert.assertNotNull(strArray36);
        org.junit.Assert.assertArrayEquals(strArray36, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean38 + "' != '" + true + "'", boolean38 == true);
    }

    @Test
    public void test164() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test164");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary2 = vCFHeader0.getSequenceDictionary();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine4 = vCFHeader0.getInfoHeaderLine("interval_merging");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNull(sAMSequenceDictionary2);
        org.junit.Assert.assertNull(vCFInfoHeaderLine4);
    }

    @Test
    public void test165() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test165");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine14 = vCFHeader0.getFilterHeaderLine("reference");
        htsjdk.variant.vcf.VCFHeader vCFHeader15 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNull(vCFFilterHeaderLine14);
    }

    @Test
    public void test166() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test166");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList2 = vCFHeader0.getContigLines();
        boolean boolean4 = vCFHeader0.hasFormatLine("[VCFHeader:\n]");
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection5 = vCFHeader0.getFormatHeaderLines();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList2);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection5);
    }

    @Test
    public void test167() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test167");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList4 = vCFHeader0.getFilterLines();
        java.util.List<java.lang.String> strList5 = vCFHeader0.getGenotypeSamples();
        java.lang.Class<?> wildcardClass6 = vCFHeader0.getClass();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList4);
        org.junit.Assert.assertNotNull(strList5);
        org.junit.Assert.assertNotNull(wildcardClass6);
    }

    @Test
    public void test168() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test168");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.hasGenotypingData();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList5 = vCFHeader0.getIDHeaderLines();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine7 = vCFHeader0.getFilterHeaderLine("#");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList5);
        org.junit.Assert.assertNull(vCFFilterHeaderLine7);
    }

    @Test
    public void test169() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test169");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
    }

    @Test
    public void test170() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test170");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList5 = vCFHeader0.getFilterLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList6 = vCFHeader0.getContigLines();
        boolean boolean7 = vCFHeader0.samplesWereAlreadySorted();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine9 = vCFHeader0.getFormatHeaderLine("intervals");
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList5);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertNull(vCFFormatHeaderLine9);
    }

    @Test
    public void test171() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test171");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection10 = vCFHeader0.getInfoHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList11 = vCFHeader0.getContigLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection10);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList11);
    }

    @Test
    public void test172() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test172");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine5 = vCFHeader0.getOtherHeaderLine("#");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine6 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine6);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNull(vCFHeaderLine5);
    }

    @Test
    public void test173() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test173");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        java.util.List<java.lang.String> strList2 = vCFHeader0.getGenotypeSamples();
        java.util.List<java.lang.String> strList3 = vCFHeader0.getGenotypeSamples();
        boolean boolean4 = vCFHeader0.isWriteCommandLine();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(strList2);
        org.junit.Assert.assertNotNull(strList3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
    }

    @Test
    public void test174() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test174");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet5 = vCFHeader0.getHeaderFields();
        java.lang.String str6 = vCFHeader0.toString();
        java.lang.Class<?> wildcardClass7 = vCFHeader0.getClass();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "[VCFHeader:\n]" + "'", str6, "[VCFHeader:\n]");
        org.junit.Assert.assertNotNull(wildcardClass7);
    }

    @Test
    public void test175() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test175");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine5 = vCFHeader0.getMetaDataLine("source");
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet3);
        org.junit.Assert.assertNull(vCFHeaderLine5);
    }

    @Test
    public void test176() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test176");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine9 = vCFHeader0.getMetaDataLine("");
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection10 = vCFHeader0.getFormatHeaderLines();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNull(vCFHeaderLine9);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection10);
    }

    @Test
    public void test177() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test177");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet5 = vCFHeader0.getMetaDataInSortedOrder();
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean8 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet5);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test178() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test178");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("contig");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine5 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertNull(vCFFormatHeaderLine5);
    }

    @Test
    public void test179() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test179");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection5 = vCFHeader0.getOtherHeaderLines();
        java.lang.String str6 = vCFHeader0.toString();
        boolean boolean7 = vCFHeader0.isWriteCommandLine();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "[VCFHeader:\n]" + "'", str6, "[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
    }

    @Test
    public void test180() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test180");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection6 = vCFHeader0.getInfoHeaderLines();
        vCFHeader0.setWriteCommandLine(true);
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection9 = vCFHeader0.getInfoHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection6);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection9);
    }

    @Test
    public void test181() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test181");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray20 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet21 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet21, strArray20);
        htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet21);
        vCFHeader23.setWriteCommandLine(false);
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion26 = vCFHeader23.getVCFHeaderVersion();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNull(vCFHeaderVersion26);
    }

    @Test
    public void test182() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test182");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection8 = vCFHeader7.getInfoHeaderLines();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader7.getSequenceDictionary();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection8);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
    }

    @Test
    public void test183() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test183");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean7 = vCFHeader0.samplesWereAlreadySorted();
        java.util.List<java.lang.String> strList8 = vCFHeader0.getGenotypeSamples();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertNotNull(strList8);
    }

    @Test
    public void test184() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test184");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        boolean boolean5 = vCFHeader4.samplesWereAlreadySorted();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList6 = vCFHeader4.getFilterLines();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList6);
    }

    @Test
    public void test185() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test185");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        java.lang.String str12 = vCFHeader0.toString();
        boolean boolean14 = vCFHeader0.hasFilterLine("interval_merging");
        boolean boolean16 = vCFHeader0.hasInfoLine("[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "[VCFHeader:\n]" + "'", str12, "[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
    }

    @Test
    public void test186() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test186");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine8 = vCFHeader0.getInfoHeaderLine("intervals");
        htsjdk.variant.vcf.VCFHeader vCFHeader9 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet10 = vCFHeader0.getMetaDataInSortedOrder();
        java.lang.String[] strArray21 = new java.lang.String[] { "[VCFHeader:\n]", "interval_merging", "interval_padding", "reference", "interval_padding", "reference", "##", "interval_merging", "contig", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet22 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean23 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet22, strArray21);
        htsjdk.variant.vcf.VCFHeader vCFHeader24 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet10, (java.util.Set<java.lang.String>) strSet22);
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNull(vCFInfoHeaderLine8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet10);
        org.junit.Assert.assertNotNull(strArray21);
        org.junit.Assert.assertArrayEquals(strArray21, new java.lang.String[] { "[VCFHeader:\n]", "interval_merging", "interval_padding", "reference", "interval_padding", "reference", "##", "interval_merging", "contig", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + true + "'", boolean23 == true);
    }

    @Test
    public void test187() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test187");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary12 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary12);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
    }

    @Test
    public void test188() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test188");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.lang.String str5 = vCFHeader0.toString();
        htsjdk.variant.vcf.VCFHeader vCFHeader6 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertEquals("'" + str5 + "' != '" + "[VCFHeader:\n]" + "'", str5, "[VCFHeader:\n]");
    }

    @Test
    public void test189() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test189");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList5 = vCFHeader0.getFilterLines();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine7 = vCFHeader0.getMetaDataLine("");
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList5);
        org.junit.Assert.assertNull(vCFHeaderLine7);
    }

    @Test
    public void test190() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test190");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean6 = vCFHeader0.hasFilterLine("");
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection8 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection9 = vCFHeader0.getInfoHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection10 = vCFHeader0.getOtherHeaderLines();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection9);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection10);
    }

    @Test
    public void test191() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test191");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean6 = vCFHeader0.hasFilterLine("");
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection8 = vCFHeader0.getOtherHeaderLines();
        boolean boolean9 = vCFHeader0.samplesWereAlreadySorted();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection8);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test192() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test192");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean12 = vCFHeader10.hasFormatLine("reference");
        java.util.List<java.lang.String> strList13 = vCFHeader10.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeader vCFHeader14 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet9, strList13);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine16 = vCFHeader14.getMetaDataLine("#");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(strList13);
        org.junit.Assert.assertNull(vCFHeaderLine16);
    }

    @Test
    public void test193() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test193");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary11 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary11);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
    }

    @Test
    public void test194() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test194");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine3 = vCFHeader0.getFormatHeaderLine("");
        boolean boolean4 = vCFHeader0.hasGenotypingData();
        boolean boolean5 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteEngineHeaders(true);
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFormatHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
    }

    @Test
    public void test195() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test195");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean7 = vCFHeader0.samplesWereAlreadySorted();
        java.util.ArrayList<java.lang.String> strList8 = vCFHeader0.getSampleNamesInOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertNotNull(strList8);
    }

    @Test
    public void test196() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test196");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray20 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet21 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet21, strArray20);
        htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet21);
        boolean boolean25 = vCFHeader23.hasFilterLine("interval_merging");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet26 = vCFHeader23.getHeaderFields();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet26);
    }

    @Test
    public void test197() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test197");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection7 = vCFHeader0.getFormatHeaderLines();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection7);
    }

    @Test
    public void test198() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test198");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList2 = vCFHeader0.getFilterLines();
        vCFHeader0.setWriteEngineHeaders(false);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine6 = vCFHeader0.getMetaDataLine("##");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList2);
        org.junit.Assert.assertNull(vCFHeaderLine6);
    }

    @Test
    public void test199() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test199");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.List<java.lang.String> strList3 = vCFHeader0.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine6 = vCFHeader0.getMetaDataLine("source");
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strList3);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
        org.junit.Assert.assertNull(vCFHeaderLine6);
    }

    @Test
    public void test200() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test200");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean5 = vCFHeader4.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine7 = vCFHeader4.getMetaDataLine("");
        int int8 = vCFHeader4.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine10 = vCFHeader4.getFilterHeaderLine("interval_merging");
        boolean boolean12 = vCFHeader4.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine14 = vCFHeader4.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine16 = vCFHeader4.getFormatHeaderLine("interval_set_rule");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet17 = vCFHeader4.getHeaderFields();
        java.util.ArrayList<java.lang.String> strList18 = vCFHeader4.getSampleNamesInOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3, (java.util.List<java.lang.String>) strList18);
        boolean boolean20 = vCFHeader19.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet3);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertNull(vCFHeaderLine7);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 8 + "'", int8 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine14);
        org.junit.Assert.assertNull(vCFFormatHeaderLine16);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet17);
        org.junit.Assert.assertNotNull(strList18);
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
    }

    @Test
    public void test201() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test201");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        vCFHeader0.setWriteCommandLine(true);
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList7 = vCFHeader0.getContigLines();
        java.util.ArrayList<java.lang.String> strList8 = vCFHeader0.getSampleNamesInOrder();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection9 = vCFHeader0.getInfoHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList7);
        org.junit.Assert.assertNotNull(strList8);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection9);
    }

    @Test
    public void test202() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test202");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        boolean boolean12 = vCFHeader0.isWriteEngineHeaders();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test203() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test203");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader6 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
    }

    @Test
    public void test204() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test204");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine5 = vCFHeader0.getInfoHeaderLine("excludeIntervals");
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap6 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNull(vCFInfoHeaderLine5);
        org.junit.Assert.assertNotNull(strMap6);
    }

    @Test
    public void test205() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test205");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList8 = vCFHeader0.getIDHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList8);
    }

    @Test
    public void test206() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test206");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("[VCFHeader:\n]");
        vCFHeader0.setWriteEngineHeaders(true);
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFHeaderLine3);
    }

    @Test
    public void test207() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test207");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList5 = vCFHeader0.getFilterLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList6 = vCFHeader0.getContigLines();
        boolean boolean7 = vCFHeader0.samplesWereAlreadySorted();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator8 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList5);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
    }

    @Test
    public void test208() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test208");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        java.lang.String str12 = vCFHeader0.toString();
        java.lang.String str13 = vCFHeader0.toString();
        boolean boolean14 = vCFHeader0.isWriteEngineHeaders();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "[VCFHeader:\n]" + "'", str12, "[VCFHeader:\n]");
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "[VCFHeader:\n]" + "'", str13, "[VCFHeader:\n]");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
    }

    @Test
    public void test209() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test209");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine8 = vCFHeader0.getInfoHeaderLine("intervals");
        htsjdk.variant.vcf.VCFHeader vCFHeader9 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion10 = vCFHeader9.getVCFHeaderVersion();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection11 = vCFHeader9.getInfoHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNull(vCFInfoHeaderLine8);
        org.junit.Assert.assertNull(vCFHeaderVersion10);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection11);
    }

    @Test
    public void test210() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test210");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray8 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9, vCFHeaderLineArray8);
        java.lang.String[] strArray12 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet13 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet13, strArray12);
        htsjdk.variant.vcf.VCFHeader vCFHeader15 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9, (java.util.Set<java.lang.String>) strSet13);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray16 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet17 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17, vCFHeaderLineArray16);
        htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17);
        htsjdk.variant.vcf.VCFHeader vCFHeader20 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray21 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet22 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean23 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet22, vCFHeaderLineArray21);
        htsjdk.variant.vcf.VCFHeader vCFHeader24 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet22);
        htsjdk.variant.vcf.VCFHeader vCFHeader25 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet22);
        java.lang.String[] strArray30 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet31 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean32 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet31, strArray30);
        htsjdk.variant.vcf.VCFHeader vCFHeader33 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet22, (java.util.Set<java.lang.String>) strSet31);
        htsjdk.variant.vcf.VCFHeader vCFHeader34 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet22);
        java.lang.String[] strArray41 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet42 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet42, strArray41);
        htsjdk.variant.vcf.VCFHeader vCFHeader44 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet22, (java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.vcf.VCFHeader vCFHeader45 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet17, (java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.vcf.VCFHeader vCFHeader46 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9, (java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.vcf.VCFHeader vCFHeader47 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet7, (java.util.Set<java.lang.String>) strSet42);
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet48 = vCFHeader47.getMetaDataInSortedOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray8);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray8, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray16);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray16, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray21);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray21, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertNotNull(strArray30);
        org.junit.Assert.assertArrayEquals(strArray30, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet48);
    }

    @Test
    public void test211() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test211");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3);
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3);
        java.util.List<java.lang.String> strList6 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3, strList6);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.List.size()\" because \"genotypeSampleNames\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet3);
    }

    @Test
    public void test212() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test212");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary4 = vCFHeader0.getSequenceDictionary();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary5 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary5);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary4);
    }

    @Test
    public void test213() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test213");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection7 = vCFHeader0.getOtherHeaderLines();
        vCFHeader0.setWriteCommandLine(false);
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection7);
    }

    @Test
    public void test214() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test214");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList10 = vCFHeader7.getFilterLines();
        boolean boolean12 = vCFHeader7.hasFilterLine("#");
        boolean boolean14 = vCFHeader7.hasInfoLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet15 = vCFHeader7.getHeaderFields();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet15);
    }

    @Test
    public void test215() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test215");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine5 = vCFHeader0.getInfoHeaderLine("reference");
        vCFHeader0.setWriteCommandLine(false);
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList8 = vCFHeader0.getContigLines();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertNull(vCFInfoHeaderLine5);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList8);
    }

    @Test
    public void test216() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test216");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList10 = vCFHeader0.getIDHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList10);
    }

    @Test
    public void test217() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test217");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteCommandLine(true);
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList4 = vCFHeader0.getContigLines();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("hi!");
        boolean boolean7 = vCFHeader0.hasGenotypingData();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList4);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test218() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test218");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray20 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet21 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet21, strArray20);
        htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet21);
        boolean boolean25 = vCFHeader23.hasFilterLine("interval_merging");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary26 = vCFHeader23.getSequenceDictionary();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary26);
    }

    @Test
    public void test219() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test219");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.hasGenotypingData();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList5 = vCFHeader0.getIDHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList6 = vCFHeader0.getContigLines();
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList5);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList6);
    }

    @Test
    public void test220() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test220");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray20 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet21 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet21, strArray20);
        htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet21);
        vCFHeader23.setWriteCommandLine(false);
        vCFHeader23.setWriteEngineHeaders(false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
    }

    @Test
    public void test221() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test221");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet5 = vCFHeader0.getHeaderFields();
        java.lang.String str6 = vCFHeader0.toString();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "[VCFHeader:\n]" + "'", str6, "[VCFHeader:\n]");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
    }

    @Test
    public void test222() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test222");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet3 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean5 = vCFHeader4.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine7 = vCFHeader4.getMetaDataLine("");
        int int8 = vCFHeader4.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine10 = vCFHeader4.getFilterHeaderLine("interval_merging");
        boolean boolean12 = vCFHeader4.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine14 = vCFHeader4.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine16 = vCFHeader4.getFormatHeaderLine("interval_set_rule");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet17 = vCFHeader4.getHeaderFields();
        java.util.ArrayList<java.lang.String> strList18 = vCFHeader4.getSampleNamesInOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader19 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet3, (java.util.List<java.lang.String>) strList18);
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine21 = vCFHeader19.getFormatHeaderLine("interval_merging");
        java.lang.String str22 = vCFHeader19.toString();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet3);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertNull(vCFHeaderLine7);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 8 + "'", int8 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine14);
        org.junit.Assert.assertNull(vCFFormatHeaderLine16);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet17);
        org.junit.Assert.assertNotNull(strList18);
        org.junit.Assert.assertNull(vCFFormatHeaderLine21);
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "[VCFHeader:\n]" + "'", str22, "[VCFHeader:\n]");
    }

    @Test
    public void test223() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test223");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine5 = vCFHeader0.getOtherHeaderLine("#");
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap6 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNull(vCFHeaderLine5);
        org.junit.Assert.assertNotNull(strMap6);
    }

    @Test
    public void test224() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test224");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("");
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection12 = vCFHeader0.getFormatHeaderLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet13 = vCFHeader0.getMetaDataInSortedOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection12);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet13);
    }

    @Test
    public void test225() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test225");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine4 = vCFHeader0.getFilterHeaderLine("interval_padding");
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNull(vCFFilterHeaderLine4);
    }

    @Test
    public void test226() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test226");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine8 = vCFHeader0.getInfoHeaderLine("intervals");
        htsjdk.variant.vcf.VCFHeader vCFHeader9 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet10 = vCFHeader0.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader11 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet10);
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNull(vCFInfoHeaderLine8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet10);
    }

    @Test
    public void test227() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test227");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary8 = vCFHeader7.getSequenceDictionary();
        vCFHeader7.setWriteEngineHeaders(true);
        java.lang.String str11 = vCFHeader7.toString();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNull(sAMSequenceDictionary8);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "[VCFHeader:\n]" + "'", str11, "[VCFHeader:\n]");
    }

    @Test
    public void test228() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test228");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        boolean boolean10 = vCFHeader7.samplesWereAlreadySorted();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList11 = vCFHeader7.getIDHeaderLines();
        boolean boolean13 = vCFHeader7.hasInfoLine("excludeIntervals");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList11);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test229() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test229");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.vcf.VCFHeader vCFHeader13 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray20 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet21 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet21, strArray20);
        htsjdk.variant.vcf.VCFHeader vCFHeader23 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet21);
        vCFHeader23.setWriteEngineHeaders(false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
    }

    @Test
    public void test230() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test230");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean11 = vCFHeader0.hasGenotypingData();
        java.lang.String str12 = vCFHeader0.toString();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet13 = vCFHeader0.getMetaDataInInputOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "[VCFHeader:\n]" + "'", str12, "[VCFHeader:\n]");
        org.junit.Assert.assertNotNull(vCFHeaderLineSet13);
    }

    @Test
    public void test231() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test231");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection10 = vCFHeader0.getInfoHeaderLines();
        java.util.ArrayList<java.lang.String> strList11 = vCFHeader0.getSampleNamesInOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection10);
        org.junit.Assert.assertNotNull(strList11);
    }

    @Test
    public void test232() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test232");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet5 = vCFHeader0.getHeaderFields();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet6 = vCFHeader0.getMetaDataInInputOrder();
        int int7 = vCFHeader0.getNGenotypeSamples();
        boolean boolean9 = vCFHeader0.hasInfoLine("source");
        java.util.ArrayList<java.lang.String> strList10 = vCFHeader0.getSampleNamesInOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet5);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet6);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(strList10);
    }

    @Test
    public void test233() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test233");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray8 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9, vCFHeaderLineArray8);
        htsjdk.variant.vcf.VCFHeader vCFHeader11 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9);
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray13 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet14 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean15 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet14, vCFHeaderLineArray13);
        htsjdk.variant.vcf.VCFHeader vCFHeader16 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet14);
        htsjdk.variant.vcf.VCFHeader vCFHeader17 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet14);
        java.lang.String[] strArray22 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.vcf.VCFHeader vCFHeader25 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet14, (java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.vcf.VCFHeader vCFHeader26 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet14);
        java.lang.String[] strArray33 = new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" };
        java.util.LinkedHashSet<java.lang.String> strSet34 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet34, strArray33);
        htsjdk.variant.vcf.VCFHeader vCFHeader36 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet14, (java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.vcf.VCFHeader vCFHeader37 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet9, (java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.vcf.VCFHeader vCFHeader38 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.vcf.VCFHeader vCFHeader39 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine41 = vCFHeader39.getInfoHeaderLine("intervals");
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray8);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray8, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray13);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray13, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "[VCFHeader:\n]", "##", "interval_merging", "##", "hi!", "interval_merging" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNull(vCFInfoHeaderLine41);
    }

    @Test
    public void test234() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test234");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine11 = vCFHeader0.getFilterHeaderLine("excludeIntervals");
        int int12 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion13 = vCFHeader0.getVCFHeaderVersion();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertNull(vCFFilterHeaderLine11);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 8 + "'", int12 == 8);
        org.junit.Assert.assertNull(vCFHeaderVersion13);
    }

    @Test
    public void test235() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test235");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList10 = vCFHeader7.getFilterLines();
        boolean boolean12 = vCFHeader7.hasFilterLine("#");
        boolean boolean14 = vCFHeader7.hasInfoLine("intervals");
        vCFHeader7.setWriteEngineHeaders(true);
        boolean boolean17 = vCFHeader7.samplesWereAlreadySorted();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList10);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
    }

    @Test
    public void test236() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test236");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        java.util.List<java.lang.String> strList4 = vCFHeader0.getGenotypeSamples();
        java.lang.Class<?> wildcardClass5 = vCFHeader0.getClass();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertNotNull(strList4);
        org.junit.Assert.assertNotNull(wildcardClass5);
    }

    @Test
    public void test237() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test237");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection2 = vCFHeader0.getFormatHeaderLines();
        boolean boolean4 = vCFHeader0.hasFormatLine("contig");
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection2);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test238() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test238");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        boolean boolean13 = vCFHeader0.samplesWereAlreadySorted();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine15 = vCFHeader0.getOtherHeaderLine("intervals");
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection16 = vCFHeader0.getFormatHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNull(vCFHeaderLine15);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection16);
    }

    @Test
    public void test239() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test239");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine5 = vCFHeader0.getInfoHeaderLine("reference");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean9 = vCFHeader0.hasInfoLine("reference");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertNull(vCFInfoHeaderLine5);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test240() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test240");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine14 = vCFHeader0.getFilterHeaderLine("reference");
        java.util.List<java.lang.String> strList15 = vCFHeader0.getGenotypeSamples();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection16 = vCFHeader0.getOtherHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNull(vCFFilterHeaderLine14);
        org.junit.Assert.assertNotNull(strList15);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection16);
    }

    @Test
    public void test241() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test241");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList4 = vCFHeader0.getFilterLines();
        vCFHeader0.setWriteCommandLine(true);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary7 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary7);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList4);
    }

    @Test
    public void test242() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test242");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList5 = vCFHeader4.getIDHeaderLines();
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary6 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader4.setSequenceDictionary(sAMSequenceDictionary6);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList5);
    }

    @Test
    public void test243() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test243");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean6 = vCFHeader0.hasFilterLine("");
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet8 = vCFHeader7.getHeaderFields();
        boolean boolean9 = vCFHeader7.samplesWereAlreadySorted();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader7.getInfoHeaderLine("reference");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet8);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
    }

    @Test
    public void test244() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test244");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.List<java.lang.String> strList9 = vCFHeader7.getGenotypeSamples();
        boolean boolean10 = vCFHeader7.isWriteEngineHeaders();
        boolean boolean11 = vCFHeader7.isWriteCommandLine();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList12 = vCFHeader7.getFilterLines();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(strList9);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList12);
    }

    @Test
    public void test245() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test245");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.List<java.lang.String> strList3 = vCFHeader0.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap5 = vCFHeader0.getSampleNameToOffset();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator6 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strList3);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
        org.junit.Assert.assertNotNull(strMap5);
    }

    @Test
    public void test246() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test246");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        boolean boolean11 = vCFHeader0.hasFormatLine("interval_merging");
        boolean boolean13 = vCFHeader0.hasFormatLine("hi!");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine14 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.addMetaDataLine(vCFHeaderLine14);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test247() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test247");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet11 = vCFHeader0.getHeaderFields();
        java.util.List<java.lang.String> strList12 = vCFHeader0.getGenotypeSamples();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet11);
        org.junit.Assert.assertNotNull(strList12);
    }

    @Test
    public void test248() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test248");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        boolean boolean10 = vCFHeader0.isWriteEngineHeaders();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap11 = vCFHeader0.getSampleNameToOffset();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList12 = vCFHeader0.getIDHeaderLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList13 = vCFHeader0.getContigLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(strMap11);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList12);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList13);
    }

    @Test
    public void test249() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test249");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.List<java.lang.String> strList9 = vCFHeader7.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeader vCFHeader10 = new htsjdk.variant.vcf.VCFHeader(vCFHeader7);
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection11 = vCFHeader7.getOtherHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection12 = vCFHeader7.getFormatHeaderLines();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(strList9);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection11);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection12);
    }

    @Test
    public void test250() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test250");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        int int6 = vCFHeader0.getNGenotypeSamples();
        boolean boolean8 = vCFHeader0.hasInfoLine("[VCFHeader:\n]");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary9 = vCFHeader0.getSequenceDictionary();
        vCFHeader0.setWriteEngineHeaders(true);
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary9);
    }

    @Test
    public void test251() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test251");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine6 = vCFHeader0.getFormatHeaderLine("intervals");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet7 = vCFHeader0.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine9 = vCFHeader0.getFormatHeaderLine("##");
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList10 = vCFHeader0.getIDHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFormatHeaderLine6);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet7);
        org.junit.Assert.assertNull(vCFFormatHeaderLine9);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList10);
    }

    @Test
    public void test252() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test252");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        java.util.ArrayList<java.lang.String> strList2 = vCFHeader0.getSampleNamesInOrder();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection3 = vCFHeader0.getOtherHeaderLines();
        vCFHeader0.setWriteEngineHeaders(false);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextComparator variantContextComparator6 = vCFHeader0.getVCFRecordComparator();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: One or more header lines must be in the header line collection.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNotNull(strList2);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection3);
    }

    @Test
    public void test253() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test253");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        vCFHeader0.setWriteCommandLine(true);
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection4 = vCFHeader0.getFormatHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFInfoHeaderLine> vCFInfoHeaderLineCollection5 = vCFHeader0.getInfoHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection4);
        org.junit.Assert.assertNotNull(vCFInfoHeaderLineCollection5);
    }

    @Test
    public void test254() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test254");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet3 = vCFHeader0.getHeaderFields();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList5 = vCFHeader0.getFilterLines();
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList6 = vCFHeader0.getContigLines();
        boolean boolean7 = vCFHeader0.samplesWereAlreadySorted();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection8 = vCFHeader0.getOtherHeaderLines();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet3);
        org.junit.Assert.assertNotNull(strMap4);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList5);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection8);
    }

    @Test
    public void test255() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test255");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine3 = vCFHeader0.getInfoHeaderLine("reference");
        boolean boolean4 = vCFHeader0.hasGenotypingData();
        java.util.List<htsjdk.variant.vcf.VCFIDHeaderLine> vCFIDHeaderLineList5 = vCFHeader0.getIDHeaderLines();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection6 = vCFHeader0.getOtherHeaderLines();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine8 = vCFHeader0.getInfoHeaderLine("");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFInfoHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(vCFIDHeaderLineList5);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection6);
        org.junit.Assert.assertNull(vCFInfoHeaderLine8);
    }

    @Test
    public void test256() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test256");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("");
        java.util.List<htsjdk.variant.vcf.VCFContigHeaderLine> vCFContigHeaderLineList12 = vCFHeader0.getContigLines();
        boolean boolean14 = vCFHeader0.hasFormatLine("contig");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
        org.junit.Assert.assertNotNull(vCFContigHeaderLineList12);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test257() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test257");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.samplesWereAlreadySorted();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getOtherHeaderLine("");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
    }

    @Test
    public void test258() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test258");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet9 = vCFHeader7.getMetaDataInInputOrder();
        boolean boolean10 = vCFHeader7.samplesWereAlreadySorted();
        vCFHeader7.setWriteEngineHeaders(true);
        java.lang.String str13 = vCFHeader7.toString();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet9);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "[VCFHeader:\n]" + "'", str13, "[VCFHeader:\n]");
    }

    @Test
    public void test259() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test259");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection1 = vCFHeader0.getFormatHeaderLines();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("interval_set_rule");
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection1);
        org.junit.Assert.assertNull(vCFHeaderLine3);
    }

    @Test
    public void test260() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test260");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = vCFHeader0.getMetaDataInSortedOrder();
        java.util.ArrayList<java.lang.String> strList2 = vCFHeader0.getSampleNamesInOrder();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection3 = vCFHeader0.getOtherHeaderLines();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap4 = vCFHeader0.getSampleNameToOffset();
        org.junit.Assert.assertNotNull(vCFHeaderLineSet1);
        org.junit.Assert.assertNotNull(strList2);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection3);
        org.junit.Assert.assertNotNull(strMap4);
    }

    @Test
    public void test261() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test261");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList4 = vCFHeader0.getFilterLines();
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.List<java.lang.String> strList6 = vCFHeader5.getGenotypeSamples();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList4);
        org.junit.Assert.assertNotNull(strList6);
    }

    @Test
    public void test262() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test262");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        boolean boolean6 = vCFHeader0.hasInfoLine("intervals");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary7 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader0.setSequenceDictionary(sAMSequenceDictionary7);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.SAMSequenceDictionary.getSequences()\" because \"dictionary\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test263() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test263");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.List<java.lang.String> strList9 = vCFHeader7.getGenotypeSamples();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet10 = vCFHeader7.getHeaderFields();
        java.util.Collection<htsjdk.variant.vcf.VCFFormatHeaderLine> vCFFormatHeaderLineCollection11 = vCFHeader7.getFormatHeaderLines();
        int int12 = vCFHeader7.getColumnCount();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(strList9);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet10);
        org.junit.Assert.assertNotNull(vCFFormatHeaderLineCollection11);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 10 + "'", int12 == 10);
    }

    @Test
    public void test264() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test264");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary8 = vCFHeader7.getSequenceDictionary();
        vCFHeader7.setWriteEngineHeaders(true);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine12 = vCFHeader7.getOtherHeaderLine("intervals");
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine14 = vCFHeader7.getMetaDataLine("##");
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet15 = vCFHeader7.getMetaDataInSortedOrder();
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNull(sAMSequenceDictionary8);
        org.junit.Assert.assertNull(vCFHeaderLine12);
        org.junit.Assert.assertNull(vCFHeaderLine14);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet15);
    }

    @Test
    public void test265() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test265");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine11 = vCFHeader0.getInfoHeaderLine("");
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection12 = vCFHeader0.getOtherHeaderLines();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet13 = vCFHeader0.getMetaDataInSortedOrder();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertNull(vCFInfoHeaderLine11);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection12);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet13);
    }

    @Test
    public void test266() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test266");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        htsjdk.variant.vcf.VCFHeader vCFHeader3 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        htsjdk.variant.vcf.VCFHeader vCFHeader4 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1);
        java.lang.String[] strArray9 = new java.lang.String[] { "intervals", "contig", "hi!", "##" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.vcf.VCFHeader vCFHeader12 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet10);
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet13 = vCFHeader12.getMetaDataInInputOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader14 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet13);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "intervals", "contig", "hi!", "##" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet13);
    }

    @Test
    public void test267() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test267");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean3 = vCFHeader0.hasFormatLine("");
        vCFHeader0.setWriteCommandLine(false);
        boolean boolean6 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean8 = vCFHeader0.hasFilterLine("excludeIntervals");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion9 = vCFHeader0.getVCFHeaderVersion();
        boolean boolean11 = vCFHeader0.hasFormatLine("interval_merging");
        boolean boolean13 = vCFHeader0.hasFormatLine("hi!");
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary14 = vCFHeader0.getSequenceDictionary();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFHeaderVersion9);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(sAMSequenceDictionary14);
    }

    @Test
    public void test268() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test268");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean4 = vCFHeader0.samplesWereAlreadySorted();
        java.util.Set<htsjdk.variant.vcf.VCFHeader.HEADER_FIELDS> hEADER_FIELDSSet5 = vCFHeader0.getHeaderFields();
        int int6 = vCFHeader0.getNGenotypeSamples();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + true + "'", boolean4 == true);
        org.junit.Assert.assertNotNull(hEADER_FIELDSSet5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test269() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test269");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        htsjdk.samtools.SAMSequenceDictionary sAMSequenceDictionary8 = vCFHeader7.getSequenceDictionary();
        vCFHeader7.setWriteEngineHeaders(true);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine12 = vCFHeader7.getOtherHeaderLine("intervals");
        vCFHeader7.setWriteCommandLine(true);
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine15 = null;
        // The following exception was thrown during execution in test generation
        try {
            vCFHeader7.addMetaDataLine(vCFHeaderLine15);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFHeaderLine.getKey()\" because \"line\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNull(sAMSequenceDictionary8);
        org.junit.Assert.assertNull(vCFHeaderLine12);
    }

    @Test
    public void test270() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test270");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean2 = vCFHeader0.hasFormatLine("reference");
        java.util.List<java.lang.String> strList3 = vCFHeader0.getGenotypeSamples();
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion4 = vCFHeader0.getVCFHeaderVersion();
        java.util.HashMap<java.lang.String, java.lang.Integer> strMap5 = vCFHeader0.getSampleNameToOffset();
        java.util.ArrayList<java.lang.String> strList6 = vCFHeader0.getSampleNamesInOrder();
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strList3);
        org.junit.Assert.assertNull(vCFHeaderVersion4);
        org.junit.Assert.assertNotNull(strMap5);
        org.junit.Assert.assertNotNull(strList6);
    }

    @Test
    public void test271() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test271");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        int int1 = vCFHeader0.getNGenotypeSamples();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine3 = vCFHeader0.getFilterHeaderLine("interval_merging");
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList4 = vCFHeader0.getFilterLines();
        htsjdk.variant.vcf.VCFHeader vCFHeader5 = new htsjdk.variant.vcf.VCFHeader(vCFHeader0);
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection6 = vCFHeader5.getOtherHeaderLines();
        org.junit.Assert.assertTrue("'" + int1 + "' != '" + 0 + "'", int1 == 0);
        org.junit.Assert.assertNull(vCFFilterHeaderLine3);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList4);
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection6);
    }

    @Test
    public void test272() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test272");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine14 = vCFHeader0.getFilterHeaderLine("reference");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine16 = vCFHeader0.getInfoHeaderLine("");
        boolean boolean18 = vCFHeader0.hasFormatLine("[VCFHeader:\n]");
        boolean boolean19 = vCFHeader0.samplesWereAlreadySorted();
        boolean boolean21 = vCFHeader0.hasInfoLine("interval_set_rule");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNull(vCFFilterHeaderLine14);
        org.junit.Assert.assertNull(vCFInfoHeaderLine16);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + false + "'", boolean21 == false);
    }

    @Test
    public void test273() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test273");
        htsjdk.variant.vcf.VCFHeaderLine[] vCFHeaderLineArray0 = new htsjdk.variant.vcf.VCFHeaderLine[] {};
        java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet1 = new java.util.LinkedHashSet<htsjdk.variant.vcf.VCFHeaderLine>();
        boolean boolean2 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, vCFHeaderLineArray0);
        java.lang.String[] strArray4 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet5 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet5, strArray4);
        htsjdk.variant.vcf.VCFHeader vCFHeader7 = new htsjdk.variant.vcf.VCFHeader((java.util.Set<htsjdk.variant.vcf.VCFHeaderLine>) vCFHeaderLineSet1, (java.util.Set<java.lang.String>) strSet5);
        java.util.List<htsjdk.variant.vcf.VCFFilterHeaderLine> vCFFilterHeaderLineList8 = vCFHeader7.getFilterLines();
        java.util.List<java.lang.String> strList9 = vCFHeader7.getGenotypeSamples();
        java.util.Set<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineSet10 = vCFHeader7.getMetaDataInSortedOrder();
        htsjdk.variant.vcf.VCFHeader vCFHeader11 = new htsjdk.variant.vcf.VCFHeader(vCFHeaderLineSet10);
        org.junit.Assert.assertNotNull(vCFHeaderLineArray0);
        org.junit.Assert.assertArrayEquals(vCFHeaderLineArray0, new htsjdk.variant.vcf.VCFHeaderLine[] {});
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + false + "'", boolean2 == false);
        org.junit.Assert.assertNotNull(strArray4);
        org.junit.Assert.assertArrayEquals(strArray4, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(vCFFilterHeaderLineList8);
        org.junit.Assert.assertNotNull(strList9);
        org.junit.Assert.assertNotNull(vCFHeaderLineSet10);
    }

    @Test
    public void test274() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test274");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        htsjdk.variant.vcf.VCFHeaderLine vCFHeaderLine3 = vCFHeader0.getMetaDataLine("");
        int int4 = vCFHeader0.getColumnCount();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine6 = vCFHeader0.getFilterHeaderLine("interval_merging");
        boolean boolean8 = vCFHeader0.hasFormatLine("");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine10 = vCFHeader0.getInfoHeaderLine("reference");
        htsjdk.variant.vcf.VCFFormatHeaderLine vCFFormatHeaderLine12 = vCFHeader0.getFormatHeaderLine("interval_set_rule");
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine14 = vCFHeader0.getFilterHeaderLine("reference");
        htsjdk.variant.vcf.VCFInfoHeaderLine vCFInfoHeaderLine16 = vCFHeader0.getInfoHeaderLine("");
        boolean boolean18 = vCFHeader0.hasFormatLine("[VCFHeader:\n]");
        java.lang.String str19 = vCFHeader0.toString();
        java.util.Collection<htsjdk.variant.vcf.VCFHeaderLine> vCFHeaderLineCollection20 = vCFHeader0.getOtherHeaderLines();
        htsjdk.variant.vcf.VCFFilterHeaderLine vCFFilterHeaderLine22 = vCFHeader0.getFilterHeaderLine("interval_set_rule");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertNull(vCFHeaderLine3);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 8 + "'", int4 == 8);
        org.junit.Assert.assertNull(vCFFilterHeaderLine6);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(vCFInfoHeaderLine10);
        org.junit.Assert.assertNull(vCFFormatHeaderLine12);
        org.junit.Assert.assertNull(vCFFilterHeaderLine14);
        org.junit.Assert.assertNull(vCFInfoHeaderLine16);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "[VCFHeader:\n]" + "'", str19, "[VCFHeader:\n]");
        org.junit.Assert.assertNotNull(vCFHeaderLineCollection20);
        org.junit.Assert.assertNull(vCFFilterHeaderLine22);
    }

    @Test
    public void test275() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test275");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = new htsjdk.variant.vcf.VCFHeader();
        boolean boolean1 = vCFHeader0.isWriteEngineHeaders();
        boolean boolean2 = vCFHeader0.isWriteCommandLine();
        boolean boolean3 = vCFHeader0.isWriteCommandLine();
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + true + "'", boolean1 == true);
        org.junit.Assert.assertTrue("'" + boolean2 + "' != '" + true + "'", boolean2 == true);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
    }
}

