
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
"""Parsing of VCF files from ``file``-like objects"""

import gzip
import os
import pathlib
import typing
from io import TextIOWrapper

from vcfpy import parser
from vcfpy.tabix import TabixFile

__author__ = "Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>"


class Reader:
    """Class for parsing of files from ``file``-like objects

    Instead of using the constructor, use the class methods
    :py:meth:`~Reader.from_stream` and
    :py:meth:`~Reader.from_path`.

    On construction, the header will be read from the file which can cause
    problems.  After construction, :py:class:`~Reader` can be used as
    an iterable of :py:class:`~vcfpy.record.Record`.

    :raises: :py:class:`~vcfpy.exceptions.InvalidHeaderException` in the case
        of problems reading the header

    .. note::
        It is important to note that the ``header`` member is used during
        the parsing of the file.  **If you need a modified version then
        create a copy, e.g., using :py:method:`~vcfpy.header.Header.copy`**.

    .. note::
        If you use the ``parsed_samples`` feature and you write out
        records then you must not change the ``FORMAT`` of the record.
    """

    @classmethod
    def from_stream(
        cls,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: list[typing.Literal["INFO", "FORMAT"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        """Create new :py:class:`Reader` from file

        .. note::
            If you use the ``parsed_samples`` feature and you write out
            records then you must not change the ``FORMAT`` of the record.

        :param stream: ``file``-like object to read from
        :param path: optional string with path to store (for display only)
        :param list record_checks: record checks to perform, can contain
            'INFO' and 'FORMAT'
        :param list parsed_samples: ``list`` of ``str`` values with names of
            samples to parse call information for (for speedup); leave to
            ``None`` for ignoring
        """
        record_checks = record_checks or []
        if tabix_path and not path:  # pragma: no cover
            raise ValueError("Must give path if tabix_path is given")
        return Reader(
            stream=stream,
            path=path,
            tabix_path=tabix_path,
            record_checks=record_checks,
            parsed_samples=parsed_samples,
        )

    @classmethod
    def from_path(
        cls,
        path: pathlib.Path | str,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: list[typing.Literal["INFO", "FORMAT"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        """Create new :py:class:`Reader` from path

        .. note::
            If you use the ``parsed_samples`` feature and you write out
            records then you must not change the ``FORMAT`` of the record.

        :param path: the path to load from (converted to ``str`` for
            compatibility with ``path.py``)
        :param tabix_path: optional string with path to TBI index,
            automatic inferral from ``path`` will be tried on the fly
            if not given
        :param list record_checks: record checks to perform, can contain
            'INFO' and 'FORMAT'
        """
        record_checks = record_checks or []
        path = str(path)
        if path.endswith(".gz") or path.endswith(".bgz"):
            f = gzip.open(path, "rt")
            if not tabix_path:
                tabix_path = path + ".tbi"
                if not os.path.exists(tabix_path):
                    tabix_path = None  # guessing path failed
        else:
            f = open(path, "rt")
        return cls.from_stream(
            stream=f,
            path=path,
            tabix_path=tabix_path,
            record_checks=record_checks,
            parsed_samples=parsed_samples,
        )

    def xǁReaderǁ__init____mutmut_orig(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_1(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = None
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_2(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is not None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_3(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(None)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_4(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_5(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is not None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_6(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(None)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_7(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_8(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks and [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_9(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = None
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_10(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = None
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_11(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = ""
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_12(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = ""
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_13(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(None, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_14(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser( self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_15(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = None
        #: the Header
        self.header = self.parser.parse_header(parsed_samples)

    def xǁReaderǁ__init____mutmut_16(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = self.parser.parse_header(None)

    def xǁReaderǁ__init____mutmut_17(
        self,
        stream: TextIOWrapper,
        path: pathlib.Path | str | None = None,
        tabix_path: pathlib.Path | str | None = None,
        record_checks: typing.Iterable[typing.Literal["FORMAT", "INFO"]] | None = None,
        parsed_samples: list[str] | None = None,
    ):
        #: stream (``file``-like object) to read from
        self.stream = stream
        #: optional ``str`` with the path to the stream
        self.path = None if path is None else str(path)
        #: optional ``str`` with path to tabix file
        self.tabix_path = None if tabix_path is None else str(tabix_path)
        #: checks to perform on records, can contain 'FORMAT' and 'INFO'
        self.record_checks = tuple(record_checks or [])
        #: if set, list of samples to parse for
        self.parsed_samples = parsed_samples
        #: the ``pysam.TabixFile`` used for reading from index bgzip-ed VCF;
        #: constructed on the fly
        self.tabix_file = None
        # the iterator through the Tabix file to use
        self.tabix_iter = None
        #: the parser to use
        self.parser = parser.Parser(stream, self.path, self.record_checks)
        #: the Header
        self.header = None

    xǁReaderǁ__init____mutmut_mutants = {
    'xǁReaderǁ__init____mutmut_1': xǁReaderǁ__init____mutmut_1, 
        'xǁReaderǁ__init____mutmut_2': xǁReaderǁ__init____mutmut_2, 
        'xǁReaderǁ__init____mutmut_3': xǁReaderǁ__init____mutmut_3, 
        'xǁReaderǁ__init____mutmut_4': xǁReaderǁ__init____mutmut_4, 
        'xǁReaderǁ__init____mutmut_5': xǁReaderǁ__init____mutmut_5, 
        'xǁReaderǁ__init____mutmut_6': xǁReaderǁ__init____mutmut_6, 
        'xǁReaderǁ__init____mutmut_7': xǁReaderǁ__init____mutmut_7, 
        'xǁReaderǁ__init____mutmut_8': xǁReaderǁ__init____mutmut_8, 
        'xǁReaderǁ__init____mutmut_9': xǁReaderǁ__init____mutmut_9, 
        'xǁReaderǁ__init____mutmut_10': xǁReaderǁ__init____mutmut_10, 
        'xǁReaderǁ__init____mutmut_11': xǁReaderǁ__init____mutmut_11, 
        'xǁReaderǁ__init____mutmut_12': xǁReaderǁ__init____mutmut_12, 
        'xǁReaderǁ__init____mutmut_13': xǁReaderǁ__init____mutmut_13, 
        'xǁReaderǁ__init____mutmut_14': xǁReaderǁ__init____mutmut_14, 
        'xǁReaderǁ__init____mutmut_15': xǁReaderǁ__init____mutmut_15, 
        'xǁReaderǁ__init____mutmut_16': xǁReaderǁ__init____mutmut_16, 
        'xǁReaderǁ__init____mutmut_17': xǁReaderǁ__init____mutmut_17
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁReaderǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁReaderǁ__init____mutmut_orig)
    xǁReaderǁ__init____mutmut_orig.__name__ = 'xǁReaderǁ__init__'



    def xǁReaderǁfetch__mutmut_orig(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_1(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is  None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_2(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is not None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_3(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None or end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_4(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("XXbegin and end must both be None or neitherXX")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_5(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and  self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_6(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file or not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_7(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if  self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_8(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file and self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_9(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is not None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_10(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("XXCannot fetch without pathXX")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_11(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile( index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_12(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path,)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_13(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = None
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_14(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is not None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_15(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=None)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_16(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = None
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_17(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=None, start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_18(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=None, end=end)
        return self

    def xǁReaderǁfetch__mutmut_19(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin, end=None)
        return self

    def xǁReaderǁfetch__mutmut_20(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch( start=begin, end=end)
        return self

    def xǁReaderǁfetch__mutmut_21(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, end=end)
        return self

    def xǁReaderǁfetch__mutmut_22(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = self.tabix_file.fetch(reference=chrom_or_region, start=begin,)
        return self

    def xǁReaderǁfetch__mutmut_23(self, chrom_or_region: str, begin: int | None = None, end: int | None = None):
        """Jump to the start position of the given chromosomal position
        and limit iteration to the end position

        :param str chrom_or_region: name of the chromosome to jump to if
            begin and end are given and a samtools region string otherwise
            (e.g. "chr1:123,456-123,900").
        :param int begin: 0-based begin position (inclusive)
        :param int end: 0-based end position (exclusive)
        """
        if begin is not None and end is None:  # pragma: no cover
            raise ValueError("begin and end must both be None or neither")
        # close tabix file if any and is open
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        # open tabix file if not yet open
        if not self.tabix_file or self.tabix_file.closed:
            if self.path is None:  # pragma: no cover
                raise ValueError("Cannot fetch without path")
            self.tabix_file = TabixFile(filename=self.path, index=self.tabix_path)
        # jump to the next position
        if begin is None:
            self.tabix_iter = self.tabix_file.fetch(region=chrom_or_region)
        else:
            self.tabix_iter = None
        return self

    xǁReaderǁfetch__mutmut_mutants = {
    'xǁReaderǁfetch__mutmut_1': xǁReaderǁfetch__mutmut_1, 
        'xǁReaderǁfetch__mutmut_2': xǁReaderǁfetch__mutmut_2, 
        'xǁReaderǁfetch__mutmut_3': xǁReaderǁfetch__mutmut_3, 
        'xǁReaderǁfetch__mutmut_4': xǁReaderǁfetch__mutmut_4, 
        'xǁReaderǁfetch__mutmut_5': xǁReaderǁfetch__mutmut_5, 
        'xǁReaderǁfetch__mutmut_6': xǁReaderǁfetch__mutmut_6, 
        'xǁReaderǁfetch__mutmut_7': xǁReaderǁfetch__mutmut_7, 
        'xǁReaderǁfetch__mutmut_8': xǁReaderǁfetch__mutmut_8, 
        'xǁReaderǁfetch__mutmut_9': xǁReaderǁfetch__mutmut_9, 
        'xǁReaderǁfetch__mutmut_10': xǁReaderǁfetch__mutmut_10, 
        'xǁReaderǁfetch__mutmut_11': xǁReaderǁfetch__mutmut_11, 
        'xǁReaderǁfetch__mutmut_12': xǁReaderǁfetch__mutmut_12, 
        'xǁReaderǁfetch__mutmut_13': xǁReaderǁfetch__mutmut_13, 
        'xǁReaderǁfetch__mutmut_14': xǁReaderǁfetch__mutmut_14, 
        'xǁReaderǁfetch__mutmut_15': xǁReaderǁfetch__mutmut_15, 
        'xǁReaderǁfetch__mutmut_16': xǁReaderǁfetch__mutmut_16, 
        'xǁReaderǁfetch__mutmut_17': xǁReaderǁfetch__mutmut_17, 
        'xǁReaderǁfetch__mutmut_18': xǁReaderǁfetch__mutmut_18, 
        'xǁReaderǁfetch__mutmut_19': xǁReaderǁfetch__mutmut_19, 
        'xǁReaderǁfetch__mutmut_20': xǁReaderǁfetch__mutmut_20, 
        'xǁReaderǁfetch__mutmut_21': xǁReaderǁfetch__mutmut_21, 
        'xǁReaderǁfetch__mutmut_22': xǁReaderǁfetch__mutmut_22, 
        'xǁReaderǁfetch__mutmut_23': xǁReaderǁfetch__mutmut_23
    }

    def fetch(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁfetch__mutmut_orig"), object.__getattribute__(self, "xǁReaderǁfetch__mutmut_mutants"), *args, **kwargs) 

    fetch.__signature__ = _mutmut_signature(xǁReaderǁfetch__mutmut_orig)
    xǁReaderǁfetch__mutmut_orig.__name__ = 'xǁReaderǁfetch'



    def xǁReaderǁclose__mutmut_orig(self):
        """Close underlying stream"""
        if self.tabix_file and not self.tabix_file.closed:
            self.tabix_file.close()
        if self.stream:
            self.stream.close()

    def xǁReaderǁclose__mutmut_1(self):
        """Close underlying stream"""
        if self.tabix_file and  self.tabix_file.closed:
            self.tabix_file.close()
        if self.stream:
            self.stream.close()

    def xǁReaderǁclose__mutmut_2(self):
        """Close underlying stream"""
        if self.tabix_file or not self.tabix_file.closed:
            self.tabix_file.close()
        if self.stream:
            self.stream.close()

    xǁReaderǁclose__mutmut_mutants = {
    'xǁReaderǁclose__mutmut_1': xǁReaderǁclose__mutmut_1, 
        'xǁReaderǁclose__mutmut_2': xǁReaderǁclose__mutmut_2
    }

    def close(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁclose__mutmut_orig"), object.__getattribute__(self, "xǁReaderǁclose__mutmut_mutants"), *args, **kwargs) 

    close.__signature__ = _mutmut_signature(xǁReaderǁclose__mutmut_orig)
    xǁReaderǁclose__mutmut_orig.__name__ = 'xǁReaderǁclose'



    def xǁReaderǁ__enter____mutmut_orig(self) -> "Reader":
        return self

    xǁReaderǁ__enter____mutmut_mutants = {

    }

    def __enter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁReaderǁ__enter____mutmut_mutants"), *args, **kwargs) 

    __enter__.__signature__ = _mutmut_signature(xǁReaderǁ__enter____mutmut_orig)
    xǁReaderǁ__enter____mutmut_orig.__name__ = 'xǁReaderǁ__enter__'



    def xǁReaderǁ__exit____mutmut_orig(self, type_: type[BaseException] | None, value: BaseException | None, traceback: typing.Any) -> None:
        self.close()

    xǁReaderǁ__exit____mutmut_mutants = {

    }

    def __exit__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁReaderǁ__exit____mutmut_mutants"), *args, **kwargs) 

    __exit__.__signature__ = _mutmut_signature(xǁReaderǁ__exit____mutmut_orig)
    xǁReaderǁ__exit____mutmut_orig.__name__ = 'xǁReaderǁ__exit__'



    def xǁReaderǁ__iter____mutmut_orig(self):
        return self

    xǁReaderǁ__iter____mutmut_mutants = {

    }

    def __iter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁ__iter____mutmut_orig"), object.__getattribute__(self, "xǁReaderǁ__iter____mutmut_mutants"), *args, **kwargs) 

    __iter__.__signature__ = _mutmut_signature(xǁReaderǁ__iter____mutmut_orig)
    xǁReaderǁ__iter____mutmut_orig.__name__ = 'xǁReaderǁ__iter__'



    def xǁReaderǁ__next____mutmut_orig(self):
        """Return next object from file

        :returns:
        :raises: ``vcfpy.exceptions.InvalidRecordException`` in the case of
            problems reading the record
        :raises: ``StopException`` if at end
        """
        if self.tabix_iter:
            return self.parser.parse_line(str(next(self.tabix_iter)))
        else:
            result = self.parser.parse_next_record()
            if result is None:
                raise StopIteration()
            else:
                return result

    def xǁReaderǁ__next____mutmut_1(self):
        """Return next object from file

        :returns:
        :raises: ``vcfpy.exceptions.InvalidRecordException`` in the case of
            problems reading the record
        :raises: ``StopException`` if at end
        """
        if self.tabix_iter:
            return self.parser.parse_line(str(next(self.tabix_iter)))
        else:
            result = None
            if result is None:
                raise StopIteration()
            else:
                return result

    def xǁReaderǁ__next____mutmut_2(self):
        """Return next object from file

        :returns:
        :raises: ``vcfpy.exceptions.InvalidRecordException`` in the case of
            problems reading the record
        :raises: ``StopException`` if at end
        """
        if self.tabix_iter:
            return self.parser.parse_line(str(next(self.tabix_iter)))
        else:
            result = self.parser.parse_next_record()
            if result is not None:
                raise StopIteration()
            else:
                return result

    xǁReaderǁ__next____mutmut_mutants = {
    'xǁReaderǁ__next____mutmut_1': xǁReaderǁ__next____mutmut_1, 
        'xǁReaderǁ__next____mutmut_2': xǁReaderǁ__next____mutmut_2
    }

    def __next__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁReaderǁ__next____mutmut_orig"), object.__getattribute__(self, "xǁReaderǁ__next____mutmut_mutants"), *args, **kwargs) 

    __next__.__signature__ = _mutmut_signature(xǁReaderǁ__next____mutmut_orig)
    xǁReaderǁ__next____mutmut_orig.__name__ = 'xǁReaderǁ__next__'


