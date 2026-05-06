
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
"""Code for representing the VCF header part

The VCF header class structure is modeled after HTSJDK
"""

import json
import pprint
import warnings
from typing import Any, Iterable, Literal

from vcfpy import exceptions
from vcfpy.exceptions import (
    DuplicateHeaderLineWarning,
    FieldInfoNotFound,
    FieldInvalidNumber,
    FieldMissingNumber,
    HeaderInvalidType,
    HeaderMissingDescription,
)

__author__ = "Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>"

# Tuples of valid entries -----------------------------------------------------
#
#: valid INFO value types
INFO_TYPES = ("Integer", "Float", "Flag", "Character", "String")
#: valid FORMAT value types
FORMAT_TYPES = ("Integer", "Float", "Character", "String")
#: valid values for "Number" entries, except for integers
VALID_NUMBERS = ("A", "R", "G", ".")
#: header lines that contain an "ID" entry
LINES_WITH_ID = ("ALT", "contig", "FILTER", "FORMAT", "INFO", "META", "PEDIGREE", "SAMPLE")

# Constants for "Number" entries ----------------------------------------------
#
#: number of alleles excluding reference
HEADER_NUMBER_ALLELES = "A"
#: number of alleles including reference
HEADER_NUMBER_REF = "R"
#: number of genotypes
HEADER_NUMBER_GENOTYPES = "G"
#: unbounded number of values
HEADER_NUMBER_UNBOUNDED = "."


class FieldInfo:
    """Core information for describing field type and number"""

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_orig(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int | str = number
        #: Description for the header field, optional
        self.description: str | None = description
        #: The id of the field, optional.
        self.id: str | None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_1(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = None
        #: Number description, either an int or constant
        self.number: int | str = number
        #: Description for the header field, optional
        self.description: str | None = description
        #: The id of the field, optional.
        self.id: str | None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_2(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int & str = number
        #: Description for the header field, optional
        self.description: str | None = description
        #: The id of the field, optional.
        self.id: str | None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_3(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int | str = None
        #: Description for the header field, optional
        self.description: str | None = description
        #: The id of the field, optional.
        self.id: str | None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_4(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int | str = number
        #: Description for the header field, optional
        self.description: str & None = description
        #: The id of the field, optional.
        self.id: str | None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_5(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int | str = number
        #: Description for the header field, optional
        self.description: str | None = None
        #: The id of the field, optional.
        self.id: str | None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_6(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int | str = number
        #: Description for the header field, optional
        self.description: str | None = description
        #: The id of the field, optional.
        self.id: str & None = id_

    # TODO: always put in id?
    def xǁFieldInfoǁ__init____mutmut_7(
        self,
        type_: Literal["Integer", "Float", "Flag", "Character", "String"],
        number: int | str,
        description: str | None = None,
        id_: str | None = None,
    ):
        #: The type, one of INFO_TYPES or FORMAT_TYPES
        self.type: Literal["Integer", "Float", "Flag", "Character", "String"] = type_
        #: Number description, either an int or constant
        self.number: int | str = number
        #: Description for the header field, optional
        self.description: str | None = description
        #: The id of the field, optional.
        self.id: str | None = None

    xǁFieldInfoǁ__init____mutmut_mutants = {
    'xǁFieldInfoǁ__init____mutmut_1': xǁFieldInfoǁ__init____mutmut_1, 
        'xǁFieldInfoǁ__init____mutmut_2': xǁFieldInfoǁ__init____mutmut_2, 
        'xǁFieldInfoǁ__init____mutmut_3': xǁFieldInfoǁ__init____mutmut_3, 
        'xǁFieldInfoǁ__init____mutmut_4': xǁFieldInfoǁ__init____mutmut_4, 
        'xǁFieldInfoǁ__init____mutmut_5': xǁFieldInfoǁ__init____mutmut_5, 
        'xǁFieldInfoǁ__init____mutmut_6': xǁFieldInfoǁ__init____mutmut_6, 
        'xǁFieldInfoǁ__init____mutmut_7': xǁFieldInfoǁ__init____mutmut_7
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFieldInfoǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFieldInfoǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁFieldInfoǁ__init____mutmut_orig)
    xǁFieldInfoǁ__init____mutmut_orig.__name__ = 'xǁFieldInfoǁ__init__'



    def xǁFieldInfoǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented  # pragma: no cover

    def xǁFieldInfoǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        return NotImplemented  # pragma: no cover

    xǁFieldInfoǁ__eq____mutmut_mutants = {
    'xǁFieldInfoǁ__eq____mutmut_1': xǁFieldInfoǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFieldInfoǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁFieldInfoǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁFieldInfoǁ__eq____mutmut_orig)
    xǁFieldInfoǁ__eq____mutmut_orig.__name__ = 'xǁFieldInfoǁ__eq__'



    def xǁFieldInfoǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented  # pragma: no cover

    def xǁFieldInfoǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return  self.__eq__(other)
        return NotImplemented  # pragma: no cover

    def xǁFieldInfoǁ__ne____mutmut_2(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return not self.__eq__(None)
        return NotImplemented  # pragma: no cover

    xǁFieldInfoǁ__ne____mutmut_mutants = {
    'xǁFieldInfoǁ__ne____mutmut_1': xǁFieldInfoǁ__ne____mutmut_1, 
        'xǁFieldInfoǁ__ne____mutmut_2': xǁFieldInfoǁ__ne____mutmut_2
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFieldInfoǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁFieldInfoǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁFieldInfoǁ__ne____mutmut_orig)
    xǁFieldInfoǁ__ne____mutmut_orig.__name__ = 'xǁFieldInfoǁ__ne__'



    def xǁFieldInfoǁ__hash____mutmut_orig(self):
        return hash(tuple(sorted(self.__dict__.items())))

    xǁFieldInfoǁ__hash____mutmut_mutants = {

    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFieldInfoǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁFieldInfoǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁFieldInfoǁ__hash____mutmut_orig)
    xǁFieldInfoǁ__hash____mutmut_orig.__name__ = 'xǁFieldInfoǁ__hash__'



    def xǁFieldInfoǁ__str____mutmut_orig(self):
        return "FieldInfo({}, {}, {}, {})".format(*map(repr, [self.type, self.number, self.description, self.id]))

    def xǁFieldInfoǁ__str____mutmut_1(self):
        return "XXFieldInfo({}, {}, {}, {})XX".format(*map(repr, [self.type, self.number, self.description, self.id]))

    def xǁFieldInfoǁ__str____mutmut_2(self):
        return "FieldInfo({}, {}, {}, {})".format(*map(None, [self.type, self.number, self.description, self.id]))

    def xǁFieldInfoǁ__str____mutmut_3(self):
        return "FieldInfo({}, {}, {}, {})".format(*map( [self.type, self.number, self.description, self.id]))

    xǁFieldInfoǁ__str____mutmut_mutants = {
    'xǁFieldInfoǁ__str____mutmut_1': xǁFieldInfoǁ__str____mutmut_1, 
        'xǁFieldInfoǁ__str____mutmut_2': xǁFieldInfoǁ__str____mutmut_2, 
        'xǁFieldInfoǁ__str____mutmut_3': xǁFieldInfoǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFieldInfoǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁFieldInfoǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁFieldInfoǁ__str____mutmut_orig)
    xǁFieldInfoǁ__str____mutmut_orig.__name__ = 'xǁFieldInfoǁ__str__'



    def xǁFieldInfoǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁFieldInfoǁ__repr____mutmut_1(self):
        return str(None)

    xǁFieldInfoǁ__repr____mutmut_mutants = {
    'xǁFieldInfoǁ__repr____mutmut_1': xǁFieldInfoǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFieldInfoǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁFieldInfoǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁFieldInfoǁ__repr____mutmut_orig)
    xǁFieldInfoǁ__repr____mutmut_orig.__name__ = 'xǁFieldInfoǁ__repr__'




# Reserved INFO keys ----------------------------------------------------------

#: Reserved fields for INFO from VCF v4.3
RESERVED_INFO = {
    # VCF v4.3, Section 1.6.1
    "AA": FieldInfo("String", 1, "Ancestral Allele"),
    "AC": FieldInfo(
        "Integer",
        "A",
        "Allele count in genotypes, for each ALT allele, in the same order as listed",
    ),
    "AD": FieldInfo("Integer", "R", "Total read depth for each allele"),
    "ADF": FieldInfo("Integer", "R", "Forward read depth for each allele"),
    "ADR": FieldInfo("Integer", "R", "Reverse read depth for each allele"),
    "AF": FieldInfo(
        "Float",
        "A",
        "Allele frequency for each ALT allele in the same order "
        "as listed: used for estimating from primary data not "
        "called genotypes",
    ),
    "AN": FieldInfo("Integer", 1, "Total number of alleles in called genotypes"),
    "BQ": FieldInfo("Float", 1, "RMS base quality at this position"),
    "CIGAR": FieldInfo(
        "String",
        "A",
        "CIGAR string describing how to align each ALT allele to the reference allele",
    ),
    "DB": FieldInfo("Flag", 0, "dbSNP membership"),
    "DP": FieldInfo(
        "Integer",
        1,
        "Combined depth across samples for small variants and Read Depth of segment containing breakend for SVs",
    ),
    "H2": FieldInfo("Flag", 0, "Membership in HapMap 2"),
    "H3": FieldInfo("Flag", 0, "Membership in HapMap 3"),
    "MQ": FieldInfo("Integer", 1, "RMS mapping quality"),
    "MQ0": FieldInfo("Integer", 1, "Number of MAPQ == 0 reads covering this record"),
    "NS": FieldInfo("Integer", 1, "Number of samples with data"),
    "SB": FieldInfo("Integer", 4, "Strand bias at this position"),
    "SOMATIC": FieldInfo("Flag", 0, "Indicates that the record is a somatic mutation, for cancer genomics"),
    "VALIDATED": FieldInfo("Flag", 0, "Validated by follow-up experiment"),
    "1000G": FieldInfo("Flag", 0, "Membership in 1000 Genomes"),
    # VCF v4.3, Section 3
    "IMPRECISE": FieldInfo("Flag", 0, "Imprecise structural variation"),
    "NOVEL": FieldInfo("Flag", 0, "Indicates a novel structural variation"),
    "END": FieldInfo(
        "Integer",
        1,
        "End position of the variant described in this record (for symbolic alleles)",
    ),
    "SVTYPE": FieldInfo("String", 1, "Type of structural variant"),
    "SVLEN": FieldInfo("Integer", 1, "Difference in length between REF and ALT alleles"),
    "CIPOS": FieldInfo("Integer", 2, "Confidence interval around POS for imprecise variants"),
    "CIEND": FieldInfo("Integer", 2, "Confidence interval around END for imprecise variants"),
    "HOMLEN": FieldInfo("Integer", ".", "Length of base pair identical micro-homology at event breakpoints"),
    "HOMSEQ": FieldInfo("String", ".", "Sequence of base pair identical micro-homology at event breakpoints"),
    "BKPTID": FieldInfo("String", ".", "ID of the assembled alternate allele in the assembly file"),
    "MEINFO": FieldInfo("String", 4, "Mobile element info of the form NAME,START,END,POLARITY"),
    "METRANS": FieldInfo("String", 4, "Mobile element transduction info of the form CHR,START,END,POLARITY"),
    "DGVID": FieldInfo("String", 1, "ID of this element in Database of Genomic Variation"),
    "DBVARID": FieldInfo("String", 1, "ID of this element in DBVAR"),
    "DBRIPID": FieldInfo("String", 1, "ID of this element in DBRIP"),
    "MATEID": FieldInfo("String", ".", "ID of mate breakends"),
    "PARID": FieldInfo("String", 1, "ID of partner breakend"),
    "EVENT": FieldInfo("String", 1, "ID of event associated to breakend"),
    "CILEN": FieldInfo("Integer", 2, "Confidence interval around the inserted material between breakends"),
    "DPADJ": FieldInfo("Integer", ".", "Read Depth of adjacency"),
    "CN": FieldInfo("Integer", 1, "Copy number of segment containing breakend"),
    "CNADJ": FieldInfo("Integer", ".", "Copy number of adjacency"),
    "CICN": FieldInfo("Integer", 2, "Confidence interval around copy number for the segment"),
    "CICNADJ": FieldInfo("Integer", ".", "Confidence interval around copy number for the adjacency"),
}

# Reserved FORMAT keys --------------------------------------------------------

RESERVED_FORMAT = {
    # VCF v 4.3, Section 1.6.2
    "AD": FieldInfo("Integer", "R", "Total, per-sample read depth"),
    "ADF": FieldInfo("Integer", "R", "Forward-strand, per-sample read depth"),
    "ADR": FieldInfo("Integer", "R", "Reverse-strand, per-sample read depth"),
    "DP": FieldInfo("Integer", 1, "Read depth at this position for this sample"),
    "EC": FieldInfo("Integer", "A", "Expected alternate allele counts for each alternate allele"),
    "FT": FieldInfo("String", "1", "Filters applied for this sample", "FORMAT/FT"),
    "GQ": FieldInfo("Integer", "G", "Phred-scale, conditional genotype quality"),
    "GP": FieldInfo("Float", "G", "Genotype posterior probabilities"),
    "GT": FieldInfo("String", 1, "Genotype call"),
    "GL": FieldInfo("Float", "G", "Log10-scaled likelihoods for genotypes"),
    "HQ": FieldInfo("Integer", 2, "Haplotype qualities"),
    "MQ": FieldInfo("Integer", 1, "RMS mapping quality"),
    "PL": FieldInfo("Integer", "G", "Phred-scaled genotype likelihoods, rounded to integers"),
    "PQ": FieldInfo("Integer", 1, "Phasing quality"),
    "PS": FieldInfo(
        "Integer",
        1,
        "Non-negative 32 bit integer giving phasing set for this sample and this chromosome",
    ),
    # VCF v4.3, Section 4
    "CN": FieldInfo("Integer", 1, "Copy number genotype for imprecise events"),
    "CNQ": FieldInfo("Float", 1, "Copy number genotype quality for imprecise events"),
    "CNL": FieldInfo("Float", "G", "Copy number genotype likelihood for imprecise events"),
    "CNP": FieldInfo("Float", "G", "Copy number posterior probabilities"),
    "NQ": FieldInfo("Integer", 1, "Phred style probability score that the variant is novel"),
    "HAP": FieldInfo("Integer", 1, "Unique haplotype identifier"),
    "AHAP": FieldInfo("Integer", 1, "Unique identifier of ancestral haplotype"),
}


# header files to enforce double-quoting for
QUOTE_FIELDS = ("Description", "Source", "Version")


def serialize_for_header__mutmut_orig(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_1(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key not in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_2(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(None)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_3(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if "XX XX" in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_4(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " not in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_5(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "XX\tXX" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_6(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" not in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_7(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value and "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_8(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(None)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_9(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "XX[{}]XX".format(", ".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_10(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format("XX, XX".join(value))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_11(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(None))  # type: ignore
    else:
        return str(value)


def serialize_for_header__mutmut_12(key: str, value: Any) -> str:
    """Serialize value for the given mapping key for a VCF header line"""
    if key in QUOTE_FIELDS:
        return json.dumps(value)
    elif isinstance(value, str):
        if " " in value or "\t" in value:
            return json.dumps(value)
        else:
            return value
    elif isinstance(value, list):
        return "[{}]".format(", ".join(value))  # type: ignore
    else:
        return str(None)

serialize_for_header__mutmut_mutants = {
'serialize_for_header__mutmut_1': serialize_for_header__mutmut_1, 
    'serialize_for_header__mutmut_2': serialize_for_header__mutmut_2, 
    'serialize_for_header__mutmut_3': serialize_for_header__mutmut_3, 
    'serialize_for_header__mutmut_4': serialize_for_header__mutmut_4, 
    'serialize_for_header__mutmut_5': serialize_for_header__mutmut_5, 
    'serialize_for_header__mutmut_6': serialize_for_header__mutmut_6, 
    'serialize_for_header__mutmut_7': serialize_for_header__mutmut_7, 
    'serialize_for_header__mutmut_8': serialize_for_header__mutmut_8, 
    'serialize_for_header__mutmut_9': serialize_for_header__mutmut_9, 
    'serialize_for_header__mutmut_10': serialize_for_header__mutmut_10, 
    'serialize_for_header__mutmut_11': serialize_for_header__mutmut_11, 
    'serialize_for_header__mutmut_12': serialize_for_header__mutmut_12
}

def serialize_for_header(*args, **kwargs):
    return _mutmut_trampoline(serialize_for_header__mutmut_orig, serialize_for_header__mutmut_mutants, *args, **kwargs) 

serialize_for_header.__signature__ = _mutmut_signature(serialize_for_header__mutmut_orig)
serialize_for_header__mutmut_orig.__name__ = 'serialize_for_header'




def header_without_lines__mutmut_orig(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_1(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(None)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_2(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = None
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_3(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = None
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_4(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(None, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_5(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "XXmappingXX"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_6(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr( "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_7(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if  isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_8(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'XXHeader line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLineXX'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_9(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("XXIDXX", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_10(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) not in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_11(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) not in remove:
                continue  # filter out
        lines.append(line)
    return Header(lines, header.samples)


def header_without_lines__mutmut_12(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(None)
    return Header(lines, header.samples)


def header_without_lines__mutmut_13(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header(None, header.samples)


def header_without_lines__mutmut_14(header: "Header", remove: Iterable[tuple[str, str]]) -> "Header":
    """Return :py:class:`Header` without lines given in ``remove``

    ``remove`` is an iterable of pairs ``key``/``ID`` with the VCF header key
    and ``ID`` of entry to remove.  In the case that a line does not have
    a ``mapping`` entry, you can give the full value to remove.

    .. code-block:: python

        # header is a vcfpy.Header, e.g., as read earlier from file
        new_header = vcfpy.without_header_lines(
            header, [('assembly', None), ('FILTER', 'PASS')])
        # now, the header lines starting with "##assembly=" and the "PASS"
        # filter line will be missing from new_header
    """
    remove = set(remove)
    # Copy over lines that are not removed
    lines: list[HeaderLine] = []
    for line in header.lines:
        if hasattr(line, "mapping"):
            if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):  # pragma: no cover
                raise HeaderInvalidType(
                    'Header line "{}={}" must be of type SimpleHeaderLine or CompoundHeaderLine'.format(
                        line.key, line.value
                    )
                )
            if (line.key, line.mapping.get("ID", None)) in remove:
                continue  # filter out
        else:
            if (line.key, line.value) in remove:
                continue  # filter out
        lines.append(line)
    return Header( header.samples)

header_without_lines__mutmut_mutants = {
'header_without_lines__mutmut_1': header_without_lines__mutmut_1, 
    'header_without_lines__mutmut_2': header_without_lines__mutmut_2, 
    'header_without_lines__mutmut_3': header_without_lines__mutmut_3, 
    'header_without_lines__mutmut_4': header_without_lines__mutmut_4, 
    'header_without_lines__mutmut_5': header_without_lines__mutmut_5, 
    'header_without_lines__mutmut_6': header_without_lines__mutmut_6, 
    'header_without_lines__mutmut_7': header_without_lines__mutmut_7, 
    'header_without_lines__mutmut_8': header_without_lines__mutmut_8, 
    'header_without_lines__mutmut_9': header_without_lines__mutmut_9, 
    'header_without_lines__mutmut_10': header_without_lines__mutmut_10, 
    'header_without_lines__mutmut_11': header_without_lines__mutmut_11, 
    'header_without_lines__mutmut_12': header_without_lines__mutmut_12, 
    'header_without_lines__mutmut_13': header_without_lines__mutmut_13, 
    'header_without_lines__mutmut_14': header_without_lines__mutmut_14
}

def header_without_lines(*args, **kwargs):
    return _mutmut_trampoline(header_without_lines__mutmut_orig, header_without_lines__mutmut_mutants, *args, **kwargs) 

header_without_lines.__signature__ = _mutmut_signature(header_without_lines__mutmut_orig)
header_without_lines__mutmut_orig.__name__ = 'header_without_lines'




class SamplesInfos:
    """Helper class for handling the samples in VCF files

    The purpose of this class is to decouple the sample name list somewhat
    from :py:class:`Header`.  This encapsulates subsetting samples for which
    the genotype should be parsed and reordering samples into output files.

    Note that when subsetting is used and the records are to be written out
    again then the ``FORMAT`` field must not be touched.
    """

    def xǁSamplesInfosǁ__init____mutmut_orig(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(sample_names)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples <= set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_1(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(None)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples <= set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_2(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = None
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples <= set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_3(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(sample_names)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = None
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples <= set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_4(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(sample_names)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = None
            assert self.parsed_samples <= set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_5(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(sample_names)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples < set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_6(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(sample_names)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples <= set(self.names), "XXMust be subset!XX"
        #: mapping from sample name to index
        self.name_to_idx = {name: idx for idx, name in enumerate(self.names)}

    def xǁSamplesInfosǁ__init____mutmut_7(self, sample_names: list[str], parsed_samples: list[str] | None = None):
        #: list of sample that are read from/written to the VCF file at
        #: hand in the given order
        self.names = list(sample_names)
        #: ``set`` with the samples for which the genotype call fields should
        #: be read; can be used for partial parsing (speedup) and defaults
        #: to the full list of samples, None if all are parsed
        self.parsed_samples = parsed_samples
        if self.parsed_samples:
            self.parsed_samples = set(self.parsed_samples)
            assert self.parsed_samples <= set(self.names), "Must be subset!"
        #: mapping from sample name to index
        self.name_to_idx = None

    xǁSamplesInfosǁ__init____mutmut_mutants = {
    'xǁSamplesInfosǁ__init____mutmut_1': xǁSamplesInfosǁ__init____mutmut_1, 
        'xǁSamplesInfosǁ__init____mutmut_2': xǁSamplesInfosǁ__init____mutmut_2, 
        'xǁSamplesInfosǁ__init____mutmut_3': xǁSamplesInfosǁ__init____mutmut_3, 
        'xǁSamplesInfosǁ__init____mutmut_4': xǁSamplesInfosǁ__init____mutmut_4, 
        'xǁSamplesInfosǁ__init____mutmut_5': xǁSamplesInfosǁ__init____mutmut_5, 
        'xǁSamplesInfosǁ__init____mutmut_6': xǁSamplesInfosǁ__init____mutmut_6, 
        'xǁSamplesInfosǁ__init____mutmut_7': xǁSamplesInfosǁ__init____mutmut_7
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁSamplesInfosǁ__init____mutmut_orig)
    xǁSamplesInfosǁ__init____mutmut_orig.__name__ = 'xǁSamplesInfosǁ__init__'



    def xǁSamplesInfosǁcopy__mutmut_orig(self):
        """Return a copy of the object"""
        return SamplesInfos(self.names)

    xǁSamplesInfosǁcopy__mutmut_mutants = {

    }

    def copy(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁcopy__mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁcopy__mutmut_mutants"), *args, **kwargs) 

    copy.__signature__ = _mutmut_signature(xǁSamplesInfosǁcopy__mutmut_orig)
    xǁSamplesInfosǁcopy__mutmut_orig.__name__ = 'xǁSamplesInfosǁcopy'



    def xǁSamplesInfosǁis_parsed__mutmut_orig(self, name: str) -> bool:
        """Return whether the sample name is parsed"""
        return (not self.parsed_samples) or name in self.parsed_samples

    def xǁSamplesInfosǁis_parsed__mutmut_1(self, name: str) -> bool:
        """Return whether the sample name is parsed"""
        return ( self.parsed_samples) or name in self.parsed_samples

    def xǁSamplesInfosǁis_parsed__mutmut_2(self, name: str) -> bool:
        """Return whether the sample name is parsed"""
        return (not self.parsed_samples) or name not in self.parsed_samples

    def xǁSamplesInfosǁis_parsed__mutmut_3(self, name: str) -> bool:
        """Return whether the sample name is parsed"""
        return (not self.parsed_samples) and name in self.parsed_samples

    xǁSamplesInfosǁis_parsed__mutmut_mutants = {
    'xǁSamplesInfosǁis_parsed__mutmut_1': xǁSamplesInfosǁis_parsed__mutmut_1, 
        'xǁSamplesInfosǁis_parsed__mutmut_2': xǁSamplesInfosǁis_parsed__mutmut_2, 
        'xǁSamplesInfosǁis_parsed__mutmut_3': xǁSamplesInfosǁis_parsed__mutmut_3
    }

    def is_parsed(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁis_parsed__mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁis_parsed__mutmut_mutants"), *args, **kwargs) 

    is_parsed.__signature__ = _mutmut_signature(xǁSamplesInfosǁis_parsed__mutmut_orig)
    xǁSamplesInfosǁis_parsed__mutmut_orig.__name__ = 'xǁSamplesInfosǁis_parsed'



    def xǁSamplesInfosǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: SamplesInfos")

    def xǁSamplesInfosǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: SamplesInfosXX")

    xǁSamplesInfosǁ__hash____mutmut_mutants = {
    'xǁSamplesInfosǁ__hash____mutmut_1': xǁSamplesInfosǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁSamplesInfosǁ__hash____mutmut_orig)
    xǁSamplesInfosǁ__hash____mutmut_orig.__name__ = 'xǁSamplesInfosǁ__hash__'



    def xǁSamplesInfosǁ__str____mutmut_orig(self):
        tpl = "SamplesInfos(names={}, name_to_idx={})"
        return tpl.format(self.names, pprint.pformat(self.name_to_idx, width=10**10))

    def xǁSamplesInfosǁ__str____mutmut_1(self):
        tpl = "XXSamplesInfos(names={}, name_to_idx={})XX"
        return tpl.format(self.names, pprint.pformat(self.name_to_idx, width=10**10))

    def xǁSamplesInfosǁ__str____mutmut_2(self):
        tpl = None
        return tpl.format(self.names, pprint.pformat(self.name_to_idx, width=10**10))

    def xǁSamplesInfosǁ__str____mutmut_3(self):
        tpl = "SamplesInfos(names={}, name_to_idx={})"
        return tpl.format(self.names, pprint.pformat(self.name_to_idx, width=11**10))

    def xǁSamplesInfosǁ__str____mutmut_4(self):
        tpl = "SamplesInfos(names={}, name_to_idx={})"
        return tpl.format(self.names, pprint.pformat(self.name_to_idx, width=10*10))

    def xǁSamplesInfosǁ__str____mutmut_5(self):
        tpl = "SamplesInfos(names={}, name_to_idx={})"
        return tpl.format(self.names, pprint.pformat(self.name_to_idx, width=10**11))

    def xǁSamplesInfosǁ__str____mutmut_6(self):
        tpl = "SamplesInfos(names={}, name_to_idx={})"
        return tpl.format(self.names, pprint.pformat(self.name_to_idx,))

    xǁSamplesInfosǁ__str____mutmut_mutants = {
    'xǁSamplesInfosǁ__str____mutmut_1': xǁSamplesInfosǁ__str____mutmut_1, 
        'xǁSamplesInfosǁ__str____mutmut_2': xǁSamplesInfosǁ__str____mutmut_2, 
        'xǁSamplesInfosǁ__str____mutmut_3': xǁSamplesInfosǁ__str____mutmut_3, 
        'xǁSamplesInfosǁ__str____mutmut_4': xǁSamplesInfosǁ__str____mutmut_4, 
        'xǁSamplesInfosǁ__str____mutmut_5': xǁSamplesInfosǁ__str____mutmut_5, 
        'xǁSamplesInfosǁ__str____mutmut_6': xǁSamplesInfosǁ__str____mutmut_6
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁSamplesInfosǁ__str____mutmut_orig)
    xǁSamplesInfosǁ__str____mutmut_orig.__name__ = 'xǁSamplesInfosǁ__str__'



    def xǁSamplesInfosǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁSamplesInfosǁ__repr____mutmut_1(self):
        return str(None)

    xǁSamplesInfosǁ__repr____mutmut_mutants = {
    'xǁSamplesInfosǁ__repr____mutmut_1': xǁSamplesInfosǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁSamplesInfosǁ__repr____mutmut_orig)
    xǁSamplesInfosǁ__repr____mutmut_orig.__name__ = 'xǁSamplesInfosǁ__repr__'



    def xǁSamplesInfosǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.names == other.names
        return NotImplemented  # pragma: no cover

    def xǁSamplesInfosǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.names != other.names
        return NotImplemented  # pragma: no cover

    xǁSamplesInfosǁ__eq____mutmut_mutants = {
    'xǁSamplesInfosǁ__eq____mutmut_1': xǁSamplesInfosǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁSamplesInfosǁ__eq____mutmut_orig)
    xǁSamplesInfosǁ__eq____mutmut_orig.__name__ = 'xǁSamplesInfosǁ__eq__'



    def xǁSamplesInfosǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.names != other.names
        return NotImplemented  # pragma: no cover

    def xǁSamplesInfosǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.names == other.names
        return NotImplemented  # pragma: no cover

    xǁSamplesInfosǁ__ne____mutmut_mutants = {
    'xǁSamplesInfosǁ__ne____mutmut_1': xǁSamplesInfosǁ__ne____mutmut_1
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSamplesInfosǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁSamplesInfosǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁSamplesInfosǁ__ne____mutmut_orig)
    xǁSamplesInfosǁ__ne____mutmut_orig.__name__ = 'xǁSamplesInfosǁ__ne__'




class Header:
    """Represent header of VCF file

    While this class allows mutating records, it should not be changed once it
    has been assigned to a writer.  Use :py:method:`~Header.copy` to create
    a copy that can be modified without problems.

    This class provides function for adding lines to a header and updating the
    supporting index data structures.  There is no explicit API for removing
    header lines, the best way is to reconstruct a new ``Header`` instance with
    a filtered list of header lines.
    """

    def xǁHeaderǁ__init____mutmut_orig(self, lines: list["HeaderLine"] | None = None, samples: SamplesInfos | None = None):
        #: ``list`` of :py:HeaderLine objects
        self.lines = lines or []
        #: :py:class:`SamplesInfo` object
        self.samples = samples
        # build indices for the different field types
        self._indices = self._build_indices()

    def xǁHeaderǁ__init____mutmut_1(self, lines: list["HeaderLine"] | None = None, samples: SamplesInfos | None = None):
        #: ``list`` of :py:HeaderLine objects
        self.lines = lines and []
        #: :py:class:`SamplesInfo` object
        self.samples = samples
        # build indices for the different field types
        self._indices = self._build_indices()

    def xǁHeaderǁ__init____mutmut_2(self, lines: list["HeaderLine"] | None = None, samples: SamplesInfos | None = None):
        #: ``list`` of :py:HeaderLine objects
        self.lines = None
        #: :py:class:`SamplesInfo` object
        self.samples = samples
        # build indices for the different field types
        self._indices = self._build_indices()

    def xǁHeaderǁ__init____mutmut_3(self, lines: list["HeaderLine"] | None = None, samples: SamplesInfos | None = None):
        #: ``list`` of :py:HeaderLine objects
        self.lines = lines or []
        #: :py:class:`SamplesInfo` object
        self.samples = None
        # build indices for the different field types
        self._indices = self._build_indices()

    def xǁHeaderǁ__init____mutmut_4(self, lines: list["HeaderLine"] | None = None, samples: SamplesInfos | None = None):
        #: ``list`` of :py:HeaderLine objects
        self.lines = lines or []
        #: :py:class:`SamplesInfo` object
        self.samples = samples
        # build indices for the different field types
        self._indices = None

    xǁHeaderǁ__init____mutmut_mutants = {
    'xǁHeaderǁ__init____mutmut_1': xǁHeaderǁ__init____mutmut_1, 
        'xǁHeaderǁ__init____mutmut_2': xǁHeaderǁ__init____mutmut_2, 
        'xǁHeaderǁ__init____mutmut_3': xǁHeaderǁ__init____mutmut_3, 
        'xǁHeaderǁ__init____mutmut_4': xǁHeaderǁ__init____mutmut_4
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁHeaderǁ__init____mutmut_orig)
    xǁHeaderǁ__init____mutmut_orig.__name__ = 'xǁHeaderǁ__init__'



    def xǁHeaderǁ_build_indices__mutmut_orig(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_1(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = None
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_2(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key not in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_3(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if  isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_4(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "XXHeader line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}XX".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_5(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(None)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_6(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["XXIDXX"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_7(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping[None] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_8(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] not in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_9(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[None]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_10(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("XXSeen {} header more than once: {}, using first occurenceXX").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_11(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["XXIDXX"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_12(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping[None]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_13(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        None,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_14(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_15(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[None][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_16(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["XXIDXX"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_17(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping[None]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_18(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][None] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_19(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = None
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_20(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = None
                result[line.key][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_21(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[None][idx] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_22(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][None] = line
        return result

    def xǁHeaderǁ_build_indices__mutmut_23(self) -> dict[str, dict["str", "HeaderLine"]]:
        """Build indices for the different field types"""
        result: dict[str, dict[str, "HeaderLine"]] = {key: {} for key in LINES_WITH_ID}
        for line in self.lines:
            if line.key in LINES_WITH_ID:
                if not isinstance(line, (SimpleHeaderLine, CompoundHeaderLine)):
                    raise HeaderInvalidType(
                        "Header line must be of type SimpleHeaderLine or CompoundHeaderLine but is {}".format(
                            type(line)
                        )
                    )
                result.setdefault(line.key, {})
                if line.mapping["ID"] in result[line.key]:
                    warnings.warn(
                        ("Seen {} header more than once: {}, using first occurence").format(
                            line.key, line.mapping["ID"]
                        ),
                        DuplicateHeaderLineWarning,
                    )
                else:
                    result[line.key][line.mapping["ID"]] = line
            else:
                result.setdefault(line.key, {})
                idx = f"{len(result[line.key])}"
                result[line.key][idx] = None
        return result

    xǁHeaderǁ_build_indices__mutmut_mutants = {
    'xǁHeaderǁ_build_indices__mutmut_1': xǁHeaderǁ_build_indices__mutmut_1, 
        'xǁHeaderǁ_build_indices__mutmut_2': xǁHeaderǁ_build_indices__mutmut_2, 
        'xǁHeaderǁ_build_indices__mutmut_3': xǁHeaderǁ_build_indices__mutmut_3, 
        'xǁHeaderǁ_build_indices__mutmut_4': xǁHeaderǁ_build_indices__mutmut_4, 
        'xǁHeaderǁ_build_indices__mutmut_5': xǁHeaderǁ_build_indices__mutmut_5, 
        'xǁHeaderǁ_build_indices__mutmut_6': xǁHeaderǁ_build_indices__mutmut_6, 
        'xǁHeaderǁ_build_indices__mutmut_7': xǁHeaderǁ_build_indices__mutmut_7, 
        'xǁHeaderǁ_build_indices__mutmut_8': xǁHeaderǁ_build_indices__mutmut_8, 
        'xǁHeaderǁ_build_indices__mutmut_9': xǁHeaderǁ_build_indices__mutmut_9, 
        'xǁHeaderǁ_build_indices__mutmut_10': xǁHeaderǁ_build_indices__mutmut_10, 
        'xǁHeaderǁ_build_indices__mutmut_11': xǁHeaderǁ_build_indices__mutmut_11, 
        'xǁHeaderǁ_build_indices__mutmut_12': xǁHeaderǁ_build_indices__mutmut_12, 
        'xǁHeaderǁ_build_indices__mutmut_13': xǁHeaderǁ_build_indices__mutmut_13, 
        'xǁHeaderǁ_build_indices__mutmut_14': xǁHeaderǁ_build_indices__mutmut_14, 
        'xǁHeaderǁ_build_indices__mutmut_15': xǁHeaderǁ_build_indices__mutmut_15, 
        'xǁHeaderǁ_build_indices__mutmut_16': xǁHeaderǁ_build_indices__mutmut_16, 
        'xǁHeaderǁ_build_indices__mutmut_17': xǁHeaderǁ_build_indices__mutmut_17, 
        'xǁHeaderǁ_build_indices__mutmut_18': xǁHeaderǁ_build_indices__mutmut_18, 
        'xǁHeaderǁ_build_indices__mutmut_19': xǁHeaderǁ_build_indices__mutmut_19, 
        'xǁHeaderǁ_build_indices__mutmut_20': xǁHeaderǁ_build_indices__mutmut_20, 
        'xǁHeaderǁ_build_indices__mutmut_21': xǁHeaderǁ_build_indices__mutmut_21, 
        'xǁHeaderǁ_build_indices__mutmut_22': xǁHeaderǁ_build_indices__mutmut_22, 
        'xǁHeaderǁ_build_indices__mutmut_23': xǁHeaderǁ_build_indices__mutmut_23
    }

    def _build_indices(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ_build_indices__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ_build_indices__mutmut_mutants"), *args, **kwargs) 

    _build_indices.__signature__ = _mutmut_signature(xǁHeaderǁ_build_indices__mutmut_orig)
    xǁHeaderǁ_build_indices__mutmut_orig.__name__ = 'xǁHeaderǁ_build_indices'



    def xǁHeaderǁcopy__mutmut_orig(self):
        """Return a copy of this header"""
        return Header([line.copy() for line in self.lines], None if self.samples is None else self.samples.copy())

    def xǁHeaderǁcopy__mutmut_1(self):
        """Return a copy of this header"""
        return Header([line.copy() for line in self.lines], None if self.samples is not None else self.samples.copy())

    xǁHeaderǁcopy__mutmut_mutants = {
    'xǁHeaderǁcopy__mutmut_1': xǁHeaderǁcopy__mutmut_1
    }

    def copy(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁcopy__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁcopy__mutmut_mutants"), *args, **kwargs) 

    copy.__signature__ = _mutmut_signature(xǁHeaderǁcopy__mutmut_orig)
    xǁHeaderǁcopy__mutmut_orig.__name__ = 'xǁHeaderǁcopy'



    def xǁHeaderǁadd_filter_line__mutmut_orig(self, mapping: dict[str, Any]):
        """Add FILTER header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(FilterHeaderLine.from_mapping(mapping))

    def xǁHeaderǁadd_filter_line__mutmut_1(self, mapping: dict[str, Any]):
        """Add FILTER header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(FilterHeaderLine.from_mapping(None))

    xǁHeaderǁadd_filter_line__mutmut_mutants = {
    'xǁHeaderǁadd_filter_line__mutmut_1': xǁHeaderǁadd_filter_line__mutmut_1
    }

    def add_filter_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁadd_filter_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁadd_filter_line__mutmut_mutants"), *args, **kwargs) 

    add_filter_line.__signature__ = _mutmut_signature(xǁHeaderǁadd_filter_line__mutmut_orig)
    xǁHeaderǁadd_filter_line__mutmut_orig.__name__ = 'xǁHeaderǁadd_filter_line'



    def xǁHeaderǁadd_contig_line__mutmut_orig(self, mapping: dict[str, Any]):
        """Add "contig" header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(ContigHeaderLine.from_mapping(mapping))

    def xǁHeaderǁadd_contig_line__mutmut_1(self, mapping: dict[str, Any]):
        """Add "contig" header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(ContigHeaderLine.from_mapping(None))

    xǁHeaderǁadd_contig_line__mutmut_mutants = {
    'xǁHeaderǁadd_contig_line__mutmut_1': xǁHeaderǁadd_contig_line__mutmut_1
    }

    def add_contig_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁadd_contig_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁadd_contig_line__mutmut_mutants"), *args, **kwargs) 

    add_contig_line.__signature__ = _mutmut_signature(xǁHeaderǁadd_contig_line__mutmut_orig)
    xǁHeaderǁadd_contig_line__mutmut_orig.__name__ = 'xǁHeaderǁadd_contig_line'



    def xǁHeaderǁadd_info_line__mutmut_orig(self, mapping: dict[str, Any]):
        """Add INFO header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(InfoHeaderLine.from_mapping(mapping))

    def xǁHeaderǁadd_info_line__mutmut_1(self, mapping: dict[str, Any]):
        """Add INFO header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(InfoHeaderLine.from_mapping(None))

    xǁHeaderǁadd_info_line__mutmut_mutants = {
    'xǁHeaderǁadd_info_line__mutmut_1': xǁHeaderǁadd_info_line__mutmut_1
    }

    def add_info_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁadd_info_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁadd_info_line__mutmut_mutants"), *args, **kwargs) 

    add_info_line.__signature__ = _mutmut_signature(xǁHeaderǁadd_info_line__mutmut_orig)
    xǁHeaderǁadd_info_line__mutmut_orig.__name__ = 'xǁHeaderǁadd_info_line'



    def xǁHeaderǁadd_format_line__mutmut_orig(self, mapping: dict[str, Any]):
        """Add FORMAT header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(FormatHeaderLine.from_mapping(mapping))

    def xǁHeaderǁadd_format_line__mutmut_1(self, mapping: dict[str, Any]):
        """Add FORMAT header line constructed from the given mapping

        :param mapping: ``OrderedDict`` with mapping to add.  It is
            recommended to use ``OrderedDict`` over ``dict`` as this makes
            the result reproducible
        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        return self.add_line(FormatHeaderLine.from_mapping(None))

    xǁHeaderǁadd_format_line__mutmut_mutants = {
    'xǁHeaderǁadd_format_line__mutmut_1': xǁHeaderǁadd_format_line__mutmut_1
    }

    def add_format_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁadd_format_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁadd_format_line__mutmut_mutants"), *args, **kwargs) 

    add_format_line.__signature__ = _mutmut_signature(xǁHeaderǁadd_format_line__mutmut_orig)
    xǁHeaderǁadd_format_line__mutmut_orig.__name__ = 'xǁHeaderǁadd_format_line'



    def xǁHeaderǁformat_ids__mutmut_orig(self) -> list[str]:
        """Return list of all format IDs"""
        return list(self._indices["FORMAT"].keys())

    def xǁHeaderǁformat_ids__mutmut_1(self) -> list[str]:
        """Return list of all format IDs"""
        return list(self._indices["XXFORMATXX"].keys())

    def xǁHeaderǁformat_ids__mutmut_2(self) -> list[str]:
        """Return list of all format IDs"""
        return list(self._indices[None].keys())

    xǁHeaderǁformat_ids__mutmut_mutants = {
    'xǁHeaderǁformat_ids__mutmut_1': xǁHeaderǁformat_ids__mutmut_1, 
        'xǁHeaderǁformat_ids__mutmut_2': xǁHeaderǁformat_ids__mutmut_2
    }

    def format_ids(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁformat_ids__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁformat_ids__mutmut_mutants"), *args, **kwargs) 

    format_ids.__signature__ = _mutmut_signature(xǁHeaderǁformat_ids__mutmut_orig)
    xǁHeaderǁformat_ids__mutmut_orig.__name__ = 'xǁHeaderǁformat_ids'



    def xǁHeaderǁfilter_ids__mutmut_orig(self):
        """Return list of all filter IDs"""
        return list(self._indices["FILTER"].keys())

    def xǁHeaderǁfilter_ids__mutmut_1(self):
        """Return list of all filter IDs"""
        return list(self._indices["XXFILTERXX"].keys())

    def xǁHeaderǁfilter_ids__mutmut_2(self):
        """Return list of all filter IDs"""
        return list(self._indices[None].keys())

    xǁHeaderǁfilter_ids__mutmut_mutants = {
    'xǁHeaderǁfilter_ids__mutmut_1': xǁHeaderǁfilter_ids__mutmut_1, 
        'xǁHeaderǁfilter_ids__mutmut_2': xǁHeaderǁfilter_ids__mutmut_2
    }

    def filter_ids(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁfilter_ids__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁfilter_ids__mutmut_mutants"), *args, **kwargs) 

    filter_ids.__signature__ = _mutmut_signature(xǁHeaderǁfilter_ids__mutmut_orig)
    xǁHeaderǁfilter_ids__mutmut_orig.__name__ = 'xǁHeaderǁfilter_ids'



    def xǁHeaderǁinfo_ids__mutmut_orig(self):
        """Return list of all info IDs"""
        return list(self._indices["INFO"].keys())

    def xǁHeaderǁinfo_ids__mutmut_1(self):
        """Return list of all info IDs"""
        return list(self._indices["XXINFOXX"].keys())

    def xǁHeaderǁinfo_ids__mutmut_2(self):
        """Return list of all info IDs"""
        return list(self._indices[None].keys())

    xǁHeaderǁinfo_ids__mutmut_mutants = {
    'xǁHeaderǁinfo_ids__mutmut_1': xǁHeaderǁinfo_ids__mutmut_1, 
        'xǁHeaderǁinfo_ids__mutmut_2': xǁHeaderǁinfo_ids__mutmut_2
    }

    def info_ids(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁinfo_ids__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁinfo_ids__mutmut_mutants"), *args, **kwargs) 

    info_ids.__signature__ = _mutmut_signature(xǁHeaderǁinfo_ids__mutmut_orig)
    xǁHeaderǁinfo_ids__mutmut_orig.__name__ = 'xǁHeaderǁinfo_ids'



    def xǁHeaderǁget_lines__mutmut_orig(self, key: str) -> Iterable["HeaderLine"]:
        """Return header lines having the given ``key`` as their type"""
        if key in self._indices:
            return self._indices[key].values()
        else:
            return []

    def xǁHeaderǁget_lines__mutmut_1(self, key: str) -> Iterable["HeaderLine"]:
        """Return header lines having the given ``key`` as their type"""
        if key not in self._indices:
            return self._indices[key].values()
        else:
            return []

    def xǁHeaderǁget_lines__mutmut_2(self, key: str) -> Iterable["HeaderLine"]:
        """Return header lines having the given ``key`` as their type"""
        if key in self._indices:
            return self._indices[None].values()
        else:
            return []

    xǁHeaderǁget_lines__mutmut_mutants = {
    'xǁHeaderǁget_lines__mutmut_1': xǁHeaderǁget_lines__mutmut_1, 
        'xǁHeaderǁget_lines__mutmut_2': xǁHeaderǁget_lines__mutmut_2
    }

    def get_lines(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁget_lines__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁget_lines__mutmut_mutants"), *args, **kwargs) 

    get_lines.__signature__ = _mutmut_signature(xǁHeaderǁget_lines__mutmut_orig)
    xǁHeaderǁget_lines__mutmut_orig.__name__ = 'xǁHeaderǁget_lines'



    def xǁHeaderǁhas_header_line__mutmut_orig(self, key: str, id_: str):
        """Return whether there is a header line with the given ID of the
        type given by ``key``

        :param key: The VCF header key/line type.
        :param id_: The ID value to compare fore

        :return: ``True`` if there is a header line starting with ``##${key}=``
            in the VCF file having the mapping entry ``ID`` set to ``id_``.
        """
        if key not in self._indices:
            return False
        else:
            return id_ in self._indices[key]

    def xǁHeaderǁhas_header_line__mutmut_1(self, key: str, id_: str):
        """Return whether there is a header line with the given ID of the
        type given by ``key``

        :param key: The VCF header key/line type.
        :param id_: The ID value to compare fore

        :return: ``True`` if there is a header line starting with ``##${key}=``
            in the VCF file having the mapping entry ``ID`` set to ``id_``.
        """
        if key  in self._indices:
            return False
        else:
            return id_ in self._indices[key]

    def xǁHeaderǁhas_header_line__mutmut_2(self, key: str, id_: str):
        """Return whether there is a header line with the given ID of the
        type given by ``key``

        :param key: The VCF header key/line type.
        :param id_: The ID value to compare fore

        :return: ``True`` if there is a header line starting with ``##${key}=``
            in the VCF file having the mapping entry ``ID`` set to ``id_``.
        """
        if key not in self._indices:
            return True
        else:
            return id_ in self._indices[key]

    def xǁHeaderǁhas_header_line__mutmut_3(self, key: str, id_: str):
        """Return whether there is a header line with the given ID of the
        type given by ``key``

        :param key: The VCF header key/line type.
        :param id_: The ID value to compare fore

        :return: ``True`` if there is a header line starting with ``##${key}=``
            in the VCF file having the mapping entry ``ID`` set to ``id_``.
        """
        if key not in self._indices:
            return False
        else:
            return id_ not in self._indices[key]

    def xǁHeaderǁhas_header_line__mutmut_4(self, key: str, id_: str):
        """Return whether there is a header line with the given ID of the
        type given by ``key``

        :param key: The VCF header key/line type.
        :param id_: The ID value to compare fore

        :return: ``True`` if there is a header line starting with ``##${key}=``
            in the VCF file having the mapping entry ``ID`` set to ``id_``.
        """
        if key not in self._indices:
            return False
        else:
            return id_ in self._indices[None]

    xǁHeaderǁhas_header_line__mutmut_mutants = {
    'xǁHeaderǁhas_header_line__mutmut_1': xǁHeaderǁhas_header_line__mutmut_1, 
        'xǁHeaderǁhas_header_line__mutmut_2': xǁHeaderǁhas_header_line__mutmut_2, 
        'xǁHeaderǁhas_header_line__mutmut_3': xǁHeaderǁhas_header_line__mutmut_3, 
        'xǁHeaderǁhas_header_line__mutmut_4': xǁHeaderǁhas_header_line__mutmut_4
    }

    def has_header_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁhas_header_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁhas_header_line__mutmut_mutants"), *args, **kwargs) 

    has_header_line.__signature__ = _mutmut_signature(xǁHeaderǁhas_header_line__mutmut_orig)
    xǁHeaderǁhas_header_line__mutmut_orig.__name__ = 'xǁHeaderǁhas_header_line'



    def xǁHeaderǁadd_line__mutmut_orig(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_1(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(None)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_2(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if  hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_3(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(None, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_4(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "XXmappingXX"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_5(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr( "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_6(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return True  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_7(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["XXIDXX"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_8(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping[None]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_9(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("XXDetected duplicate header line with type {} and ID {}. Ignoring this and subsequent oneXX").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_10(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["XXIDXX"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_11(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping[None]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_12(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                None,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_13(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_14(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return True
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_15(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[None][header_line.mapping["ID"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_16(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["XXIDXX"]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_17(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping[None]] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_18(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][None] = header_line
            return True

    def xǁHeaderǁadd_line__mutmut_19(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = None
            return True

    def xǁHeaderǁadd_line__mutmut_20(self, header_line: "HeaderLine"):
        """Add header line, updating any necessary support indices

        :return: ``False`` on conflicting line and ``True`` otherwise
        """
        self.lines.append(header_line)
        self._indices.setdefault(header_line.key, {})
        if not hasattr(header_line, "mapping"):
            return False  # no registration required
        if self.has_header_line(header_line.key, header_line.mapping["ID"]):  # pragma: no cover
            warnings.warn(
                ("Detected duplicate header line with type {} and ID {}. Ignoring this and subsequent one").format(
                    header_line.key, header_line.mapping["ID"]
                ),
                DuplicateHeaderLineWarning,
            )
            return False
        else:
            self._indices[header_line.key][header_line.mapping["ID"]] = header_line
            return False

    xǁHeaderǁadd_line__mutmut_mutants = {
    'xǁHeaderǁadd_line__mutmut_1': xǁHeaderǁadd_line__mutmut_1, 
        'xǁHeaderǁadd_line__mutmut_2': xǁHeaderǁadd_line__mutmut_2, 
        'xǁHeaderǁadd_line__mutmut_3': xǁHeaderǁadd_line__mutmut_3, 
        'xǁHeaderǁadd_line__mutmut_4': xǁHeaderǁadd_line__mutmut_4, 
        'xǁHeaderǁadd_line__mutmut_5': xǁHeaderǁadd_line__mutmut_5, 
        'xǁHeaderǁadd_line__mutmut_6': xǁHeaderǁadd_line__mutmut_6, 
        'xǁHeaderǁadd_line__mutmut_7': xǁHeaderǁadd_line__mutmut_7, 
        'xǁHeaderǁadd_line__mutmut_8': xǁHeaderǁadd_line__mutmut_8, 
        'xǁHeaderǁadd_line__mutmut_9': xǁHeaderǁadd_line__mutmut_9, 
        'xǁHeaderǁadd_line__mutmut_10': xǁHeaderǁadd_line__mutmut_10, 
        'xǁHeaderǁadd_line__mutmut_11': xǁHeaderǁadd_line__mutmut_11, 
        'xǁHeaderǁadd_line__mutmut_12': xǁHeaderǁadd_line__mutmut_12, 
        'xǁHeaderǁadd_line__mutmut_13': xǁHeaderǁadd_line__mutmut_13, 
        'xǁHeaderǁadd_line__mutmut_14': xǁHeaderǁadd_line__mutmut_14, 
        'xǁHeaderǁadd_line__mutmut_15': xǁHeaderǁadd_line__mutmut_15, 
        'xǁHeaderǁadd_line__mutmut_16': xǁHeaderǁadd_line__mutmut_16, 
        'xǁHeaderǁadd_line__mutmut_17': xǁHeaderǁadd_line__mutmut_17, 
        'xǁHeaderǁadd_line__mutmut_18': xǁHeaderǁadd_line__mutmut_18, 
        'xǁHeaderǁadd_line__mutmut_19': xǁHeaderǁadd_line__mutmut_19, 
        'xǁHeaderǁadd_line__mutmut_20': xǁHeaderǁadd_line__mutmut_20
    }

    def add_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁadd_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁadd_line__mutmut_mutants"), *args, **kwargs) 

    add_line.__signature__ = _mutmut_signature(xǁHeaderǁadd_line__mutmut_orig)
    xǁHeaderǁadd_line__mutmut_orig.__name__ = 'xǁHeaderǁadd_line'



    def xǁHeaderǁget_info_field_info__mutmut_orig(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given INFO field"""
        return self._get_field_info("INFO", key, RESERVED_INFO)

    def xǁHeaderǁget_info_field_info__mutmut_1(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given INFO field"""
        return self._get_field_info("XXINFOXX", key, RESERVED_INFO)

    def xǁHeaderǁget_info_field_info__mutmut_2(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given INFO field"""
        return self._get_field_info("INFO", None, RESERVED_INFO)

    def xǁHeaderǁget_info_field_info__mutmut_3(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given INFO field"""
        return self._get_field_info("INFO", key, None)

    def xǁHeaderǁget_info_field_info__mutmut_4(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given INFO field"""
        return self._get_field_info("INFO", RESERVED_INFO)

    def xǁHeaderǁget_info_field_info__mutmut_5(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given INFO field"""
        return self._get_field_info("INFO", key,)

    xǁHeaderǁget_info_field_info__mutmut_mutants = {
    'xǁHeaderǁget_info_field_info__mutmut_1': xǁHeaderǁget_info_field_info__mutmut_1, 
        'xǁHeaderǁget_info_field_info__mutmut_2': xǁHeaderǁget_info_field_info__mutmut_2, 
        'xǁHeaderǁget_info_field_info__mutmut_3': xǁHeaderǁget_info_field_info__mutmut_3, 
        'xǁHeaderǁget_info_field_info__mutmut_4': xǁHeaderǁget_info_field_info__mutmut_4, 
        'xǁHeaderǁget_info_field_info__mutmut_5': xǁHeaderǁget_info_field_info__mutmut_5
    }

    def get_info_field_info(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁget_info_field_info__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁget_info_field_info__mutmut_mutants"), *args, **kwargs) 

    get_info_field_info.__signature__ = _mutmut_signature(xǁHeaderǁget_info_field_info__mutmut_orig)
    xǁHeaderǁget_info_field_info__mutmut_orig.__name__ = 'xǁHeaderǁget_info_field_info'



    def xǁHeaderǁget_format_field_info__mutmut_orig(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given FORMAT field"""
        return self._get_field_info("FORMAT", key, RESERVED_FORMAT)

    def xǁHeaderǁget_format_field_info__mutmut_1(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given FORMAT field"""
        return self._get_field_info("XXFORMATXX", key, RESERVED_FORMAT)

    def xǁHeaderǁget_format_field_info__mutmut_2(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given FORMAT field"""
        return self._get_field_info("FORMAT", None, RESERVED_FORMAT)

    def xǁHeaderǁget_format_field_info__mutmut_3(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given FORMAT field"""
        return self._get_field_info("FORMAT", key, None)

    def xǁHeaderǁget_format_field_info__mutmut_4(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given FORMAT field"""
        return self._get_field_info("FORMAT", RESERVED_FORMAT)

    def xǁHeaderǁget_format_field_info__mutmut_5(self, key: str) -> FieldInfo:
        """Return :py:class:`FieldInfo` for the given FORMAT field"""
        return self._get_field_info("FORMAT", key,)

    xǁHeaderǁget_format_field_info__mutmut_mutants = {
    'xǁHeaderǁget_format_field_info__mutmut_1': xǁHeaderǁget_format_field_info__mutmut_1, 
        'xǁHeaderǁget_format_field_info__mutmut_2': xǁHeaderǁget_format_field_info__mutmut_2, 
        'xǁHeaderǁget_format_field_info__mutmut_3': xǁHeaderǁget_format_field_info__mutmut_3, 
        'xǁHeaderǁget_format_field_info__mutmut_4': xǁHeaderǁget_format_field_info__mutmut_4, 
        'xǁHeaderǁget_format_field_info__mutmut_5': xǁHeaderǁget_format_field_info__mutmut_5
    }

    def get_format_field_info(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁget_format_field_info__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁget_format_field_info__mutmut_mutants"), *args, **kwargs) 

    get_format_field_info.__signature__ = _mutmut_signature(xǁHeaderǁget_format_field_info__mutmut_orig)
    xǁHeaderǁget_format_field_info__mutmut_orig.__name__ = 'xǁHeaderǁget_format_field_info'



    def xǁHeaderǁ_get_field_info__mutmut_orig(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_1(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[None].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_2(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(None)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_3(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = None
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_4(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result or isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_5(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["XXTypeXX"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_6(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping[None],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_7(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["XXNumberXX"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_8(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping[None],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_9(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("XXDescriptionXX"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_10(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["XXIDXX"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_11(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping[None],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_12(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key not in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_13(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[None]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_14(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = None
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_15(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("XXStringXX", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_16(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", None)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_17(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String",)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_18(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = None
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_19(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "XX{} {} not found using {}/{} insteadXX".format(type_, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_20(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(None, key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_21(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, None, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_22(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format( key, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_23(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, res.type, repr(res.number)),
            FieldInfoNotFound,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_24(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
            None,
        )
        return res

    def xǁHeaderǁ_get_field_info__mutmut_25(self, type_: str, key: str, reserved: dict[str, FieldInfo]) -> FieldInfo:
        result = self._indices[type_].get(key)
        if result and isinstance(result, (SimpleHeaderLine, CompoundHeaderLine)):
            return FieldInfo(
                result.mapping["Type"],
                result.mapping["Number"],
                result.mapping.get("Description"),
                result.mapping["ID"],
            )
        if key in reserved:
            res = reserved[key]
        else:
            res = FieldInfo("String", HEADER_NUMBER_UNBOUNDED)
        warnings.warn(
            "{} {} not found using {}/{} instead".format(type_, key, res.type, repr(res.number)),
        )
        return res

    xǁHeaderǁ_get_field_info__mutmut_mutants = {
    'xǁHeaderǁ_get_field_info__mutmut_1': xǁHeaderǁ_get_field_info__mutmut_1, 
        'xǁHeaderǁ_get_field_info__mutmut_2': xǁHeaderǁ_get_field_info__mutmut_2, 
        'xǁHeaderǁ_get_field_info__mutmut_3': xǁHeaderǁ_get_field_info__mutmut_3, 
        'xǁHeaderǁ_get_field_info__mutmut_4': xǁHeaderǁ_get_field_info__mutmut_4, 
        'xǁHeaderǁ_get_field_info__mutmut_5': xǁHeaderǁ_get_field_info__mutmut_5, 
        'xǁHeaderǁ_get_field_info__mutmut_6': xǁHeaderǁ_get_field_info__mutmut_6, 
        'xǁHeaderǁ_get_field_info__mutmut_7': xǁHeaderǁ_get_field_info__mutmut_7, 
        'xǁHeaderǁ_get_field_info__mutmut_8': xǁHeaderǁ_get_field_info__mutmut_8, 
        'xǁHeaderǁ_get_field_info__mutmut_9': xǁHeaderǁ_get_field_info__mutmut_9, 
        'xǁHeaderǁ_get_field_info__mutmut_10': xǁHeaderǁ_get_field_info__mutmut_10, 
        'xǁHeaderǁ_get_field_info__mutmut_11': xǁHeaderǁ_get_field_info__mutmut_11, 
        'xǁHeaderǁ_get_field_info__mutmut_12': xǁHeaderǁ_get_field_info__mutmut_12, 
        'xǁHeaderǁ_get_field_info__mutmut_13': xǁHeaderǁ_get_field_info__mutmut_13, 
        'xǁHeaderǁ_get_field_info__mutmut_14': xǁHeaderǁ_get_field_info__mutmut_14, 
        'xǁHeaderǁ_get_field_info__mutmut_15': xǁHeaderǁ_get_field_info__mutmut_15, 
        'xǁHeaderǁ_get_field_info__mutmut_16': xǁHeaderǁ_get_field_info__mutmut_16, 
        'xǁHeaderǁ_get_field_info__mutmut_17': xǁHeaderǁ_get_field_info__mutmut_17, 
        'xǁHeaderǁ_get_field_info__mutmut_18': xǁHeaderǁ_get_field_info__mutmut_18, 
        'xǁHeaderǁ_get_field_info__mutmut_19': xǁHeaderǁ_get_field_info__mutmut_19, 
        'xǁHeaderǁ_get_field_info__mutmut_20': xǁHeaderǁ_get_field_info__mutmut_20, 
        'xǁHeaderǁ_get_field_info__mutmut_21': xǁHeaderǁ_get_field_info__mutmut_21, 
        'xǁHeaderǁ_get_field_info__mutmut_22': xǁHeaderǁ_get_field_info__mutmut_22, 
        'xǁHeaderǁ_get_field_info__mutmut_23': xǁHeaderǁ_get_field_info__mutmut_23, 
        'xǁHeaderǁ_get_field_info__mutmut_24': xǁHeaderǁ_get_field_info__mutmut_24, 
        'xǁHeaderǁ_get_field_info__mutmut_25': xǁHeaderǁ_get_field_info__mutmut_25
    }

    def _get_field_info(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ_get_field_info__mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ_get_field_info__mutmut_mutants"), *args, **kwargs) 

    _get_field_info.__signature__ = _mutmut_signature(xǁHeaderǁ_get_field_info__mutmut_orig)
    xǁHeaderǁ_get_field_info__mutmut_orig.__name__ = 'xǁHeaderǁ_get_field_info'



    def xǁHeaderǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.lines, self.samples) == (other.lines, other.samples)
        return NotImplemented  # pragma: no cover

    def xǁHeaderǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.lines, self.samples) != (other.lines, other.samples)
        return NotImplemented  # pragma: no cover

    xǁHeaderǁ__eq____mutmut_mutants = {
    'xǁHeaderǁ__eq____mutmut_1': xǁHeaderǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁHeaderǁ__eq____mutmut_orig)
    xǁHeaderǁ__eq____mutmut_orig.__name__ = 'xǁHeaderǁ__eq__'



    def xǁHeaderǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.lines, self.samples) != (other.lines, other.samples)
        return NotImplemented  # pragma: no cover

    def xǁHeaderǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.lines, self.samples) == (other.lines, other.samples)
        return NotImplemented  # pragma: no cover

    xǁHeaderǁ__ne____mutmut_mutants = {
    'xǁHeaderǁ__ne____mutmut_1': xǁHeaderǁ__ne____mutmut_1
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁHeaderǁ__ne____mutmut_orig)
    xǁHeaderǁ__ne____mutmut_orig.__name__ = 'xǁHeaderǁ__ne__'



    def xǁHeaderǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: Header")

    def xǁHeaderǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: HeaderXX")

    xǁHeaderǁ__hash____mutmut_mutants = {
    'xǁHeaderǁ__hash____mutmut_1': xǁHeaderǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁHeaderǁ__hash____mutmut_orig)
    xǁHeaderǁ__hash____mutmut_orig.__name__ = 'xǁHeaderǁ__hash__'



    def xǁHeaderǁ__str____mutmut_orig(self):
        tpl = "Header(lines={}, samples={})"
        return tpl.format(*map(repr, (self.lines, self.samples)))

    def xǁHeaderǁ__str____mutmut_1(self):
        tpl = "XXHeader(lines={}, samples={})XX"
        return tpl.format(*map(repr, (self.lines, self.samples)))

    def xǁHeaderǁ__str____mutmut_2(self):
        tpl = None
        return tpl.format(*map(repr, (self.lines, self.samples)))

    def xǁHeaderǁ__str____mutmut_3(self):
        tpl = "Header(lines={}, samples={})"
        return tpl.format(*map(None, (self.lines, self.samples)))

    def xǁHeaderǁ__str____mutmut_4(self):
        tpl = "Header(lines={}, samples={})"
        return tpl.format(*map( (self.lines, self.samples)))

    xǁHeaderǁ__str____mutmut_mutants = {
    'xǁHeaderǁ__str____mutmut_1': xǁHeaderǁ__str____mutmut_1, 
        'xǁHeaderǁ__str____mutmut_2': xǁHeaderǁ__str____mutmut_2, 
        'xǁHeaderǁ__str____mutmut_3': xǁHeaderǁ__str____mutmut_3, 
        'xǁHeaderǁ__str____mutmut_4': xǁHeaderǁ__str____mutmut_4
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁHeaderǁ__str____mutmut_orig)
    xǁHeaderǁ__str____mutmut_orig.__name__ = 'xǁHeaderǁ__str__'



    def xǁHeaderǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁHeaderǁ__repr____mutmut_1(self):
        return str(None)

    xǁHeaderǁ__repr____mutmut_mutants = {
    'xǁHeaderǁ__repr____mutmut_1': xǁHeaderǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁHeaderǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁHeaderǁ__repr____mutmut_orig)
    xǁHeaderǁ__repr____mutmut_orig.__name__ = 'xǁHeaderǁ__repr__'




class HeaderLine:
    """Base class for VCF header lines"""

    def xǁHeaderLineǁ__init____mutmut_orig(self, key: str, value: str):
        #: ``str`` with key of header line
        self.key = key
        # ``str`` with raw value of header line
        self._value = value

    def xǁHeaderLineǁ__init____mutmut_1(self, key: str, value: str):
        #: ``str`` with key of header line
        self.key = None
        # ``str`` with raw value of header line
        self._value = value

    def xǁHeaderLineǁ__init____mutmut_2(self, key: str, value: str):
        #: ``str`` with key of header line
        self.key = key
        # ``str`` with raw value of header line
        self._value = None

    xǁHeaderLineǁ__init____mutmut_mutants = {
    'xǁHeaderLineǁ__init____mutmut_1': xǁHeaderLineǁ__init____mutmut_1, 
        'xǁHeaderLineǁ__init____mutmut_2': xǁHeaderLineǁ__init____mutmut_2
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁHeaderLineǁ__init____mutmut_orig)
    xǁHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁHeaderLineǁ__init__'



    def xǁHeaderLineǁcopy__mutmut_orig(self):
        """Return a copy"""
        return self.__class__(self.key, self.value)

    xǁHeaderLineǁcopy__mutmut_mutants = {

    }

    def copy(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁcopy__mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁcopy__mutmut_mutants"), *args, **kwargs) 

    copy.__signature__ = _mutmut_signature(xǁHeaderLineǁcopy__mutmut_orig)
    xǁHeaderLineǁcopy__mutmut_orig.__name__ = 'xǁHeaderLineǁcopy'



    @property
    def value(self):
        return self._value

    def xǁHeaderLineǁserialize__mutmut_orig(self):
        """Return VCF-serialized version of this header line"""
        return "".join(("##", self.key, "=", self.value))

    def xǁHeaderLineǁserialize__mutmut_1(self):
        """Return VCF-serialized version of this header line"""
        return "XXXX".join(("##", self.key, "=", self.value))

    def xǁHeaderLineǁserialize__mutmut_2(self):
        """Return VCF-serialized version of this header line"""
        return "".join(("XX##XX", self.key, "=", self.value))

    def xǁHeaderLineǁserialize__mutmut_3(self):
        """Return VCF-serialized version of this header line"""
        return "".join(("##", self.key, "XX=XX", self.value))

    xǁHeaderLineǁserialize__mutmut_mutants = {
    'xǁHeaderLineǁserialize__mutmut_1': xǁHeaderLineǁserialize__mutmut_1, 
        'xǁHeaderLineǁserialize__mutmut_2': xǁHeaderLineǁserialize__mutmut_2, 
        'xǁHeaderLineǁserialize__mutmut_3': xǁHeaderLineǁserialize__mutmut_3
    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁHeaderLineǁserialize__mutmut_orig)
    xǁHeaderLineǁserialize__mutmut_orig.__name__ = 'xǁHeaderLineǁserialize'



    def xǁHeaderLineǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value) == (other.key, other.value)
        return NotImplemented  # pragma: no cover

    def xǁHeaderLineǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value) != (other.key, other.value)
        return NotImplemented  # pragma: no cover

    xǁHeaderLineǁ__eq____mutmut_mutants = {
    'xǁHeaderLineǁ__eq____mutmut_1': xǁHeaderLineǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁHeaderLineǁ__eq____mutmut_orig)
    xǁHeaderLineǁ__eq____mutmut_orig.__name__ = 'xǁHeaderLineǁ__eq__'



    def xǁHeaderLineǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value) != (other.key, other.value)
        return NotImplemented  # pragma: no cover

    def xǁHeaderLineǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value) == (other.key, other.value)
        return NotImplemented  # pragma: no cover

    xǁHeaderLineǁ__ne____mutmut_mutants = {
    'xǁHeaderLineǁ__ne____mutmut_1': xǁHeaderLineǁ__ne____mutmut_1
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁHeaderLineǁ__ne____mutmut_orig)
    xǁHeaderLineǁ__ne____mutmut_orig.__name__ = 'xǁHeaderLineǁ__ne__'



    def xǁHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: HeaderLine")

    def xǁHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: HeaderLineXX")

    xǁHeaderLineǁ__hash____mutmut_mutants = {
    'xǁHeaderLineǁ__hash____mutmut_1': xǁHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁHeaderLineǁ__hash____mutmut_orig)
    xǁHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁHeaderLineǁ__hash__'



    def xǁHeaderLineǁ__str____mutmut_orig(self):
        return "HeaderLine({}, {})".format(*map(repr, (self.key, self.value)))

    def xǁHeaderLineǁ__str____mutmut_1(self):
        return "XXHeaderLine({}, {})XX".format(*map(repr, (self.key, self.value)))

    def xǁHeaderLineǁ__str____mutmut_2(self):
        return "HeaderLine({}, {})".format(*map(None, (self.key, self.value)))

    def xǁHeaderLineǁ__str____mutmut_3(self):
        return "HeaderLine({}, {})".format(*map( (self.key, self.value)))

    xǁHeaderLineǁ__str____mutmut_mutants = {
    'xǁHeaderLineǁ__str____mutmut_1': xǁHeaderLineǁ__str____mutmut_1, 
        'xǁHeaderLineǁ__str____mutmut_2': xǁHeaderLineǁ__str____mutmut_2, 
        'xǁHeaderLineǁ__str____mutmut_3': xǁHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁHeaderLineǁ__str____mutmut_orig)
    xǁHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁHeaderLineǁ__str__'



    def xǁHeaderLineǁ__repr____mutmut_orig(self):
        return str(self)

    def xǁHeaderLineǁ__repr____mutmut_1(self):
        return str(None)

    xǁHeaderLineǁ__repr____mutmut_mutants = {
    'xǁHeaderLineǁ__repr____mutmut_1': xǁHeaderLineǁ__repr____mutmut_1
    }

    def __repr__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineǁ__repr____mutmut_mutants"), *args, **kwargs) 

    __repr__.__signature__ = _mutmut_signature(xǁHeaderLineǁ__repr____mutmut_orig)
    xǁHeaderLineǁ__repr____mutmut_orig.__name__ = 'xǁHeaderLineǁ__repr__'




def mapping_to_str__mutmut_orig(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_1(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["XX<XX"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_2(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = None
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_3(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i >= 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_4(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 1:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_5(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append("XX,XX")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_6(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result -= [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_7(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result = [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_8(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "XX=XX", serialize_for_header(key, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_9(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(None, value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_10(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, None)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_11(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header( value)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_12(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key,)]
    result += [">"]
    return "".join(result)


def mapping_to_str__mutmut_13(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result -= [">"]
    return "".join(result)


def mapping_to_str__mutmut_14(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result = [">"]
    return "".join(result)


def mapping_to_str__mutmut_15(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += ["XX>XX"]
    return "".join(result)


def mapping_to_str__mutmut_16(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "XXXX".join(result)


def mapping_to_str__mutmut_17(mapping: dict[str, str]) -> str:
    """Convert mapping to string"""
    result = ["<"]
    for i, (key, value) in enumerate(mapping.items()):
        if i > 0:
            result.append(",")
        result += [key, "=", serialize_for_header(key, value)]
    result += [">"]
    return "".join(None)

mapping_to_str__mutmut_mutants = {
'mapping_to_str__mutmut_1': mapping_to_str__mutmut_1, 
    'mapping_to_str__mutmut_2': mapping_to_str__mutmut_2, 
    'mapping_to_str__mutmut_3': mapping_to_str__mutmut_3, 
    'mapping_to_str__mutmut_4': mapping_to_str__mutmut_4, 
    'mapping_to_str__mutmut_5': mapping_to_str__mutmut_5, 
    'mapping_to_str__mutmut_6': mapping_to_str__mutmut_6, 
    'mapping_to_str__mutmut_7': mapping_to_str__mutmut_7, 
    'mapping_to_str__mutmut_8': mapping_to_str__mutmut_8, 
    'mapping_to_str__mutmut_9': mapping_to_str__mutmut_9, 
    'mapping_to_str__mutmut_10': mapping_to_str__mutmut_10, 
    'mapping_to_str__mutmut_11': mapping_to_str__mutmut_11, 
    'mapping_to_str__mutmut_12': mapping_to_str__mutmut_12, 
    'mapping_to_str__mutmut_13': mapping_to_str__mutmut_13, 
    'mapping_to_str__mutmut_14': mapping_to_str__mutmut_14, 
    'mapping_to_str__mutmut_15': mapping_to_str__mutmut_15, 
    'mapping_to_str__mutmut_16': mapping_to_str__mutmut_16, 
    'mapping_to_str__mutmut_17': mapping_to_str__mutmut_17
}

def mapping_to_str(*args, **kwargs):
    return _mutmut_trampoline(mapping_to_str__mutmut_orig, mapping_to_str__mutmut_mutants, *args, **kwargs) 

mapping_to_str.__signature__ = _mutmut_signature(mapping_to_str__mutmut_orig)
mapping_to_str__mutmut_orig.__name__ = 'mapping_to_str'




class SimpleHeaderLine(HeaderLine):
    """Base class for simple header lines, currently contig and filter
    header lines

    Don't use this class directly but rather the sub classes.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` in
        the case of missing key ``"ID"``
    """

    def xǁSimpleHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key,)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "XXIDXX" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID"  in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('XXMissing key "ID" in header line "{}={}"XX'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(None, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, None))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_10(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format( value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_11(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key,))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(mapping)

    def xǁSimpleHeaderLineǁ__init____mutmut_12(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = dict(None)

    def xǁSimpleHeaderLineǁ__init____mutmut_13(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        # check existence of key "ID"
        if "ID" not in mapping:
            raise exceptions.InvalidHeaderException('Missing key "ID" in header line "{}={}"'.format(key, value))
        #: ``collections.OrderedDict`` with key/value mapping of the attributes
        self.mapping = None

    xǁSimpleHeaderLineǁ__init____mutmut_mutants = {
    'xǁSimpleHeaderLineǁ__init____mutmut_1': xǁSimpleHeaderLineǁ__init____mutmut_1, 
        'xǁSimpleHeaderLineǁ__init____mutmut_2': xǁSimpleHeaderLineǁ__init____mutmut_2, 
        'xǁSimpleHeaderLineǁ__init____mutmut_3': xǁSimpleHeaderLineǁ__init____mutmut_3, 
        'xǁSimpleHeaderLineǁ__init____mutmut_4': xǁSimpleHeaderLineǁ__init____mutmut_4, 
        'xǁSimpleHeaderLineǁ__init____mutmut_5': xǁSimpleHeaderLineǁ__init____mutmut_5, 
        'xǁSimpleHeaderLineǁ__init____mutmut_6': xǁSimpleHeaderLineǁ__init____mutmut_6, 
        'xǁSimpleHeaderLineǁ__init____mutmut_7': xǁSimpleHeaderLineǁ__init____mutmut_7, 
        'xǁSimpleHeaderLineǁ__init____mutmut_8': xǁSimpleHeaderLineǁ__init____mutmut_8, 
        'xǁSimpleHeaderLineǁ__init____mutmut_9': xǁSimpleHeaderLineǁ__init____mutmut_9, 
        'xǁSimpleHeaderLineǁ__init____mutmut_10': xǁSimpleHeaderLineǁ__init____mutmut_10, 
        'xǁSimpleHeaderLineǁ__init____mutmut_11': xǁSimpleHeaderLineǁ__init____mutmut_11, 
        'xǁSimpleHeaderLineǁ__init____mutmut_12': xǁSimpleHeaderLineǁ__init____mutmut_12, 
        'xǁSimpleHeaderLineǁ__init____mutmut_13': xǁSimpleHeaderLineǁ__init____mutmut_13
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSimpleHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁSimpleHeaderLineǁ__init____mutmut_orig)
    xǁSimpleHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁSimpleHeaderLineǁ__init__'



    def xǁSimpleHeaderLineǁcopy__mutmut_orig(self):
        """Return a copy"""
        mapping = dict(self.mapping)
        return self.__class__(self.key, self.value, mapping)

    def xǁSimpleHeaderLineǁcopy__mutmut_1(self):
        """Return a copy"""
        mapping = None
        return self.__class__(self.key, self.value, mapping)

    def xǁSimpleHeaderLineǁcopy__mutmut_2(self):
        """Return a copy"""
        mapping = dict(self.mapping)
        return self.__class__(self.key, self.value, None)

    def xǁSimpleHeaderLineǁcopy__mutmut_3(self):
        """Return a copy"""
        mapping = dict(self.mapping)
        return self.__class__(self.key, self.value,)

    xǁSimpleHeaderLineǁcopy__mutmut_mutants = {
    'xǁSimpleHeaderLineǁcopy__mutmut_1': xǁSimpleHeaderLineǁcopy__mutmut_1, 
        'xǁSimpleHeaderLineǁcopy__mutmut_2': xǁSimpleHeaderLineǁcopy__mutmut_2, 
        'xǁSimpleHeaderLineǁcopy__mutmut_3': xǁSimpleHeaderLineǁcopy__mutmut_3
    }

    def copy(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleHeaderLineǁcopy__mutmut_orig"), object.__getattribute__(self, "xǁSimpleHeaderLineǁcopy__mutmut_mutants"), *args, **kwargs) 

    copy.__signature__ = _mutmut_signature(xǁSimpleHeaderLineǁcopy__mutmut_orig)
    xǁSimpleHeaderLineǁcopy__mutmut_orig.__name__ = 'xǁSimpleHeaderLineǁcopy'



    @property
    def value(self):
        return mapping_to_str(self.mapping)

    def xǁSimpleHeaderLineǁserialize__mutmut_orig(self):
        return "".join(map(str, ["##", self.key, "=", self.value]))

    def xǁSimpleHeaderLineǁserialize__mutmut_1(self):
        return "XXXX".join(map(str, ["##", self.key, "=", self.value]))

    def xǁSimpleHeaderLineǁserialize__mutmut_2(self):
        return "".join(map(None, ["##", self.key, "=", self.value]))

    def xǁSimpleHeaderLineǁserialize__mutmut_3(self):
        return "".join(map(str, ["XX##XX", self.key, "=", self.value]))

    def xǁSimpleHeaderLineǁserialize__mutmut_4(self):
        return "".join(map(str, ["##", self.key, "XX=XX", self.value]))

    def xǁSimpleHeaderLineǁserialize__mutmut_5(self):
        return "".join(map( ["##", self.key, "=", self.value]))

    xǁSimpleHeaderLineǁserialize__mutmut_mutants = {
    'xǁSimpleHeaderLineǁserialize__mutmut_1': xǁSimpleHeaderLineǁserialize__mutmut_1, 
        'xǁSimpleHeaderLineǁserialize__mutmut_2': xǁSimpleHeaderLineǁserialize__mutmut_2, 
        'xǁSimpleHeaderLineǁserialize__mutmut_3': xǁSimpleHeaderLineǁserialize__mutmut_3, 
        'xǁSimpleHeaderLineǁserialize__mutmut_4': xǁSimpleHeaderLineǁserialize__mutmut_4, 
        'xǁSimpleHeaderLineǁserialize__mutmut_5': xǁSimpleHeaderLineǁserialize__mutmut_5
    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleHeaderLineǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁSimpleHeaderLineǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁSimpleHeaderLineǁserialize__mutmut_orig)
    xǁSimpleHeaderLineǁserialize__mutmut_orig.__name__ = 'xǁSimpleHeaderLineǁserialize'



    def xǁSimpleHeaderLineǁ__str____mutmut_orig(self):
        return "SimpleHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁSimpleHeaderLineǁ__str____mutmut_1(self):
        return "XXSimpleHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁSimpleHeaderLineǁ__str____mutmut_2(self):
        return "SimpleHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁSimpleHeaderLineǁ__str____mutmut_3(self):
        return "SimpleHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁSimpleHeaderLineǁ__str____mutmut_mutants = {
    'xǁSimpleHeaderLineǁ__str____mutmut_1': xǁSimpleHeaderLineǁ__str____mutmut_1, 
        'xǁSimpleHeaderLineǁ__str____mutmut_2': xǁSimpleHeaderLineǁ__str____mutmut_2, 
        'xǁSimpleHeaderLineǁ__str____mutmut_3': xǁSimpleHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSimpleHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁSimpleHeaderLineǁ__str____mutmut_orig)
    xǁSimpleHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁSimpleHeaderLineǁ__str__'



    def xǁSimpleHeaderLineǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) == (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    def xǁSimpleHeaderLineǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) != (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    xǁSimpleHeaderLineǁ__eq____mutmut_mutants = {
    'xǁSimpleHeaderLineǁ__eq____mutmut_1': xǁSimpleHeaderLineǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleHeaderLineǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁSimpleHeaderLineǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁSimpleHeaderLineǁ__eq____mutmut_orig)
    xǁSimpleHeaderLineǁ__eq____mutmut_orig.__name__ = 'xǁSimpleHeaderLineǁ__eq__'



    def xǁSimpleHeaderLineǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) != (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    def xǁSimpleHeaderLineǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) == (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    xǁSimpleHeaderLineǁ__ne____mutmut_mutants = {
    'xǁSimpleHeaderLineǁ__ne____mutmut_1': xǁSimpleHeaderLineǁ__ne____mutmut_1
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleHeaderLineǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁSimpleHeaderLineǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁSimpleHeaderLineǁ__ne____mutmut_orig)
    xǁSimpleHeaderLineǁ__ne____mutmut_orig.__name__ = 'xǁSimpleHeaderLineǁ__ne__'




class AltAlleleHeaderLine(SimpleHeaderLine):
    """Alternative allele header line

    Mostly used for defining symbolic alleles for structural variants and
    IUPAC ambiguity codes
    """

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "AltAlleleHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return AltAlleleHeaderLine("ALT", mapping_to_str(mapping), mapping)

    def xǁAltAlleleHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["XXIDXX"]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping[None]

    def xǁAltAlleleHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = None

    xǁAltAlleleHeaderLineǁ__init____mutmut_mutants = {
    'xǁAltAlleleHeaderLineǁ__init____mutmut_1': xǁAltAlleleHeaderLineǁ__init____mutmut_1, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_2': xǁAltAlleleHeaderLineǁ__init____mutmut_2, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_3': xǁAltAlleleHeaderLineǁ__init____mutmut_3, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_4': xǁAltAlleleHeaderLineǁ__init____mutmut_4, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_5': xǁAltAlleleHeaderLineǁ__init____mutmut_5, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_6': xǁAltAlleleHeaderLineǁ__init____mutmut_6, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_7': xǁAltAlleleHeaderLineǁ__init____mutmut_7, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_8': xǁAltAlleleHeaderLineǁ__init____mutmut_8, 
        'xǁAltAlleleHeaderLineǁ__init____mutmut_9': xǁAltAlleleHeaderLineǁ__init____mutmut_9
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltAlleleHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAltAlleleHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁAltAlleleHeaderLineǁ__init____mutmut_orig)
    xǁAltAlleleHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁAltAlleleHeaderLineǁ__init__'



    def xǁAltAlleleHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: AltAlleleHeaderLine")

    def xǁAltAlleleHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: AltAlleleHeaderLineXX")

    xǁAltAlleleHeaderLineǁ__hash____mutmut_mutants = {
    'xǁAltAlleleHeaderLineǁ__hash____mutmut_1': xǁAltAlleleHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltAlleleHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁAltAlleleHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁAltAlleleHeaderLineǁ__hash____mutmut_orig)
    xǁAltAlleleHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁAltAlleleHeaderLineǁ__hash__'



    def xǁAltAlleleHeaderLineǁ__str____mutmut_orig(self):
        return "AltAlleleHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁAltAlleleHeaderLineǁ__str____mutmut_1(self):
        return "XXAltAlleleHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁAltAlleleHeaderLineǁ__str____mutmut_2(self):
        return "AltAlleleHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁAltAlleleHeaderLineǁ__str____mutmut_3(self):
        return "AltAlleleHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁAltAlleleHeaderLineǁ__str____mutmut_mutants = {
    'xǁAltAlleleHeaderLineǁ__str____mutmut_1': xǁAltAlleleHeaderLineǁ__str____mutmut_1, 
        'xǁAltAlleleHeaderLineǁ__str____mutmut_2': xǁAltAlleleHeaderLineǁ__str____mutmut_2, 
        'xǁAltAlleleHeaderLineǁ__str____mutmut_3': xǁAltAlleleHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAltAlleleHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁAltAlleleHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁAltAlleleHeaderLineǁ__str____mutmut_orig)
    xǁAltAlleleHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁAltAlleleHeaderLineǁ__str__'




class ContigHeaderLine(SimpleHeaderLine):
    """Contig header line

    Most importantly, parses the ``'length'`` key into an integer
    """

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "ContigHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return ContigHeaderLine("contig", mapping_to_str(mapping), mapping)

    def xǁContigHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "XXlengthXX" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" not in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["XXlengthXX"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_10(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping[None] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_11(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["XXlengthXX"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_12(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping[None])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_13(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = None
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_14(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'XXField "length" not found in header line {}={}XX'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_15(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(None, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_16(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, None),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_17(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format( value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_18(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key,),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_19(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                None,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_20(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_21(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["XXIDXX"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_22(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping[None]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_23(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = None
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("length")

    def xǁContigHeaderLineǁ__init____mutmut_24(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = self.mapping.get("XXlengthXX")

    def xǁContigHeaderLineǁ__init____mutmut_25(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # convert 'length' entry to integer if possible
        if "length" in self.mapping:
            mapping["length"] = int(mapping["length"])
        else:
            warnings.warn(
                'Field "length" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: name of the contig
        self.id = self.mapping["ID"]
        #: length of the contig, ``None`` if missing
        self.length = None

    xǁContigHeaderLineǁ__init____mutmut_mutants = {
    'xǁContigHeaderLineǁ__init____mutmut_1': xǁContigHeaderLineǁ__init____mutmut_1, 
        'xǁContigHeaderLineǁ__init____mutmut_2': xǁContigHeaderLineǁ__init____mutmut_2, 
        'xǁContigHeaderLineǁ__init____mutmut_3': xǁContigHeaderLineǁ__init____mutmut_3, 
        'xǁContigHeaderLineǁ__init____mutmut_4': xǁContigHeaderLineǁ__init____mutmut_4, 
        'xǁContigHeaderLineǁ__init____mutmut_5': xǁContigHeaderLineǁ__init____mutmut_5, 
        'xǁContigHeaderLineǁ__init____mutmut_6': xǁContigHeaderLineǁ__init____mutmut_6, 
        'xǁContigHeaderLineǁ__init____mutmut_7': xǁContigHeaderLineǁ__init____mutmut_7, 
        'xǁContigHeaderLineǁ__init____mutmut_8': xǁContigHeaderLineǁ__init____mutmut_8, 
        'xǁContigHeaderLineǁ__init____mutmut_9': xǁContigHeaderLineǁ__init____mutmut_9, 
        'xǁContigHeaderLineǁ__init____mutmut_10': xǁContigHeaderLineǁ__init____mutmut_10, 
        'xǁContigHeaderLineǁ__init____mutmut_11': xǁContigHeaderLineǁ__init____mutmut_11, 
        'xǁContigHeaderLineǁ__init____mutmut_12': xǁContigHeaderLineǁ__init____mutmut_12, 
        'xǁContigHeaderLineǁ__init____mutmut_13': xǁContigHeaderLineǁ__init____mutmut_13, 
        'xǁContigHeaderLineǁ__init____mutmut_14': xǁContigHeaderLineǁ__init____mutmut_14, 
        'xǁContigHeaderLineǁ__init____mutmut_15': xǁContigHeaderLineǁ__init____mutmut_15, 
        'xǁContigHeaderLineǁ__init____mutmut_16': xǁContigHeaderLineǁ__init____mutmut_16, 
        'xǁContigHeaderLineǁ__init____mutmut_17': xǁContigHeaderLineǁ__init____mutmut_17, 
        'xǁContigHeaderLineǁ__init____mutmut_18': xǁContigHeaderLineǁ__init____mutmut_18, 
        'xǁContigHeaderLineǁ__init____mutmut_19': xǁContigHeaderLineǁ__init____mutmut_19, 
        'xǁContigHeaderLineǁ__init____mutmut_20': xǁContigHeaderLineǁ__init____mutmut_20, 
        'xǁContigHeaderLineǁ__init____mutmut_21': xǁContigHeaderLineǁ__init____mutmut_21, 
        'xǁContigHeaderLineǁ__init____mutmut_22': xǁContigHeaderLineǁ__init____mutmut_22, 
        'xǁContigHeaderLineǁ__init____mutmut_23': xǁContigHeaderLineǁ__init____mutmut_23, 
        'xǁContigHeaderLineǁ__init____mutmut_24': xǁContigHeaderLineǁ__init____mutmut_24, 
        'xǁContigHeaderLineǁ__init____mutmut_25': xǁContigHeaderLineǁ__init____mutmut_25
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁContigHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁContigHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁContigHeaderLineǁ__init____mutmut_orig)
    xǁContigHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁContigHeaderLineǁ__init__'



    def xǁContigHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: ContigHeaderLine")

    def xǁContigHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: ContigHeaderLineXX")

    xǁContigHeaderLineǁ__hash____mutmut_mutants = {
    'xǁContigHeaderLineǁ__hash____mutmut_1': xǁContigHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁContigHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁContigHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁContigHeaderLineǁ__hash____mutmut_orig)
    xǁContigHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁContigHeaderLineǁ__hash__'



    def xǁContigHeaderLineǁ__str____mutmut_orig(self):
        return "ContigHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁContigHeaderLineǁ__str____mutmut_1(self):
        return "XXContigHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁContigHeaderLineǁ__str____mutmut_2(self):
        return "ContigHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁContigHeaderLineǁ__str____mutmut_3(self):
        return "ContigHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁContigHeaderLineǁ__str____mutmut_mutants = {
    'xǁContigHeaderLineǁ__str____mutmut_1': xǁContigHeaderLineǁ__str____mutmut_1, 
        'xǁContigHeaderLineǁ__str____mutmut_2': xǁContigHeaderLineǁ__str____mutmut_2, 
        'xǁContigHeaderLineǁ__str____mutmut_3': xǁContigHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁContigHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁContigHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁContigHeaderLineǁ__str____mutmut_orig)
    xǁContigHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁContigHeaderLineǁ__str__'




class FilterHeaderLine(SimpleHeaderLine):
    """FILTER header line"""

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "FilterHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return FilterHeaderLine("FILTER", mapping_to_str(mapping), mapping)

    def xǁFilterHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "XXDescriptionXX" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description"  in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'XXField "Description" not found in header line {}={}XX'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_10(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(None, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_11(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, None),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_12(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format( value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_13(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key,),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_14(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                None,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_15(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_16(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["XXIDXX"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_17(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping[None]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_18(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = None
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("Description")

    def xǁFilterHeaderLineǁ__init____mutmut_19(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = self.mapping.get("XXDescriptionXX")

    def xǁFilterHeaderLineǁ__init____mutmut_20(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        # check for "Description" key
        if "Description" not in self.mapping:  # pragma: no cover
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                FieldInfoNotFound,
            )
        #: token for the filter
        self.id = self.mapping["ID"]
        #: description for the filter, ``None`` if missing
        self.description = None

    xǁFilterHeaderLineǁ__init____mutmut_mutants = {
    'xǁFilterHeaderLineǁ__init____mutmut_1': xǁFilterHeaderLineǁ__init____mutmut_1, 
        'xǁFilterHeaderLineǁ__init____mutmut_2': xǁFilterHeaderLineǁ__init____mutmut_2, 
        'xǁFilterHeaderLineǁ__init____mutmut_3': xǁFilterHeaderLineǁ__init____mutmut_3, 
        'xǁFilterHeaderLineǁ__init____mutmut_4': xǁFilterHeaderLineǁ__init____mutmut_4, 
        'xǁFilterHeaderLineǁ__init____mutmut_5': xǁFilterHeaderLineǁ__init____mutmut_5, 
        'xǁFilterHeaderLineǁ__init____mutmut_6': xǁFilterHeaderLineǁ__init____mutmut_6, 
        'xǁFilterHeaderLineǁ__init____mutmut_7': xǁFilterHeaderLineǁ__init____mutmut_7, 
        'xǁFilterHeaderLineǁ__init____mutmut_8': xǁFilterHeaderLineǁ__init____mutmut_8, 
        'xǁFilterHeaderLineǁ__init____mutmut_9': xǁFilterHeaderLineǁ__init____mutmut_9, 
        'xǁFilterHeaderLineǁ__init____mutmut_10': xǁFilterHeaderLineǁ__init____mutmut_10, 
        'xǁFilterHeaderLineǁ__init____mutmut_11': xǁFilterHeaderLineǁ__init____mutmut_11, 
        'xǁFilterHeaderLineǁ__init____mutmut_12': xǁFilterHeaderLineǁ__init____mutmut_12, 
        'xǁFilterHeaderLineǁ__init____mutmut_13': xǁFilterHeaderLineǁ__init____mutmut_13, 
        'xǁFilterHeaderLineǁ__init____mutmut_14': xǁFilterHeaderLineǁ__init____mutmut_14, 
        'xǁFilterHeaderLineǁ__init____mutmut_15': xǁFilterHeaderLineǁ__init____mutmut_15, 
        'xǁFilterHeaderLineǁ__init____mutmut_16': xǁFilterHeaderLineǁ__init____mutmut_16, 
        'xǁFilterHeaderLineǁ__init____mutmut_17': xǁFilterHeaderLineǁ__init____mutmut_17, 
        'xǁFilterHeaderLineǁ__init____mutmut_18': xǁFilterHeaderLineǁ__init____mutmut_18, 
        'xǁFilterHeaderLineǁ__init____mutmut_19': xǁFilterHeaderLineǁ__init____mutmut_19, 
        'xǁFilterHeaderLineǁ__init____mutmut_20': xǁFilterHeaderLineǁ__init____mutmut_20
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFilterHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFilterHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁFilterHeaderLineǁ__init____mutmut_orig)
    xǁFilterHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁFilterHeaderLineǁ__init__'



    def xǁFilterHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: FilterHeaderLine")

    def xǁFilterHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: FilterHeaderLineXX")

    xǁFilterHeaderLineǁ__hash____mutmut_mutants = {
    'xǁFilterHeaderLineǁ__hash____mutmut_1': xǁFilterHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFilterHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁFilterHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁFilterHeaderLineǁ__hash____mutmut_orig)
    xǁFilterHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁFilterHeaderLineǁ__hash__'



    def xǁFilterHeaderLineǁ__str____mutmut_orig(self):
        return "FilterHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁFilterHeaderLineǁ__str____mutmut_1(self):
        return "XXFilterHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁFilterHeaderLineǁ__str____mutmut_2(self):
        return "FilterHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁFilterHeaderLineǁ__str____mutmut_3(self):
        return "FilterHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁFilterHeaderLineǁ__str____mutmut_mutants = {
    'xǁFilterHeaderLineǁ__str____mutmut_1': xǁFilterHeaderLineǁ__str____mutmut_1, 
        'xǁFilterHeaderLineǁ__str____mutmut_2': xǁFilterHeaderLineǁ__str____mutmut_2, 
        'xǁFilterHeaderLineǁ__str____mutmut_3': xǁFilterHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFilterHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁFilterHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁFilterHeaderLineǁ__str____mutmut_orig)
    xǁFilterHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁFilterHeaderLineǁ__str__'




class MetaHeaderLine(SimpleHeaderLine):
    """Alternative allele header line

    Used for defining set of valid values for samples keys
    """

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "MetaHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return MetaHeaderLine("META", mapping_to_str(mapping), mapping)

    def xǁMetaHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁMetaHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["XXIDXX"]

    def xǁMetaHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping[None]

    def xǁMetaHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = None

    xǁMetaHeaderLineǁ__init____mutmut_mutants = {
    'xǁMetaHeaderLineǁ__init____mutmut_1': xǁMetaHeaderLineǁ__init____mutmut_1, 
        'xǁMetaHeaderLineǁ__init____mutmut_2': xǁMetaHeaderLineǁ__init____mutmut_2, 
        'xǁMetaHeaderLineǁ__init____mutmut_3': xǁMetaHeaderLineǁ__init____mutmut_3, 
        'xǁMetaHeaderLineǁ__init____mutmut_4': xǁMetaHeaderLineǁ__init____mutmut_4, 
        'xǁMetaHeaderLineǁ__init____mutmut_5': xǁMetaHeaderLineǁ__init____mutmut_5, 
        'xǁMetaHeaderLineǁ__init____mutmut_6': xǁMetaHeaderLineǁ__init____mutmut_6, 
        'xǁMetaHeaderLineǁ__init____mutmut_7': xǁMetaHeaderLineǁ__init____mutmut_7, 
        'xǁMetaHeaderLineǁ__init____mutmut_8': xǁMetaHeaderLineǁ__init____mutmut_8, 
        'xǁMetaHeaderLineǁ__init____mutmut_9': xǁMetaHeaderLineǁ__init____mutmut_9
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁMetaHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁMetaHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁMetaHeaderLineǁ__init____mutmut_orig)
    xǁMetaHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁMetaHeaderLineǁ__init__'



    def xǁMetaHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: MetaHeaderLine")

    def xǁMetaHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: MetaHeaderLineXX")

    xǁMetaHeaderLineǁ__hash____mutmut_mutants = {
    'xǁMetaHeaderLineǁ__hash____mutmut_1': xǁMetaHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁMetaHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁMetaHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁMetaHeaderLineǁ__hash____mutmut_orig)
    xǁMetaHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁMetaHeaderLineǁ__hash__'



    def xǁMetaHeaderLineǁ__str____mutmut_orig(self):
        return "MetaHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁMetaHeaderLineǁ__str____mutmut_1(self):
        return "XXMetaHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁMetaHeaderLineǁ__str____mutmut_2(self):
        return "MetaHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁMetaHeaderLineǁ__str____mutmut_3(self):
        return "MetaHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁMetaHeaderLineǁ__str____mutmut_mutants = {
    'xǁMetaHeaderLineǁ__str____mutmut_1': xǁMetaHeaderLineǁ__str____mutmut_1, 
        'xǁMetaHeaderLineǁ__str____mutmut_2': xǁMetaHeaderLineǁ__str____mutmut_2, 
        'xǁMetaHeaderLineǁ__str____mutmut_3': xǁMetaHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁMetaHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁMetaHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁMetaHeaderLineǁ__str____mutmut_orig)
    xǁMetaHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁMetaHeaderLineǁ__str__'




class PedigreeHeaderLine(SimpleHeaderLine):
    """Header line for defining a pedigree entry"""

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "PedigreeHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return PedigreeHeaderLine("PEDIGREE", mapping_to_str(mapping), mapping)

    def xǁPedigreeHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["XXIDXX"]

    def xǁPedigreeHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping[None]

    def xǁPedigreeHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = None

    xǁPedigreeHeaderLineǁ__init____mutmut_mutants = {
    'xǁPedigreeHeaderLineǁ__init____mutmut_1': xǁPedigreeHeaderLineǁ__init____mutmut_1, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_2': xǁPedigreeHeaderLineǁ__init____mutmut_2, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_3': xǁPedigreeHeaderLineǁ__init____mutmut_3, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_4': xǁPedigreeHeaderLineǁ__init____mutmut_4, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_5': xǁPedigreeHeaderLineǁ__init____mutmut_5, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_6': xǁPedigreeHeaderLineǁ__init____mutmut_6, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_7': xǁPedigreeHeaderLineǁ__init____mutmut_7, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_8': xǁPedigreeHeaderLineǁ__init____mutmut_8, 
        'xǁPedigreeHeaderLineǁ__init____mutmut_9': xǁPedigreeHeaderLineǁ__init____mutmut_9
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁPedigreeHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPedigreeHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁPedigreeHeaderLineǁ__init____mutmut_orig)
    xǁPedigreeHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁPedigreeHeaderLineǁ__init__'



    def xǁPedigreeHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: PedigreeHeaderLine")

    def xǁPedigreeHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: PedigreeHeaderLineXX")

    xǁPedigreeHeaderLineǁ__hash____mutmut_mutants = {
    'xǁPedigreeHeaderLineǁ__hash____mutmut_1': xǁPedigreeHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁPedigreeHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁPedigreeHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁPedigreeHeaderLineǁ__hash____mutmut_orig)
    xǁPedigreeHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁPedigreeHeaderLineǁ__hash__'



    def xǁPedigreeHeaderLineǁ__str____mutmut_orig(self):
        return "PedigreeHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁPedigreeHeaderLineǁ__str____mutmut_1(self):
        return "XXPedigreeHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁPedigreeHeaderLineǁ__str____mutmut_2(self):
        return "PedigreeHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁPedigreeHeaderLineǁ__str____mutmut_3(self):
        return "PedigreeHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁPedigreeHeaderLineǁ__str____mutmut_mutants = {
    'xǁPedigreeHeaderLineǁ__str____mutmut_1': xǁPedigreeHeaderLineǁ__str____mutmut_1, 
        'xǁPedigreeHeaderLineǁ__str____mutmut_2': xǁPedigreeHeaderLineǁ__str____mutmut_2, 
        'xǁPedigreeHeaderLineǁ__str____mutmut_3': xǁPedigreeHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁPedigreeHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁPedigreeHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁPedigreeHeaderLineǁ__str____mutmut_orig)
    xǁPedigreeHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁPedigreeHeaderLineǁ__str__'




class SampleHeaderLine(SimpleHeaderLine):
    """Header line for defining a SAMPLE entry"""

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "SampleHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return SampleHeaderLine("SAMPLE", mapping_to_str(mapping), mapping)

    def xǁSampleHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        #: name of the alternative allele
        self.id = self.mapping["ID"]

    def xǁSampleHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping["XXIDXX"]

    def xǁSampleHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = self.mapping[None]

    def xǁSampleHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: name of the alternative allele
        self.id = None

    xǁSampleHeaderLineǁ__init____mutmut_mutants = {
    'xǁSampleHeaderLineǁ__init____mutmut_1': xǁSampleHeaderLineǁ__init____mutmut_1, 
        'xǁSampleHeaderLineǁ__init____mutmut_2': xǁSampleHeaderLineǁ__init____mutmut_2, 
        'xǁSampleHeaderLineǁ__init____mutmut_3': xǁSampleHeaderLineǁ__init____mutmut_3, 
        'xǁSampleHeaderLineǁ__init____mutmut_4': xǁSampleHeaderLineǁ__init____mutmut_4, 
        'xǁSampleHeaderLineǁ__init____mutmut_5': xǁSampleHeaderLineǁ__init____mutmut_5, 
        'xǁSampleHeaderLineǁ__init____mutmut_6': xǁSampleHeaderLineǁ__init____mutmut_6, 
        'xǁSampleHeaderLineǁ__init____mutmut_7': xǁSampleHeaderLineǁ__init____mutmut_7, 
        'xǁSampleHeaderLineǁ__init____mutmut_8': xǁSampleHeaderLineǁ__init____mutmut_8, 
        'xǁSampleHeaderLineǁ__init____mutmut_9': xǁSampleHeaderLineǁ__init____mutmut_9
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSampleHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSampleHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁSampleHeaderLineǁ__init____mutmut_orig)
    xǁSampleHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁSampleHeaderLineǁ__init__'



    def xǁSampleHeaderLineǁ__eq____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) == (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    def xǁSampleHeaderLineǁ__eq____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) != (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    xǁSampleHeaderLineǁ__eq____mutmut_mutants = {
    'xǁSampleHeaderLineǁ__eq____mutmut_1': xǁSampleHeaderLineǁ__eq____mutmut_1
    }

    def __eq__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSampleHeaderLineǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁSampleHeaderLineǁ__eq____mutmut_mutants"), *args, **kwargs) 

    __eq__.__signature__ = _mutmut_signature(xǁSampleHeaderLineǁ__eq____mutmut_orig)
    xǁSampleHeaderLineǁ__eq____mutmut_orig.__name__ = 'xǁSampleHeaderLineǁ__eq__'



    def xǁSampleHeaderLineǁ__ne____mutmut_orig(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) != (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    def xǁSampleHeaderLineǁ__ne____mutmut_1(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return (self.key, self.value, self.mapping) == (other.key, other.value, other.mapping)
        return NotImplemented  # pragma: no cover

    xǁSampleHeaderLineǁ__ne____mutmut_mutants = {
    'xǁSampleHeaderLineǁ__ne____mutmut_1': xǁSampleHeaderLineǁ__ne____mutmut_1
    }

    def __ne__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSampleHeaderLineǁ__ne____mutmut_orig"), object.__getattribute__(self, "xǁSampleHeaderLineǁ__ne____mutmut_mutants"), *args, **kwargs) 

    __ne__.__signature__ = _mutmut_signature(xǁSampleHeaderLineǁ__ne____mutmut_orig)
    xǁSampleHeaderLineǁ__ne____mutmut_orig.__name__ = 'xǁSampleHeaderLineǁ__ne__'



    def xǁSampleHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: SampleHeaderLine")

    def xǁSampleHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: SampleHeaderLineXX")

    xǁSampleHeaderLineǁ__hash____mutmut_mutants = {
    'xǁSampleHeaderLineǁ__hash____mutmut_1': xǁSampleHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSampleHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁSampleHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁSampleHeaderLineǁ__hash____mutmut_orig)
    xǁSampleHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁSampleHeaderLineǁ__hash__'



    def xǁSampleHeaderLineǁ__str____mutmut_orig(self):
        return "SampleHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁSampleHeaderLineǁ__str____mutmut_1(self):
        return "XXSampleHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁSampleHeaderLineǁ__str____mutmut_2(self):
        return "SampleHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁSampleHeaderLineǁ__str____mutmut_3(self):
        return "SampleHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁSampleHeaderLineǁ__str____mutmut_mutants = {
    'xǁSampleHeaderLineǁ__str____mutmut_1': xǁSampleHeaderLineǁ__str____mutmut_1, 
        'xǁSampleHeaderLineǁ__str____mutmut_2': xǁSampleHeaderLineǁ__str____mutmut_2, 
        'xǁSampleHeaderLineǁ__str____mutmut_3': xǁSampleHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁSampleHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁSampleHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁSampleHeaderLineǁ__str____mutmut_orig)
    xǁSampleHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁSampleHeaderLineǁ__str__'




class CompoundHeaderLine(HeaderLine):
    """Base class for compound header lines, currently format and header lines

    Compound header lines describe fields that can have more than one entry.

    Don't use this class directly but rather the sub classes.
    """

    def xǁCompoundHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key,)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(None)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = None
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "XXNumberXX" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number"  in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('XX[vcfpy] WARNING: missing number, using unbounded/"." insteadXX', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_10(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', None)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_11(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead',)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_12(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["XXNumberXX"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_13(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping[None] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_14(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "XX.XX"
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_15(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = None
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_16(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["XXNumberXX"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_17(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping[None] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_18(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["XXNumberXX"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_19(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping[None])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_20(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = None
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_21(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('XX[vcfpy] WARNING: invalid number {}, using unbounded/"." insteadXX').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_22(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["XXNumberXX"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_23(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping[None]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_24(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                None,
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_25(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
            )
            self.mapping["Number"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_26(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["XXNumberXX"] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_27(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping[None] = "."

    def xǁCompoundHeaderLineǁ__init____mutmut_28(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = "XX.XX"

    def xǁCompoundHeaderLineǁ__init____mutmut_29(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value)
        #: OrderedDict with key/value mapping
        self.mapping = dict(mapping)
        # check that 'Number' is given and use "." otherwise
        if "Number" not in self.mapping:  # pragma: no cover
            warnings.warn('[vcfpy] WARNING: missing number, using unbounded/"." instead', FieldMissingNumber)
            self.mapping["Number"] = "."
        try:
            self.mapping["Number"] = self._parse_number(self.mapping["Number"])
        except ValueError:
            warnings.warn(
                ('[vcfpy] WARNING: invalid number {}, using unbounded/"." instead').format(self.mapping["Number"]),
                FieldInvalidNumber,
            )
            self.mapping["Number"] = None

    xǁCompoundHeaderLineǁ__init____mutmut_mutants = {
    'xǁCompoundHeaderLineǁ__init____mutmut_1': xǁCompoundHeaderLineǁ__init____mutmut_1, 
        'xǁCompoundHeaderLineǁ__init____mutmut_2': xǁCompoundHeaderLineǁ__init____mutmut_2, 
        'xǁCompoundHeaderLineǁ__init____mutmut_3': xǁCompoundHeaderLineǁ__init____mutmut_3, 
        'xǁCompoundHeaderLineǁ__init____mutmut_4': xǁCompoundHeaderLineǁ__init____mutmut_4, 
        'xǁCompoundHeaderLineǁ__init____mutmut_5': xǁCompoundHeaderLineǁ__init____mutmut_5, 
        'xǁCompoundHeaderLineǁ__init____mutmut_6': xǁCompoundHeaderLineǁ__init____mutmut_6, 
        'xǁCompoundHeaderLineǁ__init____mutmut_7': xǁCompoundHeaderLineǁ__init____mutmut_7, 
        'xǁCompoundHeaderLineǁ__init____mutmut_8': xǁCompoundHeaderLineǁ__init____mutmut_8, 
        'xǁCompoundHeaderLineǁ__init____mutmut_9': xǁCompoundHeaderLineǁ__init____mutmut_9, 
        'xǁCompoundHeaderLineǁ__init____mutmut_10': xǁCompoundHeaderLineǁ__init____mutmut_10, 
        'xǁCompoundHeaderLineǁ__init____mutmut_11': xǁCompoundHeaderLineǁ__init____mutmut_11, 
        'xǁCompoundHeaderLineǁ__init____mutmut_12': xǁCompoundHeaderLineǁ__init____mutmut_12, 
        'xǁCompoundHeaderLineǁ__init____mutmut_13': xǁCompoundHeaderLineǁ__init____mutmut_13, 
        'xǁCompoundHeaderLineǁ__init____mutmut_14': xǁCompoundHeaderLineǁ__init____mutmut_14, 
        'xǁCompoundHeaderLineǁ__init____mutmut_15': xǁCompoundHeaderLineǁ__init____mutmut_15, 
        'xǁCompoundHeaderLineǁ__init____mutmut_16': xǁCompoundHeaderLineǁ__init____mutmut_16, 
        'xǁCompoundHeaderLineǁ__init____mutmut_17': xǁCompoundHeaderLineǁ__init____mutmut_17, 
        'xǁCompoundHeaderLineǁ__init____mutmut_18': xǁCompoundHeaderLineǁ__init____mutmut_18, 
        'xǁCompoundHeaderLineǁ__init____mutmut_19': xǁCompoundHeaderLineǁ__init____mutmut_19, 
        'xǁCompoundHeaderLineǁ__init____mutmut_20': xǁCompoundHeaderLineǁ__init____mutmut_20, 
        'xǁCompoundHeaderLineǁ__init____mutmut_21': xǁCompoundHeaderLineǁ__init____mutmut_21, 
        'xǁCompoundHeaderLineǁ__init____mutmut_22': xǁCompoundHeaderLineǁ__init____mutmut_22, 
        'xǁCompoundHeaderLineǁ__init____mutmut_23': xǁCompoundHeaderLineǁ__init____mutmut_23, 
        'xǁCompoundHeaderLineǁ__init____mutmut_24': xǁCompoundHeaderLineǁ__init____mutmut_24, 
        'xǁCompoundHeaderLineǁ__init____mutmut_25': xǁCompoundHeaderLineǁ__init____mutmut_25, 
        'xǁCompoundHeaderLineǁ__init____mutmut_26': xǁCompoundHeaderLineǁ__init____mutmut_26, 
        'xǁCompoundHeaderLineǁ__init____mutmut_27': xǁCompoundHeaderLineǁ__init____mutmut_27, 
        'xǁCompoundHeaderLineǁ__init____mutmut_28': xǁCompoundHeaderLineǁ__init____mutmut_28, 
        'xǁCompoundHeaderLineǁ__init____mutmut_29': xǁCompoundHeaderLineǁ__init____mutmut_29
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCompoundHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCompoundHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁCompoundHeaderLineǁ__init____mutmut_orig)
    xǁCompoundHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁCompoundHeaderLineǁ__init__'



    def xǁCompoundHeaderLineǁcopy__mutmut_orig(self):
        """Return a copy"""
        return self.__class__(self.key, self.value, dict(self.mapping))

    xǁCompoundHeaderLineǁcopy__mutmut_mutants = {

    }

    def copy(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCompoundHeaderLineǁcopy__mutmut_orig"), object.__getattribute__(self, "xǁCompoundHeaderLineǁcopy__mutmut_mutants"), *args, **kwargs) 

    copy.__signature__ = _mutmut_signature(xǁCompoundHeaderLineǁcopy__mutmut_orig)
    xǁCompoundHeaderLineǁcopy__mutmut_orig.__name__ = 'xǁCompoundHeaderLineǁcopy'



    @classmethod
    def _parse_number(cls, number: str | int | float) -> int | Literal["A", "R", "G", "."]:
        """Parse ``number`` into an ``int`` or return ``number`` if a valid
        expression for a INFO/FORMAT "Number".

        :param str number: ``str`` to parse and check
        """
        try:
            return int(number)
        except ValueError as e:
            if number in VALID_NUMBERS:
                return number
            else:
                raise e

    @property
    def value(self):
        return mapping_to_str(self.mapping)

    def xǁCompoundHeaderLineǁserialize__mutmut_orig(self):
        return "".join(map(str, ["##", self.key, "=", self.value]))

    def xǁCompoundHeaderLineǁserialize__mutmut_1(self):
        return "XXXX".join(map(str, ["##", self.key, "=", self.value]))

    def xǁCompoundHeaderLineǁserialize__mutmut_2(self):
        return "".join(map(None, ["##", self.key, "=", self.value]))

    def xǁCompoundHeaderLineǁserialize__mutmut_3(self):
        return "".join(map(str, ["XX##XX", self.key, "=", self.value]))

    def xǁCompoundHeaderLineǁserialize__mutmut_4(self):
        return "".join(map(str, ["##", self.key, "XX=XX", self.value]))

    def xǁCompoundHeaderLineǁserialize__mutmut_5(self):
        return "".join(map( ["##", self.key, "=", self.value]))

    xǁCompoundHeaderLineǁserialize__mutmut_mutants = {
    'xǁCompoundHeaderLineǁserialize__mutmut_1': xǁCompoundHeaderLineǁserialize__mutmut_1, 
        'xǁCompoundHeaderLineǁserialize__mutmut_2': xǁCompoundHeaderLineǁserialize__mutmut_2, 
        'xǁCompoundHeaderLineǁserialize__mutmut_3': xǁCompoundHeaderLineǁserialize__mutmut_3, 
        'xǁCompoundHeaderLineǁserialize__mutmut_4': xǁCompoundHeaderLineǁserialize__mutmut_4, 
        'xǁCompoundHeaderLineǁserialize__mutmut_5': xǁCompoundHeaderLineǁserialize__mutmut_5
    }

    def serialize(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCompoundHeaderLineǁserialize__mutmut_orig"), object.__getattribute__(self, "xǁCompoundHeaderLineǁserialize__mutmut_mutants"), *args, **kwargs) 

    serialize.__signature__ = _mutmut_signature(xǁCompoundHeaderLineǁserialize__mutmut_orig)
    xǁCompoundHeaderLineǁserialize__mutmut_orig.__name__ = 'xǁCompoundHeaderLineǁserialize'



    def xǁCompoundHeaderLineǁ__str____mutmut_orig(self):
        return "CompoundHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁCompoundHeaderLineǁ__str____mutmut_1(self):
        return "XXCompoundHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁCompoundHeaderLineǁ__str____mutmut_2(self):
        return "CompoundHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁCompoundHeaderLineǁ__str____mutmut_3(self):
        return "CompoundHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁCompoundHeaderLineǁ__str____mutmut_mutants = {
    'xǁCompoundHeaderLineǁ__str____mutmut_1': xǁCompoundHeaderLineǁ__str____mutmut_1, 
        'xǁCompoundHeaderLineǁ__str____mutmut_2': xǁCompoundHeaderLineǁ__str____mutmut_2, 
        'xǁCompoundHeaderLineǁ__str____mutmut_3': xǁCompoundHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁCompoundHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁCompoundHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁCompoundHeaderLineǁ__str____mutmut_orig)
    xǁCompoundHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁCompoundHeaderLineǁ__str__'




class InfoHeaderLine(CompoundHeaderLine):
    """Header line for INFO fields

    Note that the ``Number`` field will be parsed into an ``int`` if
    possible.  Otherwise, the constants ``HEADER_NUMBER_*`` will be used.
    """

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "InfoHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return InfoHeaderLine("INFO", mapping_to_str(mapping), mapping)

    def xǁInfoHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["XXIDXX"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping[None]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = None
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_10(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["XXNumberXX"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_11(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping[None]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_12(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = None
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_13(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("XXTypeXX")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_14(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = None
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_15(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "XXTypeXX" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_16(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type"  in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_17(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('XXField "Type" not found in header line, using String instead {}={}XX').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_18(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(None, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_19(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, None),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_20(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format( value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_21(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key,),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_22(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                None,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_23(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_24(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "XXStringXX"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_25(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = None
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_26(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "XXTypeXX" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_27(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" not in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_28(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_  in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_29(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping or type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_30(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("XXInvalid INFO value type {} in header line, using String instead, {}={}XX").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_31(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["XXTypeXX"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_32(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping[None], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_33(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], None, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_34(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, None
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_35(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_36(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key,
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_37(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                None,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_38(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_39(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "XXStringXX"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_40(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = None
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_41(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = None
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_42(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "XXDescriptionXX" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_43(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description"  in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_44(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'XXField "Description" not found in header line {}={}XX'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_45(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(None, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_46(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, None),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_47(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format( value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_48(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key,),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_49(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                None,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_50(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_51(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("XXDescriptionXX")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_52(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = None
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_53(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("XXSourceXX")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_54(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = None
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁInfoHeaderLineǁ__init____mutmut_55(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("XXVersionXX")

    def xǁInfoHeaderLineǁ__init____mutmut_56(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in INFO_TYPES:
            warnings.warn(
                ("Invalid INFO value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = None

    xǁInfoHeaderLineǁ__init____mutmut_mutants = {
    'xǁInfoHeaderLineǁ__init____mutmut_1': xǁInfoHeaderLineǁ__init____mutmut_1, 
        'xǁInfoHeaderLineǁ__init____mutmut_2': xǁInfoHeaderLineǁ__init____mutmut_2, 
        'xǁInfoHeaderLineǁ__init____mutmut_3': xǁInfoHeaderLineǁ__init____mutmut_3, 
        'xǁInfoHeaderLineǁ__init____mutmut_4': xǁInfoHeaderLineǁ__init____mutmut_4, 
        'xǁInfoHeaderLineǁ__init____mutmut_5': xǁInfoHeaderLineǁ__init____mutmut_5, 
        'xǁInfoHeaderLineǁ__init____mutmut_6': xǁInfoHeaderLineǁ__init____mutmut_6, 
        'xǁInfoHeaderLineǁ__init____mutmut_7': xǁInfoHeaderLineǁ__init____mutmut_7, 
        'xǁInfoHeaderLineǁ__init____mutmut_8': xǁInfoHeaderLineǁ__init____mutmut_8, 
        'xǁInfoHeaderLineǁ__init____mutmut_9': xǁInfoHeaderLineǁ__init____mutmut_9, 
        'xǁInfoHeaderLineǁ__init____mutmut_10': xǁInfoHeaderLineǁ__init____mutmut_10, 
        'xǁInfoHeaderLineǁ__init____mutmut_11': xǁInfoHeaderLineǁ__init____mutmut_11, 
        'xǁInfoHeaderLineǁ__init____mutmut_12': xǁInfoHeaderLineǁ__init____mutmut_12, 
        'xǁInfoHeaderLineǁ__init____mutmut_13': xǁInfoHeaderLineǁ__init____mutmut_13, 
        'xǁInfoHeaderLineǁ__init____mutmut_14': xǁInfoHeaderLineǁ__init____mutmut_14, 
        'xǁInfoHeaderLineǁ__init____mutmut_15': xǁInfoHeaderLineǁ__init____mutmut_15, 
        'xǁInfoHeaderLineǁ__init____mutmut_16': xǁInfoHeaderLineǁ__init____mutmut_16, 
        'xǁInfoHeaderLineǁ__init____mutmut_17': xǁInfoHeaderLineǁ__init____mutmut_17, 
        'xǁInfoHeaderLineǁ__init____mutmut_18': xǁInfoHeaderLineǁ__init____mutmut_18, 
        'xǁInfoHeaderLineǁ__init____mutmut_19': xǁInfoHeaderLineǁ__init____mutmut_19, 
        'xǁInfoHeaderLineǁ__init____mutmut_20': xǁInfoHeaderLineǁ__init____mutmut_20, 
        'xǁInfoHeaderLineǁ__init____mutmut_21': xǁInfoHeaderLineǁ__init____mutmut_21, 
        'xǁInfoHeaderLineǁ__init____mutmut_22': xǁInfoHeaderLineǁ__init____mutmut_22, 
        'xǁInfoHeaderLineǁ__init____mutmut_23': xǁInfoHeaderLineǁ__init____mutmut_23, 
        'xǁInfoHeaderLineǁ__init____mutmut_24': xǁInfoHeaderLineǁ__init____mutmut_24, 
        'xǁInfoHeaderLineǁ__init____mutmut_25': xǁInfoHeaderLineǁ__init____mutmut_25, 
        'xǁInfoHeaderLineǁ__init____mutmut_26': xǁInfoHeaderLineǁ__init____mutmut_26, 
        'xǁInfoHeaderLineǁ__init____mutmut_27': xǁInfoHeaderLineǁ__init____mutmut_27, 
        'xǁInfoHeaderLineǁ__init____mutmut_28': xǁInfoHeaderLineǁ__init____mutmut_28, 
        'xǁInfoHeaderLineǁ__init____mutmut_29': xǁInfoHeaderLineǁ__init____mutmut_29, 
        'xǁInfoHeaderLineǁ__init____mutmut_30': xǁInfoHeaderLineǁ__init____mutmut_30, 
        'xǁInfoHeaderLineǁ__init____mutmut_31': xǁInfoHeaderLineǁ__init____mutmut_31, 
        'xǁInfoHeaderLineǁ__init____mutmut_32': xǁInfoHeaderLineǁ__init____mutmut_32, 
        'xǁInfoHeaderLineǁ__init____mutmut_33': xǁInfoHeaderLineǁ__init____mutmut_33, 
        'xǁInfoHeaderLineǁ__init____mutmut_34': xǁInfoHeaderLineǁ__init____mutmut_34, 
        'xǁInfoHeaderLineǁ__init____mutmut_35': xǁInfoHeaderLineǁ__init____mutmut_35, 
        'xǁInfoHeaderLineǁ__init____mutmut_36': xǁInfoHeaderLineǁ__init____mutmut_36, 
        'xǁInfoHeaderLineǁ__init____mutmut_37': xǁInfoHeaderLineǁ__init____mutmut_37, 
        'xǁInfoHeaderLineǁ__init____mutmut_38': xǁInfoHeaderLineǁ__init____mutmut_38, 
        'xǁInfoHeaderLineǁ__init____mutmut_39': xǁInfoHeaderLineǁ__init____mutmut_39, 
        'xǁInfoHeaderLineǁ__init____mutmut_40': xǁInfoHeaderLineǁ__init____mutmut_40, 
        'xǁInfoHeaderLineǁ__init____mutmut_41': xǁInfoHeaderLineǁ__init____mutmut_41, 
        'xǁInfoHeaderLineǁ__init____mutmut_42': xǁInfoHeaderLineǁ__init____mutmut_42, 
        'xǁInfoHeaderLineǁ__init____mutmut_43': xǁInfoHeaderLineǁ__init____mutmut_43, 
        'xǁInfoHeaderLineǁ__init____mutmut_44': xǁInfoHeaderLineǁ__init____mutmut_44, 
        'xǁInfoHeaderLineǁ__init____mutmut_45': xǁInfoHeaderLineǁ__init____mutmut_45, 
        'xǁInfoHeaderLineǁ__init____mutmut_46': xǁInfoHeaderLineǁ__init____mutmut_46, 
        'xǁInfoHeaderLineǁ__init____mutmut_47': xǁInfoHeaderLineǁ__init____mutmut_47, 
        'xǁInfoHeaderLineǁ__init____mutmut_48': xǁInfoHeaderLineǁ__init____mutmut_48, 
        'xǁInfoHeaderLineǁ__init____mutmut_49': xǁInfoHeaderLineǁ__init____mutmut_49, 
        'xǁInfoHeaderLineǁ__init____mutmut_50': xǁInfoHeaderLineǁ__init____mutmut_50, 
        'xǁInfoHeaderLineǁ__init____mutmut_51': xǁInfoHeaderLineǁ__init____mutmut_51, 
        'xǁInfoHeaderLineǁ__init____mutmut_52': xǁInfoHeaderLineǁ__init____mutmut_52, 
        'xǁInfoHeaderLineǁ__init____mutmut_53': xǁInfoHeaderLineǁ__init____mutmut_53, 
        'xǁInfoHeaderLineǁ__init____mutmut_54': xǁInfoHeaderLineǁ__init____mutmut_54, 
        'xǁInfoHeaderLineǁ__init____mutmut_55': xǁInfoHeaderLineǁ__init____mutmut_55, 
        'xǁInfoHeaderLineǁ__init____mutmut_56': xǁInfoHeaderLineǁ__init____mutmut_56
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁInfoHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInfoHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁInfoHeaderLineǁ__init____mutmut_orig)
    xǁInfoHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁInfoHeaderLineǁ__init__'



    def xǁInfoHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: InfoHeaderLine")

    def xǁInfoHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: InfoHeaderLineXX")

    xǁInfoHeaderLineǁ__hash____mutmut_mutants = {
    'xǁInfoHeaderLineǁ__hash____mutmut_1': xǁInfoHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁInfoHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁInfoHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁInfoHeaderLineǁ__hash____mutmut_orig)
    xǁInfoHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁInfoHeaderLineǁ__hash__'



    def xǁInfoHeaderLineǁ__str____mutmut_orig(self):
        return "InfoHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁInfoHeaderLineǁ__str____mutmut_1(self):
        return "XXInfoHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁInfoHeaderLineǁ__str____mutmut_2(self):
        return "InfoHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁInfoHeaderLineǁ__str____mutmut_3(self):
        return "InfoHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁInfoHeaderLineǁ__str____mutmut_mutants = {
    'xǁInfoHeaderLineǁ__str____mutmut_1': xǁInfoHeaderLineǁ__str____mutmut_1, 
        'xǁInfoHeaderLineǁ__str____mutmut_2': xǁInfoHeaderLineǁ__str____mutmut_2, 
        'xǁInfoHeaderLineǁ__str____mutmut_3': xǁInfoHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁInfoHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁInfoHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁInfoHeaderLineǁ__str____mutmut_orig)
    xǁInfoHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁInfoHeaderLineǁ__str__'




class FormatHeaderLine(CompoundHeaderLine):
    """Header line for FORMAT fields"""

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "FormatHeaderLine":
        """Construct from mapping, not requiring the string value"""
        return FormatHeaderLine("FORMAT", mapping_to_str(mapping), mapping)

    def xǁFormatHeaderLineǁ__init____mutmut_orig(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_1(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(None, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_2(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, None, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_3(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, None)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_4(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__( value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_5(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_6(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value,)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_7(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["XXIDXX"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_8(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping[None]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_9(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = None
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_10(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["XXNumberXX"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_11(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping[None]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_12(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = None
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_13(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("XXTypeXX")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_14(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = None
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_15(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "XXTypeXX" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_16(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type"  in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_17(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('XXField "Type" not found in header line, using String instead {}={}XX').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_18(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(None, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_19(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, None),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_20(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format( value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_21(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key,),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_22(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                None,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_23(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_24(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "XXStringXX"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_25(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = None
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_26(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "XXTypeXX" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_27(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" not in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_28(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_  in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_29(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping or type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_30(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("XXInvalid FORMAT value type {} in header line, using String instead, {}={}XX").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_31(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["XXTypeXX"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_32(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping[None], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_33(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], None, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_34(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, None
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_35(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_36(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key,
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_37(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                None,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_38(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_39(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "XXStringXX"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_40(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = None
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_41(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = None
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_42(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "XXDescriptionXX" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_43(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description"  in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_44(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'XXField "Description" not found in header line {}={}XX'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_45(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(None, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_46(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, None),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_47(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format( value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_48(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key,),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_49(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                None,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_50(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_51(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("XXDescriptionXX")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_52(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = None
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_53(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("XXSourceXX")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_54(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = None
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("Version")

    def xǁFormatHeaderLineǁ__init____mutmut_55(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = self.mapping.get("XXVersionXX")

    def xǁFormatHeaderLineǁ__init____mutmut_56(self, key: str, value: str, mapping: dict[str, Any]):
        super().__init__(key, value, mapping)
        #: key in the INFO field
        self.id = self.mapping["ID"]
        # check for "Number" field
        self.number = self.mapping["Number"]
        # check for "Type" field
        type_ = self.mapping.get("Type")
        if "Type" not in self.mapping:
            warnings.warn(
                ('Field "Type" not found in header line, using String instead {}={}').format(key, value),
                HeaderInvalidType,
            )
            type_ = "String"
        if "Type" in self.mapping and type_ not in FORMAT_TYPES:
            warnings.warn(
                ("Invalid FORMAT value type {} in header line, using String instead, {}={}").format(
                    self.mapping["Type"], key, value
                ),
                HeaderInvalidType,
            )
            type_ = "String"
        #: value type
        self.type = type_
        # check for "Description" key
        if "Description" not in self.mapping:
            warnings.warn(
                'Field "Description" not found in header line {}={}'.format(key, value),
                HeaderMissingDescription,
            )
        #: description, should be given, ``None`` if not given
        self.description = self.mapping.get("Description")
        #: source of INFO field, ``None`` if not given
        self.source = self.mapping.get("Source")
        #: version of INFO field, ``None`` if not given
        self.version = None

    xǁFormatHeaderLineǁ__init____mutmut_mutants = {
    'xǁFormatHeaderLineǁ__init____mutmut_1': xǁFormatHeaderLineǁ__init____mutmut_1, 
        'xǁFormatHeaderLineǁ__init____mutmut_2': xǁFormatHeaderLineǁ__init____mutmut_2, 
        'xǁFormatHeaderLineǁ__init____mutmut_3': xǁFormatHeaderLineǁ__init____mutmut_3, 
        'xǁFormatHeaderLineǁ__init____mutmut_4': xǁFormatHeaderLineǁ__init____mutmut_4, 
        'xǁFormatHeaderLineǁ__init____mutmut_5': xǁFormatHeaderLineǁ__init____mutmut_5, 
        'xǁFormatHeaderLineǁ__init____mutmut_6': xǁFormatHeaderLineǁ__init____mutmut_6, 
        'xǁFormatHeaderLineǁ__init____mutmut_7': xǁFormatHeaderLineǁ__init____mutmut_7, 
        'xǁFormatHeaderLineǁ__init____mutmut_8': xǁFormatHeaderLineǁ__init____mutmut_8, 
        'xǁFormatHeaderLineǁ__init____mutmut_9': xǁFormatHeaderLineǁ__init____mutmut_9, 
        'xǁFormatHeaderLineǁ__init____mutmut_10': xǁFormatHeaderLineǁ__init____mutmut_10, 
        'xǁFormatHeaderLineǁ__init____mutmut_11': xǁFormatHeaderLineǁ__init____mutmut_11, 
        'xǁFormatHeaderLineǁ__init____mutmut_12': xǁFormatHeaderLineǁ__init____mutmut_12, 
        'xǁFormatHeaderLineǁ__init____mutmut_13': xǁFormatHeaderLineǁ__init____mutmut_13, 
        'xǁFormatHeaderLineǁ__init____mutmut_14': xǁFormatHeaderLineǁ__init____mutmut_14, 
        'xǁFormatHeaderLineǁ__init____mutmut_15': xǁFormatHeaderLineǁ__init____mutmut_15, 
        'xǁFormatHeaderLineǁ__init____mutmut_16': xǁFormatHeaderLineǁ__init____mutmut_16, 
        'xǁFormatHeaderLineǁ__init____mutmut_17': xǁFormatHeaderLineǁ__init____mutmut_17, 
        'xǁFormatHeaderLineǁ__init____mutmut_18': xǁFormatHeaderLineǁ__init____mutmut_18, 
        'xǁFormatHeaderLineǁ__init____mutmut_19': xǁFormatHeaderLineǁ__init____mutmut_19, 
        'xǁFormatHeaderLineǁ__init____mutmut_20': xǁFormatHeaderLineǁ__init____mutmut_20, 
        'xǁFormatHeaderLineǁ__init____mutmut_21': xǁFormatHeaderLineǁ__init____mutmut_21, 
        'xǁFormatHeaderLineǁ__init____mutmut_22': xǁFormatHeaderLineǁ__init____mutmut_22, 
        'xǁFormatHeaderLineǁ__init____mutmut_23': xǁFormatHeaderLineǁ__init____mutmut_23, 
        'xǁFormatHeaderLineǁ__init____mutmut_24': xǁFormatHeaderLineǁ__init____mutmut_24, 
        'xǁFormatHeaderLineǁ__init____mutmut_25': xǁFormatHeaderLineǁ__init____mutmut_25, 
        'xǁFormatHeaderLineǁ__init____mutmut_26': xǁFormatHeaderLineǁ__init____mutmut_26, 
        'xǁFormatHeaderLineǁ__init____mutmut_27': xǁFormatHeaderLineǁ__init____mutmut_27, 
        'xǁFormatHeaderLineǁ__init____mutmut_28': xǁFormatHeaderLineǁ__init____mutmut_28, 
        'xǁFormatHeaderLineǁ__init____mutmut_29': xǁFormatHeaderLineǁ__init____mutmut_29, 
        'xǁFormatHeaderLineǁ__init____mutmut_30': xǁFormatHeaderLineǁ__init____mutmut_30, 
        'xǁFormatHeaderLineǁ__init____mutmut_31': xǁFormatHeaderLineǁ__init____mutmut_31, 
        'xǁFormatHeaderLineǁ__init____mutmut_32': xǁFormatHeaderLineǁ__init____mutmut_32, 
        'xǁFormatHeaderLineǁ__init____mutmut_33': xǁFormatHeaderLineǁ__init____mutmut_33, 
        'xǁFormatHeaderLineǁ__init____mutmut_34': xǁFormatHeaderLineǁ__init____mutmut_34, 
        'xǁFormatHeaderLineǁ__init____mutmut_35': xǁFormatHeaderLineǁ__init____mutmut_35, 
        'xǁFormatHeaderLineǁ__init____mutmut_36': xǁFormatHeaderLineǁ__init____mutmut_36, 
        'xǁFormatHeaderLineǁ__init____mutmut_37': xǁFormatHeaderLineǁ__init____mutmut_37, 
        'xǁFormatHeaderLineǁ__init____mutmut_38': xǁFormatHeaderLineǁ__init____mutmut_38, 
        'xǁFormatHeaderLineǁ__init____mutmut_39': xǁFormatHeaderLineǁ__init____mutmut_39, 
        'xǁFormatHeaderLineǁ__init____mutmut_40': xǁFormatHeaderLineǁ__init____mutmut_40, 
        'xǁFormatHeaderLineǁ__init____mutmut_41': xǁFormatHeaderLineǁ__init____mutmut_41, 
        'xǁFormatHeaderLineǁ__init____mutmut_42': xǁFormatHeaderLineǁ__init____mutmut_42, 
        'xǁFormatHeaderLineǁ__init____mutmut_43': xǁFormatHeaderLineǁ__init____mutmut_43, 
        'xǁFormatHeaderLineǁ__init____mutmut_44': xǁFormatHeaderLineǁ__init____mutmut_44, 
        'xǁFormatHeaderLineǁ__init____mutmut_45': xǁFormatHeaderLineǁ__init____mutmut_45, 
        'xǁFormatHeaderLineǁ__init____mutmut_46': xǁFormatHeaderLineǁ__init____mutmut_46, 
        'xǁFormatHeaderLineǁ__init____mutmut_47': xǁFormatHeaderLineǁ__init____mutmut_47, 
        'xǁFormatHeaderLineǁ__init____mutmut_48': xǁFormatHeaderLineǁ__init____mutmut_48, 
        'xǁFormatHeaderLineǁ__init____mutmut_49': xǁFormatHeaderLineǁ__init____mutmut_49, 
        'xǁFormatHeaderLineǁ__init____mutmut_50': xǁFormatHeaderLineǁ__init____mutmut_50, 
        'xǁFormatHeaderLineǁ__init____mutmut_51': xǁFormatHeaderLineǁ__init____mutmut_51, 
        'xǁFormatHeaderLineǁ__init____mutmut_52': xǁFormatHeaderLineǁ__init____mutmut_52, 
        'xǁFormatHeaderLineǁ__init____mutmut_53': xǁFormatHeaderLineǁ__init____mutmut_53, 
        'xǁFormatHeaderLineǁ__init____mutmut_54': xǁFormatHeaderLineǁ__init____mutmut_54, 
        'xǁFormatHeaderLineǁ__init____mutmut_55': xǁFormatHeaderLineǁ__init____mutmut_55, 
        'xǁFormatHeaderLineǁ__init____mutmut_56': xǁFormatHeaderLineǁ__init____mutmut_56
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFormatHeaderLineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFormatHeaderLineǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁFormatHeaderLineǁ__init____mutmut_orig)
    xǁFormatHeaderLineǁ__init____mutmut_orig.__name__ = 'xǁFormatHeaderLineǁ__init__'



    def xǁFormatHeaderLineǁ__hash____mutmut_orig(self):
        raise TypeError("Unhashable type: FormatHeaderLine")

    def xǁFormatHeaderLineǁ__hash____mutmut_1(self):
        raise TypeError("XXUnhashable type: FormatHeaderLineXX")

    xǁFormatHeaderLineǁ__hash____mutmut_mutants = {
    'xǁFormatHeaderLineǁ__hash____mutmut_1': xǁFormatHeaderLineǁ__hash____mutmut_1
    }

    def __hash__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFormatHeaderLineǁ__hash____mutmut_orig"), object.__getattribute__(self, "xǁFormatHeaderLineǁ__hash____mutmut_mutants"), *args, **kwargs) 

    __hash__.__signature__ = _mutmut_signature(xǁFormatHeaderLineǁ__hash____mutmut_orig)
    xǁFormatHeaderLineǁ__hash____mutmut_orig.__name__ = 'xǁFormatHeaderLineǁ__hash__'



    def xǁFormatHeaderLineǁ__str____mutmut_orig(self):
        return "FormatHeaderLine({}, {}, {})".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁFormatHeaderLineǁ__str____mutmut_1(self):
        return "XXFormatHeaderLine({}, {}, {})XX".format(*map(repr, (self.key, self.value, self.mapping)))

    def xǁFormatHeaderLineǁ__str____mutmut_2(self):
        return "FormatHeaderLine({}, {}, {})".format(*map(None, (self.key, self.value, self.mapping)))

    def xǁFormatHeaderLineǁ__str____mutmut_3(self):
        return "FormatHeaderLine({}, {}, {})".format(*map( (self.key, self.value, self.mapping)))

    xǁFormatHeaderLineǁ__str____mutmut_mutants = {
    'xǁFormatHeaderLineǁ__str____mutmut_1': xǁFormatHeaderLineǁ__str____mutmut_1, 
        'xǁFormatHeaderLineǁ__str____mutmut_2': xǁFormatHeaderLineǁ__str____mutmut_2, 
        'xǁFormatHeaderLineǁ__str____mutmut_3': xǁFormatHeaderLineǁ__str____mutmut_3
    }

    def __str__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFormatHeaderLineǁ__str____mutmut_orig"), object.__getattribute__(self, "xǁFormatHeaderLineǁ__str____mutmut_mutants"), *args, **kwargs) 

    __str__.__signature__ = _mutmut_signature(xǁFormatHeaderLineǁ__str____mutmut_orig)
    xǁFormatHeaderLineǁ__str____mutmut_orig.__name__ = 'xǁFormatHeaderLineǁ__str__'


