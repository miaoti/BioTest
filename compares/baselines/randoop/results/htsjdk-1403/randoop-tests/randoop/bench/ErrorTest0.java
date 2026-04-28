package randoop.bench;

import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class ErrorTest0 {

    public static boolean debug = false;

    @Test
    public void test01() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test01");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection37 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection37);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder38.log10PError((double) (short) 100);
        java.lang.String[] strArray42 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet43 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean44 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet43, strArray42);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder45 = variantContextBuilder38.filters((java.util.Set<java.lang.String>) strSet43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder38.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap47 = variantContextBuilder38.getAttributes();
        java.lang.String[] strArray51 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder38.filters(strArray51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder52.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext55 = variantContextBuilder54.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder32.genotypesNoValidation(genotypesContext55);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypeList28 and genotypesContext55.", genotypeList28.equals(genotypesContext55) == genotypesContext55.equals(genotypeList28));
    }

    @Test
    public void test02() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test02");
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
        java.lang.String[] strArray26 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet27 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean28 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet27, strArray26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder22.filters((java.util.Set<java.lang.String>) strSet27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder22.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap31 = variantContextBuilder22.getAttributes();
        java.lang.String[] strArray35 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder22.filters(strArray35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext39 = variantContextBuilder38.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder16.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypesContext39);
        htsjdk.variant.variantcontext.Allele[] alleleArray54 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList55 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean56 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55, alleleArray54);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder57 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList55);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder61.stop((long) (byte) 0);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder40.attribute("", (java.lang.Object) variantContextBuilder63);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypesContext39 and alleleList55.", genotypesContext39.equals(alleleList55) == alleleList55.equals(genotypesContext39));
    }

    @Test
    public void test03() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test03");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection40 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder41.log10PError((double) (short) 100);
        java.lang.String[] strArray45 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet46 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean47 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet46, strArray45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder41.filters((java.util.Set<java.lang.String>) strSet46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder41.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder49.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection57 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder58.log10PError((double) (short) 100);
        java.lang.String[] strArray62 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet63 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean64 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet63, strArray62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder65 = variantContextBuilder58.filters((java.util.Set<java.lang.String>) strSet63);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder66 = variantContextBuilder58.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap67 = variantContextBuilder58.getAttributes();
        java.lang.String[] strArray71 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder58.filters(strArray71);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder72.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext75 = variantContextBuilder74.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder52.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypesContext75);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder77 = variantContextBuilder35.genotypes(genotypesContext75);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList17 and genotypesContext75.", alleleList17.equals(genotypesContext75) == genotypesContext75.equals(alleleList17));
    }

    @Test
    public void test04() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test04");
        htsjdk.variant.variantcontext.Allele[] alleleArray8 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList9 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean10 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9, alleleArray8);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder11 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder12 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList9);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder14 = variantContextBuilder12.filter("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = variantContextBuilder14.start((long) 10);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = variantContextBuilder16.copy();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder18 = new htsjdk.variant.variantcontext.VariantContextBuilder();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder18.id(".");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder21 = variantContextBuilder18.copy();
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder35.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection43 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder44.log10PError((double) (short) 100);
        java.lang.String str47 = variantContextBuilder44.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext48 = variantContextBuilder44.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder35.genotypes(genotypesContext48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = variantContextBuilder18.genotypes(genotypesContext48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = variantContextBuilder17.genotypes(genotypesContext48);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList9 and genotypesContext48.", alleleList9.equals(genotypesContext48) == genotypesContext48.equals(alleleList9));
    }

    @Test
    public void test05() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test05");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection40 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection40);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder43 = variantContextBuilder41.log10PError((double) (short) 100);
        java.lang.String[] strArray45 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet46 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean47 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet46, strArray45);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder48 = variantContextBuilder41.filters((java.util.Set<java.lang.String>) strSet46);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder41.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder49);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = variantContextBuilder49.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection57 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection57);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder60 = variantContextBuilder58.log10PError((double) (short) 100);
        java.lang.String str61 = variantContextBuilder58.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext62 = variantContextBuilder58.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder49.genotypes(genotypesContext62);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder22.genotypesNoValidation(genotypesContext62);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList17 and genotypesContext62.", alleleList17.equals(genotypesContext62) == genotypesContext62.equals(alleleList17));
    }

    @Test
    public void test06() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test06");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection73 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection73);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = variantContextBuilder74.log10PError((double) (short) 100);
        java.lang.String[] strArray78 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet79 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean80 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet79, strArray78);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder81 = variantContextBuilder74.filters((java.util.Set<java.lang.String>) strSet79);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder82 = variantContextBuilder74.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder83 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder82);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder85 = variantContextBuilder82.fullyDecoded(true);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection90 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder91 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection90);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder93 = variantContextBuilder91.log10PError((double) (short) 100);
        java.lang.String str94 = variantContextBuilder91.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext95 = variantContextBuilder91.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder96 = variantContextBuilder82.genotypes(genotypesContext95);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder97 = variantContextBuilder5.genotypes(genotypesContext95);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypeList9 and genotypesContext95.", genotypeList9.equals(genotypesContext95) == genotypesContext95.equals(genotypeList9));
    }

    @Test
    public void test07() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test07");
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
        java.util.Map<java.lang.String, java.lang.Object> strMap54 = variantContextBuilder45.getAttributes();
        java.lang.String[] strArray58 = new java.lang.String[] { "hi!", "", "" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder59 = variantContextBuilder45.filters(strArray58);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder61 = variantContextBuilder59.start((long) (short) 0);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext62 = variantContextBuilder61.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder63 = variantContextBuilder39.genotypesNoValidation(genotypesContext62);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList13 and genotypesContext62.", alleleList13.equals(genotypesContext62) == genotypesContext62.equals(alleleList13));
    }

    @Test
    public void test08() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test08");
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
        htsjdk.variant.variantcontext.Allele[] alleleArray29 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList30 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean31 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList30, alleleArray29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList30);
        java.lang.String[] strArray36 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder34.filters(strArray36);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder16.filters(strArray36);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection43 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder44.log10PError((double) (short) 100);
        java.lang.String str47 = variantContextBuilder44.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext48 = variantContextBuilder44.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder49 = variantContextBuilder38.genotypesNoValidation(genotypesContext48);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList30 and genotypesContext48.", alleleList30.equals(genotypesContext48) == genotypesContext48.equals(alleleList30));
    }

    @Test
    public void test09() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test09");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection27 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection27);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = variantContextBuilder28.log10PError((double) (short) 100);
        java.lang.String[] strArray32 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet33 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean34 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet33, strArray32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder28.filters((java.util.Set<java.lang.String>) strSet33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = variantContextBuilder28.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder36);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext38 = variantContextBuilder36.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder39 = variantContextBuilder9.genotypesNoValidation(genotypesContext38);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypeList19 and genotypesContext38.", genotypeList19.equals(genotypesContext38) == genotypesContext38.equals(genotypeList19));
    }

    @Test
    public void test10() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test10");
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
        htsjdk.variant.variantcontext.Allele[] alleleArray33 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList34 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean35 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34, alleleArray33);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList34);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder38.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder42 = variantContextBuilder40.id("");
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext43 = variantContextBuilder42.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder44 = variantContextBuilder19.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypesContext43);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList17 and genotypesContext43.", alleleList17.equals(genotypesContext43) == genotypesContext43.equals(alleleList17));
    }

    @Test
    public void test11() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test11");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection29 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder30 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection29);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder32 = variantContextBuilder30.log10PError((double) (short) 100);
        java.lang.String str33 = variantContextBuilder30.getContig();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext34 = variantContextBuilder30.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder5.genotypes(genotypesContext34);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList21 and genotypesContext34.", alleleList21.equals(genotypesContext34) == genotypesContext34.equals(alleleList21));
    }

    @Test
    public void test12() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test12");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection75 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder76 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection75);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder78 = variantContextBuilder76.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder80 = variantContextBuilder78.start((long) (short) 10);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext81 = variantContextBuilder78.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder82 = variantContextBuilder70.genotypes(genotypesContext81);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList31 and genotypesContext81.", alleleList31.equals(genotypesContext81) == genotypesContext81.equals(alleleList31));
    }

    @Test
    public void test13() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test13");
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
        htsjdk.variant.variantcontext.Allele[] alleleArray47 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList48 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean49 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48, alleleArray47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder52.id("");
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder54.stop((long) (byte) 0);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection61 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder62.log10PError((double) (short) 100);
        java.lang.String[] strArray66 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet67 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean68 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet67, strArray66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder62.filters((java.util.Set<java.lang.String>) strSet67);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder62.noID();
        java.util.Map<java.lang.String, java.lang.Object> strMap71 = variantContextBuilder62.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder54.putAttributes(strMap71);
        java.util.Map<java.lang.String, java.lang.Object> strMap73 = variantContextBuilder54.getAttributes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder7.attributes(strMap73);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypesContext32 and alleleList48.", genotypesContext32.equals(alleleList48) == alleleList48.equals(genotypesContext32));
    }

    @Test
    public void test14() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test14");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection35 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection35);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder36.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder40 = variantContextBuilder38.chr("");
        java.lang.String[] strArray43 = new java.lang.String[] { "", "" };
        java.util.ArrayList<java.lang.String> strList44 = new java.util.ArrayList<java.lang.String>();
        boolean boolean45 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strList44, strArray43);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder46 = variantContextBuilder40.rmAttributes((java.util.List<java.lang.String>) strList44);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection51 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection51);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder52.loc("hi!", (long) (byte) 10, (long) 1);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection61 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder62 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection61);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder64 = variantContextBuilder62.log10PError((double) (short) 100);
        htsjdk.variant.variantcontext.Genotype[] genotypeArray65 = new htsjdk.variant.variantcontext.Genotype[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Genotype> genotypeList66 = new java.util.ArrayList<htsjdk.variant.variantcontext.Genotype>();
        boolean boolean67 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList66, genotypeArray65);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = variantContextBuilder62.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = variantContextBuilder56.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList66);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder70 = variantContextBuilder40.genotypes((java.util.Collection<htsjdk.variant.variantcontext.Genotype>) genotypeList66);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext71 = variantContextBuilder40.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder72 = variantContextBuilder28.genotypesNoValidation(genotypesContext71);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypeList66 and genotypesContext71.", genotypeList66.equals(genotypesContext71) == genotypesContext71.equals(genotypeList66));
    }

    @Test
    public void test15() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test15");
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
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder41 = variantContextBuilder9.unfiltered();
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypeList35 and genotypesContext40.", genotypeList35.equals(genotypesContext40) == genotypesContext40.equals(genotypeList35));
    }

    @Test
    public void test16() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test16");
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection4 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder5 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection4);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder6 = variantContextBuilder5.unfiltered();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder7 = variantContextBuilder5.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder8 = variantContextBuilder5.noGenotypes();
        htsjdk.variant.variantcontext.Allele[] alleleArray21 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList22 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean23 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22, alleleArray21);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder24 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder25 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList22);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.id("");
        long long29 = variantContextBuilder26.getStart();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext30 = variantContextBuilder26.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder31 = variantContextBuilder5.genotypes(genotypesContext30);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList22 and genotypesContext30.", alleleList22.equals(genotypesContext30) == genotypesContext30.equals(alleleList22));
    }

    @Test
    public void test17() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test17");
        htsjdk.variant.variantcontext.Allele[] alleleArray12 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList13 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean14 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13, alleleArray12);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder15 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder16 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder17 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList13);
        java.lang.String[] strArray19 = new java.lang.String[] { "hi!" };
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder20 = variantContextBuilder17.filters(strArray19);
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection25 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder26 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection25);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder28 = variantContextBuilder26.log10PError((double) (short) 100);
        java.lang.String[] strArray30 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet31 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean32 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet31, strArray30);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder33 = variantContextBuilder26.filters((java.util.Set<java.lang.String>) strSet31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder26.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder34);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext36 = variantContextBuilder34.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder37 = variantContextBuilder20.genotypesNoValidation(genotypesContext36);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList13 and genotypesContext36.", alleleList13.equals(genotypesContext36) == genotypesContext36.equals(alleleList13));
    }

    @Test
    public void test18() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test18");
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
        java.util.Collection<htsjdk.variant.variantcontext.Allele> alleleCollection26 = null;
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder27 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", 0L, (long) '4', alleleCollection26);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder29 = variantContextBuilder27.log10PError((double) (short) 100);
        java.lang.String[] strArray31 = new java.lang.String[] { "" };
        java.util.LinkedHashSet<java.lang.String> strSet32 = new java.util.LinkedHashSet<java.lang.String>();
        boolean boolean33 = java.util.Collections.addAll((java.util.Collection<java.lang.String>) strSet32, strArray31);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder34 = variantContextBuilder27.filters((java.util.Set<java.lang.String>) strSet32);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder35 = variantContextBuilder27.noID();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder36 = new htsjdk.variant.variantcontext.VariantContextBuilder(variantContextBuilder35);
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext37 = variantContextBuilder35.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder38 = variantContextBuilder21.genotypesNoValidation(genotypesContext37);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList17 and genotypesContext37.", alleleList17.equals(genotypesContext37) == genotypesContext37.equals(alleleList17));
    }

    @Test
    public void test19() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test19");
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
        htsjdk.variant.variantcontext.Allele[] alleleArray47 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList48 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean49 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48, alleleArray47);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder50 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder51 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder52 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList48);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder54 = variantContextBuilder52.start(1L);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder56 = variantContextBuilder54.id("");
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext57 = variantContextBuilder56.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder58 = variantContextBuilder34.genotypes(genotypesContext57);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on genotypeList30 and genotypesContext57.", genotypeList30.equals(genotypesContext57) == genotypesContext57.equals(genotypeList30));
    }

    @Test
    public void test20() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "ErrorTest0.test20");
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
        htsjdk.variant.variantcontext.Allele[] alleleArray64 = new htsjdk.variant.variantcontext.Allele[] {};
        java.util.ArrayList<htsjdk.variant.variantcontext.Allele> alleleList65 = new java.util.ArrayList<htsjdk.variant.variantcontext.Allele>();
        boolean boolean66 = java.util.Collections.addAll((java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList65, alleleArray64);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder67 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) 0, (long) '#', (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList65);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder68 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "hi!", (long) 100, (long) (short) 0, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList65);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder69 = new htsjdk.variant.variantcontext.VariantContextBuilder("", "", (long) (short) 10, 0L, (java.util.Collection<htsjdk.variant.variantcontext.Allele>) alleleList65);
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder71 = variantContextBuilder69.id("");
        long long72 = variantContextBuilder69.getStart();
        htsjdk.variant.variantcontext.GenotypesContext genotypesContext73 = variantContextBuilder69.getGenotypes();
        htsjdk.variant.variantcontext.VariantContextBuilder variantContextBuilder74 = variantContextBuilder51.genotypes(genotypesContext73);
        // This assertion (symmetry of equals) fails
        org.junit.Assert.assertTrue("Contract failed: equals-symmetric on alleleList13 and genotypesContext73.", alleleList13.equals(genotypesContext73) == genotypesContext73.equals(alleleList13));
    }
}

