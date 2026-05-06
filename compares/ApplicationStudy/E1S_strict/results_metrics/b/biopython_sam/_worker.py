
import io, json, os, sys, traceback
from pathlib import Path

try:
    import numpy, Bio.Align  # noqa: F401
    from Bio.Align import sam as _biopython_sam
except Exception as e:  # pragma: no cover — defensive
    print(json.dumps({"_worker_fatal": type(e).__name__ + ": " + str(e)}), flush=True)
    sys.exit(2)


def one(path: str):
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"file": path, "ok": False, "err_type": "read_error",
                "err_msg": str(e)[:200]}
    buf = io.StringIO(text)
    try:
        it = _biopython_sam.AlignmentIterator(buf)
        aln_count = 0
        last_sig = None
        for aln in it:
            aln_count += 1
            tgt = str(getattr(aln, "target", ""))[:50]
            qry = str(getattr(aln, "query", ""))[:50]
            score = getattr(aln, "score", None)
            last_sig = (tgt[:20], qry[:20], str(score)[:20])
        return {
            "file": path, "ok": True, "aln_count": aln_count,
            "last_sig": last_sig, "err_type": None, "err_msg": None,
        }
    except Exception as e:
        return {"file": path, "ok": False,
                "err_type": type(e).__name__,
                "err_msg": str(e)[:200],
                "aln_count": None, "last_sig": None}


def main():
    corpus = sys.argv[1]
    files = sorted(Path(corpus).iterdir())
    for p in files:
        if not p.is_file():
            continue
        try:
            r = one(str(p))
        except BaseException as e:
            r = {"file": str(p), "ok": False, "err_type": "worker_exception",
                 "err_msg": type(e).__name__ + ": " + str(e)[:200]}
        print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
