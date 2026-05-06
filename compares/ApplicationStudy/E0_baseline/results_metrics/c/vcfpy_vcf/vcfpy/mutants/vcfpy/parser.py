
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
"""Parsing of VCF files from ``str``"""

import ast
import functools
import io
import math
import pathlib
import re
import warnings
from typing import Any, Callable, Iterable, Literal, cast

from vcfpy import exceptions, header, record

__author__ = "Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>"


# expected "#CHROM" header prefix when there are samples
REQUIRE_SAMPLE_HEADER = ("#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT")
# expected "#CHROM" header prefix when there are no samples
REQUIRE_NO_SAMPLE_HEADER = ("#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO")

#: Supported VCF versions, a warning will be issued otherwise
SUPPORTED_VCF_VERSIONS = ("VCFv4.0", "VCFv4.1", "VCFv4.2", "VCFv4.3")


class QuotedStringSplitter:
    """Helper class for splitting quoted strings

    Has support for interpreting quoting strings but also brackets.  Meant
    for splitting the VCF header line dicts
    """

    #: state constant for normal
    NORMAL = 0
    #: state constant for quoted
    QUOTED = 1
    #: state constant for delimiter
    ESCAPED = 2
    #: state constant for array
    ARRAY = 3
    #: state constant for delimiter
    DELIM = 4

    def xǁQuotedStringSplitterǁ__init____mutmut_orig(self, delim: str = ",", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_1(self, delim: str = "XX,XX", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_2(self, delim: str = ",", quote: str = 'XX"XX', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_3(self, delim: str = ",", quote: str = '"', brackets: str = "XX[]XX"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_4(self, delim: str = ",", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = None
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_5(self, delim: str = ",", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = None
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_6(self, delim: str = ",", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) != 2
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_7(self, delim: str = ",", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 3
        self.brackets = brackets

    def xǁQuotedStringSplitterǁ__init____mutmut_8(self, delim: str = ",", quote: str = '"', brackets: str = "[]"):
        #: string delimiter
        self.delim = delim
        #: quote character
        self.quote = quote
        #: two-character string with opening and closing brackets
        assert len(brackets) == 2
        self.brackets = None

    xǁQuotedStringSplitterǁ__init____mutmut_mutants = {
    'xǁQuotedStringSplitterǁ__init____mutmut_1': xǁQuotedStringSplitterǁ__init____mutmut_1, 
        'xǁQuotedStringSplitterǁ__init____mutmut_2': xǁQuotedStringSplitterǁ__init____mutmut_2, 
        'xǁQuotedStringSplitterǁ__init____mutmut_3': xǁQuotedStringSplitterǁ__init____mutmut_3, 
        'xǁQuotedStringSplitterǁ__init____mutmut_4': xǁQuotedStringSplitterǁ__init____mutmut_4, 
        'xǁQuotedStringSplitterǁ__init____mutmut_5': xǁQuotedStringSplitterǁ__init____mutmut_5, 
        'xǁQuotedStringSplitterǁ__init____mutmut_6': xǁQuotedStringSplitterǁ__init____mutmut_6, 
        'xǁQuotedStringSplitterǁ__init____mutmut_7': xǁQuotedStringSplitterǁ__init____mutmut_7, 
        'xǁQuotedStringSplitterǁ__init____mutmut_8': xǁQuotedStringSplitterǁ__init____mutmut_8
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁ__init____mutmut_orig)
    xǁQuotedStringSplitterǁ__init____mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁ__init__'



    def xǁQuotedStringSplitterǁrun__mutmut_orig(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_1(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [1]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_2(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = None
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_3(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = None
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_4(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[1, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_5(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 2, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_6(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 3, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_7(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 4, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_8(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 5], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_9(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[1, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_10(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 2, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_11(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 3, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_12(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 4, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_13(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 5]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_14(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = None
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_15(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[1, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_16(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 2, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_17(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 3, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_18(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 4, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_19(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 5] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_20(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = None
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_21(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(None):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_22(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[None](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_23(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](None, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_24(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, None, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_25(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, None, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_26(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, None)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_27(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state]( pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_28(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_29(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_30(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins,)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_31(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = None
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_32(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) != len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_33(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[None] for start, end in zip(begins, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_34(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(None, ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_35(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, None, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_36(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends, strict=True)]

    def xǁQuotedStringSplitterǁrun__mutmut_37(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip( ends, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_38(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, strict=False)]

    def xǁQuotedStringSplitterǁrun__mutmut_39(self, s: str) -> list[str]:
        """Split string ``s`` at delimiter, correctly interpreting quotes

        Further, interprets arrays wrapped in one level of ``[]``.  No
        recursive brackets are interpreted (as this would make the grammar
        non-regular and currently this complexity is not needed).  Currently,
        quoting inside of braces is not supported either.  This is just to
        support the example from VCF v4.3.
        """
        begins: list[int] = [0]
        ends: list[int] = []
        # transition table
        DISPATCH: dict[Literal[0, 1, 2, 3, 4], Callable[[str, int, list[int], list[int]], Literal[0, 1, 2, 3, 4]]] = {
            self.NORMAL: self._handle_normal,
            self.QUOTED: self._handle_quoted,
            self.ARRAY: self._handle_array,
            self.DELIM: self._handle_delim,
            self.ESCAPED: self._handle_escaped,
        }
        # run state automaton
        state: Literal[0, 1, 2, 3, 4] = self.NORMAL
        for pos, c in enumerate(s):
            state = DISPATCH[state](c, pos, begins, ends)
        ends.append(len(s))
        assert len(begins) == len(ends)
        # Build resulting list
        return [s[start:end] for start, end in zip(begins, ends,)]

    xǁQuotedStringSplitterǁrun__mutmut_mutants = {
    'xǁQuotedStringSplitterǁrun__mutmut_1': xǁQuotedStringSplitterǁrun__mutmut_1, 
        'xǁQuotedStringSplitterǁrun__mutmut_2': xǁQuotedStringSplitterǁrun__mutmut_2, 
        'xǁQuotedStringSplitterǁrun__mutmut_3': xǁQuotedStringSplitterǁrun__mutmut_3, 
        'xǁQuotedStringSplitterǁrun__mutmut_4': xǁQuotedStringSplitterǁrun__mutmut_4, 
        'xǁQuotedStringSplitterǁrun__mutmut_5': xǁQuotedStringSplitterǁrun__mutmut_5, 
        'xǁQuotedStringSplitterǁrun__mutmut_6': xǁQuotedStringSplitterǁrun__mutmut_6, 
        'xǁQuotedStringSplitterǁrun__mutmut_7': xǁQuotedStringSplitterǁrun__mutmut_7, 
        'xǁQuotedStringSplitterǁrun__mutmut_8': xǁQuotedStringSplitterǁrun__mutmut_8, 
        'xǁQuotedStringSplitterǁrun__mutmut_9': xǁQuotedStringSplitterǁrun__mutmut_9, 
        'xǁQuotedStringSplitterǁrun__mutmut_10': xǁQuotedStringSplitterǁrun__mutmut_10, 
        'xǁQuotedStringSplitterǁrun__mutmut_11': xǁQuotedStringSplitterǁrun__mutmut_11, 
        'xǁQuotedStringSplitterǁrun__mutmut_12': xǁQuotedStringSplitterǁrun__mutmut_12, 
        'xǁQuotedStringSplitterǁrun__mutmut_13': xǁQuotedStringSplitterǁrun__mutmut_13, 
        'xǁQuotedStringSplitterǁrun__mutmut_14': xǁQuotedStringSplitterǁrun__mutmut_14, 
        'xǁQuotedStringSplitterǁrun__mutmut_15': xǁQuotedStringSplitterǁrun__mutmut_15, 
        'xǁQuotedStringSplitterǁrun__mutmut_16': xǁQuotedStringSplitterǁrun__mutmut_16, 
        'xǁQuotedStringSplitterǁrun__mutmut_17': xǁQuotedStringSplitterǁrun__mutmut_17, 
        'xǁQuotedStringSplitterǁrun__mutmut_18': xǁQuotedStringSplitterǁrun__mutmut_18, 
        'xǁQuotedStringSplitterǁrun__mutmut_19': xǁQuotedStringSplitterǁrun__mutmut_19, 
        'xǁQuotedStringSplitterǁrun__mutmut_20': xǁQuotedStringSplitterǁrun__mutmut_20, 
        'xǁQuotedStringSplitterǁrun__mutmut_21': xǁQuotedStringSplitterǁrun__mutmut_21, 
        'xǁQuotedStringSplitterǁrun__mutmut_22': xǁQuotedStringSplitterǁrun__mutmut_22, 
        'xǁQuotedStringSplitterǁrun__mutmut_23': xǁQuotedStringSplitterǁrun__mutmut_23, 
        'xǁQuotedStringSplitterǁrun__mutmut_24': xǁQuotedStringSplitterǁrun__mutmut_24, 
        'xǁQuotedStringSplitterǁrun__mutmut_25': xǁQuotedStringSplitterǁrun__mutmut_25, 
        'xǁQuotedStringSplitterǁrun__mutmut_26': xǁQuotedStringSplitterǁrun__mutmut_26, 
        'xǁQuotedStringSplitterǁrun__mutmut_27': xǁQuotedStringSplitterǁrun__mutmut_27, 
        'xǁQuotedStringSplitterǁrun__mutmut_28': xǁQuotedStringSplitterǁrun__mutmut_28, 
        'xǁQuotedStringSplitterǁrun__mutmut_29': xǁQuotedStringSplitterǁrun__mutmut_29, 
        'xǁQuotedStringSplitterǁrun__mutmut_30': xǁQuotedStringSplitterǁrun__mutmut_30, 
        'xǁQuotedStringSplitterǁrun__mutmut_31': xǁQuotedStringSplitterǁrun__mutmut_31, 
        'xǁQuotedStringSplitterǁrun__mutmut_32': xǁQuotedStringSplitterǁrun__mutmut_32, 
        'xǁQuotedStringSplitterǁrun__mutmut_33': xǁQuotedStringSplitterǁrun__mutmut_33, 
        'xǁQuotedStringSplitterǁrun__mutmut_34': xǁQuotedStringSplitterǁrun__mutmut_34, 
        'xǁQuotedStringSplitterǁrun__mutmut_35': xǁQuotedStringSplitterǁrun__mutmut_35, 
        'xǁQuotedStringSplitterǁrun__mutmut_36': xǁQuotedStringSplitterǁrun__mutmut_36, 
        'xǁQuotedStringSplitterǁrun__mutmut_37': xǁQuotedStringSplitterǁrun__mutmut_37, 
        'xǁQuotedStringSplitterǁrun__mutmut_38': xǁQuotedStringSplitterǁrun__mutmut_38, 
        'xǁQuotedStringSplitterǁrun__mutmut_39': xǁQuotedStringSplitterǁrun__mutmut_39
    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁrun__mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁrun__mutmut_orig)
    xǁQuotedStringSplitterǁrun__mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁrun'



    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_orig(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.delim:
            ends.append(pos)
            return self.DELIM
        elif c == self.quote:
            return self.QUOTED
        elif c == self.brackets[0]:
            return self.ARRAY
        else:
            return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_1(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c != self.delim:
            ends.append(pos)
            return self.DELIM
        elif c == self.quote:
            return self.QUOTED
        elif c == self.brackets[0]:
            return self.ARRAY
        else:
            return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_2(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.delim:
            ends.append(None)
            return self.DELIM
        elif c == self.quote:
            return self.QUOTED
        elif c == self.brackets[0]:
            return self.ARRAY
        else:
            return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_3(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.delim:
            ends.append(pos)
            return self.DELIM
        elif c != self.quote:
            return self.QUOTED
        elif c == self.brackets[0]:
            return self.ARRAY
        else:
            return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_4(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.delim:
            ends.append(pos)
            return self.DELIM
        elif c == self.quote:
            return self.QUOTED
        elif c != self.brackets[0]:
            return self.ARRAY
        else:
            return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_5(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.delim:
            ends.append(pos)
            return self.DELIM
        elif c == self.quote:
            return self.QUOTED
        elif c == self.brackets[1]:
            return self.ARRAY
        else:
            return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_normal__mutmut_6(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.delim:
            ends.append(pos)
            return self.DELIM
        elif c == self.quote:
            return self.QUOTED
        elif c == self.brackets[None]:
            return self.ARRAY
        else:
            return self.NORMAL

    xǁQuotedStringSplitterǁ_handle_normal__mutmut_mutants = {
    'xǁQuotedStringSplitterǁ_handle_normal__mutmut_1': xǁQuotedStringSplitterǁ_handle_normal__mutmut_1, 
        'xǁQuotedStringSplitterǁ_handle_normal__mutmut_2': xǁQuotedStringSplitterǁ_handle_normal__mutmut_2, 
        'xǁQuotedStringSplitterǁ_handle_normal__mutmut_3': xǁQuotedStringSplitterǁ_handle_normal__mutmut_3, 
        'xǁQuotedStringSplitterǁ_handle_normal__mutmut_4': xǁQuotedStringSplitterǁ_handle_normal__mutmut_4, 
        'xǁQuotedStringSplitterǁ_handle_normal__mutmut_5': xǁQuotedStringSplitterǁ_handle_normal__mutmut_5, 
        'xǁQuotedStringSplitterǁ_handle_normal__mutmut_6': xǁQuotedStringSplitterǁ_handle_normal__mutmut_6
    }

    def _handle_normal(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_normal__mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_normal__mutmut_mutants"), *args, **kwargs) 

    _handle_normal.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁ_handle_normal__mutmut_orig)
    xǁQuotedStringSplitterǁ_handle_normal__mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁ_handle_normal'



    def xǁQuotedStringSplitterǁ_handle_quoted__mutmut_orig(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == "\\":
            return self.ESCAPED
        elif c == self.quote:
            return self.NORMAL
        else:
            return self.QUOTED

    def xǁQuotedStringSplitterǁ_handle_quoted__mutmut_1(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c != "\\":
            return self.ESCAPED
        elif c == self.quote:
            return self.NORMAL
        else:
            return self.QUOTED

    def xǁQuotedStringSplitterǁ_handle_quoted__mutmut_2(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == "XX\\XX":
            return self.ESCAPED
        elif c == self.quote:
            return self.NORMAL
        else:
            return self.QUOTED

    def xǁQuotedStringSplitterǁ_handle_quoted__mutmut_3(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == "\\":
            return self.ESCAPED
        elif c != self.quote:
            return self.NORMAL
        else:
            return self.QUOTED

    xǁQuotedStringSplitterǁ_handle_quoted__mutmut_mutants = {
    'xǁQuotedStringSplitterǁ_handle_quoted__mutmut_1': xǁQuotedStringSplitterǁ_handle_quoted__mutmut_1, 
        'xǁQuotedStringSplitterǁ_handle_quoted__mutmut_2': xǁQuotedStringSplitterǁ_handle_quoted__mutmut_2, 
        'xǁQuotedStringSplitterǁ_handle_quoted__mutmut_3': xǁQuotedStringSplitterǁ_handle_quoted__mutmut_3
    }

    def _handle_quoted(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_quoted__mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_quoted__mutmut_mutants"), *args, **kwargs) 

    _handle_quoted.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁ_handle_quoted__mutmut_orig)
    xǁQuotedStringSplitterǁ_handle_quoted__mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁ_handle_quoted'



    def xǁQuotedStringSplitterǁ_handle_array__mutmut_orig(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.brackets[1]:
            return self.NORMAL
        else:
            return self.ARRAY

    def xǁQuotedStringSplitterǁ_handle_array__mutmut_1(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c != self.brackets[1]:
            return self.NORMAL
        else:
            return self.ARRAY

    def xǁQuotedStringSplitterǁ_handle_array__mutmut_2(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.brackets[2]:
            return self.NORMAL
        else:
            return self.ARRAY

    def xǁQuotedStringSplitterǁ_handle_array__mutmut_3(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        if c == self.brackets[None]:
            return self.NORMAL
        else:
            return self.ARRAY

    xǁQuotedStringSplitterǁ_handle_array__mutmut_mutants = {
    'xǁQuotedStringSplitterǁ_handle_array__mutmut_1': xǁQuotedStringSplitterǁ_handle_array__mutmut_1, 
        'xǁQuotedStringSplitterǁ_handle_array__mutmut_2': xǁQuotedStringSplitterǁ_handle_array__mutmut_2, 
        'xǁQuotedStringSplitterǁ_handle_array__mutmut_3': xǁQuotedStringSplitterǁ_handle_array__mutmut_3
    }

    def _handle_array(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_array__mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_array__mutmut_mutants"), *args, **kwargs) 

    _handle_array.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁ_handle_array__mutmut_orig)
    xǁQuotedStringSplitterǁ_handle_array__mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁ_handle_array'



    def xǁQuotedStringSplitterǁ_handle_delim__mutmut_orig(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        begins.append(pos)
        return self.NORMAL

    def xǁQuotedStringSplitterǁ_handle_delim__mutmut_1(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        begins.append(None)
        return self.NORMAL

    xǁQuotedStringSplitterǁ_handle_delim__mutmut_mutants = {
    'xǁQuotedStringSplitterǁ_handle_delim__mutmut_1': xǁQuotedStringSplitterǁ_handle_delim__mutmut_1
    }

    def _handle_delim(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_delim__mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_delim__mutmut_mutants"), *args, **kwargs) 

    _handle_delim.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁ_handle_delim__mutmut_orig)
    xǁQuotedStringSplitterǁ_handle_delim__mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁ_handle_delim'



    def xǁQuotedStringSplitterǁ_handle_escaped__mutmut_orig(
        self, c: str, pos: int, begins: list[int], ends: list[int]
    ) -> Literal[0, 1, 2, 3, 4]:  # pylint: disable=W0613
        return self.QUOTED

    xǁQuotedStringSplitterǁ_handle_escaped__mutmut_mutants = {

    }

    def _handle_escaped(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_escaped__mutmut_orig"), object.__getattribute__(self, "xǁQuotedStringSplitterǁ_handle_escaped__mutmut_mutants"), *args, **kwargs) 

    _handle_escaped.__signature__ = _mutmut_signature(xǁQuotedStringSplitterǁ_handle_escaped__mutmut_orig)
    xǁQuotedStringSplitterǁ_handle_escaped__mutmut_orig.__name__ = 'xǁQuotedStringSplitterǁ_handle_escaped'




def split_quoted_string__mutmut_orig(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, quote, brackets).run(s)


def split_quoted_string__mutmut_1(s: str, delim: str = "XX,XX", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, quote, brackets).run(s)


def split_quoted_string__mutmut_2(s: str, delim: str = ",", quote: str = 'XX"XX', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, quote, brackets).run(s)


def split_quoted_string__mutmut_3(s: str, delim: str = ",", quote: str = '"', brackets: str = "XX[]XX") -> list[str]:
    return QuotedStringSplitter(delim, quote, brackets).run(s)


def split_quoted_string__mutmut_4(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(None, quote, brackets).run(s)


def split_quoted_string__mutmut_5(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, None, brackets).run(s)


def split_quoted_string__mutmut_6(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, quote, None).run(s)


def split_quoted_string__mutmut_7(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter( quote, brackets).run(s)


def split_quoted_string__mutmut_8(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, brackets).run(s)


def split_quoted_string__mutmut_9(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, quote,).run(s)


def split_quoted_string__mutmut_10(s: str, delim: str = ",", quote: str = '"', brackets: str = "[]") -> list[str]:
    return QuotedStringSplitter(delim, quote, brackets).run(None)

split_quoted_string__mutmut_mutants = {
'split_quoted_string__mutmut_1': split_quoted_string__mutmut_1, 
    'split_quoted_string__mutmut_2': split_quoted_string__mutmut_2, 
    'split_quoted_string__mutmut_3': split_quoted_string__mutmut_3, 
    'split_quoted_string__mutmut_4': split_quoted_string__mutmut_4, 
    'split_quoted_string__mutmut_5': split_quoted_string__mutmut_5, 
    'split_quoted_string__mutmut_6': split_quoted_string__mutmut_6, 
    'split_quoted_string__mutmut_7': split_quoted_string__mutmut_7, 
    'split_quoted_string__mutmut_8': split_quoted_string__mutmut_8, 
    'split_quoted_string__mutmut_9': split_quoted_string__mutmut_9, 
    'split_quoted_string__mutmut_10': split_quoted_string__mutmut_10
}

def split_quoted_string(*args, **kwargs):
    return _mutmut_trampoline(split_quoted_string__mutmut_orig, split_quoted_string__mutmut_mutants, *args, **kwargs) 

split_quoted_string.__signature__ = _mutmut_signature(split_quoted_string__mutmut_orig)
split_quoted_string__mutmut_orig.__name__ = 'split_quoted_string'




def split_mapping__mutmut_orig(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("=", 1)
    key = orig_key.strip()
    if key != orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_1(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("XX=XX", 1)
    key = orig_key.strip()
    if key != orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_2(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("=", 2)
    key = orig_key.strip()
    if key != orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_3(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = None
    key = orig_key.strip()
    if key != orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_4(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("=", 1)
    key = None
    if key != orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_5(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("=", 1)
    key = orig_key.strip()
    if key == orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_6(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("=", 1)
    key = orig_key.strip()
    if key != orig_key:
        warnings.warn(
            "XXMapping key {} has leading or trailing spaceXX".format(repr(orig_key)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value


def split_mapping__mutmut_7(pair_str: str) -> tuple[str, str]:
    """Split the ``str`` in ``pair_str`` at ``'='``

    Warn if key needs to be stripped
    """
    orig_key, value = pair_str.split("=", 1)
    key = orig_key.strip()
    if key != orig_key:
        warnings.warn(
            "Mapping key {} has leading or trailing space".format(repr(None)),
            exceptions.LeadingTrailingSpaceInKey,
        )
    return key, value

split_mapping__mutmut_mutants = {
'split_mapping__mutmut_1': split_mapping__mutmut_1, 
    'split_mapping__mutmut_2': split_mapping__mutmut_2, 
    'split_mapping__mutmut_3': split_mapping__mutmut_3, 
    'split_mapping__mutmut_4': split_mapping__mutmut_4, 
    'split_mapping__mutmut_5': split_mapping__mutmut_5, 
    'split_mapping__mutmut_6': split_mapping__mutmut_6, 
    'split_mapping__mutmut_7': split_mapping__mutmut_7
}

def split_mapping(*args, **kwargs):
    return _mutmut_trampoline(split_mapping__mutmut_orig, split_mapping__mutmut_mutants, *args, **kwargs) 

split_mapping.__signature__ = _mutmut_signature(split_mapping__mutmut_orig)
split_mapping__mutmut_orig.__name__ = 'split_mapping'




def parse_mapping__mutmut_orig(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_1(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if  value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_2(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("XX<XX") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_3(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or  value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_4(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith("XX>XX"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_5(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") and not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_6(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("XXHeader mapping value was not wrapped in angular bracketsXX")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_7(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[2:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_8(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:+1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_9(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-2], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_10(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[None], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_11(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim="XX,XX", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_12(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='XX"XX')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_13(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_14(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",",)
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_15(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = None
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_16(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool & str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_17(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str & list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_18(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = None
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_19(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool & str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_20(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str & list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_21(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "XX=XX" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_22(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" not in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_23(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(None)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_24(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = None
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_25(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('XX"XX') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_26(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('XX"XX'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_27(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') or value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_28(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(None)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_29(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = None
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_30(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("XX[XX") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_31(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("XX]XX"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_32(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") or value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_33(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[2:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_34(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:+1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_35(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-2].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_36(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[None].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_37(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split("XX,XX")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_38(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = None
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_39(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = None
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_40(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, False
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_41(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = None
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(key_values)


def parse_mapping__mutmut_42(value: str) -> dict[str, bool | str | list[str]]:
    """Parse the given VCF header line mapping

    Such a mapping consists of "key=value" pairs, separated by commas and
    wrapped into angular brackets ("<...>").  Strings are usually quoted,
    for certain known keys, exceptions are made, depending on the tag key.
    this, however, only gets important when serializing.

    :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
        there was a problem parsing the file
    """
    if not value.startswith("<") or not value.endswith(">"):
        raise exceptions.InvalidHeaderException("Header mapping value was not wrapped in angular brackets")
    # split the comma-separated list into pairs, ignoring commas in quotes
    pairs = split_quoted_string(value[1:-1], delim=",", quote='"')
    # split these pairs into key/value pairs, converting flags to mappings
    # to True
    key_values: list[tuple[str, bool | str | list[str]]] = []
    for pair in pairs:
        value_: bool | str | list[str]
        if "=" in pair:
            key, value = split_mapping(pair)
            if value.startswith('"') and value.endswith('"'):
                value_ = ast.literal_eval(value)
            elif value.startswith("[") and value.endswith("]"):
                value_ = [v.strip() for v in value[1:-1].split(",")]
            else:
                value_ = value
        else:
            key, value_ = pair, True
        key_values.append((key, value_))
    # return completely parsed mapping as OrderedDict
    return dict(None)

parse_mapping__mutmut_mutants = {
'parse_mapping__mutmut_1': parse_mapping__mutmut_1, 
    'parse_mapping__mutmut_2': parse_mapping__mutmut_2, 
    'parse_mapping__mutmut_3': parse_mapping__mutmut_3, 
    'parse_mapping__mutmut_4': parse_mapping__mutmut_4, 
    'parse_mapping__mutmut_5': parse_mapping__mutmut_5, 
    'parse_mapping__mutmut_6': parse_mapping__mutmut_6, 
    'parse_mapping__mutmut_7': parse_mapping__mutmut_7, 
    'parse_mapping__mutmut_8': parse_mapping__mutmut_8, 
    'parse_mapping__mutmut_9': parse_mapping__mutmut_9, 
    'parse_mapping__mutmut_10': parse_mapping__mutmut_10, 
    'parse_mapping__mutmut_11': parse_mapping__mutmut_11, 
    'parse_mapping__mutmut_12': parse_mapping__mutmut_12, 
    'parse_mapping__mutmut_13': parse_mapping__mutmut_13, 
    'parse_mapping__mutmut_14': parse_mapping__mutmut_14, 
    'parse_mapping__mutmut_15': parse_mapping__mutmut_15, 
    'parse_mapping__mutmut_16': parse_mapping__mutmut_16, 
    'parse_mapping__mutmut_17': parse_mapping__mutmut_17, 
    'parse_mapping__mutmut_18': parse_mapping__mutmut_18, 
    'parse_mapping__mutmut_19': parse_mapping__mutmut_19, 
    'parse_mapping__mutmut_20': parse_mapping__mutmut_20, 
    'parse_mapping__mutmut_21': parse_mapping__mutmut_21, 
    'parse_mapping__mutmut_22': parse_mapping__mutmut_22, 
    'parse_mapping__mutmut_23': parse_mapping__mutmut_23, 
    'parse_mapping__mutmut_24': parse_mapping__mutmut_24, 
    'parse_mapping__mutmut_25': parse_mapping__mutmut_25, 
    'parse_mapping__mutmut_26': parse_mapping__mutmut_26, 
    'parse_mapping__mutmut_27': parse_mapping__mutmut_27, 
    'parse_mapping__mutmut_28': parse_mapping__mutmut_28, 
    'parse_mapping__mutmut_29': parse_mapping__mutmut_29, 
    'parse_mapping__mutmut_30': parse_mapping__mutmut_30, 
    'parse_mapping__mutmut_31': parse_mapping__mutmut_31, 
    'parse_mapping__mutmut_32': parse_mapping__mutmut_32, 
    'parse_mapping__mutmut_33': parse_mapping__mutmut_33, 
    'parse_mapping__mutmut_34': parse_mapping__mutmut_34, 
    'parse_mapping__mutmut_35': parse_mapping__mutmut_35, 
    'parse_mapping__mutmut_36': parse_mapping__mutmut_36, 
    'parse_mapping__mutmut_37': parse_mapping__mutmut_37, 
    'parse_mapping__mutmut_38': parse_mapping__mutmut_38, 
    'parse_mapping__mutmut_39': parse_mapping__mutmut_39, 
    'parse_mapping__mutmut_40': parse_mapping__mutmut_40, 
    'parse_mapping__mutmut_41': parse_mapping__mutmut_41, 
    'parse_mapping__mutmut_42': parse_mapping__mutmut_42
}

def parse_mapping(*args, **kwargs):
    return _mutmut_trampoline(parse_mapping__mutmut_orig, parse_mapping__mutmut_mutants, *args, **kwargs) 

parse_mapping.__signature__ = _mutmut_signature(parse_mapping__mutmut_orig)
parse_mapping__mutmut_orig.__name__ = 'parse_mapping'




class HeaderLineParserBase:
    """Parse into appropriate HeaderLine"""

    def xǁHeaderLineParserBaseǁparse_key_value__mutmut_orig(self, key: str, value: str) -> header.HeaderLine:
        """Parse the key/value pair

        :param str key: the key to use in parsing
        :param str value: the value to parse
        :returns: :py:class:`vcfpy.header.HeaderLine` object
        """
        raise NotImplementedError("Must be overridden")

    def xǁHeaderLineParserBaseǁparse_key_value__mutmut_1(self, key: str, value: str) -> header.HeaderLine:
        """Parse the key/value pair

        :param str key: the key to use in parsing
        :param str value: the value to parse
        :returns: :py:class:`vcfpy.header.HeaderLine` object
        """
        raise NotImplementedError("XXMust be overriddenXX")

    xǁHeaderLineParserBaseǁparse_key_value__mutmut_mutants = {
    'xǁHeaderLineParserBaseǁparse_key_value__mutmut_1': xǁHeaderLineParserBaseǁparse_key_value__mutmut_1
    }

    def parse_key_value(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderLineParserBaseǁparse_key_value__mutmut_orig"), object.__getattribute__(self, "xǁHeaderLineParserBaseǁparse_key_value__mutmut_mutants"), *args, **kwargs) 

    parse_key_value.__signature__ = _mutmut_signature(xǁHeaderLineParserBaseǁparse_key_value__mutmut_orig)
    xǁHeaderLineParserBaseǁparse_key_value__mutmut_orig.__name__ = 'xǁHeaderLineParserBaseǁparse_key_value'




class StupidHeaderLineParser(HeaderLineParserBase):
    """Parse into HeaderLine (no particular structure)"""

    def xǁStupidHeaderLineParserǁparse_key_value__mutmut_orig(self, key: str, value: str) -> header.HeaderLine:
        return header.HeaderLine(key, value)

    def xǁStupidHeaderLineParserǁparse_key_value__mutmut_1(self, key: str, value: str) -> header.HeaderLine:
        return header.HeaderLine(None, value)

    def xǁStupidHeaderLineParserǁparse_key_value__mutmut_2(self, key: str, value: str) -> header.HeaderLine:
        return header.HeaderLine(key, None)

    def xǁStupidHeaderLineParserǁparse_key_value__mutmut_3(self, key: str, value: str) -> header.HeaderLine:
        return header.HeaderLine( value)

    def xǁStupidHeaderLineParserǁparse_key_value__mutmut_4(self, key: str, value: str) -> header.HeaderLine:
        return header.HeaderLine(key,)

    xǁStupidHeaderLineParserǁparse_key_value__mutmut_mutants = {
    'xǁStupidHeaderLineParserǁparse_key_value__mutmut_1': xǁStupidHeaderLineParserǁparse_key_value__mutmut_1, 
        'xǁStupidHeaderLineParserǁparse_key_value__mutmut_2': xǁStupidHeaderLineParserǁparse_key_value__mutmut_2, 
        'xǁStupidHeaderLineParserǁparse_key_value__mutmut_3': xǁStupidHeaderLineParserǁparse_key_value__mutmut_3, 
        'xǁStupidHeaderLineParserǁparse_key_value__mutmut_4': xǁStupidHeaderLineParserǁparse_key_value__mutmut_4
    }

    def parse_key_value(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁStupidHeaderLineParserǁparse_key_value__mutmut_orig"), object.__getattribute__(self, "xǁStupidHeaderLineParserǁparse_key_value__mutmut_mutants"), *args, **kwargs) 

    parse_key_value.__signature__ = _mutmut_signature(xǁStupidHeaderLineParserǁparse_key_value__mutmut_orig)
    xǁStupidHeaderLineParserǁparse_key_value__mutmut_orig.__name__ = 'xǁStupidHeaderLineParserǁparse_key_value'




class MappingHeaderLineParser(HeaderLineParserBase):
    """Parse into HeaderLine (no particular structure)"""

    def xǁMappingHeaderLineParserǁ__init____mutmut_orig(self, line_class: Callable[[str, str, dict[str, bool | str | list[str]]], header.HeaderLine]):
        """Initialize the parser"""
        #: the class to use for the VCF header line
        self.line_class = line_class

    def xǁMappingHeaderLineParserǁ__init____mutmut_1(self, line_class: Callable[[str, str, dict[str, bool | str | list[str]]], header.HeaderLine]):
        """Initialize the parser"""
        #: the class to use for the VCF header line
        self.line_class = None

    xǁMappingHeaderLineParserǁ__init____mutmut_mutants = {
    'xǁMappingHeaderLineParserǁ__init____mutmut_1': xǁMappingHeaderLineParserǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁMappingHeaderLineParserǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁMappingHeaderLineParserǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁMappingHeaderLineParserǁ__init____mutmut_orig)
    xǁMappingHeaderLineParserǁ__init____mutmut_orig.__name__ = 'xǁMappingHeaderLineParserǁ__init__'



    def xǁMappingHeaderLineParserǁparse_key_value__mutmut_orig(self, key: str, value: str) -> header.HeaderLine:
        return self.line_class(key, value, parse_mapping(value))

    def xǁMappingHeaderLineParserǁparse_key_value__mutmut_1(self, key: str, value: str) -> header.HeaderLine:
        return self.line_class(None, value, parse_mapping(value))

    def xǁMappingHeaderLineParserǁparse_key_value__mutmut_2(self, key: str, value: str) -> header.HeaderLine:
        return self.line_class(key, None, parse_mapping(value))

    def xǁMappingHeaderLineParserǁparse_key_value__mutmut_3(self, key: str, value: str) -> header.HeaderLine:
        return self.line_class(key, value, parse_mapping(None))

    def xǁMappingHeaderLineParserǁparse_key_value__mutmut_4(self, key: str, value: str) -> header.HeaderLine:
        return self.line_class( value, parse_mapping(value))

    def xǁMappingHeaderLineParserǁparse_key_value__mutmut_5(self, key: str, value: str) -> header.HeaderLine:
        return self.line_class(key, parse_mapping(value))

    xǁMappingHeaderLineParserǁparse_key_value__mutmut_mutants = {
    'xǁMappingHeaderLineParserǁparse_key_value__mutmut_1': xǁMappingHeaderLineParserǁparse_key_value__mutmut_1, 
        'xǁMappingHeaderLineParserǁparse_key_value__mutmut_2': xǁMappingHeaderLineParserǁparse_key_value__mutmut_2, 
        'xǁMappingHeaderLineParserǁparse_key_value__mutmut_3': xǁMappingHeaderLineParserǁparse_key_value__mutmut_3, 
        'xǁMappingHeaderLineParserǁparse_key_value__mutmut_4': xǁMappingHeaderLineParserǁparse_key_value__mutmut_4, 
        'xǁMappingHeaderLineParserǁparse_key_value__mutmut_5': xǁMappingHeaderLineParserǁparse_key_value__mutmut_5
    }

    def parse_key_value(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁMappingHeaderLineParserǁparse_key_value__mutmut_orig"), object.__getattribute__(self, "xǁMappingHeaderLineParserǁparse_key_value__mutmut_mutants"), *args, **kwargs) 

    parse_key_value.__signature__ = _mutmut_signature(xǁMappingHeaderLineParserǁparse_key_value__mutmut_orig)
    xǁMappingHeaderLineParserǁparse_key_value__mutmut_orig.__name__ = 'xǁMappingHeaderLineParserǁparse_key_value'




def build_header_parsers__mutmut_orig() -> dict[str, HeaderLineParserBase]:
    """Return mapping for parsers to use for each VCF header type

    Inject the WarningHelper into the parsers.
    """
    result: dict[str, HeaderLineParserBase] = {
        "ALT": MappingHeaderLineParser(header.AltAlleleHeaderLine),
        "contig": MappingHeaderLineParser(header.ContigHeaderLine),
        "FILTER": MappingHeaderLineParser(header.FilterHeaderLine),
        "FORMAT": MappingHeaderLineParser(header.FormatHeaderLine),
        "INFO": MappingHeaderLineParser(header.InfoHeaderLine),
        "META": MappingHeaderLineParser(header.MetaHeaderLine),
        "PEDIGREE": MappingHeaderLineParser(header.PedigreeHeaderLine),
        "SAMPLE": MappingHeaderLineParser(header.SampleHeaderLine),
        "__default__": StupidHeaderLineParser(),  # fallback
    }
    return result


def build_header_parsers__mutmut_1() -> dict[str, HeaderLineParserBase]:
    """Return mapping for parsers to use for each VCF header type

    Inject the WarningHelper into the parsers.
    """
    result: dict[str, HeaderLineParserBase] = None
    return result

build_header_parsers__mutmut_mutants = {
'build_header_parsers__mutmut_1': build_header_parsers__mutmut_1
}

def build_header_parsers(*args, **kwargs):
    return _mutmut_trampoline(build_header_parsers__mutmut_orig, build_header_parsers__mutmut_mutants, *args, **kwargs) 

build_header_parsers.__signature__ = _mutmut_signature(build_header_parsers__mutmut_orig)
build_header_parsers__mutmut_orig.__name__ = 'build_header_parsers'




# Field value converters
_CONVERTERS: dict[
    Literal["Integer", "Float", "Flag", "Character", "String"], Callable[[str], bool | int | float | str]
] = {
    "Integer": int,
    "Float": float,
    "Flag": lambda x: True,
    "Character": str,
    "String": str,
}


def convert_field_value__mutmut_orig(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_1(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value != ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_2(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == "XX.XX":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_3(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ not in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_4(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("XXCharacterXX", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_5(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "XXStringXX"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_6(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "XX%XX" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_7(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" not in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_8(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(None, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_9(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, None)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_10(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace( v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_11(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k,)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_12(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = None
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_13(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[None](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_14(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](None)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_15(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("XX{} cannot be converted to {}, keeping as string.XX").format(value, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_16(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(None, type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_17(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value, None),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_18(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format( type_),
                exceptions.CannotConvertValue,
            )
            return value


def convert_field_value__mutmut_19(
    type_: Literal["Integer", "Float", "Flag", "Character", "String"], value: str
) -> bool | int | float | str | None:
    """Convert atomic field value according to the type"""
    if value == ".":
        return None
    elif type_ in ("Character", "String"):
        if "%" in value:
            for k, v in record.UNESCAPE_MAPPING:
                value = value.replace(k, v)
        return value
    else:
        try:
            return _CONVERTERS[type_](value)
        except ValueError:  # pragma: no cover
            warnings.warn(
                ("{} cannot be converted to {}, keeping as string.").format(value,),
                exceptions.CannotConvertValue,
            )
            return value

convert_field_value__mutmut_mutants = {
'convert_field_value__mutmut_1': convert_field_value__mutmut_1, 
    'convert_field_value__mutmut_2': convert_field_value__mutmut_2, 
    'convert_field_value__mutmut_3': convert_field_value__mutmut_3, 
    'convert_field_value__mutmut_4': convert_field_value__mutmut_4, 
    'convert_field_value__mutmut_5': convert_field_value__mutmut_5, 
    'convert_field_value__mutmut_6': convert_field_value__mutmut_6, 
    'convert_field_value__mutmut_7': convert_field_value__mutmut_7, 
    'convert_field_value__mutmut_8': convert_field_value__mutmut_8, 
    'convert_field_value__mutmut_9': convert_field_value__mutmut_9, 
    'convert_field_value__mutmut_10': convert_field_value__mutmut_10, 
    'convert_field_value__mutmut_11': convert_field_value__mutmut_11, 
    'convert_field_value__mutmut_12': convert_field_value__mutmut_12, 
    'convert_field_value__mutmut_13': convert_field_value__mutmut_13, 
    'convert_field_value__mutmut_14': convert_field_value__mutmut_14, 
    'convert_field_value__mutmut_15': convert_field_value__mutmut_15, 
    'convert_field_value__mutmut_16': convert_field_value__mutmut_16, 
    'convert_field_value__mutmut_17': convert_field_value__mutmut_17, 
    'convert_field_value__mutmut_18': convert_field_value__mutmut_18, 
    'convert_field_value__mutmut_19': convert_field_value__mutmut_19
}

def convert_field_value(*args, **kwargs):
    return _mutmut_trampoline(convert_field_value__mutmut_orig, convert_field_value__mutmut_mutants, *args, **kwargs) 

convert_field_value.__signature__ = _mutmut_signature(convert_field_value__mutmut_orig)
convert_field_value__mutmut_orig.__name__ = 'convert_field_value'




def parse_field_value__mutmut_orig(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_1(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type != "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_2(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "XXFlagXX":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_3(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) and field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_4(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return False
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_5(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id not in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_6(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("XXFORMAT/FTXX", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_7(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "XXFTXX"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_8(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split("XX;XX") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_9(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x == "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_10(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "XX.XX"]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_11(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number != 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_12(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 2:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_13(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, None)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_14(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type,)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_15(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value != ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_16(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == "XX.XX":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split(",")]


def parse_field_value__mutmut_17(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, None) for x in value.split(",")]


def parse_field_value__mutmut_18(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type,) for x in value.split(",")]


def parse_field_value__mutmut_19(
    field_info: header.FieldInfo, value: str | bool
) -> bool | int | float | str | list[bool | int | float | str | None] | None:
    """Parse ``value`` according to ``field_info``"""
    if isinstance(value, bool) or field_info.type == "Flag":
        return True
    elif field_info.id in ("FORMAT/FT", "FT"):
        return [x for x in value.split(";") if x != "."]
    elif field_info.number == 1:
        return convert_field_value(field_info.type, value)
    else:
        if value == ".":
            return []
        else:
            return [convert_field_value(field_info.type, x) for x in value.split("XX,XX")]

parse_field_value__mutmut_mutants = {
'parse_field_value__mutmut_1': parse_field_value__mutmut_1, 
    'parse_field_value__mutmut_2': parse_field_value__mutmut_2, 
    'parse_field_value__mutmut_3': parse_field_value__mutmut_3, 
    'parse_field_value__mutmut_4': parse_field_value__mutmut_4, 
    'parse_field_value__mutmut_5': parse_field_value__mutmut_5, 
    'parse_field_value__mutmut_6': parse_field_value__mutmut_6, 
    'parse_field_value__mutmut_7': parse_field_value__mutmut_7, 
    'parse_field_value__mutmut_8': parse_field_value__mutmut_8, 
    'parse_field_value__mutmut_9': parse_field_value__mutmut_9, 
    'parse_field_value__mutmut_10': parse_field_value__mutmut_10, 
    'parse_field_value__mutmut_11': parse_field_value__mutmut_11, 
    'parse_field_value__mutmut_12': parse_field_value__mutmut_12, 
    'parse_field_value__mutmut_13': parse_field_value__mutmut_13, 
    'parse_field_value__mutmut_14': parse_field_value__mutmut_14, 
    'parse_field_value__mutmut_15': parse_field_value__mutmut_15, 
    'parse_field_value__mutmut_16': parse_field_value__mutmut_16, 
    'parse_field_value__mutmut_17': parse_field_value__mutmut_17, 
    'parse_field_value__mutmut_18': parse_field_value__mutmut_18, 
    'parse_field_value__mutmut_19': parse_field_value__mutmut_19
}

def parse_field_value(*args, **kwargs):
    return _mutmut_trampoline(parse_field_value__mutmut_orig, parse_field_value__mutmut_mutants, *args, **kwargs) 

parse_field_value.__signature__ = _mutmut_signature(parse_field_value__mutmut_orig)
parse_field_value__mutmut_orig.__name__ = 'parse_field_value'




# Regular expression for break-end
BREAKEND_PATTERN = re.compile(r"[\[\]]")


def parse_breakend__mutmut_orig(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_1(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(None)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_2(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = None
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_3(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[2].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_4(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[None].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_5(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split("XX:XX", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_6(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 2)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_7(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = None
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_8(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(None)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_9(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = None
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_10(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[1] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_11(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[None] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_12(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] != "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_13(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "XX<XX":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_14(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[2:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_15(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:+1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_16(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-2]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_17(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[None]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_18(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = None
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_19(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = True
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_20(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = None
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_21(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = False
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_22(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = None
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_23(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {False: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_24(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, True: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_25(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = None
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_26(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[1] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_27(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[None] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_28(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] != "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_29(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "XX[XX" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_30(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[1] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_31(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[None] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_32(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] != "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_33(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "XX]XX"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_34(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" and alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_35(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[None]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_36(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = None
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_37(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["XX[XX" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_38(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" not in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_39(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV[None]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_40(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = None
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_41(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) or isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_42(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation != record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_43(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[3]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_44(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[None]
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_45(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = None
    else:
        sequence = arr[0]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_46(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[1]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_47(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = arr[None]
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)


def parse_breakend__mutmut_48(alt_str: str) -> tuple[str, int, str, Literal["+", "-"], str, bool]:
    """Parse breakend and return tuple with results, parameters for BreakEnd
    constructor
    """
    arr = BREAKEND_PATTERN.split(alt_str)
    assert isinstance(arr[1], str)
    mate_chrom, mate_pos = arr[1].split(":", 1)
    mate_pos = int(mate_pos)
    if mate_chrom[0] == "<":
        mate_chrom = mate_chrom[1:-1]
        within_main_assembly = False
    else:
        within_main_assembly = True
    FWD_REV: dict[bool, Literal["+", "-"]] = {True: record.FORWARD, False: record.REVERSE}
    orientation = FWD_REV[alt_str[0] == "[" or alt_str[0] == "]"]
    mate_orientation = FWD_REV["[" in alt_str]
    assert isinstance(arr[2], str) and isinstance(arr[0], str)
    if orientation == record.FORWARD:
        sequence = arr[2]
    else:
        sequence = None
    return (mate_chrom, mate_pos, orientation, mate_orientation, sequence, within_main_assembly)

parse_breakend__mutmut_mutants = {
'parse_breakend__mutmut_1': parse_breakend__mutmut_1, 
    'parse_breakend__mutmut_2': parse_breakend__mutmut_2, 
    'parse_breakend__mutmut_3': parse_breakend__mutmut_3, 
    'parse_breakend__mutmut_4': parse_breakend__mutmut_4, 
    'parse_breakend__mutmut_5': parse_breakend__mutmut_5, 
    'parse_breakend__mutmut_6': parse_breakend__mutmut_6, 
    'parse_breakend__mutmut_7': parse_breakend__mutmut_7, 
    'parse_breakend__mutmut_8': parse_breakend__mutmut_8, 
    'parse_breakend__mutmut_9': parse_breakend__mutmut_9, 
    'parse_breakend__mutmut_10': parse_breakend__mutmut_10, 
    'parse_breakend__mutmut_11': parse_breakend__mutmut_11, 
    'parse_breakend__mutmut_12': parse_breakend__mutmut_12, 
    'parse_breakend__mutmut_13': parse_breakend__mutmut_13, 
    'parse_breakend__mutmut_14': parse_breakend__mutmut_14, 
    'parse_breakend__mutmut_15': parse_breakend__mutmut_15, 
    'parse_breakend__mutmut_16': parse_breakend__mutmut_16, 
    'parse_breakend__mutmut_17': parse_breakend__mutmut_17, 
    'parse_breakend__mutmut_18': parse_breakend__mutmut_18, 
    'parse_breakend__mutmut_19': parse_breakend__mutmut_19, 
    'parse_breakend__mutmut_20': parse_breakend__mutmut_20, 
    'parse_breakend__mutmut_21': parse_breakend__mutmut_21, 
    'parse_breakend__mutmut_22': parse_breakend__mutmut_22, 
    'parse_breakend__mutmut_23': parse_breakend__mutmut_23, 
    'parse_breakend__mutmut_24': parse_breakend__mutmut_24, 
    'parse_breakend__mutmut_25': parse_breakend__mutmut_25, 
    'parse_breakend__mutmut_26': parse_breakend__mutmut_26, 
    'parse_breakend__mutmut_27': parse_breakend__mutmut_27, 
    'parse_breakend__mutmut_28': parse_breakend__mutmut_28, 
    'parse_breakend__mutmut_29': parse_breakend__mutmut_29, 
    'parse_breakend__mutmut_30': parse_breakend__mutmut_30, 
    'parse_breakend__mutmut_31': parse_breakend__mutmut_31, 
    'parse_breakend__mutmut_32': parse_breakend__mutmut_32, 
    'parse_breakend__mutmut_33': parse_breakend__mutmut_33, 
    'parse_breakend__mutmut_34': parse_breakend__mutmut_34, 
    'parse_breakend__mutmut_35': parse_breakend__mutmut_35, 
    'parse_breakend__mutmut_36': parse_breakend__mutmut_36, 
    'parse_breakend__mutmut_37': parse_breakend__mutmut_37, 
    'parse_breakend__mutmut_38': parse_breakend__mutmut_38, 
    'parse_breakend__mutmut_39': parse_breakend__mutmut_39, 
    'parse_breakend__mutmut_40': parse_breakend__mutmut_40, 
    'parse_breakend__mutmut_41': parse_breakend__mutmut_41, 
    'parse_breakend__mutmut_42': parse_breakend__mutmut_42, 
    'parse_breakend__mutmut_43': parse_breakend__mutmut_43, 
    'parse_breakend__mutmut_44': parse_breakend__mutmut_44, 
    'parse_breakend__mutmut_45': parse_breakend__mutmut_45, 
    'parse_breakend__mutmut_46': parse_breakend__mutmut_46, 
    'parse_breakend__mutmut_47': parse_breakend__mutmut_47, 
    'parse_breakend__mutmut_48': parse_breakend__mutmut_48
}

def parse_breakend(*args, **kwargs):
    return _mutmut_trampoline(parse_breakend__mutmut_orig, parse_breakend__mutmut_mutants, *args, **kwargs) 

parse_breakend.__signature__ = _mutmut_signature(parse_breakend__mutmut_orig)
parse_breakend__mutmut_orig.__name__ = 'parse_breakend'




def process_sub_grow__mutmut_orig(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_1(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) != 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_2(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 1:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_3(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("XXInvalid VCF, empty ALTXX")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_4(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) != 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_5(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 2:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_6(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[1] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_7(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[None] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_8(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] != alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_9(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[1]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_10(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[None]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_11(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, None)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_12(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL,)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_13(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, None)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_14(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL,)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_grow__mutmut_15(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, None)


def process_sub_grow__mutmut_16(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string grows"""
    if len(alt_str) == 0:
        raise exceptions.InvalidRecordException("Invalid VCF, empty ALT")
    elif len(alt_str) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.DEL, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL,)

process_sub_grow__mutmut_mutants = {
'process_sub_grow__mutmut_1': process_sub_grow__mutmut_1, 
    'process_sub_grow__mutmut_2': process_sub_grow__mutmut_2, 
    'process_sub_grow__mutmut_3': process_sub_grow__mutmut_3, 
    'process_sub_grow__mutmut_4': process_sub_grow__mutmut_4, 
    'process_sub_grow__mutmut_5': process_sub_grow__mutmut_5, 
    'process_sub_grow__mutmut_6': process_sub_grow__mutmut_6, 
    'process_sub_grow__mutmut_7': process_sub_grow__mutmut_7, 
    'process_sub_grow__mutmut_8': process_sub_grow__mutmut_8, 
    'process_sub_grow__mutmut_9': process_sub_grow__mutmut_9, 
    'process_sub_grow__mutmut_10': process_sub_grow__mutmut_10, 
    'process_sub_grow__mutmut_11': process_sub_grow__mutmut_11, 
    'process_sub_grow__mutmut_12': process_sub_grow__mutmut_12, 
    'process_sub_grow__mutmut_13': process_sub_grow__mutmut_13, 
    'process_sub_grow__mutmut_14': process_sub_grow__mutmut_14, 
    'process_sub_grow__mutmut_15': process_sub_grow__mutmut_15, 
    'process_sub_grow__mutmut_16': process_sub_grow__mutmut_16
}

def process_sub_grow(*args, **kwargs):
    return _mutmut_trampoline(process_sub_grow__mutmut_orig, process_sub_grow__mutmut_mutants, *args, **kwargs) 

process_sub_grow.__signature__ = _mutmut_signature(process_sub_grow__mutmut_orig)
process_sub_grow__mutmut_orig.__name__ = 'process_sub_grow'




def process_sub_shrink__mutmut_orig(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_1(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) != 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_2(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 1:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_3(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("XXInvalid VCF, empty REFXX")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_4(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) != 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_5(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 2:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_6(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[1] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_7(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[None] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_8(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] != alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_9(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[1]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_10(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[None]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_11(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, None)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_12(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS,)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_13(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, None)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_14(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL,)
    else:
        return record.Substitution(record.INDEL, alt_str)


def process_sub_shrink__mutmut_15(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL, None)


def process_sub_shrink__mutmut_16(ref: str, alt_str: str) -> record.Substitution:
    """Process substution where the string shrink"""
    if len(ref) == 0:  # pragma: no cover
        raise exceptions.InvalidRecordException("Invalid VCF, empty REF")
    elif len(ref) == 1:
        if ref[0] == alt_str[0]:
            return record.Substitution(record.INS, alt_str)
        else:
            return record.Substitution(record.INDEL, alt_str)
    else:
        return record.Substitution(record.INDEL,)

process_sub_shrink__mutmut_mutants = {
'process_sub_shrink__mutmut_1': process_sub_shrink__mutmut_1, 
    'process_sub_shrink__mutmut_2': process_sub_shrink__mutmut_2, 
    'process_sub_shrink__mutmut_3': process_sub_shrink__mutmut_3, 
    'process_sub_shrink__mutmut_4': process_sub_shrink__mutmut_4, 
    'process_sub_shrink__mutmut_5': process_sub_shrink__mutmut_5, 
    'process_sub_shrink__mutmut_6': process_sub_shrink__mutmut_6, 
    'process_sub_shrink__mutmut_7': process_sub_shrink__mutmut_7, 
    'process_sub_shrink__mutmut_8': process_sub_shrink__mutmut_8, 
    'process_sub_shrink__mutmut_9': process_sub_shrink__mutmut_9, 
    'process_sub_shrink__mutmut_10': process_sub_shrink__mutmut_10, 
    'process_sub_shrink__mutmut_11': process_sub_shrink__mutmut_11, 
    'process_sub_shrink__mutmut_12': process_sub_shrink__mutmut_12, 
    'process_sub_shrink__mutmut_13': process_sub_shrink__mutmut_13, 
    'process_sub_shrink__mutmut_14': process_sub_shrink__mutmut_14, 
    'process_sub_shrink__mutmut_15': process_sub_shrink__mutmut_15, 
    'process_sub_shrink__mutmut_16': process_sub_shrink__mutmut_16
}

def process_sub_shrink(*args, **kwargs):
    return _mutmut_trampoline(process_sub_shrink__mutmut_orig, process_sub_shrink__mutmut_mutants, *args, **kwargs) 

process_sub_shrink.__signature__ = _mutmut_signature(process_sub_shrink__mutmut_orig)
process_sub_shrink__mutmut_orig.__name__ = 'process_sub_shrink'




def process_sub__mutmut_orig(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_1(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) != len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_2(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) != 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_3(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 2:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_4(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, None)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_5(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV,)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_6(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, None)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_7(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV,)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_8(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) >= len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_9(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(None, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_10(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, None)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_11(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow( alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_12(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref,)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, alt_str)


def process_sub__mutmut_13(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(None, alt_str)


def process_sub__mutmut_14(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref, None)


def process_sub__mutmut_15(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink( alt_str)


def process_sub__mutmut_16(ref: str, alt_str: str) -> record.Substitution:
    """Process substitution"""
    if len(ref) == len(alt_str):
        if len(ref) == 1:
            return record.Substitution(record.SNV, alt_str)
        else:
            return record.Substitution(record.MNV, alt_str)
    elif len(ref) > len(alt_str):
        return process_sub_grow(ref, alt_str)
    else:  # len(ref) < len(alt_str):
        return process_sub_shrink(ref,)

process_sub__mutmut_mutants = {
'process_sub__mutmut_1': process_sub__mutmut_1, 
    'process_sub__mutmut_2': process_sub__mutmut_2, 
    'process_sub__mutmut_3': process_sub__mutmut_3, 
    'process_sub__mutmut_4': process_sub__mutmut_4, 
    'process_sub__mutmut_5': process_sub__mutmut_5, 
    'process_sub__mutmut_6': process_sub__mutmut_6, 
    'process_sub__mutmut_7': process_sub__mutmut_7, 
    'process_sub__mutmut_8': process_sub__mutmut_8, 
    'process_sub__mutmut_9': process_sub__mutmut_9, 
    'process_sub__mutmut_10': process_sub__mutmut_10, 
    'process_sub__mutmut_11': process_sub__mutmut_11, 
    'process_sub__mutmut_12': process_sub__mutmut_12, 
    'process_sub__mutmut_13': process_sub__mutmut_13, 
    'process_sub__mutmut_14': process_sub__mutmut_14, 
    'process_sub__mutmut_15': process_sub__mutmut_15, 
    'process_sub__mutmut_16': process_sub__mutmut_16
}

def process_sub(*args, **kwargs):
    return _mutmut_trampoline(process_sub__mutmut_orig, process_sub__mutmut_mutants, *args, **kwargs) 

process_sub.__signature__ = _mutmut_signature(process_sub__mutmut_orig)
process_sub__mutmut_orig.__name__ = 'process_sub'




def process_alt__mutmut_orig(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_1(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "XX]XX" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_2(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" not in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_3(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "XX[XX" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_4(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" not in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_5(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str and "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_6(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(None))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_7(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_8(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[None] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_9(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] != "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_10(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "XX.XX" and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_11(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) >= 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_12(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 1:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_13(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." or len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_14(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[2:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_15(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[None])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_16(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[+1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_17(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-2] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_18(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[None] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_19(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] != "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_20(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "XX.XX" and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_21(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) >= 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_22(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 1:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_23(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." or len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_24(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:+1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_25(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-2])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_26(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[None])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_27(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[1] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_28(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[None] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_29(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] != "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_30(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "XX<XX" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_31(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[+1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_32(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-2] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_33(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[None] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_34(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] != ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_35(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == "XX>XX":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_36(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" or alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_37(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[2:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_38(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:+1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_39(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-2]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_40(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[None]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_41(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = None
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_42(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(None)
    else:  # substitution
        return process_sub(ref, alt_str)


def process_alt__mutmut_43(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(None, alt_str)


def process_alt__mutmut_44(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref, None)


def process_alt__mutmut_45(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub( alt_str)


def process_alt__mutmut_46(header: header.Header, ref: str, alt_str: str) -> record.AltRecord:
    """Process alternative value using Header in ``header``"""
    # By its nature, this function contains a large number of case distinctions
    if "]" in alt_str or "[" in alt_str:
        return record.BreakEnd(*parse_breakend(alt_str))
    elif alt_str[0] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.FORWARD, alt_str[1:])
    elif alt_str[-1] == "." and len(alt_str) > 0:
        return record.SingleBreakEnd(record.REVERSE, alt_str[:-1])
    elif alt_str[0] == "<" and alt_str[-1] == ">":
        inner = alt_str[1:-1]
        return record.SymbolicAllele(inner)
    else:  # substitution
        return process_sub(ref,)

process_alt__mutmut_mutants = {
'process_alt__mutmut_1': process_alt__mutmut_1, 
    'process_alt__mutmut_2': process_alt__mutmut_2, 
    'process_alt__mutmut_3': process_alt__mutmut_3, 
    'process_alt__mutmut_4': process_alt__mutmut_4, 
    'process_alt__mutmut_5': process_alt__mutmut_5, 
    'process_alt__mutmut_6': process_alt__mutmut_6, 
    'process_alt__mutmut_7': process_alt__mutmut_7, 
    'process_alt__mutmut_8': process_alt__mutmut_8, 
    'process_alt__mutmut_9': process_alt__mutmut_9, 
    'process_alt__mutmut_10': process_alt__mutmut_10, 
    'process_alt__mutmut_11': process_alt__mutmut_11, 
    'process_alt__mutmut_12': process_alt__mutmut_12, 
    'process_alt__mutmut_13': process_alt__mutmut_13, 
    'process_alt__mutmut_14': process_alt__mutmut_14, 
    'process_alt__mutmut_15': process_alt__mutmut_15, 
    'process_alt__mutmut_16': process_alt__mutmut_16, 
    'process_alt__mutmut_17': process_alt__mutmut_17, 
    'process_alt__mutmut_18': process_alt__mutmut_18, 
    'process_alt__mutmut_19': process_alt__mutmut_19, 
    'process_alt__mutmut_20': process_alt__mutmut_20, 
    'process_alt__mutmut_21': process_alt__mutmut_21, 
    'process_alt__mutmut_22': process_alt__mutmut_22, 
    'process_alt__mutmut_23': process_alt__mutmut_23, 
    'process_alt__mutmut_24': process_alt__mutmut_24, 
    'process_alt__mutmut_25': process_alt__mutmut_25, 
    'process_alt__mutmut_26': process_alt__mutmut_26, 
    'process_alt__mutmut_27': process_alt__mutmut_27, 
    'process_alt__mutmut_28': process_alt__mutmut_28, 
    'process_alt__mutmut_29': process_alt__mutmut_29, 
    'process_alt__mutmut_30': process_alt__mutmut_30, 
    'process_alt__mutmut_31': process_alt__mutmut_31, 
    'process_alt__mutmut_32': process_alt__mutmut_32, 
    'process_alt__mutmut_33': process_alt__mutmut_33, 
    'process_alt__mutmut_34': process_alt__mutmut_34, 
    'process_alt__mutmut_35': process_alt__mutmut_35, 
    'process_alt__mutmut_36': process_alt__mutmut_36, 
    'process_alt__mutmut_37': process_alt__mutmut_37, 
    'process_alt__mutmut_38': process_alt__mutmut_38, 
    'process_alt__mutmut_39': process_alt__mutmut_39, 
    'process_alt__mutmut_40': process_alt__mutmut_40, 
    'process_alt__mutmut_41': process_alt__mutmut_41, 
    'process_alt__mutmut_42': process_alt__mutmut_42, 
    'process_alt__mutmut_43': process_alt__mutmut_43, 
    'process_alt__mutmut_44': process_alt__mutmut_44, 
    'process_alt__mutmut_45': process_alt__mutmut_45, 
    'process_alt__mutmut_46': process_alt__mutmut_46
}

def process_alt(*args, **kwargs):
    return _mutmut_trampoline(process_alt__mutmut_orig, process_alt__mutmut_mutants, *args, **kwargs) 

process_alt.__signature__ = _mutmut_signature(process_alt__mutmut_orig)
process_alt__mutmut_orig.__name__ = 'process_alt'




class HeaderParser:
    """Helper class for parsing a VCF header"""

    def xǁHeaderParserǁ__init____mutmut_orig(self):
        #: Sub parsers to use for parsing the header lines
        self.sub_parsers = build_header_parsers()

    def xǁHeaderParserǁ__init____mutmut_1(self):
        #: Sub parsers to use for parsing the header lines
        self.sub_parsers = None

    xǁHeaderParserǁ__init____mutmut_mutants = {
    'xǁHeaderParserǁ__init____mutmut_1': xǁHeaderParserǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderParserǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHeaderParserǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁHeaderParserǁ__init____mutmut_orig)
    xǁHeaderParserǁ__init____mutmut_orig.__name__ = 'xǁHeaderParserǁ__init__'



    def xǁHeaderParserǁparse_line__mutmut_orig(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_1(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if  line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_2(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or  line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_3(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("XX##XX"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_4(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line and not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_5(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('XXInvalid VCF header line (must start with "##") {}XX'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_6(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(None))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_7(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "XX=XX" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_8(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "="  in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_9(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('XXInvalid VCF header line (must contain "=") {}XX'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_10(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(None))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_11(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[None].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_12(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = None  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_13(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(None)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_14(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = None
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_15(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(None, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_16(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["XX__default__XX"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_17(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers[None])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_18(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get( self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_19(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = None
        return sub_parser.parse_key_value(key, value)

    def xǁHeaderParserǁparse_line__mutmut_20(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(None, value)

    def xǁHeaderParserǁparse_line__mutmut_21(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key, None)

    def xǁHeaderParserǁparse_line__mutmut_22(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value( value)

    def xǁHeaderParserǁparse_line__mutmut_23(self, line: str) -> header.HeaderLine:
        """Parse VCF header ``line`` (trailing '\r\n' or '\n' is ignored)

        :param str line: ``str`` with line to parse
        :param dict sub_parsers: ``dict`` mapping header line types to
            appropriate parser objects
        :returns: appropriate :py:class:`HeaderLine` parsed from ``line``
        :raises: :py:class:`vcfpy.exceptions.InvalidHeaderException` if
            there was a problem parsing the file
        """
        if not line or not line.startswith("##"):  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must start with "##") {}'.format(line))
        if "=" not in line:  # pragma: no cover
            raise exceptions.InvalidHeaderException('Invalid VCF header line (must contain "=") {}'.format(line))
        line = line[len("##") :].rstrip()  # trim '^##' and trailing whitespace
        # split key/value pair at "="
        key, value = split_mapping(line)
        sub_parser = self.sub_parsers.get(key, self.sub_parsers["__default__"])
        return sub_parser.parse_key_value(key,)

    xǁHeaderParserǁparse_line__mutmut_mutants = {
    'xǁHeaderParserǁparse_line__mutmut_1': xǁHeaderParserǁparse_line__mutmut_1, 
        'xǁHeaderParserǁparse_line__mutmut_2': xǁHeaderParserǁparse_line__mutmut_2, 
        'xǁHeaderParserǁparse_line__mutmut_3': xǁHeaderParserǁparse_line__mutmut_3, 
        'xǁHeaderParserǁparse_line__mutmut_4': xǁHeaderParserǁparse_line__mutmut_4, 
        'xǁHeaderParserǁparse_line__mutmut_5': xǁHeaderParserǁparse_line__mutmut_5, 
        'xǁHeaderParserǁparse_line__mutmut_6': xǁHeaderParserǁparse_line__mutmut_6, 
        'xǁHeaderParserǁparse_line__mutmut_7': xǁHeaderParserǁparse_line__mutmut_7, 
        'xǁHeaderParserǁparse_line__mutmut_8': xǁHeaderParserǁparse_line__mutmut_8, 
        'xǁHeaderParserǁparse_line__mutmut_9': xǁHeaderParserǁparse_line__mutmut_9, 
        'xǁHeaderParserǁparse_line__mutmut_10': xǁHeaderParserǁparse_line__mutmut_10, 
        'xǁHeaderParserǁparse_line__mutmut_11': xǁHeaderParserǁparse_line__mutmut_11, 
        'xǁHeaderParserǁparse_line__mutmut_12': xǁHeaderParserǁparse_line__mutmut_12, 
        'xǁHeaderParserǁparse_line__mutmut_13': xǁHeaderParserǁparse_line__mutmut_13, 
        'xǁHeaderParserǁparse_line__mutmut_14': xǁHeaderParserǁparse_line__mutmut_14, 
        'xǁHeaderParserǁparse_line__mutmut_15': xǁHeaderParserǁparse_line__mutmut_15, 
        'xǁHeaderParserǁparse_line__mutmut_16': xǁHeaderParserǁparse_line__mutmut_16, 
        'xǁHeaderParserǁparse_line__mutmut_17': xǁHeaderParserǁparse_line__mutmut_17, 
        'xǁHeaderParserǁparse_line__mutmut_18': xǁHeaderParserǁparse_line__mutmut_18, 
        'xǁHeaderParserǁparse_line__mutmut_19': xǁHeaderParserǁparse_line__mutmut_19, 
        'xǁHeaderParserǁparse_line__mutmut_20': xǁHeaderParserǁparse_line__mutmut_20, 
        'xǁHeaderParserǁparse_line__mutmut_21': xǁHeaderParserǁparse_line__mutmut_21, 
        'xǁHeaderParserǁparse_line__mutmut_22': xǁHeaderParserǁparse_line__mutmut_22, 
        'xǁHeaderParserǁparse_line__mutmut_23': xǁHeaderParserǁparse_line__mutmut_23
    }

    def parse_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderParserǁparse_line__mutmut_orig"), object.__getattribute__(self, "xǁHeaderParserǁparse_line__mutmut_mutants"), *args, **kwargs) 

    parse_line.__signature__ = _mutmut_signature(xǁHeaderParserǁparse_line__mutmut_orig)
    xǁHeaderParserǁparse_line__mutmut_orig.__name__ = 'xǁHeaderParserǁparse_line'




class RecordParser:
    """Helper class for parsing VCF records"""

    def xǁRecordParserǁ__init____mutmut_orig(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_1(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = None
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_2(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = None
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_3(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks and [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_4(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = None
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_5(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 10 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_6(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 - len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_7(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = None
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_8(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 9
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_9(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = None
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_10(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = None
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_11(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = None
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_12(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "XXINFOXX" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_13(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" not in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_14(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = None
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_15(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = None
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_16(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "XXFORMATXX" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_17(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" not in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_18(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = None
        else:
            self._format_checker = NoopFormatChecker()

    def xǁRecordParserǁ__init____mutmut_19(
        self,
        header: header.Header,
        samples: header.SamplesInfos,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        #: Header with the meta information
        self.header = header
        #: SamplesInfos with sample information
        self.samples = samples
        #: The checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or [])
        # Expected number of fields
        if self.samples.names:
            self.expected_fields = 9 + len(self.samples.names)
        else:
            self.expected_fields = 8
        # Cache of FieldInfo objects by FORMAT string
        self._format_cache: dict[str, list["header.FieldInfo"]] = {}
        # Cache of FILTER entries, also applied to FORMAT/FT
        self._filter_ids = set(self.header.filter_ids())
        # Helper for checking INFO fields
        if "INFO" in self.record_checks:
            self._info_checker = InfoChecker(self.header)
        else:
            self._info_checker = NoopInfoChecker()
        # Helper for checking FORMAT fields
        if "FORMAT" in self.record_checks:
            self._format_checker = FormatChecker(self.header)
        else:
            self._format_checker = None

    xǁRecordParserǁ__init____mutmut_mutants = {
    'xǁRecordParserǁ__init____mutmut_1': xǁRecordParserǁ__init____mutmut_1, 
        'xǁRecordParserǁ__init____mutmut_2': xǁRecordParserǁ__init____mutmut_2, 
        'xǁRecordParserǁ__init____mutmut_3': xǁRecordParserǁ__init____mutmut_3, 
        'xǁRecordParserǁ__init____mutmut_4': xǁRecordParserǁ__init____mutmut_4, 
        'xǁRecordParserǁ__init____mutmut_5': xǁRecordParserǁ__init____mutmut_5, 
        'xǁRecordParserǁ__init____mutmut_6': xǁRecordParserǁ__init____mutmut_6, 
        'xǁRecordParserǁ__init____mutmut_7': xǁRecordParserǁ__init____mutmut_7, 
        'xǁRecordParserǁ__init____mutmut_8': xǁRecordParserǁ__init____mutmut_8, 
        'xǁRecordParserǁ__init____mutmut_9': xǁRecordParserǁ__init____mutmut_9, 
        'xǁRecordParserǁ__init____mutmut_10': xǁRecordParserǁ__init____mutmut_10, 
        'xǁRecordParserǁ__init____mutmut_11': xǁRecordParserǁ__init____mutmut_11, 
        'xǁRecordParserǁ__init____mutmut_12': xǁRecordParserǁ__init____mutmut_12, 
        'xǁRecordParserǁ__init____mutmut_13': xǁRecordParserǁ__init____mutmut_13, 
        'xǁRecordParserǁ__init____mutmut_14': xǁRecordParserǁ__init____mutmut_14, 
        'xǁRecordParserǁ__init____mutmut_15': xǁRecordParserǁ__init____mutmut_15, 
        'xǁRecordParserǁ__init____mutmut_16': xǁRecordParserǁ__init____mutmut_16, 
        'xǁRecordParserǁ__init____mutmut_17': xǁRecordParserǁ__init____mutmut_17, 
        'xǁRecordParserǁ__init____mutmut_18': xǁRecordParserǁ__init____mutmut_18, 
        'xǁRecordParserǁ__init____mutmut_19': xǁRecordParserǁ__init____mutmut_19
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁRecordParserǁ__init____mutmut_orig)
    xǁRecordParserǁ__init____mutmut_orig.__name__ = 'xǁRecordParserǁ__init__'



    def xǁRecordParserǁparse_line__mutmut_orig(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_1(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = None
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_2(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if  line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_3(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(None)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_4(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = None
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_5(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[1]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_6(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[None]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_7(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = None
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_8(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[2])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_9(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[None])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_10(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = None
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_11(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[3] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_12(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[None] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_13(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] != ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_14(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == "XX.XX":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_15(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = None
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_16(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[3].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_17(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[None].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_18(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split("XX;XX")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_19(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = None
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_20(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[4]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_21(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[None]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_22(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = None
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_23(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = None
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_24(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[5] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_25(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[None] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_26(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] == ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_27(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != "XX.XX":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_28(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[5].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_29(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[None].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_30(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split("XX,XX"):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_31(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, None, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_32(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, None))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_33(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_34(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref,))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_35(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[6] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_36(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[None] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_37(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] != ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_38(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == "XX.XX":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_39(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = ""
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_40(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[6])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_41(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[None])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_42(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = None
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_43(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[6])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_44(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[None])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_45(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = None
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_46(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[7] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_47(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[None] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_48(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] != ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_49(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == "XX.XX":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_50(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = None
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_51(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[7].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_52(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[None].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_53(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split("XX;XX")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_54(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = None
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_55(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(None, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_56(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "XXFILTERXX")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_57(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters( "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_58(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[8], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_59(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[None], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_60(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = None
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_61(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) != 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_62(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 10:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_63(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("XXExpected 8 or 10+ columns, got 9!XX")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_64(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) != 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_65(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 9:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_66(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = ""
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_67(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = ""
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_68(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[9].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_69(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[None].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_70(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split("XX:XX")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_71(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = None
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_72(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(None, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_73(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, None, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_74(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[9], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_75(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[None], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_76(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], None)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_77(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls( format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_78(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_79(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8],)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_80(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = None
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_81(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(None, pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_82(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, None, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_83(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, None, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_84(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, None, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_85(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, None, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_86(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, None, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_87(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, None, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_88(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, None, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_89(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, None, calls)

    def xǁRecordParserǁparse_line__mutmut_90(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_, None)

    def xǁRecordParserǁparse_line__mutmut_91(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record( pos, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_92(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, ids, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_93(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ref, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_94(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, alts, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_95(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, qual, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_96(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, filt, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_97(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, info, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_98(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, format_, calls)

    def xǁRecordParserǁparse_line__mutmut_99(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, calls)

    def xǁRecordParserǁparse_line__mutmut_100(self, line_str: str) -> "record.Record | None":
        """Parse line from file (including trailing line break) and return
        resulting Record
        """
        line_str = line_str.rstrip()
        if not line_str:
            return None  # empty line, EOF
        arr = self._split_line(line_str)
        # CHROM
        chrom = arr[0]
        # POS
        pos = int(arr[1])
        # IDS
        if arr[2] == ".":
            ids = []
        else:
            ids = arr[2].split(";")
        # REF
        ref = arr[3]
        # ALT
        alts: list[record.AltRecord] = []
        if arr[4] != ".":
            for alt in arr[4].split(","):
                alts.append(process_alt(self.header, ref, alt))
        # QUAL
        if arr[5] == ".":
            qual = None
        else:
            try:
                qual = int(arr[5])
            except ValueError:  # try as float  # pragma: no cover
                qual = float(arr[5])
        # FILTER
        if arr[6] == ".":
            filt = []
        else:
            filt = arr[6].split(";")
        self._check_filters(filt, "FILTER")
        # INFO
        info = self._parse_info(arr[7], len(alts))
        if len(arr) == 9:
            raise exceptions.IncorrectVCFFormat("Expected 8 or 10+ columns, got 9!")  # pragma: no cover
        elif len(arr) == 8:
            format_ = None
            calls = None
        else:
            # FORMAT
            format_ = arr[8].split(":")
            # sample/call columns
            calls = self._handle_calls(alts, format_, arr[8], arr)
        return record.Record(chrom, pos, ids, ref, alts, qual, filt, info, format_,)

    xǁRecordParserǁparse_line__mutmut_mutants = {
    'xǁRecordParserǁparse_line__mutmut_1': xǁRecordParserǁparse_line__mutmut_1, 
        'xǁRecordParserǁparse_line__mutmut_2': xǁRecordParserǁparse_line__mutmut_2, 
        'xǁRecordParserǁparse_line__mutmut_3': xǁRecordParserǁparse_line__mutmut_3, 
        'xǁRecordParserǁparse_line__mutmut_4': xǁRecordParserǁparse_line__mutmut_4, 
        'xǁRecordParserǁparse_line__mutmut_5': xǁRecordParserǁparse_line__mutmut_5, 
        'xǁRecordParserǁparse_line__mutmut_6': xǁRecordParserǁparse_line__mutmut_6, 
        'xǁRecordParserǁparse_line__mutmut_7': xǁRecordParserǁparse_line__mutmut_7, 
        'xǁRecordParserǁparse_line__mutmut_8': xǁRecordParserǁparse_line__mutmut_8, 
        'xǁRecordParserǁparse_line__mutmut_9': xǁRecordParserǁparse_line__mutmut_9, 
        'xǁRecordParserǁparse_line__mutmut_10': xǁRecordParserǁparse_line__mutmut_10, 
        'xǁRecordParserǁparse_line__mutmut_11': xǁRecordParserǁparse_line__mutmut_11, 
        'xǁRecordParserǁparse_line__mutmut_12': xǁRecordParserǁparse_line__mutmut_12, 
        'xǁRecordParserǁparse_line__mutmut_13': xǁRecordParserǁparse_line__mutmut_13, 
        'xǁRecordParserǁparse_line__mutmut_14': xǁRecordParserǁparse_line__mutmut_14, 
        'xǁRecordParserǁparse_line__mutmut_15': xǁRecordParserǁparse_line__mutmut_15, 
        'xǁRecordParserǁparse_line__mutmut_16': xǁRecordParserǁparse_line__mutmut_16, 
        'xǁRecordParserǁparse_line__mutmut_17': xǁRecordParserǁparse_line__mutmut_17, 
        'xǁRecordParserǁparse_line__mutmut_18': xǁRecordParserǁparse_line__mutmut_18, 
        'xǁRecordParserǁparse_line__mutmut_19': xǁRecordParserǁparse_line__mutmut_19, 
        'xǁRecordParserǁparse_line__mutmut_20': xǁRecordParserǁparse_line__mutmut_20, 
        'xǁRecordParserǁparse_line__mutmut_21': xǁRecordParserǁparse_line__mutmut_21, 
        'xǁRecordParserǁparse_line__mutmut_22': xǁRecordParserǁparse_line__mutmut_22, 
        'xǁRecordParserǁparse_line__mutmut_23': xǁRecordParserǁparse_line__mutmut_23, 
        'xǁRecordParserǁparse_line__mutmut_24': xǁRecordParserǁparse_line__mutmut_24, 
        'xǁRecordParserǁparse_line__mutmut_25': xǁRecordParserǁparse_line__mutmut_25, 
        'xǁRecordParserǁparse_line__mutmut_26': xǁRecordParserǁparse_line__mutmut_26, 
        'xǁRecordParserǁparse_line__mutmut_27': xǁRecordParserǁparse_line__mutmut_27, 
        'xǁRecordParserǁparse_line__mutmut_28': xǁRecordParserǁparse_line__mutmut_28, 
        'xǁRecordParserǁparse_line__mutmut_29': xǁRecordParserǁparse_line__mutmut_29, 
        'xǁRecordParserǁparse_line__mutmut_30': xǁRecordParserǁparse_line__mutmut_30, 
        'xǁRecordParserǁparse_line__mutmut_31': xǁRecordParserǁparse_line__mutmut_31, 
        'xǁRecordParserǁparse_line__mutmut_32': xǁRecordParserǁparse_line__mutmut_32, 
        'xǁRecordParserǁparse_line__mutmut_33': xǁRecordParserǁparse_line__mutmut_33, 
        'xǁRecordParserǁparse_line__mutmut_34': xǁRecordParserǁparse_line__mutmut_34, 
        'xǁRecordParserǁparse_line__mutmut_35': xǁRecordParserǁparse_line__mutmut_35, 
        'xǁRecordParserǁparse_line__mutmut_36': xǁRecordParserǁparse_line__mutmut_36, 
        'xǁRecordParserǁparse_line__mutmut_37': xǁRecordParserǁparse_line__mutmut_37, 
        'xǁRecordParserǁparse_line__mutmut_38': xǁRecordParserǁparse_line__mutmut_38, 
        'xǁRecordParserǁparse_line__mutmut_39': xǁRecordParserǁparse_line__mutmut_39, 
        'xǁRecordParserǁparse_line__mutmut_40': xǁRecordParserǁparse_line__mutmut_40, 
        'xǁRecordParserǁparse_line__mutmut_41': xǁRecordParserǁparse_line__mutmut_41, 
        'xǁRecordParserǁparse_line__mutmut_42': xǁRecordParserǁparse_line__mutmut_42, 
        'xǁRecordParserǁparse_line__mutmut_43': xǁRecordParserǁparse_line__mutmut_43, 
        'xǁRecordParserǁparse_line__mutmut_44': xǁRecordParserǁparse_line__mutmut_44, 
        'xǁRecordParserǁparse_line__mutmut_45': xǁRecordParserǁparse_line__mutmut_45, 
        'xǁRecordParserǁparse_line__mutmut_46': xǁRecordParserǁparse_line__mutmut_46, 
        'xǁRecordParserǁparse_line__mutmut_47': xǁRecordParserǁparse_line__mutmut_47, 
        'xǁRecordParserǁparse_line__mutmut_48': xǁRecordParserǁparse_line__mutmut_48, 
        'xǁRecordParserǁparse_line__mutmut_49': xǁRecordParserǁparse_line__mutmut_49, 
        'xǁRecordParserǁparse_line__mutmut_50': xǁRecordParserǁparse_line__mutmut_50, 
        'xǁRecordParserǁparse_line__mutmut_51': xǁRecordParserǁparse_line__mutmut_51, 
        'xǁRecordParserǁparse_line__mutmut_52': xǁRecordParserǁparse_line__mutmut_52, 
        'xǁRecordParserǁparse_line__mutmut_53': xǁRecordParserǁparse_line__mutmut_53, 
        'xǁRecordParserǁparse_line__mutmut_54': xǁRecordParserǁparse_line__mutmut_54, 
        'xǁRecordParserǁparse_line__mutmut_55': xǁRecordParserǁparse_line__mutmut_55, 
        'xǁRecordParserǁparse_line__mutmut_56': xǁRecordParserǁparse_line__mutmut_56, 
        'xǁRecordParserǁparse_line__mutmut_57': xǁRecordParserǁparse_line__mutmut_57, 
        'xǁRecordParserǁparse_line__mutmut_58': xǁRecordParserǁparse_line__mutmut_58, 
        'xǁRecordParserǁparse_line__mutmut_59': xǁRecordParserǁparse_line__mutmut_59, 
        'xǁRecordParserǁparse_line__mutmut_60': xǁRecordParserǁparse_line__mutmut_60, 
        'xǁRecordParserǁparse_line__mutmut_61': xǁRecordParserǁparse_line__mutmut_61, 
        'xǁRecordParserǁparse_line__mutmut_62': xǁRecordParserǁparse_line__mutmut_62, 
        'xǁRecordParserǁparse_line__mutmut_63': xǁRecordParserǁparse_line__mutmut_63, 
        'xǁRecordParserǁparse_line__mutmut_64': xǁRecordParserǁparse_line__mutmut_64, 
        'xǁRecordParserǁparse_line__mutmut_65': xǁRecordParserǁparse_line__mutmut_65, 
        'xǁRecordParserǁparse_line__mutmut_66': xǁRecordParserǁparse_line__mutmut_66, 
        'xǁRecordParserǁparse_line__mutmut_67': xǁRecordParserǁparse_line__mutmut_67, 
        'xǁRecordParserǁparse_line__mutmut_68': xǁRecordParserǁparse_line__mutmut_68, 
        'xǁRecordParserǁparse_line__mutmut_69': xǁRecordParserǁparse_line__mutmut_69, 
        'xǁRecordParserǁparse_line__mutmut_70': xǁRecordParserǁparse_line__mutmut_70, 
        'xǁRecordParserǁparse_line__mutmut_71': xǁRecordParserǁparse_line__mutmut_71, 
        'xǁRecordParserǁparse_line__mutmut_72': xǁRecordParserǁparse_line__mutmut_72, 
        'xǁRecordParserǁparse_line__mutmut_73': xǁRecordParserǁparse_line__mutmut_73, 
        'xǁRecordParserǁparse_line__mutmut_74': xǁRecordParserǁparse_line__mutmut_74, 
        'xǁRecordParserǁparse_line__mutmut_75': xǁRecordParserǁparse_line__mutmut_75, 
        'xǁRecordParserǁparse_line__mutmut_76': xǁRecordParserǁparse_line__mutmut_76, 
        'xǁRecordParserǁparse_line__mutmut_77': xǁRecordParserǁparse_line__mutmut_77, 
        'xǁRecordParserǁparse_line__mutmut_78': xǁRecordParserǁparse_line__mutmut_78, 
        'xǁRecordParserǁparse_line__mutmut_79': xǁRecordParserǁparse_line__mutmut_79, 
        'xǁRecordParserǁparse_line__mutmut_80': xǁRecordParserǁparse_line__mutmut_80, 
        'xǁRecordParserǁparse_line__mutmut_81': xǁRecordParserǁparse_line__mutmut_81, 
        'xǁRecordParserǁparse_line__mutmut_82': xǁRecordParserǁparse_line__mutmut_82, 
        'xǁRecordParserǁparse_line__mutmut_83': xǁRecordParserǁparse_line__mutmut_83, 
        'xǁRecordParserǁparse_line__mutmut_84': xǁRecordParserǁparse_line__mutmut_84, 
        'xǁRecordParserǁparse_line__mutmut_85': xǁRecordParserǁparse_line__mutmut_85, 
        'xǁRecordParserǁparse_line__mutmut_86': xǁRecordParserǁparse_line__mutmut_86, 
        'xǁRecordParserǁparse_line__mutmut_87': xǁRecordParserǁparse_line__mutmut_87, 
        'xǁRecordParserǁparse_line__mutmut_88': xǁRecordParserǁparse_line__mutmut_88, 
        'xǁRecordParserǁparse_line__mutmut_89': xǁRecordParserǁparse_line__mutmut_89, 
        'xǁRecordParserǁparse_line__mutmut_90': xǁRecordParserǁparse_line__mutmut_90, 
        'xǁRecordParserǁparse_line__mutmut_91': xǁRecordParserǁparse_line__mutmut_91, 
        'xǁRecordParserǁparse_line__mutmut_92': xǁRecordParserǁparse_line__mutmut_92, 
        'xǁRecordParserǁparse_line__mutmut_93': xǁRecordParserǁparse_line__mutmut_93, 
        'xǁRecordParserǁparse_line__mutmut_94': xǁRecordParserǁparse_line__mutmut_94, 
        'xǁRecordParserǁparse_line__mutmut_95': xǁRecordParserǁparse_line__mutmut_95, 
        'xǁRecordParserǁparse_line__mutmut_96': xǁRecordParserǁparse_line__mutmut_96, 
        'xǁRecordParserǁparse_line__mutmut_97': xǁRecordParserǁparse_line__mutmut_97, 
        'xǁRecordParserǁparse_line__mutmut_98': xǁRecordParserǁparse_line__mutmut_98, 
        'xǁRecordParserǁparse_line__mutmut_99': xǁRecordParserǁparse_line__mutmut_99, 
        'xǁRecordParserǁparse_line__mutmut_100': xǁRecordParserǁparse_line__mutmut_100
    }

    def parse_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁparse_line__mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁparse_line__mutmut_mutants"), *args, **kwargs) 

    parse_line.__signature__ = _mutmut_signature(xǁRecordParserǁparse_line__mutmut_orig)
    xǁRecordParserǁparse_line__mutmut_orig.__name__ = 'xǁRecordParserǁparse_line'



    def xǁRecordParserǁ_handle_calls__mutmut_orig(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_1(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str  in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_2(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[None] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_3(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, None))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_4(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info,))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_5(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = None
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_6(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = None
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_7(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[10:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_8(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[None], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_9(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=True):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_10(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:],):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_11(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(None):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_12(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(None, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_13(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[None], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_14(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], None)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_15(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data( self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_16(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str],)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_17(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = None
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_18(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(None, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_19(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, None)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_20(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call( data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_21(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample,)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_22(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = None
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_23(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(None, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_24(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run( len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_25(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("XXFTXX") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_26(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") and []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_27(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = None
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_28(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if  isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_29(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("XXFORMAT/FT field must be a list of strings but was {}XX".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_30(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(None)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_31(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[None], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_32(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], None)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_33(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str],)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_34(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = None
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_35(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if  all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_36(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("XXFORMAT/FT field must be a list of strings but was {}XX".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_37(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(None)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_38(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(None, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_39(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "XXFORMAT/FTXX", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_40(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters( "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_41(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(None)
            else:
                calls.append(record.UnparsedCall(sample, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_42(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(None, raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_43(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample, None))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_44(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall( raw_data))
        return calls

    def xǁRecordParserǁ_handle_calls__mutmut_45(
        self, alts: list[record.AltRecord], format_: list[str], format_str: str, arr: list[str]
    ) -> list["record.Call | record.UnparsedCall"]:
        """Handle FORMAT and calls columns, factored out of parse_line"""
        if format_str not in self._format_cache:
            self._format_cache[format_str] = list(map(self.header.get_format_field_info, format_))
        # per-sample calls
        calls: list["record.Call | record.UnparsedCall"] = []
        for sample, raw_data in zip(self.samples.names, arr[9:], strict=False):
            if self.samples.is_parsed(sample):
                data = self._parse_calls_data(format_, self._format_cache[format_str], raw_data)
                call = record.Call(sample, data)
                self._format_checker.run(call, len(alts))
                ft_value = call.data.get("FT") or []
                if not isinstance(ft_value, list):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value)))
                ft_value_ = cast(list[str], ft_value)
                if not all(isinstance(x, str) for x in ft_value_):  # pragma: no cover
                    raise ValueError("FORMAT/FT field must be a list of strings but was {}".format(repr(ft_value_)))
                self._check_filters(ft_value_, "FORMAT/FT", call.sample)
                calls.append(call)
            else:
                calls.append(record.UnparsedCall(sample,))
        return calls

    xǁRecordParserǁ_handle_calls__mutmut_mutants = {
    'xǁRecordParserǁ_handle_calls__mutmut_1': xǁRecordParserǁ_handle_calls__mutmut_1, 
        'xǁRecordParserǁ_handle_calls__mutmut_2': xǁRecordParserǁ_handle_calls__mutmut_2, 
        'xǁRecordParserǁ_handle_calls__mutmut_3': xǁRecordParserǁ_handle_calls__mutmut_3, 
        'xǁRecordParserǁ_handle_calls__mutmut_4': xǁRecordParserǁ_handle_calls__mutmut_4, 
        'xǁRecordParserǁ_handle_calls__mutmut_5': xǁRecordParserǁ_handle_calls__mutmut_5, 
        'xǁRecordParserǁ_handle_calls__mutmut_6': xǁRecordParserǁ_handle_calls__mutmut_6, 
        'xǁRecordParserǁ_handle_calls__mutmut_7': xǁRecordParserǁ_handle_calls__mutmut_7, 
        'xǁRecordParserǁ_handle_calls__mutmut_8': xǁRecordParserǁ_handle_calls__mutmut_8, 
        'xǁRecordParserǁ_handle_calls__mutmut_9': xǁRecordParserǁ_handle_calls__mutmut_9, 
        'xǁRecordParserǁ_handle_calls__mutmut_10': xǁRecordParserǁ_handle_calls__mutmut_10, 
        'xǁRecordParserǁ_handle_calls__mutmut_11': xǁRecordParserǁ_handle_calls__mutmut_11, 
        'xǁRecordParserǁ_handle_calls__mutmut_12': xǁRecordParserǁ_handle_calls__mutmut_12, 
        'xǁRecordParserǁ_handle_calls__mutmut_13': xǁRecordParserǁ_handle_calls__mutmut_13, 
        'xǁRecordParserǁ_handle_calls__mutmut_14': xǁRecordParserǁ_handle_calls__mutmut_14, 
        'xǁRecordParserǁ_handle_calls__mutmut_15': xǁRecordParserǁ_handle_calls__mutmut_15, 
        'xǁRecordParserǁ_handle_calls__mutmut_16': xǁRecordParserǁ_handle_calls__mutmut_16, 
        'xǁRecordParserǁ_handle_calls__mutmut_17': xǁRecordParserǁ_handle_calls__mutmut_17, 
        'xǁRecordParserǁ_handle_calls__mutmut_18': xǁRecordParserǁ_handle_calls__mutmut_18, 
        'xǁRecordParserǁ_handle_calls__mutmut_19': xǁRecordParserǁ_handle_calls__mutmut_19, 
        'xǁRecordParserǁ_handle_calls__mutmut_20': xǁRecordParserǁ_handle_calls__mutmut_20, 
        'xǁRecordParserǁ_handle_calls__mutmut_21': xǁRecordParserǁ_handle_calls__mutmut_21, 
        'xǁRecordParserǁ_handle_calls__mutmut_22': xǁRecordParserǁ_handle_calls__mutmut_22, 
        'xǁRecordParserǁ_handle_calls__mutmut_23': xǁRecordParserǁ_handle_calls__mutmut_23, 
        'xǁRecordParserǁ_handle_calls__mutmut_24': xǁRecordParserǁ_handle_calls__mutmut_24, 
        'xǁRecordParserǁ_handle_calls__mutmut_25': xǁRecordParserǁ_handle_calls__mutmut_25, 
        'xǁRecordParserǁ_handle_calls__mutmut_26': xǁRecordParserǁ_handle_calls__mutmut_26, 
        'xǁRecordParserǁ_handle_calls__mutmut_27': xǁRecordParserǁ_handle_calls__mutmut_27, 
        'xǁRecordParserǁ_handle_calls__mutmut_28': xǁRecordParserǁ_handle_calls__mutmut_28, 
        'xǁRecordParserǁ_handle_calls__mutmut_29': xǁRecordParserǁ_handle_calls__mutmut_29, 
        'xǁRecordParserǁ_handle_calls__mutmut_30': xǁRecordParserǁ_handle_calls__mutmut_30, 
        'xǁRecordParserǁ_handle_calls__mutmut_31': xǁRecordParserǁ_handle_calls__mutmut_31, 
        'xǁRecordParserǁ_handle_calls__mutmut_32': xǁRecordParserǁ_handle_calls__mutmut_32, 
        'xǁRecordParserǁ_handle_calls__mutmut_33': xǁRecordParserǁ_handle_calls__mutmut_33, 
        'xǁRecordParserǁ_handle_calls__mutmut_34': xǁRecordParserǁ_handle_calls__mutmut_34, 
        'xǁRecordParserǁ_handle_calls__mutmut_35': xǁRecordParserǁ_handle_calls__mutmut_35, 
        'xǁRecordParserǁ_handle_calls__mutmut_36': xǁRecordParserǁ_handle_calls__mutmut_36, 
        'xǁRecordParserǁ_handle_calls__mutmut_37': xǁRecordParserǁ_handle_calls__mutmut_37, 
        'xǁRecordParserǁ_handle_calls__mutmut_38': xǁRecordParserǁ_handle_calls__mutmut_38, 
        'xǁRecordParserǁ_handle_calls__mutmut_39': xǁRecordParserǁ_handle_calls__mutmut_39, 
        'xǁRecordParserǁ_handle_calls__mutmut_40': xǁRecordParserǁ_handle_calls__mutmut_40, 
        'xǁRecordParserǁ_handle_calls__mutmut_41': xǁRecordParserǁ_handle_calls__mutmut_41, 
        'xǁRecordParserǁ_handle_calls__mutmut_42': xǁRecordParserǁ_handle_calls__mutmut_42, 
        'xǁRecordParserǁ_handle_calls__mutmut_43': xǁRecordParserǁ_handle_calls__mutmut_43, 
        'xǁRecordParserǁ_handle_calls__mutmut_44': xǁRecordParserǁ_handle_calls__mutmut_44, 
        'xǁRecordParserǁ_handle_calls__mutmut_45': xǁRecordParserǁ_handle_calls__mutmut_45
    }

    def _handle_calls(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁ_handle_calls__mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁ_handle_calls__mutmut_mutants"), *args, **kwargs) 

    _handle_calls.__signature__ = _mutmut_signature(xǁRecordParserǁ_handle_calls__mutmut_orig)
    xǁRecordParserǁ_handle_calls__mutmut_orig.__name__ = 'xǁRecordParserǁ_handle_calls'



    def xǁRecordParserǁ_check_filters__mutmut_orig(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter(f, source, sample)

    def xǁRecordParserǁ_check_filters__mutmut_1(self, filt: list[str], source: str, sample: str | None = None):
        if  filt:
            return
        for f in filt:
            self._check_filter(f, source, sample)

    def xǁRecordParserǁ_check_filters__mutmut_2(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter(None, source, sample)

    def xǁRecordParserǁ_check_filters__mutmut_3(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter(f, None, sample)

    def xǁRecordParserǁ_check_filters__mutmut_4(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter(f, source, None)

    def xǁRecordParserǁ_check_filters__mutmut_5(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter( source, sample)

    def xǁRecordParserǁ_check_filters__mutmut_6(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter(f, sample)

    def xǁRecordParserǁ_check_filters__mutmut_7(self, filt: list[str], source: str, sample: str | None = None):
        if not filt:
            return
        for f in filt:
            self._check_filter(f, source,)

    xǁRecordParserǁ_check_filters__mutmut_mutants = {
    'xǁRecordParserǁ_check_filters__mutmut_1': xǁRecordParserǁ_check_filters__mutmut_1, 
        'xǁRecordParserǁ_check_filters__mutmut_2': xǁRecordParserǁ_check_filters__mutmut_2, 
        'xǁRecordParserǁ_check_filters__mutmut_3': xǁRecordParserǁ_check_filters__mutmut_3, 
        'xǁRecordParserǁ_check_filters__mutmut_4': xǁRecordParserǁ_check_filters__mutmut_4, 
        'xǁRecordParserǁ_check_filters__mutmut_5': xǁRecordParserǁ_check_filters__mutmut_5, 
        'xǁRecordParserǁ_check_filters__mutmut_6': xǁRecordParserǁ_check_filters__mutmut_6, 
        'xǁRecordParserǁ_check_filters__mutmut_7': xǁRecordParserǁ_check_filters__mutmut_7
    }

    def _check_filters(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁ_check_filters__mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁ_check_filters__mutmut_mutants"), *args, **kwargs) 

    _check_filters.__signature__ = _mutmut_signature(xǁRecordParserǁ_check_filters__mutmut_orig)
    xǁRecordParserǁ_check_filters__mutmut_orig.__name__ = 'xǁRecordParserǁ_check_filters'



    def xǁRecordParserǁ_check_filter__mutmut_orig(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_1(self, f: str, source: str, sample: str | None):
        if f != "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_2(self, f: str, source: str, sample: str | None):
        if f == "XXPASSXX":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_3(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f  in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_4(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source != "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_5(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "XXFILTERXX":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_6(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("XXFilter not found in header: {}; problem in FILTER columnXX").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_7(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(None),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_8(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source != "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_9(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "XXFORMAT/FTXX" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_10(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" or sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_11(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("XXFilter not found in header: {}; problem in FORMAT/FT column of sample {}XX").format(f, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_12(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(None, sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_13(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f, None),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_14(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format( sample),
                    exceptions.UnknownFilter,
                )

    def xǁRecordParserǁ_check_filter__mutmut_15(self, f: str, source: str, sample: str | None):
        if f == "PASS":
            pass  # the PASS filter is implicitely defined
        elif f not in self._filter_ids:  # pragma: no cover
            if source == "FILTER":
                warnings.warn(
                    ("Filter not found in header: {}; problem in FILTER column").format(f),
                    exceptions.UnknownFilter,
                )
            else:
                assert source == "FORMAT/FT" and sample
                warnings.warn(
                    ("Filter not found in header: {}; problem in FORMAT/FT column of sample {}").format(f,),
                    exceptions.UnknownFilter,
                )

    xǁRecordParserǁ_check_filter__mutmut_mutants = {
    'xǁRecordParserǁ_check_filter__mutmut_1': xǁRecordParserǁ_check_filter__mutmut_1, 
        'xǁRecordParserǁ_check_filter__mutmut_2': xǁRecordParserǁ_check_filter__mutmut_2, 
        'xǁRecordParserǁ_check_filter__mutmut_3': xǁRecordParserǁ_check_filter__mutmut_3, 
        'xǁRecordParserǁ_check_filter__mutmut_4': xǁRecordParserǁ_check_filter__mutmut_4, 
        'xǁRecordParserǁ_check_filter__mutmut_5': xǁRecordParserǁ_check_filter__mutmut_5, 
        'xǁRecordParserǁ_check_filter__mutmut_6': xǁRecordParserǁ_check_filter__mutmut_6, 
        'xǁRecordParserǁ_check_filter__mutmut_7': xǁRecordParserǁ_check_filter__mutmut_7, 
        'xǁRecordParserǁ_check_filter__mutmut_8': xǁRecordParserǁ_check_filter__mutmut_8, 
        'xǁRecordParserǁ_check_filter__mutmut_9': xǁRecordParserǁ_check_filter__mutmut_9, 
        'xǁRecordParserǁ_check_filter__mutmut_10': xǁRecordParserǁ_check_filter__mutmut_10, 
        'xǁRecordParserǁ_check_filter__mutmut_11': xǁRecordParserǁ_check_filter__mutmut_11, 
        'xǁRecordParserǁ_check_filter__mutmut_12': xǁRecordParserǁ_check_filter__mutmut_12, 
        'xǁRecordParserǁ_check_filter__mutmut_13': xǁRecordParserǁ_check_filter__mutmut_13, 
        'xǁRecordParserǁ_check_filter__mutmut_14': xǁRecordParserǁ_check_filter__mutmut_14, 
        'xǁRecordParserǁ_check_filter__mutmut_15': xǁRecordParserǁ_check_filter__mutmut_15
    }

    def _check_filter(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁ_check_filter__mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁ_check_filter__mutmut_mutants"), *args, **kwargs) 

    _check_filter.__signature__ = _mutmut_signature(xǁRecordParserǁ_check_filter__mutmut_orig)
    xǁRecordParserǁ_check_filter__mutmut_orig.__name__ = 'xǁRecordParserǁ_check_filter'



    def xǁRecordParserǁ_split_line__mutmut_orig(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = line_str.rstrip().split("\t")
        if len(arr) != self.expected_fields:
            raise exceptions.InvalidRecordException(
                "The line contains an invalid number of fields. Was {} but expected {}\n{}".format(
                    len(arr), self.expected_fields, line_str
                )
            )
        return arr

    def xǁRecordParserǁ_split_line__mutmut_1(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = line_str.rstrip().split("XX\tXX")
        if len(arr) != self.expected_fields:
            raise exceptions.InvalidRecordException(
                "The line contains an invalid number of fields. Was {} but expected {}\n{}".format(
                    len(arr), self.expected_fields, line_str
                )
            )
        return arr

    def xǁRecordParserǁ_split_line__mutmut_2(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = None
        if len(arr) != self.expected_fields:
            raise exceptions.InvalidRecordException(
                "The line contains an invalid number of fields. Was {} but expected {}\n{}".format(
                    len(arr), self.expected_fields, line_str
                )
            )
        return arr

    def xǁRecordParserǁ_split_line__mutmut_3(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = line_str.rstrip().split("\t")
        if len(arr) == self.expected_fields:
            raise exceptions.InvalidRecordException(
                "The line contains an invalid number of fields. Was {} but expected {}\n{}".format(
                    len(arr), self.expected_fields, line_str
                )
            )
        return arr

    def xǁRecordParserǁ_split_line__mutmut_4(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = line_str.rstrip().split("\t")
        if len(arr) != self.expected_fields:
            raise exceptions.InvalidRecordException(
                "XXThe line contains an invalid number of fields. Was {} but expected {}\n{}XX".format(
                    len(arr), self.expected_fields, line_str
                )
            )
        return arr

    def xǁRecordParserǁ_split_line__mutmut_5(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = line_str.rstrip().split("\t")
        if len(arr) != self.expected_fields:
            raise exceptions.InvalidRecordException(
                "The line contains an invalid number of fields. Was {} but expected {}\n{}".format(
                    len(arr), self.expected_fields, None
                )
            )
        return arr

    def xǁRecordParserǁ_split_line__mutmut_6(self, line_str: str) -> list[str]:
        """Split line and check number of columns"""
        arr = line_str.rstrip().split("\t")
        if len(arr) != self.expected_fields:
            raise exceptions.InvalidRecordException(
                "The line contains an invalid number of fields. Was {} but expected {}\n{}".format(
                    len(arr), self.expected_fields,
                )
            )
        return arr

    xǁRecordParserǁ_split_line__mutmut_mutants = {
    'xǁRecordParserǁ_split_line__mutmut_1': xǁRecordParserǁ_split_line__mutmut_1, 
        'xǁRecordParserǁ_split_line__mutmut_2': xǁRecordParserǁ_split_line__mutmut_2, 
        'xǁRecordParserǁ_split_line__mutmut_3': xǁRecordParserǁ_split_line__mutmut_3, 
        'xǁRecordParserǁ_split_line__mutmut_4': xǁRecordParserǁ_split_line__mutmut_4, 
        'xǁRecordParserǁ_split_line__mutmut_5': xǁRecordParserǁ_split_line__mutmut_5, 
        'xǁRecordParserǁ_split_line__mutmut_6': xǁRecordParserǁ_split_line__mutmut_6
    }

    def _split_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁ_split_line__mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁ_split_line__mutmut_mutants"), *args, **kwargs) 

    _split_line.__signature__ = _mutmut_signature(xǁRecordParserǁ_split_line__mutmut_orig)
    xǁRecordParserǁ_split_line__mutmut_orig.__name__ = 'xǁRecordParserǁ_split_line'



    def xǁRecordParserǁ_parse_info__mutmut_orig(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_1(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = None
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_2(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str != ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_3(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == "XX.XX":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_4(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split("XX;XX"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_5(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "XX=XX" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_6(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "="  in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_7(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = None
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_8(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[None] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_9(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(None), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_10(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), False)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_11(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = None
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_12(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(None)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_13(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = None
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_14(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[None] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_15(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(None), value)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_16(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), None)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_17(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key),)
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_18(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = None
            self._info_checker.run(key, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_19(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(None, result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_20(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[None], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_21(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key], None)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_22(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run( result[key], num_alts)
        return result

    def xǁRecordParserǁ_parse_info__mutmut_23(self, info_str: str, num_alts: int) -> dict[str, Any]:
        """Parse INFO column from string"""
        result: dict[str, Any] = {}
        if info_str == ".":
            return result
        # The standard is very nice to parsers, we can simply split at
        # semicolon characters, although I (Manuel) don't know how strict
        # programs follow this
        for entry in info_str.split(";"):
            if "=" not in entry:  # flag
                key = entry
                result[key] = parse_field_value(self.header.get_info_field_info(key), True)
            else:
                key, value = split_mapping(entry)
                result[key] = parse_field_value(self.header.get_info_field_info(key), value)
            self._info_checker.run(key, result[key],)
        return result

    xǁRecordParserǁ_parse_info__mutmut_mutants = {
    'xǁRecordParserǁ_parse_info__mutmut_1': xǁRecordParserǁ_parse_info__mutmut_1, 
        'xǁRecordParserǁ_parse_info__mutmut_2': xǁRecordParserǁ_parse_info__mutmut_2, 
        'xǁRecordParserǁ_parse_info__mutmut_3': xǁRecordParserǁ_parse_info__mutmut_3, 
        'xǁRecordParserǁ_parse_info__mutmut_4': xǁRecordParserǁ_parse_info__mutmut_4, 
        'xǁRecordParserǁ_parse_info__mutmut_5': xǁRecordParserǁ_parse_info__mutmut_5, 
        'xǁRecordParserǁ_parse_info__mutmut_6': xǁRecordParserǁ_parse_info__mutmut_6, 
        'xǁRecordParserǁ_parse_info__mutmut_7': xǁRecordParserǁ_parse_info__mutmut_7, 
        'xǁRecordParserǁ_parse_info__mutmut_8': xǁRecordParserǁ_parse_info__mutmut_8, 
        'xǁRecordParserǁ_parse_info__mutmut_9': xǁRecordParserǁ_parse_info__mutmut_9, 
        'xǁRecordParserǁ_parse_info__mutmut_10': xǁRecordParserǁ_parse_info__mutmut_10, 
        'xǁRecordParserǁ_parse_info__mutmut_11': xǁRecordParserǁ_parse_info__mutmut_11, 
        'xǁRecordParserǁ_parse_info__mutmut_12': xǁRecordParserǁ_parse_info__mutmut_12, 
        'xǁRecordParserǁ_parse_info__mutmut_13': xǁRecordParserǁ_parse_info__mutmut_13, 
        'xǁRecordParserǁ_parse_info__mutmut_14': xǁRecordParserǁ_parse_info__mutmut_14, 
        'xǁRecordParserǁ_parse_info__mutmut_15': xǁRecordParserǁ_parse_info__mutmut_15, 
        'xǁRecordParserǁ_parse_info__mutmut_16': xǁRecordParserǁ_parse_info__mutmut_16, 
        'xǁRecordParserǁ_parse_info__mutmut_17': xǁRecordParserǁ_parse_info__mutmut_17, 
        'xǁRecordParserǁ_parse_info__mutmut_18': xǁRecordParserǁ_parse_info__mutmut_18, 
        'xǁRecordParserǁ_parse_info__mutmut_19': xǁRecordParserǁ_parse_info__mutmut_19, 
        'xǁRecordParserǁ_parse_info__mutmut_20': xǁRecordParserǁ_parse_info__mutmut_20, 
        'xǁRecordParserǁ_parse_info__mutmut_21': xǁRecordParserǁ_parse_info__mutmut_21, 
        'xǁRecordParserǁ_parse_info__mutmut_22': xǁRecordParserǁ_parse_info__mutmut_22, 
        'xǁRecordParserǁ_parse_info__mutmut_23': xǁRecordParserǁ_parse_info__mutmut_23
    }

    def _parse_info(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁRecordParserǁ_parse_info__mutmut_orig"), object.__getattribute__(self, "xǁRecordParserǁ_parse_info__mutmut_mutants"), *args, **kwargs) 

    _parse_info.__signature__ = _mutmut_signature(xǁRecordParserǁ_parse_info__mutmut_orig)
    xǁRecordParserǁ_parse_info__mutmut_orig.__name__ = 'xǁRecordParserǁ_parse_info'



    @classmethod
    def _parse_calls_data(
        cls, format_: list[str], infos: list["header.FieldInfo"], gt_str: str
    ) -> dict[str, bool | int | float | str | list[bool | int | float | str | None] | None]:
        """Parse genotype call information from arrays using format array

        :param list format: List of strings with format names
        :param gt_str arr: string with genotype information values
        """
        data: dict[str, bool | int | float | str | list[bool | int | float | str | None] | None] = {}
        # The standard is very nice to parsers, we can simply split at
        # colon characters, although I (Manuel) don't know how strict
        # programs follow this
        for key, info, value in zip(format_, infos, gt_str.split(":"), strict=False):
            data[key] = parse_field_value(info, value)
        return data


class HeaderChecker:
    """Helper class for checking a VCF header"""

    def xǁHeaderCheckerǁrun__mutmut_orig(self, header: header.Header) -> None:
        """Check the header

        Warnings will be printed using ``warnings`` while errors will raise
        an exception.

        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            severe errors reading the header
        """
        self._check_header_lines(header.lines)

    xǁHeaderCheckerǁrun__mutmut_mutants = {

    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁHeaderCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁHeaderCheckerǁrun__mutmut_orig)
    xǁHeaderCheckerǁrun__mutmut_orig.__name__ = 'xǁHeaderCheckerǁrun'



    def xǁHeaderCheckerǁ_check_header_lines__mutmut_orig(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_1(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if  header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_2(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "XXThe VCF file did not contain any header lines!XX"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_3(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[1]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_4(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[None]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_5(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = None
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_6(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key == "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_7(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "XXfileformatXX":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_8(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("XXThe VCF file did not start with ##fileformatXX")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_9(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value  in SUPPORTED_VCF_VERSIONS:
            warnings.warn("Unknown VCF version {}".format(first.value), exceptions.UnknownVCFVersion)

    def xǁHeaderCheckerǁ_check_header_lines__mutmut_10(self, header_lines: list[header.HeaderLine]) -> None:
        """Check header lines, in particular for starting file "##fileformat" """
        if not header_lines:
            raise exceptions.InvalidHeaderException(
                "The VCF file did not contain any header lines!"
            )  # pragma: no cover
        first = header_lines[0]
        if first.key != "fileformat":
            raise exceptions.InvalidHeaderException("The VCF file did not start with ##fileformat")
        if first.value not in SUPPORTED_VCF_VERSIONS:
            warnings.warn("XXUnknown VCF version {}XX".format(first.value), exceptions.UnknownVCFVersion)

    xǁHeaderCheckerǁ_check_header_lines__mutmut_mutants = {
    'xǁHeaderCheckerǁ_check_header_lines__mutmut_1': xǁHeaderCheckerǁ_check_header_lines__mutmut_1, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_2': xǁHeaderCheckerǁ_check_header_lines__mutmut_2, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_3': xǁHeaderCheckerǁ_check_header_lines__mutmut_3, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_4': xǁHeaderCheckerǁ_check_header_lines__mutmut_4, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_5': xǁHeaderCheckerǁ_check_header_lines__mutmut_5, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_6': xǁHeaderCheckerǁ_check_header_lines__mutmut_6, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_7': xǁHeaderCheckerǁ_check_header_lines__mutmut_7, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_8': xǁHeaderCheckerǁ_check_header_lines__mutmut_8, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_9': xǁHeaderCheckerǁ_check_header_lines__mutmut_9, 
        'xǁHeaderCheckerǁ_check_header_lines__mutmut_10': xǁHeaderCheckerǁ_check_header_lines__mutmut_10
    }

    def _check_header_lines(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁHeaderCheckerǁ_check_header_lines__mutmut_orig"), object.__getattribute__(self, "xǁHeaderCheckerǁ_check_header_lines__mutmut_mutants"), *args, **kwargs) 

    _check_header_lines.__signature__ = _mutmut_signature(xǁHeaderCheckerǁ_check_header_lines__mutmut_orig)
    xǁHeaderCheckerǁ_check_header_lines__mutmut_orig.__name__ = 'xǁHeaderCheckerǁ_check_header_lines'




@functools.lru_cache(maxsize=32)
def binomial(n: int, k: int):
    try:
        res = math.factorial(n) // math.factorial(k) // math.factorial(n - k)
    except ValueError:
        res = 0
    return res


class AbstractInfoChecker:
    """Abstract base class for INFO field checkers"""

    def xǁAbstractInfoCheckerǁrun__mutmut_orig(self, key: str, value: str, num_alts: int) -> None:
        """Run the checker"""
        raise NotImplementedError  # pragma: no cover

    xǁAbstractInfoCheckerǁrun__mutmut_mutants = {

    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAbstractInfoCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁAbstractInfoCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁAbstractInfoCheckerǁrun__mutmut_orig)
    xǁAbstractInfoCheckerǁrun__mutmut_orig.__name__ = 'xǁAbstractInfoCheckerǁrun'




class NoopInfoChecker(AbstractInfoChecker):
    """Helper class that performs no checks"""

    def xǁNoopInfoCheckerǁrun__mutmut_orig(self, key: str, value: str, num_alts: int) -> None:
        pass

    xǁNoopInfoCheckerǁrun__mutmut_mutants = {

    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁNoopInfoCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁNoopInfoCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁNoopInfoCheckerǁrun__mutmut_orig)
    xǁNoopInfoCheckerǁrun__mutmut_orig.__name__ = 'xǁNoopInfoCheckerǁrun'




class InfoChecker(AbstractInfoChecker):
    """Helper class for checking an INFO field"""

    def xǁInfoCheckerǁ__init____mutmut_orig(self, header: header.Header):
        #: VCFHeader to use for checking
        self.header = header

    def xǁInfoCheckerǁ__init____mutmut_1(self, header: header.Header):
        #: VCFHeader to use for checking
        self.header = None

    xǁInfoCheckerǁ__init____mutmut_mutants = {
    'xǁInfoCheckerǁ__init____mutmut_1': xǁInfoCheckerǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁInfoCheckerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInfoCheckerǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁInfoCheckerǁ__init____mutmut_orig)
    xǁInfoCheckerǁ__init____mutmut_orig.__name__ = 'xǁInfoCheckerǁ__init__'



    def xǁInfoCheckerǁrun__mutmut_orig(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_1(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(None)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_2(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = None
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_3(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if  isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_4(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            "XX.XX": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_5(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "XXAXX": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_6(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "XXRXX": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_7(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts - 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_8(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 2,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_9(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "XXGXX": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_10(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts - 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_11(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 2, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_12(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 3),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_13(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = None
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_14(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = None
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_15(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) == expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_16(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "XXNumber of elements for INFO field {} is {} instead of {}XX"
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_17(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = None
            warnings.warn(tpl.format(key, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_18(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format(None, len(value), field_info.number), exceptions.IncorrectListLength)

    def xǁInfoCheckerǁrun__mutmut_19(self, key: str, value: str, num_alts: int) -> None:
        """Check value in INFO[key] of record

        Currently, only checks for consistent counts are implemented

        :param str key: key of INFO entry to check
        :param value: value to check
        :param int alts: list of alternative alleles, for length
        """
        field_info = self.header.get_info_field_info(key)
        if not isinstance(value, list):
            return
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + 1, 2),  # diploid only at the moment
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for INFO field {} is {} instead of {}"
            warnings.warn(tpl.format( len(value), field_info.number), exceptions.IncorrectListLength)

    xǁInfoCheckerǁrun__mutmut_mutants = {
    'xǁInfoCheckerǁrun__mutmut_1': xǁInfoCheckerǁrun__mutmut_1, 
        'xǁInfoCheckerǁrun__mutmut_2': xǁInfoCheckerǁrun__mutmut_2, 
        'xǁInfoCheckerǁrun__mutmut_3': xǁInfoCheckerǁrun__mutmut_3, 
        'xǁInfoCheckerǁrun__mutmut_4': xǁInfoCheckerǁrun__mutmut_4, 
        'xǁInfoCheckerǁrun__mutmut_5': xǁInfoCheckerǁrun__mutmut_5, 
        'xǁInfoCheckerǁrun__mutmut_6': xǁInfoCheckerǁrun__mutmut_6, 
        'xǁInfoCheckerǁrun__mutmut_7': xǁInfoCheckerǁrun__mutmut_7, 
        'xǁInfoCheckerǁrun__mutmut_8': xǁInfoCheckerǁrun__mutmut_8, 
        'xǁInfoCheckerǁrun__mutmut_9': xǁInfoCheckerǁrun__mutmut_9, 
        'xǁInfoCheckerǁrun__mutmut_10': xǁInfoCheckerǁrun__mutmut_10, 
        'xǁInfoCheckerǁrun__mutmut_11': xǁInfoCheckerǁrun__mutmut_11, 
        'xǁInfoCheckerǁrun__mutmut_12': xǁInfoCheckerǁrun__mutmut_12, 
        'xǁInfoCheckerǁrun__mutmut_13': xǁInfoCheckerǁrun__mutmut_13, 
        'xǁInfoCheckerǁrun__mutmut_14': xǁInfoCheckerǁrun__mutmut_14, 
        'xǁInfoCheckerǁrun__mutmut_15': xǁInfoCheckerǁrun__mutmut_15, 
        'xǁInfoCheckerǁrun__mutmut_16': xǁInfoCheckerǁrun__mutmut_16, 
        'xǁInfoCheckerǁrun__mutmut_17': xǁInfoCheckerǁrun__mutmut_17, 
        'xǁInfoCheckerǁrun__mutmut_18': xǁInfoCheckerǁrun__mutmut_18, 
        'xǁInfoCheckerǁrun__mutmut_19': xǁInfoCheckerǁrun__mutmut_19
    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁInfoCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁInfoCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁInfoCheckerǁrun__mutmut_orig)
    xǁInfoCheckerǁrun__mutmut_orig.__name__ = 'xǁInfoCheckerǁrun'




class AbstractNoopFormatChecker:
    """Abstract base class for FORMAT field checkers"""

    def xǁAbstractNoopFormatCheckerǁrun__mutmut_orig(self, call: "record.Call", num_alts: int) -> None:
        raise NotImplementedError  # pragma: no cover

    xǁAbstractNoopFormatCheckerǁrun__mutmut_mutants = {

    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁAbstractNoopFormatCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁAbstractNoopFormatCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁAbstractNoopFormatCheckerǁrun__mutmut_orig)
    xǁAbstractNoopFormatCheckerǁrun__mutmut_orig.__name__ = 'xǁAbstractNoopFormatCheckerǁrun'




class NoopFormatChecker(AbstractNoopFormatChecker):
    """Helper class that performs no checks"""

    def xǁNoopFormatCheckerǁrun__mutmut_orig(self, call: "record.Call", num_alts: int) -> None:
        pass

    xǁNoopFormatCheckerǁrun__mutmut_mutants = {

    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁNoopFormatCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁNoopFormatCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁNoopFormatCheckerǁrun__mutmut_orig)
    xǁNoopFormatCheckerǁrun__mutmut_orig.__name__ = 'xǁNoopFormatCheckerǁrun'




class FormatChecker(AbstractNoopFormatChecker):
    """Helper class for checking a FORMAT field"""

    def xǁFormatCheckerǁ__init____mutmut_orig(self, header: header.Header):
        #: VCFHeader to use for checking
        self.header = header

    def xǁFormatCheckerǁ__init____mutmut_1(self, header: header.Header):
        #: VCFHeader to use for checking
        self.header = None

    xǁFormatCheckerǁ__init____mutmut_mutants = {
    'xǁFormatCheckerǁ__init____mutmut_1': xǁFormatCheckerǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFormatCheckerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFormatCheckerǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁFormatCheckerǁ__init____mutmut_orig)
    xǁFormatCheckerǁ__init____mutmut_orig.__name__ = 'xǁFormatCheckerǁ__init__'



    def xǁFormatCheckerǁrun__mutmut_orig(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, key, value, num_alts)

    def xǁFormatCheckerǁrun__mutmut_1(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(None, key, value, num_alts)

    def xǁFormatCheckerǁrun__mutmut_2(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, None, value, num_alts)

    def xǁFormatCheckerǁrun__mutmut_3(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, key, None, num_alts)

    def xǁFormatCheckerǁrun__mutmut_4(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, key, value, None)

    def xǁFormatCheckerǁrun__mutmut_5(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count( key, value, num_alts)

    def xǁFormatCheckerǁrun__mutmut_6(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, value, num_alts)

    def xǁFormatCheckerǁrun__mutmut_7(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, key, num_alts)

    def xǁFormatCheckerǁrun__mutmut_8(self, call: "record.Call", num_alts: int) -> None:
        """Check ``FORMAT`` of a record.Call

        Currently, only checks for consistent counts are implemented
        """
        for key, value in call.data.items():
            self._check_count(call, key, value,)

    xǁFormatCheckerǁrun__mutmut_mutants = {
    'xǁFormatCheckerǁrun__mutmut_1': xǁFormatCheckerǁrun__mutmut_1, 
        'xǁFormatCheckerǁrun__mutmut_2': xǁFormatCheckerǁrun__mutmut_2, 
        'xǁFormatCheckerǁrun__mutmut_3': xǁFormatCheckerǁrun__mutmut_3, 
        'xǁFormatCheckerǁrun__mutmut_4': xǁFormatCheckerǁrun__mutmut_4, 
        'xǁFormatCheckerǁrun__mutmut_5': xǁFormatCheckerǁrun__mutmut_5, 
        'xǁFormatCheckerǁrun__mutmut_6': xǁFormatCheckerǁrun__mutmut_6, 
        'xǁFormatCheckerǁrun__mutmut_7': xǁFormatCheckerǁrun__mutmut_7, 
        'xǁFormatCheckerǁrun__mutmut_8': xǁFormatCheckerǁrun__mutmut_8
    }

    def run(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFormatCheckerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁFormatCheckerǁrun__mutmut_mutants"), *args, **kwargs) 

    run.__signature__ = _mutmut_signature(xǁFormatCheckerǁrun__mutmut_orig)
    xǁFormatCheckerǁrun__mutmut_orig.__name__ = 'xǁFormatCheckerǁrun'



    def xǁFormatCheckerǁ_check_count__mutmut_orig(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_1(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(None)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_2(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = None
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_3(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id != "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_4(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "XXGTXX":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_5(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = None
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_6(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            "XX.XX": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_7(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "XXAXX": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_8(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "XXRXX": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_9(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts - 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_10(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 2,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_11(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "XXGXX": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_12(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts - num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_13(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, None),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_14(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles,),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_15(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = None
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_16(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = None
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_17(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) == expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_18(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "XXNumber of elements for FORMAT field {} is {} instead of {} (number specifier {})XX"
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_19(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = None
            warnings.warn(
                tpl.format(key, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_20(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(None, len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_21(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), None, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_22(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format( len(value), expected, field_info.number),
                exceptions.IncorrectListLength,
            )

    def xǁFormatCheckerǁ_check_count__mutmut_23(self, call: "record.Call", key: str, value: str, num_alts: int) -> None:
        field_info = self.header.get_format_field_info(key)
        if field_info.id == "GT":
            return
        if isinstance(value, list):
            return
        num_alleles = len(call.gt_alleles or [])
        TABLE = {
            ".": len(value),
            "A": num_alts,
            "R": num_alts + 1,
            "G": binomial(num_alts + num_alleles, num_alleles),
        }
        expected = TABLE.get(str(field_info.number), field_info.number)
        if len(value) != expected:
            tpl = "Number of elements for FORMAT field {} is {} instead of {} (number specifier {})"
            warnings.warn(
                tpl.format(key, len(value), field_info.number),
                exceptions.IncorrectListLength,
            )

    xǁFormatCheckerǁ_check_count__mutmut_mutants = {
    'xǁFormatCheckerǁ_check_count__mutmut_1': xǁFormatCheckerǁ_check_count__mutmut_1, 
        'xǁFormatCheckerǁ_check_count__mutmut_2': xǁFormatCheckerǁ_check_count__mutmut_2, 
        'xǁFormatCheckerǁ_check_count__mutmut_3': xǁFormatCheckerǁ_check_count__mutmut_3, 
        'xǁFormatCheckerǁ_check_count__mutmut_4': xǁFormatCheckerǁ_check_count__mutmut_4, 
        'xǁFormatCheckerǁ_check_count__mutmut_5': xǁFormatCheckerǁ_check_count__mutmut_5, 
        'xǁFormatCheckerǁ_check_count__mutmut_6': xǁFormatCheckerǁ_check_count__mutmut_6, 
        'xǁFormatCheckerǁ_check_count__mutmut_7': xǁFormatCheckerǁ_check_count__mutmut_7, 
        'xǁFormatCheckerǁ_check_count__mutmut_8': xǁFormatCheckerǁ_check_count__mutmut_8, 
        'xǁFormatCheckerǁ_check_count__mutmut_9': xǁFormatCheckerǁ_check_count__mutmut_9, 
        'xǁFormatCheckerǁ_check_count__mutmut_10': xǁFormatCheckerǁ_check_count__mutmut_10, 
        'xǁFormatCheckerǁ_check_count__mutmut_11': xǁFormatCheckerǁ_check_count__mutmut_11, 
        'xǁFormatCheckerǁ_check_count__mutmut_12': xǁFormatCheckerǁ_check_count__mutmut_12, 
        'xǁFormatCheckerǁ_check_count__mutmut_13': xǁFormatCheckerǁ_check_count__mutmut_13, 
        'xǁFormatCheckerǁ_check_count__mutmut_14': xǁFormatCheckerǁ_check_count__mutmut_14, 
        'xǁFormatCheckerǁ_check_count__mutmut_15': xǁFormatCheckerǁ_check_count__mutmut_15, 
        'xǁFormatCheckerǁ_check_count__mutmut_16': xǁFormatCheckerǁ_check_count__mutmut_16, 
        'xǁFormatCheckerǁ_check_count__mutmut_17': xǁFormatCheckerǁ_check_count__mutmut_17, 
        'xǁFormatCheckerǁ_check_count__mutmut_18': xǁFormatCheckerǁ_check_count__mutmut_18, 
        'xǁFormatCheckerǁ_check_count__mutmut_19': xǁFormatCheckerǁ_check_count__mutmut_19, 
        'xǁFormatCheckerǁ_check_count__mutmut_20': xǁFormatCheckerǁ_check_count__mutmut_20, 
        'xǁFormatCheckerǁ_check_count__mutmut_21': xǁFormatCheckerǁ_check_count__mutmut_21, 
        'xǁFormatCheckerǁ_check_count__mutmut_22': xǁFormatCheckerǁ_check_count__mutmut_22, 
        'xǁFormatCheckerǁ_check_count__mutmut_23': xǁFormatCheckerǁ_check_count__mutmut_23
    }

    def _check_count(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁFormatCheckerǁ_check_count__mutmut_orig"), object.__getattribute__(self, "xǁFormatCheckerǁ_check_count__mutmut_mutants"), *args, **kwargs) 

    _check_count.__signature__ = _mutmut_signature(xǁFormatCheckerǁ_check_count__mutmut_orig)
    xǁFormatCheckerǁ_check_count__mutmut_orig.__name__ = 'xǁFormatCheckerǁ_check_count'




class Parser:
    """Class for line-wise parsing of VCF files

    In most cases, you want to use :py:class:`vcfpy.reader.Reader` instead.

    :param stream: ``file``-like object to read from
    :param str path: path the VCF is parsed from, for display purposes
        only, optional
    """

    def xǁParserǁ__init____mutmut_orig(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_1(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = None
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_2(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is not None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_3(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(None)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_4(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_5(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks and []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_6(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) and None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_7(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_8(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = ""
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_9(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = None  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_10(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = ""
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_11(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = ""
        # helper for checking the header
        self._header_checker = HeaderChecker()

    def xǁParserǁ__init____mutmut_12(
        self,
        stream: "io.TextIOWrapper",
        path: pathlib.Path | str | None = None,
        record_checks: Iterable[Literal["FORMAT", "INFO"]] | None = None,
    ):
        self.stream = stream
        self.path = None if path is None else str(path)
        #: checks to perform, can contain 'INFO' and 'FORMAT'
        self.record_checks = tuple(record_checks or []) or None
        #: header, once it has been read
        self.header = None
        # the currently read line
        self._line = stream.readline()  # trailing '\n'
        #: :py:class:`vcfpy.header.SamplesInfos` with sample information;
        #: set on parsing the header
        self.samples = None
        # helper for parsing the records
        self._record_parser = None
        # helper for checking the header
        self._header_checker = None

    xǁParserǁ__init____mutmut_mutants = {
    'xǁParserǁ__init____mutmut_1': xǁParserǁ__init____mutmut_1, 
        'xǁParserǁ__init____mutmut_2': xǁParserǁ__init____mutmut_2, 
        'xǁParserǁ__init____mutmut_3': xǁParserǁ__init____mutmut_3, 
        'xǁParserǁ__init____mutmut_4': xǁParserǁ__init____mutmut_4, 
        'xǁParserǁ__init____mutmut_5': xǁParserǁ__init____mutmut_5, 
        'xǁParserǁ__init____mutmut_6': xǁParserǁ__init____mutmut_6, 
        'xǁParserǁ__init____mutmut_7': xǁParserǁ__init____mutmut_7, 
        'xǁParserǁ__init____mutmut_8': xǁParserǁ__init____mutmut_8, 
        'xǁParserǁ__init____mutmut_9': xǁParserǁ__init____mutmut_9, 
        'xǁParserǁ__init____mutmut_10': xǁParserǁ__init____mutmut_10, 
        'xǁParserǁ__init____mutmut_11': xǁParserǁ__init____mutmut_11, 
        'xǁParserǁ__init____mutmut_12': xǁParserǁ__init____mutmut_12
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁParserǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁParserǁ__init____mutmut_orig)
    xǁParserǁ__init____mutmut_orig.__name__ = 'xǁParserǁ__init__'



    def xǁParserǁ_read_next_line__mutmut_orig(self):
        """Read next line store in self._line and return old one"""
        prev_line = self._line
        self._line = self.stream.readline()
        return prev_line

    def xǁParserǁ_read_next_line__mutmut_1(self):
        """Read next line store in self._line and return old one"""
        prev_line = None
        self._line = self.stream.readline()
        return prev_line

    def xǁParserǁ_read_next_line__mutmut_2(self):
        """Read next line store in self._line and return old one"""
        prev_line = self._line
        self._line = None
        return prev_line

    xǁParserǁ_read_next_line__mutmut_mutants = {
    'xǁParserǁ_read_next_line__mutmut_1': xǁParserǁ_read_next_line__mutmut_1, 
        'xǁParserǁ_read_next_line__mutmut_2': xǁParserǁ_read_next_line__mutmut_2
    }

    def _read_next_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁ_read_next_line__mutmut_orig"), object.__getattribute__(self, "xǁParserǁ_read_next_line__mutmut_mutants"), *args, **kwargs) 

    _read_next_line.__signature__ = _mutmut_signature(xǁParserǁ_read_next_line__mutmut_orig)
    xǁParserǁ_read_next_line__mutmut_orig.__name__ = 'xǁParserǁ_read_next_line'



    def xǁParserǁparse_header__mutmut_orig(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_1(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = None
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_2(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = None
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_3(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("XX##XX"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_4(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line or self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_5(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(None)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_6(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = None
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_7(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(None, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_8(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header( self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_9(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = None
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_10(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = None
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_11(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("XX#XX"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_12(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line or self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Expecting non-header line or EOF after "#CHROM" line')
        return self.header

    def xǁParserǁparse_header__mutmut_13(self, parsed_samples: list[str] | None = None):
        """Read and parse :py:class:`vcfpy.header.Header` from file, set
        into ``self.header`` and return it

        :param list parsed_samples: ``list`` of ``str`` for subsetting the
            samples to parse
        :returns: ``vcfpy.header.Header``
        :raises: ``vcfpy.exceptions.InvalidHeaderException`` in the case of
            problems reading the header
        """
        # parse header lines
        sub_parser = HeaderParser()
        header_lines: list[header.HeaderLine] = []
        while self._line and self._line.startswith("##"):
            header_lines.append(sub_parser.parse_line(self._line))
            self._read_next_line()
        # parse sample info line
        self.samples = self._handle_sample_line(parsed_samples)
        # construct Header object
        self.header = header.Header(header_lines, self.samples)
        # check header for consistency
        self._header_checker.run(self.header)
        # construct record parser
        self._record_parser = RecordParser(self.header, self.samples, self.record_checks)
        # read next line, must not be header
        self._read_next_line()
        if self._line and self._line.startswith("#"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('XXExpecting non-header line or EOF after "#CHROM" lineXX')
        return self.header

    xǁParserǁparse_header__mutmut_mutants = {
    'xǁParserǁparse_header__mutmut_1': xǁParserǁparse_header__mutmut_1, 
        'xǁParserǁparse_header__mutmut_2': xǁParserǁparse_header__mutmut_2, 
        'xǁParserǁparse_header__mutmut_3': xǁParserǁparse_header__mutmut_3, 
        'xǁParserǁparse_header__mutmut_4': xǁParserǁparse_header__mutmut_4, 
        'xǁParserǁparse_header__mutmut_5': xǁParserǁparse_header__mutmut_5, 
        'xǁParserǁparse_header__mutmut_6': xǁParserǁparse_header__mutmut_6, 
        'xǁParserǁparse_header__mutmut_7': xǁParserǁparse_header__mutmut_7, 
        'xǁParserǁparse_header__mutmut_8': xǁParserǁparse_header__mutmut_8, 
        'xǁParserǁparse_header__mutmut_9': xǁParserǁparse_header__mutmut_9, 
        'xǁParserǁparse_header__mutmut_10': xǁParserǁparse_header__mutmut_10, 
        'xǁParserǁparse_header__mutmut_11': xǁParserǁparse_header__mutmut_11, 
        'xǁParserǁparse_header__mutmut_12': xǁParserǁparse_header__mutmut_12, 
        'xǁParserǁparse_header__mutmut_13': xǁParserǁparse_header__mutmut_13
    }

    def parse_header(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁparse_header__mutmut_orig"), object.__getattribute__(self, "xǁParserǁparse_header__mutmut_mutants"), *args, **kwargs) 

    parse_header.__signature__ = _mutmut_signature(xǁParserǁparse_header__mutmut_orig)
    xǁParserǁparse_header__mutmut_orig.__name__ = 'xǁParserǁparse_header'



    def xǁParserǁ_handle_sample_line__mutmut_orig(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_1(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if  self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_2(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or  self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_3(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("XX#CHROMXX"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_4(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line and not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_5(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('XXMissing line starting with "#CHROM"XX')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_6(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = None
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_7(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("XXFORMATXX") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_8(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("XXFORMATXX" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_9(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" not in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_10(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("XXINFOXX")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_11(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = None
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_12(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos != -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_13(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == +1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_14(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -2:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_15(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('XXIll-formatted line starting with "#CHROM"XX')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_16(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if "XX XX" in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_17(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " not in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_18(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[None]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_19(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "XXFound space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formattedXX",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_20(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = None
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_21(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("XX\tXX")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_22(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = None

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_23(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(None)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_24(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[None], parsed_samples)

    def xǁParserǁ_handle_sample_line__mutmut_25(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :], None)

    def xǁParserǁ_handle_sample_line__mutmut_26(self, parsed_samples: list[str] | None = None):
        """ "Check and interpret the "##CHROM" line and return samples"""
        if not self._line or not self._line.startswith("#CHROM"):  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Missing line starting with "#CHROM"')
        # check for space before INFO
        line = self._line.rstrip()
        pos = line.find("FORMAT") if ("FORMAT" in line) else line.find("INFO")
        if pos == -1:  # pragma: no cover
            raise exceptions.IncorrectVCFFormat('Ill-formatted line starting with "#CHROM"')
        if " " in line[:pos]:
            warnings.warn(
                "Found space in #CHROM line, splitting at whitespace instead of tab; this VCF file is ill-formatted",
                exceptions.SpaceInChromLine,
            )
            arr = self._line.rstrip().split()
        else:
            arr = self._line.rstrip().split("\t")

        self._check_samples_line(arr)
        return header.SamplesInfos(arr[len(REQUIRE_SAMPLE_HEADER) :],)

    xǁParserǁ_handle_sample_line__mutmut_mutants = {
    'xǁParserǁ_handle_sample_line__mutmut_1': xǁParserǁ_handle_sample_line__mutmut_1, 
        'xǁParserǁ_handle_sample_line__mutmut_2': xǁParserǁ_handle_sample_line__mutmut_2, 
        'xǁParserǁ_handle_sample_line__mutmut_3': xǁParserǁ_handle_sample_line__mutmut_3, 
        'xǁParserǁ_handle_sample_line__mutmut_4': xǁParserǁ_handle_sample_line__mutmut_4, 
        'xǁParserǁ_handle_sample_line__mutmut_5': xǁParserǁ_handle_sample_line__mutmut_5, 
        'xǁParserǁ_handle_sample_line__mutmut_6': xǁParserǁ_handle_sample_line__mutmut_6, 
        'xǁParserǁ_handle_sample_line__mutmut_7': xǁParserǁ_handle_sample_line__mutmut_7, 
        'xǁParserǁ_handle_sample_line__mutmut_8': xǁParserǁ_handle_sample_line__mutmut_8, 
        'xǁParserǁ_handle_sample_line__mutmut_9': xǁParserǁ_handle_sample_line__mutmut_9, 
        'xǁParserǁ_handle_sample_line__mutmut_10': xǁParserǁ_handle_sample_line__mutmut_10, 
        'xǁParserǁ_handle_sample_line__mutmut_11': xǁParserǁ_handle_sample_line__mutmut_11, 
        'xǁParserǁ_handle_sample_line__mutmut_12': xǁParserǁ_handle_sample_line__mutmut_12, 
        'xǁParserǁ_handle_sample_line__mutmut_13': xǁParserǁ_handle_sample_line__mutmut_13, 
        'xǁParserǁ_handle_sample_line__mutmut_14': xǁParserǁ_handle_sample_line__mutmut_14, 
        'xǁParserǁ_handle_sample_line__mutmut_15': xǁParserǁ_handle_sample_line__mutmut_15, 
        'xǁParserǁ_handle_sample_line__mutmut_16': xǁParserǁ_handle_sample_line__mutmut_16, 
        'xǁParserǁ_handle_sample_line__mutmut_17': xǁParserǁ_handle_sample_line__mutmut_17, 
        'xǁParserǁ_handle_sample_line__mutmut_18': xǁParserǁ_handle_sample_line__mutmut_18, 
        'xǁParserǁ_handle_sample_line__mutmut_19': xǁParserǁ_handle_sample_line__mutmut_19, 
        'xǁParserǁ_handle_sample_line__mutmut_20': xǁParserǁ_handle_sample_line__mutmut_20, 
        'xǁParserǁ_handle_sample_line__mutmut_21': xǁParserǁ_handle_sample_line__mutmut_21, 
        'xǁParserǁ_handle_sample_line__mutmut_22': xǁParserǁ_handle_sample_line__mutmut_22, 
        'xǁParserǁ_handle_sample_line__mutmut_23': xǁParserǁ_handle_sample_line__mutmut_23, 
        'xǁParserǁ_handle_sample_line__mutmut_24': xǁParserǁ_handle_sample_line__mutmut_24, 
        'xǁParserǁ_handle_sample_line__mutmut_25': xǁParserǁ_handle_sample_line__mutmut_25, 
        'xǁParserǁ_handle_sample_line__mutmut_26': xǁParserǁ_handle_sample_line__mutmut_26
    }

    def _handle_sample_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁ_handle_sample_line__mutmut_orig"), object.__getattribute__(self, "xǁParserǁ_handle_sample_line__mutmut_mutants"), *args, **kwargs) 

    _handle_sample_line.__signature__ = _mutmut_signature(xǁParserǁ_handle_sample_line__mutmut_orig)
    xǁParserǁ_handle_sample_line__mutmut_orig.__name__ = 'xǁParserǁ_handle_sample_line'



    @classmethod
    def _check_samples_line(cls, arr: list[str]):
        """Peform additional check on samples line"""
        if len(arr) <= len(REQUIRE_NO_SAMPLE_HEADER):
            if tuple(arr) != REQUIRE_NO_SAMPLE_HEADER:
                raise exceptions.IncorrectVCFFormat(  # pragma: no cover
                    "Sample header line indicates no sample but does not equal required prefix {}".format(
                        "\t".join(REQUIRE_NO_SAMPLE_HEADER)
                    )
                )
        elif tuple(arr[: len(REQUIRE_SAMPLE_HEADER)]) != REQUIRE_SAMPLE_HEADER:
            raise exceptions.IncorrectVCFFormat(  # pragma: no cover
                'Sample header line (starting with "#CHROM") does not start with required prefix {}'.format(
                    "\t".join(REQUIRE_SAMPLE_HEADER)
                )
            )

    def xǁParserǁparse_line__mutmut_orig(self, line: str):
        """Parse the given line without reading another one from the stream"""
        if self._record_parser is None:
            raise exceptions.InvalidRecordException("Cannot parse record before parsing header")  # pragma: no cover
        return self._record_parser.parse_line(line)

    def xǁParserǁparse_line__mutmut_1(self, line: str):
        """Parse the given line without reading another one from the stream"""
        if self._record_parser is not None:
            raise exceptions.InvalidRecordException("Cannot parse record before parsing header")  # pragma: no cover
        return self._record_parser.parse_line(line)

    def xǁParserǁparse_line__mutmut_2(self, line: str):
        """Parse the given line without reading another one from the stream"""
        if self._record_parser is None:
            raise exceptions.InvalidRecordException("XXCannot parse record before parsing headerXX")  # pragma: no cover
        return self._record_parser.parse_line(line)

    def xǁParserǁparse_line__mutmut_3(self, line: str):
        """Parse the given line without reading another one from the stream"""
        if self._record_parser is None:
            raise exceptions.InvalidRecordException("Cannot parse record before parsing header")  # pragma: no cover
        return self._record_parser.parse_line(None)

    xǁParserǁparse_line__mutmut_mutants = {
    'xǁParserǁparse_line__mutmut_1': xǁParserǁparse_line__mutmut_1, 
        'xǁParserǁparse_line__mutmut_2': xǁParserǁparse_line__mutmut_2, 
        'xǁParserǁparse_line__mutmut_3': xǁParserǁparse_line__mutmut_3
    }

    def parse_line(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁparse_line__mutmut_orig"), object.__getattribute__(self, "xǁParserǁparse_line__mutmut_mutants"), *args, **kwargs) 

    parse_line.__signature__ = _mutmut_signature(xǁParserǁparse_line__mutmut_orig)
    xǁParserǁparse_line__mutmut_orig.__name__ = 'xǁParserǁparse_line'



    def xǁParserǁparse_next_record__mutmut_orig(self):
        """Read, parse and return next :py:class:`vcfpy.record.Record`

        :returns: next VCF record or ``None`` if at end
        :raises: ``vcfpy.exceptions.InvalidRecordException`` in the case of
            problems reading the record
        """
        return self.parse_line(self._read_next_line())

    xǁParserǁparse_next_record__mutmut_mutants = {

    }

    def parse_next_record(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁparse_next_record__mutmut_orig"), object.__getattribute__(self, "xǁParserǁparse_next_record__mutmut_mutants"), *args, **kwargs) 

    parse_next_record.__signature__ = _mutmut_signature(xǁParserǁparse_next_record__mutmut_orig)
    xǁParserǁparse_next_record__mutmut_orig.__name__ = 'xǁParserǁparse_next_record'



    def xǁParserǁprint_warn_summary__mutmut_orig(self):
        """If there were any warnings, print summary with warnings"""

    xǁParserǁprint_warn_summary__mutmut_mutants = {

    }

    def print_warn_summary(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁParserǁprint_warn_summary__mutmut_orig"), object.__getattribute__(self, "xǁParserǁprint_warn_summary__mutmut_mutants"), *args, **kwargs) 

    print_warn_summary.__signature__ = _mutmut_signature(xǁParserǁprint_warn_summary__mutmut_orig)
    xǁParserǁprint_warn_summary__mutmut_orig.__name__ = 'xǁParserǁprint_warn_summary'


        # TODO: remove?
