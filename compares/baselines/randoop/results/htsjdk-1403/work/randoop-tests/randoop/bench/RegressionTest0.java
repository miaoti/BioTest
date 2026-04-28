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
        java.lang.Object obj0 = new java.lang.Object();
        java.lang.Class<?> wildcardClass1 = obj0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
    }

    @Test
    public void test002() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test002");
        htsjdk.variant.variantcontext.VariantContext variantContext0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder1 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContext0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: VariantContextBuilder parent argument cannot be null in VariantContextBuilder");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test003() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test003");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.Allele[] alleleArray6 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList7 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean8 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList7, alleleArray6);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList7, 1);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray6);
        org.junit.Assert.assertArrayEquals(alleleArray6, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
    }

    @Test
    public void test004() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test004");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.variant.variantcontext.Allele> alleleList27 = variantContextBuilder5.getAlleles();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
    }

    @Test
    public void test005() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test005");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.stop((long) 100);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext10 = variantContextBuilder8.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Alleles cannot be null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
    }

    @Test
    public void test006() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test006");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray15 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList16 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean17 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList16, alleleArray15);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder5.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList16, (int) (byte) 100, (int) ' ');
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(alleleArray15);
        org.junit.Assert.assertArrayEquals(alleleArray15, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean17 + "' != '" + false + "'", boolean17 == false);
    }

    @Test
    public void test007() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test007");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray10 = new java.lang.String[] { "", "", "", "" };
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.alleles(strArray10);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(strArray10);
        org.junit.Assert.assertArrayEquals(strArray10, new java.lang.String[] { "", "", "", "" });
    }

    @Test
    public void test008() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test008");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        java.lang.Class<?> wildcardClass14 = variantContextBuilder12.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(wildcardClass14);
    }

    @Test
    public void test009() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test009");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.start(1L);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext20 = variantContextBuilder19.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test010() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test010");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.filters(strArray18);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext21 = variantContextBuilder19.make(true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test011() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test011");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.Allele[] alleleArray22 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList23 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList23, alleleArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList23);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder5.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList23, (int) (byte) 1, (int) (short) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(alleleArray22);
        org.junit.Assert.assertArrayEquals(alleleArray22, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + false + "'", boolean24 == false);
    }

    @Test
    public void test012() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test012");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.variant.variantcontext.Allele> alleleList14 = variantContextBuilder5.getAlleles();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
    }

    @Test
    public void test013() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test013");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.Allele[] alleleArray36 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList37 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean38 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37, alleleArray36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37);
        java.lang.String[] strArray44 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList45 = new java.util.ArrayList<java.lang.String>();
        boolean boolean46 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList45, strArray44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList45);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder23.alleles((java.util.List<java.lang.String>) strList45);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(alleleArray36);
        org.junit.Assert.assertArrayEquals(alleleArray36, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean38 + "' != '" + false + "'", boolean38 == false);
        org.junit.Assert.assertNotNull(strArray44);
        org.junit.Assert.assertArrayEquals(strArray44, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + true + "'", boolean46 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
    }

    @Test
    public void test014() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test014");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder1 = variantContextBuilder0.passFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder1);
    }

    @Test
    public void test015() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test015");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder5.fullyDecoded(false);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
    }

    @Test
    public void test016() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test016");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext21 = variantContextBuilder17.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: ID field cannot be the null or the empty string");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test017() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test017");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        boolean boolean7 = variantContextBuilder5.isFullyDecoded();
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test018() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test018");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection33 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder34.log10PError((double) (short) 100);
        java.lang.String[] strArray38 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet39 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean40 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet39, strArray38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder34.filters((java.util.Set<java.lang.String>) strSet39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder34.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap43 = variantContextBuilder34.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap44 = variantContextBuilder34.getAttributes();
        java.lang.String[] strArray48 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList49 = new java.util.ArrayList<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder34.rmAttributes((java.util.List<java.lang.String>) strList49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder28.rmAttributes((java.util.List<java.lang.String>) strList49);
        java.lang.Class<?> wildcardClass53 = strList49.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(strArray38);
        org.junit.Assert.assertArrayEquals(strArray38, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strMap43);
        org.junit.Assert.assertNotNull(strMap44);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(wildcardClass53);
    }

    @Test
    public void test019() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test019");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext14 = variantContextBuilder12.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test020() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test020");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder17.fullyDecoded(false);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext26 = variantContextBuilder25.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
    }

    @Test
    public void test021() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test021");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder7.putAttributes(strMap22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder23.unfiltered();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
    }

    @Test
    public void test022() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test022");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap15 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray19 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList20 = new java.util.ArrayList<java.lang.String>();
        boolean boolean21 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList20, strArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList20);
        long long23 = variantContextBuilder22.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strMap15);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertTrue("'" + long23 + "' != '" + 0L + "'", long23 == 0L);
    }

    @Test
    public void test023() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test023");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String str8 = variantContextBuilder5.getContig();
        java.util.List<htsjdk.variant.variantcontext.Allele> alleleList9 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.computeEndFromAlleles(alleleList9, (int) (byte) 1, (int) (byte) 1);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.List.get(int)\" because \"alleles\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertEquals("'" + str8 + "' != '" + "hi!" + "'", str8, "hi!");
    }

    @Test
    public void test024() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test024");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder7.putAttributes(strMap22);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection28 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder29.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray32 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList33 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean34 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList33, genotypeArray32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder29.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList33);
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder29.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection41 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder42.log10PError((double) (short) 100);
        java.lang.String[] strArray46 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet47 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean48 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet47, strArray46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder42.filters((java.util.Set<java.lang.String>) strSet47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder42.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection55 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection55);
        java.lang.String[] strArray59 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet60 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean61 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet60, strArray59);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder56.filters((java.util.Set<java.lang.String>) strSet60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder42.filters((java.util.Set<java.lang.String>) strSet60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder42.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection70 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection70);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder73 = variantContextBuilder71.log10PError((double) (short) 100);
        java.lang.String[] strArray75 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet76 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean77 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet76, strArray75);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder78 = variantContextBuilder71.filters((java.util.Set<java.lang.String>) strSet76);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder79 = variantContextBuilder71.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap80 = variantContextBuilder71.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap81 = variantContextBuilder71.getAttributes();
        java.lang.String[] strArray85 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList86 = new java.util.ArrayList<java.lang.String>();
        boolean boolean87 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList86, strArray85);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = variantContextBuilder71.rmAttributes((java.util.List<java.lang.String>) strList86);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder89 = variantContextBuilder65.rmAttributes((java.util.List<java.lang.String>) strList86);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder90 = variantContextBuilder29.rmAttributes((java.util.List<java.lang.String>) strList86);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder91 = variantContextBuilder7.alleles((java.util.List<java.lang.String>) strList86);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(genotypeArray32);
        org.junit.Assert.assertArrayEquals(genotypeArray32, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(strArray46);
        org.junit.Assert.assertArrayEquals(strArray46, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + true + "'", boolean48 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(strArray59);
        org.junit.Assert.assertArrayEquals(strArray59, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean61 + "' != '" + true + "'", boolean61 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder73);
        org.junit.Assert.assertNotNull(strArray75);
        org.junit.Assert.assertArrayEquals(strArray75, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean77 + "' != '" + true + "'", boolean77 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder78);
        org.junit.Assert.assertNotNull(variantContextBuilder79);
        org.junit.Assert.assertNotNull(strMap80);
        org.junit.Assert.assertNotNull(strMap81);
        org.junit.Assert.assertNotNull(strArray85);
        org.junit.Assert.assertArrayEquals(strArray85, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean87 + "' != '" + true + "'", boolean87 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder88);
        org.junit.Assert.assertNotNull(variantContextBuilder89);
        org.junit.Assert.assertNotNull(variantContextBuilder90);
    }

    @Test
    public void test025() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test025");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noID();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
    }

    @Test
    public void test026() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test026");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        boolean boolean15 = variantContextBuilder14.isFullyDecoded();
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder14.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList17, (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
    }

    @Test
    public void test027() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test027");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext9 = variantContextBuilder7.make(true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test028() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test028");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        long long29 = variantContextBuilder28.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertTrue("'" + long29 + "' != '" + 0L + "'", long29 == 0L);
    }

    @Test
    public void test029() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test029");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray18 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList19 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19, genotypeArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder9.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.variant.variantcontext.Allele> alleleList23 = variantContextBuilder22.getAlleles();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(genotypeArray18);
        org.junit.Assert.assertArrayEquals(genotypeArray18, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
    }

    @Test
    public void test030() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test030");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.chr("");
        java.lang.String[] strArray12 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder9.rmAttributes((java.util.List<java.lang.String>) strList13);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext17 = variantContextBuilder15.make(true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test031() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test031");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext13 = variantContextBuilder11.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Alleles cannot be null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
    }

    @Test
    public void test032() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test032");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext6 = variantContextBuilder5.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Alleles cannot be null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test033() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test033");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder21.source("");
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
    }

    @Test
    public void test034() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test034");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder10.log10PError((double) 0L);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray19 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.genotypes(genotypeArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder12.genotypes(genotypeArray19);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(genotypeArray19);
        org.junit.Assert.assertArrayEquals(genotypeArray19, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
    }

    @Test
    public void test035() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test035");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder15.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.source("hi!");
        java.util.Set<java.lang.String> strSet22 = variantContextBuilder21.getFilters();
        boolean boolean23 = variantContextBuilder21.isFullyDecoded();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strSet22);
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
    }

    @Test
    public void test036() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test036");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap15 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray17 = new java.lang.String[] { "hi!" };
        java.util.ArrayList<java.lang.String> strList18 = new java.util.ArrayList<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList18);
        htsjdk.variant.variantcontext.Allele[] alleleArray33 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList34 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34, alleleArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.Allele[] alleleArray52 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList53 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean54 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53, alleleArray52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        java.lang.String[] strArray60 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList61 = new java.util.ArrayList<java.lang.String>();
        boolean boolean62 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList61, strArray60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder57.rmAttributes((java.util.List<java.lang.String>) strList61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder57.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder38.attribute("", (java.lang.Object) variantContextBuilder65);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection71 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection71);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder72.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection79 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder80 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection79);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder82 = variantContextBuilder80.log10PError((double) (short) 100);
        java.lang.String[] strArray84 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet85 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean86 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet85, strArray84);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder87 = variantContextBuilder80.filters((java.util.Set<java.lang.String>) strSet85);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = variantContextBuilder80.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap89 = variantContextBuilder80.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder90 = variantContextBuilder74.putAttributes(strMap89);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder91 = variantContextBuilder38.attributes(strMap89);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder92 = variantContextBuilder5.attributes(strMap89);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strMap15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(alleleArray33);
        org.junit.Assert.assertArrayEquals(alleleArray33, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + false + "'", boolean35 == false);
        org.junit.Assert.assertNotNull(alleleArray52);
        org.junit.Assert.assertArrayEquals(alleleArray52, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean54 + "' != '" + false + "'", boolean54 == false);
        org.junit.Assert.assertNotNull(strArray60);
        org.junit.Assert.assertArrayEquals(strArray60, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean62 + "' != '" + true + "'", boolean62 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder74);
        org.junit.Assert.assertNotNull(variantContextBuilder82);
        org.junit.Assert.assertNotNull(strArray84);
        org.junit.Assert.assertArrayEquals(strArray84, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean86 + "' != '" + true + "'", boolean86 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder87);
        org.junit.Assert.assertNotNull(variantContextBuilder88);
        org.junit.Assert.assertNotNull(strMap89);
        org.junit.Assert.assertNotNull(variantContextBuilder90);
        org.junit.Assert.assertNotNull(variantContextBuilder91);
        org.junit.Assert.assertNotNull(variantContextBuilder92);
    }

    @Test
    public void test037() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test037");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection50 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder51.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection58 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.log10PError((double) (short) 100);
        java.lang.String[] strArray63 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet64 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet64, strArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder59.filters((java.util.Set<java.lang.String>) strSet64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder59.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap68 = variantContextBuilder59.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder53.putAttributes(strMap68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder17.attributes(strMap68);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection75 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection75);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder78 = variantContextBuilder76.log10PError((double) (short) 100);
        java.lang.String[] strArray80 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet81 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean82 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet81, strArray80);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder83 = variantContextBuilder76.filters((java.util.Set<java.lang.String>) strSet81);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder84 = variantContextBuilder76.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap85 = variantContextBuilder76.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap86 = variantContextBuilder76.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray91 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList92 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean93 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList92, alleleArray91);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder94 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList92);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder95 = variantContextBuilder76.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList92);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder97 = variantContextBuilder70.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList92, (int) '4');
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(strArray63);
        org.junit.Assert.assertArrayEquals(strArray63, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(strMap68);
        org.junit.Assert.assertNotNull(variantContextBuilder69);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(variantContextBuilder78);
        org.junit.Assert.assertNotNull(strArray80);
        org.junit.Assert.assertArrayEquals(strArray80, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean82 + "' != '" + true + "'", boolean82 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder83);
        org.junit.Assert.assertNotNull(variantContextBuilder84);
        org.junit.Assert.assertNotNull(strMap85);
        org.junit.Assert.assertNotNull(strMap86);
        org.junit.Assert.assertNotNull(alleleArray91);
        org.junit.Assert.assertArrayEquals(alleleArray91, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean93 + "' != '" + false + "'", boolean93 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder95);
    }

    @Test
    public void test038() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test038");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        long long27 = variantContextBuilder26.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertTrue("'" + long27 + "' != '" + 0L + "'", long27 == 0L);
    }

    @Test
    public void test039() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test039");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        long long27 = variantContextBuilder5.getStart();
        java.util.List<java.lang.String> strList28 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder5.alleles(strList28);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.List.size()\" because \"alleleStrings\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertTrue("'" + long27 + "' != '" + 0L + "'", long27 == 0L);
    }

    @Test
    public void test040() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test040");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        boolean boolean16 = variantContextBuilder13.isFullyDecoded();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
    }

    @Test
    public void test041() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test041");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection50 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder51.log10PError((double) (short) 100);
        java.lang.String[] strArray55 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet56 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean57 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet56, strArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder51.filters((java.util.Set<java.lang.String>) strSet56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder51.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap60 = variantContextBuilder51.getAttributes();
        java.lang.String[] strArray64 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder51.filters(strArray64);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder17.alleles(strArray64);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Unexpected base in allele bases 'HI!'");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(strArray55);
        org.junit.Assert.assertArrayEquals(strArray55, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean57 + "' != '" + true + "'", boolean57 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(strMap60);
        org.junit.Assert.assertNotNull(strArray64);
        org.junit.Assert.assertArrayEquals(strArray64, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder65);
    }

    @Test
    public void test042() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test042");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.filters(strArray18);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext21 = variantContextBuilder5.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test043() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test043");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray18 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList19 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19, genotypeArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder9.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext24 = variantContextBuilder9.make(true);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Alleles cannot be null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(genotypeArray18);
        org.junit.Assert.assertArrayEquals(genotypeArray18, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
    }

    @Test
    public void test044() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test044");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        long long12 = variantContextBuilder11.getStart();
        long long13 = variantContextBuilder11.getStop();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertTrue("'" + long12 + "' != '" + 0L + "'", long12 == 0L);
        org.junit.Assert.assertTrue("'" + long13 + "' != '" + 52L + "'", long13 == 52L);
    }

    @Test
    public void test045() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test045");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder10.loc(".", 0L, (long) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder10.stop(10L);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test046() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test046");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        long long13 = variantContextBuilder12.getStart();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder12.fullyDecoded(false);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertTrue("'" + long13 + "' != '" + 100L + "'", long13 == 100L);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test047() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test047");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        boolean boolean46 = variantContextBuilder45.isFullyDecoded();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + false + "'", boolean46 == false);
    }

    @Test
    public void test048() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test048");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder13.fullyDecoded(true);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext18 = variantContextBuilder13.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test049() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test049");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.copy();
        java.lang.String[] strArray16 = new java.lang.String[] { "hi!", "." };
        java.util.ArrayList<java.lang.String> strList17 = new java.util.ArrayList<java.lang.String>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList17, strArray16);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder13.alleles((java.util.List<java.lang.String>) strList17);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Unexpected base in allele bases 'HI!'");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray16);
        org.junit.Assert.assertArrayEquals(strArray16, new java.lang.String[] { "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
    }

    @Test
    public void test050() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test050");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder27.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder19.putAttributes(strMap36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder19.fullyDecoded(false);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder45.log10PError((double) (short) 100);
        java.lang.String[] strArray49 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet50 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean51 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet50, strArray49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder45.filters((java.util.Set<java.lang.String>) strSet50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder45.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder53.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray56 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList57 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean58 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList57, alleleArray56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder55.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder19.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList57);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(strArray49);
        org.junit.Assert.assertArrayEquals(strArray49, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + true + "'", boolean51 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(alleleArray56);
        org.junit.Assert.assertArrayEquals(alleleArray56, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean58 + "' != '" + false + "'", boolean58 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
    }

    @Test
    public void test051() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test051");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.start((long) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray25 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList26 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList26, genotypeArray25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder22.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList26);
        java.util.Map<java.lang.String, java.lang.Object> strMap29 = variantContextBuilder22.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder14.attributes(strMap29);
        java.lang.String str31 = variantContextBuilder14.getID();
        long long32 = variantContextBuilder14.getStart();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(genotypeArray25);
        org.junit.Assert.assertArrayEquals(genotypeArray25, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(strMap29);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertEquals("'" + str31 + "' != '" + "." + "'", str31, ".");
        org.junit.Assert.assertTrue("'" + long32 + "' != '" + 10L + "'", long32 == 10L);
    }

    @Test
    public void test052() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test052");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray18 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList19 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19, genotypeArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder9.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        java.lang.Class<?> wildcardClass23 = variantContextBuilder22.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(genotypeArray18);
        org.junit.Assert.assertArrayEquals(genotypeArray18, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(wildcardClass23);
    }

    @Test
    public void test053() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test053");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder7.putAttributes(strMap22);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext24 = variantContextBuilder7.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
    }

    @Test
    public void test054() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test054");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder2 = variantContextBuilder0.id(".");
        long long3 = variantContextBuilder2.getStop();
        org.junit.Assert.assertNotNull(variantContextBuilder2);
        org.junit.Assert.assertTrue("'" + long3 + "' != '" + (-1L) + "'", long3 == (-1L));
    }

    @Test
    public void test055() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test055");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder13.start(10L);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.Allele[] alleleArray50 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList51 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean52 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList51, alleleArray50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList51);
        java.lang.String[] strArray58 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList59 = new java.util.ArrayList<java.lang.String>();
        boolean boolean60 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList59, strArray58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder55.rmAttributes((java.util.List<java.lang.String>) strList59);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder55.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder36.attribute("", (java.lang.Object) variantContextBuilder63);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection69 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection69);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder70.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection77 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder78 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection77);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder80 = variantContextBuilder78.log10PError((double) (short) 100);
        java.lang.String[] strArray82 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet83 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean84 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet83, strArray82);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder85 = variantContextBuilder78.filters((java.util.Set<java.lang.String>) strSet83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = variantContextBuilder78.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap87 = variantContextBuilder78.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = variantContextBuilder72.putAttributes(strMap87);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder89 = variantContextBuilder36.attributes(strMap87);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder90 = variantContextBuilder18.putAttributes(strMap87);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(alleleArray50);
        org.junit.Assert.assertArrayEquals(alleleArray50, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean52 + "' != '" + false + "'", boolean52 == false);
        org.junit.Assert.assertNotNull(strArray58);
        org.junit.Assert.assertArrayEquals(strArray58, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean60 + "' != '" + true + "'", boolean60 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder72);
        org.junit.Assert.assertNotNull(variantContextBuilder80);
        org.junit.Assert.assertNotNull(strArray82);
        org.junit.Assert.assertArrayEquals(strArray82, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean84 + "' != '" + true + "'", boolean84 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder85);
        org.junit.Assert.assertNotNull(variantContextBuilder86);
        org.junit.Assert.assertNotNull(strMap87);
        org.junit.Assert.assertNotNull(variantContextBuilder88);
        org.junit.Assert.assertNotNull(variantContextBuilder89);
        org.junit.Assert.assertNotNull(variantContextBuilder90);
    }

    @Test
    public void test056() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test056");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        long long20 = variantContextBuilder17.getStart();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext21 = variantContextBuilder17.getGenotypes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertTrue("'" + long20 + "' != '" + 10L + "'", long20 == 10L);
        org.junit.Assert.assertNotNull(genotypesContext21);
    }

    @Test
    public void test057() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test057");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder18.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection46 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.log10PError((double) (short) 100);
        java.lang.String[] strArray51 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet52 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean53 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet52, strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder47.filters((java.util.Set<java.lang.String>) strSet52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder47.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap56 = variantContextBuilder47.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap57 = variantContextBuilder47.getAttributes();
        java.lang.String[] strArray61 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList62 = new java.util.ArrayList<java.lang.String>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList62, strArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder47.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder5.noGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strArray51);
        org.junit.Assert.assertArrayEquals(strArray51, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean53 + "' != '" + true + "'", boolean53 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strMap56);
        org.junit.Assert.assertNotNull(strMap57);
        org.junit.Assert.assertNotNull(strArray61);
        org.junit.Assert.assertArrayEquals(strArray61, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + true + "'", boolean63 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
    }

    @Test
    public void test058() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test058");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection24 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection24);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray26 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder25.genotypes(genotypeArray26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder17.genotypes(genotypeArray26);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection33 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder34.log10PError((double) (short) 100);
        java.lang.String[] strArray38 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet39 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean40 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet39, strArray38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder34.filters((java.util.Set<java.lang.String>) strSet39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder34.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap43 = variantContextBuilder34.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap44 = variantContextBuilder34.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder28.putAttributes(strMap44);
        long long46 = variantContextBuilder28.getStop();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(genotypeArray26);
        org.junit.Assert.assertArrayEquals(genotypeArray26, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(strArray38);
        org.junit.Assert.assertArrayEquals(strArray38, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strMap43);
        org.junit.Assert.assertNotNull(strMap44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertTrue("'" + long46 + "' != '" + 0L + "'", long46 == 0L);
    }

    @Test
    public void test059() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test059");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.chr("");
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder5.alleles((java.util.List<java.lang.String>) strList21);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
    }

    @Test
    public void test060() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test060");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.chr("");
        java.lang.String[] strArray12 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder9.rmAttributes((java.util.List<java.lang.String>) strList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection22 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder23.log10PError((double) (short) 100);
        java.lang.String[] strArray27 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet28 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean29 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet28, strArray27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder23.filters((java.util.Set<java.lang.String>) strSet28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder23.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap32 = variantContextBuilder23.getAttributes();
        java.lang.String[] strArray36 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder23.filters(strArray36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder15.filters(strArray36);
        htsjdk.variant.variantcontext.Allele[] alleleArray55 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList56 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean57 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56, alleleArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 52L, (long) 1, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder15.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList56, (-1));
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(strArray27);
        org.junit.Assert.assertArrayEquals(strArray27, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + true + "'", boolean29 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(strMap32);
        org.junit.Assert.assertNotNull(strArray36);
        org.junit.Assert.assertArrayEquals(strArray36, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(alleleArray55);
        org.junit.Assert.assertArrayEquals(alleleArray55, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean57 + "' != '" + false + "'", boolean57 == false);
    }

    @Test
    public void test061() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test061");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder32.log10PError((double) (short) 100);
        java.lang.String[] strArray36 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet37 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean38 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet37, strArray36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder32.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder40.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray43 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList44 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44, alleleArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder42.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder42.source("hi!");
        java.util.Set<java.lang.String> strSet49 = variantContextBuilder48.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder26.filters(strSet49);
        htsjdk.variant.variantcontext.Allele[] alleleArray63 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList64 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList64, alleleArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList64);
        java.lang.String[] strArray70 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder68.filters(strArray70);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder50.alleles(strArray70);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Unexpected base in allele bases 'HI!'");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(strArray36);
        org.junit.Assert.assertArrayEquals(strArray36, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean38 + "' != '" + true + "'", boolean38 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(alleleArray43);
        org.junit.Assert.assertArrayEquals(alleleArray43, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + false + "'", boolean45 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(strSet49);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(alleleArray63);
        org.junit.Assert.assertArrayEquals(alleleArray63, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + false + "'", boolean65 == false);
        org.junit.Assert.assertNotNull(strArray70);
        org.junit.Assert.assertArrayEquals(strArray70, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder71);
    }

    @Test
    public void test062() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test062");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.start((long) 100);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
    }

    @Test
    public void test063() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test063");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.lang.String str17 = variantContextBuilder13.getID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder13.log10PError((double) (short) 100);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "." + "'", str17, ".");
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test064() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test064");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Map<java.lang.String, java.lang.Object> strMap29 = variantContextBuilder13.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap30 = variantContextBuilder13.getAttributes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(strMap29);
        org.junit.Assert.assertNotNull(strMap30);
    }

    @Test
    public void test065() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test065");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder17.fullyDecoded(false);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder27.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap37 = variantContextBuilder27.getAttributes();
        java.lang.String[] strArray41 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList42 = new java.util.ArrayList<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder27.rmAttributes((java.util.List<java.lang.String>) strList42);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.alleles((java.util.List<java.lang.String>) strList42);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(strMap37);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
    }

    @Test
    public void test066() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test066");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap15 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray19 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList20 = new java.util.ArrayList<java.lang.String>();
        boolean boolean21 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList20, strArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder5.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder23.copy();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strMap15);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
    }

    @Test
    public void test067() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test067");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection33 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder34.log10PError((double) (short) 100);
        java.lang.String[] strArray38 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet39 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean40 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet39, strArray38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder34.filters((java.util.Set<java.lang.String>) strSet39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder34.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap43 = variantContextBuilder34.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap44 = variantContextBuilder34.getAttributes();
        java.lang.String[] strArray48 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList49 = new java.util.ArrayList<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder34.rmAttributes((java.util.List<java.lang.String>) strList49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder28.rmAttributes((java.util.List<java.lang.String>) strList49);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext54 = variantContextBuilder52.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(strArray38);
        org.junit.Assert.assertArrayEquals(strArray38, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strMap43);
        org.junit.Assert.assertNotNull(strMap44);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
    }

    @Test
    public void test068() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test068");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        java.util.Set<java.lang.String> strSet8 = variantContextBuilder7.getFilters();
        java.util.Map<java.lang.String, java.lang.Object> strMap9 = variantContextBuilder7.getAttributes();
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNull(strSet8);
        org.junit.Assert.assertNotNull(strMap9);
    }

    @Test
    public void test069() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test069");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder1 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder0);
    }

    @Test
    public void test070() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test070");
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 52L, (long) 1, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection27 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection27);
        java.lang.String[] strArray31 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder28.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet32);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
    }

    @Test
    public void test071() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test071");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        java.util.Set<java.lang.String> strSet46 = variantContextBuilder45.getFilters();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNull(strSet46);
    }

    @Test
    public void test072() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test072");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.start((long) 10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder16.copy();
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext18 = variantContextBuilder17.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
    }

    @Test
    public void test073() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test073");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder21.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray24 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList25 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean26 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList25, alleleArray24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder23.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.attribute("hi!", (java.lang.Object) variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(alleleArray24);
        org.junit.Assert.assertArrayEquals(alleleArray24, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
    }

    @Test
    public void test074() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test074");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.chr("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder7.log10PError((double) 100.0f);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
    }

    @Test
    public void test075() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test075");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.lang.Class<?> wildcardClass16 = variantContextBuilder13.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(wildcardClass16);
    }

    @Test
    public void test076() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test076");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.chr("");
        java.lang.String[] strArray12 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder9.rmAttributes((java.util.List<java.lang.String>) strList13);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext17 = variantContextBuilder15.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test077() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test077");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection37 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder38.log10PError((double) (short) 100);
        java.lang.String[] strArray42 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet43 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean44 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet43, strArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder38.filters((java.util.Set<java.lang.String>) strSet43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder38.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap47 = variantContextBuilder38.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap48 = variantContextBuilder38.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray53 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList54 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean55 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList54, alleleArray53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder38.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "hi!", (long) ' ', (long) ' ', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList54);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder28.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList54, (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertNotNull(strArray42);
        org.junit.Assert.assertArrayEquals(strArray42, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean44 + "' != '" + true + "'", boolean44 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(strMap47);
        org.junit.Assert.assertNotNull(strMap48);
        org.junit.Assert.assertNotNull(alleleArray53);
        org.junit.Assert.assertArrayEquals(alleleArray53, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean55 + "' != '" + false + "'", boolean55 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
    }

    @Test
    public void test078() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test078");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.start((long) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        long long23 = variantContextBuilder22.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext24 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder22.genotypes(genotypesContext24);
        java.lang.String[] strArray29 = new java.lang.String[] { "hi!", "hi!", "." };
        java.util.ArrayList<java.lang.String> strList30 = new java.util.ArrayList<java.lang.String>();
        boolean boolean31 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList30, strArray29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder25.rmAttributes((java.util.List<java.lang.String>) strList30);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder16.alleles((java.util.List<java.lang.String>) strList30);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Unexpected base in allele bases 'HI!'");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertTrue("'" + long23 + "' != '" + 52L + "'", long23 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(strArray29);
        org.junit.Assert.assertArrayEquals(strArray29, new java.lang.String[] { "hi!", "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + true + "'", boolean31 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
    }

    @Test
    public void test079() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test079");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        long long11 = variantContextBuilder10.getStart();
        java.lang.Class<?> wildcardClass12 = variantContextBuilder10.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertTrue("'" + long11 + "' != '" + 10L + "'", long11 == 10L);
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test080() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test080");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.filters(strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection27 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection27);
        java.lang.Class<?> wildcardClass29 = variantContextBuilder28.getClass();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder21.attribute("", (java.lang.Object) wildcardClass29);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(wildcardClass29);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
    }

    @Test
    public void test081() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test081");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection16 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.chr("");
        java.lang.String[] strArray24 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList25 = new java.util.ArrayList<java.lang.String>();
        boolean boolean26 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList25, strArray24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder21.rmAttributes((java.util.List<java.lang.String>) strList25);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection32 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder33.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection42 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder43.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray46 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList47 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean48 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList47, genotypeArray46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder43.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder37.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder21.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList47);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strArray24);
        org.junit.Assert.assertArrayEquals(strArray24, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + true + "'", boolean26 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(genotypeArray46);
        org.junit.Assert.assertArrayEquals(genotypeArray46, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + false + "'", boolean48 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
    }

    @Test
    public void test082() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test082");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        long long10 = variantContextBuilder9.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertTrue("'" + long10 + "' != '" + 10L + "'", long10 == 10L);
    }

    @Test
    public void test083() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test083");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.log10PError((-1.0d));
        boolean boolean10 = variantContextBuilder9.isFullyDecoded();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test084() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test084");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        boolean boolean16 = variantContextBuilder15.isFullyDecoded();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.noID();
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
    }

    @Test
    public void test085() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test085");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.start((long) (short) 10);
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.variant.variantcontext.Allele> alleleList10 = variantContextBuilder9.getAlleles();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
    }

    @Test
    public void test086() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test086");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection33 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder34.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.chr("");
        java.lang.String[] strArray41 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList42 = new java.util.ArrayList<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder38.rmAttributes((java.util.List<java.lang.String>) strList42);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder5.alleles((java.util.List<java.lang.String>) strList42);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
    }

    @Test
    public void test087() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test087");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.start((long) (short) 0);
        long long14 = variantContextBuilder11.getStop();
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
    }

    @Test
    public void test088() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test088");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.log10PError((-1.0d));
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray18 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList19 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19, genotypeArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder15.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder15.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection28 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder29.log10PError((double) (short) 100);
        java.lang.String[] strArray33 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet34 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder29.filters((java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder29.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap38 = variantContextBuilder29.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap39 = variantContextBuilder29.getAttributes();
        java.lang.String[] strArray41 = new java.lang.String[] { "hi!" };
        java.util.ArrayList<java.lang.String> strList42 = new java.util.ArrayList<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder29.rmAttributes((java.util.List<java.lang.String>) strList42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder15.rmAttributes((java.util.List<java.lang.String>) strList42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList42);
        long long47 = variantContextBuilder5.getStop();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(genotypeArray18);
        org.junit.Assert.assertArrayEquals(genotypeArray18, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(strMap38);
        org.junit.Assert.assertNotNull(strMap39);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertTrue("'" + long47 + "' != '" + 52L + "'", long47 == 52L);
    }

    @Test
    public void test089() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test089");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.filters(strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext22 = variantContextBuilder21.getGenotypes();
        long long23 = variantContextBuilder21.getStop();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(genotypesContext22);
        org.junit.Assert.assertTrue("'" + long23 + "' != '" + 52L + "'", long23 == 52L);
    }

    @Test
    public void test090() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test090");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        long long14 = variantContextBuilder13.getStop();
        htsjdk.variant.variantcontext.Allele[] alleleArray23 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList24 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24, alleleArray23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.chr("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection36 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder37.log10PError((double) (short) 100);
        java.lang.String[] strArray41 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet42 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder37.filters((java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder37.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap46 = variantContextBuilder37.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap47 = variantContextBuilder37.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray52 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList53 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean54 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53, alleleArray52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder37.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder28.attribute("hi!", (java.lang.Object) variantContextBuilder56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
        org.junit.Assert.assertNotNull(alleleArray23);
        org.junit.Assert.assertArrayEquals(alleleArray23, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(strMap46);
        org.junit.Assert.assertNotNull(strMap47);
        org.junit.Assert.assertNotNull(alleleArray52);
        org.junit.Assert.assertArrayEquals(alleleArray52, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean54 + "' != '" + false + "'", boolean54 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
    }

    @Test
    public void test091() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test091");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.chr("");
        java.lang.String[] strArray12 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder9.rmAttributes((java.util.List<java.lang.String>) strList13);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection20 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder21.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection30 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder31.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray34 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList35 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean36 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList35, genotypeArray34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder31.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder25.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder9.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList35);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext40 = variantContextBuilder9.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(genotypeArray34);
        org.junit.Assert.assertArrayEquals(genotypeArray34, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + false + "'", boolean36 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(genotypesContext40);
    }

    @Test
    public void test092() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test092");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        long long7 = variantContextBuilder5.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertTrue("'" + long7 + "' != '" + 0L + "'", long7 == 0L);
    }

    @Test
    public void test093() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test093");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        java.lang.String[] strArray25 = new java.lang.String[] { "hi!", "", "hi!" };
        java.util.ArrayList<java.lang.String> strList26 = new java.util.ArrayList<java.lang.String>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList26, strArray25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder21.rmAttributes((java.util.List<java.lang.String>) strList26);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strArray25);
        org.junit.Assert.assertArrayEquals(strArray25, new java.lang.String[] { "hi!", "", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + true + "'", boolean27 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
    }

    @Test
    public void test094() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test094");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection20 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection20);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray22 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder21.genotypes(genotypeArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder13.genotypes(genotypeArray22);
        htsjdk.variant.variantcontext.Allele[] alleleArray37 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList38 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean39 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38, alleleArray37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder42.id("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection49 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection49);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray51 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder50.genotypes(genotypeArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder42.genotypes(genotypeArray51);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection58 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.log10PError((double) (short) 100);
        java.lang.String[] strArray63 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet64 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet64, strArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder59.filters((java.util.Set<java.lang.String>) strSet64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder59.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap68 = variantContextBuilder59.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap69 = variantContextBuilder59.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder53.putAttributes(strMap69);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder24.putAttributes(strMap69);
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(genotypeArray22);
        org.junit.Assert.assertArrayEquals(genotypeArray22, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(alleleArray37);
        org.junit.Assert.assertArrayEquals(alleleArray37, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + false + "'", boolean39 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(genotypeArray51);
        org.junit.Assert.assertArrayEquals(genotypeArray51, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(strArray63);
        org.junit.Assert.assertArrayEquals(strArray63, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(strMap68);
        org.junit.Assert.assertNotNull(strMap69);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
    }

    @Test
    public void test095() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test095");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder18.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection46 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.log10PError((double) (short) 100);
        java.lang.String[] strArray51 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet52 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean53 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet52, strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder47.filters((java.util.Set<java.lang.String>) strSet52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder47.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap56 = variantContextBuilder47.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap57 = variantContextBuilder47.getAttributes();
        java.lang.String[] strArray61 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList62 = new java.util.ArrayList<java.lang.String>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList62, strArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder47.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext67 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder5.genotypes(genotypesContext67);
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.variant.variantcontext.Allele> alleleList69 = variantContextBuilder5.getAlleles();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strArray51);
        org.junit.Assert.assertArrayEquals(strArray51, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean53 + "' != '" + true + "'", boolean53 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strMap56);
        org.junit.Assert.assertNotNull(strMap57);
        org.junit.Assert.assertNotNull(strArray61);
        org.junit.Assert.assertArrayEquals(strArray61, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + true + "'", boolean63 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
    }

    @Test
    public void test096() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test096");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder5.chr("hi!");
        long long17 = variantContextBuilder5.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertTrue("'" + long17 + "' != '" + 0L + "'", long17 == 0L);
    }

    @Test
    public void test097() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test097");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.id("");
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext22 = variantContextBuilder21.getGenotypes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(genotypesContext22);
    }

    @Test
    public void test098() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test098");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.source("");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
    }

    @Test
    public void test099() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test099");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        java.util.Set<java.lang.String> strSet8 = variantContextBuilder7.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder7.id("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder7.loc("hi!", (long) '#', (long) 10);
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNull(strSet8);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
    }

    @Test
    public void test100() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test100");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder15.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder19.passFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder20.id("");
        java.util.Map<java.lang.String, java.lang.Object> strMap23 = variantContextBuilder20.getAttributes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(strMap23);
    }

    @Test
    public void test101() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test101");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap15 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray20 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList21 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21, alleleArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder5.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.rmAttribute("hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strMap15);
        org.junit.Assert.assertNotNull(alleleArray20);
        org.junit.Assert.assertArrayEquals(alleleArray20, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + false + "'", boolean22 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
    }

    @Test
    public void test102() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test102");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.start((long) (short) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.log10PError((double) (short) 100);
        java.lang.String[] strArray19 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet20 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean21 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet20, strArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder15.filters((java.util.Set<java.lang.String>) strSet20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder15.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap24 = variantContextBuilder15.getAttributes();
        java.lang.String[] strArray28 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder15.filters(strArray28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder29.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext32 = variantContextBuilder31.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder7.genotypesNoValidation(genotypesContext32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder7.unfiltered();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + true + "'", boolean21 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(strMap24);
        org.junit.Assert.assertNotNull(strArray28);
        org.junit.Assert.assertArrayEquals(strArray28, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(genotypesContext32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
    }

    @Test
    public void test103() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test103");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.lang.String str7 = variantContextBuilder5.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection13 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.log10PError((double) (short) 100);
        java.lang.String[] strArray18 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet19 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet19, strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder14.filters((java.util.Set<java.lang.String>) strSet19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder14.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap23 = variantContextBuilder14.getAttributes();
        java.lang.String[] strArray27 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder14.filters(strArray27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder8.filters(strArray27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder8);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection35 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.log10PError((double) (short) 100);
        java.lang.String[] strArray40 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet41 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean42 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet41, strArray40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder36.filters((java.util.Set<java.lang.String>) strSet41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder44.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap47 = variantContextBuilder44.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection52 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder53.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder55.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap58 = variantContextBuilder57.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder44.attributes(strMap58);
        java.util.Map<java.lang.String, java.lang.Object> strMap60 = variantContextBuilder44.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder30.putAttributes(strMap60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder30.passFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "hi!" + "'", str7, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(strMap23);
        org.junit.Assert.assertNotNull(strArray27);
        org.junit.Assert.assertArrayEquals(strArray27, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray40);
        org.junit.Assert.assertArrayEquals(strArray40, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean42 + "' != '" + true + "'", boolean42 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(strMap47);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(strMap58);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(strMap60);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
    }

    @Test
    public void test104() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test104");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder15.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        java.lang.String[] strArray26 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet27 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean28 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet27, strArray26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder22.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection35 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection35);
        java.lang.String[] strArray39 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet40 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.filters((java.util.Set<java.lang.String>) strSet40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet40);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection48 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder49.log10PError((double) (short) 100);
        java.lang.String[] strArray53 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet54 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean55 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet54, strArray53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder49.filters((java.util.Set<java.lang.String>) strSet54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder49.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder57.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray60 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList61 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean62 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList61, alleleArray60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder59.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder59.source("hi!");
        java.util.Set<java.lang.String> strSet66 = variantContextBuilder65.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder43.filters(strSet66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder15.filters(strSet66);
        long long69 = variantContextBuilder15.getStart();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection74 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder75 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection74);
        java.lang.String[] strArray78 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet79 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean80 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet79, strArray78);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder81 = variantContextBuilder75.filters((java.util.Set<java.lang.String>) strSet79);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder83 = variantContextBuilder81.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection84 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder85 = variantContextBuilder83.genotypes(genotypeCollection84);
        boolean boolean86 = variantContextBuilder85.isFullyDecoded();
        java.util.Map<java.lang.String, java.lang.Object> strMap87 = variantContextBuilder85.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = variantContextBuilder15.putAttributes(strMap87);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(strArray26);
        org.junit.Assert.assertArrayEquals(strArray26, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(strArray53);
        org.junit.Assert.assertArrayEquals(strArray53, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean55 + "' != '" + true + "'", boolean55 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(alleleArray60);
        org.junit.Assert.assertArrayEquals(alleleArray60, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean62 + "' != '" + false + "'", boolean62 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(strSet66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
        org.junit.Assert.assertTrue("'" + long69 + "' != '" + 0L + "'", long69 == 0L);
        org.junit.Assert.assertNotNull(strArray78);
        org.junit.Assert.assertArrayEquals(strArray78, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean80 + "' != '" + true + "'", boolean80 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder81);
        org.junit.Assert.assertNotNull(variantContextBuilder83);
        org.junit.Assert.assertNotNull(variantContextBuilder85);
        org.junit.Assert.assertTrue("'" + boolean86 + "' != '" + false + "'", boolean86 == false);
        org.junit.Assert.assertNotNull(strMap87);
        org.junit.Assert.assertNotNull(variantContextBuilder88);
    }

    @Test
    public void test105() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test105");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.filters(strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.start((long) (short) 0);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext23 = variantContextBuilder19.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
    }

    @Test
    public void test106() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test106");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        htsjdk.variant.variantcontext.Allele[] alleleArray13 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList14 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean15 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList14, alleleArray13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList14);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList14, (int) '#', (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(alleleArray13);
        org.junit.Assert.assertArrayEquals(alleleArray13, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
    }

    @Test
    public void test107() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test107");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection34 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection34);
        long long36 = variantContextBuilder35.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext37 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder35.genotypes(genotypesContext37);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        java.lang.String[] strArray48 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet49 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder45.filters((java.util.Set<java.lang.String>) strSet49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder38.attribute(".", (java.lang.Object) variantContextBuilder45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder28.attribute("", (java.lang.Object) variantContextBuilder38);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection58 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.log10PError((double) (short) 100);
        java.lang.String[] strArray63 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet64 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet64, strArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder59.filters((java.util.Set<java.lang.String>) strSet64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder59.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder67.fullyDecoded(true);
        htsjdk.variant.variantcontext.Allele[] alleleArray83 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList84 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean85 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84, alleleArray83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder87 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84);
        java.lang.String[] strArray90 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder91 = variantContextBuilder88.filters(strArray90);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder92 = variantContextBuilder70.filters(strArray90);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder93 = variantContextBuilder38.filters(strArray90);
        java.lang.Class<?> wildcardClass94 = variantContextBuilder38.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertTrue("'" + long36 + "' != '" + 52L + "'", long36 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(strArray63);
        org.junit.Assert.assertArrayEquals(strArray63, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(alleleArray83);
        org.junit.Assert.assertArrayEquals(alleleArray83, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean85 + "' != '" + false + "'", boolean85 == false);
        org.junit.Assert.assertNotNull(strArray90);
        org.junit.Assert.assertArrayEquals(strArray90, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder91);
        org.junit.Assert.assertNotNull(variantContextBuilder92);
        org.junit.Assert.assertNotNull(variantContextBuilder93);
        org.junit.Assert.assertNotNull(wildcardClass94);
    }

    @Test
    public void test108() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test108");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder18.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection46 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.log10PError((double) (short) 100);
        java.lang.String[] strArray51 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet52 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean53 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet52, strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder47.filters((java.util.Set<java.lang.String>) strSet52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder47.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap56 = variantContextBuilder47.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap57 = variantContextBuilder47.getAttributes();
        java.lang.String[] strArray61 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList62 = new java.util.ArrayList<java.lang.String>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList62, strArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder47.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder66.noGenotypes();
        java.lang.Class<?> wildcardClass68 = variantContextBuilder67.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strArray51);
        org.junit.Assert.assertArrayEquals(strArray51, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean53 + "' != '" + true + "'", boolean53 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strMap56);
        org.junit.Assert.assertNotNull(strMap57);
        org.junit.Assert.assertNotNull(strArray61);
        org.junit.Assert.assertArrayEquals(strArray61, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + true + "'", boolean63 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(wildcardClass68);
    }

    @Test
    public void test109() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test109");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection34 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection34);
        long long36 = variantContextBuilder35.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext37 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder35.genotypes(genotypesContext37);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        java.lang.String[] strArray48 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet49 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder45.filters((java.util.Set<java.lang.String>) strSet49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder38.attribute(".", (java.lang.Object) variantContextBuilder45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder28.attribute("", (java.lang.Object) variantContextBuilder38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder53.start((long) (short) -1);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext57 = variantContextBuilder55.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertTrue("'" + long36 + "' != '" + 52L + "'", long36 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
    }

    @Test
    public void test110() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test110");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection50 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder51.log10PError((double) (short) 100);
        java.lang.String[] strArray55 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet56 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean57 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet56, strArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder51.filters((java.util.Set<java.lang.String>) strSet56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder17.filters((java.util.Set<java.lang.String>) strSet56);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(strArray55);
        org.junit.Assert.assertArrayEquals(strArray55, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean57 + "' != '" + true + "'", boolean57 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
    }

    @Test
    public void test111() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test111");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        long long14 = variantContextBuilder13.getStop();
        htsjdk.variant.variantcontext.Allele[] alleleArray23 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList24 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24, alleleArray23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.chr("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection35 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.log10PError((double) (short) 100);
        java.lang.String[] strArray40 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet41 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean42 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet41, strArray40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder36.filters((java.util.Set<java.lang.String>) strSet41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder44.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray47 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList48 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean49 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48, alleleArray47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder46.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder30.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
        org.junit.Assert.assertNotNull(alleleArray23);
        org.junit.Assert.assertArrayEquals(alleleArray23, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray40);
        org.junit.Assert.assertArrayEquals(strArray40, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean42 + "' != '" + true + "'", boolean42 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(alleleArray47);
        org.junit.Assert.assertArrayEquals(alleleArray47, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean49 + "' != '" + false + "'", boolean49 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
    }

    @Test
    public void test112() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test112");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder27.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder19.putAttributes(strMap36);
        java.util.Map<java.lang.String, java.lang.Object> strMap38 = variantContextBuilder37.getAttributes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(strMap38);
    }

    @Test
    public void test113() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test113");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection33 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder34.log10PError((double) (short) 100);
        java.lang.String[] strArray38 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet39 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean40 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet39, strArray38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder34.filters((java.util.Set<java.lang.String>) strSet39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder34.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap43 = variantContextBuilder34.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap44 = variantContextBuilder34.getAttributes();
        java.lang.String[] strArray48 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList49 = new java.util.ArrayList<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder34.rmAttributes((java.util.List<java.lang.String>) strList49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder28.rmAttributes((java.util.List<java.lang.String>) strList49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder52.id(".");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(strArray38);
        org.junit.Assert.assertArrayEquals(strArray38, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean40 + "' != '" + true + "'", boolean40 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strMap43);
        org.junit.Assert.assertNotNull(strMap44);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
    }

    @Test
    public void test114() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test114");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder18.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection46 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.log10PError((double) (short) 100);
        java.lang.String[] strArray51 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet52 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean53 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet52, strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder47.filters((java.util.Set<java.lang.String>) strSet52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder47.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap56 = variantContextBuilder47.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap57 = variantContextBuilder47.getAttributes();
        java.lang.String[] strArray61 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList62 = new java.util.ArrayList<java.lang.String>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList62, strArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder47.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder5.copy();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strArray51);
        org.junit.Assert.assertArrayEquals(strArray51, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean53 + "' != '" + true + "'", boolean53 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strMap56);
        org.junit.Assert.assertNotNull(strMap57);
        org.junit.Assert.assertNotNull(strArray61);
        org.junit.Assert.assertArrayEquals(strArray61, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + true + "'", boolean63 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
    }

    @Test
    public void test115() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test115");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.Allele[] alleleArray20 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList21 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21, alleleArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.Allele[] alleleArray39 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList40 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList40, alleleArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList40);
        java.lang.String[] strArray47 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList48 = new java.util.ArrayList<java.lang.String>();
        boolean boolean49 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList48, strArray47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder44.rmAttributes((java.util.List<java.lang.String>) strList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder44.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder25.attribute("", (java.lang.Object) variantContextBuilder52);
        htsjdk.variant.variantcontext.Allele[] alleleArray66 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList67 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean68 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList67, alleleArray66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList67);
        java.lang.String[] strArray73 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder71.filters(strArray73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder75 = variantContextBuilder25.filters(strArray73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder5.filters(strArray73);
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(alleleArray20);
        org.junit.Assert.assertArrayEquals(alleleArray20, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + false + "'", boolean22 == false);
        org.junit.Assert.assertNotNull(alleleArray39);
        org.junit.Assert.assertArrayEquals(alleleArray39, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + false + "'", boolean41 == false);
        org.junit.Assert.assertNotNull(strArray47);
        org.junit.Assert.assertArrayEquals(strArray47, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean49 + "' != '" + true + "'", boolean49 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(alleleArray66);
        org.junit.Assert.assertArrayEquals(alleleArray66, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean68 + "' != '" + false + "'", boolean68 == false);
        org.junit.Assert.assertNotNull(strArray73);
        org.junit.Assert.assertArrayEquals(strArray73, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder74);
        org.junit.Assert.assertNotNull(variantContextBuilder75);
        org.junit.Assert.assertNotNull(variantContextBuilder76);
    }

    @Test
    public void test116() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test116");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection29 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder30.log10PError((double) (short) 100);
        java.lang.String[] strArray34 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet35 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean36 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet35, strArray34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder30.filters((java.util.Set<java.lang.String>) strSet35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder30.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap39 = variantContextBuilder30.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap40 = variantContextBuilder30.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray45 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList46 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean47 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46, alleleArray45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder30.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "hi!", (long) ' ', (long) ' ', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder17.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder51.noGenotypes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(strArray34);
        org.junit.Assert.assertArrayEquals(strArray34, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + true + "'", boolean36 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strMap39);
        org.junit.Assert.assertNotNull(strMap40);
        org.junit.Assert.assertNotNull(alleleArray45);
        org.junit.Assert.assertArrayEquals(alleleArray45, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean47 + "' != '" + false + "'", boolean47 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
    }

    @Test
    public void test117() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test117");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder10.loc(".", 0L, (long) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder10.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder16.rmAttribute(".");
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test118() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test118");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        java.lang.String str11 = variantContextBuilder5.getID();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertEquals("'" + str11 + "' != '" + "." + "'", str11, ".");
    }

    @Test
    public void test119() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test119");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.id("");
        java.lang.Class<?> wildcardClass22 = variantContextBuilder19.getClass();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(wildcardClass22);
    }

    @Test
    public void test120() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test120");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection33 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder34.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.start((long) (short) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection43 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder44.log10PError((double) (short) 100);
        java.lang.String[] strArray48 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet49 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder44.filters((java.util.Set<java.lang.String>) strSet49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder44.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap53 = variantContextBuilder44.getAttributes();
        java.lang.String[] strArray57 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder44.filters(strArray57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder58.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext61 = variantContextBuilder60.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder36.genotypesNoValidation(genotypesContext61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypesContext61);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(strMap53);
        org.junit.Assert.assertNotNull(strArray57);
        org.junit.Assert.assertArrayEquals(strArray57, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertNotNull(genotypesContext61);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
    }

    @Test
    public void test121() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test121");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder17.passFilters();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
    }

    @Test
    public void test122() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test122");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.start((long) (short) 10);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext10 = variantContextBuilder7.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(genotypesContext10);
    }

    @Test
    public void test123() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test123");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder27.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder19.putAttributes(strMap36);
        java.util.Map<java.lang.String, java.lang.Object> strMap38 = variantContextBuilder19.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder19.start((long) '#');
        long long41 = variantContextBuilder19.getStart();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(strMap38);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertTrue("'" + long41 + "' != '" + 35L + "'", long41 == 35L);
    }

    @Test
    public void test124() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test124");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder1 = variantContextBuilder0.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder2 = variantContextBuilder0.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection7);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder8.log10PError((double) (short) 100);
        java.lang.String[] strArray12 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet13 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder8.filters((java.util.Set<java.lang.String>) strSet13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder8.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap17 = variantContextBuilder8.getAttributes();
        java.util.Set<java.lang.String> strSet18 = variantContextBuilder8.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder2.filters(strSet18);
        org.junit.Assert.assertNotNull(variantContextBuilder1);
        org.junit.Assert.assertNotNull(variantContextBuilder2);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(strMap17);
        org.junit.Assert.assertNotNull(strSet18);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test125() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test125");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder17.fullyDecoded(false);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection30 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder31.log10PError((double) (short) 100);
        java.lang.String[] strArray35 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder31.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder31.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap40 = variantContextBuilder31.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap41 = variantContextBuilder31.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray46 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList47 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean48 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47, alleleArray46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder31.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder17.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder51.source(".");
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(strMap40);
        org.junit.Assert.assertNotNull(strMap41);
        org.junit.Assert.assertNotNull(alleleArray46);
        org.junit.Assert.assertArrayEquals(alleleArray46, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + false + "'", boolean48 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
    }

    @Test
    public void test126() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test126");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        boolean boolean16 = variantContextBuilder15.isFullyDecoded();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder15.stop(0L);
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test127() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test127");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.chr("");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext18 = variantContextBuilder14.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test128() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test128");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.rmAttribute("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection39 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder40.log10PError((double) (short) 100);
        java.lang.String[] strArray44 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet45 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean46 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet45, strArray44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder40.filters((java.util.Set<java.lang.String>) strSet45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder40.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap49 = variantContextBuilder40.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap50 = variantContextBuilder40.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray55 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList56 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean57 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56, alleleArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder40.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "hi!", (long) ' ', (long) ' ', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder28.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList56, (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strArray44);
        org.junit.Assert.assertArrayEquals(strArray44, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + true + "'", boolean46 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(strMap49);
        org.junit.Assert.assertNotNull(strMap50);
        org.junit.Assert.assertNotNull(alleleArray55);
        org.junit.Assert.assertArrayEquals(alleleArray55, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean57 + "' != '" + false + "'", boolean57 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
    }

    @Test
    public void test129() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test129");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder27.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder19.putAttributes(strMap36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder19.fullyDecoded(false);
        java.lang.String str40 = variantContextBuilder39.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder39.filter("hi!");
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertEquals("'" + str40 + "' != '" + "" + "'", str40, "");
        org.junit.Assert.assertNotNull(variantContextBuilder42);
    }

    @Test
    public void test130() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test130");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder20.chr("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder20.start((long) 1);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
    }

    @Test
    public void test131() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test131");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.lang.String[] strArray12 = new java.lang.String[] { "hi!", "hi!", "." };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder8.rmAttributes((java.util.List<java.lang.String>) strList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder8.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder8.filter("");
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "hi!", "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test132() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test132");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection29 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder30.log10PError((double) (short) 100);
        java.lang.String[] strArray34 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet35 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean36 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet35, strArray34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder30.filters((java.util.Set<java.lang.String>) strSet35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder30.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap39 = variantContextBuilder30.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap40 = variantContextBuilder30.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray45 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList46 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean47 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46, alleleArray45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder30.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "hi!", (long) ' ', (long) ' ', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder17.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList46);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection57 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder58.log10PError((double) (short) 100);
        java.lang.String str61 = variantContextBuilder58.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder17.attribute("", (java.lang.Object) str61);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(strArray34);
        org.junit.Assert.assertArrayEquals(strArray34, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + true + "'", boolean36 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strMap39);
        org.junit.Assert.assertNotNull(strMap40);
        org.junit.Assert.assertNotNull(alleleArray45);
        org.junit.Assert.assertArrayEquals(alleleArray45, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean47 + "' != '" + false + "'", boolean47 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertEquals("'" + str61 + "' != '" + "hi!" + "'", str61, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder62);
    }

    @Test
    public void test133() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test133");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder21.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder21.noGenotypes();
        htsjdk.variant.variantcontext.Allele[] alleleArray32 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList33 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean34 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33, alleleArray32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("hi!", "", 10L, (long) '4', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder21.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "", (long) ' ', (-1L), (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "", (long) ' ', 100L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder5.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList33, (int) 'a', (int) '#');
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(alleleArray32);
        org.junit.Assert.assertArrayEquals(alleleArray32, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
    }

    @Test
    public void test134() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test134");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.stop((long) 100);
        java.util.Set<java.lang.String> strSet9 = variantContextBuilder5.getFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNull(strSet9);
    }

    @Test
    public void test135() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test135");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder5.filter("hi!");
        htsjdk.variant.variantcontext.Allele[] alleleArray30 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList31 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean32 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31, alleleArray30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder35.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder37.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder45.log10PError((double) (short) 100);
        java.lang.String[] strArray49 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet50 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean51 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet50, strArray49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder45.filters((java.util.Set<java.lang.String>) strSet50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder45.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap54 = variantContextBuilder45.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder37.putAttributes(strMap54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder37.fullyDecoded(false);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection62 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder63.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder65.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap68 = variantContextBuilder67.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder57.attributes(strMap68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder5.attribute("", (java.lang.Object) variantContextBuilder57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder70.copy();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(alleleArray30);
        org.junit.Assert.assertArrayEquals(alleleArray30, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(strArray49);
        org.junit.Assert.assertArrayEquals(strArray49, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + true + "'", boolean51 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(strMap54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(strMap68);
        org.junit.Assert.assertNotNull(variantContextBuilder69);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
    }

    @Test
    public void test136() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test136");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.genotypes(genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder7.noID();
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
    }

    @Test
    public void test137() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test137");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder12.loc("", (long) (short) 1, (long) 1);
        java.lang.Object obj20 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder12.attribute("", obj20);
        long long22 = variantContextBuilder12.getStart();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertTrue("'" + long22 + "' != '" + 1L + "'", long22 == 1L);
    }

    @Test
    public void test138() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test138");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder13.unfiltered();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection19 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder20.unfiltered();
        java.lang.String str22 = variantContextBuilder20.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder20.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection28 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder29.log10PError((double) (short) 100);
        java.lang.String[] strArray33 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet34 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder29.filters((java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder29.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap38 = variantContextBuilder29.getAttributes();
        java.lang.String[] strArray42 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder29.filters(strArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder23.filters(strArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder13.filters(strArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder45.id("");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext49 = variantContextBuilder47.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: ID field cannot be the null or the empty string");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertEquals("'" + str22 + "' != '" + "hi!" + "'", str22, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(strMap38);
        org.junit.Assert.assertNotNull(strArray42);
        org.junit.Assert.assertArrayEquals(strArray42, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
    }

    @Test
    public void test139() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test139");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder5.filter("hi!");
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext17 = variantContextBuilder16.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test140() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test140");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder12.noGenotypes();
        java.lang.String str16 = variantContextBuilder15.getContig();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertEquals("'" + str16 + "' != '" + "hi!" + "'", str16, "hi!");
    }

    @Test
    public void test141() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test141");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder21.noGenotypes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
    }

    @Test
    public void test142() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test142");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder9.id(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder9.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder26.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection34 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder35.log10PError((double) (short) 100);
        java.lang.String str38 = variantContextBuilder35.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext39 = variantContextBuilder35.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder26.genotypes(genotypesContext39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder9.genotypes(genotypesContext39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder8.genotypes(genotypesContext39);
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertEquals("'" + str38 + "' != '" + "hi!" + "'", str38, "hi!");
        org.junit.Assert.assertNotNull(genotypesContext39);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
    }

    @Test
    public void test143() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test143");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap15 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray20 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList21 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21, alleleArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder5.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.start((long) (byte) 100);
        java.lang.Class<?> wildcardClass27 = variantContextBuilder26.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strMap15);
        org.junit.Assert.assertNotNull(alleleArray20);
        org.junit.Assert.assertArrayEquals(alleleArray20, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + false + "'", boolean22 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(wildcardClass27);
    }

    @Test
    public void test144() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test144");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.lang.String str7 = variantContextBuilder5.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.source(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder9.stop((long) (byte) -1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder9.passFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "hi!" + "'", str7, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
    }

    @Test
    public void test145() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test145");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder13.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        java.lang.String str25 = variantContextBuilder22.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext26 = variantContextBuilder22.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder13.genotypes(genotypesContext26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.stop((long) (short) 100);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertEquals("'" + str25 + "' != '" + "hi!" + "'", str25, "hi!");
        org.junit.Assert.assertNotNull(genotypesContext26);
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
    }

    @Test
    public void test146() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test146");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder2 = variantContextBuilder0.id(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder4 = variantContextBuilder2.start((long) ' ');
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder2);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        org.junit.Assert.assertNotNull(variantContextBuilder2);
        org.junit.Assert.assertNotNull(variantContextBuilder4);
        org.junit.Assert.assertNotNull(variantContextBuilder6);
    }

    @Test
    public void test147() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test147");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext13 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder5.genotypes(genotypesContext13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder5.log10PError((double) 1.0f);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test148() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test148");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder2 = variantContextBuilder0.id(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder3 = variantContextBuilder0.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection8 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder9.log10PError((double) (short) 100);
        java.lang.String[] strArray13 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet14 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean15 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet14, strArray13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder9.filters((java.util.Set<java.lang.String>) strSet14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder9.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.log10PError((double) (short) 100);
        java.lang.String str29 = variantContextBuilder26.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext30 = variantContextBuilder26.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder17.genotypes(genotypesContext30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder0.genotypes(genotypesContext30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder32.noGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder2);
        org.junit.Assert.assertNotNull(variantContextBuilder3);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strArray13);
        org.junit.Assert.assertArrayEquals(strArray13, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertEquals("'" + str29 + "' != '" + "hi!" + "'", str29, "hi!");
        org.junit.Assert.assertNotNull(genotypesContext30);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
    }

    @Test
    public void test149() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test149");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet19 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet19, strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.filters((java.util.Set<java.lang.String>) strSet19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder8.attribute(".", (java.lang.Object) variantContextBuilder15);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection27 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.log10PError((double) (short) 100);
        java.lang.String str31 = variantContextBuilder28.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext32 = variantContextBuilder28.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder22.genotypes(genotypesContext32);
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertEquals("'" + str31 + "' != '" + "hi!" + "'", str31, "hi!");
        org.junit.Assert.assertNotNull(genotypesContext32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
    }

    @Test
    public void test150() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test150");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder7.putAttributes(strMap22);
        htsjdk.variant.variantcontext.Allele[] alleleArray32 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList33 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean34 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33, alleleArray32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder38.start((long) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection45 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder46.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray49 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList50 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean51 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList50, genotypeArray49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder46.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList50);
        java.util.Map<java.lang.String, java.lang.Object> strMap53 = variantContextBuilder46.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder38.attributes(strMap53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder23.putAttributes(strMap53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder23.chr("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder57.noGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(alleleArray32);
        org.junit.Assert.assertArrayEquals(alleleArray32, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(genotypeArray49);
        org.junit.Assert.assertArrayEquals(genotypeArray49, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + false + "'", boolean51 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(strMap53);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
    }

    @Test
    public void test151() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test151");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder13.log10PError((double) (byte) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder16.rmAttribute("");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test152() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test152");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        java.lang.String str15 = variantContextBuilder12.getContig();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "hi!" + "'", str15, "hi!");
    }

    @Test
    public void test153() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test153");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap36 = variantContextBuilder27.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder19.putAttributes(strMap36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder19.fullyDecoded(false);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder45.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap50 = variantContextBuilder49.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder39.attributes(strMap50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder39.noGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder39.copy();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strMap36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strMap50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
    }

    @Test
    public void test154() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test154");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.stop((long) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.source("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection15 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection15);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder16.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray29 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList30 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean31 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList30, genotypeArray29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder26.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder20.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList30);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection39 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder40.log10PError((double) (short) 100);
        java.lang.String[] strArray44 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet45 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean46 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet45, strArray44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder40.filters((java.util.Set<java.lang.String>) strSet45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder40.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection53 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection53);
        java.lang.String[] strArray57 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet58 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean59 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet58, strArray57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder54.filters((java.util.Set<java.lang.String>) strSet58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder40.filters((java.util.Set<java.lang.String>) strSet58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder40.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection68 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder69.log10PError((double) (short) 100);
        java.lang.String[] strArray73 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet74 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean75 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet74, strArray73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder69.filters((java.util.Set<java.lang.String>) strSet74);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder77 = variantContextBuilder69.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap78 = variantContextBuilder69.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap79 = variantContextBuilder69.getAttributes();
        java.lang.String[] strArray83 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList84 = new java.util.ArrayList<java.lang.String>();
        boolean boolean85 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList84, strArray83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = variantContextBuilder69.rmAttributes((java.util.List<java.lang.String>) strList84);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder87 = variantContextBuilder63.rmAttributes((java.util.List<java.lang.String>) strList84);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = variantContextBuilder34.alleles((java.util.List<java.lang.String>) strList84);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(genotypeArray29);
        org.junit.Assert.assertArrayEquals(genotypeArray29, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + false + "'", boolean31 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strArray44);
        org.junit.Assert.assertArrayEquals(strArray44, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + true + "'", boolean46 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(strArray57);
        org.junit.Assert.assertArrayEquals(strArray57, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean59 + "' != '" + true + "'", boolean59 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
        org.junit.Assert.assertNotNull(strArray73);
        org.junit.Assert.assertArrayEquals(strArray73, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean75 + "' != '" + true + "'", boolean75 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder76);
        org.junit.Assert.assertNotNull(variantContextBuilder77);
        org.junit.Assert.assertNotNull(strMap78);
        org.junit.Assert.assertNotNull(strMap79);
        org.junit.Assert.assertNotNull(strArray83);
        org.junit.Assert.assertArrayEquals(strArray83, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean85 + "' != '" + true + "'", boolean85 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder86);
        org.junit.Assert.assertNotNull(variantContextBuilder87);
    }

    @Test
    public void test155() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test155");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        long long21 = variantContextBuilder17.getStart();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder26.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.noGenotypes();
        htsjdk.variant.variantcontext.Allele[] alleleArray37 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList38 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean39 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38, alleleArray37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("hi!", "", 10L, (long) '4', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder26.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "", (long) ' ', (-1L), (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList38);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder17.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList38, 10, (int) (byte) -1);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertTrue("'" + long21 + "' != '" + 10L + "'", long21 == 10L);
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(alleleArray37);
        org.junit.Assert.assertArrayEquals(alleleArray37, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean39 + "' != '" + false + "'", boolean39 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
    }

    @Test
    public void test156() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test156");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.lang.String[] strArray12 = new java.lang.String[] { "hi!", "hi!", "." };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder8.rmAttributes((java.util.List<java.lang.String>) strList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder8.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder17.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.id("");
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "hi!", "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
    }

    @Test
    public void test157() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test157");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder7.putAttributes(strMap22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder7.id("hi!");
        long long26 = variantContextBuilder25.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertTrue("'" + long26 + "' != '" + 0L + "'", long26 == 0L);
    }

    @Test
    public void test158() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test158");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder13.log10PError((double) (byte) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder16.source("");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test159() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test159");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder13.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.start((-1L));
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test160() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test160");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("hi!", "", 10L, (long) '4', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.stop((long) '#');
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder14.unfiltered();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test161() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test161");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.rmAttribute("");
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
    }

    @Test
    public void test162() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test162");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", 10L, (long) (byte) 1, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test163() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test163");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        long long14 = variantContextBuilder13.getStop();
        htsjdk.variant.variantcontext.Allele[] alleleArray23 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList24 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24, alleleArray23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.chr("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection36 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder37.log10PError((double) (short) 100);
        java.lang.String[] strArray41 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet42 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder37.filters((java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder37.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap46 = variantContextBuilder37.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap47 = variantContextBuilder37.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray52 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList53 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean54 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53, alleleArray52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder37.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder28.attribute("hi!", (java.lang.Object) variantContextBuilder56);
        java.lang.String str58 = variantContextBuilder57.getContig();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
        org.junit.Assert.assertNotNull(alleleArray23);
        org.junit.Assert.assertArrayEquals(alleleArray23, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(strMap46);
        org.junit.Assert.assertNotNull(strMap47);
        org.junit.Assert.assertNotNull(alleleArray52);
        org.junit.Assert.assertArrayEquals(alleleArray52, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean54 + "' != '" + false + "'", boolean54 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertEquals("'" + str58 + "' != '" + "" + "'", str58, "");
    }

    @Test
    public void test164() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test164");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        htsjdk.variant.variantcontext.Allele[] alleleArray21 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList22 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean23 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22, alleleArray21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22);
        java.lang.String[] strArray29 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList30 = new java.util.ArrayList<java.lang.String>();
        boolean boolean31 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList30, strArray29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder26.rmAttributes((java.util.List<java.lang.String>) strList30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder26.fullyDecoded(false);
        java.util.Map<java.lang.String, java.lang.Object> strMap35 = variantContextBuilder34.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder5.putAttributes(strMap35);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext37 = variantContextBuilder5.getGenotypes();
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(alleleArray21);
        org.junit.Assert.assertArrayEquals(alleleArray21, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean23 + "' != '" + false + "'", boolean23 == false);
        org.junit.Assert.assertNotNull(strArray29);
        org.junit.Assert.assertArrayEquals(strArray29, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + true + "'", boolean31 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(strMap35);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNull(genotypesContext37);
    }

    @Test
    public void test165() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test165");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection34 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection34);
        long long36 = variantContextBuilder35.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext37 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder35.genotypes(genotypesContext37);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        java.lang.String[] strArray48 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet49 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder45.filters((java.util.Set<java.lang.String>) strSet49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder38.attribute(".", (java.lang.Object) variantContextBuilder45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder28.attribute("", (java.lang.Object) variantContextBuilder38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder53.source(".");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertTrue("'" + long36 + "' != '" + 52L + "'", long36 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
    }

    @Test
    public void test166() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test166");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.lang.String str7 = variantContextBuilder5.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection13 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder14.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection23 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray27 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList28 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean29 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList28, genotypeArray27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder24.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder18.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder8.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder8.log10PError((double) (-1.0f));
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "hi!" + "'", str7, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(genotypeArray27);
        org.junit.Assert.assertArrayEquals(genotypeArray27, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + false + "'", boolean29 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
    }

    @Test
    public void test167() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test167");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.chr("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder16.noGenotypes();
        htsjdk.variant.variantcontext.Genotype[] genotypeArray18 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.genotypes(genotypeArray18);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(genotypeArray18);
        org.junit.Assert.assertArrayEquals(genotypeArray18, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test168() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test168");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        boolean boolean16 = variantContextBuilder15.isFullyDecoded();
        java.util.Map<java.lang.String, java.lang.Object> strMap17 = variantContextBuilder15.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection22 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder23.log10PError((double) (short) 100);
        java.lang.String[] strArray27 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet28 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean29 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet28, strArray27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder23.filters((java.util.Set<java.lang.String>) strSet28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder23.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection36 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection36);
        java.lang.String[] strArray40 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet41 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean42 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet41, strArray40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder37.filters((java.util.Set<java.lang.String>) strSet41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder23.filters((java.util.Set<java.lang.String>) strSet41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder23.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection51 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder52.log10PError((double) (short) 100);
        java.lang.String[] strArray56 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet57 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean58 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet57, strArray56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder52.filters((java.util.Set<java.lang.String>) strSet57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder52.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap61 = variantContextBuilder52.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap62 = variantContextBuilder52.getAttributes();
        java.lang.String[] strArray66 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList67 = new java.util.ArrayList<java.lang.String>();
        boolean boolean68 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList67, strArray66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder52.rmAttributes((java.util.List<java.lang.String>) strList67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder46.rmAttributes((java.util.List<java.lang.String>) strList67);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder15.alleles((java.util.List<java.lang.String>) strList67);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(strMap17);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(strArray27);
        org.junit.Assert.assertArrayEquals(strArray27, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean29 + "' != '" + true + "'", boolean29 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(strArray40);
        org.junit.Assert.assertArrayEquals(strArray40, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean42 + "' != '" + true + "'", boolean42 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(strArray56);
        org.junit.Assert.assertArrayEquals(strArray56, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean58 + "' != '" + true + "'", boolean58 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertNotNull(strMap61);
        org.junit.Assert.assertNotNull(strMap62);
        org.junit.Assert.assertNotNull(strArray66);
        org.junit.Assert.assertArrayEquals(strArray66, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean68 + "' != '" + true + "'", boolean68 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder69);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
    }

    @Test
    public void test169() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test169");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder15.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder19.passFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder19);
        htsjdk.variant.variantcontext.Allele[] alleleArray30 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList31 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean32 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31, alleleArray30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder19.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList31);
        java.lang.String str36 = variantContextBuilder35.getContig();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(alleleArray30);
        org.junit.Assert.assertArrayEquals(alleleArray30, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + false + "'", boolean32 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertEquals("'" + str36 + "' != '" + "hi!" + "'", str36, "hi!");
    }

    @Test
    public void test170() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test170");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder12.loc("", (long) (short) 1, (long) 1);
        java.lang.Object obj20 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder12.attribute("", obj20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder12.start((long) (byte) 10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder23.stop((long) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection30 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder31.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection40 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder41.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray44 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList45 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean46 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList45, genotypeArray44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder41.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder35.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder48.chr("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection55 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection55);
        java.lang.String[] strArray59 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet60 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean61 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet60, strArray59);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder56.filters((java.util.Set<java.lang.String>) strSet60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder62.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection65 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder64.genotypes(genotypeCollection65);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection71 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection71);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray73 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder72.genotypes(genotypeArray73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder75 = variantContextBuilder64.genotypes(genotypeArray73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder48.genotypes(genotypeArray73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder77 = variantContextBuilder23.genotypes(genotypeArray73);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(genotypeArray44);
        org.junit.Assert.assertArrayEquals(genotypeArray44, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + false + "'", boolean46 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(strArray59);
        org.junit.Assert.assertArrayEquals(strArray59, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean61 + "' != '" + true + "'", boolean61 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(genotypeArray73);
        org.junit.Assert.assertArrayEquals(genotypeArray73, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder74);
        org.junit.Assert.assertNotNull(variantContextBuilder75);
        org.junit.Assert.assertNotNull(variantContextBuilder76);
        org.junit.Assert.assertNotNull(variantContextBuilder77);
    }

    @Test
    public void test171() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test171");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder5.filters(strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext22 = variantContextBuilder21.getGenotypes();
        // The following exception was thrown during execution in test generation
        try {
            java.util.List<htsjdk.variant.variantcontext.Allele> alleleList23 = variantContextBuilder21.getAlleles();
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.Collection.toArray()\" because \"c\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(genotypesContext22);
    }

    @Test
    public void test172() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test172");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder15.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        java.lang.String[] strArray26 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet27 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean28 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet27, strArray26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder22.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection35 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection35);
        java.lang.String[] strArray39 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet40 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.filters((java.util.Set<java.lang.String>) strSet40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet40);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection48 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder49.log10PError((double) (short) 100);
        java.lang.String[] strArray53 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet54 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean55 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet54, strArray53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder49.filters((java.util.Set<java.lang.String>) strSet54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder49.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder57.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray60 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList61 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean62 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList61, alleleArray60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder59.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder59.source("hi!");
        java.util.Set<java.lang.String> strSet66 = variantContextBuilder65.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder43.filters(strSet66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder15.filters(strSet66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder15.chr("");
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(strArray26);
        org.junit.Assert.assertArrayEquals(strArray26, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder43);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(strArray53);
        org.junit.Assert.assertArrayEquals(strArray53, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean55 + "' != '" + true + "'", boolean55 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(alleleArray60);
        org.junit.Assert.assertArrayEquals(alleleArray60, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean62 + "' != '" + false + "'", boolean62 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(strSet66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
    }

    @Test
    public void test173() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test173");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder5.filter("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder5.log10PError((double) 0);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test174() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test174");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder10.loc(".", 0L, (long) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.id(".");
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test175() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test175");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        long long11 = variantContextBuilder10.getStart();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder10.start((long) (byte) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder13.noGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder14.loc("hi!", (long) (short) 10, (long) (short) 1);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray19 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder14.genotypes(genotypeArray19);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertTrue("'" + long11 + "' != '" + 10L + "'", long11 == 10L);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test176() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test176");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder17.fullyDecoded(false);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection30 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder31.log10PError((double) (short) 100);
        java.lang.String[] strArray35 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder31.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder31.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap40 = variantContextBuilder31.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap41 = variantContextBuilder31.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray46 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList47 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean48 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47, alleleArray46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder31.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder17.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList47);
        long long52 = variantContextBuilder17.getStart();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(strMap40);
        org.junit.Assert.assertNotNull(strMap41);
        org.junit.Assert.assertNotNull(alleleArray46);
        org.junit.Assert.assertArrayEquals(alleleArray46, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean48 + "' != '" + false + "'", boolean48 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertTrue("'" + long52 + "' != '" + 10L + "'", long52 == 10L);
    }

    @Test
    public void test177() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test177");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        long long12 = variantContextBuilder11.getStart();
        htsjdk.variant.variantcontext.Allele[] alleleArray25 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList26 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26, alleleArray25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26);
        java.lang.String[] strArray33 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList34 = new java.util.ArrayList<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder30.rmAttributes((java.util.List<java.lang.String>) strList34);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder11.alleles((java.util.List<java.lang.String>) strList34);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertTrue("'" + long12 + "' != '" + 0L + "'", long12 == 0L);
        org.junit.Assert.assertNotNull(alleleArray25);
        org.junit.Assert.assertArrayEquals(alleleArray25, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
    }

    @Test
    public void test178() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test178");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder15.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder19.passFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder20.id("");
        java.lang.String str23 = variantContextBuilder20.getContig();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertEquals("'" + str23 + "' != '" + "hi!" + "'", str23, "hi!");
    }

    @Test
    public void test179() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test179");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder46.noID();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
    }

    @Test
    public void test180() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test180");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder18.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection46 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.log10PError((double) (short) 100);
        java.lang.String[] strArray51 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet52 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean53 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet52, strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder47.filters((java.util.Set<java.lang.String>) strSet52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder47.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap56 = variantContextBuilder47.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap57 = variantContextBuilder47.getAttributes();
        java.lang.String[] strArray61 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList62 = new java.util.ArrayList<java.lang.String>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList62, strArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder47.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder66.noGenotypes();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext68 = variantContextBuilder67.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strArray51);
        org.junit.Assert.assertArrayEquals(strArray51, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean53 + "' != '" + true + "'", boolean53 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strMap56);
        org.junit.Assert.assertNotNull(strMap57);
        org.junit.Assert.assertNotNull(strArray61);
        org.junit.Assert.assertArrayEquals(strArray61, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + true + "'", boolean63 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNull(genotypesContext68);
    }

    @Test
    public void test181() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test181");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext18 = variantContextBuilder17.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test182() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test182");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        long long14 = variantContextBuilder13.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext15 = variantContextBuilder13.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
        org.junit.Assert.assertNull(genotypesContext15);
    }

    @Test
    public void test183() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test183");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        long long22 = variantContextBuilder19.getStart();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder19);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertTrue("'" + long22 + "' != '" + 10L + "'", long22 == 10L);
    }

    @Test
    public void test184() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test184");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.lang.String[] strArray12 = new java.lang.String[] { "hi!", "hi!", "." };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder8.rmAttributes((java.util.List<java.lang.String>) strList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder8.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder17.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.rmAttribute("hi!");
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "hi!", "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
    }

    @Test
    public void test185() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test185");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        long long14 = variantContextBuilder13.getStop();
        htsjdk.variant.variantcontext.Allele[] alleleArray23 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList24 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24, alleleArray23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.chr("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection36 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder37.log10PError((double) (short) 100);
        java.lang.String[] strArray41 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet42 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder37.filters((java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder37.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap46 = variantContextBuilder37.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap47 = variantContextBuilder37.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray52 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList53 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean54 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53, alleleArray52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder37.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder28.attribute("hi!", (java.lang.Object) variantContextBuilder56);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection62 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder63.log10PError((double) (short) 100);
        java.lang.String[] strArray67 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet68 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean69 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet68, strArray67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder63.filters((java.util.Set<java.lang.String>) strSet68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder63.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap72 = variantContextBuilder63.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap73 = variantContextBuilder63.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder57.attributes(strMap73);
        long long75 = variantContextBuilder57.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
        org.junit.Assert.assertNotNull(alleleArray23);
        org.junit.Assert.assertArrayEquals(alleleArray23, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(strMap46);
        org.junit.Assert.assertNotNull(strMap47);
        org.junit.Assert.assertNotNull(alleleArray52);
        org.junit.Assert.assertArrayEquals(alleleArray52, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean54 + "' != '" + false + "'", boolean54 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(strArray67);
        org.junit.Assert.assertArrayEquals(strArray67, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean69 + "' != '" + true + "'", boolean69 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
        org.junit.Assert.assertNotNull(strMap72);
        org.junit.Assert.assertNotNull(strMap73);
        org.junit.Assert.assertNotNull(variantContextBuilder74);
        org.junit.Assert.assertTrue("'" + long75 + "' != '" + 0L + "'", long75 == 0L);
    }

    @Test
    public void test186() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test186");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.start((long) (short) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        boolean boolean16 = variantContextBuilder15.isFullyDecoded();
        java.util.Map<java.lang.String, java.lang.Object> strMap17 = variantContextBuilder15.getAttributes();
        java.lang.String str18 = variantContextBuilder15.getID();
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertNotNull(strMap17);
        org.junit.Assert.assertEquals("'" + str18 + "' != '" + "." + "'", str18, ".");
    }

    @Test
    public void test187() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test187");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        long long14 = variantContextBuilder13.getStop();
        htsjdk.variant.variantcontext.Allele[] alleleArray23 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList24 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24, alleleArray23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList24);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext30 = variantContextBuilder13.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + long14 + "' != '" + 52L + "'", long14 == 52L);
        org.junit.Assert.assertNotNull(alleleArray23);
        org.junit.Assert.assertArrayEquals(alleleArray23, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + false + "'", boolean25 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
    }

    @Test
    public void test188() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test188");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        long long13 = variantContextBuilder12.getStart();
        boolean boolean14 = variantContextBuilder12.isFullyDecoded();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder12.fullyDecoded(true);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertTrue("'" + long13 + "' != '" + 100L + "'", long13 == 100L);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test189() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test189");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.noGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder13.noID();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
    }

    @Test
    public void test190() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test190");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder10.loc(".", 0L, (long) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder14.loc(".", (-1L), 100L);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection23 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder24.unfiltered();
        java.lang.String str26 = variantContextBuilder24.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder24.noGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.stop(52L);
        htsjdk.variant.variantcontext.Allele[] alleleArray42 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList43 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean44 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43, alleleArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.id("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection54 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection54);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray56 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder55.genotypes(genotypeArray56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder47.genotypes(genotypeArray56);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection63 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder64.log10PError((double) (short) 100);
        java.lang.String[] strArray68 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet69 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean70 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet69, strArray68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder64.filters((java.util.Set<java.lang.String>) strSet69);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder64.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap73 = variantContextBuilder64.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap74 = variantContextBuilder64.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder75 = variantContextBuilder58.putAttributes(strMap74);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder29.putAttributes(strMap74);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder77 = variantContextBuilder14.attributes(strMap74);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertEquals("'" + str26 + "' != '" + "hi!" + "'", str26, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(alleleArray42);
        org.junit.Assert.assertArrayEquals(alleleArray42, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean44 + "' != '" + false + "'", boolean44 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(genotypeArray56);
        org.junit.Assert.assertArrayEquals(genotypeArray56, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(strArray68);
        org.junit.Assert.assertArrayEquals(strArray68, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean70 + "' != '" + true + "'", boolean70 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
        org.junit.Assert.assertNotNull(variantContextBuilder72);
        org.junit.Assert.assertNotNull(strMap73);
        org.junit.Assert.assertNotNull(strMap74);
        org.junit.Assert.assertNotNull(variantContextBuilder75);
        org.junit.Assert.assertNotNull(variantContextBuilder76);
        org.junit.Assert.assertNotNull(variantContextBuilder77);
    }

    @Test
    public void test191() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test191");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder21.start((long) (-1));
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder21.source("hi!");
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
    }

    @Test
    public void test192() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test192");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder7.putAttributes(strMap22);
        htsjdk.variant.variantcontext.Allele[] alleleArray32 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList33 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean34 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33, alleleArray32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder38.start((long) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection45 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder46.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray49 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList50 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean51 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList50, genotypeArray49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder46.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList50);
        java.util.Map<java.lang.String, java.lang.Object> strMap53 = variantContextBuilder46.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder38.attributes(strMap53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder23.putAttributes(strMap53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder23.chr("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder57.passFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(alleleArray32);
        org.junit.Assert.assertArrayEquals(alleleArray32, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean34 + "' != '" + false + "'", boolean34 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(genotypeArray49);
        org.junit.Assert.assertArrayEquals(genotypeArray49, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean51 + "' != '" + false + "'", boolean51 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(strMap53);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
    }

    @Test
    public void test193() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test193");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext11 = variantContextBuilder10.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(genotypesContext11);
    }

    @Test
    public void test194() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test194");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder17.unfiltered();
        htsjdk.variant.variantcontext.Allele[] alleleArray33 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList34 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34, alleleArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder17.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList34, 1, 100);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(alleleArray33);
        org.junit.Assert.assertArrayEquals(alleleArray33, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + false + "'", boolean35 == false);
    }

    @Test
    public void test195() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test195");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap14 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder5.chr("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        java.lang.String[] strArray26 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet27 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean28 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet27, strArray26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder22.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder30.genotypes(genotypeCollection31);
        java.util.Map<java.lang.String, java.lang.Object> strMap33 = variantContextBuilder32.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection38 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder39.log10PError((double) (short) 100);
        java.lang.String[] strArray43 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet44 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet44, strArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder39.filters((java.util.Set<java.lang.String>) strSet44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder39.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection52 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection52);
        java.lang.String[] strArray56 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet57 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean58 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet57, strArray56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder53.filters((java.util.Set<java.lang.String>) strSet57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder39.filters((java.util.Set<java.lang.String>) strSet57);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection65 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection65);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder66.log10PError((double) (short) 100);
        java.lang.String[] strArray70 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet71 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean72 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet71, strArray70);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder73 = variantContextBuilder66.filters((java.util.Set<java.lang.String>) strSet71);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder66.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder74.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray77 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList78 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean79 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList78, alleleArray77);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder80 = variantContextBuilder76.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList78);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder82 = variantContextBuilder76.source("hi!");
        java.util.Set<java.lang.String> strSet83 = variantContextBuilder82.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder84 = variantContextBuilder60.filters(strSet83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder85 = variantContextBuilder32.filters(strSet83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = variantContextBuilder16.filters(strSet83);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strMap14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(strArray26);
        org.junit.Assert.assertArrayEquals(strArray26, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean28 + "' != '" + true + "'", boolean28 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(strMap33);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(strArray43);
        org.junit.Assert.assertArrayEquals(strArray43, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + true + "'", boolean45 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(strArray56);
        org.junit.Assert.assertArrayEquals(strArray56, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean58 + "' != '" + true + "'", boolean58 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
        org.junit.Assert.assertNotNull(strArray70);
        org.junit.Assert.assertArrayEquals(strArray70, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean72 + "' != '" + true + "'", boolean72 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder73);
        org.junit.Assert.assertNotNull(variantContextBuilder74);
        org.junit.Assert.assertNotNull(variantContextBuilder76);
        org.junit.Assert.assertNotNull(alleleArray77);
        org.junit.Assert.assertArrayEquals(alleleArray77, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean79 + "' != '" + false + "'", boolean79 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder80);
        org.junit.Assert.assertNotNull(variantContextBuilder82);
        org.junit.Assert.assertNotNull(strSet83);
        org.junit.Assert.assertNotNull(variantContextBuilder84);
        org.junit.Assert.assertNotNull(variantContextBuilder85);
        org.junit.Assert.assertNotNull(variantContextBuilder86);
    }

    @Test
    public void test196() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test196");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        java.util.Map<java.lang.String, java.lang.Object> strMap24 = variantContextBuilder23.getAttributes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(strMap24);
    }

    @Test
    public void test197() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test197");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        long long16 = variantContextBuilder15.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertTrue("'" + long16 + "' != '" + 0L + "'", long16 == 0L);
    }

    @Test
    public void test198() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test198");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.chr("");
        java.lang.String str17 = variantContextBuilder16.getContig();
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertEquals("'" + str17 + "' != '" + "" + "'", str17, "");
    }

    @Test
    public void test199() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test199");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        java.util.Set<java.lang.String> strSet8 = variantContextBuilder7.getFilters();
        long long9 = variantContextBuilder7.getStop();
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNull(strSet8);
        org.junit.Assert.assertTrue("'" + long9 + "' != '" + 35L + "'", long9 == 35L);
    }

    @Test
    public void test200() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test200");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        java.util.Set<java.lang.String> strSet8 = variantContextBuilder7.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder7.source("hi!");
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNull(strSet8);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
    }

    @Test
    public void test201() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test201");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder13.copy();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
    }

    @Test
    public void test202() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test202");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.genotypes(genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder7.log10PError((double) (-1));
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
    }

    @Test
    public void test203() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test203");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder2 = variantContextBuilder0.id(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder3 = variantContextBuilder0.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection8 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder9.log10PError((double) (short) 100);
        java.lang.String[] strArray13 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet14 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean15 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet14, strArray13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder9.filters((java.util.Set<java.lang.String>) strSet14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder9.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.log10PError((double) (short) 100);
        java.lang.String str29 = variantContextBuilder26.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext30 = variantContextBuilder26.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder17.genotypes(genotypesContext30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder0.genotypes(genotypesContext30);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext34 = variantContextBuilder0.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Contig cannot be null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder2);
        org.junit.Assert.assertNotNull(variantContextBuilder3);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strArray13);
        org.junit.Assert.assertArrayEquals(strArray13, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertEquals("'" + str29 + "' != '" + "hi!" + "'", str29, "hi!");
        org.junit.Assert.assertNotNull(genotypesContext30);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
    }

    @Test
    public void test204() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test204");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder13.start(10L);
        java.util.List<htsjdk.variant.variantcontext.Allele> alleleList19 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder18.computeEndFromAlleles(alleleList19, (int) (byte) 0);
            org.junit.Assert.fail("Expected exception of type java.lang.NullPointerException; message: Cannot invoke \"java.util.List.get(int)\" because \"alleles\" is null");
        } catch (java.lang.NullPointerException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test205() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test205");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder13.log10PError((double) (byte) 1);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext18 = variantContextBuilder13.make(false);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Alleles cannot be null");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
    }

    @Test
    public void test206() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test206");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet19 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet19, strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.filters((java.util.Set<java.lang.String>) strSet19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder8.attribute(".", (java.lang.Object) variantContextBuilder15);
        java.lang.String str23 = variantContextBuilder15.getContig();
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertEquals("'" + str23 + "' != '" + "hi!" + "'", str23, "hi!");
    }

    @Test
    public void test207() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test207");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet19 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet19, strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.filters((java.util.Set<java.lang.String>) strSet19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder8.attribute(".", (java.lang.Object) variantContextBuilder15);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder31.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder31.noGenotypes();
        htsjdk.variant.variantcontext.Allele[] alleleArray42 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList43 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean44 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43, alleleArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("hi!", "", 10L, (long) '4', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder31.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "", (long) ' ', (-1L), (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "", (long) ' ', 100L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList43);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder15.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList43, 10, (int) (short) 100);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(alleleArray42);
        org.junit.Assert.assertArrayEquals(alleleArray42, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean44 + "' != '" + false + "'", boolean44 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
    }

    @Test
    public void test208() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test208");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Map<java.lang.String, java.lang.Object> strMap29 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder13.stop((-1L));
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder13.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder32.unfiltered();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(strMap29);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
    }

    @Test
    public void test209() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test209");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.lang.String str7 = variantContextBuilder5.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection13 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray17 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList18 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList18, genotypeArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder14.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList18);
        java.util.Map<java.lang.String, java.lang.Object> strMap21 = variantContextBuilder14.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection40 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection40);
        java.lang.String[] strArray44 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet45 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean46 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet45, strArray44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder41.filters((java.util.Set<java.lang.String>) strSet45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder27.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection55 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder56.log10PError((double) (short) 100);
        java.lang.String[] strArray60 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet61 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean62 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet61, strArray60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder56.filters((java.util.Set<java.lang.String>) strSet61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder56.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap65 = variantContextBuilder56.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap66 = variantContextBuilder56.getAttributes();
        java.lang.String[] strArray70 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList71 = new java.util.ArrayList<java.lang.String>();
        boolean boolean72 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList71, strArray70);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder73 = variantContextBuilder56.rmAttributes((java.util.List<java.lang.String>) strList71);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder50.rmAttributes((java.util.List<java.lang.String>) strList71);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder75 = variantContextBuilder14.rmAttributes((java.util.List<java.lang.String>) strList71);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder5.alleles((java.util.List<java.lang.String>) strList71);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "hi!" + "'", str7, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(genotypeArray17);
        org.junit.Assert.assertArrayEquals(genotypeArray17, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strMap21);
        org.junit.Assert.assertNotNull(variantContextBuilder29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(strArray44);
        org.junit.Assert.assertArrayEquals(strArray44, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + true + "'", boolean46 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(strArray60);
        org.junit.Assert.assertArrayEquals(strArray60, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean62 + "' != '" + true + "'", boolean62 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(strMap65);
        org.junit.Assert.assertNotNull(strMap66);
        org.junit.Assert.assertNotNull(strArray70);
        org.junit.Assert.assertArrayEquals(strArray70, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean72 + "' != '" + true + "'", boolean72 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder73);
        org.junit.Assert.assertNotNull(variantContextBuilder74);
        org.junit.Assert.assertNotNull(variantContextBuilder75);
    }

    @Test
    public void test210() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test210");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Genotype> genotypeCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.genotypes(genotypeCollection14);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder15.getAttributes();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext17 = variantContextBuilder15.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(genotypesContext17);
    }

    @Test
    public void test211() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test211");
        htsjdk.variant.variantcontext.Allele[] alleleArray4 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList5 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean6 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5, alleleArray4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList5);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.genotypes(genotypeArray8);
        java.util.Map<java.lang.String, java.lang.Object> strMap10 = variantContextBuilder9.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection15 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection15);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder16.log10PError((double) (short) 100);
        java.lang.String[] strArray20 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet21 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder16.filters((java.util.Set<java.lang.String>) strSet21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder16.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder24.unfiltered();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection30 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder31.unfiltered();
        java.lang.String str33 = variantContextBuilder31.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder31.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection39 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder40.log10PError((double) (short) 100);
        java.lang.String[] strArray44 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet45 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean46 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet45, strArray44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder40.filters((java.util.Set<java.lang.String>) strSet45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder40.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap49 = variantContextBuilder40.getAttributes();
        java.lang.String[] strArray53 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder40.filters(strArray53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder34.filters(strArray53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder24.filters(strArray53);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder9.filters(strArray53);
        boolean boolean58 = variantContextBuilder9.isFullyDecoded();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection63 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder64.log10PError((double) (short) 100);
        java.lang.String[] strArray68 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet69 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean70 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet69, strArray68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder64.filters((java.util.Set<java.lang.String>) strSet69);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder64.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap73 = variantContextBuilder64.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap74 = variantContextBuilder64.getAttributes();
        java.lang.String[] strArray78 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList79 = new java.util.ArrayList<java.lang.String>();
        boolean boolean80 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList79, strArray78);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder81 = variantContextBuilder64.rmAttributes((java.util.List<java.lang.String>) strList79);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder82 = variantContextBuilder9.rmAttributes((java.util.List<java.lang.String>) strList79);
        org.junit.Assert.assertNotNull(alleleArray4);
        org.junit.Assert.assertArrayEquals(alleleArray4, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(strMap10);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertEquals("'" + str33 + "' != '" + "hi!" + "'", str33, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(strArray44);
        org.junit.Assert.assertArrayEquals(strArray44, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean46 + "' != '" + true + "'", boolean46 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(strMap49);
        org.junit.Assert.assertNotNull(strArray53);
        org.junit.Assert.assertArrayEquals(strArray53, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertTrue("'" + boolean58 + "' != '" + false + "'", boolean58 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(strArray68);
        org.junit.Assert.assertArrayEquals(strArray68, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean70 + "' != '" + true + "'", boolean70 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
        org.junit.Assert.assertNotNull(variantContextBuilder72);
        org.junit.Assert.assertNotNull(strMap73);
        org.junit.Assert.assertNotNull(strMap74);
        org.junit.Assert.assertNotNull(strArray78);
        org.junit.Assert.assertArrayEquals(strArray78, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean80 + "' != '" + true + "'", boolean80 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder81);
        org.junit.Assert.assertNotNull(variantContextBuilder82);
    }

    @Test
    public void test212() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test212");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder10.log10PError((double) 0L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder10.log10PError((double) (-1.0f));
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
    }

    @Test
    public void test213() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test213");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder19.log10PError((double) (short) 100);
        java.lang.String[] strArray23 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet24 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean25 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet24, strArray23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = variantContextBuilder19.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap28 = variantContextBuilder19.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap29 = variantContextBuilder19.getAttributes();
        java.lang.String[] strArray31 = new java.lang.String[] { "hi!" };
        java.util.ArrayList<java.lang.String> strList32 = new java.util.ArrayList<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder19.rmAttributes((java.util.List<java.lang.String>) strList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder35.rmAttribute("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection42 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder43.log10PError((double) (short) 100);
        java.lang.String[] strArray47 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet48 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean49 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet48, strArray47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder43.filters((java.util.Set<java.lang.String>) strSet48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder43.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection56 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection56);
        java.lang.String[] strArray60 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet61 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean62 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet61, strArray60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder57.filters((java.util.Set<java.lang.String>) strSet61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder43.filters((java.util.Set<java.lang.String>) strSet61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder64.loc("", (long) '4', (long) (short) 100);
        htsjdk.variant.variantcontext.Allele[] alleleArray81 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList82 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean83 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList82, alleleArray81);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder84 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList82);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder85 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList82);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList82);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = variantContextBuilder86.id("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection93 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder94 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection93);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray95 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder96 = variantContextBuilder94.genotypes(genotypeArray95);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder97 = variantContextBuilder86.genotypes(genotypeArray95);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder98 = variantContextBuilder68.genotypes(genotypeArray95);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder99 = variantContextBuilder35.genotypes(genotypeArray95);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strArray23);
        org.junit.Assert.assertArrayEquals(strArray23, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean25 + "' != '" + true + "'", boolean25 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder27);
        org.junit.Assert.assertNotNull(strMap28);
        org.junit.Assert.assertNotNull(strMap29);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + true + "'", boolean33 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(strArray47);
        org.junit.Assert.assertArrayEquals(strArray47, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean49 + "' != '" + true + "'", boolean49 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(strArray60);
        org.junit.Assert.assertArrayEquals(strArray60, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean62 + "' != '" + true + "'", boolean62 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
        org.junit.Assert.assertNotNull(alleleArray81);
        org.junit.Assert.assertArrayEquals(alleleArray81, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean83 + "' != '" + false + "'", boolean83 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder88);
        org.junit.Assert.assertNotNull(genotypeArray95);
        org.junit.Assert.assertArrayEquals(genotypeArray95, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder96);
        org.junit.Assert.assertNotNull(variantContextBuilder97);
        org.junit.Assert.assertNotNull(variantContextBuilder98);
        org.junit.Assert.assertNotNull(variantContextBuilder99);
    }

    @Test
    public void test214() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test214");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.lang.String str7 = variantContextBuilder5.getContig();
        java.lang.Class<?> wildcardClass8 = variantContextBuilder5.getClass();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "hi!" + "'", str7, "hi!");
        org.junit.Assert.assertNotNull(wildcardClass8);
    }

    @Test
    public void test215() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test215");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("hi!", "", 10L, (long) '4', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder12.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError(1.0d);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test216() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test216");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder5.start((long) (byte) 100);
        java.lang.String[] strArray31 = new java.lang.String[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder5.filters(strArray31);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(strArray31);
        org.junit.Assert.assertArrayEquals(strArray31, new java.lang.String[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder32);
    }

    @Test
    public void test217() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test217");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.lang.String[] strArray12 = new java.lang.String[] { "hi!", "hi!", "." };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder8.rmAttributes((java.util.List<java.lang.String>) strList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder8.attribute("", (java.lang.Object) (-1.0d));
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "hi!", "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test218() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test218");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder15.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder19.passFilters();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.log10PError((double) (short) 100);
        java.lang.String[] strArray30 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet31 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean32 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet31, strArray30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder26.filters((java.util.Set<java.lang.String>) strSet31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder26.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap35 = variantContextBuilder26.getAttributes();
        java.lang.String[] strArray39 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder26.filters(strArray39);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder19.alleles(strArray39);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Unexpected base in allele bases 'HI!'");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(strArray30);
        org.junit.Assert.assertArrayEquals(strArray30, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean32 + "' != '" + true + "'", boolean32 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(variantContextBuilder34);
        org.junit.Assert.assertNotNull(strMap35);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder40);
    }

    @Test
    public void test219() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test219");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        java.lang.String[] strArray8 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet9 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet9, strArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder11.log10PError((double) (byte) 100);
        org.junit.Assert.assertNotNull(strArray8);
        org.junit.Assert.assertArrayEquals(strArray8, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
    }

    @Test
    public void test220() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test220");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        java.util.Map<java.lang.String, java.lang.Object> strMap46 = variantContextBuilder45.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder45.fullyDecoded(false);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(strMap46);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
    }

    @Test
    public void test221() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test221");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.Allele[] alleleArray36 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList37 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean38 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37, alleleArray36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList37);
        htsjdk.variant.variantcontext.Allele[] alleleArray55 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList56 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean57 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56, alleleArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList56);
        java.lang.String[] strArray63 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList64 = new java.util.ArrayList<java.lang.String>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList64, strArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder60.rmAttributes((java.util.List<java.lang.String>) strList64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder60.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder41.attribute("", (java.lang.Object) variantContextBuilder68);
        htsjdk.variant.variantcontext.Allele[] alleleArray82 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList83 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean84 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList83, alleleArray82);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder85 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder87 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList83);
        java.lang.String[] strArray89 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder90 = variantContextBuilder87.filters(strArray89);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder91 = variantContextBuilder41.filters(strArray89);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder92 = variantContextBuilder23.filters(strArray89);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(alleleArray36);
        org.junit.Assert.assertArrayEquals(alleleArray36, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean38 + "' != '" + false + "'", boolean38 == false);
        org.junit.Assert.assertNotNull(alleleArray55);
        org.junit.Assert.assertArrayEquals(alleleArray55, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean57 + "' != '" + false + "'", boolean57 == false);
        org.junit.Assert.assertNotNull(strArray63);
        org.junit.Assert.assertArrayEquals(strArray63, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
        org.junit.Assert.assertNotNull(variantContextBuilder69);
        org.junit.Assert.assertNotNull(alleleArray82);
        org.junit.Assert.assertArrayEquals(alleleArray82, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean84 + "' != '" + false + "'", boolean84 == false);
        org.junit.Assert.assertNotNull(strArray89);
        org.junit.Assert.assertArrayEquals(strArray89, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder90);
        org.junit.Assert.assertNotNull(variantContextBuilder91);
        org.junit.Assert.assertNotNull(variantContextBuilder92);
    }

    @Test
    public void test222() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test222");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection12 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.log10PError((double) (short) 100);
        java.lang.String[] strArray17 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet18 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean19 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet18, strArray17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder13.filters((java.util.Set<java.lang.String>) strSet18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder13.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder21.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection29 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder30.log10PError((double) (short) 100);
        java.lang.String[] strArray34 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet35 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean36 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet35, strArray34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder30.filters((java.util.Set<java.lang.String>) strSet35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder30.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap39 = variantContextBuilder30.getAttributes();
        java.lang.String[] strArray43 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder30.filters(strArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder44.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext47 = variantContextBuilder46.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder24.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypesContext47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder7.genotypesNoValidation(genotypesContext47);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection54 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder55.log10PError((double) (short) 100);
        java.lang.String[] strArray59 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet60 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean61 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet60, strArray59);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder55.filters((java.util.Set<java.lang.String>) strSet60);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder55.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder63);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext65 = variantContextBuilder63.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder49.genotypesNoValidation(genotypesContext65);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strArray17);
        org.junit.Assert.assertArrayEquals(strArray17, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + true + "'", boolean19 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(strArray34);
        org.junit.Assert.assertArrayEquals(strArray34, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean36 + "' != '" + true + "'", boolean36 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strMap39);
        org.junit.Assert.assertNotNull(strArray43);
        org.junit.Assert.assertArrayEquals(strArray43, new java.lang.String[] { "hi!", "", "" });
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(genotypesContext47);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(strArray59);
        org.junit.Assert.assertArrayEquals(strArray59, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean61 + "' != '" + true + "'", boolean61 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
        org.junit.Assert.assertNotNull(variantContextBuilder63);
        org.junit.Assert.assertNotNull(genotypesContext65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
    }

    @Test
    public void test223() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test223");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder26.loc("", (long) '4', (long) (short) 100);
        htsjdk.variant.variantcontext.Allele[] alleleArray43 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList44 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44, alleleArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder48.id("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection55 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection55);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray57 = new htsjdk.variant.variantcontext.Genotype[] {};
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder56.genotypes(genotypeArray57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder48.genotypes(genotypeArray57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder30.genotypes(genotypeArray57);
        java.util.Map<java.lang.String, java.lang.Object> strMap61 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder60.attributes(strMap61);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(alleleArray43);
        org.junit.Assert.assertArrayEquals(alleleArray43, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + false + "'", boolean45 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(genotypeArray57);
        org.junit.Assert.assertArrayEquals(genotypeArray57, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(variantContextBuilder59);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
    }

    @Test
    public void test224() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test224");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection18 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection18);
        java.lang.String[] strArray22 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder19.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder5.rmAttribute("hi!");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder5.start((long) (byte) 100);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext31 = variantContextBuilder5.getGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(genotypesContext31);
    }

    @Test
    public void test225() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test225");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder14.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder15.noID();
        htsjdk.variant.variantcontext.Allele[] alleleArray25 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList26 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26, alleleArray25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList26);
        long long30 = variantContextBuilder29.getStart();
        java.lang.String[] strArray33 = new java.lang.String[] { "", "" };
        java.util.LinkedHashSet<java.lang.String> strSet34 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder29.filters((java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder16.filters((java.util.Set<java.lang.String>) strSet34);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(alleleArray25);
        org.junit.Assert.assertArrayEquals(alleleArray25, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertTrue("'" + long30 + "' != '" + 100L + "'", long30 == 100L);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
    }

    @Test
    public void test226() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test226");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        long long12 = variantContextBuilder11.getStart();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder11.stop((long) (byte) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder14.passFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertTrue("'" + long12 + "' != '" + 0L + "'", long12 == 0L);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test227() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test227");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.lang.String[] strArray12 = new java.lang.String[] { "hi!", "hi!", "." };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder8.rmAttributes((java.util.List<java.lang.String>) strList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder8.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder17.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection23 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.log10PError((double) (short) 100);
        java.lang.String[] strArray28 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet29 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean30 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet29, strArray28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder24.filters((java.util.Set<java.lang.String>) strSet29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder24.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder32.fullyDecoded(true);
        htsjdk.variant.variantcontext.Allele[] alleleArray48 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList49 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList49, alleleArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList49);
        java.lang.String[] strArray55 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder53.filters(strArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder35.filters(strArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder18.filters(strArray55);
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "hi!", "hi!", "." });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray28);
        org.junit.Assert.assertArrayEquals(strArray28, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean30 + "' != '" + true + "'", boolean30 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder35);
        org.junit.Assert.assertNotNull(alleleArray48);
        org.junit.Assert.assertArrayEquals(alleleArray48, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + false + "'", boolean50 == false);
        org.junit.Assert.assertNotNull(strArray55);
        org.junit.Assert.assertArrayEquals(strArray55, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
    }

    @Test
    public void test228() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test228");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder14.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder15.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder15.source("");
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test229() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test229");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder12.loc("", (long) (short) 1, (long) 1);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext19 = variantContextBuilder12.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Cannot create a VariantContext with an empty allele list");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
    }

    @Test
    public void test230() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test230");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.id("");
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext20 = variantContextBuilder19.getGenotypes();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(genotypesContext20);
    }

    @Test
    public void test231() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test231");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder7.chr("");
        java.lang.String[] strArray12 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList13 = new java.util.ArrayList<java.lang.String>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList13, strArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder9.rmAttributes((java.util.List<java.lang.String>) strList13);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContext variantContext16 = variantContextBuilder9.make();
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: log10PError cannot be > 0 : 1.0");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(strArray12);
        org.junit.Assert.assertArrayEquals(strArray12, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + true + "'", boolean14 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
    }

    @Test
    public void test232() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test232");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection11 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection11);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.log10PError((double) (short) 100);
        java.lang.String[] strArray16 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet17 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet17, strArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder12.filters((java.util.Set<java.lang.String>) strSet17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder12.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        java.lang.String[] strArray29 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet30 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean31 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet30, strArray29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder26.filters((java.util.Set<java.lang.String>) strSet30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder12.filters((java.util.Set<java.lang.String>) strSet30);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection38 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder39.log10PError((double) (short) 100);
        java.lang.String[] strArray43 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet44 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet44, strArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder39.filters((java.util.Set<java.lang.String>) strSet44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder39.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray50 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList51 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean52 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList51, alleleArray50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder49.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder49.source("hi!");
        java.util.Set<java.lang.String> strSet56 = variantContextBuilder55.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = variantContextBuilder33.filters(strSet56);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder5.filters(strSet56);
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(strArray16);
        org.junit.Assert.assertArrayEquals(strArray16, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray29);
        org.junit.Assert.assertArrayEquals(strArray29, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean31 + "' != '" + true + "'", boolean31 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder32);
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(strArray43);
        org.junit.Assert.assertArrayEquals(strArray43, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + true + "'", boolean45 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(alleleArray50);
        org.junit.Assert.assertArrayEquals(alleleArray50, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean52 + "' != '" + false + "'", boolean52 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strSet56);
        org.junit.Assert.assertNotNull(variantContextBuilder57);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
    }

    @Test
    public void test233() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test233");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.start((long) 10);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray25 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList26 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean27 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList26, genotypeArray25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder22.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList26);
        java.util.Map<java.lang.String, java.lang.Object> strMap29 = variantContextBuilder22.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder14.attributes(strMap29);
        java.lang.String str31 = variantContextBuilder14.getID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder14.source("");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection38 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection38);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder39.log10PError((double) (short) 100);
        java.lang.String[] strArray43 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet44 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet44, strArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder39.filters((java.util.Set<java.lang.String>) strSet44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder39.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap48 = variantContextBuilder39.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap49 = variantContextBuilder39.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray54 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList55 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean56 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55, alleleArray54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder39.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder14.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList55, (-1), 0);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(genotypeArray25);
        org.junit.Assert.assertArrayEquals(genotypeArray25, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean27 + "' != '" + false + "'", boolean27 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(strMap29);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertEquals("'" + str31 + "' != '" + "." + "'", str31, ".");
        org.junit.Assert.assertNotNull(variantContextBuilder33);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(strArray43);
        org.junit.Assert.assertArrayEquals(strArray43, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + true + "'", boolean45 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(strMap48);
        org.junit.Assert.assertNotNull(strMap49);
        org.junit.Assert.assertNotNull(alleleArray54);
        org.junit.Assert.assertArrayEquals(alleleArray54, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean56 + "' != '" + false + "'", boolean56 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
    }

    @Test
    public void test234() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test234");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Map<java.lang.String, java.lang.Object> strMap29 = variantContextBuilder13.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder13.stop((-1L));
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection36 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder37.log10PError((double) (short) 100);
        java.lang.String[] strArray41 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet42 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder37.filters((java.util.Set<java.lang.String>) strSet42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder37.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = variantContextBuilder45.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray48 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList49 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList49, alleleArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder47.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList49);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder13.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList49, 100);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(strMap29);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder47);
        org.junit.Assert.assertNotNull(alleleArray48);
        org.junit.Assert.assertArrayEquals(alleleArray48, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + false + "'", boolean50 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
    }

    @Test
    public void test235() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test235");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.noID();
        long long8 = variantContextBuilder7.getStart();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertTrue("'" + long8 + "' != '" + 0L + "'", long8 == 0L);
    }

    @Test
    public void test236() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test236");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.log10PError((-1.0d));
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder15.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray18 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList19 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19, genotypeArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList19);
        java.util.Map<java.lang.String, java.lang.Object> strMap22 = variantContextBuilder15.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder15.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection28 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder29.log10PError((double) (short) 100);
        java.lang.String[] strArray33 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet34 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder29.filters((java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder29.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap38 = variantContextBuilder29.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap39 = variantContextBuilder29.getAttributes();
        java.lang.String[] strArray41 = new java.lang.String[] { "hi!" };
        java.util.ArrayList<java.lang.String> strList42 = new java.util.ArrayList<java.lang.String>();
        boolean boolean43 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList42, strArray41);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder29.rmAttributes((java.util.List<java.lang.String>) strList42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder15.rmAttributes((java.util.List<java.lang.String>) strList42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList42);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection51 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder52.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray55 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList56 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean57 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList56, genotypeArray55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder52.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList56);
        java.util.Map<java.lang.String, java.lang.Object> strMap59 = variantContextBuilder52.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder46.putAttributes(strMap59);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = variantContextBuilder46.fullyDecoded(false);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder46.fullyDecoded(false);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(genotypeArray18);
        org.junit.Assert.assertArrayEquals(genotypeArray18, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + false + "'", boolean20 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(strMap22);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(strMap38);
        org.junit.Assert.assertNotNull(strMap39);
        org.junit.Assert.assertNotNull(strArray41);
        org.junit.Assert.assertArrayEquals(strArray41, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertTrue("'" + boolean43 + "' != '" + true + "'", boolean43 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder46);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(genotypeArray55);
        org.junit.Assert.assertArrayEquals(genotypeArray55, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean57 + "' != '" + false + "'", boolean57 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder58);
        org.junit.Assert.assertNotNull(strMap59);
        org.junit.Assert.assertNotNull(variantContextBuilder60);
        org.junit.Assert.assertNotNull(variantContextBuilder62);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
    }

    @Test
    public void test237() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test237");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection8 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder9.log10PError((double) (short) 100);
        java.lang.String[] strArray13 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet14 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean15 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet14, strArray13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder9.filters((java.util.Set<java.lang.String>) strSet14);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder9.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap18 = variantContextBuilder9.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap19 = variantContextBuilder9.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray24 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList25 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean26 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList25, alleleArray24);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder9.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "hi!", (long) ' ', (long) ' ', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList25);
        htsjdk.variant.variantcontext.Allele[] alleleArray43 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList44 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44, alleleArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList44);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder48.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder50.id("");
        htsjdk.variant.variantcontext.Allele[] alleleArray61 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList62 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList62, alleleArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder65.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder67.start((long) 10);
        java.util.List<htsjdk.variant.variantcontext.Allele> alleleList70 = variantContextBuilder67.getAlleles();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder52.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList70);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder29.attribute(".", (java.lang.Object) alleleList70);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strArray13);
        org.junit.Assert.assertArrayEquals(strArray13, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder16);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(strMap18);
        org.junit.Assert.assertNotNull(strMap19);
        org.junit.Assert.assertNotNull(alleleArray24);
        org.junit.Assert.assertArrayEquals(alleleArray24, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean26 + "' != '" + false + "'", boolean26 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(alleleArray43);
        org.junit.Assert.assertArrayEquals(alleleArray43, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean45 + "' != '" + false + "'", boolean45 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder50);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(alleleArray61);
        org.junit.Assert.assertArrayEquals(alleleArray61, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + false + "'", boolean63 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(variantContextBuilder69);
        org.junit.Assert.assertNotNull(alleleList70);
        org.junit.Assert.assertNotNull(variantContextBuilder71);
        org.junit.Assert.assertNotNull(variantContextBuilder72);
    }

    @Test
    public void test238() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test238");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.noGenotypes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder18.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap28 = variantContextBuilder18.getAttributes();
        htsjdk.variant.variantcontext.Allele[] alleleArray33 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList34 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34, alleleArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder18.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder(".", "hi!", (long) ' ', (long) ' ', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder5.computeEndFromAlleles((java.util.List<htsjdk.variant.variantcontext.Allele>) alleleList34, (int) (byte) 10, (int) (byte) 10);
            org.junit.Assert.fail("Expected exception of type java.lang.IndexOutOfBoundsException; message: Index 0 out of bounds for length 0");
        } catch (java.lang.IndexOutOfBoundsException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(strMap28);
        org.junit.Assert.assertNotNull(alleleArray33);
        org.junit.Assert.assertArrayEquals(alleleArray33, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + false + "'", boolean35 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
    }

    @Test
    public void test239() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test239");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        long long6 = variantContextBuilder5.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext7 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.genotypes(genotypesContext7);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection14 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection14);
        java.lang.String[] strArray18 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet19 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean20 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet19, strArray18);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder15.filters((java.util.Set<java.lang.String>) strSet19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder8.attribute(".", (java.lang.Object) variantContextBuilder15);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection28 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection28);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder29.log10PError((double) (short) 100);
        java.lang.String[] strArray33 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet34 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder29.filters((java.util.Set<java.lang.String>) strSet34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder29.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder37.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection45 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder46.log10PError((double) (short) 100);
        java.lang.String str49 = variantContextBuilder46.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext50 = variantContextBuilder46.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder37.genotypes(genotypesContext50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder22.attribute("hi!", (java.lang.Object) genotypesContext50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder22.chr("");
        org.junit.Assert.assertTrue("'" + long6 + "' != '" + 52L + "'", long6 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder8);
        org.junit.Assert.assertNotNull(strArray18);
        org.junit.Assert.assertArrayEquals(strArray18, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(variantContextBuilder31);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
        org.junit.Assert.assertNotNull(variantContextBuilder37);
        org.junit.Assert.assertNotNull(variantContextBuilder40);
        org.junit.Assert.assertNotNull(variantContextBuilder48);
        org.junit.Assert.assertEquals("'" + str49 + "' != '" + "hi!" + "'", str49, "hi!");
        org.junit.Assert.assertNotNull(genotypesContext50);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
    }

    @Test
    public void test240() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test240");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        long long11 = variantContextBuilder10.getStart();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder10.start((long) (byte) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder13.noGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder14.loc("hi!", (long) (short) 10, (long) (short) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder14.unfiltered();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertTrue("'" + long11 + "' != '" + 10L + "'", long11 == 10L);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
    }

    @Test
    public void test241() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test241");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        long long13 = variantContextBuilder12.getStart();
        java.lang.String[] strArray16 = new java.lang.String[] { "", "" };
        java.util.LinkedHashSet<java.lang.String> strSet17 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet17, strArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder12.filters((java.util.Set<java.lang.String>) strSet17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder12.fullyDecoded(false);
        org.junit.Assert.assertNotNull(alleleArray8);
        org.junit.Assert.assertArrayEquals(alleleArray8, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertTrue("'" + long13 + "' != '" + 100L + "'", long13 == 100L);
        org.junit.Assert.assertNotNull(strArray16);
        org.junit.Assert.assertArrayEquals(strArray16, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + true + "'", boolean18 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder21);
    }

    @Test
    public void test242() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test242");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        java.util.Map<java.lang.String, java.lang.Object> strMap16 = variantContextBuilder13.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection21 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = variantContextBuilder22.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder24.chr("");
        java.util.Map<java.lang.String, java.lang.Object> strMap27 = variantContextBuilder26.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder13.attributes(strMap27);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection34 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection34);
        long long36 = variantContextBuilder35.getStop();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext37 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder35.genotypes(genotypesContext37);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection44 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection44);
        java.lang.String[] strArray48 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet49 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean50 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet49, strArray48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder45.filters((java.util.Set<java.lang.String>) strSet49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder38.attribute(".", (java.lang.Object) variantContextBuilder45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder28.attribute("", (java.lang.Object) variantContextBuilder38);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection58 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.log10PError((double) (short) 100);
        java.lang.String[] strArray63 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet64 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet64, strArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder59.filters((java.util.Set<java.lang.String>) strSet64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder59.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder67.fullyDecoded(true);
        htsjdk.variant.variantcontext.Allele[] alleleArray83 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList84 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean85 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84, alleleArray83);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder86 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder87 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder88 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList84);
        java.lang.String[] strArray90 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder91 = variantContextBuilder88.filters(strArray90);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder92 = variantContextBuilder70.filters(strArray90);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder93 = variantContextBuilder38.filters(strArray90);
        java.util.Map<java.lang.String, java.lang.Object> strMap94 = variantContextBuilder93.getAttributes();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(strMap16);
        org.junit.Assert.assertNotNull(variantContextBuilder24);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strMap27);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertTrue("'" + long36 + "' != '" + 52L + "'", long36 == 52L);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(strArray48);
        org.junit.Assert.assertArrayEquals(strArray48, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean50 + "' != '" + true + "'", boolean50 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder51);
        org.junit.Assert.assertNotNull(variantContextBuilder52);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(strArray63);
        org.junit.Assert.assertArrayEquals(strArray63, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(alleleArray83);
        org.junit.Assert.assertArrayEquals(alleleArray83, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean85 + "' != '" + false + "'", boolean85 == false);
        org.junit.Assert.assertNotNull(strArray90);
        org.junit.Assert.assertArrayEquals(strArray90, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder91);
        org.junit.Assert.assertNotNull(variantContextBuilder92);
        org.junit.Assert.assertNotNull(variantContextBuilder93);
        org.junit.Assert.assertNotNull(strMap94);
    }

    @Test
    public void test243() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test243");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder20.chr("");
        java.util.List<htsjdk.variant.variantcontext.Allele> alleleList23 = variantContextBuilder20.getAlleles();
        java.lang.Class<?> wildcardClass24 = alleleList23.getClass();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
        org.junit.Assert.assertNotNull(alleleList23);
        org.junit.Assert.assertNotNull(wildcardClass24);
    }

    @Test
    public void test244() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test244");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.Allele[] alleleArray31 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList32 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32, alleleArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList32);
        java.lang.String[] strArray39 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList40 = new java.util.ArrayList<java.lang.String>();
        boolean boolean41 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList40, strArray39);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder36.rmAttributes((java.util.List<java.lang.String>) strList40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder36.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder17.attribute("", (java.lang.Object) variantContextBuilder44);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection50 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection50);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder53 = variantContextBuilder51.log10PError((double) (short) 100);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection58 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.log10PError((double) (short) 100);
        java.lang.String[] strArray63 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet64 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean65 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet64, strArray63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder59.filters((java.util.Set<java.lang.String>) strSet64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = variantContextBuilder59.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap68 = variantContextBuilder59.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder53.putAttributes(strMap68);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder17.attributes(strMap68);
        java.util.Set<java.lang.String> strSet71 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder17.filters(strSet71);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(alleleArray31);
        org.junit.Assert.assertArrayEquals(alleleArray31, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean33 + "' != '" + false + "'", boolean33 == false);
        org.junit.Assert.assertNotNull(strArray39);
        org.junit.Assert.assertArrayEquals(strArray39, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean41 + "' != '" + true + "'", boolean41 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder42);
        org.junit.Assert.assertNotNull(variantContextBuilder44);
        org.junit.Assert.assertNotNull(variantContextBuilder45);
        org.junit.Assert.assertNotNull(variantContextBuilder53);
        org.junit.Assert.assertNotNull(variantContextBuilder61);
        org.junit.Assert.assertNotNull(strArray63);
        org.junit.Assert.assertArrayEquals(strArray63, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean65 + "' != '" + true + "'", boolean65 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder67);
        org.junit.Assert.assertNotNull(strMap68);
        org.junit.Assert.assertNotNull(variantContextBuilder69);
        org.junit.Assert.assertNotNull(variantContextBuilder70);
        org.junit.Assert.assertNotNull(variantContextBuilder72);
    }

    @Test
    public void test245() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test245");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        java.lang.String str15 = variantContextBuilder14.getContig();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertEquals("'" + str15 + "' != '" + "hi!" + "'", str15, "hi!");
    }

    @Test
    public void test246() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test246");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = variantContextBuilder13.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.Allele[] alleleArray16 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList17 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean18 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17, alleleArray16);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder15.alleles((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder19.passFilters();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.chr("");
        java.lang.String[] strArray33 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList34 = new java.util.ArrayList<java.lang.String>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList34, strArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder30.rmAttributes((java.util.List<java.lang.String>) strList34);
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder20.alleles((java.util.List<java.lang.String>) strList34);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: Null alleles are not supported");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertNotNull(variantContextBuilder15);
        org.junit.Assert.assertNotNull(alleleArray16);
        org.junit.Assert.assertArrayEquals(alleleArray16, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean18 + "' != '" + false + "'", boolean18 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder28);
        org.junit.Assert.assertNotNull(variantContextBuilder30);
        org.junit.Assert.assertNotNull(strArray33);
        org.junit.Assert.assertArrayEquals(strArray33, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean35 + "' != '" + true + "'", boolean35 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder36);
    }

    @Test
    public void test247() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test247");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray20 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList21 = new java.util.ArrayList<java.lang.String>();
        boolean boolean22 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList21, strArray20);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder23 = variantContextBuilder17.rmAttributes((java.util.List<java.lang.String>) strList21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder17.fullyDecoded(false);
        long long26 = variantContextBuilder25.getStop();
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray20);
        org.junit.Assert.assertArrayEquals(strArray20, new java.lang.String[] { "", "" });
        org.junit.Assert.assertTrue("'" + boolean22 + "' != '" + true + "'", boolean22 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder23);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertTrue("'" + long26 + "' != '" + 0L + "'", long26 == 0L);
    }

    @Test
    public void test248() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test248");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray8 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9, genotypeArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList9);
        java.util.Map<java.lang.String, java.lang.Object> strMap12 = variantContextBuilder5.getAttributes();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection17 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection17);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.log10PError((double) (short) 100);
        java.lang.String[] strArray22 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet23 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean24 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet23, strArray22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet23);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = variantContextBuilder18.noID();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection31 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection31);
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "hi!" };
        java.util.LinkedHashSet<java.lang.String> strSet36 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean37 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet36, strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder32.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder18.filters((java.util.Set<java.lang.String>) strSet36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder18.rmAttribute("hi!");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection46 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder47 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder47.log10PError((double) (short) 100);
        java.lang.String[] strArray51 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet52 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean53 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet52, strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder47.filters((java.util.Set<java.lang.String>) strSet52);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder55 = variantContextBuilder47.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap56 = variantContextBuilder47.getAttributes();
        java.util.Map<java.lang.String, java.lang.Object> strMap57 = variantContextBuilder47.getAttributes();
        java.lang.String[] strArray61 = new java.lang.String[] { "", "hi!", "" };
        java.util.ArrayList<java.lang.String> strList62 = new java.util.ArrayList<java.lang.String>();
        boolean boolean63 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList62, strArray61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder47.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder41.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder5.rmAttributes((java.util.List<java.lang.String>) strList62);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext67 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder5.genotypes(genotypesContext67);
        java.util.Set<java.lang.String> strSet69 = variantContextBuilder5.getFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(genotypeArray8);
        org.junit.Assert.assertArrayEquals(genotypeArray8, new htsjdk.variant.variantcontext.Genotype[] {});
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
        org.junit.Assert.assertNotNull(strMap12);
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(strArray22);
        org.junit.Assert.assertArrayEquals(strArray22, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean24 + "' != '" + true + "'", boolean24 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder25);
        org.junit.Assert.assertNotNull(variantContextBuilder26);
        org.junit.Assert.assertNotNull(strArray35);
        org.junit.Assert.assertArrayEquals(strArray35, new java.lang.String[] { "hi!", "hi!" });
        org.junit.Assert.assertTrue("'" + boolean37 + "' != '" + true + "'", boolean37 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder38);
        org.junit.Assert.assertNotNull(variantContextBuilder39);
        org.junit.Assert.assertNotNull(variantContextBuilder41);
        org.junit.Assert.assertNotNull(variantContextBuilder49);
        org.junit.Assert.assertNotNull(strArray51);
        org.junit.Assert.assertArrayEquals(strArray51, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean53 + "' != '" + true + "'", boolean53 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder54);
        org.junit.Assert.assertNotNull(variantContextBuilder55);
        org.junit.Assert.assertNotNull(strMap56);
        org.junit.Assert.assertNotNull(strMap57);
        org.junit.Assert.assertNotNull(strArray61);
        org.junit.Assert.assertArrayEquals(strArray61, new java.lang.String[] { "", "hi!", "" });
        org.junit.Assert.assertTrue("'" + boolean63 + "' != '" + true + "'", boolean63 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder64);
        org.junit.Assert.assertNotNull(variantContextBuilder65);
        org.junit.Assert.assertNotNull(variantContextBuilder66);
        org.junit.Assert.assertNotNull(variantContextBuilder68);
        org.junit.Assert.assertNull(strSet69);
    }

    @Test
    public void test249() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test249");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.loc("hi!", (long) (byte) 10, (long) 1);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder10 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder10.loc(".", 0L, (long) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = variantContextBuilder14.loc(".", (-1L), 100L);
        java.util.Set<java.lang.String> strSet19 = variantContextBuilder14.getFilters();
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNotNull(variantContextBuilder10);
        org.junit.Assert.assertNotNull(variantContextBuilder14);
        org.junit.Assert.assertNotNull(variantContextBuilder18);
        org.junit.Assert.assertNull(strSet19);
    }

    @Test
    public void test250() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test250");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder22 = variantContextBuilder20.stop(10L);
        org.junit.Assert.assertNotNull(alleleArray12);
        org.junit.Assert.assertArrayEquals(alleleArray12, new htsjdk.variant.variantcontext.Allele[] {});
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
        org.junit.Assert.assertNotNull(strArray19);
        org.junit.Assert.assertArrayEquals(strArray19, new java.lang.String[] { "hi!" });
        org.junit.Assert.assertNotNull(variantContextBuilder20);
        org.junit.Assert.assertNotNull(variantContextBuilder22);
    }

    @Test
    public void test251() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test251");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.log10PError((double) (short) 100);
        java.lang.String[] strArray9 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet10 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean11 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet10, strArray9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = variantContextBuilder5.filters((java.util.Set<java.lang.String>) strSet10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder13 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder13);
        boolean boolean15 = variantContextBuilder14.isFullyDecoded();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder14.id(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder19 = variantContextBuilder17.fullyDecoded(true);
        boolean boolean20 = variantContextBuilder17.isFullyDecoded();
        org.junit.Assert.assertNotNull(variantContextBuilder7);
        org.junit.Assert.assertNotNull(strArray9);
        org.junit.Assert.assertArrayEquals(strArray9, new java.lang.String[] { "" });
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
        org.junit.Assert.assertNotNull(variantContextBuilder12);
        org.junit.Assert.assertNotNull(variantContextBuilder13);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + false + "'", boolean15 == false);
        org.junit.Assert.assertNotNull(variantContextBuilder17);
        org.junit.Assert.assertNotNull(variantContextBuilder19);
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
    }

    @Test
    public void test252() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test252");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        java.lang.String str7 = variantContextBuilder5.getContig();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder9 = variantContextBuilder5.source(".");
        java.util.Set<java.lang.String> strSet10 = variantContextBuilder5.getFilters();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = variantContextBuilder5.noGenotypes();
        org.junit.Assert.assertNotNull(variantContextBuilder6);
        org.junit.Assert.assertEquals("'" + str7 + "' != '" + "hi!" + "'", str7, "hi!");
        org.junit.Assert.assertNotNull(variantContextBuilder9);
        org.junit.Assert.assertNull(strSet10);
        org.junit.Assert.assertNotNull(variantContextBuilder11);
    }

    @Test
    public void test253() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test253");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = null;
        // The following exception was thrown during execution in test generation
        try {
            htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder1 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder0);
            org.junit.Assert.fail("Expected exception of type java.lang.IllegalArgumentException; message: BUG: VariantContext parent argument cannot be null in VariantContextBuilder");
        } catch (java.lang.IllegalArgumentException e) {
            // Expected exception.
        }
    }

    @Test
    public void test254() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test254");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder0 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder1 = variantContextBuilder0.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder2 = variantContextBuilder0.noGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder3 = variantContextBuilder0.noGenotypes();
        java.util.Map<java.lang.String, java.lang.Object> strMap4 = variantContextBuilder0.getAttributes();
        org.junit.Assert.assertNotNull(variantContextBuilder1);
        org.junit.Assert.assertNotNull(variantContextBuilder2);
        org.junit.Assert.assertNotNull(variantContextBuilder3);
        org.junit.Assert.assertNull(strMap4);
    }
}

