
from inspect import signature as _mutmut_signature

def _mutmut_trampoline(orig, mutants, *args, **kwargs):
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from __main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from __main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        return orig(*args, **kwargs)
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        return orig(*args, **kwargs)
    mutant_name = mutant_under_test.rpartition('.')[-1]
    return mutants[mutant_name](*args, **kwargs)


# -*- coding: utf-8 -*-

from vcfpy.exceptions import (
    HeaderNotFound,
    IncorrectVCFFormat,
    InvalidHeaderException,
    InvalidRecordException,
    VCFPyException,
)
from vcfpy.header import (
    AltAlleleHeaderLine,
    CompoundHeaderLine,
    ContigHeaderLine,
    FieldInfo,
    FilterHeaderLine,
    FormatHeaderLine,
    Header,
    HeaderLine,
    InfoHeaderLine,
    MetaHeaderLine,
    PedigreeHeaderLine,
    SampleHeaderLine,
    SamplesInfos,
    SimpleHeaderLine,
    header_without_lines,
)
from vcfpy.reader import Reader
from vcfpy.record import (
    BND,
    DEL,
    FIVE_PRIME,
    FORWARD,
    HET,
    HOM_ALT,
    HOM_REF,
    INDEL,
    INS,
    MIXED,
    MNV,
    REVERSE,
    SNV,
    SV,
    SYMBOLIC,
    THREE_PRIME,
    AltRecord,
    BreakEnd,
    Call,
    Record,
    SingleBreakEnd,
    Substitution,
    SymbolicAllele,
    UnparsedCall,
)
from vcfpy.version import __version__
from vcfpy.writer import Writer

__all__ = [
    "VCFPyException",
    "IncorrectVCFFormat",
    "InvalidHeaderException",
    "InvalidRecordException",
    "HeaderNotFound",
    "Header",
    "MetaHeaderLine",
    "SimpleHeaderLine",
    "CompoundHeaderLine",
    "InfoHeaderLine",
    "FilterHeaderLine",
    "FormatHeaderLine",
    "ContigHeaderLine",
    "AltAlleleHeaderLine",
    "PedigreeHeaderLine",
    "SampleHeaderLine",
    "FieldInfo",
    "SamplesInfos",
    "header_without_lines",
    "Reader",
    "HeaderLine",
    "Writer",
    "Record",
    "Call",
    "UnparsedCall",
    "AltRecord",
    "Substitution",
    "SymbolicAllele",
    "BreakEnd",
    "SingleBreakEnd",
    "HOM_REF",
    "HET",
    "HOM_ALT",
    "SNV",
    "MNV",
    "INDEL",
    "INS",
    "DEL",
    "SV",
    "BND",
    "SYMBOLIC",
    "MIXED",
    "FORWARD",
    "REVERSE",
    "FIVE_PRIME",
    "THREE_PRIME",
    "__version__",
]
