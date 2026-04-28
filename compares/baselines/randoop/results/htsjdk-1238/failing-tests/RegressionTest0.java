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
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test002() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test002");
        int int0 = htsjdk.samtools.SAMSequenceRecord.UNKNOWN_SEQUENCE_LENGTH;
        org.junit.Assert.assertTrue("'" + int0 + "' != '" + 0 + "'", int0 == 0);
    }

    @Test
    public void test003() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test003");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.URI_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "UR" + "'", str0, "UR");
    }

    @Test
    public void test004() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test004");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.RESERVED_MRNM_SEQUENCE_NAME;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "=" + "'", str0, "=");
    }

    @Test
    public void test005() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test005");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.RESERVED_RNEXT_SEQUENCE_NAME;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "=" + "'", str0, "=");
    }

    @Test
    public void test006() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test006");
        java.util.Set<java.lang.String> strSet0 = htsjdk.samtools.SAMSequenceRecord.STANDARD_TAGS;
        org.junit.Assert.assertNotNull(strSet0);
    }

    @Test
    public void test007() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test007");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.ASSEMBLY_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "AS" + "'", str0, "AS");
    }

    @Test
    public void test008() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test008");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.SEQUENCE_NAME_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "SN" + "'", str0, "SN");
    }

    @Test
    public void test009() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test009");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("UR");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "UR" + "'", str1, "UR");
    }

    @Test
    public void test010() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test010");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str7 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test011() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test011");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "" + "'", str1, "");
    }

    @Test
    public void test012() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test012");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("SN");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "SN" + "'", str1, "SN");
    }

    @Test
    public void test013() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test013");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.MD5_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "M5" + "'", str0, "M5");
    }

    @Test
    public void test014() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test014");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.DESCRIPTION_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "DS" + "'", str0, "DS");
    }

    @Test
    public void test015() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test015");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("=");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "=" + "'", str1, "=");
    }

    @Test
    public void test016() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test016");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        boolean boolean10 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord9);
        java.lang.Class<?> wildcardClass11 = sAMSequenceRecord9.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(wildcardClass11);
    }

    @Test
    public void test017() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test017");
        htsjdk.samtools.SAMSequenceRecord.validateSequenceName("SN");
    }

    @Test
    public void test018() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test018");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        java.lang.String str10 = sAMSequenceRecord2.getAssembly();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str10);
    }

    @Test
    public void test019() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test019");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setMd5("AS");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
    }

    @Test
    public void test020() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test020");
        long long0 = htsjdk.samtools.SAMSequenceRecord.serialVersionUID;
        org.junit.Assert.assertTrue("'" + long0 + "' != '" + 1L + "'", long0 == 1L);
    }

    @Test
    public void test021() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test021");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("M5");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str7 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test022() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test022");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("", (-1));
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test023() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test023");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.SPECIES_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "SP" + "'", str0, "SP");
    }

    @Test
    public void test024() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test024");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.String str4 = sAMSequenceRecord2.getAttribute("");
        org.junit.Assert.assertNull(str4);
    }

    @Test
    public void test025() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test025");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str10 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str10);
    }

    @Test
    public void test026() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test026");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        int int6 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertTrue("'" + int6 + "' != '" + 1 + "'", int6 == 1);
    }

    @Test
    public void test027() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test027");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str8 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
    }

    @Test
    public void test028() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test028");
        htsjdk.samtools.SAMSequenceRecord.validateSequenceName("DS");
    }

    @Test
    public void test029() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test029");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        sAMSequenceRecord2.setSpecies("hi!");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str18 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
    }

    @Test
    public void test030() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test030");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("=", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '=' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test031() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test031");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        java.lang.Class<?> wildcardClass7 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(wildcardClass7);
    }

    @Test
    public void test032() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test032");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord.validateSequenceName("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '@SQ?SN:UR?LN:1?M5:@SQ?SN:UR?LN:1?AS:AS' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test033() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test033");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str7 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test034() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test034");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        java.lang.String str9 = sAMSequenceRecord7.getSequenceName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "UR" + "'", str9, "UR");
    }

    @Test
    public void test035() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test035");
        java.lang.String str0 = htsjdk.samtools.SAMSequenceRecord.SEQUENCE_LENGTH_TAG;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "LN" + "'", str0, "LN");
    }

    @Test
    public void test036() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test036");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.String str18 = sAMSequenceRecord11.getDescription();
        java.lang.String str19 = sAMSequenceRecord11.getDescription();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNull(str19);
    }

    @Test
    public void test037() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test037");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.Class<?> wildcardClass7 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(wildcardClass7);
    }

    @Test
    public void test038() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test038");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        sAMSequenceRecord2.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
    }

    @Test
    public void test039() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test039");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str19 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
    }

    @Test
    public void test040() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test040");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("hi!", 10);
        int int3 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 10 + "'", int3 == 10);
    }

    @Test
    public void test041() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test041");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.Class<?> wildcardClass19 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNotNull(wildcardClass19);
    }

    @Test
    public void test042() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test042");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        sAMSequenceRecord7.setSequenceLength((int) (byte) 100);
        sAMSequenceRecord7.setSequenceIndex((int) '#');
        java.lang.Class<?> wildcardClass13 = sAMSequenceRecord7.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertNotNull(wildcardClass13);
    }

    @Test
    public void test043() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test043");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("DS");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "DS" + "'", str1, "DS");
    }

    @Test
    public void test044() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test044");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("M5");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "M5" + "'", str1, "M5");
    }

    @Test
    public void test045() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test045");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("SP", (int) '4');
    }

    @Test
    public void test046() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test046");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int21 = sAMSequenceRecord18.getSequenceIndex();
        java.lang.String str22 = sAMSequenceRecord18.getDescription();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "" + "'", str22, "");
    }

    @Test
    public void test047() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test047");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("M5");
        int int7 = sAMSequenceRecord2.getSequenceIndex();
        sAMSequenceRecord2.setMd5("");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test048() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test048");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int26 = sAMSequenceRecord25.getSequenceIndex();
        int int27 = sAMSequenceRecord25.getSequenceLength();
        java.lang.String str28 = sAMSequenceRecord25.getDescription();
        boolean boolean29 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord25);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str30 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + int27 + "' != '" + 1 + "'", int27 == 1);
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
    }

    @Test
    public void test049() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test049");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        java.lang.String str8 = sAMSequenceRecord2.getAssembly();
        java.lang.Class<?> wildcardClass9 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertNotNull(wildcardClass9);
    }

    @Test
    public void test050() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test050");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (byte) -1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + (-1) + "'", int4 == (-1));
    }

    @Test
    public void test051() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test051");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("@SQ\tSN:UR\tLN:1\tAS:AS", 1);
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '@SQ?SN:UR?LN:1?AS:AS' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test052() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test052");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str10 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test053() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test053");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        java.lang.String str21 = sAMSequenceRecord2.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str21, "@SQ\tSN:UR\tLN:1");
    }

    @Test
    public void test054() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test054");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int26 = sAMSequenceRecord25.getSequenceIndex();
        int int27 = sAMSequenceRecord25.getSequenceLength();
        java.lang.String str28 = sAMSequenceRecord25.getDescription();
        boolean boolean29 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord25);
        int int30 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + int27 + "' != '" + 1 + "'", int27 == 1);
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertTrue("'" + int30 + "' != '" + 1 + "'", int30 == 1);
    }

    @Test
    public void test055() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test055");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        sAMSequenceRecord2.setAssembly("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
    }

    @Test
    public void test056() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test056");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name 'SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test057() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test057");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str16 = sAMSequenceRecord11.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
    }

    @Test
    public void test058() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test058");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord2.setDescription("UR");
        java.lang.Class<?> wildcardClass12 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test059() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test059");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord18.setDescription("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
    }

    @Test
    public void test060() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test060");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("M5");
        int int7 = sAMSequenceRecord2.getSequenceIndex();
        java.lang.String str8 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test061() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test061");
        htsjdk.samtools.SAMSequenceRecord.validateSequenceName("UR");
    }

    @Test
    public void test062() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test062");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str23 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test063() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test063");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceLength();
        int int4 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 1 + "'", int3 == 1);
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + (-1) + "'", int4 == (-1));
    }

    @Test
    public void test064() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test064");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("UR");
    }

    @Test
    public void test065() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test065");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        boolean boolean10 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord9);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str11 = sAMSequenceRecord9.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test066() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test066");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        sAMSequenceRecord7.setSequenceLength((int) (byte) 100);
        sAMSequenceRecord7.setSequenceIndex((int) '#');
        sAMSequenceRecord7.setDescription("");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test067() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test067");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("M5", (java.lang.Object) 0.0f);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int13 = sAMSequenceRecord12.getSequenceIndex();
        int int14 = sAMSequenceRecord12.getSequenceLength();
        java.lang.String str15 = sAMSequenceRecord12.getDescription();
        java.lang.String str16 = sAMSequenceRecord12.getSequenceName();
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 1 + "'", int14 == 1);
        org.junit.Assert.assertNull(str15);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "UR" + "'", str16, "UR");
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
    }

    @Test
    public void test068() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test068");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int21 = sAMSequenceRecord18.getSequenceIndex();
        sAMSequenceRecord18.setSpecies("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
    }

    @Test
    public void test069() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test069");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        java.lang.String str7 = sAMSequenceRecord2.getSAMString();
        java.lang.String str8 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setSequenceIndex(1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str7, "@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test070() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test070");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str7 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
    }

    @Test
    public void test071() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test071");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("", (int) '4');
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test072() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test072");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str1, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test073() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test073");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
    }

    @Test
    public void test074() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test074");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str21 = sAMSequenceRecord18.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord18.getSequenceName();
        java.lang.Class<?> wildcardClass23 = sAMSequenceRecord18.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "UR" + "'", str22, "UR");
        org.junit.Assert.assertNotNull(wildcardClass23);
    }

    @Test
    public void test075() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test075");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord21.setSequenceIndex(1);
        int int32 = sAMSequenceRecord21.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertTrue("'" + int32 + "' != '" + 1 + "'", int32 == 1);
    }

    @Test
    public void test076() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test076");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("=");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '=' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test077() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test077");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setDescription("SN");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
    }

    @Test
    public void test078() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test078");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("hi!");
        sAMSequenceRecord1.setSequenceIndex((int) (short) 100);
    }

    @Test
    public void test079() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test079");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord2.getSAMString();
        sAMSequenceRecord2.setAttribute("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)", "");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str8, "@SQ\tSN:UR\tLN:1");
    }

    @Test
    public void test080() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test080");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        sAMSequenceRecord2.setAttribute("SN", "@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test081() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test081");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        java.lang.String str32 = sAMSequenceRecord2.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertEquals("'" + str32 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str32, "@SQ\tSN:UR\tLN:1");
    }

    @Test
    public void test082() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test082");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("hi!", "hi!");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
    }

    @Test
    public void test083() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test083");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.String str18 = sAMSequenceRecord11.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str18, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test084() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test084");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setSequenceLength((int) (short) 0);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
    }

    @Test
    public void test085() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test085");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        java.lang.String str7 = sAMSequenceRecord2.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord10 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMSequenceRecord10.equals(obj11);
        boolean boolean14 = sAMSequenceRecord10.equals((java.lang.Object) 100.0f);
        int int15 = sAMSequenceRecord10.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet16 = sAMSequenceRecord10.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int20 = sAMSequenceRecord19.getSequenceIndex();
        sAMSequenceRecord19.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean23 = sAMSequenceRecord10.isSameSequence(sAMSequenceRecord19);
        java.lang.String str25 = sAMSequenceRecord10.getAttribute("");
        java.lang.String str26 = sAMSequenceRecord10.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord27 = sAMSequenceRecord10.clone();
        boolean boolean28 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord10);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertTrue("'" + int15 + "' != '" + 1 + "'", int15 == 1);
        org.junit.Assert.assertNotNull(strEntrySet16);
        org.junit.Assert.assertTrue("'" + int20 + "' != '" + (-1) + "'", int20 == (-1));
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + true + "'", boolean23 == true);
        org.junit.Assert.assertNull(str25);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertNotNull(sAMSequenceRecord27);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + false + "'", boolean28 == false);
    }

    @Test
    public void test086() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test086");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("@SQ\tSN:UR\tLN:1");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '@SQ?SN:UR?LN:1' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test087() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test087");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("LN");
    }

    @Test
    public void test088() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test088");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("M5", (java.lang.Object) 0.0f);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj13 = null;
        boolean boolean14 = sAMSequenceRecord12.equals(obj13);
        sAMSequenceRecord12.setAssembly("AS");
        java.lang.String str17 = sAMSequenceRecord12.getSAMString();
        java.lang.String str18 = sAMSequenceRecord12.getDescription();
        boolean boolean19 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str17, "@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
    }

    @Test
    public void test089() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test089");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = sAMSequenceRecord2.clone();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str20 = sAMSequenceRecord19.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNotNull(sAMSequenceRecord19);
    }

    @Test
    public void test090() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test090");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet23 = sAMSequenceRecord2.getAttributes();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str24 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNotNull(strEntrySet23);
    }

    @Test
    public void test091() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test091");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceLength();
        sAMSequenceRecord2.setAttribute("SN", (java.lang.Object) 1L);
        sAMSequenceRecord2.setSequenceLength((int) 'a');
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 1 + "'", int3 == 1);
    }

    @Test
    public void test092() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test092");
        htsjdk.samtools.SAMSequenceRecord.validateSequenceName("SP");
    }

    @Test
    public void test093() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test093");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMSequenceRecord11.equals(obj12);
        sAMSequenceRecord11.setSequenceLength((int) (short) 10);
        sAMSequenceRecord11.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord11.setAttribute("", "UR");
        sAMSequenceRecord7.setAttribute("SP", (java.lang.Object) sAMSequenceRecord11);
        int int23 = sAMSequenceRecord11.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 10 + "'", int23 == 10);
    }

    @Test
    public void test094() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test094");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSequenceIndex(100);
        int int11 = sAMSequenceRecord2.getSequenceIndex();
        sAMSequenceRecord2.setMd5("=");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 100 + "'", int11 == 100);
    }

    @Test
    public void test095() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test095");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        sAMSequenceRecord2.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str6 = sAMSequenceRecord2.getAssembly();
        java.lang.String str8 = sAMSequenceRecord2.getAttribute("hi!");
        sAMSequenceRecord2.setSequenceLength(0);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertNull(str6);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test096() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test096");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord34 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj35 = null;
        boolean boolean36 = sAMSequenceRecord34.equals(obj35);
        sAMSequenceRecord34.setSequenceLength((int) (short) 10);
        sAMSequenceRecord34.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord34.setSequenceIndex(100);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord46 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj47 = null;
        boolean boolean48 = sAMSequenceRecord46.equals(obj47);
        sAMSequenceRecord46.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord53 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int54 = sAMSequenceRecord53.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord57 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj58 = null;
        boolean boolean59 = sAMSequenceRecord57.equals(obj58);
        boolean boolean60 = sAMSequenceRecord53.isSameSequence(sAMSequenceRecord57);
        boolean boolean61 = sAMSequenceRecord46.isSameSequence(sAMSequenceRecord57);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord62 = sAMSequenceRecord46.clone();
        java.lang.String str64 = sAMSequenceRecord62.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int65 = sAMSequenceRecord62.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord68 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int69 = sAMSequenceRecord68.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord72 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj73 = null;
        boolean boolean74 = sAMSequenceRecord72.equals(obj73);
        boolean boolean75 = sAMSequenceRecord68.isSameSequence(sAMSequenceRecord72);
        boolean boolean76 = sAMSequenceRecord62.isSameSequence(sAMSequenceRecord68);
        sAMSequenceRecord34.setAttribute("hi!", (java.lang.Object) boolean76);
        boolean boolean78 = sAMSequenceRecord23.equals((java.lang.Object) sAMSequenceRecord34);
        java.lang.Class<?> wildcardClass79 = sAMSequenceRecord34.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + false + "'", boolean36 == false);
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + false + "'", boolean48 == false);
        org.junit.Assert.assertTrue("'" + int54 + "' != '" + (-1) + "'", int54 == (-1));
        org.junit.Assert.assertTrue("'" + boolean59 + "' != '" + false + "'", boolean59 == false);
        org.junit.Assert.assertTrue("'" + boolean60 + "' != '" + true + "'", boolean60 == true);
        org.junit.Assert.assertTrue("'" + boolean61 + "' != '" + true + "'", boolean61 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord62);
        org.junit.Assert.assertNull(str64);
        org.junit.Assert.assertTrue("'" + int65 + "' != '" + (-1) + "'", int65 == (-1));
        org.junit.Assert.assertTrue("'" + int69 + "' != '" + (-1) + "'", int69 == (-1));
        org.junit.Assert.assertTrue("'" + boolean74 + "' != '" + false + "'", boolean74 == false);
        org.junit.Assert.assertTrue("'" + boolean75 + "' != '" + true + "'", boolean75 == true);
        org.junit.Assert.assertTrue("'" + boolean76 + "' != '" + true + "'", boolean76 == true);
        org.junit.Assert.assertTrue("'" + boolean78 + "' != '" + false + "'", boolean78 == false);
        org.junit.Assert.assertNotNull(wildcardClass79);
    }

    @Test
    public void test097() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test097");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        sAMSequenceRecord23.setSequenceIndex(1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
    }

    @Test
    public void test098() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test098");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = sAMSequenceRecord2.clone();
        int int7 = sAMSequenceRecord6.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNotNull(sAMSequenceRecord6);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
    }

    @Test
    public void test099() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test099");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        sAMSequenceRecord21.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord28 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int29 = sAMSequenceRecord28.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord32 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMSequenceRecord32.equals(obj33);
        boolean boolean35 = sAMSequenceRecord28.isSameSequence(sAMSequenceRecord32);
        boolean boolean36 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord32);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord37 = sAMSequenceRecord21.clone();
        java.lang.String str39 = sAMSequenceRecord37.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int40 = sAMSequenceRecord37.getSequenceIndex();
        boolean boolean41 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord37);
        sAMSequenceRecord2.setAttribute("LN", "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int29 + "' != '" + (-1) + "'", int29 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + true + "'", boolean36 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord37);
        org.junit.Assert.assertNull(str39);
        org.junit.Assert.assertTrue("'" + int40 + "' != '" + (-1) + "'", int40 == (-1));
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
    }

    @Test
    public void test100() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test100");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int7 = sAMSequenceRecord6.getSequenceLength();
        boolean boolean8 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + true + "'", boolean8 == true);
    }

    @Test
    public void test101() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test101");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord2.getSAMString();
        int int9 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str8, "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertTrue("'" + int9 + "' != '" + (-1) + "'", int9 == (-1));
    }

    @Test
    public void test102() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test102");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        boolean boolean25 = sAMSequenceRecord21.equals((java.lang.Object) 100.0f);
        int int26 = sAMSequenceRecord21.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet27 = sAMSequenceRecord21.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int31 = sAMSequenceRecord30.getSequenceIndex();
        sAMSequenceRecord30.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean34 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord30);
        java.lang.String str36 = sAMSequenceRecord21.getAttribute("");
        java.lang.String str37 = sAMSequenceRecord21.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord38 = sAMSequenceRecord21.clone();
        boolean boolean39 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet40 = sAMSequenceRecord21.getAttributes();
        java.lang.String str41 = sAMSequenceRecord21.getDescription();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + 1 + "'", int26 == 1);
        org.junit.Assert.assertNotNull(strEntrySet27);
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + (-1) + "'", int31 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
        org.junit.Assert.assertNull(str36);
        org.junit.Assert.assertNull(str37);
        org.junit.Assert.assertNotNull(sAMSequenceRecord38);
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + true + "'", boolean39 == true);
        org.junit.Assert.assertNotNull(strEntrySet40);
        org.junit.Assert.assertNull(str41);
    }

    @Test
    public void test103() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test103");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str32 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
    }

    @Test
    public void test104() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test104");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        java.lang.String str10 = sAMSequenceRecord6.getDescription();
        int int11 = sAMSequenceRecord6.getSequenceLength();
        int int12 = sAMSequenceRecord6.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 1 + "'", int11 == 1);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 1 + "'", int12 == 1);
    }

    @Test
    public void test105() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test105");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int21 = sAMSequenceRecord18.getSequenceLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 1 + "'", int21 == 1);
    }

    @Test
    public void test106() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test106");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "@SQ" + "'", str1, "@SQ");
    }

    @Test
    public void test107() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test107");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        java.lang.String str23 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNull(str23);
    }

    @Test
    public void test108() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test108");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("", "@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSpecies("hi!");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test109() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test109");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceLength();
        java.lang.Class<?> wildcardClass4 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 1 + "'", int3 == 1);
        org.junit.Assert.assertNotNull(wildcardClass4);
    }

    @Test
    public void test110() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test110");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("hi!", 10);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet3 = sAMSequenceRecord2.getAttributes();
        sAMSequenceRecord2.setAssembly("hi!");
        org.junit.Assert.assertNotNull(strEntrySet3);
    }

    @Test
    public void test111() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test111");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        boolean boolean25 = sAMSequenceRecord21.equals((java.lang.Object) 100.0f);
        int int26 = sAMSequenceRecord21.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet27 = sAMSequenceRecord21.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int31 = sAMSequenceRecord30.getSequenceIndex();
        sAMSequenceRecord30.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean34 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord30);
        java.lang.String str36 = sAMSequenceRecord21.getAttribute("");
        java.lang.String str37 = sAMSequenceRecord21.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord38 = sAMSequenceRecord21.clone();
        boolean boolean39 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        java.lang.String str40 = sAMSequenceRecord21.getDescription();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + 1 + "'", int26 == 1);
        org.junit.Assert.assertNotNull(strEntrySet27);
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + (-1) + "'", int31 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
        org.junit.Assert.assertNull(str36);
        org.junit.Assert.assertNull(str37);
        org.junit.Assert.assertNotNull(sAMSequenceRecord38);
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + true + "'", boolean39 == true);
        org.junit.Assert.assertNull(str40);
    }

    @Test
    public void test112() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test112");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceLength();
        sAMSequenceRecord2.setSpecies("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + 1 + "'", int3 == 1);
    }

    @Test
    public void test113() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test113");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord18.setAttribute("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)", "=");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
    }

    @Test
    public void test114() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test114");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSpecies("");
        sAMSequenceRecord2.setAssembly("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
    }

    @Test
    public void test115() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test115");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        sAMSequenceRecord2.setAssembly("UR");
        sAMSequenceRecord2.setSpecies("UR");
        int int25 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
    }

    @Test
    public void test116() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test116");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '@SQ?SN:UR?LN:1?M5:@SQ?SN:UR?LN:1?AS:AS' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test117() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test117");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMSequenceRecord11.equals(obj12);
        sAMSequenceRecord11.setSequenceLength((int) (short) 10);
        sAMSequenceRecord11.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord11.setAttribute("", "UR");
        sAMSequenceRecord7.setAttribute("SP", (java.lang.Object) sAMSequenceRecord11);
        sAMSequenceRecord7.setSequenceIndex((int) (short) -1);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
    }

    @Test
    public void test118() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test118");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.Class<?> wildcardClass10 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNotNull(wildcardClass10);
    }

    @Test
    public void test119() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test119");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setAssembly("SN");
        int int10 = sAMSequenceRecord2.getSequenceIndex();
        java.lang.String str12 = sAMSequenceRecord2.getAttribute("SN");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertNull(str12);
    }

    @Test
    public void test120() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test120");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord19.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNotNull(sAMSequenceRecord19);
        org.junit.Assert.assertEquals("'" + str20 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str20, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test121() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test121");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int13 = sAMSequenceRecord12.getSequenceIndex();
        int int14 = sAMSequenceRecord12.getSequenceLength();
        java.lang.String str15 = sAMSequenceRecord12.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord16 = sAMSequenceRecord12.clone();
        sAMSequenceRecord2.setAttribute("@SQ\tSN:UR\tLN:1", (java.lang.Object) sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 1 + "'", int14 == 1);
        org.junit.Assert.assertNull(str15);
        org.junit.Assert.assertNotNull(sAMSequenceRecord16);
    }

    @Test
    public void test122() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test122");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        java.lang.String str8 = sAMSequenceRecord2.getAttribute("=");
        sAMSequenceRecord2.setMd5("hi!");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str11 = sAMSequenceRecord2.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test123() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test123");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        java.lang.String str7 = sAMSequenceRecord2.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord8 = sAMSequenceRecord2.clone();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertNotNull(sAMSequenceRecord8);
    }

    @Test
    public void test124() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test124");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        java.lang.String str19 = sAMSequenceRecord2.toString();
        java.lang.String str20 = sAMSequenceRecord2.getDescription();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str19, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNull(str20);
    }

    @Test
    public void test125() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test125");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        java.lang.String str10 = sAMSequenceRecord2.toString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertEquals("'" + str10 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str10, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test126() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test126");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        java.lang.String str31 = sAMSequenceRecord21.getAttribute("hi!");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str32 = sAMSequenceRecord21.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertNull(str31);
    }

    @Test
    public void test127() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test127");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSpecies("");
        java.lang.Object obj9 = null;
        boolean boolean10 = sAMSequenceRecord2.equals(obj9);
        int int11 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + 1 + "'", int11 == 1);
    }

    @Test
    public void test128() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test128");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSequenceLength((int) (byte) 0);
        java.lang.Class<?> wildcardClass12 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test129() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test129");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setAssembly("SN");
        int int10 = sAMSequenceRecord2.getSequenceIndex();
        sAMSequenceRecord2.setSequenceIndex((int) 'a');
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
    }

    @Test
    public void test130() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test130");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.Class<?> wildcardClass18 = sAMSequenceRecord11.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertNotNull(wildcardClass18);
    }

    @Test
    public void test131() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test131");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        java.lang.String str19 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNull(str19);
    }

    @Test
    public void test132() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test132");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = sAMSequenceRecord2.clone();
        sAMSequenceRecord19.setSequenceIndex((-1));
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNotNull(sAMSequenceRecord19);
    }

    @Test
    public void test133() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test133");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        java.lang.String str19 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setSpecies("");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str19, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test134() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test134");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int26 = sAMSequenceRecord25.getSequenceIndex();
        int int27 = sAMSequenceRecord25.getSequenceLength();
        java.lang.String str28 = sAMSequenceRecord25.getDescription();
        boolean boolean29 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord25);
        java.lang.Object obj31 = null;
        sAMSequenceRecord2.setAttribute("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)", obj31);
        int int33 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + (-1) + "'", int26 == (-1));
        org.junit.Assert.assertTrue("'" + int27 + "' != '" + 1 + "'", int27 == 1);
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertTrue("'" + int33 + "' != '" + (-1) + "'", int33 == (-1));
    }

    @Test
    public void test135() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test135");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("SN", (int) ' ');
    }

    @Test
    public void test136() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test136");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int21 = sAMSequenceRecord18.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord24 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int25 = sAMSequenceRecord24.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord28 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj29 = null;
        boolean boolean30 = sAMSequenceRecord28.equals(obj29);
        boolean boolean31 = sAMSequenceRecord24.isSameSequence(sAMSequenceRecord28);
        boolean boolean32 = sAMSequenceRecord18.isSameSequence(sAMSequenceRecord24);
        java.lang.String str33 = sAMSequenceRecord24.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + (-1) + "'", int25 == (-1));
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + true + "'", boolean31 == true);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
        org.junit.Assert.assertNull(str33);
    }

    @Test
    public void test137() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test137");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord5 = sAMSequenceRecord2.clone();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet6 = sAMSequenceRecord2.getAttributes();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet7 = sAMSequenceRecord2.getAttributes();
        java.lang.String str8 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNotNull(sAMSequenceRecord5);
        org.junit.Assert.assertNotNull(strEntrySet6);
        org.junit.Assert.assertNotNull(strEntrySet7);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test138() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test138");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.String str18 = sAMSequenceRecord11.getDescription();
        sAMSequenceRecord11.setAttribute("=", "SN");
        sAMSequenceRecord11.setAttribute("M5", "=");
        java.lang.String str25 = sAMSequenceRecord11.getAssembly();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNull(str25);
    }

    @Test
    public void test139() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test139");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        sAMSequenceRecord7.setSequenceLength((int) (byte) 100);
        int int11 = sAMSequenceRecord7.getSequenceIndex();
        java.lang.String str12 = sAMSequenceRecord7.getDescription();
        int int13 = sAMSequenceRecord7.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + (-1) + "'", int11 == (-1));
        org.junit.Assert.assertNull(str12);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
    }

    @Test
    public void test140() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test140");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        java.lang.String str10 = sAMSequenceRecord2.getDescription();
        java.lang.String str12 = sAMSequenceRecord2.getAttribute("@SQ");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertNull(str12);
    }

    @Test
    public void test141() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test141");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (short) -1);
        sAMSequenceRecord11.setAttribute("AS", (java.lang.Object) (short) -1);
        java.lang.String str21 = sAMSequenceRecord11.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS\tAS:-1" + "'", str21, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS\tAS:-1");
    }

    @Test
    public void test142() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test142");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        sAMSequenceRecord2.setSpecies("=");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (short) -1);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord15 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj16 = null;
        boolean boolean17 = sAMSequenceRecord15.equals(obj16);
        sAMSequenceRecord15.setSequenceLength((int) (short) 10);
        sAMSequenceRecord15.setAttribute("hi!", (java.lang.Object) 0L);
        java.lang.String str23 = sAMSequenceRecord15.getDescription();
        boolean boolean24 = sAMSequenceRecord12.isSameSequence(sAMSequenceRecord15);
        sAMSequenceRecord2.setAttribute("", (java.lang.Object) sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
        org.junit.Assert.assertNull(str23);
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
    }

    @Test
    public void test143() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test143");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (byte) -1);
        java.lang.Class<?> wildcardClass3 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertNotNull(wildcardClass3);
    }

    @Test
    public void test144() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test144");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord21.setSequenceIndex(1);
        sAMSequenceRecord21.setSpecies("hi!");
        sAMSequenceRecord21.setSequenceLength((int) (short) 10);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
    }

    @Test
    public void test145() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test145");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.String str18 = sAMSequenceRecord11.getDescription();
        sAMSequenceRecord11.setAttribute("M5", "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertNull(str18);
    }

    @Test
    public void test146() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test146");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (short) -1);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord5 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj6 = null;
        boolean boolean7 = sAMSequenceRecord5.equals(obj6);
        sAMSequenceRecord5.setSequenceLength((int) (short) 10);
        sAMSequenceRecord5.setAttribute("hi!", (java.lang.Object) 0L);
        java.lang.String str13 = sAMSequenceRecord5.getDescription();
        boolean boolean14 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord5);
        java.lang.String str15 = sAMSequenceRecord2.getSpecies();
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
        org.junit.Assert.assertNull(str13);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNull(str15);
    }

    @Test
    public void test147() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test147");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setDescription("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        sAMSequenceRecord2.setSpecies("@SQ\tSN:UR\tLN:1");
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet12 = sAMSequenceRecord2.getAttributes();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertNotNull(strEntrySet12);
    }

    @Test
    public void test148() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test148");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        boolean boolean10 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord9);
        java.lang.String str11 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("=", (java.lang.Object) (byte) 100);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet15 = sAMSequenceRecord2.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)" + "'", str11, "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNotNull(strEntrySet15);
    }

    @Test
    public void test149() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test149");
        htsjdk.samtools.SAMSequenceRecord.validateSequenceName("hi!");
    }

    @Test
    public void test150() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test150");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.String str18 = sAMSequenceRecord11.getDescription();
        sAMSequenceRecord11.setAttribute("=", "SN");
        sAMSequenceRecord11.setAttribute("M5", "=");
        sAMSequenceRecord11.setSequenceLength((int) (byte) 0);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertNull(str18);
    }

    @Test
    public void test151() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test151");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord.validateSequenceName("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name 'SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test152() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test152");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setAssembly("SN");
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet10 = sAMSequenceRecord2.getAttributes();
        java.lang.String str11 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord14 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj15 = null;
        boolean boolean16 = sAMSequenceRecord14.equals(obj15);
        sAMSequenceRecord14.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord14.isSameSequence(sAMSequenceRecord25);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = sAMSequenceRecord14.clone();
        java.lang.String str31 = sAMSequenceRecord30.getAssembly();
        boolean boolean32 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord30);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertNotNull(strEntrySet10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)" + "'", str11, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)");
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + true + "'", boolean29 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord30);
        org.junit.Assert.assertNull(str31);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
    }

    @Test
    public void test153() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test153");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        java.lang.String str19 = sAMSequenceRecord13.getSequenceName();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "UR" + "'", str19, "UR");
    }

    @Test
    public void test154() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test154");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        sAMSequenceRecord2.setAttribute("AS", "LN");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
    }

    @Test
    public void test155() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test155");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("@SQ");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "@SQ" + "'", str1, "@SQ");
    }

    @Test
    public void test156() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test156");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("LN");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "LN" + "'", str1, "LN");
    }

    @Test
    public void test157() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test157");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int21 = sAMSequenceRecord18.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord24 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int25 = sAMSequenceRecord24.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord28 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj29 = null;
        boolean boolean30 = sAMSequenceRecord28.equals(obj29);
        boolean boolean31 = sAMSequenceRecord24.isSameSequence(sAMSequenceRecord28);
        boolean boolean32 = sAMSequenceRecord18.isSameSequence(sAMSequenceRecord24);
        java.lang.Class<?> wildcardClass33 = sAMSequenceRecord24.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + (-1) + "'", int25 == (-1));
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + true + "'", boolean31 == true);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
        org.junit.Assert.assertNotNull(wildcardClass33);
    }

    @Test
    public void test158() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test158");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet16 = sAMSequenceRecord11.getAttributes();
        int int17 = sAMSequenceRecord11.getSequenceLength();
        java.lang.String str18 = sAMSequenceRecord11.getSpecies();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(strEntrySet16);
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + 1 + "'", int17 == 1);
        org.junit.Assert.assertNull(str18);
    }

    @Test
    public void test159() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test159");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        java.lang.String str10 = sAMSequenceRecord6.getDescription();
        java.lang.String str11 = sAMSequenceRecord6.getMd5();
        sAMSequenceRecord6.setSequenceLength((int) (short) -1);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord14 = sAMSequenceRecord6.clone();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertNull(str11);
        org.junit.Assert.assertNotNull(sAMSequenceRecord14);
    }

    @Test
    public void test160() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test160");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        sAMSequenceRecord2.setAttribute("@SQ\tSN:UR\tLN:1\tAS:AS", "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSequenceIndex(0);
        java.lang.Class<?> wildcardClass23 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNotNull(wildcardClass23);
    }

    @Test
    public void test161() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test161");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        java.lang.String str8 = sAMSequenceRecord2.getAssembly();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = null;
        boolean boolean10 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord9);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test162() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test162");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        sAMSequenceRecord2.setSpecies("=");
        java.lang.String str9 = sAMSequenceRecord2.getAssembly();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "AS" + "'", str9, "AS");
    }

    @Test
    public void test163() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test163");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
    }

    @Test
    public void test164() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test164");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (byte) -1);
        java.lang.String str3 = sAMSequenceRecord2.getMd5();
        java.lang.String str4 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord5 = sAMSequenceRecord2.clone();
        org.junit.Assert.assertNull(str3);
        org.junit.Assert.assertEquals("'" + str4 + "' != '" + "DS" + "'", str4, "DS");
        org.junit.Assert.assertNotNull(sAMSequenceRecord5);
    }

    @Test
    public void test165() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test165");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "@SQ" + "'", str1, "@SQ");
    }

    @Test
    public void test166() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test166");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        int int10 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str12 = sAMSequenceRecord2.getAttribute("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + 10 + "'", int10 == 10);
        org.junit.Assert.assertNull(str12);
    }

    @Test
    public void test167() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test167");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("M5");
        sAMSequenceRecord2.setAssembly("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        sAMSequenceRecord2.setMd5("=");
        java.lang.String str12 = sAMSequenceRecord2.getAttribute("UR");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str12);
    }

    @Test
    public void test168() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test168");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        sAMSequenceRecord2.setAttribute("", (java.lang.Object) ' ');
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
    }

    @Test
    public void test169() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test169");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        boolean boolean10 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord9);
        java.lang.String str11 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("=", (java.lang.Object) (byte) 100);
        sAMSequenceRecord2.setAssembly("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSpecies("hi!");
        java.lang.Class<?> wildcardClass19 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)" + "'", str11, "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNotNull(wildcardClass19);
    }

    @Test
    public void test170() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test170");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord2.getSAMString();
        java.lang.String str9 = sAMSequenceRecord2.getSequenceName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str8, "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "UR" + "'", str9, "UR");
    }

    @Test
    public void test171() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test171");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord2.getSAMString();
        java.lang.String str9 = sAMSequenceRecord2.getAssembly();
        sAMSequenceRecord2.setDescription("SN");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str8, "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertNull(str9);
    }

    @Test
    public void test172() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test172");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSequenceIndex(100);
        sAMSequenceRecord2.setAssembly("hi!");
        sAMSequenceRecord2.setSequenceIndex((int) (short) 100);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test173() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test173");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        java.lang.String str8 = sAMSequenceRecord2.getAttribute("AS");
        java.lang.String str10 = sAMSequenceRecord2.getAttribute("");
        sAMSequenceRecord2.setAssembly("UR");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "AS" + "'", str8, "AS");
        org.junit.Assert.assertNull(str10);
    }

    @Test
    public void test174() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test174");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord.validateSequenceName("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name 'SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test175() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test175");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (byte) -1);
        java.lang.String str3 = sAMSequenceRecord2.getMd5();
        java.lang.String str4 = sAMSequenceRecord2.getSequenceName();
        sAMSequenceRecord2.setSequenceLength((int) (short) -1);
        java.lang.String str7 = sAMSequenceRecord2.getSpecies();
        org.junit.Assert.assertNull(str3);
        org.junit.Assert.assertEquals("'" + str4 + "' != '" + "DS" + "'", str4, "DS");
        org.junit.Assert.assertNull(str7);
    }

    @Test
    public void test176() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test176");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSpecies("");
        java.lang.String str9 = sAMSequenceRecord2.getSAMString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "@SQ\tSN:UR\tLN:1\tSP:" + "'", str9, "@SQ\tSN:UR\tLN:1\tSP:");
    }

    @Test
    public void test177() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test177");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        sAMSequenceRecord7.setSequenceLength((int) (byte) 100);
        int int11 = sAMSequenceRecord7.getSequenceIndex();
        java.lang.String str12 = sAMSequenceRecord7.getDescription();
        java.lang.String str13 = sAMSequenceRecord7.getMd5();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + (-1) + "'", int11 == (-1));
        org.junit.Assert.assertNull(str12);
        org.junit.Assert.assertNull(str13);
    }

    @Test
    public void test178() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test178");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord18.setAssembly("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
    }

    @Test
    public void test179() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test179");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        java.lang.String str7 = sAMSequenceRecord2.getMd5();
        sAMSequenceRecord2.setMd5("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null))");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str7);
    }

    @Test
    public void test180() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test180");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        sAMSequenceRecord2.setAssembly("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS\tAS:-1");
        int int10 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
    }

    @Test
    public void test181() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test181");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord18.setMd5("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord34 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int35 = sAMSequenceRecord34.getSequenceIndex();
        int int36 = sAMSequenceRecord34.getSequenceLength();
        java.lang.String str37 = sAMSequenceRecord34.getDescription();
        java.lang.String str38 = sAMSequenceRecord34.getSequenceName();
        boolean boolean39 = sAMSequenceRecord18.isSameSequence(sAMSequenceRecord34);
        java.lang.String str40 = sAMSequenceRecord34.getDescription();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertTrue("'" + int35 + "' != '" + (-1) + "'", int35 == (-1));
        org.junit.Assert.assertTrue("'" + int36 + "' != '" + 1 + "'", int36 == 1);
        org.junit.Assert.assertNull(str37);
        org.junit.Assert.assertEquals("'" + str38 + "' != '" + "UR" + "'", str38, "UR");
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + true + "'", boolean39 == true);
        org.junit.Assert.assertNull(str40);
    }

    @Test
    public void test182() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test182");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet18 = sAMSequenceRecord13.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord22 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int23 = sAMSequenceRecord22.getSequenceIndex();
        sAMSequenceRecord22.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord13.setAttribute("SP", (java.lang.Object) sAMSequenceRecord22);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(strEntrySet18);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + (-1) + "'", int23 == (-1));
    }

    @Test
    public void test183() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test183");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord2.setAttribute("", "UR");
        int int13 = sAMSequenceRecord2.getSequenceIndex();
        int int14 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str16 = sAMSequenceRecord2.getAttribute("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 10 + "'", int14 == 10);
        org.junit.Assert.assertNull(str16);
    }

    @Test
    public void test184() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test184");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("", "@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str26 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord29 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj30 = null;
        boolean boolean31 = sAMSequenceRecord29.equals(obj30);
        sAMSequenceRecord29.setAssembly("M5");
        sAMSequenceRecord29.setAssembly("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        sAMSequenceRecord29.setSpecies("");
        java.lang.String str38 = sAMSequenceRecord29.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord41 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj42 = null;
        boolean boolean43 = sAMSequenceRecord41.equals(obj42);
        sAMSequenceRecord41.setSequenceLength((int) (short) 10);
        sAMSequenceRecord41.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord41.setAttribute("", "UR");
        int int52 = sAMSequenceRecord41.getSequenceIndex();
        java.lang.String str53 = sAMSequenceRecord41.toString();
        boolean boolean54 = sAMSequenceRecord29.isSameSequence(sAMSequenceRecord41);
        boolean boolean55 = sAMSequenceRecord2.equals((java.lang.Object) boolean54);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertEquals("'" + str26 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str26, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertEquals("'" + str38 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null))" + "'", str38, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null))");
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + false + "'", boolean43 == false);
        org.junit.Assert.assertTrue("'" + int52 + "' != '" + (-1) + "'", int52 == (-1));
        org.junit.Assert.assertEquals("'" + str53 + "' != '" + "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)" + "'", str53, "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + boolean54 + "' != '" + false + "'", boolean54 == false);
        org.junit.Assert.assertTrue("'" + boolean55 + "' != '" + false + "'", boolean55 == false);
    }

    @Test
    public void test185() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test185");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("AS");
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet2 = sAMSequenceRecord1.getAttributes();
        org.junit.Assert.assertNotNull(strEntrySet2);
    }

    @Test
    public void test186() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test186");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord2.setSequenceLength((int) (byte) 0);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test187() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test187");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        sAMSequenceRecord2.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str6 = sAMSequenceRecord2.getAssembly();
        java.lang.String str8 = sAMSequenceRecord2.getAttribute("hi!");
        java.lang.String str9 = sAMSequenceRecord2.getSpecies();
        java.lang.String str11 = sAMSequenceRecord2.getAttribute("SP");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertNull(str6);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertNull(str9);
        org.junit.Assert.assertNull(str11);
    }

    @Test
    public void test188() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test188");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord2.getSAMString();
        sAMSequenceRecord2.setSequenceIndex((-1));
        sAMSequenceRecord2.setAttribute("SN", "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS\tAS:-1");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str8, "@SQ\tSN:UR\tLN:1");
    }

    @Test
    public void test189() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test189");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        java.lang.String str8 = sAMSequenceRecord2.toString();
        java.lang.String str9 = sAMSequenceRecord2.getSequenceName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str8, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "UR" + "'", str9, "UR");
    }

    @Test
    public void test190() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test190");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str21 = sAMSequenceRecord18.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord18.getSequenceName();
        int int23 = sAMSequenceRecord18.getSequenceIndex();
        sAMSequenceRecord18.setSequenceIndex((int) (short) 100);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "UR" + "'", str22, "UR");
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + (-1) + "'", int23 == (-1));
    }

    @Test
    public void test191() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test191");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        java.lang.String str6 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
    }

    @Test
    public void test192() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test192");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        sAMSequenceRecord2.setAssembly("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test193() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test193");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord18.setMd5("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord34 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int35 = sAMSequenceRecord34.getSequenceIndex();
        int int36 = sAMSequenceRecord34.getSequenceLength();
        java.lang.String str37 = sAMSequenceRecord34.getDescription();
        java.lang.String str38 = sAMSequenceRecord34.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord39 = sAMSequenceRecord34.clone();
        sAMSequenceRecord34.setDescription("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord34.setSequenceLength((int) (byte) 0);
        sAMSequenceRecord34.setSpecies("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean46 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord34);
        sAMSequenceRecord18.setSequenceIndex((int) (short) 0);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertTrue("'" + int35 + "' != '" + (-1) + "'", int35 == (-1));
        org.junit.Assert.assertTrue("'" + int36 + "' != '" + 1 + "'", int36 == 1);
        org.junit.Assert.assertNull(str37);
        org.junit.Assert.assertEquals("'" + str38 + "' != '" + "UR" + "'", str38, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord39);
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + false + "'", boolean46 == false);
    }

    @Test
    public void test194() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test194");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord21.setSequenceIndex(1);
        sAMSequenceRecord21.setSpecies("hi!");
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet34 = sAMSequenceRecord21.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertNotNull(strEntrySet34);
    }

    @Test
    public void test195() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test195");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord34 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj35 = null;
        boolean boolean36 = sAMSequenceRecord34.equals(obj35);
        sAMSequenceRecord34.setSequenceLength((int) (short) 10);
        sAMSequenceRecord34.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord34.setSequenceIndex(100);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord46 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj47 = null;
        boolean boolean48 = sAMSequenceRecord46.equals(obj47);
        sAMSequenceRecord46.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord53 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int54 = sAMSequenceRecord53.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord57 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj58 = null;
        boolean boolean59 = sAMSequenceRecord57.equals(obj58);
        boolean boolean60 = sAMSequenceRecord53.isSameSequence(sAMSequenceRecord57);
        boolean boolean61 = sAMSequenceRecord46.isSameSequence(sAMSequenceRecord57);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord62 = sAMSequenceRecord46.clone();
        java.lang.String str64 = sAMSequenceRecord62.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int65 = sAMSequenceRecord62.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord68 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int69 = sAMSequenceRecord68.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord72 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj73 = null;
        boolean boolean74 = sAMSequenceRecord72.equals(obj73);
        boolean boolean75 = sAMSequenceRecord68.isSameSequence(sAMSequenceRecord72);
        boolean boolean76 = sAMSequenceRecord62.isSameSequence(sAMSequenceRecord68);
        sAMSequenceRecord34.setAttribute("hi!", (java.lang.Object) boolean76);
        boolean boolean78 = sAMSequenceRecord23.equals((java.lang.Object) sAMSequenceRecord34);
        java.lang.String str79 = sAMSequenceRecord34.getSequenceName();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + false + "'", boolean36 == false);
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + false + "'", boolean48 == false);
        org.junit.Assert.assertTrue("'" + int54 + "' != '" + (-1) + "'", int54 == (-1));
        org.junit.Assert.assertTrue("'" + boolean59 + "' != '" + false + "'", boolean59 == false);
        org.junit.Assert.assertTrue("'" + boolean60 + "' != '" + true + "'", boolean60 == true);
        org.junit.Assert.assertTrue("'" + boolean61 + "' != '" + true + "'", boolean61 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord62);
        org.junit.Assert.assertNull(str64);
        org.junit.Assert.assertTrue("'" + int65 + "' != '" + (-1) + "'", int65 == (-1));
        org.junit.Assert.assertTrue("'" + int69 + "' != '" + (-1) + "'", int69 == (-1));
        org.junit.Assert.assertTrue("'" + boolean74 + "' != '" + false + "'", boolean74 == false);
        org.junit.Assert.assertTrue("'" + boolean75 + "' != '" + true + "'", boolean75 == true);
        org.junit.Assert.assertTrue("'" + boolean76 + "' != '" + true + "'", boolean76 == true);
        org.junit.Assert.assertTrue("'" + boolean78 + "' != '" + false + "'", boolean78 == false);
        org.junit.Assert.assertEquals("'" + str79 + "' != '" + "UR" + "'", str79, "UR");
    }

    @Test
    public void test196() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test196");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = sAMSequenceRecord2.clone();
        java.lang.String str24 = sAMSequenceRecord23.getAssembly();
        java.lang.String str25 = sAMSequenceRecord23.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNotNull(sAMSequenceRecord23);
        org.junit.Assert.assertNull(str24);
        org.junit.Assert.assertEquals("'" + str25 + "' != '" + "@SQ\tSN:UR\tLN:1\tDS:\tSN:=" + "'", str25, "@SQ\tSN:UR\tLN:1\tDS:\tSN:=");
    }

    @Test
    public void test197() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test197");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("", "@SQ\tSN:UR\tLN:1\tAS:AS");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord28 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj29 = null;
        boolean boolean30 = sAMSequenceRecord28.equals(obj29);
        sAMSequenceRecord28.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord35 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int36 = sAMSequenceRecord35.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord39 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj40 = null;
        boolean boolean41 = sAMSequenceRecord39.equals(obj40);
        boolean boolean42 = sAMSequenceRecord35.isSameSequence(sAMSequenceRecord39);
        boolean boolean43 = sAMSequenceRecord28.isSameSequence(sAMSequenceRecord39);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord44 = sAMSequenceRecord28.clone();
        java.lang.String str46 = sAMSequenceRecord44.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str47 = sAMSequenceRecord44.getSequenceName();
        java.lang.String str48 = sAMSequenceRecord44.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord49 = sAMSequenceRecord44.clone();
        boolean boolean50 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord44);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertTrue("'" + int36 + "' != '" + (-1) + "'", int36 == (-1));
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + false + "'", boolean41 == false);
        org.junit.Assert.assertTrue("'" + boolean42 + "' != '" + true + "'", boolean42 == true);
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord44);
        org.junit.Assert.assertNull(str46);
        org.junit.Assert.assertEquals("'" + str47 + "' != '" + "UR" + "'", str47, "UR");
        org.junit.Assert.assertEquals("'" + str48 + "' != '" + "UR" + "'", str48, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord49);
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
    }

    @Test
    public void test198() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test198");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet16 = sAMSequenceRecord11.getAttributes();
        sAMSequenceRecord11.setAttribute("UR", "=");
        sAMSequenceRecord11.setSequenceLength(1);
        java.lang.String str22 = sAMSequenceRecord11.getDescription();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet23 = sAMSequenceRecord11.getAttributes();
        java.lang.String str24 = sAMSequenceRecord11.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(strEntrySet16);
        org.junit.Assert.assertNull(str22);
        org.junit.Assert.assertNotNull(strEntrySet23);
        org.junit.Assert.assertEquals("'" + str24 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str24, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test199() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test199");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        sAMSequenceRecord2.setAssembly("UR");
        int int23 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + 35 + "'", int23 == 35);
    }

    @Test
    public void test200() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test200");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("@SQ\tSN:UR\tLN:1\tSP:");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '@SQ?SN:UR?LN:1?SP:' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test201() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test201");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str19 = sAMSequenceRecord2.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str19, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test202() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test202");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int21 = sAMSequenceRecord18.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord24 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int25 = sAMSequenceRecord24.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord28 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj29 = null;
        boolean boolean30 = sAMSequenceRecord28.equals(obj29);
        boolean boolean31 = sAMSequenceRecord24.isSameSequence(sAMSequenceRecord28);
        boolean boolean32 = sAMSequenceRecord18.isSameSequence(sAMSequenceRecord24);
        sAMSequenceRecord18.setAttribute("@SQ\tSN:UR\tLN:1\tDS:\tSN:=", (java.lang.Object) "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + (-1) + "'", int25 == (-1));
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + false + "'", boolean30 == false);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + true + "'", boolean31 == true);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
    }

    @Test
    public void test203() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test203");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord2.getMd5();
        int int21 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord24 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj25 = null;
        boolean boolean26 = sAMSequenceRecord24.equals(obj25);
        boolean boolean28 = sAMSequenceRecord24.equals((java.lang.Object) 100.0f);
        int int29 = sAMSequenceRecord24.getSequenceIndex();
        java.lang.String str30 = sAMSequenceRecord24.getDescription();
        java.lang.String str31 = sAMSequenceRecord24.getSAMString();
        boolean boolean32 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord24);
        java.lang.String str33 = sAMSequenceRecord2.getAssembly();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNotNull(sAMSequenceRecord19);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + false + "'", boolean28 == false);
        org.junit.Assert.assertTrue("'" + int29 + "' != '" + (-1) + "'", int29 == (-1));
        org.junit.Assert.assertNull(str30);
        org.junit.Assert.assertEquals("'" + str31 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str31, "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
        org.junit.Assert.assertNull(str33);
    }

    @Test
    public void test204() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test204");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        java.lang.String str10 = sAMSequenceRecord6.getDescription();
        java.lang.String str11 = sAMSequenceRecord6.getMd5();
        sAMSequenceRecord6.setSequenceLength((int) (short) -1);
        sAMSequenceRecord6.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertNull(str11);
    }

    @Test
    public void test205() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test205");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        boolean boolean8 = sAMSequenceRecord2.equals((java.lang.Object) (short) 1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test206() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test206");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet16 = sAMSequenceRecord11.getAttributes();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(strEntrySet16);
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
    }

    @Test
    public void test207() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test207");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMSequenceRecord11.equals(obj12);
        sAMSequenceRecord11.setSequenceLength((int) (short) 10);
        sAMSequenceRecord11.setAttribute("hi!", (java.lang.Object) 0L);
        sAMSequenceRecord11.setAttribute("", "UR");
        sAMSequenceRecord7.setAttribute("SP", (java.lang.Object) sAMSequenceRecord11);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        sAMSequenceRecord25.setSequenceLength((int) (short) 10);
        sAMSequenceRecord25.setAttribute("M5", (java.lang.Object) 0.0f);
        boolean boolean33 = sAMSequenceRecord11.isSameSequence(sAMSequenceRecord25);
        java.lang.String str34 = sAMSequenceRecord25.toString();
        java.lang.String str35 = sAMSequenceRecord25.getMd5();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertEquals("'" + str34 + "' != '" + "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)" + "'", str34, "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        org.junit.Assert.assertEquals("'" + str35 + "' != '" + "0.0" + "'", str35, "0.0");
    }

    @Test
    public void test208() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test208");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("M5");
    }

    @Test
    public void test209() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test209");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        java.lang.String str7 = sAMSequenceRecord2.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord10 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj11 = null;
        boolean boolean12 = sAMSequenceRecord10.equals(obj11);
        sAMSequenceRecord10.setAssembly("AS");
        java.lang.String str15 = sAMSequenceRecord10.getSAMString();
        sAMSequenceRecord10.setSpecies("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        int int18 = sAMSequenceRecord10.getSequenceLength();
        boolean boolean19 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord10);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str15, "@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + 1 + "'", int18 == 1);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
    }

    @Test
    public void test210() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test210");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int13 = sAMSequenceRecord12.getSequenceIndex();
        sAMSequenceRecord12.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean16 = sAMSequenceRecord6.isSameSequence(sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
    }

    @Test
    public void test211() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test211");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        sAMSequenceRecord7.setSequenceLength((int) (byte) 100);
        int int11 = sAMSequenceRecord7.getSequenceIndex();
        int int12 = sAMSequenceRecord7.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertTrue("'" + int11 + "' != '" + (-1) + "'", int11 == (-1));
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + 100 + "'", int12 == 100);
    }

    @Test
    public void test212() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test212");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord2.getMd5();
        int int21 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord24 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj25 = null;
        boolean boolean26 = sAMSequenceRecord24.equals(obj25);
        boolean boolean28 = sAMSequenceRecord24.equals((java.lang.Object) 100.0f);
        int int29 = sAMSequenceRecord24.getSequenceIndex();
        java.lang.String str30 = sAMSequenceRecord24.getDescription();
        java.lang.String str31 = sAMSequenceRecord24.getSAMString();
        boolean boolean32 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord24);
        int int33 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNotNull(sAMSequenceRecord19);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + (-1) + "'", int21 == (-1));
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + false + "'", boolean28 == false);
        org.junit.Assert.assertTrue("'" + int29 + "' != '" + (-1) + "'", int29 == (-1));
        org.junit.Assert.assertNull(str30);
        org.junit.Assert.assertEquals("'" + str31 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str31, "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
        org.junit.Assert.assertTrue("'" + int33 + "' != '" + 1 + "'", int33 == 1);
    }

    @Test
    public void test213() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test213");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj13 = null;
        boolean boolean14 = sAMSequenceRecord12.equals(obj13);
        sAMSequenceRecord12.setSequenceLength((int) (short) 10);
        java.lang.String str17 = sAMSequenceRecord12.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord20 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj21 = null;
        boolean boolean22 = sAMSequenceRecord20.equals(obj21);
        sAMSequenceRecord20.setSequenceLength((int) (short) 10);
        sAMSequenceRecord20.setAttribute("hi!", (java.lang.Object) 0L);
        boolean boolean28 = sAMSequenceRecord12.equals((java.lang.Object) sAMSequenceRecord20);
        boolean boolean29 = sAMSequenceRecord9.equals((java.lang.Object) sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertNotNull(sAMSequenceRecord9);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + false + "'", boolean22 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + false + "'", boolean28 == false);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
    }

    @Test
    public void test214() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test214");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord5 = sAMSequenceRecord2.clone();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet6 = sAMSequenceRecord2.getAttributes();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet7 = sAMSequenceRecord2.getAttributes();
        java.lang.String str8 = sAMSequenceRecord2.getAssembly();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNotNull(sAMSequenceRecord5);
        org.junit.Assert.assertNotNull(strEntrySet6);
        org.junit.Assert.assertNotNull(strEntrySet7);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test215() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test215");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        sAMSequenceRecord13.setSequenceLength((int) ' ');
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
    }

    @Test
    public void test216() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test216");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("SP");
    }

    @Test
    public void test217() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test217");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        java.lang.String str10 = sAMSequenceRecord6.getDescription();
        sAMSequenceRecord6.setDescription("UR");
        java.lang.Class<?> wildcardClass13 = sAMSequenceRecord6.getClass();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertNotNull(wildcardClass13);
    }

    @Test
    public void test218() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test218");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test219() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test219");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("M5");
        sAMSequenceRecord2.setAssembly("SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
        sAMSequenceRecord2.setMd5("=");
        sAMSequenceRecord2.setSequenceLength((int) (byte) 1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test220() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test220");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = sAMSequenceRecord2.clone();
        java.lang.String str10 = sAMSequenceRecord2.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertNotNull(sAMSequenceRecord9);
        org.junit.Assert.assertNull(str10);
    }

    @Test
    public void test221() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test221");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        sAMSequenceRecord21.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord28 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int29 = sAMSequenceRecord28.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord32 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj33 = null;
        boolean boolean34 = sAMSequenceRecord32.equals(obj33);
        boolean boolean35 = sAMSequenceRecord28.isSameSequence(sAMSequenceRecord32);
        boolean boolean36 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord32);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord37 = sAMSequenceRecord21.clone();
        java.lang.String str39 = sAMSequenceRecord37.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int40 = sAMSequenceRecord37.getSequenceIndex();
        boolean boolean41 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord37);
        java.lang.String str43 = sAMSequenceRecord37.getAttribute("AS");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str44 = sAMSequenceRecord37.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + int29 + "' != '" + (-1) + "'", int29 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + true + "'", boolean36 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord37);
        org.junit.Assert.assertNull(str39);
        org.junit.Assert.assertTrue("'" + int40 + "' != '" + (-1) + "'", int40 == (-1));
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNull(str43);
    }

    @Test
    public void test222() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test222");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj12 = null;
        boolean boolean13 = sAMSequenceRecord11.equals(obj12);
        java.lang.String str14 = sAMSequenceRecord11.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord15 = sAMSequenceRecord11.clone();
        boolean boolean16 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + false + "'", boolean13 == false);
        org.junit.Assert.assertNull(str14);
        org.junit.Assert.assertNotNull(sAMSequenceRecord15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
    }

    @Test
    public void test223() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test223");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str19 = sAMSequenceRecord18.getAssembly();
        sAMSequenceRecord18.setDescription("SP");
        sAMSequenceRecord18.setAttribute("SN", "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str19);
    }

    @Test
    public void test224() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test224");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("AS");
        sAMSequenceRecord1.setSequenceIndex((int) (byte) 10);
        int int4 = sAMSequenceRecord1.getSequenceLength();
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 0 + "'", int4 == 0);
    }

    @Test
    public void test225() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test225");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setDescription("@SQ");
        sAMSequenceRecord2.setSequenceIndex((int) ' ');
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test226() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test226");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSpecies("");
        java.lang.String str10 = sAMSequenceRecord2.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS\tAS:-1");
        java.lang.String str11 = sAMSequenceRecord2.toString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str11, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test227() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test227");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet16 = sAMSequenceRecord11.getAttributes();
        int int17 = sAMSequenceRecord11.getSequenceLength();
        java.lang.String str19 = sAMSequenceRecord11.getAttribute("@SQ");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(strEntrySet16);
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + 1 + "'", int17 == 1);
        org.junit.Assert.assertNull(str19);
    }

    @Test
    public void test228() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test228");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        int int8 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str9 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str10 = sAMSequenceRecord2.getSpecies();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertTrue("'" + int8 + "' != '" + 1 + "'", int8 == 1);
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "UR" + "'", str9, "UR");
        org.junit.Assert.assertNull(str10);
    }

    @Test
    public void test229() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test229");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (byte) -1);
        java.lang.String str3 = sAMSequenceRecord2.getMd5();
        java.lang.String str4 = sAMSequenceRecord2.getAssembly();
        org.junit.Assert.assertNull(str3);
        org.junit.Assert.assertNull(str4);
    }

    @Test
    public void test230() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test230");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        boolean boolean25 = sAMSequenceRecord21.equals((java.lang.Object) 100.0f);
        int int26 = sAMSequenceRecord21.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet27 = sAMSequenceRecord21.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int31 = sAMSequenceRecord30.getSequenceIndex();
        sAMSequenceRecord30.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean34 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord30);
        java.lang.String str36 = sAMSequenceRecord21.getAttribute("");
        java.lang.String str37 = sAMSequenceRecord21.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord38 = sAMSequenceRecord21.clone();
        boolean boolean39 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet40 = sAMSequenceRecord21.getAttributes();
        java.lang.String str41 = sAMSequenceRecord21.toString();
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str42 = sAMSequenceRecord21.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + 1 + "'", int26 == 1);
        org.junit.Assert.assertNotNull(strEntrySet27);
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + (-1) + "'", int31 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
        org.junit.Assert.assertNull(str36);
        org.junit.Assert.assertNull(str37);
        org.junit.Assert.assertNotNull(sAMSequenceRecord38);
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + true + "'", boolean39 == true);
        org.junit.Assert.assertNotNull(strEntrySet40);
        org.junit.Assert.assertEquals("'" + str41 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str41, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test231() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test231");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str7 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setAssembly("SN");
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet10 = sAMSequenceRecord2.getAttributes();
        java.lang.String str11 = sAMSequenceRecord2.toString();
        int int12 = sAMSequenceRecord2.getSequenceIndex();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNull(str7);
        org.junit.Assert.assertNotNull(strEntrySet10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)" + "'", str11, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)");
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
    }

    @Test
    public void test232() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test232");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = sAMSequenceRecord2.clone();
        java.lang.String str7 = sAMSequenceRecord6.getSpecies();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNotNull(sAMSequenceRecord6);
        org.junit.Assert.assertNull(str7);
    }

    @Test
    public void test233() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test233");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getDescription();
        sAMSequenceRecord7.setSequenceLength((int) (byte) 100);
        sAMSequenceRecord7.setSequenceIndex((int) '#');
        java.lang.String str13 = sAMSequenceRecord7.toString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "SAMSequenceRecord(name=UR,length=100,dict_index=35,assembly=null)" + "'", str13, "SAMSequenceRecord(name=UR,length=100,dict_index=35,assembly=null)");
    }

    @Test
    public void test234() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test234");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        java.lang.String str19 = sAMSequenceRecord18.getAssembly();
        sAMSequenceRecord18.setSequenceLength(0);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str19);
    }

    @Test
    public void test235() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test235");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet16 = sAMSequenceRecord11.getAttributes();
        sAMSequenceRecord11.setAttribute("UR", "=");
        java.lang.String str20 = sAMSequenceRecord11.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(strEntrySet16);
        org.junit.Assert.assertEquals("'" + str20 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str20, "@SQ\tSN:UR\tLN:1\tAS:AS");
    }

    @Test
    public void test236() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test236");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord2.getSAMString();
        java.lang.String str9 = sAMSequenceRecord2.getAssembly();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord12 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int13 = sAMSequenceRecord12.getSequenceIndex();
        int int14 = sAMSequenceRecord12.getSequenceLength();
        java.lang.String str15 = sAMSequenceRecord12.getDescription();
        java.lang.String str16 = sAMSequenceRecord12.getSequenceName();
        java.lang.String str17 = sAMSequenceRecord12.getDescription();
        int int18 = sAMSequenceRecord12.getSequenceLength();
        java.lang.String str19 = sAMSequenceRecord12.getSequenceName();
        boolean boolean20 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord12);
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "@SQ\tSN:UR\tLN:1" + "'", str8, "@SQ\tSN:UR\tLN:1");
        org.junit.Assert.assertNull(str9);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + (-1) + "'", int13 == (-1));
        org.junit.Assert.assertTrue("'" + int14 + "' != '" + 1 + "'", int14 == 1);
        org.junit.Assert.assertNull(str15);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "UR" + "'", str16, "UR");
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + 1 + "'", int18 == 1);
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "UR" + "'", str19, "UR");
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
    }

    @Test
    public void test237() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test237");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        boolean boolean10 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord9);
        java.lang.String str11 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAssembly("SAMSequenceRecord(name=UR,length=100,dict_index=35,assembly=null)");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)" + "'", str11, "SAMSequenceRecord(name=UR,length=10,dict_index=-1,assembly=null)");
    }

    @Test
    public void test238() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test238");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getSpecies();
        sAMSequenceRecord7.setSequenceLength(0);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test239() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test239");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceIndex((int) (byte) 1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test240() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test240");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet18 = sAMSequenceRecord13.getAttributes();
        int int19 = sAMSequenceRecord13.getSequenceLength();
        sAMSequenceRecord13.setSpecies("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord13.setSpecies("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str24 = sAMSequenceRecord13.getDescription();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = sAMSequenceRecord13.clone();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(strEntrySet18);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 1 + "'", int19 == 1);
        org.junit.Assert.assertNull(str24);
        org.junit.Assert.assertNotNull(sAMSequenceRecord25);
    }

    @Test
    public void test241() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test241");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord8 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj9 = null;
        boolean boolean10 = sAMSequenceRecord8.equals(obj9);
        boolean boolean12 = sAMSequenceRecord8.equals((java.lang.Object) 100.0f);
        int int13 = sAMSequenceRecord8.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet14 = sAMSequenceRecord8.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord17 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int18 = sAMSequenceRecord17.getSequenceIndex();
        sAMSequenceRecord17.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean21 = sAMSequenceRecord8.isSameSequence(sAMSequenceRecord17);
        java.lang.String str23 = sAMSequenceRecord8.getAttribute("");
        java.lang.String str24 = sAMSequenceRecord8.getSpecies();
        sAMSequenceRecord8.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord29 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int30 = sAMSequenceRecord29.getSequenceIndex();
        int int31 = sAMSequenceRecord29.getSequenceLength();
        java.lang.String str32 = sAMSequenceRecord29.getDescription();
        java.lang.String str33 = sAMSequenceRecord29.getSequenceName();
        java.lang.String str34 = sAMSequenceRecord29.getDescription();
        sAMSequenceRecord29.setAssembly("SN");
        boolean boolean37 = sAMSequenceRecord8.equals((java.lang.Object) sAMSequenceRecord29);
        boolean boolean38 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord8);
        java.lang.String str39 = sAMSequenceRecord2.getSequenceName();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + int13 + "' != '" + 1 + "'", int13 == 1);
        org.junit.Assert.assertNotNull(strEntrySet14);
        org.junit.Assert.assertTrue("'" + int18 + "' != '" + (-1) + "'", int18 == (-1));
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
        org.junit.Assert.assertNull(str23);
        org.junit.Assert.assertNull(str24);
        org.junit.Assert.assertTrue("'" + int30 + "' != '" + (-1) + "'", int30 == (-1));
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + 1 + "'", int31 == 1);
        org.junit.Assert.assertNull(str32);
        org.junit.Assert.assertEquals("'" + str33 + "' != '" + "UR" + "'", str33, "UR");
        org.junit.Assert.assertNull(str34);
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + false + "'", boolean37 == false);
        org.junit.Assert.assertTrue("'" + boolean38 + "' != '" + false + "'", boolean38 == false);
        org.junit.Assert.assertEquals("'" + str39 + "' != '" + "UR" + "'", str39, "UR");
    }

    @Test
    public void test242() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test242");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet18 = sAMSequenceRecord13.getAttributes();
        int int19 = sAMSequenceRecord13.getSequenceLength();
        sAMSequenceRecord13.setSpecies("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str23 = sAMSequenceRecord13.getAttribute("0.0");
        sAMSequenceRecord13.setSpecies("DS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(strEntrySet18);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 1 + "'", int19 == 1);
        org.junit.Assert.assertNull(str23);
    }

    @Test
    public void test243() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test243");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        int int22 = sAMSequenceRecord2.getSequenceLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + 1 + "'", int22 == 1);
    }

    @Test
    public void test244() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test244");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord13.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        boolean boolean25 = sAMSequenceRecord21.equals((java.lang.Object) 100.0f);
        int int26 = sAMSequenceRecord21.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet27 = sAMSequenceRecord21.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int31 = sAMSequenceRecord30.getSequenceIndex();
        sAMSequenceRecord30.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean34 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord30);
        java.lang.String str36 = sAMSequenceRecord21.getAttribute("");
        java.lang.String str37 = sAMSequenceRecord21.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord38 = sAMSequenceRecord21.clone();
        boolean boolean39 = sAMSequenceRecord18.equals((java.lang.Object) sAMSequenceRecord21);
        sAMSequenceRecord21.setMd5("M5");
        // The following exception was thrown during execution in test generation
        try {
            java.lang.String str42 = sAMSequenceRecord21.getId();
            org.junit.Assert.fail("Expected exception of type java.lang.UnsupportedOperationException; message: Method not implemented for: class htsjdk.samtools.SAMSequenceRecord");
        } catch (java.lang.UnsupportedOperationException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + 1 + "'", int26 == 1);
        org.junit.Assert.assertNotNull(strEntrySet27);
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + (-1) + "'", int31 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
        org.junit.Assert.assertNull(str36);
        org.junit.Assert.assertNull(str37);
        org.junit.Assert.assertNotNull(sAMSequenceRecord38);
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + true + "'", boolean39 == true);
    }

    @Test
    public void test245() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test245");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        java.lang.String str8 = sAMSequenceRecord7.getSpecies();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str8);
    }

    @Test
    public void test246() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test246");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj22 = null;
        boolean boolean23 = sAMSequenceRecord21.equals(obj22);
        boolean boolean25 = sAMSequenceRecord21.equals((java.lang.Object) 100.0f);
        int int26 = sAMSequenceRecord21.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet27 = sAMSequenceRecord21.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int31 = sAMSequenceRecord30.getSequenceIndex();
        sAMSequenceRecord30.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean34 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord30);
        java.lang.String str35 = sAMSequenceRecord30.getSAMString();
        int int36 = sAMSequenceRecord30.getSequenceIndex();
        boolean boolean37 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord30);
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertTrue("'" + int26 + "' != '" + 1 + "'", int26 == 1);
        org.junit.Assert.assertNotNull(strEntrySet27);
        org.junit.Assert.assertTrue("'" + int31 + "' != '" + (-1) + "'", int31 == (-1));
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + true + "'", boolean34 == true);
        org.junit.Assert.assertEquals("'" + str35 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str35, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int36 + "' != '" + (-1) + "'", int36 == (-1));
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + false + "'", boolean37 == false);
    }

    @Test
    public void test247() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test247");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        sAMSequenceRecord2.setSequenceIndex(100);
    }

    @Test
    public void test248() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test248");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord24 = sAMSequenceRecord23.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = sAMSequenceRecord23.clone();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNotNull(sAMSequenceRecord23);
        org.junit.Assert.assertNotNull(sAMSequenceRecord24);
        org.junit.Assert.assertNotNull(sAMSequenceRecord25);
    }

    @Test
    public void test249() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test249");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord8 = sAMSequenceRecord2.clone();
        java.lang.String str9 = sAMSequenceRecord8.getSequenceName();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNotNull(sAMSequenceRecord8);
        org.junit.Assert.assertEquals("'" + str9 + "' != '" + "UR" + "'", str9, "UR");
    }

    @Test
    public void test250() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test250");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord2.setSequenceIndex(100);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord14 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj15 = null;
        boolean boolean16 = sAMSequenceRecord14.equals(obj15);
        sAMSequenceRecord14.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord21 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int22 = sAMSequenceRecord21.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord25 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj26 = null;
        boolean boolean27 = sAMSequenceRecord25.equals(obj26);
        boolean boolean28 = sAMSequenceRecord21.isSameSequence(sAMSequenceRecord25);
        boolean boolean29 = sAMSequenceRecord14.isSameSequence(sAMSequenceRecord25);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = sAMSequenceRecord14.clone();
        java.lang.String str32 = sAMSequenceRecord30.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int33 = sAMSequenceRecord30.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord36 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int37 = sAMSequenceRecord36.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord40 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj41 = null;
        boolean boolean42 = sAMSequenceRecord40.equals(obj41);
        boolean boolean43 = sAMSequenceRecord36.isSameSequence(sAMSequenceRecord40);
        boolean boolean44 = sAMSequenceRecord30.isSameSequence(sAMSequenceRecord36);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) boolean44);
        sAMSequenceRecord2.setAssembly("AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + true + "'", boolean29 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord30);
        org.junit.Assert.assertNull(str32);
        org.junit.Assert.assertTrue("'" + int33 + "' != '" + (-1) + "'", int33 == (-1));
        org.junit.Assert.assertTrue("'" + int37 + "' != '" + (-1) + "'", int37 == (-1));
        org.junit.Assert.assertTrue("'" + boolean42 + "' != '" + false + "'", boolean42 == false);
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertTrue("'" + boolean44 + "' != '" + true + "'", boolean44 == true);
    }

    @Test
    public void test251() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test251");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        sAMSequenceRecord2.setSpecies("=");
        sAMSequenceRecord2.setSequenceIndex((int) 'a');
        sAMSequenceRecord2.setSequenceIndex((int) (short) 100);
        java.lang.String str24 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=SN)", "SN");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertEquals("'" + str24 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=100,assembly=null)" + "'", str24, "SAMSequenceRecord(name=UR,length=1,dict_index=100,assembly=null)");
    }

    @Test
    public void test252() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test252");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSpecies("");
        java.lang.String str9 = sAMSequenceRecord2.getAssembly();
        sAMSequenceRecord2.setDescription("");
        java.lang.String str12 = sAMSequenceRecord2.getSAMString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNull(str6);
        org.junit.Assert.assertNull(str9);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "@SQ\tSN:UR\tLN:1\tSP:\tDS:" + "'", str12, "@SQ\tSN:UR\tLN:1\tSP:\tDS:");
    }

    @Test
    public void test253() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test253");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 0);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
    }

    @Test
    public void test254() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test254");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("SN");
    }

    @Test
    public void test255() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test255");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        sAMSequenceRecord2.setAssembly("UR");
        java.lang.String str23 = sAMSequenceRecord2.getSAMString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertEquals("'" + str23 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:UR" + "'", str23, "@SQ\tSN:UR\tLN:1\tAS:UR");
    }

    @Test
    public void test256() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test256");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        java.lang.String str8 = sAMSequenceRecord2.getAttribute("AS");
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tSP:\tDS:");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "AS" + "'", str8, "AS");
    }

    @Test
    public void test257() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test257");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.samtools.SAMSequenceRecord.validateSequenceName("@SQ\tSN:UR\tLN:1\tSP:");
            org.junit.Assert.fail("Expected exception of type htsjdk.samtools.SAMException; message: Sequence name '@SQ?SN:UR?LN:1?SP:' doesn't match regex: '[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*' ");
        } catch (htsjdk.samtools.SAMException e) {
            // Expected exception.
        }
    }

    @Test
    public void test258() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test258");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        sAMSequenceRecord11.setSequenceIndex((int) (short) 1);
        java.lang.String str19 = sAMSequenceRecord11.getMd5();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertEquals("'" + str19 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str19, "@SQ\tSN:UR\tLN:1\tAS:AS");
    }

    @Test
    public void test259() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test259");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        sAMSequenceRecord2.setAttribute("", "@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str26 = sAMSequenceRecord2.getAssembly();
        java.lang.String str27 = sAMSequenceRecord2.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord30 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj31 = null;
        boolean boolean32 = sAMSequenceRecord30.equals(obj31);
        sAMSequenceRecord30.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord37 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int38 = sAMSequenceRecord37.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord41 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj42 = null;
        boolean boolean43 = sAMSequenceRecord41.equals(obj42);
        boolean boolean44 = sAMSequenceRecord37.isSameSequence(sAMSequenceRecord41);
        boolean boolean45 = sAMSequenceRecord30.isSameSequence(sAMSequenceRecord41);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord46 = sAMSequenceRecord41.clone();
        java.lang.String str47 = sAMSequenceRecord46.getAssembly();
        java.lang.String str48 = sAMSequenceRecord46.getAssembly();
        boolean boolean49 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord46);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertNull(str27);
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertTrue("'" + int38 + "' != '" + (-1) + "'", int38 == (-1));
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + false + "'", boolean43 == false);
        org.junit.Assert.assertTrue("'" + boolean44 + "' != '" + true + "'", boolean44 == true);
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + true + "'", boolean45 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord46);
        org.junit.Assert.assertNull(str47);
        org.junit.Assert.assertNull(str48);
        org.junit.Assert.assertTrue("'" + boolean49 + "' != '" + true + "'", boolean49 == true);
    }

    @Test
    public void test260() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test260");
        java.lang.String str1 = htsjdk.samtools.SAMSequenceRecord.truncateSequenceName("@SQ\tSN:UR\tLN:1\tSP:");
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "@SQ" + "'", str1, "@SQ");
    }

    @Test
    public void test261() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test261");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        java.lang.String str17 = sAMSequenceRecord11.getSpecies();
        sAMSequenceRecord11.setSequenceIndex((int) (byte) -1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertNull(str17);
    }

    @Test
    public void test262() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test262");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord34 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj35 = null;
        boolean boolean36 = sAMSequenceRecord34.equals(obj35);
        sAMSequenceRecord34.setSequenceLength((int) (short) 10);
        sAMSequenceRecord34.setAssembly("@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord34.setSequenceIndex(100);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord46 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj47 = null;
        boolean boolean48 = sAMSequenceRecord46.equals(obj47);
        sAMSequenceRecord46.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord53 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int54 = sAMSequenceRecord53.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord57 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj58 = null;
        boolean boolean59 = sAMSequenceRecord57.equals(obj58);
        boolean boolean60 = sAMSequenceRecord53.isSameSequence(sAMSequenceRecord57);
        boolean boolean61 = sAMSequenceRecord46.isSameSequence(sAMSequenceRecord57);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord62 = sAMSequenceRecord46.clone();
        java.lang.String str64 = sAMSequenceRecord62.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        int int65 = sAMSequenceRecord62.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord68 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int69 = sAMSequenceRecord68.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord72 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj73 = null;
        boolean boolean74 = sAMSequenceRecord72.equals(obj73);
        boolean boolean75 = sAMSequenceRecord68.isSameSequence(sAMSequenceRecord72);
        boolean boolean76 = sAMSequenceRecord62.isSameSequence(sAMSequenceRecord68);
        sAMSequenceRecord34.setAttribute("hi!", (java.lang.Object) boolean76);
        boolean boolean78 = sAMSequenceRecord23.equals((java.lang.Object) sAMSequenceRecord34);
        java.lang.String str79 = sAMSequenceRecord34.getAssembly();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + false + "'", boolean36 == false);
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + false + "'", boolean48 == false);
        org.junit.Assert.assertTrue("'" + int54 + "' != '" + (-1) + "'", int54 == (-1));
        org.junit.Assert.assertTrue("'" + boolean59 + "' != '" + false + "'", boolean59 == false);
        org.junit.Assert.assertTrue("'" + boolean60 + "' != '" + true + "'", boolean60 == true);
        org.junit.Assert.assertTrue("'" + boolean61 + "' != '" + true + "'", boolean61 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord62);
        org.junit.Assert.assertNull(str64);
        org.junit.Assert.assertTrue("'" + int65 + "' != '" + (-1) + "'", int65 == (-1));
        org.junit.Assert.assertTrue("'" + int69 + "' != '" + (-1) + "'", int69 == (-1));
        org.junit.Assert.assertTrue("'" + boolean74 + "' != '" + false + "'", boolean74 == false);
        org.junit.Assert.assertTrue("'" + boolean75 + "' != '" + true + "'", boolean75 == true);
        org.junit.Assert.assertTrue("'" + boolean76 + "' != '" + true + "'", boolean76 == true);
        org.junit.Assert.assertTrue("'" + boolean78 + "' != '" + false + "'", boolean78 == false);
        org.junit.Assert.assertEquals("'" + str79 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str79, "@SQ\tSN:UR\tLN:1\tAS:AS");
    }

    @Test
    public void test263() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test263");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        sAMSequenceRecord6.setAttribute("UR", "@SQ\tSN:UR\tLN:1\tDS:\tSN:=");
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test264() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test264");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str21 = sAMSequenceRecord18.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord18.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = sAMSequenceRecord18.clone();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet24 = sAMSequenceRecord23.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "UR" + "'", str22, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord23);
        org.junit.Assert.assertNotNull(strEntrySet24);
    }

    @Test
    public void test265() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test265");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        int int4 = sAMSequenceRecord2.getSequenceLength();
        java.lang.String str5 = sAMSequenceRecord2.getDescription();
        java.lang.String str6 = sAMSequenceRecord2.getSequenceName();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord7 = sAMSequenceRecord2.clone();
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str10 = sAMSequenceRecord2.getAssembly();
        java.lang.String str11 = sAMSequenceRecord2.getDescription();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + int4 + "' != '" + 1 + "'", int4 == 1);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertEquals("'" + str6 + "' != '" + "UR" + "'", str6, "UR");
        org.junit.Assert.assertNotNull(sAMSequenceRecord7);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str11, "@SQ\tSN:UR\tLN:1\tAS:AS");
    }

    @Test
    public void test266() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test266");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        java.lang.String str5 = sAMSequenceRecord2.getMd5();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = sAMSequenceRecord2.clone();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord10 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (byte) -1);
        sAMSequenceRecord10.setSequenceIndex((int) ' ');
        sAMSequenceRecord2.setAttribute("SN", (java.lang.Object) sAMSequenceRecord10);
        java.lang.String str14 = sAMSequenceRecord2.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str5);
        org.junit.Assert.assertNotNull(sAMSequenceRecord6);
        org.junit.Assert.assertEquals("'" + str14 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str14, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test267() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test267");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setAssembly("AS");
        java.lang.String str8 = sAMSequenceRecord2.getAttribute("AS");
        java.lang.String str10 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str11 = sAMSequenceRecord2.getSAMString();
        sAMSequenceRecord2.setSequenceIndex(1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "AS" + "'", str8, "AS");
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str11, "@SQ\tSN:UR\tLN:1\tAS:AS");
    }

    @Test
    public void test268() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test268");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord18 = sAMSequenceRecord2.clone();
        java.lang.String str20 = sAMSequenceRecord18.getAttribute("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str21 = sAMSequenceRecord18.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord18.getSequenceName();
        int int23 = sAMSequenceRecord18.getSequenceIndex();
        int int24 = sAMSequenceRecord18.getSequenceLength();
        java.lang.String str25 = sAMSequenceRecord18.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(sAMSequenceRecord18);
        org.junit.Assert.assertNull(str20);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "UR" + "'", str22, "UR");
        org.junit.Assert.assertTrue("'" + int23 + "' != '" + (-1) + "'", int23 == (-1));
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + 1 + "'", int24 == 1);
        org.junit.Assert.assertEquals("'" + str25 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str25, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test269() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test269");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        java.lang.String str10 = sAMSequenceRecord2.getDescription();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet11 = sAMSequenceRecord2.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertNotNull(strEntrySet11);
    }

    @Test
    public void test270() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test270");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", (int) '#');
        java.lang.String str3 = sAMSequenceRecord2.getAssembly();
        sAMSequenceRecord2.setDescription("@SQ\tSN:UR\tLN:1\tDS:\tSN:=");
        org.junit.Assert.assertNull(str3);
    }

    @Test
    public void test271() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test271");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        sAMSequenceRecord2.setMd5("AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
    }

    @Test
    public void test272() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test272");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord19 = new htsjdk.samtools.SAMSequenceRecord("DS", (int) (short) -1);
        sAMSequenceRecord11.setAttribute("AS", (java.lang.Object) (short) -1);
        int int21 = sAMSequenceRecord11.getSequenceLength();
        int int22 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("0.0");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertTrue("'" + int21 + "' != '" + 1 + "'", int21 == 1);
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
    }

    @Test
    public void test273() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test273");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet5 = sAMSequenceRecord2.getAttributes();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNotNull(strEntrySet5);
    }

    @Test
    public void test274() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test274");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setSequenceLength((int) (short) 10);
        sAMSequenceRecord2.setAttribute("hi!", (java.lang.Object) 0L);
        java.lang.String str10 = sAMSequenceRecord2.getDescription();
        sAMSequenceRecord2.setDescription("SN");
        java.lang.String str13 = sAMSequenceRecord2.getSequenceName();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertEquals("'" + str13 + "' != '" + "UR" + "'", str13, "UR");
    }

    @Test
    public void test275() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test275");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord1 = new htsjdk.samtools.SAMSequenceRecord("AS");
        java.lang.String str2 = sAMSequenceRecord1.getMd5();
        org.junit.Assert.assertNull(str2);
    }

    @Test
    public void test276() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test276");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int3 = sAMSequenceRecord2.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord6 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj7 = null;
        boolean boolean8 = sAMSequenceRecord6.equals(obj7);
        boolean boolean9 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord6);
        java.lang.String str10 = sAMSequenceRecord6.getDescription();
        java.lang.String str11 = sAMSequenceRecord6.getMd5();
        java.lang.String str12 = sAMSequenceRecord6.toString();
        org.junit.Assert.assertTrue("'" + int3 + "' != '" + (-1) + "'", int3 == (-1));
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNull(str10);
        org.junit.Assert.assertNull(str11);
        org.junit.Assert.assertEquals("'" + str12 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str12, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test277() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test277");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet18 = sAMSequenceRecord13.getAttributes();
        int int19 = sAMSequenceRecord13.getSequenceLength();
        sAMSequenceRecord13.setSpecies("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        sAMSequenceRecord13.setSpecies("@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str24 = sAMSequenceRecord13.getDescription();
        int int25 = sAMSequenceRecord13.getSequenceLength();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(strEntrySet18);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 1 + "'", int19 == 1);
        org.junit.Assert.assertNull(str24);
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
    }

    @Test
    public void test278() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test278");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str17 = sAMSequenceRecord2.getAttribute("");
        java.lang.String str18 = sAMSequenceRecord2.getSpecies();
        sAMSequenceRecord2.setSequenceIndex((int) '#');
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord23 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int24 = sAMSequenceRecord23.getSequenceIndex();
        int int25 = sAMSequenceRecord23.getSequenceLength();
        java.lang.String str26 = sAMSequenceRecord23.getDescription();
        java.lang.String str27 = sAMSequenceRecord23.getSequenceName();
        java.lang.String str28 = sAMSequenceRecord23.getDescription();
        sAMSequenceRecord23.setAssembly("SN");
        boolean boolean31 = sAMSequenceRecord2.equals((java.lang.Object) sAMSequenceRecord23);
        java.lang.String str32 = sAMSequenceRecord2.getAssembly();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNull(str17);
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertTrue("'" + int24 + "' != '" + (-1) + "'", int24 == (-1));
        org.junit.Assert.assertTrue("'" + int25 + "' != '" + 1 + "'", int25 == 1);
        org.junit.Assert.assertNull(str26);
        org.junit.Assert.assertEquals("'" + str27 + "' != '" + "UR" + "'", str27, "UR");
        org.junit.Assert.assertNull(str28);
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertNull(str32);
    }

    @Test
    public void test279() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test279");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet18 = sAMSequenceRecord13.getAttributes();
        int int19 = sAMSequenceRecord13.getSequenceLength();
        sAMSequenceRecord13.setSpecies("@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        java.lang.String str23 = sAMSequenceRecord13.getAttribute("0.0");
        sAMSequenceRecord13.setAssembly("@SQ\tSN:UR\tLN:1\tAS:UR");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertNotNull(strEntrySet18);
        org.junit.Assert.assertTrue("'" + int19 + "' != '" + 1 + "'", int19 == 1);
        org.junit.Assert.assertNull(str23);
    }

    @Test
    public void test280() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test280");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        java.lang.String str22 = sAMSequenceRecord2.toString();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet23 = sAMSequenceRecord2.getAttributes();
        java.lang.String str24 = sAMSequenceRecord2.toString();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str22, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
        org.junit.Assert.assertNotNull(strEntrySet23);
        org.junit.Assert.assertEquals("'" + str24 + "' != '" + "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)" + "'", str24, "SAMSequenceRecord(name=UR,length=1,dict_index=-1,assembly=null)");
    }

    @Test
    public void test281() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test281");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceIndex();
        java.lang.String str8 = sAMSequenceRecord2.getDescription();
        java.lang.String str9 = sAMSequenceRecord2.getMd5();
        java.lang.Class<?> wildcardClass10 = sAMSequenceRecord2.getClass();
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + (-1) + "'", int7 == (-1));
        org.junit.Assert.assertNull(str8);
        org.junit.Assert.assertNull(str9);
        org.junit.Assert.assertNotNull(wildcardClass10);
    }

    @Test
    public void test282() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test282");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        boolean boolean6 = sAMSequenceRecord2.equals((java.lang.Object) 100.0f);
        int int7 = sAMSequenceRecord2.getSequenceLength();
        java.util.Set<java.util.Map.Entry<java.lang.String, java.lang.String>> strEntrySet8 = sAMSequenceRecord2.getAttributes();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord11 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int12 = sAMSequenceRecord11.getSequenceIndex();
        sAMSequenceRecord11.setMd5("@SQ\tSN:UR\tLN:1\tAS:AS");
        boolean boolean15 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord11);
        java.lang.String str16 = sAMSequenceRecord11.getSAMString();
        int int17 = sAMSequenceRecord11.getSequenceIndex();
        java.lang.String str18 = sAMSequenceRecord11.getDescription();
        sAMSequenceRecord11.setAttribute("=", "SN");
        sAMSequenceRecord11.setAttribute("M5", "=");
        java.lang.String str26 = sAMSequenceRecord11.getAttribute("");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + int7 + "' != '" + 1 + "'", int7 == 1);
        org.junit.Assert.assertNotNull(strEntrySet8);
        org.junit.Assert.assertTrue("'" + int12 + "' != '" + (-1) + "'", int12 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS" + "'", str16, "@SQ\tSN:UR\tLN:1\tM5:@SQ\tSN:UR\tLN:1\tAS:AS");
        org.junit.Assert.assertTrue("'" + int17 + "' != '" + (-1) + "'", int17 == (-1));
        org.junit.Assert.assertNull(str18);
        org.junit.Assert.assertNull(str26);
    }

    @Test
    public void test283() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test283");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord2 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj3 = null;
        boolean boolean4 = sAMSequenceRecord2.equals(obj3);
        sAMSequenceRecord2.setDescription("");
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord9 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        int int10 = sAMSequenceRecord9.getSequenceIndex();
        htsjdk.samtools.SAMSequenceRecord sAMSequenceRecord13 = new htsjdk.samtools.SAMSequenceRecord("UR", 1);
        java.lang.Object obj14 = null;
        boolean boolean15 = sAMSequenceRecord13.equals(obj14);
        boolean boolean16 = sAMSequenceRecord9.isSameSequence(sAMSequenceRecord13);
        boolean boolean17 = sAMSequenceRecord2.isSameSequence(sAMSequenceRecord13);
        sAMSequenceRecord2.setAttribute("SN", "=");
        java.lang.String str21 = sAMSequenceRecord2.getSequenceName();
        int int22 = sAMSequenceRecord2.getSequenceIndex();
        java.lang.String str24 = sAMSequenceRecord2.getAttribute("AS");
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + int10 + "' != '" + (-1) + "'", int10 == (-1));
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + true + "'", boolean17 == true);
        org.junit.Assert.assertEquals("'" + str21 + "' != '" + "UR" + "'", str21, "UR");
        org.junit.Assert.assertTrue("'" + int22 + "' != '" + (-1) + "'", int22 == (-1));
        org.junit.Assert.assertNull(str24);
    }
}

