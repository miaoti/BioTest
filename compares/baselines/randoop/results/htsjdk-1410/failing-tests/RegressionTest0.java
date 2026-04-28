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
    public void test005() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test005");
        int int0 = htsjdk.samtools.SAMRecord.NO_ALIGNMENT_START;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 0 + "'", int0 == 0);
    }

    @Test
    public void test006() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test006");
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
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
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
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 2147483647 + "'", int0 == 2147483647);
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
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList15 = sAMRecord1.isValid(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNotNull(sAMValidationErrorList15);
    }

    @Test
    public void test023() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test023");
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
    public void test024() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test024");
        long long0 = htsjdk.samtools.SAMRecord.serialVersionUID;
        org.junit.Assert.assertTrue("'" + long0 + "' != '" + 1L + "'", long0 == 1L);
    }

    @Test
    public void test025() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test025");
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
    public void test026() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test026");
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
    public void test027() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test027");
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
    public void test028() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test028");
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
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test029() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test029");
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
    public void test030() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test030");
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
    public void test031() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test031");
        java.lang.String str0 = htsjdk.samtools.SAMRecord.NO_ALIGNMENT_REFERENCE_NAME;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "*" + "'", str0, "*");
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
    public void test033() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test033");
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
    public void test034() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test034");
        byte[] byteArray0 = htsjdk.samtools.SAMRecord.NULL_SEQUENCE;
        org.junit.Assert.assertNotNull(byteArray0);
        org.junit.Assert.assertArrayEquals(byteArray0, new byte[] {});
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
    public void test036() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test036");
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
    public void test037() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test037");
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
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertNull(sAMValidationErrorList16);
    }

    @Test
    public void test038() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test038");
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
    public void test039() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test039");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        sAMRecord1.setReadUmappedFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test040() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test040");
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
    public void test041() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test041");
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
    public void test042() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test042");
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
    public void test043() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test043");
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
    public void test044() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test044");
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
    public void test045() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test045");
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
    public void test046() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test046");
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
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
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
    public void test048() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test048");
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
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList14);
        org.junit.Assert.assertNotNull(sAMFlagSet19);
        org.junit.Assert.assertNull(obj20);
    }

    @Test
    public void test049() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test049");
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
    public void test050() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test050");
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
    public void test051() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test051");
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
        java.lang.String str16 = sAMRecord1.getCigarString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "*" + "'", str16, "*");
    }

    @Test
    public void test052() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test052");
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
    public void test053() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test053");
        byte[] byteArray0 = htsjdk.samtools.SAMRecord.NULL_QUALS;
        org.junit.Assert.assertNotNull(byteArray0);
        org.junit.Assert.assertArrayEquals(byteArray0, new byte[] {});
    }

    @Test
    public void test054() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test054");
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
    public void test055() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test055");
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
    public void test056() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test056");
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
    public void test057() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test057");
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
    public void test058() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test058");
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
    public void test059() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test059");
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
    public void test060() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test060");
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
    public void test063() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test063");
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
    public void test064() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test064");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        sAMRecord1.setReadPairedFlag(true);
        boolean boolean9 = sAMRecord1.getNotPrimaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test065() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test065");
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
    public void test066() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test066");
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
    public void test067() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test067");
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
        sAMRecord13.setFlags(2147483647);
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
    public void test068() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test068");
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
    public void test069() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test069");
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
    public void test070() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test070");
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
    public void test071() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test071");
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
    public void test072() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test072");
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
    public void test073() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test073");
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
    public void test074() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test074");
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
    }

    @Test
    public void test076() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test076");
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
        sAMRecord1.setFlags(2147483647);
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
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
    }

    @Test
    public void test077() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test077");
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
    public void test078() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test078");
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
    public void test079() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test079");
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
    public void test080() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test080");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        sAMRecord1.reverseComplement();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
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
    public void test082() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test082");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        java.lang.String str7 = sAMRecord1.getContig();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "*" + "'", str7, "*");
    }

    @Test
    public void test083() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test083");
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
    public void test084() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test084");
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
    public void test085() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test085");
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
    public void test086() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test086");
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
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "null" + "'", str14, "null");
        org.junit.Assert.assertNull(sAMFileHeader17);
        org.junit.Assert.assertNotNull(byteArray20);
        org.junit.Assert.assertArrayEquals(byteArray20, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
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
    public void test088() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test088");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Character char14 = sAMRecord1.getCharacterAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test089() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test089");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        int int7 = sAMRecord1.getMappingQuality();
        sAMRecord1.setReadName("*");
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setAttribute("", (java.lang.Object) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
    }

    @Test
    public void test090() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test090");
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
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean36 = sAMRecord21.getProperPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
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
    }

    @Test
    public void test091() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test091");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int7 = sAMRecord1.getStart();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
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
        boolean boolean6 = sAMRecord1.isSecondaryOrSupplementary();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test093() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test093");
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
        int int32 = sAMRecord30.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord30.setSecondaryAlignment(true);
        boolean boolean36 = sAMRecord17.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord30, (int) (short) -1);
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
        org.junit.Assert.assertTrue("'" + int32 + "' != '" + 0 + "'", int32 == 0);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + false + "'", boolean36 == false);
    }

    @Test
    public void test094() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test094");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        boolean boolean10 = sAMRecord1.getSupplementaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test095() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test095");
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
            java.lang.String str17 = sAMRecord1.getStringAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
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
    public void test096() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test096");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        htsjdk.samtools.SAMFileSource sAMFileSource9 = sAMRecord1.getFileSource();
        java.lang.String str10 = sAMRecord1.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMFileSource9);
        org.junit.Assert.assertEquals("'" + str10 + "' != '" + "null 0b aligned to *:0--1." + "'", str10, "null 0b aligned to *:0--1.");
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
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        boolean boolean13 = sAMRecord1.getReadNegativeStrandFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test098() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test098");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Object obj11 = sAMRecord1.getAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test099() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test099");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        java.lang.Class<?> wildcardClass11 = sAMRecord1.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertNotNull(wildcardClass11);
    }

    @Test
    public void test100() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test100");
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
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Character char18 = sAMRecord1.getCharacterAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
    }

    @Test
    public void test101() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test101");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        byte[] byteArray10 = sAMRecord1.getOriginalBaseQualities();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(byteArray10);
    }

    @Test
    public void test102() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test102");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getUnclippedEnd();
        // The following exception was thrown during execution in test generation
        try {
            int int8 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test103() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test103");
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
        int int37 = sAMRecord21.getCigarLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
        org.junit.Assert.assertTrue("'" + int37 + "' != '" + 0 + "'", int37 == 0);
    }

    @Test
    public void test104() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test104");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList6 = sAMRecord1.isValid();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertNotNull(sAMValidationErrorList6);
    }

    @Test
    public void test105() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test105");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        // The following exception was thrown during execution in test generation
        try {
            short[] shortArray8 = sAMRecord1.getSignedShortArrayAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
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
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        htsjdk.samtools.SAMFileSource sAMFileSource9 = sAMRecord1.getFileSource();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean10 = sAMRecord1.getSecondOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNull(sAMFileSource9);
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        byte[] byteArray15 = sAMRecord1.getReadBases();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertNotNull(byteArray15);
        org.junit.Assert.assertArrayEquals(byteArray15, new byte[] {});
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
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray9 = sAMRecord1.getUnsignedIntArrayAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test109() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test109");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setAlignmentStart((int) (short) 100);
        java.lang.String str12 = sAMRecord1.getReferenceName();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "*" + "'", str12, "*");
    }

    @Test
    public void test110() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test110");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        htsjdk.samtools.SAMRecord sAMRecord8 = new htsjdk.samtools.SAMRecord(sAMFileHeader7);
        sAMRecord8.setDuplicateReadFlag(false);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMRecord8.equals(obj11);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList14 = sAMRecord8.isValid(false);
        sAMRecord8.setMateReferenceName("hi!");
        sAMRecord8.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet19 = sAMRecord8.getSAMFlags();
        java.lang.String str20 = sAMRecord8.getBaseQualityString();
        byte[] byteArray21 = sAMRecord8.getReadBases();
        sAMRecord1.setOriginalBaseQualities(byteArray21);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList14);
        org.junit.Assert.assertNotNull(sAMFlagSet19);
        org.junit.Assert.assertEquals("'" + str20 + "' != '" + "*" + "'", str20, "*");
        org.junit.Assert.assertNotNull(byteArray21);
        org.junit.Assert.assertArrayEquals(byteArray21, new byte[] {});
    }

    @Test
    public void test111() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test111");
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
        java.lang.Object obj37 = sAMRecord1.clone();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
        org.junit.Assert.assertNotNull(obj37);
        org.junit.Assert.assertEquals(obj37.toString(), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.lang.String.valueOf(obj37), "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals(java.util.Objects.toString(obj37), "null 0b aligned to *:0--1.");
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
        byte[] byteArray8 = sAMRecord1.getReadBases();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*", (java.lang.Object) (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(byteArray8);
        org.junit.Assert.assertArrayEquals(byteArray8, new byte[] {});
    }

    @Test
    public void test113() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test113");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord10 = sAMRecord1.getReadGroup();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertNull(sAMReadGroupRecord10);
    }

    @Test
    public void test114() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test114");
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
        sAMRecord21.setMateReferenceIndex((int) (short) -1);
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
    public void test115() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test115");
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
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord24 = sAMRecord1.getReadGroup();
        sAMRecord1.setMateUnmappedFlag(false);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
        org.junit.Assert.assertNull(sAMReadGroupRecord24);
    }

    @Test
    public void test116() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test116");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        sAMRecord1.setInferredInsertSize((int) (short) 1);
        org.junit.Assert.assertNull(obj5);
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord15 = sAMRecord1.getReadGroup();
        sAMRecord1.setFlags(2147483647);
        java.lang.String str18 = sAMRecord1.getBaseQualityString();
        int int19 = sAMRecord1.getAlignmentStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "*" + "'", str18, "*");
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
    }

    @Test
    public void test118() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test118");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        int int6 = sAMRecord1.getInferredInsertSize();
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader7);
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test119() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test119");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader15);
        sAMRecord1.setReadNegativeStrandFlag(false);
        sAMRecord1.clearAttributes();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
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
        java.lang.Object obj7 = sAMRecord1.getAttribute((short) 100);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Float float9 = sAMRecord1.getFloatAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(obj7);
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord13 = sAMRecord1.deepCopy();
        java.lang.String str14 = sAMRecord1.getReferenceName();
        java.lang.String str15 = sAMRecord1.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str15, "null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
    }

    @Test
    public void test122() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test122");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet10 = sAMRecord1.getSAMFlags();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(sAMFlagSet10);
    }

    @Test
    public void test123() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test123");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setReadNegativeStrandFlag(false);
        boolean boolean12 = sAMRecord1.isSecondaryOrSupplementary();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test124() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test124");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        java.lang.Long long3 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 10);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean4 = sAMRecord1.getSecondOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(long3);
    }

    @Test
    public void test125() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test125");
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
        sAMRecord1.setMateNegativeStrandFlag(false);
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
    public void test126() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test126");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        sAMRecord1.setMateAlignmentStart((int) (byte) 0);
        sAMRecord1.setReadUmappedFlag(true);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
    }

    @Test
    public void test127() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test127");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        byte[] byteArray8 = sAMRecord1.getReadBases();
        boolean boolean9 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(byteArray8);
        org.junit.Assert.assertArrayEquals(byteArray8, new byte[] {});
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test128() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test128");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList11 = sAMRecord1.getAlignmentBlocks();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean12 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertNotNull(alignmentBlockList11);
    }

    @Test
    public void test129() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test129");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        int int4 = sAMRecord1.getStart();
        java.lang.Object obj6 = sAMRecord1.getAttribute((short) (byte) 100);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 0 + "'", int4 == 0);
        org.junit.Assert.assertNull(obj6);
    }

    @Test
    public void test130() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test130");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader24 = null;
        htsjdk.samtools.SAMRecord sAMRecord25 = new htsjdk.samtools.SAMRecord(sAMFileHeader24);
        htsjdk.samtools.SAMFileHeader sAMFileHeader26 = sAMRecord25.getHeader();
        byte[] byteArray29 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord25.setBaseQualities(byteArray29);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList31 = sAMRecord25.getAlignmentBlocks();
        htsjdk.samtools.SAMFileHeader sAMFileHeader32 = null;
        htsjdk.samtools.SAMRecord sAMRecord33 = new htsjdk.samtools.SAMRecord(sAMFileHeader32);
        htsjdk.samtools.SAMFileHeader sAMFileHeader34 = sAMRecord33.getHeader();
        byte[] byteArray37 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord33.setBaseQualities(byteArray37);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList39 = sAMRecord33.getAlignmentBlocks();
        boolean boolean40 = sAMRecord33.getReadPairedFlag();
        java.lang.Object obj41 = sAMRecord18.setTransientAttribute((java.lang.Object) sAMRecord25, (java.lang.Object) boolean40);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNull(sAMFileHeader26);
        org.junit.Assert.assertNotNull(byteArray29);
        org.junit.Assert.assertArrayEquals(byteArray29, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(alignmentBlockList31);
        org.junit.Assert.assertNull(sAMFileHeader34);
        org.junit.Assert.assertNotNull(byteArray37);
        org.junit.Assert.assertArrayEquals(byteArray37, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(alignmentBlockList39);
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + false + "'", boolean40 == false);
        org.junit.Assert.assertNull(obj41);
    }

    @Test
    public void test131() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test131");
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
            sAMRecord1.setMateReferenceIndex((int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
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
    public void test132() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test132");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray9 = sAMRecord1.getSignedIntArrayAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
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
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Float float10 = sAMRecord1.getFloatAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        sAMRecord7.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj12 = sAMRecord1.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.ValidationStringency validationStringency13 = null;
        sAMRecord1.setValidationStringency(validationStringency13);
        boolean boolean15 = sAMRecord1.isSecondaryAlignment();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean16 = sAMRecord1.getMateNegativeStrandFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test135() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test135");
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
        sAMRecord1.setReadPairedFlag(false);
        java.util.List<java.lang.String> strList26 = htsjdk.samtools.SAMRecord.TAGS_TO_REVERSE_COMPLEMENT;
        java.util.Collection<java.lang.String> strCollection27 = null;
        sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList26, strCollection27, true);
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(strList26);
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        java.lang.String str15 = sAMRecord1.getCigarString();
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray17 = sAMRecord1.getFloatArrayAttribute("null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?0?-1?*?*?0?0?*?*?");
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
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        java.lang.String str16 = sAMRecord1.getSAMString();
        sAMRecord1.setSupplementaryAlignmentFlag(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = null;
        htsjdk.samtools.SAMRecord sAMRecord20 = new htsjdk.samtools.SAMRecord(sAMFileHeader19);
        sAMRecord20.setReadUnmappedFlag(true);
        java.lang.Object obj24 = sAMRecord20.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar25 = sAMRecord20.getCigar();
        sAMRecord1.setCigar(cigar25);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n" + "'", str16, "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNotNull(cigar25);
    }

    @Test
    public void test138() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test138");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        sAMRecord1.setHeader(sAMFileHeader6);
        sAMRecord1.setReadUmappedFlag(true);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
    }

    @Test
    public void test139() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test139");
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
        int int17 = sAMRecord1.getReadPositionAtReferencePosition((int) '#', true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertNotNull(byteArray14);
        org.junit.Assert.assertArrayEquals(byteArray14, new byte[] {});
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + 0 + "'", int17 == 0);
    }

    @Test
    public void test140() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test140");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSupplementaryAlignmentFlag(true);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        sAMRecord1.reverseComplement(false);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
    }

    @Test
    public void test141() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test141");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        java.lang.String str7 = sAMRecord1.getSAMString();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean8 = sAMRecord1.getMateNegativeStrandFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "null\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str7, "null\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        java.lang.String str14 = sAMRecord1.getBaseQualityString();
        java.lang.String str15 = sAMRecord1.getCigarString();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean17 = sAMRecord1.isUnsignedArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
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
    public void test143() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test143");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = sAMRecord1.getHeader();
        sAMRecord1.setCigarString("*");
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = sAMRecord1.getHeader();
        org.junit.Assert.assertNull(sAMFileHeader4);
        org.junit.Assert.assertNull(sAMFileHeader7);
    }

    @Test
    public void test144() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test144");
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
        java.lang.String str19 = sAMRecord14.getReadString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertNull(sAMFileHeader15);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "*" + "'", str19, "*");
    }

    @Test
    public void test145() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test145");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        int int7 = sAMRecord1.getStart();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean8 = sAMRecord1.getProperPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
    }

    @Test
    public void test146() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test146");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        java.lang.Class<?> wildcardClass4 = sAMRecord1.getClass();
        org.junit.Assert.assertNotNull(wildcardClass4);
    }

    @Test
    public void test147() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test147");
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
        boolean boolean16 = sAMRecord1.getReadNegativeStrandFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
    }

    @Test
    public void test148() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test148");
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
        int int16 = sAMRecord1.getInferredInsertSize();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
    }

    @Test
    public void test149() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test149");
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
        sAMRecord1.setFirstOfPairFlag(true);
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
    }

    @Test
    public void test150() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test150");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = sAMRecord1.getHeader();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNull(sAMFileHeader15);
    }

    @Test
    public void test151() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test151");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList7 = sAMRecord1.getAlignmentBlocks();
        java.lang.String str8 = sAMRecord1.getPairedReadName();
        byte[] byteArray9 = sAMRecord1.getBaseQualities();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(alignmentBlockList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "null" + "'", str8, "null");
        org.junit.Assert.assertNotNull(byteArray9);
        org.junit.Assert.assertArrayEquals(byteArray9, new byte[] { (byte) 0, (byte) 0 });
    }

    @Test
    public void test152() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test152");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int6 = sAMRecord1.getUnclippedStart();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList8 = sAMRecord1.validateCigar((long) (short) -1);
        // The following exception was thrown during execution in test generation
        try {
            int int9 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList8);
    }

    @Test
    public void test153() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test153");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = sAMRecord1.getHeader();
        sAMRecord1.setMateAlignmentStart((int) (short) 1);
        org.junit.Assert.assertNull(sAMFileHeader4);
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
        java.lang.String str6 = sAMRecord1.getPairedReadName();
        int int7 = sAMRecord1.getUnclippedStart();
        int int8 = sAMRecord1.getLengthOnReference();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 0 + "'", int8 == 0);
    }

    @Test
    public void test155() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test155");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        byte[] byteArray5 = sAMRecord1.getBaseQualities();
        java.lang.Object obj6 = sAMRecord1.clone();
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray8 = sAMRecord1.getUnsignedIntArrayAttribute("null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?*?*?0?0?*?*?");
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
    public void test156() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test156");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        java.lang.Object obj7 = sAMRecord1.getAttribute((short) 100);
        int int8 = sAMRecord1.getUnclippedStart();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(obj7);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 0 + "'", int8 == 0);
    }

    @Test
    public void test157() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test157");
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
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean36 = sAMRecord21.getMateNegativeStrandFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
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
        sAMRecord13.setFlags(2147483647);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean31 = sAMRecord1.getMateUnmappedFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
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
    public void test159() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test159");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        int int11 = sAMRecord1.getAlignmentStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
    }

    @Test
    public void test160() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test160");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setAlignmentStart((int) (short) 1);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean12 = sAMRecord1.getFirstOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
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
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader13 = null;
        htsjdk.samtools.SAMRecord sAMRecord14 = new htsjdk.samtools.SAMRecord(sAMFileHeader13);
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = sAMRecord14.getHeader();
        sAMRecord14.setProperPairFlag(true);
        boolean boolean18 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord14);
        int int19 = sAMRecord14.getUnclippedStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertNull(sAMFileHeader15);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 0 + "'", int19 == 0);
    }

    @Test
    public void test162() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test162");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader37 = null;
        htsjdk.samtools.SAMRecord sAMRecord38 = new htsjdk.samtools.SAMRecord(sAMFileHeader37);
        sAMRecord38.setMappingQuality((-1));
        boolean boolean41 = sAMRecord38.getReadNegativeStrandFlag();
        int int42 = sAMRecord38.getLengthOnReference();
        sAMRecord38.setSecondaryAlignment(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader45 = null;
        htsjdk.samtools.SAMRecord sAMRecord46 = new htsjdk.samtools.SAMRecord(sAMFileHeader45);
        sAMRecord46.setDuplicateReadFlag(false);
        java.lang.Object obj49 = null;
        boolean boolean50 = sAMRecord46.equals(obj49);
        boolean boolean51 = sAMRecord38.overlaps((htsjdk.samtools.util.Locatable) sAMRecord46);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList52 = sAMRecord38.getAttributes();
        htsjdk.samtools.SAMFileHeader sAMFileHeader53 = null;
        htsjdk.samtools.SAMRecord sAMRecord54 = new htsjdk.samtools.SAMRecord(sAMFileHeader53);
        int int56 = sAMRecord54.getReferencePositionAtReadPosition((int) (byte) -1);
        int int58 = sAMRecord54.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar59 = sAMRecord54.getCigar();
        int int62 = sAMRecord54.getReadPositionAtReferencePosition((int) ' ', false);
        int int63 = sAMRecord54.getAttributesBinarySize();
        boolean boolean65 = sAMRecord38.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord54, (int) (short) 0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader66 = null;
        htsjdk.samtools.SAMRecord sAMRecord67 = new htsjdk.samtools.SAMRecord(sAMFileHeader66);
        sAMRecord67.setDuplicateReadFlag(false);
        java.lang.Object obj70 = null;
        boolean boolean71 = sAMRecord67.equals(obj70);
        htsjdk.samtools.SAMFileHeader sAMFileHeader72 = null;
        htsjdk.samtools.SAMRecord sAMRecord73 = new htsjdk.samtools.SAMRecord(sAMFileHeader72);
        sAMRecord73.setDuplicateReadFlag(false);
        sAMRecord73.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj78 = sAMRecord67.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord79 = sAMRecord67.deepCopy();
        int int80 = sAMRecord79.getAlignmentStart();
        byte[] byteArray81 = sAMRecord79.getBaseQualities();
        sAMRecord54.setReadBases(byteArray81);
        sAMRecord54.setReadNegativeStrandFlag(true);
        java.lang.String str85 = sAMRecord54.getSAMString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader86 = null;
        htsjdk.samtools.SAMRecord sAMRecord87 = new htsjdk.samtools.SAMRecord(sAMFileHeader86);
        int int89 = sAMRecord87.getReferencePositionAtReadPosition((int) (byte) -1);
        int int91 = sAMRecord87.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar92 = sAMRecord87.getCigar();
        int int95 = sAMRecord87.getReadPositionAtReferencePosition((int) ' ', false);
        int int96 = sAMRecord87.getAttributesBinarySize();
        htsjdk.samtools.ValidationStringency validationStringency97 = sAMRecord87.getValidationStringency();
        sAMRecord54.setValidationStringency(validationStringency97);
        sAMRecord21.setValidationStringency(validationStringency97);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + false + "'", boolean41 == false);
        org.junit.Assert.assertTrue("'" + int42 + "' != '" + 0 + "'", int42 == 0);
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + false + "'", boolean50 == false);
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + true + "'", boolean51 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList52);
        org.junit.Assert.assertTrue("'" + int56 + "' != '" + 0 + "'", int56 == 0);
        org.junit.Assert.assertTrue("'" + int58 + "' != '" + 0 + "'", int58 == 0);
        org.junit.Assert.assertNotNull(cigar59);
        org.junit.Assert.assertTrue("'" + int62 + "' != '" + 0 + "'", int62 == 0);
        org.junit.Assert.assertTrue("'" + int63 + "' != '" + (-1) + "'", int63 == (-1));
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertTrue("'" + boolean71 + "' != '" + false + "'", boolean71 == false);
        org.junit.Assert.assertNull(obj78);
        org.junit.Assert.assertNotNull(sAMRecord79);
        org.junit.Assert.assertTrue("'" + int80 + "' != '" + 0 + "'", int80 == 0);
        org.junit.Assert.assertNotNull(byteArray81);
        org.junit.Assert.assertArrayEquals(byteArray81, new byte[] {});
        org.junit.Assert.assertEquals("'" + str85 + "' != '" + "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str85, "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + int89 + "' != '" + 0 + "'", int89 == 0);
        org.junit.Assert.assertTrue("'" + int91 + "' != '" + 0 + "'", int91 == 0);
        org.junit.Assert.assertNotNull(cigar92);
        org.junit.Assert.assertTrue("'" + int95 + "' != '" + 0 + "'", int95 == 0);
        org.junit.Assert.assertTrue("'" + int96 + "' != '" + (-1) + "'", int96 == (-1));
        org.junit.Assert.assertTrue("'" + validationStringency97 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency97.equals(htsjdk.samtools.ValidationStringency.SILENT));
    }

    @Test
    public void test163() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test163");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        htsjdk.samtools.ValidationStringency validationStringency11 = sAMRecord1.getValidationStringency();
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList12 = sAMRecord1.getAlignmentBlocks();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + validationStringency11 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency11.equals(htsjdk.samtools.ValidationStringency.SILENT));
        org.junit.Assert.assertNotNull(alignmentBlockList12);
    }

    @Test
    public void test164() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test164");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        htsjdk.samtools.SAMFileHeader sAMFileHeader10 = null;
        htsjdk.samtools.SAMRecord sAMRecord11 = new htsjdk.samtools.SAMRecord(sAMFileHeader10);
        sAMRecord11.setReadUnmappedFlag(true);
        java.lang.Object obj15 = sAMRecord11.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar16 = sAMRecord11.getCigar();
        java.lang.String str17 = sAMRecord11.getSAMString();
        boolean boolean18 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord11);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList19 = sAMRecord11.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertNull(obj15);
        org.junit.Assert.assertNotNull(cigar16);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "null\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str17, "null\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(sAMTagAndValueList19);
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
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        int int12 = sAMRecord1.getAttributesBinarySize();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
    }

    @Test
    public void test166() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test166");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        htsjdk.samtools.SAMRecord sAMRecord7 = sAMRecord1.deepCopy();
        java.lang.String str8 = sAMRecord1.getReadString();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Float float10 = sAMRecord1.getFloatAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(sAMRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
    }

    @Test
    public void test167() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test167");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        java.lang.String str3 = sAMRecord1.getMateReferenceName();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Integer int5 = sAMRecord1.getIntegerAttribute("null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?16?*?0?0?*?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
    }

    @Test
    public void test168() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test168");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader4 = sAMRecord1.getHeader();
        sAMRecord1.setCigarString("*");
        // The following exception was thrown during execution in test generation
        try {
            int int7 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader4);
    }

    @Test
    public void test169() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test169");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setAlignmentStart((int) (short) 100);
        int int12 = sAMRecord1.getMappingQuality();
        int int13 = sAMRecord1.getAttributesBinarySize();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 100 + "'", int12 == 100);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
    }

    @Test
    public void test170() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test170");
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
        java.lang.String str48 = sAMRecord17.getSAMString();
        int int49 = sAMRecord17.getLengthOnReference();
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
        org.junit.Assert.assertEquals("'" + str48 + "' != '" + "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str48, "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + int49 + "' != '" + 0 + "'", int49 == 0);
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
        sAMRecord1.setReadNegativeStrandFlag(true);
        sAMRecord1.setReadNegativeStrandFlag(true);
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
    }

    @Test
    public void test172() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test172");
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
        byte[] byteArray24 = sAMRecord1.getBaseQualities();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str26 = sAMRecord1.getStringAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
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
        org.junit.Assert.assertNotNull(byteArray24);
        org.junit.Assert.assertArrayEquals(byteArray24, new byte[] {});
    }

    @Test
    public void test173() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test173");
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
        sAMRecord14.setMappingQuality((-1));
        boolean boolean17 = sAMRecord14.getReadNegativeStrandFlag();
        int int18 = sAMRecord14.getLengthOnReference();
        sAMRecord14.setSecondaryAlignment(true);
        sAMRecord14.setMappingQuality((int) (short) 100);
        sAMRecord14.setAlignmentStart((int) (short) 100);
        int int25 = sAMRecord14.getMappingQuality();
        java.lang.Object obj26 = sAMRecord1.getTransientAttribute((java.lang.Object) sAMRecord14);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + 0 + "'", int18 == 0);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 100 + "'", int25 == 100);
        org.junit.Assert.assertNull(obj26);
    }

    @Test
    public void test174() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test174");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSupplementaryAlignmentFlag(true);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        boolean boolean9 = sAMRecord1.getSupplementaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
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
        java.lang.String str12 = sAMRecord1.getPairedReadName();
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "null" + "'", str12, "null");
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
    }

    @Test
    public void test176() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test176");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet11 = sAMRecord1.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        sAMRecord13.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord13.setReferenceName("");
        htsjdk.samtools.SAMFileHeader sAMFileHeader20 = null;
        htsjdk.samtools.SAMRecord sAMRecord21 = new htsjdk.samtools.SAMRecord(sAMFileHeader20);
        sAMRecord21.setDuplicateReadFlag(false);
        java.lang.Object obj24 = null;
        boolean boolean25 = sAMRecord21.equals(obj24);
        java.lang.String str26 = sAMRecord21.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader27 = null;
        htsjdk.samtools.SAMRecord sAMRecord28 = new htsjdk.samtools.SAMRecord(sAMFileHeader27);
        htsjdk.samtools.SAMFileHeader sAMFileHeader29 = sAMRecord28.getHeader();
        byte[] byteArray32 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord28.setBaseQualities(byteArray32);
        sAMRecord21.setBaseQualities(byteArray32);
        sAMRecord13.setBaseQualities(byteArray32);
        sAMRecord1.setReadBases(byteArray32);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertNotNull(sAMFlagSet11);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertEquals("'" + str26 + "' != '" + "null" + "'", str26, "null");
        org.junit.Assert.assertNull(sAMFileHeader29);
        org.junit.Assert.assertNotNull(byteArray32);
        org.junit.Assert.assertArrayEquals(byteArray32, new byte[] { (byte) 0, (byte) 0 });
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
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        sAMRecord1.setFirstOfPairFlag(false);
        sAMRecord1.setReadNegativeStrandFlag(true);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
    }

    @Test
    public void test178() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test178");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        int int7 = sAMRecord1.getReadPositionAtReferencePosition((int) (short) -1);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList8 = sAMRecord1.getAlignmentBlocks();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
        org.junit.Assert.assertNotNull(alignmentBlockList8);
    }

    @Test
    public void test179() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test179");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean8 = sAMRecord1.getReadPairedFlag();
        byte[] byteArray9 = sAMRecord1.getBaseQualities();
        htsjdk.samtools.SAMFileHeader sAMFileHeader10 = null;
        sAMRecord1.setHeader(sAMFileHeader10);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertNotNull(byteArray9);
        org.junit.Assert.assertArrayEquals(byteArray9, new byte[] {});
    }

    @Test
    public void test180() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test180");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        sAMRecord1.setHeader(sAMFileHeader12);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
    }

    @Test
    public void test181() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test181");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord6 = sAMRecord1.getReadGroup();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMReadGroupRecord6);
    }

    @Test
    public void test182() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test182");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReferenceName("");
        int int12 = sAMRecord1.getMappingQuality();
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray14 = sAMRecord1.getSignedIntArrayAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 100 + "'", int12 == 100);
    }

    @Test
    public void test183() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test183");
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
        byte[] byteArray24 = sAMRecord1.getBaseQualities();
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray26 = sAMRecord1.getFloatArrayAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
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
        org.junit.Assert.assertNotNull(byteArray24);
        org.junit.Assert.assertArrayEquals(byteArray24, new byte[] {});
    }

    @Test
    public void test184() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test184");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setAlignmentStart((int) (short) 100);
        int int12 = sAMRecord1.getMappingQuality();
        int int13 = sAMRecord1.getUnclippedEnd();
        int int16 = sAMRecord1.getReadPositionAtReferencePosition((-1), false);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 100 + "'", int12 == 100);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 99 + "'", int13 == 99);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
    }

    @Test
    public void test185() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test185");
        int int0 = htsjdk.samtools.SAMRecord.UNKNOWN_MAPPING_QUALITY;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 255 + "'", int0 == 255);
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
        sAMRecord1.reverseComplement();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
    }

    @Test
    public void test187() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test187");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        int int5 = sAMRecord1.getMappingQuality();
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord7 = sAMRecord1.getReadGroup();
        java.lang.Class<?> wildcardClass8 = sAMRecord1.getClass();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertNull(sAMReadGroupRecord7);
        org.junit.Assert.assertNotNull(wildcardClass8);
    }

    @Test
    public void test188() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test188");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setReadUmappedFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setBaseQualityString("null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Invalid fastq character: ?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
    }

    @Test
    public void test189() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test189");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setReadFailsVendorQualityCheckFlag(false);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord7 = sAMRecord1.getReadGroup();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(sAMReadGroupRecord7);
    }

    @Test
    public void test190() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test190");
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
        sAMRecord1.setFlags((int) (byte) 10);
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
    public void test191() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test191");
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
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray17 = sAMRecord13.getFloatArrayAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + (-1) + "'", int15 == (-1));
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
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setReadNegativeStrandFlag(false);
        sAMRecord1.setMateUnmappedFlag(false);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Short short15 = sAMRecord1.getShortAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
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
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList15 = sAMRecord9.isValid(false);
        sAMRecord9.setMateReferenceName("hi!");
        sAMRecord9.setAlignmentStart((int) (short) 1);
        int int20 = sAMRecord9.getStart();
        java.lang.Object obj21 = sAMRecord1.getTransientAttribute((java.lang.Object) int20);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList15);
        org.junit.Assert.assertTrue("'" + int20 + "' != '" + 1 + "'", int20 == 1);
        org.junit.Assert.assertNull(obj21);
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
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        sAMRecord1.setReadString("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        java.lang.String str16 = sAMRecord1.getPairedReadName();
        boolean boolean17 = sAMRecord1.isSecondaryOrSupplementary();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "null" + "'", str16, "null");
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
    }

    @Test
    public void test195() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test195");
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
        sAMRecord1.setReadString("null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertNotNull(sAMValidationErrorList25);
    }

    @Test
    public void test196() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test196");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean11 = sAMRecord1.isUnsignedArrayAttribute("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?256?*?*?-1?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
    }

    @Test
    public void test197() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test197");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int7 = sAMRecord1.getMateAlignmentStart();
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
    }

    @Test
    public void test198() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test198");
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
        sAMRecord1.setReadString("null");
        java.lang.String str17 = sAMRecord1.toString();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "null 4b aligned to *:0--1." + "'", str17, "null 4b aligned to *:0--1.");
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
        sAMRecord1.setReadNegativeStrandFlag(false);
        int int12 = sAMRecord1.getMappingQuality();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
    }

    @Test
    public void test200() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test200");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setAlignmentStart((int) (short) 100);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        sAMRecord13.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord13.setReferenceName("hi!");
        sAMRecord13.setFlags((int) (byte) 100);
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        htsjdk.samtools.SAMFileHeader sAMFileHeader24 = sAMRecord23.getHeader();
        java.lang.String str25 = sAMRecord23.getMateReferenceName();
        java.lang.String str26 = sAMRecord23.toString();
        htsjdk.samtools.SAMFileHeader sAMFileHeader27 = null;
        htsjdk.samtools.SAMRecord sAMRecord28 = new htsjdk.samtools.SAMRecord(sAMFileHeader27);
        int int30 = sAMRecord28.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList32 = sAMRecord28.validateCigar((long) (byte) 100);
        int int33 = sAMRecord28.getUnclippedStart();
        java.lang.Object obj34 = sAMRecord13.setTransientAttribute((java.lang.Object) str26, (java.lang.Object) int33);
        htsjdk.samtools.SAMFileHeader sAMFileHeader35 = null;
        htsjdk.samtools.SAMRecord sAMRecord36 = new htsjdk.samtools.SAMRecord(sAMFileHeader35);
        sAMRecord36.setReadUnmappedFlag(true);
        java.lang.Object obj40 = sAMRecord36.getAttribute((short) 10);
        htsjdk.samtools.SAMFileHeader sAMFileHeader41 = sAMRecord36.getHeader();
        java.lang.Object obj42 = sAMRecord1.setTransientAttribute((java.lang.Object) int33, (java.lang.Object) sAMFileHeader41);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMFileHeader24);
        org.junit.Assert.assertEquals("'" + str25 + "' != '" + "*" + "'", str25, "*");
        org.junit.Assert.assertEquals("'" + str26 + "' != '" + "null 0b aligned to *:0--1." + "'", str26, "null 0b aligned to *:0--1.");
        org.junit.Assert.assertTrue("'" + int30 + "' != '" + 0 + "'", int30 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList32);
        org.junit.Assert.assertTrue("'" + int33 + "' != '" + 0 + "'", int33 == 0);
        org.junit.Assert.assertNull(obj34);
        org.junit.Assert.assertNull(obj40);
        org.junit.Assert.assertNull(sAMFileHeader41);
        org.junit.Assert.assertNull(obj42);
    }

    @Test
    public void test201() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test201");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList7 = sAMRecord1.getAlignmentBlocks();
        java.lang.String str8 = sAMRecord1.getPairedReadName();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray10 = sAMRecord1.getSignedByteArrayAttribute("null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?16?*?0?0?*?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(alignmentBlockList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "null" + "'", str8, "null");
    }

    @Test
    public void test202() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test202");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setProperPairFlag(true);
        byte[] byteArray5 = sAMRecord1.getBaseQualities();
        int int6 = sAMRecord1.getReadLength();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] {});
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test203() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test203");
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
        java.lang.Long long17 = sAMRecord1.getUnsignedIntegerAttribute((short) 100);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "*" + "'", str14, "*");
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
        org.junit.Assert.assertNull(long17);
    }

    @Test
    public void test204() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test204");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        int int4 = sAMRecord1.getMappingQuality();
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 0 + "'", int4 == 0);
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        int int11 = sAMRecord9.getReferencePositionAtReadPosition((int) (byte) -1);
        boolean boolean13 = sAMRecord1.withinDistanceOf((htsjdk.samtools.util.Locatable) sAMRecord9, (int) ' ');
        sAMRecord1.setFirstOfPairFlag(false);
        sAMRecord1.setReadString("null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
    }

    @Test
    public void test206() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test206");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        sAMRecord1.setFlags(0);
    }

    @Test
    public void test207() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test207");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = null;
        htsjdk.samtools.SAMRecord sAMRecord7 = new htsjdk.samtools.SAMRecord(sAMFileHeader6);
        sAMRecord7.setDuplicateReadFlag(false);
        java.lang.Object obj10 = null;
        boolean boolean11 = sAMRecord7.equals(obj10);
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        sAMRecord13.setDuplicateReadFlag(false);
        sAMRecord13.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj18 = sAMRecord7.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord19 = sAMRecord7.deepCopy();
        htsjdk.samtools.Cigar cigar20 = sAMRecord7.getCigar();
        sAMRecord1.setCigar(cigar20);
        sAMRecord1.setReadUmappedFlag(true);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertNull(obj18);
        org.junit.Assert.assertNotNull(sAMRecord19);
        org.junit.Assert.assertNotNull(cigar20);
    }

    @Test
    public void test208() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test208");
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
        sAMRecord23.setDuplicateReadFlag(false);
        sAMRecord23.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord23.setReferenceName("hi!");
        java.lang.Object obj30 = sAMRecord1.setTransientAttribute((java.lang.Object) wildcardClass21, (java.lang.Object) "hi!");
        java.lang.Object obj32 = sAMRecord1.getAttribute((short) 100);
        sAMRecord1.setSecondaryAlignment(true);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(wildcardClass21);
        org.junit.Assert.assertNull(obj30);
        org.junit.Assert.assertNull(obj32);
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
        sAMRecord1.setReadUnmappedFlag(true);
        sAMRecord1.setReferenceName("null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test210() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test210");
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
        java.lang.String str17 = sAMRecord1.format();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList19 = sAMRecord1.validateCigar((long) '#');
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*" + "'", str17, "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        org.junit.Assert.assertNull(sAMValidationErrorList19);
    }

    @Test
    public void test211() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test211");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setSecondOfPairFlag(true);
        java.lang.Long long9 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Long long11 = sAMRecord1.getUnsignedIntegerAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(long9);
    }

    @Test
    public void test212() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test212");
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
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean23 = sAMRecord1.getSecondOfPairFlag();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: Inappropriate call if not paired read");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "null 0b aligned to *:0--1." + "'", str22, "null 0b aligned to *:0--1.");
    }

    @Test
    public void test213() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test213");
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
            java.lang.Integer int15 = sAMRecord13.getIntegerAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
    }

    @Test
    public void test214() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test214");
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
        boolean boolean16 = sAMRecord1.getSupplementaryAlignmentFlag();
        java.lang.Object obj18 = sAMRecord1.getTransientAttribute((java.lang.Object) 'a');
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNull(obj18);
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
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        byte[] byteArray10 = sAMRecord1.getOriginalBaseQualities();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNull(byteArray10);
    }

    @Test
    public void test216() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test216");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        boolean boolean7 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test217() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test217");
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
        java.lang.String str15 = sAMRecord1.getBaseQualityString();
        sAMRecord1.setReferenceName("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertNotNull(byteArray14);
        org.junit.Assert.assertArrayEquals(byteArray14, new byte[] {});
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "*" + "'", str15, "*");
    }

    @Test
    public void test218() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test218");
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
        sAMRecord23.setDuplicateReadFlag(false);
        sAMRecord23.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord23.setReferenceName("hi!");
        java.lang.Object obj30 = sAMRecord1.setTransientAttribute((java.lang.Object) wildcardClass21, (java.lang.Object) "hi!");
        java.lang.Object obj32 = sAMRecord1.getAttribute((short) 100);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord33 = sAMRecord1.getReadGroup();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(wildcardClass21);
        org.junit.Assert.assertNull(obj30);
        org.junit.Assert.assertNull(obj32);
        org.junit.Assert.assertNull(sAMReadGroupRecord33);
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
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        byte[] byteArray13 = sAMRecord1.getOriginalBaseQualities();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertNull(byteArray13);
    }

    @Test
    public void test220() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test220");
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
        java.lang.String str16 = sAMRecord1.getSAMString();
        int int17 = sAMRecord1.getInferredInsertSize();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n" + "'", str16, "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + 0 + "'", int17 == 0);
    }

    @Test
    public void test221() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test221");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        htsjdk.samtools.SAMFileHeader sAMFileHeader10 = null;
        htsjdk.samtools.SAMRecord sAMRecord11 = new htsjdk.samtools.SAMRecord(sAMFileHeader10);
        sAMRecord11.setReadUnmappedFlag(true);
        java.lang.Object obj15 = sAMRecord11.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar16 = sAMRecord11.getCigar();
        java.lang.String str17 = sAMRecord11.getSAMString();
        boolean boolean18 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord11);
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray20 = sAMRecord11.getFloatArrayAttribute("null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?*?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertNull(obj15);
        org.junit.Assert.assertNotNull(cigar16);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "null\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str17, "null\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
    }

    @Test
    public void test222() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test222");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList5 = sAMRecord1.validateCigar((long) (byte) 100);
        // The following exception was thrown during execution in test generation
        try {
            int int6 = sAMRecord1.getReadNameLength();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"String.length()\" because \"this.mReadName\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
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
        java.lang.Object obj7 = sAMRecord1.getAttribute((short) 100);
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList8 = sAMRecord1.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(obj7);
        org.junit.Assert.assertNotNull(sAMTagAndValueList8);
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
        sAMRecord1.setSecondaryAlignment(true);
        boolean boolean14 = sAMRecord1.getDuplicateReadFlag();
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = null;
        htsjdk.samtools.SAMRecord sAMRecord16 = new htsjdk.samtools.SAMRecord(sAMFileHeader15);
        sAMRecord16.setDuplicateReadFlag(false);
        java.lang.Object obj19 = null;
        boolean boolean20 = sAMRecord16.equals(obj19);
        java.lang.String str21 = sAMRecord16.getPairedReadName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        htsjdk.samtools.SAMFileHeader sAMFileHeader24 = sAMRecord23.getHeader();
        byte[] byteArray27 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord23.setBaseQualities(byteArray27);
        sAMRecord16.setBaseQualities(byteArray27);
        sAMRecord1.setBaseQualities(byteArray27);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "null" + "'", str21, "null");
        org.junit.Assert.assertNull(sAMFileHeader24);
        org.junit.Assert.assertNotNull(byteArray27);
        org.junit.Assert.assertArrayEquals(byteArray27, new byte[] { (byte) 0, (byte) 0 });
    }

    @Test
    public void test225() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test225");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        int int6 = sAMRecord1.getInferredInsertSize();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) (short) 100, true);
        sAMRecord1.setReadString("hi!");
        int int12 = sAMRecord1.getEnd();
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
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
        java.lang.String str13 = sAMRecord1.getBaseQualityString();
        boolean boolean14 = sAMRecord1.getReadPairedFlag();
        sAMRecord1.reverseComplement(false);
        // The following exception was thrown during execution in test generation
        try {
            boolean boolean18 = sAMRecord1.hasAttribute("null");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "*" + "'", str13, "*");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test227() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test227");
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
        sAMRecord1.setFlags(2147483647);
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
        boolean boolean35 = sAMRecord1.getFirstOfPairFlag();
        sAMRecord1.setMateReferenceName("null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray39 = sAMRecord1.getFloatArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
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
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        int int16 = sAMRecord1.getUnclippedEnd();
        sAMRecord1.setMateReferenceName("");
        int int19 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + (-1) + "'", int16 == (-1));
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + (-1) + "'", int19 == (-1));
    }

    @Test
    public void test229() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test229");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
        java.lang.Class<?> wildcardClass12 = sAMRecord1.getClass();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test230() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test230");
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
        int int16 = sAMRecord1.getAlignmentEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + (-1) + "'", int16 == (-1));
    }

    @Test
    public void test231() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test231");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        int int6 = sAMRecord1.getLengthOnReference();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
    }

    @Test
    public void test232() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test232");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        byte[] byteArray5 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord1.setBaseQualities(byteArray5);
        htsjdk.samtools.SAMRecord sAMRecord7 = sAMRecord1.deepCopy();
        boolean boolean8 = sAMRecord1.getSupplementaryAlignmentFlag();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertNotNull(byteArray5);
        org.junit.Assert.assertArrayEquals(byteArray5, new byte[] { (byte) 0, (byte) 0 });
        org.junit.Assert.assertNotNull(sAMRecord7);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test233() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test233");
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
        sAMRecord1.setInferredInsertSize((int) ' ');
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Float float19 = sAMRecord1.getFloatAttribute("null 0b aligned to *:0--1.");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null 0b aligned to *:0--1.");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(sAMTagAndValueList15);
    }

    @Test
    public void test234() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test234");
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
        sAMRecord1.setReadPairedFlag(false);
        boolean boolean26 = sAMRecord1.getReadNegativeStrandFlag();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertEquals("'" + str3 + "' != '" + "*" + "'", str3, "*");
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList11);
        org.junit.Assert.assertNotNull(sAMFlagSet16);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 4680 + "'", int23 == 4680);
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
    }

    @Test
    public void test235() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test235");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray7 = sAMRecord1.getFloatArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
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
        java.lang.Class<?> wildcardClass10 = sAMRecord1.getClass();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(wildcardClass10);
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
        sAMRecord1.setSupplementaryAlignmentFlag(true);
        int int8 = sAMRecord1.getUnclippedEnd();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + (-1) + "'", int8 == (-1));
    }

    @Test
    public void test238() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test238");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        sAMRecord1.setMateAlignmentStart((-1));
        sAMRecord1.setFlags(255);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
    }

    @Test
    public void test239() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test239");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        // The following exception was thrown during execution in test generation
        try {
            float[] floatArray9 = sAMRecord1.getFloatArrayAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test240() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test240");
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
        int int16 = sAMRecord1.getFlags();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMReadGroupRecord15);
        org.junit.Assert.assertTrue("'" + int16 + "' != '" + 0 + "'", int16 == 0);
    }

    @Test
    public void test241() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test241");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        htsjdk.samtools.SAMFileHeader sAMFileHeader6 = sAMRecord1.getHeader();
        boolean boolean7 = sAMRecord1.getReadNegativeStrandFlag();
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertNull(sAMFileHeader6);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test242() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test242");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
    }

    @Test
    public void test243() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test243");
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
        sAMRecord8.setMateUnmappedFlag(false);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertNull(sAMValidationErrorList5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNull(obj17);
    }

    @Test
    public void test244() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test244");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        java.lang.String[] strArray20 = new java.lang.String[] { "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n", "*", "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n", "*", "*", "*", "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n", "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*", "null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n", "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*", "*", "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n", "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        java.util.List<java.lang.String> strList23 = htsjdk.samtools.SAMRecord.TAGS_TO_REVERSE_COMPLEMENT;
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.reverseComplement((java.util.Collection<java.lang.String>) strList21, (java.util.Collection<java.lang.String>) strList23, false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?16?*?0?0?*?*?0?0?*?*?");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n", "*", "null\t16\t*\t0\t0\t*\t*\t0\t0\t*\t*\n", "*", "*", "*", "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n", "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*", "null\t0\t*\t0\t0\t*\t*\t0\t0\t*\t*\n", "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*", "*", "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n", "null\t256\t*\t0\t-1\t*\t*\t0\t0\t*\t*\n" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(strList23);
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
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setSupplementaryAlignmentFlag(false);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test246() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test246");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet11 = sAMRecord1.getSAMFlags();
        boolean boolean12 = sAMRecord1.getReadUnmappedFlag();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertNotNull(sAMFlagSet11);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test247() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test247");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        sAMRecord1.setMappingQuality((int) (byte) 100);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test248() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test248");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        sAMRecord1.setFlags(99);
        sAMRecord1.setReadString("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        boolean boolean17 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        java.util.List<htsjdk.samtools.SAMRecord.SAMTagAndValue> sAMTagAndValueList18 = sAMRecord1.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNotNull(sAMTagAndValueList18);
    }

    @Test
    public void test249() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test249");
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
        byte[] byteArray24 = sAMRecord1.getBaseQualities();
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray26 = sAMRecord1.getSignedByteArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
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
        org.junit.Assert.assertNotNull(byteArray24);
        org.junit.Assert.assertArrayEquals(byteArray24, new byte[] {});
    }

    @Test
    public void test250() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test250");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        htsjdk.samtools.SAMFileHeader sAMFileHeader2 = sAMRecord1.getHeader();
        sAMRecord1.setReadUmappedFlag(false);
        boolean boolean5 = sAMRecord1.getNotPrimaryAlignmentFlag();
        org.junit.Assert.assertNull(sAMFileHeader2);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
    }

    @Test
    public void test251() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test251");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int11 = sAMRecord1.getReadPositionAtReferencePosition((int) (short) 0);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
    }

    @Test
    public void test252() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test252");
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
        byte[] byteArray37 = sAMRecord21.getReadBases();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Byte byte39 = sAMRecord21.getByteAttribute("hi!");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: hi!");
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
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
        org.junit.Assert.assertNotNull(byteArray37);
        org.junit.Assert.assertArrayEquals(byteArray37, new byte[] {});
    }

    @Test
    public void test253() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test253");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        int int9 = sAMRecord1.getAttributesBinarySize();
        sAMRecord1.setNotPrimaryAlignmentFlag(true);
        int int12 = sAMRecord1.getStart();
        int int15 = sAMRecord1.getReadPositionAtReferencePosition(0, false);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 0 + "'", int15 == 0);
    }

    @Test
    public void test254() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test254");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        htsjdk.samtools.ValidationStringency validationStringency11 = sAMRecord1.getValidationStringency();
        sAMRecord1.setMateNegativeStrandFlag(true);
        boolean boolean14 = sAMRecord1.getReadFailsVendorQualityCheckFlag();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + validationStringency11 + "' != '" + htsjdk.samtools.ValidationStringency.SILENT + "'", validationStringency11.equals(htsjdk.samtools.ValidationStringency.SILENT));
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
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
        sAMRecord1.setReferenceIndex((-1));
        sAMRecord1.setReadUnmappedFlag(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertNotNull(sAMFlagSet11);
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
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet12 = sAMRecord1.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader13 = null;
        htsjdk.samtools.SAMRecord sAMRecord14 = new htsjdk.samtools.SAMRecord(sAMFileHeader13);
        htsjdk.samtools.SAMFileHeader sAMFileHeader15 = sAMRecord14.getHeader();
        sAMRecord14.setProperPairFlag(true);
        boolean boolean18 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord14);
        java.lang.String str19 = sAMRecord1.getBaseQualityString();
        int int20 = sAMRecord1.getUnclippedStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(sAMFlagSet12);
        org.junit.Assert.assertNull(sAMFileHeader15);
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "*" + "'", str19, "*");
        org.junit.Assert.assertTrue("'" + int20 + "' != '" + 0 + "'", int20 == 0);
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
        java.lang.String str8 = sAMRecord1.getReferenceName();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "null" + "'", str6, "null");
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 0 + "'", int7 == 0);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
    }

    @Test
    public void test258() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test258");
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
        java.lang.String str17 = sAMRecord1.getCigarString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "*" + "'", str17, "*");
    }

    @Test
    public void test259() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test259");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        int int8 = sAMRecord1.getAlignmentEnd();
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setReferenceIndex((int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalStateException; message: A non-null SAMFileHeader is required to resolve the reference index or name");
        } catch (java.lang.IllegalStateException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + (-1) + "'", int8 == (-1));
    }

    @Test
    public void test260() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test260");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList11 = sAMRecord1.getAlignmentBlocks();
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = sAMRecord1.getHeader();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertNotNull(alignmentBlockList11);
        org.junit.Assert.assertNull(sAMFileHeader12);
    }

    @Test
    public void test261() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test261");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        sAMRecord1.setFlags((int) (byte) 1);
        boolean boolean9 = sAMRecord1.getSupplementaryAlignmentFlag();
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test262() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test262");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        sAMRecord1.setMateAlignmentStart((-1));
        htsjdk.samtools.SAMFileHeader sAMFileHeader12 = null;
        htsjdk.samtools.SAMRecord sAMRecord13 = new htsjdk.samtools.SAMRecord(sAMFileHeader12);
        htsjdk.samtools.SAMFileHeader sAMFileHeader14 = sAMRecord13.getHeader();
        sAMRecord13.setProperPairFlag(true);
        byte[] byteArray17 = sAMRecord13.getBaseQualities();
        sAMRecord1.setOriginalBaseQualities(byteArray17);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertNull(sAMFileHeader14);
        org.junit.Assert.assertNotNull(byteArray17);
        org.junit.Assert.assertArrayEquals(byteArray17, new byte[] {});
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
        int int27 = sAMRecord1.getCigarLength();
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
        org.junit.Assert.assertTrue("'" + int27 + "' != '" + 0 + "'", int27 == 0);
    }

    @Test
    public void test264() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test264");
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
        java.lang.String str37 = sAMRecord1.getSAMString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(obj20);
        org.junit.Assert.assertNotNull(sAMRecord21);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList29);
        org.junit.Assert.assertTrue("'" + int34 + "' != '" + 1 + "'", int34 == 1);
        org.junit.Assert.assertNull(obj35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "*" + "'", str36, "*");
        org.junit.Assert.assertEquals("'" + str37 + "' != '" + "null\t384\t*\t0\t0\t*\t*\t0\t0\t*\t*\n" + "'", str37, "null\t384\t*\t0\t0\t*\t*\t0\t0\t*\t*\n");
    }

    @Test
    public void test265() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test265");
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
        java.lang.String str25 = sAMRecord1.format();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 0 + "'", int12 == 0);
        org.junit.Assert.assertNull(obj21);
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "null 0b aligned to *:0--1." + "'", str22, "null 0b aligned to *:0--1.");
        org.junit.Assert.assertEquals("'" + str25 + "' != '" + "null\t1024\t*\t*\t-1\t*\t*\t*\t*\t*\t*" + "'", str25, "null\t1024\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
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
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        htsjdk.samtools.SAMRecord sAMRecord9 = new htsjdk.samtools.SAMRecord(sAMFileHeader8);
        sAMRecord9.setDuplicateReadFlag(false);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMRecord9.equals(obj12);
        boolean boolean14 = sAMRecord1.overlaps((htsjdk.samtools.util.Locatable) sAMRecord9);
        boolean boolean15 = sAMRecord1.getReadUnmappedFlag();
        java.lang.String str16 = sAMRecord1.format();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*" + "'", str16, "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
    }

    @Test
    public void test267() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test267");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        int int3 = sAMRecord1.getReferencePositionAtReadPosition((int) (byte) -1);
        int int5 = sAMRecord1.getReadPositionAtReferencePosition((int) (byte) 0);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int9 = sAMRecord1.getReadPositionAtReferencePosition((int) ' ', false);
        int int10 = sAMRecord1.getAttributesBinarySize();
        java.lang.String str11 = sAMRecord1.format();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 0 + "'", int3 == 0);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + 0 + "'", int9 == 0);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*" + "'", str11, "null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*");
    }

    @Test
    public void test268() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test268");
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
        // The following exception was thrown during execution in test generation
        try {
            int[] intArray17 = sAMRecord1.getUnsignedIntArrayAttribute("*");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: *");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test269() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test269");
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
        boolean boolean19 = sAMRecord1.getReadUnmappedFlag();
        sAMRecord1.setBaseQualityString("hi!");
        htsjdk.samtools.SAMFileHeader sAMFileHeader23 = null;
        htsjdk.samtools.SAMRecord sAMRecord24 = new htsjdk.samtools.SAMRecord(sAMFileHeader23);
        int int26 = sAMRecord24.getReferencePositionAtReadPosition((int) (byte) -1);
        sAMRecord24.setSecondaryAlignment(true);
        sAMRecord24.setSecondOfPairFlag(true);
        htsjdk.samtools.SAMFileHeader sAMFileHeader31 = null;
        htsjdk.samtools.SAMRecord sAMRecord32 = new htsjdk.samtools.SAMRecord(sAMFileHeader31);
        sAMRecord32.setDuplicateReadFlag(false);
        java.lang.Object obj35 = null;
        boolean boolean36 = sAMRecord32.equals(obj35);
        htsjdk.samtools.SAMFileHeader sAMFileHeader37 = null;
        htsjdk.samtools.SAMRecord sAMRecord38 = new htsjdk.samtools.SAMRecord(sAMFileHeader37);
        sAMRecord38.setDuplicateReadFlag(false);
        sAMRecord38.setReadFailsVendorQualityCheckFlag(true);
        java.lang.Object obj43 = sAMRecord32.getTransientAttribute((java.lang.Object) true);
        htsjdk.samtools.SAMRecord sAMRecord44 = sAMRecord32.deepCopy();
        htsjdk.samtools.SAMFileHeader sAMFileHeader45 = null;
        htsjdk.samtools.SAMRecord sAMRecord46 = new htsjdk.samtools.SAMRecord(sAMFileHeader45);
        sAMRecord46.setDuplicateReadFlag(false);
        java.lang.Object obj49 = null;
        boolean boolean50 = sAMRecord46.equals(obj49);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList52 = sAMRecord46.isValid(false);
        sAMRecord46.setMateReferenceName("hi!");
        sAMRecord46.setAlignmentStart((int) (short) 1);
        int int57 = sAMRecord46.getStart();
        java.lang.Object obj58 = sAMRecord24.setTransientAttribute((java.lang.Object) sAMRecord44, (java.lang.Object) int57);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList60 = sAMRecord24.isValid(true);
        // The following exception was thrown during execution in test generation
        try {
            sAMRecord1.setAttribute("null\t0\t*\t*\t0\t*\t*\t*\t*\t*\t*", (java.lang.Object) sAMRecord24);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?*?0?*?*?*?*?*?*");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + 0 + "'", int18 == 0);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + 0 + "'", int26 == 0);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + false + "'", boolean36 == false);
        org.junit.Assert.assertNull(obj43);
        org.junit.Assert.assertNotNull(sAMRecord44);
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + false + "'", boolean50 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList52);
        org.junit.Assert.assertTrue("'" + int57 + "' != '" + 1 + "'", int57 == 1);
        org.junit.Assert.assertNull(obj58);
        org.junit.Assert.assertNotNull(sAMValidationErrorList60);
    }

    @Test
    public void test270() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test270");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        sAMRecord1.setBaseQualityString("");
        int int6 = sAMRecord1.getStart();
        int int7 = sAMRecord1.getUnclippedEnd();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Integer int9 = sAMRecord1.getIntegerAttribute("");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: ");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 0 + "'", int6 == 0);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test271() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test271");
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
        // The following exception was thrown during execution in test generation
        try {
            java.lang.Object obj27 = sAMRecord1.getAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
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
    }

    @Test
    public void test272() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test272");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        byte[] byteArray8 = sAMRecord1.getReadBases();
        htsjdk.samtools.Cigar cigar9 = null;
        sAMRecord1.setCigar(cigar9);
        sAMRecord1.reverseComplement(false);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertNotNull(byteArray8);
        org.junit.Assert.assertArrayEquals(byteArray8, new byte[] {});
    }

    @Test
    public void test273() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test273");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReadPairedFlag(false);
        sAMRecord1.setReferenceName("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
    }

    @Test
    public void test274() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test274");
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
        sAMRecord13.setFlags(2147483647);
        boolean boolean30 = sAMRecord1.contains((htsjdk.samtools.util.Locatable) sAMRecord13);
        htsjdk.samtools.Cigar cigar31 = sAMRecord1.getCigar();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(obj24);
        org.junit.Assert.assertNull(sAMReadGroupRecord27);
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertNotNull(cigar31);
    }

    @Test
    public void test275() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test275");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setReadUnmappedFlag(true);
        java.lang.Object obj5 = sAMRecord1.getAttribute((short) 10);
        htsjdk.samtools.Cigar cigar6 = sAMRecord1.getCigar();
        int int7 = sAMRecord1.getLengthOnReference();
        htsjdk.samtools.SAMFileHeader sAMFileHeader8 = null;
        sAMRecord1.setHeaderStrict(sAMFileHeader8);
        sAMRecord1.setFlags(255);
        org.junit.Assert.assertNull(obj5);
        org.junit.Assert.assertNotNull(cigar6);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
    }

    @Test
    public void test276() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test276");
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
        sAMRecord1.setMateNegativeStrandFlag(false);
        htsjdk.samtools.SAMFileHeader sAMFileHeader17 = null;
        htsjdk.samtools.SAMRecord sAMRecord18 = new htsjdk.samtools.SAMRecord(sAMFileHeader17);
        htsjdk.samtools.SAMFileHeader sAMFileHeader19 = sAMRecord18.getHeader();
        byte[] byteArray22 = new byte[] { (byte) 0, (byte) 0 };
        sAMRecord18.setBaseQualities(byteArray22);
        sAMRecord1.setOriginalBaseQualities(byteArray22);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNull(sAMFileHeader19);
        org.junit.Assert.assertNotNull(byteArray22);
        org.junit.Assert.assertArrayEquals(byteArray22, new byte[] { (byte) 0, (byte) 0 });
    }

    @Test
    public void test277() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test277");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        sAMRecord1.setReadPairedFlag(false);
        htsjdk.samtools.SAMReadGroupRecord sAMReadGroupRecord12 = sAMRecord1.getReadGroup();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertNull(sAMReadGroupRecord12);
    }

    @Test
    public void test278() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test278");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        sAMRecord1.setReadFailsVendorQualityCheckFlag(true);
        sAMRecord1.setReferenceName("hi!");
        boolean boolean8 = sAMRecord1.getReadUnmappedFlag();
        boolean boolean9 = sAMRecord1.getDuplicateReadFlag();
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test279() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test279");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setMappingQuality((-1));
        boolean boolean4 = sAMRecord1.getReadNegativeStrandFlag();
        int int5 = sAMRecord1.getLengthOnReference();
        sAMRecord1.setSecondaryAlignment(true);
        sAMRecord1.setMappingQuality((int) (short) 100);
        int int11 = sAMRecord1.getReferencePositionAtReadPosition((int) (short) 0);
        boolean boolean12 = sAMRecord1.getReadUnmappedFlag();
        int int13 = sAMRecord1.getCigarLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 0 + "'", int13 == 0);
    }

    @Test
    public void test280() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test280");
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
        int int14 = sAMRecord9.getAlignmentStart();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 0 + "'", int11 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
    }

    @Test
    public void test281() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test281");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        java.lang.String str8 = sAMRecord1.getMateReferenceName();
        java.lang.Long long10 = sAMRecord1.getUnsignedIntegerAttribute((short) (byte) 1);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet11 = sAMRecord1.getSAMFlags();
        sAMRecord1.setReferenceIndex((-1));
        int int14 = sAMRecord1.getFlags();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertNull(long10);
        org.junit.Assert.assertNotNull(sAMFlagSet11);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
    }

    @Test
    public void test282() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test282");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        boolean boolean4 = sAMRecord1.getReadUnmappedFlag();
        htsjdk.samtools.SAMFileHeader sAMFileHeader5 = null;
        htsjdk.samtools.SAMRecord sAMRecord6 = new htsjdk.samtools.SAMRecord(sAMFileHeader5);
        htsjdk.samtools.SAMFileHeader sAMFileHeader7 = sAMRecord6.getHeader();
        java.lang.String str8 = sAMRecord6.getMateReferenceName();
        htsjdk.samtools.SAMFileHeader sAMFileHeader9 = null;
        htsjdk.samtools.SAMRecord sAMRecord10 = new htsjdk.samtools.SAMRecord(sAMFileHeader9);
        sAMRecord10.setDuplicateReadFlag(false);
        java.lang.Object obj13 = null;
        boolean boolean14 = sAMRecord10.equals(obj13);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList16 = sAMRecord10.isValid(false);
        sAMRecord10.setMateReferenceName("hi!");
        sAMRecord10.setFirstOfPairFlag(true);
        java.util.Set<htsjdk.samtools.SAMFlag> sAMFlagSet21 = sAMRecord10.getSAMFlags();
        htsjdk.samtools.SAMFileHeader sAMFileHeader22 = null;
        htsjdk.samtools.SAMRecord sAMRecord23 = new htsjdk.samtools.SAMRecord(sAMFileHeader22);
        htsjdk.samtools.SAMFileHeader sAMFileHeader24 = sAMRecord23.getHeader();
        sAMRecord23.setProperPairFlag(true);
        boolean boolean27 = sAMRecord10.contains((htsjdk.samtools.util.Locatable) sAMRecord23);
        int int28 = sAMRecord6.computeIndexingBinIfAbsent(sAMRecord23);
        int int31 = sAMRecord23.getReadPositionAtReferencePosition(2147483647, true);
        boolean boolean32 = sAMRecord23.getSupplementaryAlignmentFlag();
        java.lang.Object obj33 = sAMRecord1.getTransientAttribute((java.lang.Object) boolean32);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(sAMFileHeader7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "*" + "'", str8, "*");
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList16);
        org.junit.Assert.assertNotNull(sAMFlagSet21);
        org.junit.Assert.assertNull(sAMFileHeader24);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + true + "'", boolean27 == true);
        org.junit.Assert.assertTrue("'" + int28 + "' != '" + 4680 + "'", int28 == 4680);
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + 0 + "'", int31 == 0);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertNull(obj33);
    }

    @Test
    public void test283() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test283");
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
        java.lang.String str17 = sAMRecord1.format();
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList18 = sAMRecord1.isValid();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int5 + "' != '" + 0 + "'", int5 == 0);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*" + "'", str17, "null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        org.junit.Assert.assertNotNull(sAMValidationErrorList18);
    }

    @Test
    public void test284() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test284");
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
        // The following exception was thrown during execution in test generation
        try {
            byte[] byteArray27 = sAMRecord1.getUnsignedByteArrayAttribute("null\t0\t*\t0\t0\tnull\t*\t0\t0\t*\t*\n");
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: String tag does not have length() == 2: null?0?*?0?0?null?*?0?0?*?*?");
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
    }

    @Test
    public void test285() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test285");
        htsjdk.samtools.SAMFileHeader sAMFileHeader0 = null;
        htsjdk.samtools.SAMRecord sAMRecord1 = new htsjdk.samtools.SAMRecord(sAMFileHeader0);
        sAMRecord1.setDuplicateReadFlag(false);
        java.lang.Object obj4 = null;
        boolean boolean5 = sAMRecord1.equals(obj4);
        java.util.List<htsjdk.samtools.SAMValidationError> sAMValidationErrorList7 = sAMRecord1.isValid(false);
        sAMRecord1.setMateReferenceName("hi!");
        sAMRecord1.setSecondOfPairFlag(false);
        boolean boolean12 = sAMRecord1.getSupplementaryAlignmentFlag();
        sAMRecord1.setFlags(99);
        sAMRecord1.setReadString("null\t256\t*\t*\t-1\t*\t*\t*\t*\t*\t*");
        sAMRecord1.setMappingQuality((int) (short) 1);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNotNull(sAMValidationErrorList7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test286() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test286");
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
        byte[] byteArray15 = sAMRecord13.getBaseQualities();
        java.util.List<htsjdk.samtools.AlignmentBlock> alignmentBlockList16 = sAMRecord13.getAlignmentBlocks();
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + false + "'", boolean5 == false);
        org.junit.Assert.assertNull(obj12);
        org.junit.Assert.assertNotNull(sAMRecord13);
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 0 + "'", int14 == 0);
        org.junit.Assert.assertNotNull(byteArray15);
        org.junit.Assert.assertArrayEquals(byteArray15, new byte[] {});
        org.junit.Assert.assertNotNull(alignmentBlockList16);
    }
}

