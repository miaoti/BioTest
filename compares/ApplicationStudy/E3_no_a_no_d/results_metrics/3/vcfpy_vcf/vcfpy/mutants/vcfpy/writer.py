
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
"""Writing of VCF files to ``file``-like objects

Currently, only writing to plain-text files is supported
"""

import pathlib
import typing
from typing import IO, Any, Literal, cast

from vcfpy import bgzf, parser, record
from vcfpy.header import FieldInfo, Header

__author__ = "Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>"


def format_atomic__mutmut_orig(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, v)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_1(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r not in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, v)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_2(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[None]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, v)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_3(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(None, v)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_4(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, None)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_5(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace( v)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_6(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k,)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_7(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = None
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_8(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, v)
    # String-format the given value
    if value is not None:
        return "."
    else:
        return str(value)


def format_atomic__mutmut_9(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, v)
    # String-format the given value
    if value is None:
        return "XX.XX"
    else:
        return str(value)


def format_atomic__mutmut_10(value: Any | None, section: Literal["INFO", "FORMAT"]) -> str:
    """Format atomic value

    This function also takes care of escaping the value in case one of the
    reserved characters occurs in the value.
    """
    # Perform escaping
    if isinstance(value, str):
        if any(r in value for r in record.RESERVED_CHARS[section]):
            for k, v in record.ESCAPE_MAPPING:
                value = value.replace(k, v)
    # String-format the given value
    if value is None:
        return "."
    else:
        return str(None)

format_atomic__mutmut_mutants = {
'format_atomic__mutmut_1': format_atomic__mutmut_1, 
    'format_atomic__mutmut_2': format_atomic__mutmut_2, 
    'format_atomic__mutmut_3': format_atomic__mutmut_3, 
    'format_atomic__mutmut_4': format_atomic__mutmut_4, 
    'format_atomic__mutmut_5': format_atomic__mutmut_5, 
    'format_atomic__mutmut_6': format_atomic__mutmut_6, 
    'format_atomic__mutmut_7': format_atomic__mutmut_7, 
    'format_atomic__mutmut_8': format_atomic__mutmut_8, 
    'format_atomic__mutmut_9': format_atomic__mutmut_9, 
    'format_atomic__mutmut_10': format_atomic__mutmut_10
}

def format_atomic(*args, **kwargs):
    return _mutmut_trampoline(format_atomic__mutmut_orig, format_atomic__mutmut_mutants, *args, **kwargs) 

format_atomic.__signature__ = _mutmut_signature(format_atomic__mutmut_orig)
format_atomic__mutmut_orig.__name__ = 'format_atomic'




def format_value__mutmut_orig(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_1(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section != "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_2(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "XXFORMATXX" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_3(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id not in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_4(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("XXFORMAT/FTXX", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_5(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "XXFTXX"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_6(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" or field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_7(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if  value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_8(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "XX.XX"
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_9(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return "XX;XX".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_10(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(None, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_11(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, None) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_12(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic( section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_13(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x,) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_14(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number != 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_15(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 2:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_16(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is not None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_17(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "XX.XX"
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_18(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(None, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_19(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, None)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_20(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic( section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_21(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value,)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_22(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(None) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_23(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is  list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_24(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("XXExpected list value for field with Number != 1XX")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_25(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if  value:
            return "."
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_26(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "XX.XX"
        else:
            return ",".join((format_atomic(x, section) for x in value))


def format_value__mutmut_27(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return "XX,XX".join((format_atomic(x, section) for x in value))


def format_value__mutmut_28(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(None, section) for x in value))


def format_value__mutmut_29(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x, None) for x in value))


def format_value__mutmut_30(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic( section) for x in value))


def format_value__mutmut_31(
    field_info: FieldInfo, value: str | None | int | bool | float | list[Any], section: Literal["INFO", "FORMAT"]
):
    """Format possibly compound value given the FieldInfo"""
    if section == "FORMAT" and field_info.id in ("FORMAT/FT", "FT"):
        if not value:
            return "."
        elif isinstance(value, list):
            return ";".join((format_atomic(x, section) for x in value))
    elif field_info.number == 1:
        if value is None:
            return "."
        else:
            return format_atomic(value, section)
    else:
        if type(value) is not list:  # pragma: no cover
            raise ValueError("Expected list value for field with Number != 1")
        if not value:
            return "."
        else:
            return ",".join((format_atomic(x,) for x in value))

format_value__mutmut_mutants = {
'format_value__mutmut_1': format_value__mutmut_1, 
    'format_value__mutmut_2': format_value__mutmut_2, 
    'format_value__mutmut_3': format_value__mutmut_3, 
    'format_value__mutmut_4': format_value__mutmut_4, 
    'format_value__mutmut_5': format_value__mutmut_5, 
    'format_value__mutmut_6': format_value__mutmut_6, 
    'format_value__mutmut_7': format_value__mutmut_7, 
    'format_value__mutmut_8': format_value__mutmut_8, 
    'format_value__mutmut_9': format_value__mutmut_9, 
    'format_value__mutmut_10': format_value__mutmut_10, 
    'format_value__mutmut_11': format_value__mutmut_11, 
    'format_value__mutmut_12': format_value__mutmut_12, 
    'format_value__mutmut_13': format_value__mutmut_13, 
    'format_value__mutmut_14': format_value__mutmut_14, 
    'format_value__mutmut_15': format_value__mutmut_15, 
    'format_value__mutmut_16': format_value__mutmut_16, 
    'format_value__mutmut_17': format_value__mutmut_17, 
    'format_value__mutmut_18': format_value__mutmut_18, 
    'format_value__mutmut_19': format_value__mutmut_19, 
    'format_value__mutmut_20': format_value__mutmut_20, 
    'format_value__mutmut_21': format_value__mutmut_21, 
    'format_value__mutmut_22': format_value__mutmut_22, 
    'format_value__mutmut_23': format_value__mutmut_23, 
    'format_value__mutmut_24': format_value__mutmut_24, 
    'format_value__mutmut_25': format_value__mutmut_25, 
    'format_value__mutmut_26': format_value__mutmut_26, 
    'format_value__mutmut_27': format_value__mutmut_27, 
    'format_value__mutmut_28': format_value__mutmut_28, 
    'format_value__mutmut_29': format_value__mutmut_29, 
    'format_value__mutmut_30': format_value__mutmut_30, 
    'format_value__mutmut_31': format_value__mutmut_31
}

def format_value(*args, **kwargs):
    return _mutmut_trampoline(format_value__mutmut_orig, format_value__mutmut_mutants, *args, **kwargs) 

format_value.__signature__ = _mutmut_signature(format_value__mutmut_orig)
format_value__mutmut_orig.__name__ = 'format_value'




class Writer:
    """Class for writing VCF files to ``file``-like objects

    Instead of using the constructor, use the class methods
    :py:meth:`~Writer.from_stream` and
    :py:meth:`~Writer.from_path`.

    The writer has to be constructed with a :py:class:`~vcfpy.header.Header`
    object and the full VCF header will be written immediately on construction.
    This, of course, implies that modifying the header after construction is
    illegal.
    """

    @classmethod
    def from_stream(
        cls,
        stream: IO[str] | IO[bytes],
        header: Header,
        path: pathlib.Path | str | None = None,
        use_bgzf: bool | None = None,
    ):
        """Create new :py:class:`Writer` from file

        Note that for getting bgzf support, you have to pass in a stream
        opened in binary mode.  Further, you either have to provide a ``path``
        ending in ``".gz"`` or set ``use_bgzf=True``.  Otherwise, you will
        get the notorious "TypeError: 'str' does not support the buffer
        interface".

        :param stream: ``file``-like object to write to
        :param header: VCF header to use, lines and samples are deep-copied
        :param path: optional string with path to store (for display only)
        :param use_bgzf: indicator whether to write bgzf to ``stream``
            if ``True``, prevent if ``False``, interpret ``path`` if ``None``
        """
        path = str(path)
        if use_bgzf or (use_bgzf is None and path and path.endswith(".gz")):
            stream_b = cast(IO[bytes], stream)
            stream_: IO[str] = bgzf.BgzfWriter(fileobj=stream_b)
        else:
            stream_ = cast(IO[str], stream)
        return Writer(stream_, header, path)

    @classmethod
    def from_path(cls, path: pathlib.Path | str, header: Header):
        """Create new :py:class:`Writer` from path

        :param path: the path to load from (converted to ``str`` for
            compatibility with ``path.py``)
        :param header: VCF header to use, lines and samples are deep-copied
        """
        path = str(path)
        use_bgzf = False  # we already interpret path
        if path.endswith(".gz"):
            f = bgzf.BgzfWriter(filename=path)
        else:
            f = open(path, "wt")
        return cls.from_stream(f, header, path, use_bgzf=use_bgzf)

    def xǁWriterǁ__init____mutmut_orig(self, stream: IO[str], header: Header, path: pathlib.Path | str | None = None):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: the :py:class:~vcfpy.header.Header` to write out, will be
        #: deep-copied into the ``Writer`` on initialization
        self.header = header.copy()
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        # write out headers
        self._write_header()

    def xǁWriterǁ__init____mutmut_1(self, stream: IO[str], header: Header, path: pathlib.Path | str | None = None):
        #: stream (``file``-like object) to read from
        self.stream = None
        #: the :py:class:~vcfpy.header.Header` to write out, will be
        #: deep-copied into the ``Writer`` on initialization
        self.header = header.copy()
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        # write out headers
        self._write_header()

    def xǁWriterǁ__init____mutmut_2(self, stream: IO[str], header: Header, path: pathlib.Path | str | None = None):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: the :py:class:~vcfpy.header.Header` to write out, will be
        #: deep-copied into the ``Writer`` on initialization
        self.header = None
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        # write out headers
        self._write_header()

    def xǁWriterǁ__init____mutmut_3(self, stream: IO[str], header: Header, path: pathlib.Path | str | None = None):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: the :py:class:~vcfpy.header.Header` to write out, will be
        #: deep-copied into the ``Writer`` on initialization
        self.header = header.copy()
        #: optional ``str`` with the path to the stream
        self.path = None if path is not None else str(path)
        # write out headers
        self._write_header()

    def xǁWriterǁ__init____mutmut_4(self, stream: IO[str], header: Header, path: pathlib.Path | str | None = None):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: the :py:class:~vcfpy.header.Header` to write out, will be
        #: deep-copied into the ``Writer`` on initialization
        self.header = header.copy()
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(None)
        # write out headers
        self._write_header()

    def xǁWriterǁ__init____mutmut_5(self, stream: IO[str], header: Header, path: pathlib.Path | str | None = None):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: the :py:class:~vcfpy.header.Header` to write out, will be
        #: deep-copied into the ``Writer`` on initialization
        self.header = header.copy()
        #: optional ``str`` with the path to the stream
        self.path = None
        # write out headers
        self._write_header()

    xǁWriterǁ__init____mutmut_mutants = {
    'xǁWriterǁ__init____mutmut_1': xǁWriterǁ__init____mutmut_1, 
        'xǁWriterǁ__init____mutmut_2': xǁWriterǁ__init____mutmut_2, 
        'xǁWriterǁ__init____mutmut_3': xǁWriterǁ__init____mutmut_3, 
        'xǁWriterǁ__init____mutmut_4': xǁWriterǁ__init____mutmut_4, 
        'xǁWriterǁ__init____mutmut_5': xǁWriterǁ__init____mutmut_5
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁWriterǁ__init____mutmut_orig)
    xǁWriterǁ__init____mutmut_orig.__name__ = 'xǁWriterǁ__init__'



    def xǁWriterǁ_write_header__mutmut_orig(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples and self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
                file=self.stream,
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_1(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(),)
        if self.header.samples and self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
                file=self.stream,
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_2(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples or self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
                file=self.stream,
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_3(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples and self.header.samples.names:
            print(
                "XX\tXX".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
                file=self.stream,
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_4(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples and self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) - self.header.samples.names),
                file=self.stream,
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_5(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples and self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_6(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples and self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
                file=self.stream,
            )
        else:
            print("XX\tXX".join(parser.REQUIRE_NO_SAMPLE_HEADER), file=self.stream)

    def xǁWriterǁ_write_header__mutmut_7(self):
        """Write out the header"""
        for line in self.header.lines:
            print(line.serialize(), file=self.stream)
        if self.header.samples and self.header.samples.names:
            print(
                "\t".join(list(parser.REQUIRE_SAMPLE_HEADER) + self.header.samples.names),
                file=self.stream,
            )
        else:
            print("\t".join(parser.REQUIRE_NO_SAMPLE_HEADER),)

    xǁWriterǁ_write_header__mutmut_mutants = {
    'xǁWriterǁ_write_header__mutmut_1': xǁWriterǁ_write_header__mutmut_1, 
        'xǁWriterǁ_write_header__mutmut_2': xǁWriterǁ_write_header__mutmut_2, 
        'xǁWriterǁ_write_header__mutmut_3': xǁWriterǁ_write_header__mutmut_3, 
        'xǁWriterǁ_write_header__mutmut_4': xǁWriterǁ_write_header__mutmut_4, 
        'xǁWriterǁ_write_header__mutmut_5': xǁWriterǁ_write_header__mutmut_5, 
        'xǁWriterǁ_write_header__mutmut_6': xǁWriterǁ_write_header__mutmut_6, 
        'xǁWriterǁ_write_header__mutmut_7': xǁWriterǁ_write_header__mutmut_7
    }

    def _write_header(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ_write_header__mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ_write_header__mutmut_mutants"), *args, **kwargs) 

    _write_header.__signature__ = _mutmut_signature(xǁWriterǁ_write_header__mutmut_orig)
    xǁWriterǁ_write_header__mutmut_orig.__name__ = 'xǁWriterǁ_write_header'



    def xǁWriterǁclose__mutmut_orig(self):
        """Close underlying stream"""
        self.stream.close()

    xǁWriterǁclose__mutmut_mutants = {

    }

    def close(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁclose__mutmut_orig"), object.__getattribute__(self, "xǁWriterǁclose__mutmut_mutants"), *args, **kwargs) 

    close.__signature__ = _mutmut_signature(xǁWriterǁclose__mutmut_orig)
    xǁWriterǁclose__mutmut_orig.__name__ = 'xǁWriterǁclose'



    def xǁWriterǁwrite_record__mutmut_orig(self, record: record.Record):
        """Write out the given :py:class:`vcfpy.record.Record` to this
        Writer"""
        self._serialize_record(record)

    def xǁWriterǁwrite_record__mutmut_1(self, record: record.Record):
        """Write out the given :py:class:`vcfpy.record.Record` to this
        Writer"""
        self._serialize_record(None)

    xǁWriterǁwrite_record__mutmut_mutants = {
    'xǁWriterǁwrite_record__mutmut_1': xǁWriterǁwrite_record__mutmut_1
    }

    def write_record(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁwrite_record__mutmut_orig"), object.__getattribute__(self, "xǁWriterǁwrite_record__mutmut_mutants"), *args, **kwargs) 

    write_record.__signature__ = _mutmut_signature(xǁWriterǁwrite_record__mutmut_orig)
    xǁWriterǁwrite_record__mutmut_orig.__name__ = 'xǁWriterǁwrite_record'



    def xǁWriterǁ_serialize_record__mutmut_orig(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_1(self, record: record.Record):
        """Serialize whole Record"""
        f = None
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_2(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = None
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_3(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f("XX;XX".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_4(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if  record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_5(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append("XX.XX")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_6(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append("XX,XX".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_7(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f("XX;XX".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_8(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(None)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_9(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append("XX:XX".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_10(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = None
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_11(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = None
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_12(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row -= [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_13(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row = [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_14(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[None]) for s in names]
        print(*row, sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_15(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="XX\tXX", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_16(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print( sep="\t", file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_17(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, file=self.stream)

    def xǁWriterǁ_serialize_record__mutmut_18(self, record: record.Record):
        """Serialize whole Record"""
        f = self._empty_to_dot
        row: list[Any] = [record.CHROM, record.POS]
        row.append(f(";".join(record.ID)))
        row.append(f(record.REF))
        if not record.ALT:
            row.append(".")
        else:
            row.append(",".join([f(a.serialize()) for a in record.ALT]))
        row.append(f(record.QUAL))
        row.append(f(";".join(record.FILTER)))
        row.append(f(self._serialize_info(record)))
        if record.FORMAT:
            row.append(":".join(record.FORMAT))
        if self.header.samples:
            names = self.header.samples.names
        else:
            names = []
        row += [self._serialize_call(record.FORMAT, record.call_for_sample[s]) for s in names]
        print(*row, sep="\t",)

    xǁWriterǁ_serialize_record__mutmut_mutants = {
    'xǁWriterǁ_serialize_record__mutmut_1': xǁWriterǁ_serialize_record__mutmut_1, 
        'xǁWriterǁ_serialize_record__mutmut_2': xǁWriterǁ_serialize_record__mutmut_2, 
        'xǁWriterǁ_serialize_record__mutmut_3': xǁWriterǁ_serialize_record__mutmut_3, 
        'xǁWriterǁ_serialize_record__mutmut_4': xǁWriterǁ_serialize_record__mutmut_4, 
        'xǁWriterǁ_serialize_record__mutmut_5': xǁWriterǁ_serialize_record__mutmut_5, 
        'xǁWriterǁ_serialize_record__mutmut_6': xǁWriterǁ_serialize_record__mutmut_6, 
        'xǁWriterǁ_serialize_record__mutmut_7': xǁWriterǁ_serialize_record__mutmut_7, 
        'xǁWriterǁ_serialize_record__mutmut_8': xǁWriterǁ_serialize_record__mutmut_8, 
        'xǁWriterǁ_serialize_record__mutmut_9': xǁWriterǁ_serialize_record__mutmut_9, 
        'xǁWriterǁ_serialize_record__mutmut_10': xǁWriterǁ_serialize_record__mutmut_10, 
        'xǁWriterǁ_serialize_record__mutmut_11': xǁWriterǁ_serialize_record__mutmut_11, 
        'xǁWriterǁ_serialize_record__mutmut_12': xǁWriterǁ_serialize_record__mutmut_12, 
        'xǁWriterǁ_serialize_record__mutmut_13': xǁWriterǁ_serialize_record__mutmut_13, 
        'xǁWriterǁ_serialize_record__mutmut_14': xǁWriterǁ_serialize_record__mutmut_14, 
        'xǁWriterǁ_serialize_record__mutmut_15': xǁWriterǁ_serialize_record__mutmut_15, 
        'xǁWriterǁ_serialize_record__mutmut_16': xǁWriterǁ_serialize_record__mutmut_16, 
        'xǁWriterǁ_serialize_record__mutmut_17': xǁWriterǁ_serialize_record__mutmut_17, 
        'xǁWriterǁ_serialize_record__mutmut_18': xǁWriterǁ_serialize_record__mutmut_18
    }

    def _serialize_record(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ_serialize_record__mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ_serialize_record__mutmut_mutants"), *args, **kwargs) 

    _serialize_record.__signature__ = _mutmut_signature(xǁWriterǁ_serialize_record__mutmut_orig)
    xǁWriterǁ_serialize_record__mutmut_orig.__name__ = 'xǁWriterǁ_serialize_record'



    def xǁWriterǁ_serialize_info__mutmut_orig(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_1(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = None
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_2(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(None)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_3(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = None
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_4(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type != "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_5(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "XXFlagXX":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_6(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(None)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_7(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("XX{}={}XX".format(key, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_8(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(None, format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_9(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(None, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_10(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, None, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_11(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "XXINFOXX")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_12(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value( value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_13(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_14(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format( format_value(info, value, "INFO")))
        return ";".join(result)

    def xǁWriterǁ_serialize_info__mutmut_15(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return "XX;XX".join(result)

    def xǁWriterǁ_serialize_info__mutmut_16(self, record: record.Record) -> str:
        """Return serialized version of record.INFO"""
        result: list[str] = []
        for key, value in record.INFO.items():
            info = self.header.get_info_field_info(key)
            if info.type == "Flag":
                result.append(key)
            else:
                result.append("{}={}".format(key, format_value(info, value, "INFO")))
        return ";".join(None)

    xǁWriterǁ_serialize_info__mutmut_mutants = {
    'xǁWriterǁ_serialize_info__mutmut_1': xǁWriterǁ_serialize_info__mutmut_1, 
        'xǁWriterǁ_serialize_info__mutmut_2': xǁWriterǁ_serialize_info__mutmut_2, 
        'xǁWriterǁ_serialize_info__mutmut_3': xǁWriterǁ_serialize_info__mutmut_3, 
        'xǁWriterǁ_serialize_info__mutmut_4': xǁWriterǁ_serialize_info__mutmut_4, 
        'xǁWriterǁ_serialize_info__mutmut_5': xǁWriterǁ_serialize_info__mutmut_5, 
        'xǁWriterǁ_serialize_info__mutmut_6': xǁWriterǁ_serialize_info__mutmut_6, 
        'xǁWriterǁ_serialize_info__mutmut_7': xǁWriterǁ_serialize_info__mutmut_7, 
        'xǁWriterǁ_serialize_info__mutmut_8': xǁWriterǁ_serialize_info__mutmut_8, 
        'xǁWriterǁ_serialize_info__mutmut_9': xǁWriterǁ_serialize_info__mutmut_9, 
        'xǁWriterǁ_serialize_info__mutmut_10': xǁWriterǁ_serialize_info__mutmut_10, 
        'xǁWriterǁ_serialize_info__mutmut_11': xǁWriterǁ_serialize_info__mutmut_11, 
        'xǁWriterǁ_serialize_info__mutmut_12': xǁWriterǁ_serialize_info__mutmut_12, 
        'xǁWriterǁ_serialize_info__mutmut_13': xǁWriterǁ_serialize_info__mutmut_13, 
        'xǁWriterǁ_serialize_info__mutmut_14': xǁWriterǁ_serialize_info__mutmut_14, 
        'xǁWriterǁ_serialize_info__mutmut_15': xǁWriterǁ_serialize_info__mutmut_15, 
        'xǁWriterǁ_serialize_info__mutmut_16': xǁWriterǁ_serialize_info__mutmut_16
    }

    def _serialize_info(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ_serialize_info__mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ_serialize_info__mutmut_mutants"), *args, **kwargs) 

    _serialize_info.__signature__ = _mutmut_signature(xǁWriterǁ_serialize_info__mutmut_orig)
    xǁWriterǁ_serialize_info__mutmut_orig.__name__ = 'xǁWriterǁ_serialize_info'



    def xǁWriterǁ_serialize_call__mutmut_orig(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str | None] = [
                format_value(self.header.get_format_field_info(key), call.data.get(key), "FORMAT") for key in format_
            ]
            return ":".join([r for r in result if r is not None])

    def xǁWriterǁ_serialize_call__mutmut_1(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str & None] = [
                format_value(self.header.get_format_field_info(key), call.data.get(key), "FORMAT") for key in format_
            ]
            return ":".join([r for r in result if r is not None])

    def xǁWriterǁ_serialize_call__mutmut_2(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str | None] = [
                format_value(self.header.get_format_field_info(None), call.data.get(key), "FORMAT") for key in format_
            ]
            return ":".join([r for r in result if r is not None])

    def xǁWriterǁ_serialize_call__mutmut_3(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str | None] = [
                format_value(self.header.get_format_field_info(key), call.data.get(None), "FORMAT") for key in format_
            ]
            return ":".join([r for r in result if r is not None])

    def xǁWriterǁ_serialize_call__mutmut_4(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str | None] = None
            return ":".join([r for r in result if r is not None])

    def xǁWriterǁ_serialize_call__mutmut_5(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str | None] = [
                format_value(self.header.get_format_field_info(key), call.data.get(key), "FORMAT") for key in format_
            ]
            return "XX:XX".join([r for r in result if r is not None])

    def xǁWriterǁ_serialize_call__mutmut_6(self, format_: list[str], call: record.Call | record.UnparsedCall) -> str:
        """Return serialized version of the Call using the record's FORMAT'"""
        if isinstance(call, record.UnparsedCall):
            return call.unparsed_data
        else:
            result: list[str | None] = [
                format_value(self.header.get_format_field_info(key), call.data.get(key), "FORMAT") for key in format_
            ]
            return ":".join([r for r in result if r is  None])

    xǁWriterǁ_serialize_call__mutmut_mutants = {
    'xǁWriterǁ_serialize_call__mutmut_1': xǁWriterǁ_serialize_call__mutmut_1, 
        'xǁWriterǁ_serialize_call__mutmut_2': xǁWriterǁ_serialize_call__mutmut_2, 
        'xǁWriterǁ_serialize_call__mutmut_3': xǁWriterǁ_serialize_call__mutmut_3, 
        'xǁWriterǁ_serialize_call__mutmut_4': xǁWriterǁ_serialize_call__mutmut_4, 
        'xǁWriterǁ_serialize_call__mutmut_5': xǁWriterǁ_serialize_call__mutmut_5, 
        'xǁWriterǁ_serialize_call__mutmut_6': xǁWriterǁ_serialize_call__mutmut_6
    }

    def _serialize_call(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ_serialize_call__mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ_serialize_call__mutmut_mutants"), *args, **kwargs) 

    _serialize_call.__signature__ = _mutmut_signature(xǁWriterǁ_serialize_call__mutmut_orig)
    xǁWriterǁ_serialize_call__mutmut_orig.__name__ = 'xǁWriterǁ_serialize_call'



    @classmethod
    def _empty_to_dot(cls, val: Any) -> str:
        """Return val or '.' if empty value"""
        if val == "" or val is None or val == []:
            return "."
        else:
            return val

    def xǁWriterǁ__enter____mutmut_orig(self) -> "Writer":
        return self

    xǁWriterǁ__enter____mutmut_mutants = {

    }

    def __enter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ__enter____mutmut_mutants"), *args, **kwargs) 

    __enter__.__signature__ = _mutmut_signature(xǁWriterǁ__enter____mutmut_orig)
    xǁWriterǁ__enter____mutmut_orig.__name__ = 'xǁWriterǁ__enter__'



    def xǁWriterǁ__exit____mutmut_orig(self, type_: type[BaseException] | None, value: BaseException | None, traceback: typing.Any) -> None:
        self.close()

    xǁWriterǁ__exit____mutmut_mutants = {

    }

    def __exit__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁWriterǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁWriterǁ__exit____mutmut_mutants"), *args, **kwargs) 

    __exit__.__signature__ = _mutmut_signature(xǁWriterǁ__exit____mutmut_orig)
    xǁWriterǁ__exit____mutmut_orig.__name__ = 'xǁWriterǁ__exit__'


