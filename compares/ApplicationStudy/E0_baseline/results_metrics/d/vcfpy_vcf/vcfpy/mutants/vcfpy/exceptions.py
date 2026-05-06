
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
"""Exceptions for the vcfpy module"""

__author__ = "Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>"


class VCFPyException(RuntimeError):
    """Base class for module's exception"""


class InvalidHeaderException(VCFPyException):
    """Raised in the case of invalid header formatting"""


class InvalidRecordException(VCFPyException):
    """Raised in the case of invalid record formatting"""


class IncorrectVCFFormat(VCFPyException):
    """Raised on problems parsing VCF"""


class HeaderNotFound(VCFPyException):
    """Raised when a VCF header could not be found"""


class VCFPyWarning(Warning):
    """Base class for module's warnings"""


class DuplicateHeaderLineWarning(VCFPyWarning):
    """A header line occurs twice in a header"""


class FieldInfoNotFound(VCFPyWarning):
    """A header field is not found, default is used"""


class FieldMissingNumber(VCFPyWarning):
    """Raised when compound heade misses number"""


class FieldInvalidNumber(VCFPyWarning):
    """Raised when compound header has invalid number"""


class HeaderInvalidType(VCFPyWarning):
    """Raised when compound header has invalid type"""


class HeaderMissingDescription(VCFPyWarning):
    """Raised when compound header has missing description"""


class LeadingTrailingSpaceInKey(VCFPyWarning):
    """Leading or trailing space in key"""


class UnknownFilter(VCFPyWarning):
    """Missing FILTER"""


class UnknownVCFVersion(VCFPyWarning):
    """Unknown VCF version"""


class IncorrectListLength(VCFPyWarning):
    """Wrong length of multi-element field"""


class SpaceInChromLine(VCFPyWarning):
    """Space instead of TAB in ##CHROM line"""


class CannotConvertValue(VCFPyWarning):
    """Cannot convert value."""


class CannotModifyUnparsedCallWarning(VCFPyWarning):
    """Cannot modify unparsed call instance."""
