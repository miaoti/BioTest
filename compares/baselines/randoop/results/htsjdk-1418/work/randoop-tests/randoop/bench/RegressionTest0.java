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
        long long0 = htsjdk.variant.vcf.VCFHeaderLine.serialVersionUID;
        org.junit.Assert.assertTrue("'" + long0 + "' != '" + 1L + "'", long0 == 1L);
    }

    @Test
    public void test002() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test002");
        java.lang.String str0 = htsjdk.variant.vcf.VCFSimpleHeaderLine.ID_ATTRIBUTE;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "ID" + "'", str0, "ID");
    }

    @Test
    public void test003() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test003");
        boolean boolean1 = htsjdk.variant.vcf.VCFHeaderLine.isHeaderLine("ID");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + false + "'", boolean1 == false);
    }

    @Test
    public void test004() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test004");
        java.lang.Object obj0 = new java.lang.Object();
        java.lang.Class<?> wildcardClass1 = obj0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
    }

    @Test
    public void test005() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test005");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test006() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test006");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test007() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test007");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test008() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test008");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test009() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test009");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test010() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test010");
        boolean boolean1 = htsjdk.variant.vcf.VCFHeaderLine.isHeaderLine("hi!");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + false + "'", boolean1 == false);
    }

    @Test
    public void test011() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test011");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test012() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test012");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test013() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test013");
        java.lang.String str0 = htsjdk.variant.vcf.VCFSimpleHeaderLine.DESCRIPTION_ATTRIBUTE;
        org.junit.Assert.assertEquals("'" + str0 + "' != '" + "Description" + "'", str0, "Description");
    }

    @Test
    public void test014() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test014");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test015() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test015");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test016() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test016");
        boolean boolean1 = htsjdk.variant.vcf.VCFHeaderLine.isHeaderLine("");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + false + "'", boolean1 == false);
    }

    @Test
    public void test017() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test017");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test018() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test018");
        boolean boolean1 = htsjdk.variant.vcf.VCFHeaderLine.isHeaderLine("Description");
        org.junit.Assert.assertTrue("'" + boolean1 + "' != '" + false + "'", boolean1 == false);
    }

    @Test
    public void test019() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test019");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test020() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test020");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test021() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test021");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test022() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test022");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test023() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test023");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test024() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test024");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test025() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test025");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test026() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test026");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test027() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test027");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test028() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test028");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test029() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test029");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test030() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test030");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test031() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test031");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test032() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test032");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test033() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test033");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test034() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test034");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test035() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test035");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test036() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test036");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test037() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test037");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test038() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test038");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test039() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test039");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test040() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test040");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test041() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test041");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test042() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test042");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test043() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test043");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test044() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test044");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test045() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test045");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test046() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test046");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test047() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test047");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test048() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test048");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test049() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test049");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test050() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test050");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test051() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test051");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test052() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test052");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test053() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test053");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test054() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test054");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test055() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test055");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test056() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test056");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test057() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test057");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test058() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test058");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test059() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test059");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test060() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test060");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test061() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test061");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test062() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test062");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test063() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test063");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test064() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test064");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test065() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test065");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test066() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test066");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test067() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test067");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test068() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test068");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test069() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test069");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test070() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test070");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test071() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test071");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test072() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test072");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test073() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test073");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test074() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test074");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test075() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test075");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test076() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test076");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test077() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test077");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test078() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test078");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test079() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test079");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test080() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test080");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test081() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test081");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test082() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test082");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test083() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test083");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test084() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test084");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test085() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test085");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test086() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test086");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test087() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test087");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test088() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test088");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test089() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test089");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test090() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test090");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test091() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test091");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test092() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test092");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test093() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test093");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test094() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test094");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test095() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test095");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test096() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test096");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test097() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test097");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test098() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test098");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test099() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test099");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test100() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test100");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test101() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test101");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test102() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test102");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test103() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test103");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test104() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test104");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test105() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test105");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test106() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test106");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test107() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test107");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test108() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test108");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test109() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test109");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test110() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test110");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test111() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test111");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test112() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test112");
        java.util.Map<java.lang.String, java.lang.String> strMap0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine2 = new htsjdk.variant.vcf.VCFContigHeaderLine(strMap0, (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Map.get(Object)\" because \"mapping\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test113() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test113");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test114() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test114");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test115() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test115");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test116() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test116");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test117() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test117");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test118() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test118");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test119() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test119");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test120() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test120");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test121() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test121");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test122() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test122");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test123() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test123");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test124() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test124");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test125() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test125");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test126() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test126");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test127() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test127");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test128() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test128");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test129() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test129");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test130() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test130");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test131() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test131");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test132() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test132");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test133() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test133");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test134() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test134");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test135() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test135");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test136() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test136");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test137() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test137");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test138() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test138");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test139() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test139");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test140() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test140");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test141() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test141");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test142() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test142");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test143() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test143");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test144() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test144");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test145() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test145");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test146() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test146");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test147() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test147");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test148() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test148");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test149() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test149");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test150() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test150");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test151() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test151");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test152() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test152");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test153() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test153");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test154() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test154");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test155() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test155");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test156() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test156");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test157() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test157");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test158() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test158");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test159() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test159");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test160() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test160");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test161() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test161");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test162() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test162");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test163() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test163");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test164() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test164");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test165() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test165");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test166() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test166");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test167() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test167");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test168() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test168");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test169() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test169");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test170() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test170");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test171() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test171");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test172() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test172");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test173() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test173");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test174() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test174");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test175() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test175");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test176() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test176");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test177() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test177");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test178() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test178");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test179() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test179");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test180() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test180");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test181() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test181");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test182() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test182");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test183() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test183");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test184() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test184");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test185() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test185");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test186() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test186");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test187() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test187");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test188() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test188");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test189() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test189");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test190() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test190");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test191() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test191");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test192() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test192");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test193() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test193");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test194() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test194");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test195() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test195");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test196() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test196");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test197() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test197");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test198() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test198");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test199() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test199");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test200() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test200");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test201() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test201");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test202() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test202");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test203() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test203");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test204() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test204");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test205() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test205");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test206() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test206");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test207() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test207");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test208() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test208");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test209() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test209");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test210() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test210");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test211() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test211");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test212() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test212");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test213() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test213");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test214() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test214");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test215() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test215");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test216() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test216");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test217() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test217");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test218() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test218");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test219() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test219");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test220() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test220");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test221() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test221");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test222() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test222");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test223() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test223");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test224() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test224");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test225() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test225");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test226() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test226");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test227() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test227");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test228() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test228");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test229() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test229");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test230() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test230");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test231() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test231");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test232() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test232");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test233() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test233");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test234() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test234");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test235() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test235");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test236() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test236");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test237() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test237");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test238() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test238");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test239() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test239");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test240() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test240");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test241() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test241");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test242() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test242");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test243() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test243");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test244() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test244");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test245() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test245");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test246() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test246");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test247() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test247");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test248() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test248");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test249() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test249");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test250() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test250");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test251() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test251");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test252() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test252");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test253() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test253");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test254() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test254");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test255() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test255");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test256() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test256");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test257() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test257");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test258() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test258");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test259() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test259");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test260() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test260");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test261() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test261");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test262() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test262");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test263() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test263");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test264() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test264");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test265() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test265");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test266() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test266");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test267() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test267");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test268() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test268");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test269() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test269");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test270() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test270");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test271() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test271");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test272() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test272");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test273() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test273");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test274() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test274");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test275() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test275");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test276() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test276");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test277() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test277");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test278() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test278");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test279() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test279");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test280() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test280");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test281() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test281");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test282() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test282");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test283() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test283");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test284() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test284");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test285() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test285");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "Description", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test286() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test286");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test287() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test287");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test288() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test288");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test289() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test289");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test290() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test290");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test291() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test291");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test292() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test292");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test293() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test293");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test294() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test294");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test295() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test295");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test296() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test296");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test297() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test297");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test298() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test298");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test299() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test299");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test300() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test300");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test301() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test301");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test302() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test302");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test303() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test303");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test304() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test304");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test305() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test305");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test306() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test306");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test307() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test307");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test308() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test308");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test309() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test309");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test310() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test310");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test311() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test311");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test312() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test312");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test313() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test313");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "hi!", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test314() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test314");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test315() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test315");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "Description", (int) 'a');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test316() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test316");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "", (int) (byte) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test317() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test317");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test318() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test318");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "hi!", (int) (short) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test319() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test319");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test320() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test320");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "ID", (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test321() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test321");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (short) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test322() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test322");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "ID", (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test323() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test323");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test324() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test324");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "ID", (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test325() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test325");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "Description", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test326() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test326");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("Description", vCFHeaderVersion1, "", (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test327() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test327");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "Description", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test328() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test328");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("hi!", vCFHeaderVersion1, "ID", 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test329() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test329");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "", (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test330() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test330");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("ID", vCFHeaderVersion1, "hi!", (int) (short) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test331() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test331");
        htsjdk.variant.vcf.VCFHeaderVersion vCFHeaderVersion1 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFContigHeaderLine vCFContigHeaderLine4 = new htsjdk.variant.vcf.VCFContigHeaderLine("", vCFHeaderVersion1, "hi!", 10);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"htsjdk.variant.vcf.VCFLineParser.parseLine(String, java.util.List, java.util.List)\" because the return value of \"java.util.Map.get(Object)\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }
}

