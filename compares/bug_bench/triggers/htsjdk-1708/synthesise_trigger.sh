#!/usr/bin/env bash
# Synthesise the CRAM trigger for htsjdk-1708 using samtools.
# Requires: samtools >= 1.17 (from htslib), a reference FASTA.
#
# Produces: trigger.cram (3 containers × ~10k reads, all at pos 1).

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ref="${1:-${here}/ref.fa}"
out="${2:-${here}/trigger.cram}"

if [[ ! -s "$ref" ]]; then
    echo "Need a reference FASTA at $ref or pass one as the first argument." >&2
    exit 1
fi

sam_tmp="$(mktemp --suffix=.sam)"
samtools faidx "$ref"

# Header: one SQ for the reference.
printf '@HD\tVN:1.6\tSO:coordinate\n' > "$sam_tmp"
samtools view -H "$ref" >> "$sam_tmp" 2>/dev/null || \
    printf '@SQ\tSN:%s\tLN:%s\n' \
        "$(head -1 "${ref}.fai" | cut -f1)" \
        "$(head -1 "${ref}.fai" | cut -f2)" >> "$sam_tmp"

ref_name="$(head -1 "${ref}.fai" | cut -f1)"
seq="$(head -2 "$ref" | tail -1 | cut -c1-50)"
qual="$(printf 'I%.0s' $(seq 1 50))"

# Replicate one record 25k times, all at position 1. ~10k reads per
# container means three containers worth of data.
for i in $(seq 1 25000); do
    printf 'r%d\t0\t%s\t1\t60\t50M\t*\t0\t0\t%s\t%s\n' \
        "$i" "$ref_name" "$seq" "$qual" >> "$sam_tmp"
done

samtools view -T "$ref" -C -o "$out" "$sam_tmp"
rm -f "$sam_tmp"
echo "[trigger] wrote $out ($(stat -c %s "$out") bytes)"
