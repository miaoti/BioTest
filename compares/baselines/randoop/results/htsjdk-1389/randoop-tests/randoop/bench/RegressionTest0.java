package randoop.bench;

import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class RegressionTest0 {

    public static boolean debug = false;

    @Test
    public void test01() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test01");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 'a');
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "97.00" + "'", str1, "97.00");
    }

    @Test
    public void test02() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test02");
        java.nio.charset.Charset charset0 = htsjdk.variant.vcf.VCFEncoder.VCF_CHARSET;
        java.lang.Class<?> wildcardClass1 = charset0.getClass();
        org.junit.Assert.assertNotNull(charset0);
        org.junit.Assert.assertNotNull(wildcardClass1);
    }

    @Test
    public void test03() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test03");
        java.lang.Object obj0 = new java.lang.Object();
        java.lang.Class<?> wildcardClass1 = obj0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
    }

    @Test
    public void test04() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test04");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (short) 0);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "0.00" + "'", str1, "0.00");
    }

    @Test
    public void test05() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test05");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFEncoder vCFEncoder3 = new htsjdk.variant.vcf.VCFEncoder(vCFHeader0, true, true);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: The VCF header must not be null.");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test06() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test06");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble(0.0d);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "0.00" + "'", str1, "0.00");
    }

    @Test
    public void test07() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test07");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) '4');
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "52.00" + "'", str1, "52.00");
    }

    @Test
    public void test08() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test08");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFEncoder vCFEncoder3 = new htsjdk.variant.vcf.VCFEncoder(vCFHeader0, true, false);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: The VCF header must not be null.");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test09() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test09");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 0);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "0.00" + "'", str1, "0.00");
    }

    @Test
    public void test10() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test10");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (byte) 10);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "10.00" + "'", str1, "10.00");
    }

    @Test
    public void test11() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test11");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFEncoder vCFEncoder3 = new htsjdk.variant.vcf.VCFEncoder(vCFHeader0, false, false);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: The VCF header must not be null.");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test12() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test12");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 100.0f);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "100.00" + "'", str1, "100.00");
    }

    @Test
    public void test13() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test13");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 100L);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "100.00" + "'", str1, "100.00");
    }

    @Test
    public void test14() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test14");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (short) 100);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "100.00" + "'", str1, "100.00");
    }

    @Test
    public void test15() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test15");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble(100.0d);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "100.00" + "'", str1, "100.00");
    }

    @Test
    public void test16() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test16");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (byte) 1);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "1.00" + "'", str1, "1.00");
    }

    @Test
    public void test17() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test17");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 1);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "1.00" + "'", str1, "1.00");
    }

    @Test
    public void test18() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test18");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (-1));
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "-1.000e+00" + "'", str1, "-1.000e+00");
    }

    @Test
    public void test19() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test19");
        htsjdk.variant.vcf.VCFHeader vCFHeader0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.vcf.VCFEncoder vCFEncoder3 = new htsjdk.variant.vcf.VCFEncoder(vCFHeader0, false, true);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: The VCF header must not be null.");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
    }

    @Test
    public void test20() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test20");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 10.0f);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "10.00" + "'", str1, "10.00");
    }

    @Test
    public void test21() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test21");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (byte) -1);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "-1.000e+00" + "'", str1, "-1.000e+00");
    }

    @Test
    public void test22() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test22");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((-1.0d));
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "-1.000e+00" + "'", str1, "-1.000e+00");
    }

    @Test
    public void test23() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test23");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 10);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "10.00" + "'", str1, "10.00");
    }

    @Test
    public void test24() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test24");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 100);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "100.00" + "'", str1, "100.00");
    }

    @Test
    public void test25() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test25");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (byte) 100);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "100.00" + "'", str1, "100.00");
    }

    @Test
    public void test26() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test26");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (-1.0f));
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "-1.000e+00" + "'", str1, "-1.000e+00");
    }

    @Test
    public void test27() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test27");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble(1.0d);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "1.00" + "'", str1, "1.00");
    }

    @Test
    public void test28() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test28");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (short) 1);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "1.00" + "'", str1, "1.00");
    }

    @Test
    public void test29() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test29");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (byte) 0);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "0.00" + "'", str1, "0.00");
    }

    @Test
    public void test30() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test30");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 0.0f);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "0.00" + "'", str1, "0.00");
    }

    @Test
    public void test31() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test31");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) '#');
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "35.00" + "'", str1, "35.00");
    }

    @Test
    public void test32() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test32");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (short) -1);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "-1.000e+00" + "'", str1, "-1.000e+00");
    }

    @Test
    public void test33() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test33");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 0L);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "0.00" + "'", str1, "0.00");
    }

    @Test
    public void test34() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test34");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) ' ');
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "32.00" + "'", str1, "32.00");
    }

    @Test
    public void test35() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test35");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 1L);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "1.00" + "'", str1, "1.00");
    }

    @Test
    public void test36() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test36");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (short) 10);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "10.00" + "'", str1, "10.00");
    }

    @Test
    public void test37() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test37");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) (-1L));
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "-1.000e+00" + "'", str1, "-1.000e+00");
    }

    @Test
    public void test38() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test38");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble(10.0d);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "10.00" + "'", str1, "10.00");
    }

    @Test
    public void test39() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test39");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 1.0f);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "1.00" + "'", str1, "1.00");
    }

    @Test
    public void test40() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test40");
        java.lang.String str1 = htsjdk.variant.vcf.VCFEncoder.formatVCFDouble((double) 10L);
        org.junit.Assert.assertEquals("'" + str1 + "' != '" + "10.00" + "'", str1, "10.00");
    }
}

