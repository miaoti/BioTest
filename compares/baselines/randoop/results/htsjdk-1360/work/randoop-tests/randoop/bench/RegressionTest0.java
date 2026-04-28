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
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        java.lang.String[] strArray9 = new java.lang.String[] { "hi!", "hi!" };
        java.util.ArrayList<java.lang.String> strList10 = new java.util.ArrayList<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList10, strArray9);
        java.lang.String[] strArray14 = new java.lang.String[] { "hi!", "hi!" };
        java.util.ArrayList<java.lang.String> strList15 = new java.util.ArrayList<java.lang.String>();
        boolean boolean16 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList15, strArray14);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList10, (java.util.Collection<java.lang.String>) strList15, true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(strArray14);
        org.junit.Assert.assertArrayEquals(strArray14, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
    }

    @Test
    public void test002() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test002");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray11 = sAMRecord1.getSignedIntArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test003() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test003");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean7 = sAMRecord1.getSecondOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test004() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test004");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        boolean boolean4 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test005() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test005");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
    }

    @Test
    public void test006() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test006");
        int int0 = htsjdk.samtools.SAMRecord.NO_ALIGNMENT_START;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 0 + "'", int0 == 0);
    }

    @Test
    public void test007() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test007");
        java.lang.String str0 = htsjdk.samtools.SAMRecord.NULL_SEQUENCE_STRING;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "*" + "'", str0, "*");
    }

    @Test
    public void test008() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test008");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        java.lang.String[] strArray7 = new java.lang.String[] { "", "hi!" };
        java.util.ArrayList<java.lang.String> strList8 = new java.util.ArrayList<java.lang.String>();
        boolean boolean9 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList8, strArray7);
        java.util.List<java.lang.String> strList10 = htsjdk.samtools.SAMRecord.TAGS_TO_REVERSE;
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList8, (java.util.Collection<java.lang.String>) strList10, true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(strArray7);
        org.junit.Assert.assertArrayEquals(strArray7, new java.lang.String[] { "", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNotNull(strList10);
    }

    @Test
    public void test009() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test009");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Object obj5 = sAMRecord1.getAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test010() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test010");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Byte byte15 = sAMRecord13.getByteAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
    }

    @Test
    public void test011() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test011");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.lang.String str12 = sAMRecord1.getCigarString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "*" + "'", str12, "*");
    }

    @Test
    public void test012() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test012");
        java.lang.String str0 = htsjdk.samtools.SAMRecord.NULL_QUALS_STRING;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "*" + "'", str0, "*");
    }

    @Test
    public void test013() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test013");
        int int0 = htsjdk.samtools.SAMRecord.NO_MAPPING_QUALITY;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 0 + "'", int0 == 0);
    }

    @Test
    public void test014() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test014");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray10 = sAMRecord1.getSignedByteArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
    }

    @Test
    public void test015() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test015");
        int int0 = htsjdk.samtools.SAMRecord.NO_ALIGNMENT_REFERENCE_INDEX;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + (-1) + "'", int0 == (-1));
    }

    @Test
    public void test016() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test016");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        htsjdk.samtools.Cigar cigar9 = null;
        sAMRecord1.setCigar(cigar9);
        sAMRecord1.setInferredInsertSize(0);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test017() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test017");
        java.lang.String str0 = htsjdk.samtools.SAMRecord.NO_ALIGNMENT_CIGAR;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "*" + "'", str0, "*");
    }

    @Test
    public void test018() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test018");
        int int0 = htsjdk.samtools.SAMRecord.MAX_INSERT_SIZE;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 536870912 + "'", int0 == 536870912);
    }

    @Test
    public void test019() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test019");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean7 = sAMRecord1.getMateUnmappedFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test020() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test020");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex(0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(obj5);
    }

    @Test
    public void test021() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test021");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Float float8 = sAMRecord1.getFloatAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test022() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test022");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Short short6 = sAMRecord1.getShortAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test023() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test023");
        long long0 = htsjdk.samtools.SAMRecord.serialVersionUID;
        org.junit.Assert.assertTrue("'" + long0 + "' != '" + 1L + "'", long0 == 1L);
    }

    @Test
    public void test024() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test024");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test025() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test025");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        // The following exception was thrown during execution in test generation
        try {
            short[] shortArray15 = sAMRecord1.getSignedShortArrayAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
    }

    @Test
    public void test026() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test026");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray17 = sAMRecord1.getSignedIntArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
    }

    @Test
    public void test027() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test027");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test028() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test028");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray9 = sAMRecord1.getSignedByteArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test029() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test029");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int6 = sAMRecord1.getUnclippedStart();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList8 = sAMRecord1.validateCigar((long) (short) -1);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList8);
    }

    @Test
    public void test030() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test030");
        java.lang.String str0 = htsjdk.samtools.SAMRecord.NO_ALIGNMENT_REFERENCE_NAME;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "*" + "'", str0, "*");
    }

    @Test
    public void test031() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test031");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        java.lang.String[] strArray15 = new java.lang.String[] { "null 0b aligned to *:0--1.", "null 0b aligned to *:0--1." };
        java.util.ArrayList<java.lang.String> strList16 = new java.util.ArrayList<java.lang.String>();
        boolean boolean17 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList16, strArray15);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList16, (java.util.Collection<java.lang.String>) strList21, true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(strArray15);
        org.junit.Assert.assertArrayEquals(strArray15, new java.lang.String[] { "null 0b aligned to *:0--1.", "null 0b aligned to *:0--1." });
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
    }

    @Test
    public void test032() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test032");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        boolean boolean15 = sAMRecord1.isSecondaryAlignment();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        sAMRecord18.setDuplicateReadFlag(false);
        java.lang.Object obj21 = null;
        boolean boolean22 = sAMRecord18.equals(obj21);
        htsjdk.samtools.SAMFileHeader sAMFileHeader23 = null;
        htsjdk.samtools.SAMRecord sAMRecord24 = new htsjdk.samtools.SAMRecord(sAMFileHeader23);
        sAMRecord24.setDuplicateReadFlag(false);
        sAMRecord24.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj29 = sAMRecord18.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency30 = null;
        sAMRecord18.setValidationStringency(validationStringency30);
        boolean boolean32 = sAMRecord18.isSecondaryAlignment();
        boolean boolean33 = sAMRecord18.getSupplementaryAlignmentFlag();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setAttribute("hi!", (java.lang.Object) sAMRecord18);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + false + "'", boolean22 == false);
        org.junit.Assert.assertNull(obj29);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
    }

    @Test
    public void test033() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test033");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setMateReferenceIndex((int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test034() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test034");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        java.lang.String str11 = sAMRecord1.toString();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean13 = sAMRecord1.isUnsignedArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "null 0b aligned to *:0--1." + "'", str11, "null 0b aligned to *:0--1.");
    }

    @Test
    public void test035() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test035");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Long long9 = sAMRecord1.getUnsignedIntegerAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test036() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test036");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean13 = sAMRecord1.getMateUnmappedFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test037() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test037");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        sAMRecord1.setFlags((int) (byte) 100);
        // The following exception was thrown during execution in test generation
        try {
            int int10 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test038() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test038");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        sAMRecord1.setMateNegativeStrandFlag(true);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test039() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test039");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        // The following exception was thrown during execution in test generation
        try {
            short[] shortArray14 = sAMRecord1.getUnsignedShortArrayAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
    }

    @Test
    public void test040() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test040");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        byte[] byteArray9 = sAMRecord1.getBaseQualities();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean10 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(byteArray9);
        org.junit.Assert.assertArrayEquals(byteArray9, new byte[] {});
    }

    @Test
    public void test041() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test041");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        byte[] byteArray9 = sAMRecord1.getBaseQualities();
        java.lang.String str10 = sAMRecord1.format();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList12 = sAMRecord1.validateCigar(10L);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean13 = sAMRecord1.getMateUnmappedFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(byteArray9);
        org.junit.Assert.assertArrayEquals(byteArray9, new byte[] {});
        org.junit.Assert.assertEquals("'" + str10 + "' != '" + "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*" + "'", str10, "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        org.junit.Assert.assertNull(sAMValidationErrorList12);
    }

    @Test
    public void test042() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test042");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        int int11 = sAMRecord1.getReferencePositionAtReadPosition((int) (short) 0);
        // The following exception was thrown during execution in test generation
        try {
            int int12 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
    }

    @Test
    public void test043() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test043");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray8 = sAMRecord1.getSignedByteArrayAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
    }

    @Test
    public void test044() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test044");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Byte byte5 = sAMRecord1.getByteAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test045() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test045");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        htsjdk.samtools.Cigar cigar14 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Byte byte16 = sAMRecord1.getByteAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNotNull(cigar14);
    }

    @Test
    public void test046() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test046");
        byte[] byteArray0 = htsjdk.samtools.SAMRecord.NULL_QUALS;
        org.junit.Assert.assertNotNull(byteArray0);
        org.junit.Assert.assertArrayEquals(byteArray0, new byte[] {});
    }

    @Test
    public void test047() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test047");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        byte[] byteArray8 = sAMRecord1.getVariableBinaryRepresentation();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(byteArray8);
    }

    @Test
    public void test048() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test048");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader9 = null;
        htsjdk.samtools.SAMRecord sAMRecord10 = new htsjdk.samtools.SAMRecord(sAMFileHeader9);
        sAMRecord10.setDuplicateReadFlag(false);
        java.lang.Object obj13 = null;
        boolean boolean14 = sAMRecord10.equals(obj13);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList16 = sAMRecord10.isValid(false);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setUnsignedArrayAttribute("null 0b aligned to *:0--1.", (java.lang.Object) sAMRecord10);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Non-array passed to setUnsignedArrayAttribute for tag null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList16);
    }

    @Test
    public void test049() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test049");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray8 = sAMRecord1.getUnsignedIntArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test050() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test050");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        // The following exception was thrown during execution in test generation
        try {
            short[] shortArray9 = sAMRecord1.getSignedShortArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test051() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test051");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        boolean boolean7 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test052() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test052");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = sAMRecord1.getHeader();
        sAMRecord1.setCigarString("*");
        org.junit.Assert.assertNull(sAMFileHeader4);
    }

    @Test
    public void test053() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test053");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        int int11 = sAMRecord1.getReferencePositionAtReadPosition((int) (short) 0);
        boolean boolean12 = sAMRecord1.getReadUnmappedFlag();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Object obj14 = sAMRecord1.getAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test054() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test054");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray8 = sAMRecord1.getFloatArrayAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test055() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test055");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        // The following exception was thrown during execution in test generation
        try {
            short[] shortArray15 = sAMRecord1.getUnsignedShortArrayAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
    }

    @Test
    public void test056() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test056");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test057() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test057");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        sAMRecord8.setMappingQuality((int) (short) 100);
        sAMRecord8.setReferenceName("");
        sAMRecord8.setReadUnmappedFlag(true);
        java.lang.Object obj21 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        sAMRecord1.setSecondaryAlignment(true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
    }

    @Test
    public void test058() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test058");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
    }

    @Test
    public void test059() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test059");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        // The following exception was thrown during execution in test generation
        try {
            int int16 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test060() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test060");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean13 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test061() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test061");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean32 = sAMRecord13.hasAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
    }

    @Test
    public void test062() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test062");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        htsjdk.samtools.Cigar cigar9 = null;
        sAMRecord1.setCigar(cigar9);
        boolean boolean11 = sAMRecord1.isSecondaryOrSupplementary();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
    }

    @Test
    public void test063() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test063");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getUnclippedEnd();
        sAMRecord1.setMappingQuality(100);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test064() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test064");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        int int12 = sAMRecord1.getUnclippedEnd();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
    }

    @Test
    public void test065() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test065");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean6 = sAMRecord1.getMateNegativeStrandFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
    }

    @Test
    public void test066() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test066");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        // The following exception was thrown during execution in test generation
        try {
            short[] shortArray7 = sAMRecord1.getSignedShortArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test067() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test067");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        htsjdk.samtools.Cigar cigar9 = null;
        sAMRecord1.setCigar(cigar9);
        java.lang.String str11 = sAMRecord1.getSAMString();
        sAMRecord1.reverseComplement();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n" + "'", str11, "null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
    }

    @Test
    public void test068() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test068");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        java.lang.Long long3 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 10);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Character char5 = sAMRecord1.getCharacterAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(long3);
    }

    @Test
    public void test069() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test069");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        sAMRecord1.setFlags(536870912);
        java.lang.String str18 = sAMRecord1.getBaseQualityString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        sAMRecord20.setMappingQuality((-1));
        boolean boolean23 = sAMRecord20.getReadNegativeStrandFlag();
        int int24 = sAMRecord20.getLengthOnReference();
        sAMRecord20.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader27 = null;
        htsjdk.samtools.SAMRecord sAMRecord28 = new htsjdk.samtools.SAMRecord(sAMFileHeader27);
        sAMRecord28.setDuplicateReadFlag(false);
        java.lang.Object obj31 = null;
        boolean boolean32 = sAMRecord28.equals(obj31);
        boolean boolean33 = sAMRecord20.overlaps((htsjdk.samtools.util.Locatable) sAMRecord28);
        boolean boolean34 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord20);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Object obj36 = sAMRecord1.getAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "*" + "'", str18, "*");
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + 0 + "'", int24 == 0);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
    }

    @Test
    public void test070() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test070");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        htsjdk.samtools.Cigar cigar9 = null;
        sAMRecord1.setCigar(cigar9);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean11 = sAMRecord1.getMateNegativeStrandFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test071() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test071");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        java.lang.Object obj7 = sAMRecord1.getAttribute((short) 100);
        int int9 = sAMRecord1.getReferencePositionAtReadPosition(0);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean11 = sAMRecord1.isUnsignedArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(obj7);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test072() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test072");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean16 = sAMRecord9.isUnsignedArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
    }

    @Test
    public void test073() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test073");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setReadNegativeStrandFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test074() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test074");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = null;
        htsjdk.samtools.SAMRecord sAMRecord15 = new htsjdk.samtools.SAMRecord(sAMFileHeader14);
        sAMRecord15.setDuplicateReadFlag(false);
        sAMRecord15.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj20 = sAMRecord9.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord21 = sAMRecord9.deepCopy();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setDuplicateReadFlag(false);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMRecord23.equals(obj26);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList29 = sAMRecord23.isValid(false);
        sAMRecord23.setMateReferenceName("hi!");
        sAMRecord23.setAlignmentStart((int) (short) 1);
        int int34 = sAMRecord23.getStart();
        java.lang.Object obj35 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord21, (java.lang.Object) int34);
        java.lang.String str36 = sAMRecord1.getReadString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
    }

    @Test
    public void test075() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test075");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        java.lang.String str15 = sAMRecord1.format();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*" + "'", str15, "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
    }

    @Test
    public void test076() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test076");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        htsjdk.samtools.SAMRecord sAMRecord7 = sAMRecord1.deepCopy();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Integer int9 = sAMRecord1.getIntegerAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(sAMRecord7);
    }

    @Test
    public void test077() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test077");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        byte[] byteArray5 = sAMRecord1.getBaseQualities();
        java.lang.Object obj6 = sAMRecord1.clone();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean8 = sAMRecord1.hasAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] {});
        org.junit.Assert.assertNotNull(obj6);
        org.junit.Assert.assertEquals(obj6.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj6), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj6), "null 0b aligned to *:0--1.");
    }

    @Test
    public void test078() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test078");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList25 = sAMRecord1.isValid(false);
        byte[] byteArray26 = sAMRecord1.getOriginalBaseQualities();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setBaseQualityString("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Invalid fastq character: ?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(sAMValidationErrorList25);
        org.junit.Assert.assertNull(byteArray26);
    }

    @Test
    public void test079() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test079");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        htsjdk.samtools.SAMRecord sAMRecord14 = sAMRecord1.deepCopy();
        int int15 = sAMRecord1.getStart();
        int int16 = sAMRecord1.getFlags();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNotNull(sAMRecord14);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
    }

    @Test
    public void test080() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test080");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        sAMRecord1.setFirstOfPairFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
    }

    @Test
    public void test081() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test081");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        sAMRecord1.setFlags(536870912);
        java.lang.String str18 = sAMRecord1.getBaseQualityString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        sAMRecord20.setMappingQuality((-1));
        boolean boolean23 = sAMRecord20.getReadNegativeStrandFlag();
        int int24 = sAMRecord20.getLengthOnReference();
        sAMRecord20.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader27 = null;
        htsjdk.samtools.SAMRecord sAMRecord28 = new htsjdk.samtools.SAMRecord(sAMFileHeader27);
        sAMRecord28.setDuplicateReadFlag(false);
        java.lang.Object obj31 = null;
        boolean boolean32 = sAMRecord28.equals(obj31);
        boolean boolean33 = sAMRecord20.overlaps((htsjdk.samtools.util.Locatable) sAMRecord28);
        boolean boolean34 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord20);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean35 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "*" + "'", str18, "*");
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + 0 + "'", int24 == 0);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
    }

    @Test
    public void test082() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test082");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        sAMRecord1.setReadPairedFlag(true);
        boolean boolean9 = sAMRecord1.getNotPrimaryAlignmentFlag();
        java.lang.String str10 = sAMRecord1.getBaseQualityString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertEquals("'" + str10 + "' != '" + "*" + "'", str10, "*");
    }

    @Test
    public void test083() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test083");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList8 = sAMRecord1.isValid(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertNotNull(sAMValidationErrorList8);
    }

    @Test
    public void test084() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test084");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setDuplicateReadFlag(false);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMRecord8.equals(obj11);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList14 = sAMRecord8.isValid(false);
        sAMRecord8.setMateReferenceName("hi!");
        sAMRecord8.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet19 = sAMRecord8.getSAMFlags();
        java.lang.Object obj20 = sAMRecord1.removeTransientAttribute((java.lang.Object) sAMFlagSet19);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Class<?> wildcardClass21 = obj20.getClass();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList14);
        org.junit.Assert.assertNotNull(sAMFlagSet19);
        org.junit.Assert.assertNull(obj20);
    }

    @Test
    public void test085() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test085");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getUnclippedEnd();
        sAMRecord1.setSecondOfPairFlag(false);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test086() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test086");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        sAMRecord8.setMappingQuality((int) (short) 100);
        sAMRecord8.setReferenceName("");
        sAMRecord8.setReadUnmappedFlag(true);
        java.lang.Object obj21 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        java.lang.String str22 = sAMRecord1.toString();
        sAMRecord1.setDuplicateReadFlag(true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "null 0b aligned to *:0--1." + "'", str22, "null 0b aligned to *:0--1.");
    }

    @Test
    public void test087() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test087");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        int int15 = sAMRecord1.getUnclippedStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
    }

    @Test
    public void test088() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test088");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        java.lang.String str15 = sAMRecord1.getCigarString();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str17 = sAMRecord1.getStringAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "*" + "'", str15, "*");
    }

    @Test
    public void test089() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test089");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Object obj11 = sAMRecord1.getAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test090() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test090");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        sAMRecord1.setReadNegativeStrandFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        sAMRecord18.setDuplicateReadFlag(false);
        java.lang.Class<?> wildcardClass21 = sAMRecord18.getClass();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setMappingQuality((-1));
        boolean boolean26 = sAMRecord23.getReadNegativeStrandFlag();
        int int27 = sAMRecord23.getLengthOnReference();
        java.lang.Object obj28 = sAMRecord1.setTransientAttribute((java.lang.Object) wildcardClass21, (java.lang.Object) sAMRecord23);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Class<?> wildcardClass29 = obj28.getClass();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(wildcardClass21);
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertTrue("'" + int27 + "' != '" + 0 + "'", int27 == 0);
        org.junit.Assert.assertNull(obj28);
    }

    @Test
    public void test091() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test091");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReadPairedFlag(false);
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test092() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test092");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        sAMRecord8.setMappingQuality((int) (short) 100);
        sAMRecord8.setReferenceName("");
        sAMRecord8.setReadUnmappedFlag(true);
        java.lang.Object obj21 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        // The following exception was thrown during execution in test generation
        try {
            int int22 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
    }

    @Test
    public void test093() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test093");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setProperPairFlag(true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test094() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test094");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        int int7 = sAMRecord1.getMappingQuality();
        sAMRecord1.setReadName("*");
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray11 = sAMRecord1.getUnsignedIntArrayAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
    }

    @Test
    public void test095() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test095");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        java.lang.Object obj7 = sAMRecord1.getAttribute((short) 100);
        java.lang.String str8 = sAMRecord1.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(obj7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "null\t0\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n" + "'", str8, "null\t0\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n");
    }

    @Test
    public void test096() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test096");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        sAMRecord1.setMateAlignmentStart((-1));
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setAttribute("hi!", (java.lang.Object) false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test097() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test097");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord31 = sAMRecord13.getReadGroup();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNull(sAMReadGroupRecord31);
    }

    @Test
    public void test098() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test098");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        htsjdk.samtools.SAMFileSource sAMFileSource9 = sAMRecord1.getFileSource();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Short short11 = sAMRecord1.getShortAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMFileSource9);
    }

    @Test
    public void test099() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test099");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = null;
        htsjdk.samtools.SAMRecord sAMRecord15 = new htsjdk.samtools.SAMRecord(sAMFileHeader14);
        sAMRecord15.setDuplicateReadFlag(false);
        sAMRecord15.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj20 = sAMRecord9.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord21 = sAMRecord9.deepCopy();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setDuplicateReadFlag(false);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMRecord23.equals(obj26);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList29 = sAMRecord23.isValid(false);
        sAMRecord23.setMateReferenceName("hi!");
        sAMRecord23.setAlignmentStart((int) (short) 1);
        int int34 = sAMRecord23.getStart();
        java.lang.Object obj35 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord21, (java.lang.Object) int34);
        java.lang.String str36 = sAMRecord21.getMateReferenceName();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord21.setMateReferenceIndex((int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
    }

    @Test
    public void test100() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test100");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList11 = sAMRecord1.getAlignmentBlocks();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertNotNull(alignmentBlockList11);
    }

    @Test
    public void test101() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test101");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        sAMRecord1.setReadString("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test102() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test102");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        boolean boolean13 = sAMRecord1.getDuplicateReadFlag();
        int int14 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + (-1) + "'", int14 == (-1));
    }

    @Test
    public void test103() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test103");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        byte[] byteArray8 = sAMRecord1.getReadBases();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str10 = sAMRecord1.getStringAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(byteArray8);
        org.junit.Assert.assertArrayEquals(byteArray8, new byte[] {});
    }

    @Test
    public void test104() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test104");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        sAMRecord30.setDuplicateReadFlag(false);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMRecord30.equals(obj33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        sAMRecord36.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj41 = sAMRecord30.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord42 = sAMRecord30.deepCopy();
        int int43 = sAMRecord42.getAlignmentStart();
        byte[] byteArray44 = sAMRecord42.getBaseQualities();
        sAMRecord17.setReadBases(byteArray44);
        sAMRecord17.setReadNegativeStrandFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray49 = sAMRecord17.getUnsignedByteArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNull(obj41);
        org.junit.Assert.assertNotNull(sAMRecord42);
        org.junit.Assert.assertTrue("'" + int43 + "' != '" + 0 + "'", int43 == 0);
        org.junit.Assert.assertNotNull(byteArray44);
        org.junit.Assert.assertArrayEquals(byteArray44, new byte[] {});
    }

    @Test
    public void test105() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test105");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList4 = sAMRecord1.getAlignmentBlocks();
        org.junit.Assert.assertNotNull(alignmentBlockList4);
    }

    @Test
    public void test106() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test106");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        int int16 = sAMRecord1.getAttributesBinarySize();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + (-1) + "'", int16 == (-1));
    }

    @Test
    public void test107() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test107");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        boolean boolean14 = sAMRecord1.getReadPairedFlag();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean15 = sAMRecord1.getSecondOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test108() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test108");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        htsjdk.samtools.Cigar cigar14 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = sAMRecord16.getHeader();
        byte[] byteArray20 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord16.setBaseQualities(byteArray20);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList22 = sAMRecord16.getAlignmentBlocks();
        boolean boolean23 = sAMRecord16.getReadPairedFlag();
        boolean boolean24 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord16);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNotNull(cigar14);
        org.junit.Assert.assertNull(sAMFileHeader17);
        org.junit.Assert.assertNotNull(byteArray20);
        org.junit.Assert.assertArrayEquals(byteArray20, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(alignmentBlockList22);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
    }

    @Test
    public void test109() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test109");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        sAMRecord1.setMateNegativeStrandFlag(false);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test110() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test110");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        boolean boolean25 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord13);
        htsjdk.samtools.SAMFileHeader sAMFileHeader26 = null;
        htsjdk.samtools.SAMRecord sAMRecord27 = new htsjdk.samtools.SAMRecord(sAMFileHeader26);
        sAMRecord27.setDuplicateReadFlag(false);
        java.lang.Object obj30 = null;
        boolean boolean31 = sAMRecord27.equals(obj30);
        htsjdk.samtools.SAMFileHeader sAMFileHeader32 = null;
        htsjdk.samtools.SAMRecord sAMRecord33 = new htsjdk.samtools.SAMRecord(sAMFileHeader32);
        sAMRecord33.setDuplicateReadFlag(false);
        sAMRecord33.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj38 = sAMRecord27.getTransientAttribute((java.lang.Object) true);
        java.lang.Object obj39 = sAMRecord1.removeTransientAttribute((java.lang.Object) sAMRecord27);
        boolean boolean40 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertNull(obj38);
        org.junit.Assert.assertNull(obj39);
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + false + "'", boolean40 == false);
    }

    @Test
    public void test111() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test111");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.Cigar cigar8 = null;
        sAMRecord1.setCigar(cigar8);
        sAMRecord1.setMateUnmappedFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList12 = sAMRecord1.isValid();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.samtools.Cigar.numCigarElements()\" because the return value of \"htsjdk.samtools.SAMRecord.getCigar()\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test112() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test112");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        boolean boolean31 = sAMRecord1.isSecondaryOrSupplementary();
        sAMRecord1.setReadNegativeStrandFlag(true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
    }

    @Test
    public void test113() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test113");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        sAMRecord1.setMateAlignmentStart((int) (short) 100);
        sAMRecord1.reverseComplement(false);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
    }

    @Test
    public void test114() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test114");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        java.lang.Object obj7 = sAMRecord1.getAttribute((short) 100);
        int int9 = sAMRecord1.getReferencePositionAtReadPosition(0);
        byte[] byteArray10 = sAMRecord1.getBaseQualities();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(obj7);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertNotNull(byteArray10);
        org.junit.Assert.assertArrayEquals(byteArray10, new byte[] {});
    }

    @Test
    public void test115() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test115");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean5 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
    }

    @Test
    public void test116() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test116");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        sAMRecord1.setProperPairFlag(false);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
    }

    @Test
    public void test117() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test117");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        java.lang.String str7 = sAMRecord1.getContig();
        sAMRecord1.setSupplementaryAlignmentFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "*" + "'", str7, "*");
    }

    @Test
    public void test118() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test118");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        int int15 = sAMRecord1.getReadLength();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = sAMRecord1.getHeader();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertNull(sAMFileHeader16);
    }

    @Test
    public void test119() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test119");
        int int0 = htsjdk.samtools.SAMRecord.UNKNOWN_MAPPING_QUALITY;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 255 + "'", int0 == 255);
    }

    @Test
    public void test120() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test120");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        sAMRecord1.setReadNegativeStrandFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        sAMRecord18.setDuplicateReadFlag(false);
        java.lang.Class<?> wildcardClass21 = sAMRecord18.getClass();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setMappingQuality((-1));
        boolean boolean26 = sAMRecord23.getReadNegativeStrandFlag();
        int int27 = sAMRecord23.getLengthOnReference();
        java.lang.Object obj28 = sAMRecord1.setTransientAttribute((java.lang.Object) wildcardClass21, (java.lang.Object) sAMRecord23);
        java.lang.Object obj30 = sAMRecord1.removeTransientAttribute((java.lang.Object) (-1.0d));
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(wildcardClass21);
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertTrue("'" + int27 + "' != '" + 0 + "'", int27 == 0);
        org.junit.Assert.assertNull(obj28);
        org.junit.Assert.assertNull(obj30);
    }

    @Test
    public void test121() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test121");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        byte[] byteArray14 = sAMRecord1.getReadBases();
        java.lang.String str15 = sAMRecord1.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertNotNull(byteArray14);
        org.junit.Assert.assertArrayEquals(byteArray14, new byte[] {});
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n" + "'", str15, "null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n");
    }

    @Test
    public void test122() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test122");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setDuplicateReadFlag(false);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMRecord8.equals(obj11);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList14 = sAMRecord8.isValid(false);
        sAMRecord8.setMateReferenceName("hi!");
        sAMRecord8.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet19 = sAMRecord8.getSAMFlags();
        java.lang.Object obj20 = sAMRecord1.removeTransientAttribute((java.lang.Object) sAMFlagSet19);
        sAMRecord1.clearAttributes();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList14);
        org.junit.Assert.assertNotNull(sAMFlagSet19);
        org.junit.Assert.assertNull(obj20);
    }

    @Test
    public void test123() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test123");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int6 = sAMRecord1.getUnclippedStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        boolean boolean15 = sAMRecord8.getReadPairedFlag();
        java.lang.Object obj17 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord8, (java.lang.Object) 100);
        boolean boolean18 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNull(obj17);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
    }

    @Test
    public void test124() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test124");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        sAMRecord30.setDuplicateReadFlag(false);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMRecord30.equals(obj33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        sAMRecord36.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj41 = sAMRecord30.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord42 = sAMRecord30.deepCopy();
        int int43 = sAMRecord42.getAlignmentStart();
        byte[] byteArray44 = sAMRecord42.getBaseQualities();
        sAMRecord17.setReadBases(byteArray44);
        htsjdk.samtools.SAMFileHeader sAMFileHeader46 = null;
        htsjdk.samtools.SAMRecord sAMRecord47 = new htsjdk.samtools.SAMRecord(sAMFileHeader46);
        sAMRecord47.setDuplicateReadFlag(false);
        java.lang.Object obj50 = null;
        boolean boolean51 = sAMRecord47.equals(obj50);
        htsjdk.samtools.SAMFileHeader sAMFileHeader52 = null;
        htsjdk.samtools.SAMRecord sAMRecord53 = new htsjdk.samtools.SAMRecord(sAMFileHeader52);
        sAMRecord53.setDuplicateReadFlag(false);
        sAMRecord53.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj58 = sAMRecord47.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord59 = sAMRecord47.deepCopy();
        sAMRecord59.setReadName("");
        byte[] byteArray62 = htsjdk.samtools.SAMRecord.NULL_SEQUENCE;
        sAMRecord59.setOriginalBaseQualities(byteArray62);
        sAMRecord17.setOriginalBaseQualities(byteArray62);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNull(obj41);
        org.junit.Assert.assertNotNull(sAMRecord42);
        org.junit.Assert.assertTrue("'" + int43 + "' != '" + 0 + "'", int43 == 0);
        org.junit.Assert.assertNotNull(byteArray44);
        org.junit.Assert.assertArrayEquals(byteArray44, new byte[] {});
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + false + "'", boolean51 == false);
        org.junit.Assert.assertNull(obj58);
        org.junit.Assert.assertNotNull(sAMRecord59);
        org.junit.Assert.assertNotNull(byteArray62);
        org.junit.Assert.assertArrayEquals(byteArray62, new byte[] {});
    }

    @Test
    public void test125() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test125");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        int int12 = sAMRecord1.getStart();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray14 = sAMRecord1.getSignedByteArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 1 + "'", int12 == 1);
    }

    @Test
    public void test126() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test126");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord13.getAlignmentBlocks();
        java.lang.String str32 = sAMRecord13.getReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader33 = null;
        htsjdk.samtools.SAMRecord sAMRecord34 = new htsjdk.samtools.SAMRecord(sAMFileHeader33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = sAMRecord34.getHeader();
        sAMRecord34.setProperPairFlag(true);
        byte[] byteArray38 = sAMRecord34.getBaseQualities();
        java.lang.Object obj39 = sAMRecord34.clone();
        boolean boolean40 = sAMRecord13.overlaps((htsjdk.samtools.util.Locatable) sAMRecord34);
        htsjdk.samtools.SAMFileHeader sAMFileHeader41 = sAMRecord34.getHeader();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertEquals("'" + str32 + "' != '" + "*" + "'", str32, "*");
        org.junit.Assert.assertNull(sAMFileHeader35);
        org.junit.Assert.assertNotNull(byteArray38);
        org.junit.Assert.assertArrayEquals(byteArray38, new byte[] {});
        org.junit.Assert.assertNotNull(obj39);
        org.junit.Assert.assertEquals(obj39.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj39), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj39), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
        org.junit.Assert.assertNull(sAMFileHeader41);
    }

    @Test
    public void test127() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test127");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray11 = sAMRecord1.getFloatArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
    }

    @Test
    public void test128() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test128");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        sAMRecord1.setMappingQuality((-1));
        java.lang.Object obj17 = sAMRecord1.clone();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(obj17);
        org.junit.Assert.assertEquals(obj17.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj17), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj17), "null 0b aligned to *:0--1.");
    }

    @Test
    public void test129() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test129");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        java.lang.String str14 = sAMRecord9.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = sAMRecord16.getHeader();
        byte[] byteArray20 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord16.setBaseQualities(byteArray20);
        sAMRecord9.setBaseQualities(byteArray20);
        sAMRecord1.setBaseQualities(byteArray20);
        boolean boolean24 = sAMRecord1.getReadNegativeStrandFlag();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList26 = sAMRecord1.validateCigar((long) (byte) 10);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Integer int27 = sAMRecord1.getReferenceIndex();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "null" + "'", str14, "null");
        org.junit.Assert.assertNull(sAMFileHeader17);
        org.junit.Assert.assertNotNull(byteArray20);
        org.junit.Assert.assertArrayEquals(byteArray20, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
        org.junit.Assert.assertNull(sAMValidationErrorList26);
    }

    @Test
    public void test130() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test130");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = null;
        htsjdk.samtools.SAMRecord sAMRecord15 = new htsjdk.samtools.SAMRecord(sAMFileHeader14);
        sAMRecord15.setDuplicateReadFlag(false);
        sAMRecord15.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj20 = sAMRecord9.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord21 = sAMRecord9.deepCopy();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setDuplicateReadFlag(false);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMRecord23.equals(obj26);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList29 = sAMRecord23.isValid(false);
        sAMRecord23.setMateReferenceName("hi!");
        sAMRecord23.setAlignmentStart((int) (short) 1);
        int int34 = sAMRecord23.getStart();
        java.lang.Object obj35 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord21, (java.lang.Object) int34);
        int int36 = sAMRecord21.getCigarLength();
        java.lang.String str37 = sAMRecord21.getReferenceName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertTrue("'" + int36 + "' != '" + 0 + "'", int36 == 0);
        org.junit.Assert.assertEquals("'" + str37 + "' != '" + "*" + "'", str37, "*");
    }

    @Test
    public void test131() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test131");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        sAMRecord1.setHeader(sAMFileHeader6);
        java.lang.String[] strArray10 = new java.lang.String[] { "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*", "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n" };
        java.util.ArrayList<java.lang.String> strList11 = new java.util.ArrayList<java.lang.String>();
        boolean boolean12 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList11, strArray10);
        java.util.List<java.lang.String> strList13 = htsjdk.samtools.SAMRecord.TAGS_TO_REVERSE;
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList11, (java.util.Collection<java.lang.String>) strList13, true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*", "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n" });
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(strList13);
    }

    @Test
    public void test132() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test132");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        java.lang.String str14 = sAMRecord1.getReferenceName();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList16 = sAMRecord1.validateCigar((long) (byte) 100);
        java.lang.String str17 = sAMRecord1.getCigarString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertNull(sAMValidationErrorList16);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "*" + "'", str17, "*");
    }

    @Test
    public void test133() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test133");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        byte[] byteArray8 = sAMRecord1.getReadBases();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(byteArray8);
        org.junit.Assert.assertArrayEquals(byteArray8, new byte[] {});
    }

    @Test
    public void test134() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test134");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        boolean boolean13 = sAMRecord1.getDuplicateReadFlag();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Character char15 = sAMRecord1.getCharacterAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test135() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test135");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        sAMRecord1.setMateNegativeStrandFlag(true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test136() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test136");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord13.getAlignmentBlocks();
        java.lang.String str32 = sAMRecord13.getReferenceName();
        java.lang.Object obj33 = null;
        java.lang.Object obj34 = sAMRecord13.getTransientAttribute(obj33);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertEquals("'" + str32 + "' != '" + "*" + "'", str32, "*");
        org.junit.Assert.assertNull(obj34);
    }

    @Test
    public void test137() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test137");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        sAMRecord30.setDuplicateReadFlag(false);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMRecord30.equals(obj33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        sAMRecord36.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj41 = sAMRecord30.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord42 = sAMRecord30.deepCopy();
        int int43 = sAMRecord42.getAlignmentStart();
        byte[] byteArray44 = sAMRecord42.getBaseQualities();
        sAMRecord17.setReadBases(byteArray44);
        sAMRecord17.setReadNegativeStrandFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str49 = sAMRecord17.getStringAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNull(obj41);
        org.junit.Assert.assertNotNull(sAMRecord42);
        org.junit.Assert.assertTrue("'" + int43 + "' != '" + 0 + "'", int43 == 0);
        org.junit.Assert.assertNotNull(byteArray44);
        org.junit.Assert.assertArrayEquals(byteArray44, new byte[] {});
    }

    @Test
    public void test138() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test138");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        boolean boolean10 = sAMRecord1.getSupplementaryAlignmentFlag();
        sAMRecord1.setReadUmappedFlag(true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test139() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test139");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        sAMRecord1.reverseComplement();
        int int10 = sAMRecord1.getMappingQuality();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 0 + "'", int10 == 0);
    }

    @Test
    public void test140() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test140");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        sAMRecord13.setReadFailsVendorQualityCheckFlag(false);
        htsjdk.samtools.SAMFileSource sAMFileSource16 = sAMRecord13.getFileSource();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNull(sAMFileSource16);
    }

    @Test
    public void test141() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test141");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        java.lang.String str12 = sAMRecord1.getSAMString();
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet13 = sAMRecord1.getSAMFlags();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n" + "'", str12, "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n");
        org.junit.Assert.assertNotNull(sAMFlagSet13);
    }

    @Test
    public void test142() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test142");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        boolean boolean13 = sAMRecord1.getDuplicateReadFlag();
        sAMRecord1.setProperPairFlag(true);
        byte[] byteArray16 = sAMRecord1.getBaseQualities();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNotNull(byteArray16);
        org.junit.Assert.assertArrayEquals(byteArray16, new byte[] {});
    }

    @Test
    public void test143() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test143");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList25 = sAMRecord1.isValid(false);
        byte[] byteArray26 = sAMRecord1.getOriginalBaseQualities();
        sAMRecord1.reverseComplement(false);
        java.lang.Long long30 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 0);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean31 = sAMRecord1.getMateNegativeStrandFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(sAMValidationErrorList25);
        org.junit.Assert.assertNull(byteArray26);
        org.junit.Assert.assertNull(long30);
    }

    @Test
    public void test144() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test144");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        sAMRecord30.setDuplicateReadFlag(false);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMRecord30.equals(obj33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        sAMRecord36.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj41 = sAMRecord30.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord42 = sAMRecord30.deepCopy();
        int int43 = sAMRecord42.getAlignmentStart();
        byte[] byteArray44 = sAMRecord42.getBaseQualities();
        sAMRecord17.setReadBases(byteArray44);
        sAMRecord17.setReadNegativeStrandFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray49 = sAMRecord17.getSignedByteArrayAttribute("null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?1?0?*?hi!?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNull(obj41);
        org.junit.Assert.assertNotNull(sAMRecord42);
        org.junit.Assert.assertTrue("'" + int43 + "' != '" + 0 + "'", int43 == 0);
        org.junit.Assert.assertNotNull(byteArray44);
        org.junit.Assert.assertArrayEquals(byteArray44, new byte[] {});
    }

    @Test
    public void test145() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test145");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        java.lang.String str4 = sAMRecord1.toString();
        sAMRecord1.setDuplicateReadFlag(false);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertEquals("'" + str4 + "' != '" + "null 0b aligned to *:0--1." + "'", str4, "null 0b aligned to *:0--1.");
    }

    @Test
    public void test146() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test146");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int6 = sAMRecord1.getStart();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test147() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test147");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setAlignmentStart((int) (short) 100);
        int int12 = sAMRecord1.getMappingQuality();
        sAMRecord1.setReadName("null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 100 + "'", int12 == 100);
    }

    @Test
    public void test148() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test148");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getInferredInsertSize();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test149() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test149");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setFlags((int) (short) 0);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
    }

    @Test
    public void test150() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test150");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.Cigar cigar8 = null;
        sAMRecord1.setCigar(cigar8);
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray11 = sAMRecord1.getSignedIntArrayAttribute("null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?*?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test151() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test151");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        sAMRecord1.setReadString("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        sAMRecord1.setAlignmentStart((int) (short) 100);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test152() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test152");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        java.lang.String str12 = sAMRecord1.getSAMString();
        int int13 = sAMRecord1.getUnclippedEnd();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n" + "'", str12, "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 0 + "'", int13 == 0);
    }

    @Test
    public void test153() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test153");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        byte[] byteArray9 = sAMRecord1.getBaseQualities();
        java.lang.String str10 = sAMRecord1.format();
        java.lang.Object obj11 = sAMRecord1.clone();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(byteArray9);
        org.junit.Assert.assertArrayEquals(byteArray9, new byte[] {});
        org.junit.Assert.assertEquals("'" + str10 + "' != '" + "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*" + "'", str10, "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        org.junit.Assert.assertNotNull(obj11);
        org.junit.Assert.assertEquals(obj11.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj11), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj11), "null 0b aligned to *:0--1.");
    }

    @Test
    public void test154() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test154");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader13 = null;
        htsjdk.samtools.SAMRecord sAMRecord14 = new htsjdk.samtools.SAMRecord(sAMFileHeader13);
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = sAMRecord14.getHeader();
        sAMRecord14.setProperPairFlag(true);
        boolean boolean18 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord14);
        int int19 = sAMRecord14.getMateAlignmentStart();
        sAMRecord14.setProperPairFlag(true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertNull(sAMFileHeader15);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
    }

    @Test
    public void test155() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test155");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        int int7 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) 1);
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
    }

    @Test
    public void test156() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test156");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        htsjdk.samtools.SAMFileHeader sAMFileHeader9 = sAMRecord8.getHeader();
        byte[] byteArray12 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord8.setBaseQualities(byteArray12);
        sAMRecord1.setBaseQualities(byteArray12);
        sAMRecord1.reverseComplement();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertNull(sAMFileHeader9);
        org.junit.Assert.assertNotNull(byteArray12);
        org.junit.Assert.assertArrayEquals(byteArray12, new byte[] { (byte) 0, (byte) 0 });
    }

    @Test
    public void test157() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test157");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        byte[] byteArray14 = sAMRecord1.getReadBases();
        sAMRecord1.reverseComplement(false);
        java.lang.Long long18 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertNotNull(byteArray14);
        org.junit.Assert.assertArrayEquals(byteArray14, new byte[] {});
        org.junit.Assert.assertNull(long18);
    }

    @Test
    public void test158() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test158");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord13.getAlignmentBlocks();
        java.lang.String str32 = sAMRecord13.getReferenceName();
        java.lang.Class<?> wildcardClass33 = sAMRecord13.getClass();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertEquals("'" + str32 + "' != '" + "*" + "'", str32, "*");
        org.junit.Assert.assertNotNull(wildcardClass33);
    }

    @Test
    public void test159() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test159");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        boolean boolean8 = sAMRecord1.isSecondaryAlignment();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + true + "'", boolean8 == true);
    }

    @Test
    public void test160() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test160");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.ValidationStringency validationStringency14 = null;
        sAMRecord1.setValidationStringency(validationStringency14);
        int int16 = sAMRecord1.getReadLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
    }

    @Test
    public void test161() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test161");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        sAMRecord1.setFlags(536870912);
        java.lang.String str18 = sAMRecord1.getBaseQualityString();
        int int19 = sAMRecord1.getAlignmentStart();
        java.lang.String str20 = sAMRecord1.toString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader21 = null;
        htsjdk.samtools.SAMRecord sAMRecord22 = new htsjdk.samtools.SAMRecord(sAMFileHeader21);
        sAMRecord22.setDuplicateReadFlag(false);
        java.lang.Object obj25 = null;
        boolean boolean26 = sAMRecord22.equals(obj25);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList28 = sAMRecord22.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        int int32 = sAMRecord30.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean34 = sAMRecord22.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord30, (int) ' ');
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        java.lang.Object obj39 = null;
        boolean boolean40 = sAMRecord36.equals(obj39);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList42 = sAMRecord36.isValid(false);
        sAMRecord36.setMateReferenceName("hi!");
        java.lang.Object obj45 = sAMRecord22.getTransientAttribute((java.lang.Object) sAMRecord36);
        boolean boolean46 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord36);
        sAMRecord1.setFlags(1);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "*" + "'", str18, "*");
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertEquals("'" + str20 + "' != '" + "null 0b aligned to *:0--1." + "'", str20, "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList28);
        org.junit.Assert.assertTrue("'" + int32 + "' != '" + 0 + "'", int32 == 0);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + false + "'", boolean40 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList42);
        org.junit.Assert.assertNull(obj45);
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + true + "'", boolean46 == true);
    }

    @Test
    public void test162() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test162");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord7 = sAMRecord1.getReadGroup();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean8 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertNull(sAMReadGroupRecord7);
    }

    @Test
    public void test163() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test163");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        sAMRecord30.setDuplicateReadFlag(false);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMRecord30.equals(obj33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        sAMRecord36.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj41 = sAMRecord30.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord42 = sAMRecord30.deepCopy();
        int int43 = sAMRecord42.getAlignmentStart();
        byte[] byteArray44 = sAMRecord42.getBaseQualities();
        sAMRecord17.setReadBases(byteArray44);
        boolean boolean46 = sAMRecord17.isSecondaryOrSupplementary();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNull(obj41);
        org.junit.Assert.assertNotNull(sAMRecord42);
        org.junit.Assert.assertTrue("'" + int43 + "' != '" + 0 + "'", int43 == 0);
        org.junit.Assert.assertNotNull(byteArray44);
        org.junit.Assert.assertArrayEquals(byteArray44, new byte[] {});
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + false + "'", boolean46 == false);
    }

    @Test
    public void test164() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test164");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        int int15 = sAMRecord1.getReadLength();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        sAMRecord17.setDuplicateReadFlag(false);
        java.lang.Object obj20 = null;
        boolean boolean21 = sAMRecord17.equals(obj20);
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setDuplicateReadFlag(false);
        sAMRecord23.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj28 = sAMRecord17.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency29 = null;
        sAMRecord17.setValidationStringency(validationStringency29);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord31 = sAMRecord17.getReadGroup();
        sAMRecord17.setFlags(536870912);
        java.lang.String str34 = sAMRecord17.getBaseQualityString();
        int int35 = sAMRecord17.getAlignmentStart();
        java.lang.Object obj36 = sAMRecord1.getTransientAttribute((java.lang.Object) int35);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + false + "'", boolean21 == false);
        org.junit.Assert.assertNull(obj28);
        org.junit.Assert.assertNull(sAMReadGroupRecord31);
        org.junit.Assert.assertEquals("'" + str34 + "' != '" + "*" + "'", str34, "*");
        org.junit.Assert.assertTrue("'" + int35 + "' != '" + 0 + "'", int35 == 0);
        org.junit.Assert.assertNull(obj36);
    }

    @Test
    public void test165() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test165");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        int int16 = sAMRecord1.getReadPositionAtReferencePosition((int) (short) 0, false);
        boolean boolean17 = sAMRecord1.isSecondaryOrSupplementary();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
    }

    @Test
    public void test166() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test166");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        java.lang.String str15 = sAMRecord1.getCigarString();
        sAMRecord1.setReadString("null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "*" + "'", str15, "*");
    }

    @Test
    public void test167() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test167");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        sAMRecord1.setReadName("hi!");
        int int18 = sAMRecord1.getReferencePositionAtReadPosition((int) (short) 0);
        int int19 = sAMRecord1.getCigarLength();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean21 = sAMRecord1.isUnsignedArrayAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + 0 + "'", int18 == 0);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
    }

    @Test
    public void test168() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test168");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord13.getAlignmentBlocks();
        java.lang.String str32 = sAMRecord13.getReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader33 = null;
        htsjdk.samtools.SAMRecord sAMRecord34 = new htsjdk.samtools.SAMRecord(sAMFileHeader33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = sAMRecord34.getHeader();
        sAMRecord34.setProperPairFlag(true);
        byte[] byteArray38 = sAMRecord34.getBaseQualities();
        java.lang.Object obj39 = sAMRecord34.clone();
        boolean boolean40 = sAMRecord13.overlaps((htsjdk.samtools.util.Locatable) sAMRecord34);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean42 = sAMRecord34.hasAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertEquals("'" + str32 + "' != '" + "*" + "'", str32, "*");
        org.junit.Assert.assertNull(sAMFileHeader35);
        org.junit.Assert.assertNotNull(byteArray38);
        org.junit.Assert.assertArrayEquals(byteArray38, new byte[] {});
        org.junit.Assert.assertNotNull(obj39);
        org.junit.Assert.assertEquals(obj39.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj39), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj39), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
    }

    @Test
    public void test169() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test169");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        java.lang.String str14 = sAMRecord9.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = sAMRecord16.getHeader();
        byte[] byteArray20 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord16.setBaseQualities(byteArray20);
        sAMRecord9.setBaseQualities(byteArray20);
        sAMRecord1.setBaseQualities(byteArray20);
        boolean boolean24 = sAMRecord1.getReadNegativeStrandFlag();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Integer int25 = sAMRecord1.getReferenceIndex();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "null" + "'", str14, "null");
        org.junit.Assert.assertNull(sAMFileHeader17);
        org.junit.Assert.assertNotNull(byteArray20);
        org.junit.Assert.assertArrayEquals(byteArray20, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
    }

    @Test
    public void test170() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test170");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        int int4 = sAMRecord1.getEnd();
        int int5 = sAMRecord1.getAlignmentStart();
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + (-1) + "'", int4 == (-1));
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test171() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test171");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        byte[] byteArray14 = sAMRecord1.getReadBases();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray16 = sAMRecord1.getSignedByteArrayAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertNotNull(byteArray14);
        org.junit.Assert.assertArrayEquals(byteArray14, new byte[] {});
    }

    @Test
    public void test172() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test172");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = null;
        htsjdk.samtools.SAMRecord sAMRecord30 = new htsjdk.samtools.SAMRecord(sAMFileHeader29);
        sAMRecord30.setDuplicateReadFlag(false);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMRecord30.equals(obj33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setDuplicateReadFlag(false);
        sAMRecord36.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj41 = sAMRecord30.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord42 = sAMRecord30.deepCopy();
        int int43 = sAMRecord42.getAlignmentStart();
        byte[] byteArray44 = sAMRecord42.getBaseQualities();
        sAMRecord17.setReadBases(byteArray44);
        sAMRecord17.setSecondOfPairFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray49 = sAMRecord17.getSignedByteArrayAttribute("null\t0\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?-1?*?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNull(obj41);
        org.junit.Assert.assertNotNull(sAMRecord42);
        org.junit.Assert.assertTrue("'" + int43 + "' != '" + 0 + "'", int43 == 0);
        org.junit.Assert.assertNotNull(byteArray44);
        org.junit.Assert.assertArrayEquals(byteArray44, new byte[] {});
    }

    @Test
    public void test173() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test173");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getUnclippedEnd();
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList10 = sAMRecord1.isValid(false);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList10);
    }

    @Test
    public void test174() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test174");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getAlignmentStart();
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
    }

    @Test
    public void test175() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test175");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        boolean boolean25 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.lang.Long long27 = sAMRecord13.getUnsignedIntegerAttribute((short) (byte) 10);
        byte[] byteArray28 = sAMRecord13.getVariableBinaryRepresentation();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNull(long27);
        org.junit.Assert.assertNull(byteArray28);
    }

    @Test
    public void test176() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test176");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.lang.Long long25 = sAMRecord18.getUnsignedIntegerAttribute((short) 1);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNull(long25);
    }

    @Test
    public void test177() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test177");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        htsjdk.samtools.Cigar cigar14 = sAMRecord1.getCigar();
        sAMRecord1.setAlignmentStart((int) (short) -1);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNotNull(cigar14);
    }

    @Test
    public void test178() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test178");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        byte[] byteArray5 = sAMRecord1.getBaseQualities();
        java.lang.Object obj6 = sAMRecord1.clone();
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList15 = sAMRecord9.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean21 = sAMRecord9.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) ' ');
        java.lang.String str22 = sAMRecord9.getBaseQualityString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader23 = null;
        sAMRecord9.setHeaderStrict(sAMFileHeader23);
        sAMRecord9.setReadNegativeStrandFlag(false);
        htsjdk.samtools.ValidationStringency validationStringency27 = sAMRecord9.getValidationStringency();
        java.lang.Object obj28 = sAMRecord1.setTransientAttribute((java.lang.Object) "null\t0\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n", (java.lang.Object) validationStringency27);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] {});
        org.junit.Assert.assertNotNull(obj6);
        org.junit.Assert.assertEquals(obj6.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj6), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj6), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "*" + "'", str22, "*");
        org.junit.Assert.assertTrue("'" + validationStringency27 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency27.equals(htsjdk.samtools.ValidationStringency.SILENT));
        org.junit.Assert.assertNull(obj28);
    }

    @Test
    public void test179() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test179");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        htsjdk.samtools.SAMRecord sAMRecord14 = sAMRecord13.deepCopy();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNotNull(sAMRecord14);
    }

    @Test
    public void test180() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test180");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        int int7 = sAMRecord1.getMappingQuality();
        int int8 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 0 + "'", int8 == 0);
    }

    @Test
    public void test181() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test181");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        java.lang.String str14 = sAMRecord13.getPairedReadName();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "null" + "'", str14, "null");
    }

    @Test
    public void test182() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test182");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test183() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test183");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        sAMRecord1.setInferredInsertSize(4680);
        boolean boolean8 = sAMRecord1.isSecondaryOrSupplementary();
        java.lang.String[] strArray11 = new java.lang.String[] { "", "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n" };
        java.util.ArrayList<java.lang.String> strList12 = new java.util.ArrayList<java.lang.String>();
        boolean boolean13 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList12, strArray11);
        java.lang.String[] strArray19 = new java.lang.String[] { "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n", "null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n", "null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList20 = new java.util.ArrayList<java.lang.String>();
        boolean boolean21 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList20, strArray19);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList12, (java.util.Collection<java.lang.String>) strList20, false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(strArray11);
        org.junit.Assert.assertArrayEquals(strArray11, new java.lang.String[] { "", "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n" });
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n", "null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n", "null\t64\t*\t0\t0\t*\thi!\t0\t0\t*\t*\n", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
    }

    @Test
    public void test184() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test184");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getLengthOnReference();
        boolean boolean7 = sAMRecord1.isSecondaryOrSupplementary();
        int int10 = sAMRecord1.getReadPositionAtReferencePosition((int) 'a', true);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 0 + "'", int10 == 0);
    }

    @Test
    public void test185() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test185");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList13 = sAMRecord9.validateCigar((long) (byte) 100);
        int int14 = sAMRecord9.getUnclippedStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        sAMRecord16.setMappingQuality((-1));
        boolean boolean19 = sAMRecord16.getReadNegativeStrandFlag();
        int int20 = sAMRecord16.getLengthOnReference();
        sAMRecord16.setSecondaryAlignment(true);
        boolean boolean23 = sAMRecord16.getReadPairedFlag();
        java.lang.Object obj25 = sAMRecord9.setTransientAttribute((java.lang.Object) sAMRecord16, (java.lang.Object) 100);
        boolean boolean26 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.lang.String str27 = sAMRecord9.getPairedReadName();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
        org.junit.Assert.assertTrue("'" + int20 + "' != '" + 0 + "'", int20 == 0);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertNull(obj25);
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + true + "'", boolean26 == true);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "null" + "'", str27, "null");
    }

    @Test
    public void test186() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test186");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        boolean boolean25 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.lang.Long long27 = sAMRecord13.getUnsignedIntegerAttribute((short) (byte) 10);
        // The following exception was thrown during execution in test generation
        try {
            int int28 = sAMRecord13.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNull(long27);
    }

    @Test
    public void test187() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test187");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader13 = null;
        htsjdk.samtools.SAMRecord sAMRecord14 = new htsjdk.samtools.SAMRecord(sAMFileHeader13);
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = sAMRecord14.getHeader();
        sAMRecord14.setProperPairFlag(true);
        boolean boolean18 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord14);
        int int19 = sAMRecord14.getMateAlignmentStart();
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList20 = sAMRecord14.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertNull(sAMFileHeader15);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertNotNull(sAMTagAndValueList20);
    }

    @Test
    public void test188() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test188");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        int int16 = sAMRecord1.getEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + (-1) + "'", int16 == (-1));
    }

    @Test
    public void test189() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test189");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        sAMRecord1.setReadUmappedFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray15 = sAMRecord1.getFloatArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test190() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test190");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        int int14 = sAMRecord13.getAlignmentStart();
        int int15 = sAMRecord13.getAttributesBinarySize();
        sAMRecord13.setSecondaryAlignment(false);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList19 = sAMRecord13.validateCigar((long) (short) 0);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + (-1) + "'", int15 == (-1));
        org.junit.Assert.assertNull(sAMValidationErrorList19);
    }

    @Test
    public void test191() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test191");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int8 = sAMRecord1.getReadPositionAtReferencePosition(0);
        int int9 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 0 + "'", int8 == 0);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
    }

    @Test
    public void test192() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test192");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = null;
        htsjdk.samtools.SAMRecord sAMRecord15 = new htsjdk.samtools.SAMRecord(sAMFileHeader14);
        sAMRecord15.setDuplicateReadFlag(false);
        java.lang.Object obj18 = null;
        boolean boolean19 = sAMRecord15.equals(obj18);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList21 = sAMRecord15.isValid(false);
        sAMRecord15.setMateReferenceName("hi!");
        java.lang.Object obj24 = sAMRecord1.getTransientAttribute((java.lang.Object) sAMRecord15);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean26 = sAMRecord1.hasAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList21);
        org.junit.Assert.assertNull(obj24);
    }

    @Test
    public void test193() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test193");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        int int14 = sAMRecord1.getStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
    }

    @Test
    public void test194() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test194");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord13.getAlignmentBlocks();
        java.lang.String str32 = sAMRecord13.getReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader33 = null;
        htsjdk.samtools.SAMRecord sAMRecord34 = new htsjdk.samtools.SAMRecord(sAMFileHeader33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = sAMRecord34.getHeader();
        sAMRecord34.setProperPairFlag(true);
        byte[] byteArray38 = sAMRecord34.getBaseQualities();
        java.lang.Object obj39 = sAMRecord34.clone();
        boolean boolean40 = sAMRecord13.overlaps((htsjdk.samtools.util.Locatable) sAMRecord34);
        sAMRecord13.setAlignmentStart((int) (byte) 1);
        byte[] byteArray43 = sAMRecord13.getReadBases();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertEquals("'" + str32 + "' != '" + "*" + "'", str32, "*");
        org.junit.Assert.assertNull(sAMFileHeader35);
        org.junit.Assert.assertNotNull(byteArray38);
        org.junit.Assert.assertArrayEquals(byteArray38, new byte[] {});
        org.junit.Assert.assertNotNull(obj39);
        org.junit.Assert.assertEquals(obj39.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj39), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj39), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
        org.junit.Assert.assertNotNull(byteArray43);
        org.junit.Assert.assertArrayEquals(byteArray43, new byte[] {});
    }

    @Test
    public void test195() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test195");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        java.lang.String str4 = sAMRecord1.toString();
        java.lang.Class<?> wildcardClass5 = sAMRecord1.getClass();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertEquals("'" + str4 + "' != '" + "null 0b aligned to *:0--1." + "'", str4, "null 0b aligned to *:0--1.");
        org.junit.Assert.assertNotNull(wildcardClass5);
    }

    @Test
    public void test196() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test196");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int6 = sAMRecord1.getUnclippedStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        boolean boolean15 = sAMRecord8.getReadPairedFlag();
        java.lang.Object obj17 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord8, (java.lang.Object) 100);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader20 = null;
        htsjdk.samtools.SAMRecord sAMRecord21 = new htsjdk.samtools.SAMRecord(sAMFileHeader20);
        java.lang.Long long23 = sAMRecord21.getUnsignedIntegerAttribute((short) (byte) 10);
        java.lang.Object obj24 = sAMRecord21.clone();
        boolean boolean25 = sAMRecord1.equals(obj24);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNull(obj17);
        org.junit.Assert.assertNull(long23);
        org.junit.Assert.assertNotNull(obj24);
        org.junit.Assert.assertEquals(obj24.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj24), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj24), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + true + "'", boolean25 == true);
    }

    @Test
    public void test197() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test197");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        int int16 = sAMRecord1.getUnclippedEnd();
        htsjdk.samtools.SAMFileSource sAMFileSource17 = sAMRecord1.getFileSource();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + (-1) + "'", int16 == (-1));
        org.junit.Assert.assertNull(sAMFileSource17);
    }

    @Test
    public void test198() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test198");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        int int8 = sAMRecord1.getAlignmentEnd();
        int int9 = sAMRecord1.getInferredInsertSize();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + (-1) + "'", int8 == (-1));
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test199() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test199");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        boolean boolean13 = sAMRecord1.getDuplicateReadFlag();
        int int14 = sAMRecord1.getLengthOnReference();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
    }

    @Test
    public void test200() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test200");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test201() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test201");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        int int7 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test202() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test202");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        int int16 = sAMRecord1.getReferencePositionAtReadPosition((int) 'a');
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet17 = sAMRecord1.getSAMFlags();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
        org.junit.Assert.assertNotNull(sAMFlagSet17);
    }

    @Test
    public void test203() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test203");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setDuplicateReadFlag(false);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMRecord8.equals(obj11);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList14 = sAMRecord8.isValid(false);
        sAMRecord8.setMateReferenceName("hi!");
        sAMRecord8.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet19 = sAMRecord8.getSAMFlags();
        java.lang.Object obj20 = sAMRecord1.removeTransientAttribute((java.lang.Object) sAMFlagSet19);
        sAMRecord1.setMateReferenceName("");
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList14);
        org.junit.Assert.assertNotNull(sAMFlagSet19);
        org.junit.Assert.assertNull(obj20);
    }

    @Test
    public void test204() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test204");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSupplementaryAlignmentFlag(true);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Class<?> wildcardClass9 = sAMRecord1.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNotNull(wildcardClass9);
    }

    @Test
    public void test205() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test205");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        boolean boolean13 = sAMRecord1.getReadNegativeStrandFlag();
        int int14 = sAMRecord1.getFlags();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
    }

    @Test
    public void test206() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test206");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        sAMRecord1.setHeader(sAMFileHeader6);
        boolean boolean8 = sAMRecord1.getReadNegativeStrandFlag();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test207() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test207");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        boolean boolean25 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord13);
        htsjdk.samtools.SAMFileHeader sAMFileHeader26 = null;
        htsjdk.samtools.SAMRecord sAMRecord27 = new htsjdk.samtools.SAMRecord(sAMFileHeader26);
        sAMRecord27.setDuplicateReadFlag(false);
        java.lang.Object obj30 = null;
        boolean boolean31 = sAMRecord27.equals(obj30);
        htsjdk.samtools.SAMFileHeader sAMFileHeader32 = null;
        htsjdk.samtools.SAMRecord sAMRecord33 = new htsjdk.samtools.SAMRecord(sAMFileHeader32);
        sAMRecord33.setDuplicateReadFlag(false);
        sAMRecord33.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj38 = sAMRecord27.getTransientAttribute((java.lang.Object) true);
        java.lang.Object obj39 = sAMRecord1.removeTransientAttribute((java.lang.Object) sAMRecord27);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertNull(obj38);
        org.junit.Assert.assertNull(obj39);
    }

    @Test
    public void test208() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test208");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Float float13 = sAMRecord1.getFloatAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test209() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test209");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        boolean boolean25 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.lang.Long long27 = sAMRecord13.getUnsignedIntegerAttribute((short) (byte) 10);
        java.util.List<java.lang.String> strList28 = htsjdk.samtools.SAMRecord.TAGS_TO_REVERSE_COMPLEMENT;
        java.util.List<java.lang.String> strList29 = htsjdk.samtools.SAMRecord.TAGS_TO_REVERSE_COMPLEMENT;
        sAMRecord13.reverseComplement((java.util.Collection<java.lang.String>) strList28, (java.util.Collection<java.lang.String>) strList29, true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNull(long27);
        org.junit.Assert.assertNotNull(strList28);
        org.junit.Assert.assertNotNull(strList29);
    }

    @Test
    public void test210() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test210");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        sAMRecord1.setFlags((int) (byte) 100);
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray11 = sAMRecord1.getFloatArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test211() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test211");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
    }

    @Test
    public void test212() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test212");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = null;
        htsjdk.samtools.SAMRecord sAMRecord15 = new htsjdk.samtools.SAMRecord(sAMFileHeader14);
        sAMRecord15.setDuplicateReadFlag(false);
        sAMRecord15.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj20 = sAMRecord9.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord21 = sAMRecord9.deepCopy();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setDuplicateReadFlag(false);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMRecord23.equals(obj26);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList29 = sAMRecord23.isValid(false);
        sAMRecord23.setMateReferenceName("hi!");
        sAMRecord23.setAlignmentStart((int) (short) 1);
        int int34 = sAMRecord23.getStart();
        java.lang.Object obj35 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord21, (java.lang.Object) int34);
        int int36 = sAMRecord1.getMateAlignmentStart();
        java.lang.String str37 = sAMRecord1.getMateReferenceName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertTrue("'" + int36 + "' != '" + 0 + "'", int36 == 0);
        org.junit.Assert.assertEquals("'" + str37 + "' != '" + "*" + "'", str37, "*");
    }

    @Test
    public void test213() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test213");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setAlignmentStart((int) (short) 100);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList13 = sAMRecord1.isValid(false);
        int int14 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(sAMValidationErrorList13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 99 + "'", int14 == 99);
    }

    @Test
    public void test214() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test214");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        sAMRecord1.setAlignmentStart((-1));
        sAMRecord1.setNotPrimaryAlignmentFlag(false);
        sAMRecord1.setMappingQuality((int) (byte) 100);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test215() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test215");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        sAMRecord1.setFlags(536870912);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMRecord19.equals(obj22);
        java.lang.String str24 = sAMRecord19.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader25 = null;
        htsjdk.samtools.SAMRecord sAMRecord26 = new htsjdk.samtools.SAMRecord(sAMFileHeader25);
        htsjdk.samtools.SAMFileHeader sAMFileHeader27 = sAMRecord26.getHeader();
        byte[] byteArray30 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord26.setBaseQualities(byteArray30);
        sAMRecord19.setBaseQualities(byteArray30);
        sAMRecord1.setBaseQualities(byteArray30);
        htsjdk.samtools.SAMFileHeader sAMFileHeader34 = sAMRecord1.getHeader();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertEquals("'" + str24 + "' != '" + "null" + "'", str24, "null");
        org.junit.Assert.assertNull(sAMFileHeader27);
        org.junit.Assert.assertNotNull(byteArray30);
        org.junit.Assert.assertArrayEquals(byteArray30, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNull(sAMFileHeader34);
    }

    @Test
    public void test216() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test216");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        htsjdk.samtools.SAMRecord sAMRecord7 = sAMRecord1.deepCopy();
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet8 = sAMRecord7.getSAMFlags();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(sAMRecord7);
        org.junit.Assert.assertNotNull(sAMFlagSet8);
    }

    @Test
    public void test217() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test217");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        byte[] byteArray8 = sAMRecord1.getReadBases();
        org.junit.Assert.assertNotNull(byteArray8);
        org.junit.Assert.assertArrayEquals(byteArray8, new byte[] {});
    }

    @Test
    public void test218() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test218");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        sAMRecord1.setFlags(536870912);
        java.lang.String str18 = sAMRecord1.getBaseQualityString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        sAMRecord20.setMappingQuality((-1));
        boolean boolean23 = sAMRecord20.getReadNegativeStrandFlag();
        int int24 = sAMRecord20.getLengthOnReference();
        sAMRecord20.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader27 = null;
        htsjdk.samtools.SAMRecord sAMRecord28 = new htsjdk.samtools.SAMRecord(sAMFileHeader27);
        sAMRecord28.setDuplicateReadFlag(false);
        java.lang.Object obj31 = null;
        boolean boolean32 = sAMRecord28.equals(obj31);
        boolean boolean33 = sAMRecord20.overlaps((htsjdk.samtools.util.Locatable) sAMRecord28);
        boolean boolean34 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord20);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean35 = sAMRecord20.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "*" + "'", str18, "*");
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + 0 + "'", int24 == 0);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
    }

    @Test
    public void test219() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test219");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        boolean boolean31 = sAMRecord13.getNotPrimaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
    }

    @Test
    public void test220() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test220");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList25 = sAMRecord1.isValid(false);
        byte[] byteArray26 = sAMRecord1.getOriginalBaseQualities();
        sAMRecord1.reverseComplement(false);
        sAMRecord1.setSupplementaryAlignmentFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray32 = sAMRecord1.getSignedIntArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(sAMValidationErrorList25);
        org.junit.Assert.assertNull(byteArray26);
    }

    @Test
    public void test221() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test221");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        htsjdk.samtools.SAMRecord sAMRecord7 = sAMRecord1.deepCopy();
        boolean boolean8 = sAMRecord1.getNotPrimaryAlignmentFlag();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(sAMRecord7);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test222() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test222");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        sAMRecord1.setMateAlignmentStart((int) (short) 100);
        int int9 = sAMRecord1.getAttributesBinarySize();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
    }

    @Test
    public void test223() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test223");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.ValidationStringency validationStringency14 = null;
        sAMRecord1.setValidationStringency(validationStringency14);
        htsjdk.samtools.SAMFileSource sAMFileSource16 = sAMRecord1.getFileSource();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileSource16);
    }

    @Test
    public void test224() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test224");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        boolean boolean13 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setFlags((int) (short) 10);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test225() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test225");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        boolean boolean14 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        sAMRecord16.setMappingQuality((-1));
        boolean boolean19 = sAMRecord16.getReadNegativeStrandFlag();
        int int20 = sAMRecord16.getLengthOnReference();
        sAMRecord16.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader23 = null;
        htsjdk.samtools.SAMRecord sAMRecord24 = new htsjdk.samtools.SAMRecord(sAMFileHeader23);
        sAMRecord24.setDuplicateReadFlag(false);
        java.lang.Object obj27 = null;
        boolean boolean28 = sAMRecord24.equals(obj27);
        boolean boolean29 = sAMRecord16.overlaps((htsjdk.samtools.util.Locatable) sAMRecord24);
        sAMRecord16.setMappingQuality((-1));
        int int32 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord16);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
        org.junit.Assert.assertTrue("'" + int20 + "' != '" + 0 + "'", int20 == 0);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + false + "'", boolean28 == false);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + true + "'", boolean29 == true);
        org.junit.Assert.assertTrue("'" + int32 + "' != '" + 4680 + "'", int32 == 4680);
    }

    @Test
    public void test226() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test226");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader13 = null;
        htsjdk.samtools.SAMRecord sAMRecord14 = new htsjdk.samtools.SAMRecord(sAMFileHeader13);
        sAMRecord14.setDuplicateReadFlag(false);
        java.lang.Object obj17 = null;
        boolean boolean18 = sAMRecord14.equals(obj17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        sAMRecord20.setDuplicateReadFlag(false);
        sAMRecord20.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj25 = sAMRecord14.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord26 = sAMRecord14.deepCopy();
        boolean boolean27 = sAMRecord1.equals((java.lang.Object) sAMRecord26);
        htsjdk.samtools.SAMFileHeader sAMFileHeader28 = null;
        htsjdk.samtools.SAMRecord sAMRecord29 = new htsjdk.samtools.SAMRecord(sAMFileHeader28);
        sAMRecord29.setReadUnmappedFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader32 = sAMRecord29.getHeader();
        boolean boolean33 = sAMRecord26.overlaps((htsjdk.samtools.util.Locatable) sAMRecord29);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNull(obj25);
        org.junit.Assert.assertNotNull(sAMRecord26);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNull(sAMFileHeader32);
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
    }

    @Test
    public void test227() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test227");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        sAMRecord8.setMappingQuality((int) (short) 100);
        sAMRecord8.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        int int22 = sAMRecord20.getReferencePositionAtReadPosition((int) (byte) -1);
        int int24 = sAMRecord20.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar25 = sAMRecord20.getCigar();
        int int28 = sAMRecord20.getReadPositionAtReferencePosition((int) ' ', false);
        int int29 = sAMRecord20.getAttributesBinarySize();
        htsjdk.samtools.ValidationStringency validationStringency30 = sAMRecord20.getValidationStringency();
        sAMRecord8.setValidationStringency(validationStringency30);
        sAMRecord1.setValidationStringency(validationStringency30);
        htsjdk.samtools.ValidationStringency validationStringency33 = sAMRecord1.getValidationStringency();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + 0 + "'", int22 == 0);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + 0 + "'", int24 == 0);
        org.junit.Assert.assertNotNull(cigar25);
        org.junit.Assert.assertTrue("'" + int28 + "' != '" + 0 + "'", int28 == 0);
        org.junit.Assert.assertTrue("'" + int29 + "' != '" + (-1) + "'", int29 == (-1));
        org.junit.Assert.assertTrue("'" + validationStringency30 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency30.equals(htsjdk.samtools.ValidationStringency.SILENT));
        org.junit.Assert.assertTrue("'" + validationStringency33 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency33.equals(htsjdk.samtools.ValidationStringency.SILENT));
    }

    @Test
    public void test228() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test228");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        int int11 = sAMRecord1.getReferencePositionAtReadPosition((int) (short) 0);
        int int12 = sAMRecord1.getEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
    }

    @Test
    public void test229() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test229");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        int int15 = sAMRecord1.getReadLength();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray17 = sAMRecord1.getSignedByteArrayAttribute("null\t0\t*\t1\t0\t*\thi!\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?1?0?*?hi!?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
    }

    @Test
    public void test230() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test230");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = null;
        htsjdk.samtools.SAMRecord sAMRecord15 = new htsjdk.samtools.SAMRecord(sAMFileHeader14);
        sAMRecord15.setDuplicateReadFlag(false);
        sAMRecord15.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj20 = sAMRecord9.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord21 = sAMRecord9.deepCopy();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        sAMRecord23.setDuplicateReadFlag(false);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMRecord23.equals(obj26);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList29 = sAMRecord23.isValid(false);
        sAMRecord23.setMateReferenceName("hi!");
        sAMRecord23.setAlignmentStart((int) (short) 1);
        int int34 = sAMRecord23.getStart();
        java.lang.Object obj35 = sAMRecord1.setTransientAttribute((java.lang.Object) sAMRecord21, (java.lang.Object) int34);
        sAMRecord1.setReadUnmappedFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray39 = sAMRecord1.getUnsignedByteArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
    }

    @Test
    public void test231() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test231");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getMappingQuality();
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
    }

    @Test
    public void test232() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test232");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.ValidationStringency validationStringency14 = null;
        sAMRecord1.setValidationStringency(validationStringency14);
        // The following exception was thrown during execution in test generation
        try {
            int int16 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test233() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test233");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList25 = sAMRecord1.isValid(false);
        byte[] byteArray26 = sAMRecord1.getOriginalBaseQualities();
        sAMRecord1.reverseComplement(false);
        sAMRecord1.setSupplementaryAlignmentFlag(false);
        boolean boolean31 = sAMRecord1.getDuplicateReadFlag();
        int int32 = sAMRecord1.getFlags();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(sAMValidationErrorList25);
        org.junit.Assert.assertNull(byteArray26);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertTrue("'" + int32 + "' != '" + 0 + "'", int32 == 0);
    }

    @Test
    public void test234() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test234");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getUnclippedEnd();
        java.lang.String str8 = sAMRecord1.getPairedReadName();
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "null" + "'", str8, "null");
    }

    @Test
    public void test235() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test235");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList7 = sAMRecord1.getAlignmentBlocks();
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        boolean boolean9 = sAMRecord1.isSecondaryOrSupplementary();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setBaseQualityString("null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Invalid fastq character: ?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(alignmentBlockList7);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test236() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test236");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMRecord13.equals(obj16);
        htsjdk.samtools.SAMFileHeader sAMFileHeader18 = null;
        htsjdk.samtools.SAMRecord sAMRecord19 = new htsjdk.samtools.SAMRecord(sAMFileHeader18);
        sAMRecord19.setDuplicateReadFlag(false);
        sAMRecord19.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj24 = sAMRecord13.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency25 = null;
        sAMRecord13.setValidationStringency(validationStringency25);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord27 = sAMRecord13.getReadGroup();
        sAMRecord13.setFlags(536870912);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord13.getAlignmentBlocks();
        htsjdk.samtools.SAMFileHeader sAMFileHeader32 = null;
        htsjdk.samtools.SAMRecord sAMRecord33 = new htsjdk.samtools.SAMRecord(sAMFileHeader32);
        sAMRecord33.setDuplicateReadFlag(false);
        java.lang.Object obj36 = null;
        boolean boolean37 = sAMRecord33.equals(obj36);
        htsjdk.samtools.SAMFileHeader sAMFileHeader38 = null;
        htsjdk.samtools.SAMRecord sAMRecord39 = new htsjdk.samtools.SAMRecord(sAMFileHeader38);
        sAMRecord39.setDuplicateReadFlag(false);
        sAMRecord39.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj44 = sAMRecord33.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency45 = null;
        sAMRecord33.setValidationStringency(validationStringency45);
        boolean boolean47 = sAMRecord33.isSecondaryAlignment();
        java.lang.String str48 = sAMRecord33.getCigarString();
        java.lang.Object obj50 = sAMRecord33.getAttribute((short) 0);
        java.lang.Object obj51 = sAMRecord13.removeTransientAttribute((java.lang.Object) sAMRecord33);
        java.lang.String str52 = sAMRecord33.format();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + false + "'", boolean37 == false);
        org.junit.Assert.assertNull(obj44);
        org.junit.Assert.assertTrue("'" + boolean47 + "' != '" + false + "'", boolean47 == false);
        org.junit.Assert.assertEquals("'" + str48 + "' != '" + "*" + "'", str48, "*");
        org.junit.Assert.assertNull(obj50);
        org.junit.Assert.assertNull(obj51);
        org.junit.Assert.assertEquals("'" + str52 + "' != '" + "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*" + "'", str52, "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
    }

    @Test
    public void test237() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test237");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        int int15 = sAMRecord13.getReferencePositionAtReadPosition((int) (byte) -1);
        int int17 = sAMRecord13.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar18 = sAMRecord13.getCigar();
        int int21 = sAMRecord13.getReadPositionAtReferencePosition((int) ' ', false);
        int int22 = sAMRecord13.getAttributesBinarySize();
        htsjdk.samtools.ValidationStringency validationStringency23 = sAMRecord13.getValidationStringency();
        sAMRecord1.setValidationStringency(validationStringency23);
        java.lang.String str25 = sAMRecord1.format();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + 0 + "'", int17 == 0);
        org.junit.Assert.assertNotNull(cigar18);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + validationStringency23 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency23.equals(htsjdk.samtools.ValidationStringency.SILENT));
        org.junit.Assert.assertEquals("'" + str25 + "' != '" + "null\t256\t\t*\t100\t*\t*\t*\t*\t*\t*" + "'", str25, "null\t256\t\t*\t100\t*\t*\t*\t*\t*\t*");
    }

    @Test
    public void test238() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test238");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.lang.Object obj25 = sAMRecord18.getAttribute((short) 10);
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray27 = sAMRecord18.getUnsignedIntArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNull(obj25);
    }

    @Test
    public void test239() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test239");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader16 = null;
        htsjdk.samtools.SAMRecord sAMRecord17 = new htsjdk.samtools.SAMRecord(sAMFileHeader16);
        int int19 = sAMRecord17.getReferencePositionAtReadPosition((int) (byte) -1);
        int int21 = sAMRecord17.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar22 = sAMRecord17.getCigar();
        int int25 = sAMRecord17.getReadPositionAtReferencePosition((int) ' ', false);
        int int26 = sAMRecord17.getAttributesBinarySize();
        boolean boolean28 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord17, (int) (short) 0);
        int int29 = sAMRecord1.getUnclippedStart();
        int int30 = sAMRecord1.getReadLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 0 + "'", int21 == 0);
        org.junit.Assert.assertNotNull(cigar22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + int29 + "' != '" + 0 + "'", int29 == 0);
        org.junit.Assert.assertTrue("'" + int30 + "' != '" + 0 + "'", int30 == 0);
    }

    @Test
    public void test240() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test240");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        sAMRecord1.setAlignmentStart((-1));
        sAMRecord1.setNotPrimaryAlignmentFlag(false);
        sAMRecord1.setFirstOfPairFlag(false);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test241() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test241");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        java.lang.String str14 = sAMRecord1.getCigarString();
        sAMRecord1.setFirstOfPairFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
    }

    @Test
    public void test242() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test242");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        sAMRecord1.reverseComplement(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
    }

    @Test
    public void test243() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test243");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setBaseQualityString("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Invalid fastq character:  ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
    }

    @Test
    public void test244() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test244");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        boolean boolean8 = sAMRecord1.getDuplicateReadFlag();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test245() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test245");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList15 = sAMRecord1.getAttributes();
        int int16 = sAMRecord1.getCigarLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
    }

    @Test
    public void test246() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test246");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setMappingQuality((-1));
        boolean boolean11 = sAMRecord8.getReadNegativeStrandFlag();
        int int12 = sAMRecord8.getLengthOnReference();
        sAMRecord8.setSecondaryAlignment(true);
        sAMRecord8.setMappingQuality((int) (short) 100);
        sAMRecord8.setReferenceName("");
        sAMRecord8.setReadUnmappedFlag(true);
        java.lang.Object obj21 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet22 = sAMRecord1.getSAMFlags();
        sAMRecord1.setReadUmappedFlag(true);
        int int25 = sAMRecord1.getAlignmentStart();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
        org.junit.Assert.assertNotNull(sAMFlagSet22);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 0 + "'", int25 == 0);
    }

    @Test
    public void test247() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test247");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        sAMRecord1.setReadPairedFlag(true);
        java.lang.String str9 = sAMRecord1.getReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader10 = null;
        htsjdk.samtools.SAMRecord sAMRecord11 = new htsjdk.samtools.SAMRecord(sAMFileHeader10);
        sAMRecord11.setDuplicateReadFlag(false);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMRecord11.equals(obj14);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList17 = sAMRecord11.isValid(false);
        sAMRecord11.setMateReferenceName("hi!");
        sAMRecord11.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet22 = sAMRecord11.getSAMFlags();
        boolean boolean23 = sAMRecord11.getDuplicateReadFlag();
        int int24 = sAMRecord11.getUnclippedEnd();
        java.lang.Object obj25 = sAMRecord1.getTransientAttribute((java.lang.Object) int24);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str9);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList17);
        org.junit.Assert.assertNotNull(sAMFlagSet22);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertNull(obj25);
    }

    @Test
    public void test248() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test248");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        sAMRecord1.setHeader(sAMFileHeader6);
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList9 = sAMRecord1.isValid();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList9);
    }

    @Test
    public void test249() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test249");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray8 = sAMRecord1.getUnsignedByteArrayAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
    }

    @Test
    public void test250() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test250");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        int int6 = sAMRecord1.getInferredInsertSize();
        sAMRecord1.setMappingQuality((int) (short) 1);
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test251() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test251");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        sAMRecord1.setReadUnmappedFlag(true);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList11 = sAMRecord1.getAlignmentBlocks();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(alignmentBlockList11);
    }

    @Test
    public void test252() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test252");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        sAMRecord1.setMateAlignmentStart((int) (byte) 0);
        int int13 = sAMRecord1.getInferredInsertSize();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 0 + "'", int13 == 0);
    }

    @Test
    public void test253() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test253");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        sAMRecord1.setReadPairedFlag(true);
        java.lang.String str9 = sAMRecord1.getReadName();
        sAMRecord1.reverseComplement(true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str9);
    }

    @Test
    public void test254() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test254");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setDuplicateReadFlag(false);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMRecord8.equals(obj11);
        htsjdk.samtools.SAMFileHeader sAMFileHeader13 = null;
        htsjdk.samtools.SAMRecord sAMRecord14 = new htsjdk.samtools.SAMRecord(sAMFileHeader13);
        sAMRecord14.setDuplicateReadFlag(false);
        sAMRecord14.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj19 = sAMRecord8.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord20 = sAMRecord8.deepCopy();
        java.lang.String str21 = sAMRecord8.getReferenceName();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList23 = sAMRecord8.validateCigar((long) (byte) 100);
        boolean boolean24 = sAMRecord1.equals((java.lang.Object) (byte) 100);
        htsjdk.samtools.SAMFileHeader sAMFileHeader25 = null;
        htsjdk.samtools.SAMRecord sAMRecord26 = new htsjdk.samtools.SAMRecord(sAMFileHeader25);
        sAMRecord26.setDuplicateReadFlag(false);
        java.lang.Object obj29 = null;
        boolean boolean30 = sAMRecord26.equals(obj29);
        htsjdk.samtools.SAMFileHeader sAMFileHeader31 = null;
        htsjdk.samtools.SAMRecord sAMRecord32 = new htsjdk.samtools.SAMRecord(sAMFileHeader31);
        sAMRecord32.setDuplicateReadFlag(false);
        sAMRecord32.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj37 = sAMRecord26.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord38 = sAMRecord26.deepCopy();
        sAMRecord38.setReadName("");
        byte[] byteArray41 = htsjdk.samtools.SAMRecord.NULL_SEQUENCE;
        sAMRecord38.setOriginalBaseQualities(byteArray41);
        sAMRecord1.setBaseQualities(byteArray41);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNull(obj19);
        org.junit.Assert.assertNotNull(sAMRecord20);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "*" + "'", str21, "*");
        org.junit.Assert.assertNull(sAMValidationErrorList23);
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNull(obj37);
        org.junit.Assert.assertNotNull(sAMRecord38);
        org.junit.Assert.assertNotNull(byteArray41);
        org.junit.Assert.assertArrayEquals(byteArray41, new byte[] {});
    }

    @Test
    public void test255() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test255");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet11 = sAMRecord1.getSAMFlags();
        java.lang.String str12 = sAMRecord1.getReadName();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertNotNull(sAMFlagSet11);
        org.junit.Assert.assertNull(str12);
    }

    @Test
    public void test256() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test256");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList15 = sAMRecord1.isValid(false);
        java.lang.String str16 = sAMRecord1.format();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNotNull(sAMValidationErrorList15);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*" + "'", str16, "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
    }

    @Test
    public void test257() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test257");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        int int7 = sAMRecord1.getUnclippedStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setMappingQuality((-1));
        boolean boolean12 = sAMRecord9.getReadNegativeStrandFlag();
        int int13 = sAMRecord9.getLengthOnReference();
        htsjdk.samtools.Cigar cigar14 = sAMRecord9.getCigar();
        int int16 = sAMRecord9.getReadPositionAtReferencePosition(0);
        boolean boolean17 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 0 + "'", int13 == 0);
        org.junit.Assert.assertNotNull(cigar14);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
    }

    @Test
    public void test258() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test258");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList15 = sAMRecord1.isValid(false);
        int int16 = sAMRecord1.getAttributesBinarySize();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNotNull(sAMValidationErrorList15);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + (-1) + "'", int16 == (-1));
    }

    @Test
    public void test259() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test259");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex(0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
    }

    @Test
    public void test260() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test260");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList13 = sAMRecord9.validateCigar((long) (byte) 100);
        int int14 = sAMRecord9.getUnclippedStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        sAMRecord16.setMappingQuality((-1));
        boolean boolean19 = sAMRecord16.getReadNegativeStrandFlag();
        int int20 = sAMRecord16.getLengthOnReference();
        sAMRecord16.setSecondaryAlignment(true);
        boolean boolean23 = sAMRecord16.getReadPairedFlag();
        java.lang.Object obj25 = sAMRecord9.setTransientAttribute((java.lang.Object) sAMRecord16, (java.lang.Object) 100);
        boolean boolean26 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        boolean boolean27 = sAMRecord9.getReadPairedFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
        org.junit.Assert.assertTrue("'" + int20 + "' != '" + 0 + "'", int20 == 0);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertNull(obj25);
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + true + "'", boolean26 == true);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
    }

    @Test
    public void test261() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test261");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        htsjdk.samtools.Cigar cigar9 = null;
        sAMRecord1.setCigar(cigar9);
        java.lang.String str11 = sAMRecord1.getSAMString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        int int15 = sAMRecord13.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList17 = sAMRecord13.validateCigar((long) (byte) 100);
        int int18 = sAMRecord13.getUnclippedStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        sAMRecord20.setMappingQuality((-1));
        boolean boolean23 = sAMRecord20.getReadNegativeStrandFlag();
        int int24 = sAMRecord20.getLengthOnReference();
        sAMRecord20.setSecondaryAlignment(true);
        boolean boolean27 = sAMRecord20.getReadPairedFlag();
        java.lang.Object obj29 = sAMRecord13.setTransientAttribute((java.lang.Object) sAMRecord20, (java.lang.Object) 100);
        htsjdk.samtools.Cigar cigar30 = sAMRecord13.getCigar();
        sAMRecord1.setCigar(cigar30);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n" + "'", str11, "null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList17);
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + 0 + "'", int18 == 0);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + 0 + "'", int24 == 0);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNull(obj29);
        org.junit.Assert.assertNotNull(cigar30);
    }

    @Test
    public void test262() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test262");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        int int14 = sAMRecord1.getAlignmentEnd();
        sAMRecord1.setReferenceName("null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + (-1) + "'", int14 == (-1));
    }

    @Test
    public void test263() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test263");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = null;
        htsjdk.samtools.SAMRecord sAMRecord5 = new htsjdk.samtools.SAMRecord(sAMFileHeader4);
        sAMRecord5.setDuplicateReadFlag(false);
        java.lang.Object obj8 = null;
        boolean boolean9 = sAMRecord5.equals(obj8);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList11 = sAMRecord5.isValid(false);
        sAMRecord5.setMateReferenceName("hi!");
        sAMRecord5.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet16 = sAMRecord5.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        sAMRecord18.setProperPairFlag(true);
        boolean boolean22 = sAMRecord5.contains((htsjdk.samtools.util.Locatable) sAMRecord18);
        int int23 = sAMRecord1.computeIndexingBinIfAbsent(sAMRecord18);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList25 = sAMRecord1.isValid(false);
        byte[] byteArray26 = sAMRecord1.getOriginalBaseQualities();
        sAMRecord1.reverseComplement(false);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean29 = sAMRecord1.getSecondOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(sAMValidationErrorList25);
        org.junit.Assert.assertNull(byteArray26);
    }

    @Test
    public void test264() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test264");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        htsjdk.samtools.SAMRecord sAMRecord14 = sAMRecord1.deepCopy();
        int int15 = sAMRecord1.getStart();
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord16 = sAMRecord1.getReadGroup();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertNotNull(sAMRecord14);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertNull(sAMReadGroupRecord16);
    }

    @Test
    public void test265() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test265");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord11 = sAMRecord1.getReadGroup();
        java.lang.String str12 = sAMRecord1.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertNull(sAMReadGroupRecord11);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str12, "null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
    }

    @Test
    public void test266() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test266");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        htsjdk.samtools.SAMFileSource sAMFileSource9 = sAMRecord1.getFileSource();
        java.lang.String str10 = sAMRecord1.toString();
        boolean boolean11 = sAMRecord1.getNotPrimaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMFileSource9);
        org.junit.Assert.assertEquals("'" + str10 + "' != '" + "null 0b aligned to *:0--1." + "'", str10, "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
    }

    @Test
    public void test267() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test267");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int6 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + (-1) + "'", int6 == (-1));
    }

    @Test
    public void test268() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test268");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        java.lang.String str14 = sAMRecord9.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = sAMRecord16.getHeader();
        byte[] byteArray20 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord16.setBaseQualities(byteArray20);
        sAMRecord9.setBaseQualities(byteArray20);
        sAMRecord1.setBaseQualities(byteArray20);
        boolean boolean24 = sAMRecord1.getReadNegativeStrandFlag();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList26 = sAMRecord1.validateCigar((long) (byte) 10);
        htsjdk.samtools.SAMFileSource sAMFileSource27 = sAMRecord1.getFileSource();
        boolean boolean28 = sAMRecord1.getSupplementaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "null" + "'", str14, "null");
        org.junit.Assert.assertNull(sAMFileHeader17);
        org.junit.Assert.assertNotNull(byteArray20);
        org.junit.Assert.assertArrayEquals(byteArray20, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
        org.junit.Assert.assertNull(sAMValidationErrorList26);
        org.junit.Assert.assertNull(sAMFileSource27);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + false + "'", boolean28 == false);
    }
}

