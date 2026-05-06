
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
"""Code for representing a VCF record

The VCF record structure is modeled after the one of PyVCF
"""

import re
import warnings
from typing import Any, Iterator, Literal, Sequence

from vcfpy.exceptions import CannotModifyUnparsedCallWarning

#: Code for single nucleotide variant allele
SNV = "SNV"
#: Code for a multi nucleotide variant allele
MNV = "MNV"
#: Code for "clean" deletion allele
DEL = "DEL"
#: Code for "clean" insertion allele
INS = "INS"
#: Code for indel allele, includes substitutions of unequal length
INDEL = "INDEL"
#: Code for structural variant allele
SV = "SV"
#: Code for break-end allele
BND = "BND"
#: Code for symbolic allele that is neither SV nor BND
SYMBOLIC = "SYMBOLIC"

#: Code for mixed variant type
MIXED = "MIXED"

#: Code for homozygous reference
HOM_REF = 0
#: Code for heterozygous
HET = 1
#: Code for homozygous alternative
HOM_ALT = 2

#: Characters reserved in VCF, have to be escaped in INFO fields
RESERVED_CHARS: dict[Literal["INFO", "FORMAT"], str] = {"INFO": ";=%,\r\n\t", "FORMAT": ":=%,\r\n\t"}
#: Mapping for escaping reserved characters
ESCAPE_MAPPING = [
    ("%", "%25"),
    (":", "%3A"),
    (";", "%3B"),
    ("=", "%3D"),
    (",", "%2C"),
    ("\r", "%0D"),
    ("\n", "%0A"),
    ("\t", "%09"),
]
#: Mapping from escaped characters to reserved one
UNESCAPE_MAPPING = [(v, k) for k, v in ESCAPE_MAPPING]


class Record:
    """Represent one record from the VCF file

    Record objects are iterators of their calls
    """

    def xǁRecordǁ__init____mutmut_orig(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_1(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(None) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_2(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) == bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_3(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(None):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_4(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("XXEither provide both FORMAT and calls or none.XX")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_5(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = None
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_6(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = None
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_7(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS + 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_8(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 2
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_9(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = None
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_10(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = ""  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_11(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(None)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_12(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = None
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_13(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = None
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_14(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(None)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_15(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = None
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_16(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = None
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_17(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = None
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_18(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = None
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_19(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT and []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_20(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = None
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_21(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls and []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_22(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = None
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = {}
        self.update_calls(self.calls)

    def xǁRecordǁ__init____mutmut_23(
        self,
        CHROM: str,
        POS: int,
        ID: list[str],
        REF: str,
        ALT: list["AltRecord"],
        QUAL: float | None,
        FILTER: list[str],
        INFO: dict[str, Any],
        FORMAT: list[str] | None = None,
        calls: Sequence["Call | UnparsedCall"] | None = None,
    ):
        if bool(FORMAT) != bool(calls):
            raise ValueError("Either provide both FORMAT and calls or none.")
        #: A ``str`` with the chromosome name
        self.CHROM = CHROM
        #: An ``int`` with a 1-based begin position
        self.POS = POS
        #: An ``int`` with a 0-based begin position
        self.begin = POS - 1
        #: An ``int`` with a 0-based end position
        self.end = None  # XXX
        #: A list of the semicolon-separated values of the ID column
        self.ID = list(ID)
        #: A ``str`` with the REF value
        self.REF = REF
        #: A list of alternative allele records of type :py:class:`AltRecord`
        self.ALT: list["AltRecord"] = list(ALT)
        #: The quality value, can be ``None``
        self.QUAL = QUAL
        #: A list of strings for the FILTER column
        self.FILTER = FILTER
        #: An OrderedDict giving the values of the INFO column, flags are
        #: mapped to ``True``
        self.INFO = INFO
        #: A list of strings for the FORMAT column.  Optional, must be given if
        #: and only if ``calls`` is also given.
        self.FORMAT = FORMAT or []
        #: A list of genotype :py:class:`Call` objects.  Optional, must be given if
        #: and only if ``FORMAT`` is also given.
        self.calls = calls or []
        #: A mapping from sample name to entry in self.calls.
        self.call_for_sample = None
        self.update_calls(self.calls)

    xǁRecordǁ__init____mutmut_mutants = {
    'xǁRecordǁ__init____mutmut_1': xǁRecordǁ__init____mutmut_1, 
        'xǁRecordǁ__init____mutmut_2': xǁRecordǁ__init____mutmut_2, 
        'xǁRecordǁ__init____mutmut_3': xǁRecordǁ__init____mutmut_3, 
        'xǁRecordǁ__init____mutmut_4': xǁRecordǁ__init____mutmut_4, 
        'xǁRecordǁ__init____mutmut_5': xǁRecordǁ__init____mutmut_5, 
        'xǁRecordǁ__init____mutmut_6': xǁRecordǁ__init____mutmut_6, 
        'xǁRecordǁ__init____mutmut_7': xǁRecordǁ__init____mutmut_7, 
        'xǁRecordǁ__init____mutmut_8': xǁRecordǁ__init____mutmut_8, 
        'xǁRecordǁ__init____mutmut_9': xǁRecordǁ__init____mutmut_9, 
        'xǁRecordǁ__init____mutmut_10': xǁRecordǁ__init____mutmut_10, 
        'xǁRecordǁ__init____mutmut_11': xǁRecordǁ__init____mutmut_11, 
        'xǁRecordǁ__init____mutmut_12': xǁRecordǁ__init____mutmut_12, 
        'xǁRecordǁ__init____mutmut_13': xǁRecordǁ__init____mutmut_13, 
        'xǁRecordǁ__init____mutmut_14': xǁRecordǁ__init____mutmut_14, 
        'xǁRecordǁ__init____mutmut_15': xǁRecordǁ__init____mutmut_15, 
        'xǁRecordǁ__init____mutmut_16': xǁRecordǁ__init____mutmut_16, 
        'xǁRecordǁ__init____mutmut_17': xǁRecordǁ__init____mutmut_17, 
        'xǁRecordǁ__init____mutmut_18': xǁRecordǁ__init____mutmut_18, 
        'xǁRecordǁ__init____mutmut_19': xǁRecordǁ__init____mutmut_19, 
        'xǁRecordǁ__init____mutmut_20': xǁRecordǁ__init____mutmut_20, 
        'xǁRecordǁ__init____mutmut_21': xǁRecordǁ__init____mutmut_21, 
        'xǁRecordǁ__init____mutmut_22': xǁRecordǁ__init____mutmut_22, 
        'xǁRecordǁ__init____mutmut_23': xǁRecordǁ__init____mutmut_23
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁRecordǁ__init____mutmut_orig)
    xǁRecordǁ__init____mutmut_orig.__name__ = 'xǁRecordǁ__init__'



    def xǁRecordǁupdate_calls__mutmut_orig(self, calls: Sequence["Call | UnparsedCall"]):
        """Update ``self.calls`` and other fields as necessary."""
        for call in calls:
            call.site = self
        self.call_for_sample = {call.sample: call for call in calls}

    def xǁRecordǁupdate_calls__mutmut_1(self, calls: Sequence["Call | UnparsedCall"]):
        """Update ``self.calls`` and other fields as necessary."""
        for call in calls:
            call.site = None
        self.call_for_sample = {call.sample: call for call in calls}

    def xǁRecordǁupdate_calls__mutmut_2(self, calls: Sequence["Call | UnparsedCall"]):
        """Update ``self.calls`` and other fields as necessary."""
        for call in calls:
            call.site = self
        self.call_for_sample = None

    xǁRecordǁupdate_calls__mutmut_mutants = {
    'xǁRecordǁupdate_calls__mutmut_1': xǁRecordǁupdate_calls__mutmut_1, 
        'xǁRecordǁupdate_calls__mutmut_2': xǁRecordǁupdate_calls__mutmut_2
    }

    def update_calls(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁupdate_calls__mutmut_orig"), object.__getattribute__(self, "xǁRecordǁupdate_calls__mutmut_mutants"), *args, **kwargs) 

    update_calls.__signature__ = _mutmut_signature(xǁRecordǁupdate_calls__mutmut_orig)
    xǁRecordǁupdate_calls__mutmut_orig.__name__ = 'xǁRecordǁupdate_calls'



    def xǁRecordǁis_snv__mutmut_orig(self):
        """Return ``True`` if it is a SNV"""
        return len(self.REF) == 1 and all(a.type == "SNV" for a in self.ALT)

    def xǁRecordǁis_snv__mutmut_1(self):
        """Return ``True`` if it is a SNV"""
        return len(self.REF) != 1 and all(a.type == "SNV" for a in self.ALT)

    def xǁRecordǁis_snv__mutmut_2(self):
        """Return ``True`` if it is a SNV"""
        return len(self.REF) == 2 and all(a.type == "SNV" for a in self.ALT)

    def xǁRecordǁis_snv__mutmut_3(self):
        """Return ``True`` if it is a SNV"""
        return len(self.REF) == 1 and all(a.type != "SNV" for a in self.ALT)

    def xǁRecordǁis_snv__mutmut_4(self):
        """Return ``True`` if it is a SNV"""
        return len(self.REF) == 1 and all(a.type == "XXSNVXX" for a in self.ALT)

    def xǁRecordǁis_snv__mutmut_5(self):
        """Return ``True`` if it is a SNV"""
        return len(self.REF) == 1 or all(a.type == "SNV" for a in self.ALT)

    xǁRecordǁis_snv__mutmut_mutants = {
    'xǁRecordǁis_snv__mutmut_1': xǁRecordǁis_snv__mutmut_1, 
        'xǁRecordǁis_snv__mutmut_2': xǁRecordǁis_snv__mutmut_2, 
        'xǁRecordǁis_snv__mutmut_3': xǁRecordǁis_snv__mutmut_3, 
        'xǁRecordǁis_snv__mutmut_4': xǁRecordǁis_snv__mutmut_4, 
        'xǁRecordǁis_snv__mutmut_5': xǁRecordǁis_snv__mutmut_5
    }

    def is_snv(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁis_snv__mutmut_orig"), object.__getattribute__(self, "xǁRecordǁis_snv__mutmut_mutants"), *args, **kwargs) 

    is_snv.__signature__ = _mutmut_signature(xǁRecordǁis_snv__mutmut_orig)
    xǁRecordǁis_snv__mutmut_orig.__name__ = 'xǁRecordǁis_snv'



    @property
    def affected_start(self):
        """Return affected start position in 0-based coordinates

        For SNVs, MNVs, and deletions, the behaviour is the start position.
        In the case of insertions, the position behind the insert position is
        returned, yielding a 0-length interval together with
        :py:meth:`~Record.affected_end`
        """
        types = {alt.type for alt in self.ALT}  # set!
        BAD_MIX = {INS, SV, BND, SYMBOLIC}  # don't mix well with others
        if (BAD_MIX & types) and len(types) == 1 and list(types)[0] == INS:
            # Only insertions, return 0-based position right of first base
            return self.POS  # right of first base
        else:  # Return 0-based start position of first REF base
            return self.POS - 1  # left of first base

    @property
    def affected_end(self):
        """Return affected start position in 0-based coordinates

        For SNVs, MNVs, and deletions, the behaviour is based on the start
        position and the length of the REF.  In the case of insertions, the
        position behind the insert position is returned, yielding a 0-length
        interval together with :py:meth:`~Record.affected_start`
        """
        types = {alt.type for alt in self.ALT}  # set!
        BAD_MIX = {INS, SV, BND, SYMBOLIC}  # don't mix well with others
        if (BAD_MIX & types) and len(types) == 1 and list(types)[0] == INS:
            # Only insertions, return 0-based position right of first base
            return self.POS  # right of first base
        else:  # Return 0-based end position, behind last REF base
            return (self.POS - 1) + len(self.REF)

    def xǁRecordǁadd_filter__mutmut_orig(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "PASS" in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f != "PASS"]
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_1(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label  in self.FILTER:
            if "PASS" in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f != "PASS"]
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_2(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "XXPASSXX" in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f != "PASS"]
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_3(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "PASS" not in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f != "PASS"]
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_4(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "PASS" in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f == "PASS"]
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_5(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "PASS" in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f != "XXPASSXX"]
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_6(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "PASS" in self.FILTER:
                self.FILTER = None
            self.FILTER.append(label)

    def xǁRecordǁadd_filter__mutmut_7(self, label: str):
        """Add label to FILTER if not set yet, removing ``PASS`` entry if
        present
        """
        if label not in self.FILTER:
            if "PASS" in self.FILTER:
                self.FILTER = [f for f in self.FILTER if f != "PASS"]
            self.FILTER.append(None)

    xǁRecordǁadd_filter__mutmut_mutants = {
    'xǁRecordǁadd_filter__mutmut_1': xǁRecordǁadd_filter__mutmut_1, 
        'xǁRecordǁadd_filter__mutmut_2': xǁRecordǁadd_filter__mutmut_2, 
        'xǁRecordǁadd_filter__mutmut_3': xǁRecordǁadd_filter__mutmut_3, 
        'xǁRecordǁadd_filter__mutmut_4': xǁRecordǁadd_filter__mutmut_4, 
        'xǁRecordǁadd_filter__mutmut_5': xǁRecordǁadd_filter__mutmut_5, 
        'xǁRecordǁadd_filter__mutmut_6': xǁRecordǁadd_filter__mutmut_6, 
        'xǁRecordǁadd_filter__mutmut_7': xǁRecordǁadd_filter__mutmut_7
    }

    def add_filter(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁadd_filter__mutmut_orig"), object.__getattribute__(self, "xǁRecordǁadd_filter__mutmut_mutants"), *args, **kwargs) 

    add_filter.__signature__ = _mutmut_signature(xǁRecordǁadd_filter__mutmut_orig)
    xǁRecordǁadd_filter__mutmut_orig.__name__ = 'xǁRecordǁadd_filter'



    def xǁRecordǁadd_format__mutmut_orig(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_1(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key not in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_2(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(None)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_3(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is  None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_4(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("XXUnparsedCall encountered, skippingXX", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_5(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", None)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_6(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping",)
                else:
                    call.data.setdefault(key, value)

    def xǁRecordǁadd_format__mutmut_7(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(None, value)

    def xǁRecordǁadd_format__mutmut_8(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key, None)

    def xǁRecordǁadd_format__mutmut_9(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault( value)

    def xǁRecordǁadd_format__mutmut_10(self, key: str, value: Any | None = None):
        """Add an entry to format

        The record's calls ``data[key]`` will be set to ``value`` if not yet
        set and value is not ``None``.  If key is already in FORMAT then
        nothing is done.
        """
        if key in self.FORMAT:
            return
        self.FORMAT.append(key)
        if value is not None:
            for call in self:
                if isinstance(call, UnparsedCall):
                    warnings.warn("UnparsedCall encountered, skipping", CannotModifyUnparsedCallWarning)
                else:
                    call.data.setdefault(key,)

    xǁRecordǁadd_format__mutmut_mutants = {
    'xǁRecordǁadd_format__mutmut_1': xǁRecordǁadd_format__mutmut_1, 
        'xǁRecordǁadd_format__mutmut_2': xǁRecordǁadd_format__mutmut_2, 
        'xǁRecordǁadd_format__mutmut_3': xǁRecordǁadd_format__mutmut_3, 
        'xǁRecordǁadd_format__mutmut_4': xǁRecordǁadd_format__mutmut_4, 
        'xǁRecordǁadd_format__mutmut_5': xǁRecordǁadd_format__mutmut_5, 
        'xǁRecordǁadd_format__mutmut_6': xǁRecordǁadd_format__mutmut_6, 
        'xǁRecordǁadd_format__mutmut_7': xǁRecordǁadd_format__mutmut_7, 
        'xǁRecordǁadd_format__mutmut_8': xǁRecordǁadd_format__mutmut_8, 
        'xǁRecordǁadd_format__mutmut_9': xǁRecordǁadd_format__mutmut_9, 
        'xǁRecordǁadd_format__mutmut_10': xǁRecordǁadd_format__mutmut_10
    }

    def add_format(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁadd_format__mutmut_orig"), object.__getattribute__(self, "xǁRecordǁadd_format__mutmut_mutants"), *args, **kwargs) 

    add_format.__signature__ = _mutmut_signature(xǁRecordǁadd_format__mutmut_orig)
    xǁRecordǁadd_format__mutmut_orig.__name__ = 'xǁRecordǁadd_format'



    def xǁRecordǁ__iter____mutmut_orig(self) -> Iterator["Call | UnparsedCall"]:
        """Return generator yielding from ``self.calls``"""
        yield from self.calls

    xǁRecordǁ__iter____mutmut_mutants = {

    }

    def __iter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__iter____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__iter____mutmut_mutants"), *args, **kwargs) 

    __iter__.__signature__ = _mutmut_signature(xǁRecordǁ__iter____mutmut_orig)
    xǁRecordǁ__iter____mutmut_orig.__name__ = 'xǁRecordǁ__iter__'



    def xǁRecordǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁRecordǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁRecordǁ__eq____mutmut_mutants = {
    'xǁRecordǁ__eq____mutmut_1': xǁRecordǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁRecordǁ__eq____mutmut_orig)
    xǁRecordǁ__eq____mutmut_orig.__name__ = 'xǁRecordǁ__eq__'



    def xǁRecordǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁRecordǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁRecordǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁRecordǁ__ne____mutmut_mutants = {
    'xǁRecordǁ__ne____mutmut_1': xǁRecordǁ__ne____mutmut_1, 
        'xǁRecordǁ__ne____mutmut_2': xǁRecordǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁRecordǁ__ne____mutmut_orig)
    xǁRecordǁ__ne____mutmut_orig.__name__ = 'xǁRecordǁ__ne__'



    def xǁRecordǁ__hash____mutmut_orig(self):
        return hash(tuple(sorted(self.__dict__.items())))

    xǁRecordǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁRecordǁ__hash____mutmut_orig)
    xǁRecordǁ__hash____mutmut_orig.__name__ = 'xǁRecordǁ__hash__'



    def xǁRecordǁ__str____mutmut_orig(self):
        tpl = "Record({})"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁRecordǁ__str____mutmut_1(self):
        tpl = "XXRecord({})XX"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁRecordǁ__str____mutmut_2(self):
        tpl = None
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁRecordǁ__str____mutmut_3(self):
        tpl = "Record({})"
        lst: list[Any] = None
        return tpl.format(", ".join(map(repr, lst)))

    def xǁRecordǁ__str____mutmut_4(self):
        tpl = "Record({})"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format("XX, XX".join(map(repr, lst)))

    def xǁRecordǁ__str____mutmut_5(self):
        tpl = "Record({})"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map(None, lst)))

    def xǁRecordǁ__str____mutmut_6(self):
        tpl = "Record({})"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map(repr, None)))

    def xǁRecordǁ__str____mutmut_7(self):
        tpl = "Record({})"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map( lst)))

    def xǁRecordǁ__str____mutmut_8(self):
        tpl = "Record({})"
        lst: list[Any] = [
            self.CHROM,
            self.POS,
            self.ID,
            self.REF,
            self.ALT,
            self.QUAL,
            self.FILTER,
            self.INFO,
            self.FORMAT,
            self.calls,
        ]
        return tpl.format(", ".join(map(repr,)))

    xǁRecordǁ__str____mutmut_mutants = {
    'xǁRecordǁ__str____mutmut_1': xǁRecordǁ__str____mutmut_1, 
        'xǁRecordǁ__str____mutmut_2': xǁRecordǁ__str____mutmut_2, 
        'xǁRecordǁ__str____mutmut_3': xǁRecordǁ__str____mutmut_3, 
        'xǁRecordǁ__str____mutmut_4': xǁRecordǁ__str____mutmut_4, 
        'xǁRecordǁ__str____mutmut_5': xǁRecordǁ__str____mutmut_5, 
        'xǁRecordǁ__str____mutmut_6': xǁRecordǁ__str____mutmut_6, 
        'xǁRecordǁ__str____mutmut_7': xǁRecordǁ__str____mutmut_7, 
        'xǁRecordǁ__str____mutmut_8': xǁRecordǁ__str____mutmut_8
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁRecordǁ__str____mutmut_orig)
    xǁRecordǁ__str____mutmut_orig.__name__ = 'xǁRecordǁ__str__'



    def xǁRecordǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁRecordǁ__repr____mutmut_1(self):
        return str(None)

    xǁRecordǁ__repr____mutmut_mutants = {
    'xǁRecordǁ__repr____mutmut_1': xǁRecordǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁRecordǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁRecordǁ__repr____mutmut_orig)
    xǁRecordǁ__repr____mutmut_orig.__name__ = 'xǁRecordǁ__repr__'




class UnparsedCall:
    """Placeholder for :py:class:`Call` when parsing only a subset of fields"""

    def xǁUnparsedCallǁ__init____mutmut_orig(self, sample: str, unparsed_data: Any, site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: ``str`` with the unparsed data
        self.unparsed_data = unparsed_data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site

    def xǁUnparsedCallǁ__init____mutmut_1(self, sample: str, unparsed_data: Any, site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = None
        #: ``str`` with the unparsed data
        self.unparsed_data = unparsed_data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site

    def xǁUnparsedCallǁ__init____mutmut_2(self, sample: str, unparsed_data: Any, site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: ``str`` with the unparsed data
        self.unparsed_data = None
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site

    def xǁUnparsedCallǁ__init____mutmut_3(self, sample: str, unparsed_data: Any, site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: ``str`` with the unparsed data
        self.unparsed_data = unparsed_data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = None

    xǁUnparsedCallǁ__init____mutmut_mutants = {
    'xǁUnparsedCallǁ__init____mutmut_1': xǁUnparsedCallǁ__init____mutmut_1, 
        'xǁUnparsedCallǁ__init____mutmut_2': xǁUnparsedCallǁ__init____mutmut_2, 
        'xǁUnparsedCallǁ__init____mutmut_3': xǁUnparsedCallǁ__init____mutmut_3
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁUnparsedCallǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁUnparsedCallǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁUnparsedCallǁ__init____mutmut_orig)
    xǁUnparsedCallǁ__init____mutmut_orig.__name__ = 'xǁUnparsedCallǁ__init__'




#: Regular expression for splitting alleles
ALLELE_DELIM = re.compile(r"[|/]")


class Call:
    """The information for a genotype callable

    By VCF, this should always include the genotype information and
    can contain an arbitrary number of further annotation, e.g., the
    coverage at the variant position.
    """

    def xǁCallǁ__init____mutmut_orig(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_1(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = None
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_2(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = None
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_3(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = None
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_4(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int & None] | None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_5(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] & None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_6(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = ""
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_7(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = None
        #: whether or not the variant is fully called
        self.called = ""
        #: the number of alleles in this sample's call
        self.ploidy = None
        self._genotype_updated()

    def xǁCallǁ__init____mutmut_8(self, sample: str, data: dict[str, Any], site: Record | None = None):
        #: the name of the sample for which the call was made
        self.sample = sample
        #: an OrderedDict with the key/value pair information from the
        #: call's data
        self.data: dict[str, Any] = data
        #: the :py:class:`Record` of this :py:class:`Call`
        self.site = site
        #: the allele numbers (0, 1, ...) in this calls or None for no-call
        self.gt_alleles: list[int | None] | None = None
        #: whether or not the variant is fully called
        self.called = None
        #: the number of alleles in this sample's call
        self.ploidy = ""
        self._genotype_updated()

    xǁCallǁ__init____mutmut_mutants = {
    'xǁCallǁ__init____mutmut_1': xǁCallǁ__init____mutmut_1, 
        'xǁCallǁ__init____mutmut_2': xǁCallǁ__init____mutmut_2, 
        'xǁCallǁ__init____mutmut_3': xǁCallǁ__init____mutmut_3, 
        'xǁCallǁ__init____mutmut_4': xǁCallǁ__init____mutmut_4, 
        'xǁCallǁ__init____mutmut_5': xǁCallǁ__init____mutmut_5, 
        'xǁCallǁ__init____mutmut_6': xǁCallǁ__init____mutmut_6, 
        'xǁCallǁ__init____mutmut_7': xǁCallǁ__init____mutmut_7, 
        'xǁCallǁ__init____mutmut_8': xǁCallǁ__init____mutmut_8
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCallǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁCallǁ__init____mutmut_orig)
    xǁCallǁ__init____mutmut_orig.__name__ = 'xǁCallǁ__init__'



    def xǁCallǁset_genotype__mutmut_orig(self, genotype: str | None):
        """Set ``self.data["GT"]`` to ``genotype`` and properly update related
        properties.
        """
        self.data["GT"] = genotype
        self._genotype_updated()

    def xǁCallǁset_genotype__mutmut_1(self, genotype: str | None):
        """Set ``self.data["GT"]`` to ``genotype`` and properly update related
        properties.
        """
        self.data["XXGTXX"] = genotype
        self._genotype_updated()

    def xǁCallǁset_genotype__mutmut_2(self, genotype: str | None):
        """Set ``self.data["GT"]`` to ``genotype`` and properly update related
        properties.
        """
        self.data[None] = genotype
        self._genotype_updated()

    def xǁCallǁset_genotype__mutmut_3(self, genotype: str | None):
        """Set ``self.data["GT"]`` to ``genotype`` and properly update related
        properties.
        """
        self.data["GT"] = None
        self._genotype_updated()

    xǁCallǁset_genotype__mutmut_mutants = {
    'xǁCallǁset_genotype__mutmut_1': xǁCallǁset_genotype__mutmut_1, 
        'xǁCallǁset_genotype__mutmut_2': xǁCallǁset_genotype__mutmut_2, 
        'xǁCallǁset_genotype__mutmut_3': xǁCallǁset_genotype__mutmut_3
    }

    def set_genotype(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁset_genotype__mutmut_orig"), object.__getattribute__(self, "xǁCallǁset_genotype__mutmut_mutants"), *args, **kwargs) 

    set_genotype.__signature__ = _mutmut_signature(xǁCallǁset_genotype__mutmut_orig)
    xǁCallǁset_genotype__mutmut_orig.__name__ = 'xǁCallǁset_genotype'



    def xǁCallǁ_genotype_updated__mutmut_orig(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_1(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("XXGTXX", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_2(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is not None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_3(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = ""
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_4(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = ""
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_5(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = ""
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_6(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = None
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_7(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["XXGTXX"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_8(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data[None])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_9(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele != ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_10(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == "XX.XX":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_11(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(None))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_12(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is  None for al in self.gt_alleles)
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_13(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = None
            self.ploidy = len(self.gt_alleles)

    def xǁCallǁ_genotype_updated__mutmut_14(self):
        """Update fields related to ``self.data["GT"]``."""
        if self.data.get("GT", None) is None:
            self.gt_alleles = None
            self.called = None
            self.ploidy = None
        else:
            self.gt_alleles = []
            for allele in ALLELE_DELIM.split(str(self.data["GT"])):
                if allele == ".":
                    self.gt_alleles.append(None)
                else:
                    self.gt_alleles.append(int(allele))
            self.called = all(al is not None for al in self.gt_alleles)
            self.ploidy = None

    xǁCallǁ_genotype_updated__mutmut_mutants = {
    'xǁCallǁ_genotype_updated__mutmut_1': xǁCallǁ_genotype_updated__mutmut_1, 
        'xǁCallǁ_genotype_updated__mutmut_2': xǁCallǁ_genotype_updated__mutmut_2, 
        'xǁCallǁ_genotype_updated__mutmut_3': xǁCallǁ_genotype_updated__mutmut_3, 
        'xǁCallǁ_genotype_updated__mutmut_4': xǁCallǁ_genotype_updated__mutmut_4, 
        'xǁCallǁ_genotype_updated__mutmut_5': xǁCallǁ_genotype_updated__mutmut_5, 
        'xǁCallǁ_genotype_updated__mutmut_6': xǁCallǁ_genotype_updated__mutmut_6, 
        'xǁCallǁ_genotype_updated__mutmut_7': xǁCallǁ_genotype_updated__mutmut_7, 
        'xǁCallǁ_genotype_updated__mutmut_8': xǁCallǁ_genotype_updated__mutmut_8, 
        'xǁCallǁ_genotype_updated__mutmut_9': xǁCallǁ_genotype_updated__mutmut_9, 
        'xǁCallǁ_genotype_updated__mutmut_10': xǁCallǁ_genotype_updated__mutmut_10, 
        'xǁCallǁ_genotype_updated__mutmut_11': xǁCallǁ_genotype_updated__mutmut_11, 
        'xǁCallǁ_genotype_updated__mutmut_12': xǁCallǁ_genotype_updated__mutmut_12, 
        'xǁCallǁ_genotype_updated__mutmut_13': xǁCallǁ_genotype_updated__mutmut_13, 
        'xǁCallǁ_genotype_updated__mutmut_14': xǁCallǁ_genotype_updated__mutmut_14
    }

    def _genotype_updated(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ_genotype_updated__mutmut_orig"), object.__getattribute__(self, "xǁCallǁ_genotype_updated__mutmut_mutants"), *args, **kwargs) 

    _genotype_updated.__signature__ = _mutmut_signature(xǁCallǁ_genotype_updated__mutmut_orig)
    xǁCallǁ_genotype_updated__mutmut_orig.__name__ = 'xǁCallǁ_genotype_updated'



    @property
    def is_phased(self):
        """Return boolean indicating whether this call is phased"""
        return "|" in self.data.get("GT", "")

    @property
    def gt_phase_char(self):
        """Return character to use for phasing"""
        return "/" if not self.is_phased else "|"

    @property
    def gt_bases(self) -> tuple[str | None, ...]:
        """Return the actual genotype bases, e.g. if VCF genotype is 0/1,
        could return ('A', 'T')
        """
        result: list[str | None] = []
        for a in self.gt_alleles or []:
            if a is None:
                result.append(None)
            elif a == 0:
                if self.site is None:
                    raise ValueError("Cannot determine bases without site being set")
                result.append(self.site.REF)
            else:
                if self.site is None:  # pragma: no cover
                    raise ValueError("Cannot determine bases without site being set")
                result.append(getattr(self.site.ALT[a - 1], "value", None))
        return tuple(result)

    @property
    def gt_type(self) -> Literal[0, 1, 2] | None:
        """The type of genotype, returns one of ``HOM_REF``, ``HOM_ALT``, and
        ``HET``.
        """
        if not self.called or not self.gt_alleles:
            return None  # not called
        elif all(a == 0 for a in self.gt_alleles):
            return HOM_REF
        elif len(set(self.gt_alleles)) == 1:
            return HOM_ALT
        else:
            return HET

    def xǁCallǁis_filtered__mutmut_orig(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_1(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["XXPASSXX"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_2(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore and ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_3(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = None
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_4(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "XXFTXX" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_5(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT"  in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_6(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or  self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_7(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["XXFTXX"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_8(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data[None]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_9(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data and not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_10(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return True
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_11(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["XXFTXX"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_12(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data[None]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_13(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft not in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_14(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if  require:
                return True
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_15(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return False
            elif ft in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_16(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft not in require:
                return True
        return False

    def xǁCallǁis_filtered__mutmut_17(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return False
        return False

    def xǁCallǁis_filtered__mutmut_18(self, require: list[str] | None = None, ignore: list[str] | None = None):
        """Return ``True`` for filtered calls

        :param iterable ignore: if set, the filters to ignore, make sure to
            include 'PASS', when setting, default is ``['PASS']``
        :param iterable require: if set, the filters to require for returning
            ``True``
        """
        ignore = ignore or ["PASS"]
        if "FT" not in self.data or not self.data["FT"]:
            return False
        for ft in self.data["FT"]:
            if ft in ignore:
                continue  # skip
            if not require:
                return True
            elif ft in require:
                return True
        return True

    xǁCallǁis_filtered__mutmut_mutants = {
    'xǁCallǁis_filtered__mutmut_1': xǁCallǁis_filtered__mutmut_1, 
        'xǁCallǁis_filtered__mutmut_2': xǁCallǁis_filtered__mutmut_2, 
        'xǁCallǁis_filtered__mutmut_3': xǁCallǁis_filtered__mutmut_3, 
        'xǁCallǁis_filtered__mutmut_4': xǁCallǁis_filtered__mutmut_4, 
        'xǁCallǁis_filtered__mutmut_5': xǁCallǁis_filtered__mutmut_5, 
        'xǁCallǁis_filtered__mutmut_6': xǁCallǁis_filtered__mutmut_6, 
        'xǁCallǁis_filtered__mutmut_7': xǁCallǁis_filtered__mutmut_7, 
        'xǁCallǁis_filtered__mutmut_8': xǁCallǁis_filtered__mutmut_8, 
        'xǁCallǁis_filtered__mutmut_9': xǁCallǁis_filtered__mutmut_9, 
        'xǁCallǁis_filtered__mutmut_10': xǁCallǁis_filtered__mutmut_10, 
        'xǁCallǁis_filtered__mutmut_11': xǁCallǁis_filtered__mutmut_11, 
        'xǁCallǁis_filtered__mutmut_12': xǁCallǁis_filtered__mutmut_12, 
        'xǁCallǁis_filtered__mutmut_13': xǁCallǁis_filtered__mutmut_13, 
        'xǁCallǁis_filtered__mutmut_14': xǁCallǁis_filtered__mutmut_14, 
        'xǁCallǁis_filtered__mutmut_15': xǁCallǁis_filtered__mutmut_15, 
        'xǁCallǁis_filtered__mutmut_16': xǁCallǁis_filtered__mutmut_16, 
        'xǁCallǁis_filtered__mutmut_17': xǁCallǁis_filtered__mutmut_17, 
        'xǁCallǁis_filtered__mutmut_18': xǁCallǁis_filtered__mutmut_18
    }

    def is_filtered(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁis_filtered__mutmut_orig"), object.__getattribute__(self, "xǁCallǁis_filtered__mutmut_mutants"), *args, **kwargs) 

    is_filtered.__signature__ = _mutmut_signature(xǁCallǁis_filtered__mutmut_orig)
    xǁCallǁis_filtered__mutmut_orig.__name__ = 'xǁCallǁis_filtered'



    @property
    def is_het(self) -> bool:
        """Return ``True`` for heterozygous calls"""
        return self.gt_type == HET

    @property
    def is_variant(self) -> bool:
        """Return ``True`` for non-hom-ref calls"""
        return bool(self.gt_type)

    def xǁCallǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁCallǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁCallǁ__eq____mutmut_mutants = {
    'xǁCallǁ__eq____mutmut_1': xǁCallǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁCallǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁCallǁ__eq____mutmut_orig)
    xǁCallǁ__eq____mutmut_orig.__name__ = 'xǁCallǁ__eq__'



    def xǁCallǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁCallǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁCallǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁCallǁ__ne____mutmut_mutants = {
    'xǁCallǁ__ne____mutmut_1': xǁCallǁ__ne____mutmut_1, 
        'xǁCallǁ__ne____mutmut_2': xǁCallǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁCallǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁCallǁ__ne____mutmut_orig)
    xǁCallǁ__ne____mutmut_orig.__name__ = 'xǁCallǁ__ne__'



    def xǁCallǁ__hash____mutmut_orig(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    xǁCallǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁCallǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁCallǁ__hash____mutmut_orig)
    xǁCallǁ__hash____mutmut_orig.__name__ = 'xǁCallǁ__hash__'



    def xǁCallǁ__str____mutmut_orig(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁCallǁ__str____mutmut_1(self):
        tpl = "XXCall({})XX"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁCallǁ__str____mutmut_2(self):
        tpl = None
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁCallǁ__str____mutmut_3(self):
        tpl = "Call({})"
        lst: list[str & dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(repr, lst)))

    def xǁCallǁ__str____mutmut_4(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = None
        return tpl.format(", ".join(map(repr, lst)))

    def xǁCallǁ__str____mutmut_5(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format("XX, XX".join(map(repr, lst)))

    def xǁCallǁ__str____mutmut_6(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(None, lst)))

    def xǁCallǁ__str____mutmut_7(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(repr, None)))

    def xǁCallǁ__str____mutmut_8(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map( lst)))

    def xǁCallǁ__str____mutmut_9(self):
        tpl = "Call({})"
        lst: list[str | dict[str, Any]] = [self.sample, self.data]
        return tpl.format(", ".join(map(repr,)))

    xǁCallǁ__str____mutmut_mutants = {
    'xǁCallǁ__str____mutmut_1': xǁCallǁ__str____mutmut_1, 
        'xǁCallǁ__str____mutmut_2': xǁCallǁ__str____mutmut_2, 
        'xǁCallǁ__str____mutmut_3': xǁCallǁ__str____mutmut_3, 
        'xǁCallǁ__str____mutmut_4': xǁCallǁ__str____mutmut_4, 
        'xǁCallǁ__str____mutmut_5': xǁCallǁ__str____mutmut_5, 
        'xǁCallǁ__str____mutmut_6': xǁCallǁ__str____mutmut_6, 
        'xǁCallǁ__str____mutmut_7': xǁCallǁ__str____mutmut_7, 
        'xǁCallǁ__str____mutmut_8': xǁCallǁ__str____mutmut_8, 
        'xǁCallǁ__str____mutmut_9': xǁCallǁ__str____mutmut_9
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁCallǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁCallǁ__str____mutmut_orig)
    xǁCallǁ__str____mutmut_orig.__name__ = 'xǁCallǁ__str__'



    def xǁCallǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁCallǁ__repr____mutmut_1(self):
        return str(None)

    xǁCallǁ__repr____mutmut_mutants = {
    'xǁCallǁ__repr____mutmut_1': xǁCallǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCallǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁCallǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁCallǁ__repr____mutmut_orig)
    xǁCallǁ__repr____mutmut_orig.__name__ = 'xǁCallǁ__repr__'




class AltRecord:
    """An alternative allele Record

    Currently, can be a substitution, an SV placeholder, or breakend
    """

    def xǁAltRecordǁ__init____mutmut_orig(
        self, type_: Literal["SNV", "MNV", "DEL", "INS", "INDEL", "SV", "BND", "SYMBOLIC", "MIXED"] | None = None
    ):
        #: String describing the type of the variant, could be one of
        #: SNV, MNV, could be any of teh types described in the ALT
        #: header lines, such as DUP, DEL, INS, ...
        self.type = type_

    def xǁAltRecordǁ__init____mutmut_1(
        self, type_: Literal["SNV", "MNV", "DEL", "INS", "INDEL", "SV", "BND", "SYMBOLIC", "MIXED"] | None = None
    ):
        #: String describing the type of the variant, could be one of
        #: SNV, MNV, could be any of teh types described in the ALT
        #: header lines, such as DUP, DEL, INS, ...
        self.type = None

    xǁAltRecordǁ__init____mutmut_mutants = {
    'xǁAltRecordǁ__init____mutmut_1': xǁAltRecordǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltRecordǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAltRecordǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁAltRecordǁ__init____mutmut_orig)
    xǁAltRecordǁ__init____mutmut_orig.__name__ = 'xǁAltRecordǁ__init__'



    def xǁAltRecordǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁAltRecordǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁAltRecordǁ__eq____mutmut_mutants = {
    'xǁAltRecordǁ__eq____mutmut_1': xǁAltRecordǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltRecordǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁAltRecordǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁAltRecordǁ__eq____mutmut_orig)
    xǁAltRecordǁ__eq____mutmut_orig.__name__ = 'xǁAltRecordǁ__eq__'



    def xǁAltRecordǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁAltRecordǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁAltRecordǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁAltRecordǁ__ne____mutmut_mutants = {
    'xǁAltRecordǁ__ne____mutmut_1': xǁAltRecordǁ__ne____mutmut_1, 
        'xǁAltRecordǁ__ne____mutmut_2': xǁAltRecordǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltRecordǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁAltRecordǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁAltRecordǁ__ne____mutmut_orig)
    xǁAltRecordǁ__ne____mutmut_orig.__name__ = 'xǁAltRecordǁ__ne__'



    def xǁAltRecordǁ__hash____mutmut_orig(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    xǁAltRecordǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltRecordǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁAltRecordǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁAltRecordǁ__hash____mutmut_orig)
    xǁAltRecordǁ__hash____mutmut_orig.__name__ = 'xǁAltRecordǁ__hash__'



    def xǁAltRecordǁserialize__mutmut_orig(self) -> str:
        """Return ``str`` with representation for VCF file"""
        raise NotImplementedError("Abstract class, implemented in sub class")

    def xǁAltRecordǁserialize__mutmut_1(self) -> str:
        """Return ``str`` with representation for VCF file"""
        raise NotImplementedError("XXAbstract class, implemented in sub classXX")

    xǁAltRecordǁserialize__mutmut_mutants = {
    'xǁAltRecordǁserialize__mutmut_1': xǁAltRecordǁserialize__mutmut_1
    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltRecordǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁAltRecordǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁAltRecordǁserialize__mutmut_orig)
    xǁAltRecordǁserialize__mutmut_orig.__name__ = 'xǁAltRecordǁserialize'




class Substitution(AltRecord):
    """A basic alternative allele record describing a REF->AltRecord
    substitution

    Note that this subsumes MNVs, insertions, and deletions.
    """

    def xǁSubstitutionǁ__init____mutmut_orig(
        self, type_: Literal["SNV", "MNV", "DEL", "INS", "INDEL", "SV", "BND", "SYMBOLIC", "MIXED"], value: str
    ):
        super().__init__(type_)
        #: The alternative base sequence to use in the substitution
        self.value = value

    def xǁSubstitutionǁ__init____mutmut_1(
        self, type_: Literal["SNV", "MNV", "DEL", "INS", "INDEL", "SV", "BND", "SYMBOLIC", "MIXED"], value: str
    ):
        super().__init__(None)
        #: The alternative base sequence to use in the substitution
        self.value = value

    def xǁSubstitutionǁ__init____mutmut_2(
        self, type_: Literal["SNV", "MNV", "DEL", "INS", "INDEL", "SV", "BND", "SYMBOLIC", "MIXED"], value: str
    ):
        super().__init__(type_)
        #: The alternative base sequence to use in the substitution
        self.value = None

    xǁSubstitutionǁ__init____mutmut_mutants = {
    'xǁSubstitutionǁ__init____mutmut_1': xǁSubstitutionǁ__init____mutmut_1, 
        'xǁSubstitutionǁ__init____mutmut_2': xǁSubstitutionǁ__init____mutmut_2
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁSubstitutionǁ__init____mutmut_orig)
    xǁSubstitutionǁ__init____mutmut_orig.__name__ = 'xǁSubstitutionǁ__init__'



    def xǁSubstitutionǁserialize__mutmut_orig(self) -> str:
        return self.value

    xǁSubstitutionǁserialize__mutmut_mutants = {

    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁSubstitutionǁserialize__mutmut_orig)
    xǁSubstitutionǁserialize__mutmut_orig.__name__ = 'xǁSubstitutionǁserialize'



    def xǁSubstitutionǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁSubstitutionǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁSubstitutionǁ__eq____mutmut_mutants = {
    'xǁSubstitutionǁ__eq____mutmut_1': xǁSubstitutionǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁSubstitutionǁ__eq____mutmut_orig)
    xǁSubstitutionǁ__eq____mutmut_orig.__name__ = 'xǁSubstitutionǁ__eq__'



    def xǁSubstitutionǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁSubstitutionǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁSubstitutionǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁSubstitutionǁ__ne____mutmut_mutants = {
    'xǁSubstitutionǁ__ne____mutmut_1': xǁSubstitutionǁ__ne____mutmut_1, 
        'xǁSubstitutionǁ__ne____mutmut_2': xǁSubstitutionǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁSubstitutionǁ__ne____mutmut_orig)
    xǁSubstitutionǁ__ne____mutmut_orig.__name__ = 'xǁSubstitutionǁ__ne__'



    def xǁSubstitutionǁ__hash____mutmut_orig(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    xǁSubstitutionǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁSubstitutionǁ__hash____mutmut_orig)
    xǁSubstitutionǁ__hash____mutmut_orig.__name__ = 'xǁSubstitutionǁ__hash__'



    def xǁSubstitutionǁ__str____mutmut_orig(self) -> str:
        tpl = "Substitution(type_={}, value={})"
        return tpl.format(*map(repr, [self.type, self.value]))

    def xǁSubstitutionǁ__str____mutmut_1(self) -> str:
        tpl = "XXSubstitution(type_={}, value={})XX"
        return tpl.format(*map(repr, [self.type, self.value]))

    def xǁSubstitutionǁ__str____mutmut_2(self) -> str:
        tpl = None
        return tpl.format(*map(repr, [self.type, self.value]))

    def xǁSubstitutionǁ__str____mutmut_3(self) -> str:
        tpl = "Substitution(type_={}, value={})"
        return tpl.format(*map(None, [self.type, self.value]))

    def xǁSubstitutionǁ__str____mutmut_4(self) -> str:
        tpl = "Substitution(type_={}, value={})"
        return tpl.format(*map( [self.type, self.value]))

    xǁSubstitutionǁ__str____mutmut_mutants = {
    'xǁSubstitutionǁ__str____mutmut_1': xǁSubstitutionǁ__str____mutmut_1, 
        'xǁSubstitutionǁ__str____mutmut_2': xǁSubstitutionǁ__str____mutmut_2, 
        'xǁSubstitutionǁ__str____mutmut_3': xǁSubstitutionǁ__str____mutmut_3, 
        'xǁSubstitutionǁ__str____mutmut_4': xǁSubstitutionǁ__str____mutmut_4
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁSubstitutionǁ__str____mutmut_orig)
    xǁSubstitutionǁ__str____mutmut_orig.__name__ = 'xǁSubstitutionǁ__str__'



    def xǁSubstitutionǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁSubstitutionǁ__repr____mutmut_1(self):
        return str(None)

    xǁSubstitutionǁ__repr____mutmut_mutants = {
    'xǁSubstitutionǁ__repr____mutmut_1': xǁSubstitutionǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSubstitutionǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁSubstitutionǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁSubstitutionǁ__repr____mutmut_orig)
    xǁSubstitutionǁ__repr____mutmut_orig.__name__ = 'xǁSubstitutionǁ__repr__'




#: code for five prime orientation :py:class:`BreakEnd`
FIVE_PRIME = "5"
#: code for three prime orientation :py:class:`BreakEnd`
THREE_PRIME = "3"

#: code for forward orientation
FORWARD = "+"
#: code for reverse orientation
REVERSE = "-"


class BreakEnd(AltRecord):
    """A placeholder for a breakend"""

    def xǁBreakEndǁ__init____mutmut_orig(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_1(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("XXBNDXX")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_2(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = None
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_3(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = None
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_4(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = None
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_5(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = None
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_6(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = None
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = within_main_assembly

    def xǁBreakEndǁ__init____mutmut_7(
        self,
        mate_chrom: str | None,
        mate_pos: int | None,
        orientation: str | None,
        mate_orientation: Literal["+", "-"] | None,
        sequence: str,
        within_main_assembly: bool | None,
    ):
        super().__init__("BND")
        #: chromosome of the mate breakend
        self.mate_chrom = mate_chrom
        #: position of the mate breakend
        self.mate_pos = mate_pos
        #: orientation of this breakend
        self.orientation = orientation
        #: orientation breakend's mate
        self.mate_orientation = mate_orientation
        #: breakpoint's connecting sequence
        self.sequence = sequence
        #: ``bool`` specifying if the breakend mate is within the assembly
        #: (``True``) or in an ancillary assembly (``False``)
        self.within_main_assembly = None

    xǁBreakEndǁ__init____mutmut_mutants = {
    'xǁBreakEndǁ__init____mutmut_1': xǁBreakEndǁ__init____mutmut_1, 
        'xǁBreakEndǁ__init____mutmut_2': xǁBreakEndǁ__init____mutmut_2, 
        'xǁBreakEndǁ__init____mutmut_3': xǁBreakEndǁ__init____mutmut_3, 
        'xǁBreakEndǁ__init____mutmut_4': xǁBreakEndǁ__init____mutmut_4, 
        'xǁBreakEndǁ__init____mutmut_5': xǁBreakEndǁ__init____mutmut_5, 
        'xǁBreakEndǁ__init____mutmut_6': xǁBreakEndǁ__init____mutmut_6, 
        'xǁBreakEndǁ__init____mutmut_7': xǁBreakEndǁ__init____mutmut_7
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁBreakEndǁ__init____mutmut_orig)
    xǁBreakEndǁ__init____mutmut_orig.__name__ = 'xǁBreakEndǁ__init__'



    def xǁBreakEndǁserialize__mutmut_orig(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_1(self):
        """Return string representation for VCF"""
        if self.mate_chrom is not None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_2(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "XX.XX"
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_3(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = None
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_4(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = None
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_5(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "XX<{}>XX".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_6(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = None
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_7(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is not None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_8(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("XXmate_orientation must be set if mate_chrom is setXX")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_9(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "XX[{}:{}[XX", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_10(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "XX]{}:{}]XX"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_11(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[None]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_12(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = None
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_13(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(None, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_14(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format( self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_15(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = None
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_16(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation != FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_17(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag - self.sequence
        else:
            return self.sequence + remote_tag

    def xǁBreakEndǁserialize__mutmut_18(self):
        """Return string representation for VCF"""
        if self.mate_chrom is None:
            remote_tag = "."
        else:
            if self.within_main_assembly:
                mate_chrom = self.mate_chrom
            else:
                mate_chrom = "<{}>".format(self.mate_chrom)
            if self.mate_orientation is None:  # pragma: no cover
                raise ValueError("mate_orientation must be set if mate_chrom is set")
            tpl = {FORWARD: "[{}:{}[", REVERSE: "]{}:{}]"}[self.mate_orientation]
            remote_tag = tpl.format(mate_chrom, self.mate_pos)
        if self.orientation == FORWARD:
            return remote_tag + self.sequence
        else:
            return self.sequence - remote_tag

    xǁBreakEndǁserialize__mutmut_mutants = {
    'xǁBreakEndǁserialize__mutmut_1': xǁBreakEndǁserialize__mutmut_1, 
        'xǁBreakEndǁserialize__mutmut_2': xǁBreakEndǁserialize__mutmut_2, 
        'xǁBreakEndǁserialize__mutmut_3': xǁBreakEndǁserialize__mutmut_3, 
        'xǁBreakEndǁserialize__mutmut_4': xǁBreakEndǁserialize__mutmut_4, 
        'xǁBreakEndǁserialize__mutmut_5': xǁBreakEndǁserialize__mutmut_5, 
        'xǁBreakEndǁserialize__mutmut_6': xǁBreakEndǁserialize__mutmut_6, 
        'xǁBreakEndǁserialize__mutmut_7': xǁBreakEndǁserialize__mutmut_7, 
        'xǁBreakEndǁserialize__mutmut_8': xǁBreakEndǁserialize__mutmut_8, 
        'xǁBreakEndǁserialize__mutmut_9': xǁBreakEndǁserialize__mutmut_9, 
        'xǁBreakEndǁserialize__mutmut_10': xǁBreakEndǁserialize__mutmut_10, 
        'xǁBreakEndǁserialize__mutmut_11': xǁBreakEndǁserialize__mutmut_11, 
        'xǁBreakEndǁserialize__mutmut_12': xǁBreakEndǁserialize__mutmut_12, 
        'xǁBreakEndǁserialize__mutmut_13': xǁBreakEndǁserialize__mutmut_13, 
        'xǁBreakEndǁserialize__mutmut_14': xǁBreakEndǁserialize__mutmut_14, 
        'xǁBreakEndǁserialize__mutmut_15': xǁBreakEndǁserialize__mutmut_15, 
        'xǁBreakEndǁserialize__mutmut_16': xǁBreakEndǁserialize__mutmut_16, 
        'xǁBreakEndǁserialize__mutmut_17': xǁBreakEndǁserialize__mutmut_17, 
        'xǁBreakEndǁserialize__mutmut_18': xǁBreakEndǁserialize__mutmut_18
    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁBreakEndǁserialize__mutmut_orig)
    xǁBreakEndǁserialize__mutmut_orig.__name__ = 'xǁBreakEndǁserialize'



    def xǁBreakEndǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁBreakEndǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁBreakEndǁ__eq____mutmut_mutants = {
    'xǁBreakEndǁ__eq____mutmut_1': xǁBreakEndǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁBreakEndǁ__eq____mutmut_orig)
    xǁBreakEndǁ__eq____mutmut_orig.__name__ = 'xǁBreakEndǁ__eq__'



    def xǁBreakEndǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁBreakEndǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁBreakEndǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁBreakEndǁ__ne____mutmut_mutants = {
    'xǁBreakEndǁ__ne____mutmut_1': xǁBreakEndǁ__ne____mutmut_1, 
        'xǁBreakEndǁ__ne____mutmut_2': xǁBreakEndǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁBreakEndǁ__ne____mutmut_orig)
    xǁBreakEndǁ__ne____mutmut_orig.__name__ = 'xǁBreakEndǁ__ne__'



    def xǁBreakEndǁ__hash____mutmut_orig(self):
        return hash(tuple(sorted(self.__dict__.items())))

    xǁBreakEndǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁBreakEndǁ__hash____mutmut_orig)
    xǁBreakEndǁ__hash____mutmut_orig.__name__ = 'xǁBreakEndǁ__hash__'



    def xǁBreakEndǁ__str____mutmut_orig(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map(repr, vals)))

    def xǁBreakEndǁ__str____mutmut_1(self):
        tpl = "XXBreakEnd({})XX"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map(repr, vals)))

    def xǁBreakEndǁ__str____mutmut_2(self):
        tpl = None
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map(repr, vals)))

    def xǁBreakEndǁ__str____mutmut_3(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = None
        return tpl.format(", ".join(map(repr, vals)))

    def xǁBreakEndǁ__str____mutmut_4(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format("XX, XX".join(map(repr, vals)))

    def xǁBreakEndǁ__str____mutmut_5(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map(None, vals)))

    def xǁBreakEndǁ__str____mutmut_6(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map(repr, None)))

    def xǁBreakEndǁ__str____mutmut_7(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map( vals)))

    def xǁBreakEndǁ__str____mutmut_8(self):
        tpl = "BreakEnd({})"
        vals: list[Any] = [
            self.mate_chrom,
            self.mate_pos,
            self.orientation,
            self.mate_orientation,
            self.sequence,
            self.within_main_assembly,
        ]
        return tpl.format(", ".join(map(repr,)))

    xǁBreakEndǁ__str____mutmut_mutants = {
    'xǁBreakEndǁ__str____mutmut_1': xǁBreakEndǁ__str____mutmut_1, 
        'xǁBreakEndǁ__str____mutmut_2': xǁBreakEndǁ__str____mutmut_2, 
        'xǁBreakEndǁ__str____mutmut_3': xǁBreakEndǁ__str____mutmut_3, 
        'xǁBreakEndǁ__str____mutmut_4': xǁBreakEndǁ__str____mutmut_4, 
        'xǁBreakEndǁ__str____mutmut_5': xǁBreakEndǁ__str____mutmut_5, 
        'xǁBreakEndǁ__str____mutmut_6': xǁBreakEndǁ__str____mutmut_6, 
        'xǁBreakEndǁ__str____mutmut_7': xǁBreakEndǁ__str____mutmut_7, 
        'xǁBreakEndǁ__str____mutmut_8': xǁBreakEndǁ__str____mutmut_8
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁBreakEndǁ__str____mutmut_orig)
    xǁBreakEndǁ__str____mutmut_orig.__name__ = 'xǁBreakEndǁ__str__'



    def xǁBreakEndǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁBreakEndǁ__repr____mutmut_1(self):
        return str(None)

    xǁBreakEndǁ__repr____mutmut_mutants = {
    'xǁBreakEndǁ__repr____mutmut_1': xǁBreakEndǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBreakEndǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁBreakEndǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁBreakEndǁ__repr____mutmut_orig)
    xǁBreakEndǁ__repr____mutmut_orig.__name__ = 'xǁBreakEndǁ__repr__'




class SingleBreakEnd(BreakEnd):
    """A placeholder for a single breakend"""

    def xǁSingleBreakEndǁ__init____mutmut_orig(self, orientation: str, sequence: str):
        super().__init__(None, None, orientation, None, sequence, None)

    def xǁSingleBreakEndǁ__init____mutmut_1(self, orientation: str, sequence: str):
        super().__init__(None, None, None, None, sequence, None)

    def xǁSingleBreakEndǁ__init____mutmut_2(self, orientation: str, sequence: str):
        super().__init__(None, None, orientation, None, None, None)

    def xǁSingleBreakEndǁ__init____mutmut_3(self, orientation: str, sequence: str):
        super().__init__(None, None, None, sequence, None)

    def xǁSingleBreakEndǁ__init____mutmut_4(self, orientation: str, sequence: str):
        super().__init__(None, None, orientation, None, None)

    xǁSingleBreakEndǁ__init____mutmut_mutants = {
    'xǁSingleBreakEndǁ__init____mutmut_1': xǁSingleBreakEndǁ__init____mutmut_1, 
        'xǁSingleBreakEndǁ__init____mutmut_2': xǁSingleBreakEndǁ__init____mutmut_2, 
        'xǁSingleBreakEndǁ__init____mutmut_3': xǁSingleBreakEndǁ__init____mutmut_3, 
        'xǁSingleBreakEndǁ__init____mutmut_4': xǁSingleBreakEndǁ__init____mutmut_4
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSingleBreakEndǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSingleBreakEndǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁSingleBreakEndǁ__init____mutmut_orig)
    xǁSingleBreakEndǁ__init____mutmut_orig.__name__ = 'xǁSingleBreakEndǁ__init__'



    def xǁSingleBreakEndǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁSingleBreakEndǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁSingleBreakEndǁ__eq____mutmut_mutants = {
    'xǁSingleBreakEndǁ__eq____mutmut_1': xǁSingleBreakEndǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSingleBreakEndǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁSingleBreakEndǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁSingleBreakEndǁ__eq____mutmut_orig)
    xǁSingleBreakEndǁ__eq____mutmut_orig.__name__ = 'xǁSingleBreakEndǁ__eq__'



    def xǁSingleBreakEndǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁSingleBreakEndǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁSingleBreakEndǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁSingleBreakEndǁ__ne____mutmut_mutants = {
    'xǁSingleBreakEndǁ__ne____mutmut_1': xǁSingleBreakEndǁ__ne____mutmut_1, 
        'xǁSingleBreakEndǁ__ne____mutmut_2': xǁSingleBreakEndǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSingleBreakEndǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁSingleBreakEndǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁSingleBreakEndǁ__ne____mutmut_orig)
    xǁSingleBreakEndǁ__ne____mutmut_orig.__name__ = 'xǁSingleBreakEndǁ__ne__'



    def xǁSingleBreakEndǁ__hash____mutmut_orig(self):
        return hash(tuple(sorted(self.__dict__.items())))

    xǁSingleBreakEndǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSingleBreakEndǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁSingleBreakEndǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁSingleBreakEndǁ__hash____mutmut_orig)
    xǁSingleBreakEndǁ__hash____mutmut_orig.__name__ = 'xǁSingleBreakEndǁ__hash__'



    def xǁSingleBreakEndǁ__str____mutmut_orig(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map(repr, vals)))

    def xǁSingleBreakEndǁ__str____mutmut_1(self):
        tpl = "XXSingleBreakEnd({})XX"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map(repr, vals)))

    def xǁSingleBreakEndǁ__str____mutmut_2(self):
        tpl = None
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map(repr, vals)))

    def xǁSingleBreakEndǁ__str____mutmut_3(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = None
        return tpl.format(", ".join(map(repr, vals)))

    def xǁSingleBreakEndǁ__str____mutmut_4(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format("XX, XX".join(map(repr, vals)))

    def xǁSingleBreakEndǁ__str____mutmut_5(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map(None, vals)))

    def xǁSingleBreakEndǁ__str____mutmut_6(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map(repr, None)))

    def xǁSingleBreakEndǁ__str____mutmut_7(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map( vals)))

    def xǁSingleBreakEndǁ__str____mutmut_8(self):
        tpl = "SingleBreakEnd({})"
        vals: list[Any] = [self.orientation, self.sequence]
        return tpl.format(", ".join(map(repr,)))

    xǁSingleBreakEndǁ__str____mutmut_mutants = {
    'xǁSingleBreakEndǁ__str____mutmut_1': xǁSingleBreakEndǁ__str____mutmut_1, 
        'xǁSingleBreakEndǁ__str____mutmut_2': xǁSingleBreakEndǁ__str____mutmut_2, 
        'xǁSingleBreakEndǁ__str____mutmut_3': xǁSingleBreakEndǁ__str____mutmut_3, 
        'xǁSingleBreakEndǁ__str____mutmut_4': xǁSingleBreakEndǁ__str____mutmut_4, 
        'xǁSingleBreakEndǁ__str____mutmut_5': xǁSingleBreakEndǁ__str____mutmut_5, 
        'xǁSingleBreakEndǁ__str____mutmut_6': xǁSingleBreakEndǁ__str____mutmut_6, 
        'xǁSingleBreakEndǁ__str____mutmut_7': xǁSingleBreakEndǁ__str____mutmut_7, 
        'xǁSingleBreakEndǁ__str____mutmut_8': xǁSingleBreakEndǁ__str____mutmut_8
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSingleBreakEndǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSingleBreakEndǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁSingleBreakEndǁ__str____mutmut_orig)
    xǁSingleBreakEndǁ__str____mutmut_orig.__name__ = 'xǁSingleBreakEndǁ__str__'




class SymbolicAllele(AltRecord):
    """A placeholder for a symbolic allele

    The allele symbol must be defined in the header using an ``ALT`` header
    before being parsed.  Usually, this is used for succinct descriptions of
    structural variants or IUPAC parameters.
    """

    def xǁSymbolicAlleleǁ__init____mutmut_orig(self, value: str):
        super().__init__(SYMBOLIC)
        #: The symbolic value, e.g. 'DUP'
        self.value = value

    def xǁSymbolicAlleleǁ__init____mutmut_1(self, value: str):
        super().__init__(None)
        #: The symbolic value, e.g. 'DUP'
        self.value = value

    def xǁSymbolicAlleleǁ__init____mutmut_2(self, value: str):
        super().__init__(SYMBOLIC)
        #: The symbolic value, e.g. 'DUP'
        self.value = None

    xǁSymbolicAlleleǁ__init____mutmut_mutants = {
    'xǁSymbolicAlleleǁ__init____mutmut_1': xǁSymbolicAlleleǁ__init____mutmut_1, 
        'xǁSymbolicAlleleǁ__init____mutmut_2': xǁSymbolicAlleleǁ__init____mutmut_2
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁ__init____mutmut_orig)
    xǁSymbolicAlleleǁ__init____mutmut_orig.__name__ = 'xǁSymbolicAlleleǁ__init__'



    def xǁSymbolicAlleleǁserialize__mutmut_orig(self):
        return "<{}>".format(self.value)

    def xǁSymbolicAlleleǁserialize__mutmut_1(self):
        return "XX<{}>XX".format(self.value)

    xǁSymbolicAlleleǁserialize__mutmut_mutants = {
    'xǁSymbolicAlleleǁserialize__mutmut_1': xǁSymbolicAlleleǁserialize__mutmut_1
    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁserialize__mutmut_orig)
    xǁSymbolicAlleleǁserialize__mutmut_orig.__name__ = 'xǁSymbolicAlleleǁserialize'



    def xǁSymbolicAlleleǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError  # pragma: no cover

    def xǁSymbolicAlleleǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        raise NotImplementedError  # pragma: no cover

    xǁSymbolicAlleleǁ__eq____mutmut_mutants = {
    'xǁSymbolicAlleleǁ__eq____mutmut_1': xǁSymbolicAlleleǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁ__eq____mutmut_orig)
    xǁSymbolicAlleleǁ__eq____mutmut_orig.__name__ = 'xǁSymbolicAlleleǁ__eq__'



    def xǁSymbolicAlleleǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁSymbolicAlleleǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        raise NotImplementedError  # pragma: no cover

    def xǁSymbolicAlleleǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        raise NotImplementedError  # pragma: no cover

    xǁSymbolicAlleleǁ__ne____mutmut_mutants = {
    'xǁSymbolicAlleleǁ__ne____mutmut_1': xǁSymbolicAlleleǁ__ne____mutmut_1, 
        'xǁSymbolicAlleleǁ__ne____mutmut_2': xǁSymbolicAlleleǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁ__ne____mutmut_orig)
    xǁSymbolicAlleleǁ__ne____mutmut_orig.__name__ = 'xǁSymbolicAlleleǁ__ne__'



    def xǁSymbolicAlleleǁ__hash____mutmut_orig(self):
        return hash(tuple(sorted(self.__dict__.items())))

    xǁSymbolicAlleleǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁ__hash____mutmut_orig)
    xǁSymbolicAlleleǁ__hash____mutmut_orig.__name__ = 'xǁSymbolicAlleleǁ__hash__'



    def xǁSymbolicAlleleǁ__str____mutmut_orig(self):
        return "SymbolicAllele({})".format(repr(self.value))

    def xǁSymbolicAlleleǁ__str____mutmut_1(self):
        return "XXSymbolicAllele({})XX".format(repr(self.value))

    xǁSymbolicAlleleǁ__str____mutmut_mutants = {
    'xǁSymbolicAlleleǁ__str____mutmut_1': xǁSymbolicAlleleǁ__str____mutmut_1
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁ__str____mutmut_orig)
    xǁSymbolicAlleleǁ__str____mutmut_orig.__name__ = 'xǁSymbolicAlleleǁ__str__'



    def xǁSymbolicAlleleǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁSymbolicAlleleǁ__repr____mutmut_1(self):
        return str(None)

    xǁSymbolicAlleleǁ__repr____mutmut_mutants = {
    'xǁSymbolicAlleleǁ__repr____mutmut_1': xǁSymbolicAlleleǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSymbolicAlleleǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁSymbolicAlleleǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁSymbolicAlleleǁ__repr____mutmut_orig)
    xǁSymbolicAlleleǁ__repr____mutmut_orig.__name__ = 'xǁSymbolicAlleleǁ__repr__'


