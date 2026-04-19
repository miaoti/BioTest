/*
 * biotest_harness.c — TEMPLATE skeleton for a C-language SUT.
 *
 * Fill in the FILL_IN sections with calls into your SUT's library.
 * The framework calls this binary via:
 *   ./biotest_harness VCF /path/to/file.vcf
 *      → emits canonical JSON on stdout.
 *   ./biotest_harness --mode discover_methods VCF
 *      → emits {"methods": [...]} from a precomputed manifest.
 *   ./biotest_harness --mode query VCF /path/to/file.vcf \
 *                     --methods name1,name2,name3
 *      → emits {"method_results": {...}}.
 *
 * Reference: Chen-Kuo-Liu-Tse 2018 §3.2; MR-Scout TOSEM 2024.
 *
 * SETUP:
 *   1. Replace `Record`, `parse_input`, `free_record` with your SUT's
 *      parsed-record type and lifecycle functions.
 *   2. Implement `dispatch_method(name, rec)` — switch on `name` and
 *      call into your SUT's library, returning a stack-allocated string
 *      ready to print as JSON.
 *   3. Generate the methods manifest once: see harnesses/c/README.md
 *      step 1, output goes into the embedded JSON below or beside the
 *      binary at runtime.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* FILL_IN: include your SUT's public header */
/* #include "my_sut/parser.h" */

/* FILL_IN: type alias for the parsed-record struct */
typedef struct Record Record;

/* FILL_IN: open `path`, parse, return pointer to first record (or NULL on error) */
static Record *parse_input(const char *path) {
    (void)path;
    return NULL;
}

/* FILL_IN: free what parse_input allocated */
static void free_record(Record *r) {
    (void)r;
}

/* FILL_IN: dispatch — return a malloc'd JSON-ready value string for `name`.
 * Caller frees. Use jsonify_bool/_int/_str helpers below. */
static char *dispatch_method(const char *name, Record *r);

/* ---------------------------------------------------------------- *
 * Tiny JSON helpers — keep dependencies zero so this compiles
 * standalone with `gcc biotest_harness.c -o biotest_harness`.
 * ---------------------------------------------------------------- */

static char *jsonify_bool(int v) {
    return v ? strdup("true") : strdup("false");
}

static char *jsonify_int(long long v) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%lld", v);
    return strdup(buf);
}

static char *jsonify_str(const char *s) {
    if (s == NULL) return strdup("null");
    /* WARNING: minimal escaping — extend for production use */
    size_t n = strlen(s);
    char *out = malloc(n + 16);
    snprintf(out, n + 16, "\"%s\"", s);
    return out;
}

static char *jsonify_error(const char *msg) {
    char *e = malloc(strlen(msg) + 32);
    snprintf(e, strlen(msg) + 32, "{\"__error__\":\"%s\"}", msg);
    return e;
}

/* ---------------------------------------------------------------- *
 * Mode dispatch. Two CLI shapes:
 *   biotest_harness VCF <path>                → parse mode
 *   biotest_harness --mode <name> ...         → query / discover modes
 * ---------------------------------------------------------------- */

static int run_parse(const char *fmt, const char *path) {
    Record *r = parse_input(path);
    if (r == NULL) {
        fprintf(stderr, "parse failed for %s\n", path);
        return 1;
    }
    /* FILL_IN: emit your canonical JSON for `r`.
     * Match the schema in test_engine/canonical/schema.py
     * (CanonicalVcf or CanonicalSam, depending on `fmt`). */
    (void)fmt;
    printf("{}\n");
    free_record(r);
    return 0;
}

static int run_discover(const char *fmt) {
    /* The methods manifest is precomputed (see harnesses/c/README.md
     * step 1). For simplicity, embed it directly here OR read from a
     * sibling manifest.json file at runtime. */
    (void)fmt;
    printf("{\"methods\":[]}\n");  /* FILL_IN: emit your manifest */
    return 0;
}

static int run_query(const char *fmt, const char *path, const char *methods_csv) {
    (void)fmt;
    Record *r = parse_input(path);
    printf("{\"method_results\":{");
    int first = 1;
    char *copy = strdup(methods_csv);
    char *tok = strtok(copy, ",");
    while (tok) {
        if (!first) printf(",");
        first = 0;
        printf("\"%s\":", tok);
        char *val = (r == NULL)
            ? jsonify_error("parse_failed")
            : dispatch_method(tok, r);
        printf("%s", val ? val : "null");
        free(val);
        tok = strtok(NULL, ",");
    }
    free(copy);
    printf("}}\n");
    if (r != NULL) free_record(r);
    return 0;
}

int main(int argc, char **argv) {
    /* Minimal arg-parser for the three CLI shapes. */
    if (argc < 2) {
        fprintf(stderr,
            "Usage:\n"
            "  %s <VCF|SAM> <path>                          # parse\n"
            "  %s --mode discover_methods <VCF|SAM>         # discover\n"
            "  %s --mode query <VCF|SAM> <path> --methods n1,n2  # query\n",
            argv[0], argv[0], argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "--mode") == 0 && argc >= 3) {
        const char *mode = argv[2];
        if (strcmp(mode, "discover_methods") == 0 && argc >= 4) {
            return run_discover(argv[3]);
        }
        if (strcmp(mode, "query") == 0 && argc >= 7
                && strcmp(argv[5], "--methods") == 0) {
            return run_query(argv[3], argv[4], argv[6]);
        }
        fprintf(stderr, "Bad --mode invocation\n");
        return 1;
    }
    /* Default: parse mode */
    if (argc < 3) {
        fprintf(stderr, "parse mode requires <VCF|SAM> <path>\n");
        return 1;
    }
    return run_parse(argv[1], argv[2]);
}

/* FILL_IN: dispatch table */
static char *dispatch_method(const char *name, Record *r) {
    /* Example skeleton — uncomment + replace with real SUT calls:
     *
     *   if (strcmp(name, "is_structural") == 0) {
     *       return jsonify_bool(rec_is_structural(r));
     *   }
     *   if (strcmp(name, "n_alleles") == 0) {
     *       return jsonify_int(rec_n_alleles(r));
     *   }
     *   if (strcmp(name, "chrom") == 0) {
     *       return jsonify_str(rec_chrom(r));
     *   }
     */
    (void)r;
    return jsonify_error("unknown method");
}
