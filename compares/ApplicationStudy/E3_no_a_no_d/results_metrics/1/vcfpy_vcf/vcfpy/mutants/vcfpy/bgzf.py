
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
"""Support code for writing BGZF files

Shamelessly taken from Biopython
"""

#                 Biopython License Agreement
#
# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.
#
# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.

import codecs
import struct
import typing
import zlib
from typing import Iterable

# For Python 2 can just use: _bgzf_magic = '\x1f\x8b\x08\x04'
# but need to use bytes on Python 3
_bgzf_magic = b"\x1f\x8b\x08\x04"
_bgzf_header = b"\x1f\x8b\x08\x04\x00\x00\x00\x00\x00\xff\x06\x00\x42\x43\x02\x00"
_bgzf_eof = (
    b"\x1f\x8b\x08\x04\x00\x00\x00\x00\x00\xff\x06\x00BC\x02\x00\x1b\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00"
)
_bytes_BC = b"BC"


def make_virtual_offset__mutmut_orig(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_1(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset <= 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_2(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 1 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_3(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset > 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_4(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65537:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_5(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 and within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_6(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("XXRequire 0 <= within_block_offset < 2**16, got %iXX" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_7(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" / within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_8(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset <= 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_9(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 1 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_10(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset > 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_11(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710657:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_12(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 and block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_13(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("XXRequire 0 <= block_start_offset < 2**48, got %iXX" % block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_14(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" / block_start_offset)
    return (block_start_offset << 16) | within_block_offset


def make_virtual_offset__mutmut_15(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset >> 16) | within_block_offset


def make_virtual_offset__mutmut_16(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 17) | within_block_offset


def make_virtual_offset__mutmut_17(block_start_offset: int, within_block_offset: int) -> int:
    """Compute a BGZF virtual offset from block start and within block offsets.
    The BAM indexing scheme records read positions using a 64 bit
    'virtual offset', comprising in C terms:
    block_start_offset << 16 | within_block_offset
    Here block_start_offset is the file offset of the BGZF block
    start (unsigned integer using up to 64-16 = 48 bits), and
    within_block_offset within the (decompressed) block (unsigned
    16 bit integer).

    >>> make_virtual_offset(0, 0)
    0
    >>> make_virtual_offset(0, 1)
    1
    >>> make_virtual_offset(0, 2**16 - 1)
    65535
    >>> make_virtual_offset(0, 2**16)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= within_block_offset < 2**16, got 65536
    >>> 65536 == make_virtual_offset(1, 0)
    True
    >>> 65537 == make_virtual_offset(1, 1)
    True
    >>> 131071 == make_virtual_offset(1, 2**16 - 1)
    True
    >>> 6553600000 == make_virtual_offset(100000, 0)
    True
    >>> 6553600001 == make_virtual_offset(100000, 1)
    True
    >>> 6553600010 == make_virtual_offset(100000, 10)
    True
    >>> make_virtual_offset(2**48, 0)
    Traceback (most recent call last):
    ...
    ValueError: Require 0 <= block_start_offset < 2**48, got 281474976710656
    """
    if within_block_offset < 0 or within_block_offset >= 65536:
        raise ValueError("Require 0 <= within_block_offset < 2**16, got %i" % within_block_offset)
    if block_start_offset < 0 or block_start_offset >= 281474976710656:
        raise ValueError("Require 0 <= block_start_offset < 2**48, got %i" % block_start_offset)
    return (block_start_offset << 16) & within_block_offset

make_virtual_offset__mutmut_mutants = {
'make_virtual_offset__mutmut_1': make_virtual_offset__mutmut_1, 
    'make_virtual_offset__mutmut_2': make_virtual_offset__mutmut_2, 
    'make_virtual_offset__mutmut_3': make_virtual_offset__mutmut_3, 
    'make_virtual_offset__mutmut_4': make_virtual_offset__mutmut_4, 
    'make_virtual_offset__mutmut_5': make_virtual_offset__mutmut_5, 
    'make_virtual_offset__mutmut_6': make_virtual_offset__mutmut_6, 
    'make_virtual_offset__mutmut_7': make_virtual_offset__mutmut_7, 
    'make_virtual_offset__mutmut_8': make_virtual_offset__mutmut_8, 
    'make_virtual_offset__mutmut_9': make_virtual_offset__mutmut_9, 
    'make_virtual_offset__mutmut_10': make_virtual_offset__mutmut_10, 
    'make_virtual_offset__mutmut_11': make_virtual_offset__mutmut_11, 
    'make_virtual_offset__mutmut_12': make_virtual_offset__mutmut_12, 
    'make_virtual_offset__mutmut_13': make_virtual_offset__mutmut_13, 
    'make_virtual_offset__mutmut_14': make_virtual_offset__mutmut_14, 
    'make_virtual_offset__mutmut_15': make_virtual_offset__mutmut_15, 
    'make_virtual_offset__mutmut_16': make_virtual_offset__mutmut_16, 
    'make_virtual_offset__mutmut_17': make_virtual_offset__mutmut_17
}

def make_virtual_offset(*args, **kwargs):
    return _mutmut_trampoline(make_virtual_offset__mutmut_orig, make_virtual_offset__mutmut_mutants, *args, **kwargs) 

make_virtual_offset.__signature__ = _mutmut_signature(make_virtual_offset__mutmut_orig)
make_virtual_offset__mutmut_orig.__name__ = 'make_virtual_offset'




def split_virtual_offset__mutmut_orig(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset >> 16
    within_block = virtual_offset ^ (start_offset << 16)
    return start_offset, within_block


def split_virtual_offset__mutmut_1(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset << 16
    within_block = virtual_offset ^ (start_offset << 16)
    return start_offset, within_block


def split_virtual_offset__mutmut_2(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset >> 17
    within_block = virtual_offset ^ (start_offset << 16)
    return start_offset, within_block


def split_virtual_offset__mutmut_3(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = None
    within_block = virtual_offset ^ (start_offset << 16)
    return start_offset, within_block


def split_virtual_offset__mutmut_4(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset >> 16
    within_block = virtual_offset & (start_offset << 16)
    return start_offset, within_block


def split_virtual_offset__mutmut_5(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset >> 16
    within_block = virtual_offset ^ (start_offset >> 16)
    return start_offset, within_block


def split_virtual_offset__mutmut_6(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset >> 16
    within_block = virtual_offset ^ (start_offset << 17)
    return start_offset, within_block


def split_virtual_offset__mutmut_7(virtual_offset: int) -> tuple[int, int]:
    """Split a 64-bit BGZF virtual offset into block start and within block offsets.

    Returns a tuple of (block_start_offset, within_block_offset).

    >>> split_virtual_offset(0)
    (0, 0)
    >>> split_virtual_offset(1)
    (0, 1)
    >>> split_virtual_offset(65535)
    (0, 65535)
    >>> split_virtual_offset(65536)
    (1, 0)
    >>> split_virtual_offset(65537)
    (1, 1)
    >>> split_virtual_offset(1195311108)
    (18239, 4)
    """
    start_offset = virtual_offset >> 16
    within_block = None
    return start_offset, within_block

split_virtual_offset__mutmut_mutants = {
'split_virtual_offset__mutmut_1': split_virtual_offset__mutmut_1, 
    'split_virtual_offset__mutmut_2': split_virtual_offset__mutmut_2, 
    'split_virtual_offset__mutmut_3': split_virtual_offset__mutmut_3, 
    'split_virtual_offset__mutmut_4': split_virtual_offset__mutmut_4, 
    'split_virtual_offset__mutmut_5': split_virtual_offset__mutmut_5, 
    'split_virtual_offset__mutmut_6': split_virtual_offset__mutmut_6, 
    'split_virtual_offset__mutmut_7': split_virtual_offset__mutmut_7
}

def split_virtual_offset(*args, **kwargs):
    return _mutmut_trampoline(split_virtual_offset__mutmut_orig, split_virtual_offset__mutmut_mutants, *args, **kwargs) 

split_virtual_offset.__signature__ = _mutmut_signature(split_virtual_offset__mutmut_orig)
split_virtual_offset__mutmut_orig.__name__ = 'split_virtual_offset'




def _load_bgzf_block__mutmut_orig(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_1(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(11)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_2(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = None
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_3(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) <= 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_4(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 11:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_5(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("XXEOFXX")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_6(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:5] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_7(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[None] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_8(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] == _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_9(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:5]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_10(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[None]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_11(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[4]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_12(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[None]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_13(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = None
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_14(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if  (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_15(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg | 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_16(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 5):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_17(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("XXBGZF file missing FEXTRA flagXX")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_18(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(3)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_19(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = None
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_20(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) <= 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_21(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 3:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_22(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("XXTruncated BGZF extra field lengthXX")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_23(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("XX<HXX", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_24(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", None)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_25(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H",)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_26(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[1]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_27(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[None]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_28(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = None
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_29(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen <= 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_30(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 7:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_31(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("XXInvalid BGZF extra field lengthXX")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_32(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(None)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_33(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = None
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_34(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) <= xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_35(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("XXTruncated BGZF extra fieldXX")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_36(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:3] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_37(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[None] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_38(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] == _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_39(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("XXMissing BC subfield in BGZF headerXX")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_40(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) <= 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_41(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 7:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_42(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("XXBC subfield too shortXX")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_43(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("XX<HXX", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_44(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[3:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_45(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:5])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_46(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[None])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_47(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[1]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_48(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[None]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_49(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = None
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_50(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen == 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_51(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 3:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_52(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("XX<HXX", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_53(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[5:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_54(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:7])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_55(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[None])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_56(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[1]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_57(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[None]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_58(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = None

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_59(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 11 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_60(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 - 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_61(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 3 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_62(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 - xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_63(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = None
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_64(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize - 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_65(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 2) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_66(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) + header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_67(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size + 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_68(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 9

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_69(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = None

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_70(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size < 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_71(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 1:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_72(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(None)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_73(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = None
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_74(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) == cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_75(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(9)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_76(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = None
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_77(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) == 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_78(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 9:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_79(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("XXTruncated BGZF trailerXX")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_80(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("XX<IIXX", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_81(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", None)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_82(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II",)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_83(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = None

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_84(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(None, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_85(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, +15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_86(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -16)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_87(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress( -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_88(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = None
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_89(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) == isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_90(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(None) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_91(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) | 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_92(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 4294967296 != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_93(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF == crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_94(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("XXCRC32 mismatch in BGZF blockXX")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 1, result


def _load_bgzf_block__mutmut_95(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("XXlatin-1XX")

    return bsize + 1, result


def _load_bgzf_block__mutmut_96(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = None

    return bsize + 1, result


def _load_bgzf_block__mutmut_97(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize - 1, result


def _load_bgzf_block__mutmut_98(handle: typing.IO[bytes]) -> tuple[int, str]:
    """Load the next BGZF block from the file handle.

    Returns a tuple of (block_size, decompressed_data_as_string).
    Raises StopIteration if EOF is reached.
    """
    # Read the complete gzip header (10 bytes)
    # ID1 ID2 CM FLG MTIME(4) XFL OS
    header = handle.read(10)
    if len(header) < 10:  # pragma: no cover
        raise StopIteration("EOF")

    # Check magic bytes
    if header[:4] != _bgzf_magic:  # pragma: no cover
        raise ValueError(f"Invalid BGZF magic: {header[:4]!r}")

    # Check FLG field - should have FEXTRA bit set (0x04)
    flg = header[3]
    if not (flg & 0x04):  # pragma: no cover
        raise ValueError("BGZF file missing FEXTRA flag")

    # Read XLEN (extra field length)
    xlen_bytes = handle.read(2)
    if len(xlen_bytes) < 2:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field length")

    xlen = struct.unpack("<H", xlen_bytes)[0]
    if xlen < 6:  # pragma: no cover
        raise ValueError("Invalid BGZF extra field length")

    # Read the extra field
    extra_data = handle.read(xlen)
    if len(extra_data) < xlen:  # pragma: no cover
        raise ValueError("Truncated BGZF extra field")

    # Parse the BC subfield to get BSIZE
    if extra_data[:2] != _bytes_BC:  # pragma: no cover
        raise ValueError("Missing BC subfield in BGZF header")

    if len(extra_data) < 6:  # pragma: no cover
        raise ValueError("BC subfield too short")

    # BC subfield: SI1='B' SI2='C' SLEN=2 BSIZE(2 bytes)
    slen = struct.unpack("<H", extra_data[2:4])[0]
    if slen != 2:  # pragma: no cover
        raise ValueError(f"Expected BC subfield length 2, got {slen}")

    bsize = struct.unpack("<H", extra_data[4:6])[0]

    # Calculate compressed data size
    # Total block size = BSIZE + 1
    # Header size = 10 + 2 + XLEN  (header(10) + xlen(2) + extra(XLEN))
    # Trailer size = 8 (CRC32 + ISIZE)
    header_size = 10 + 2 + xlen
    cdata_size = (bsize + 1) - header_size - 8

    if cdata_size <= 0:  # pragma: no cover
        raise ValueError(f"Invalid compressed data size: {cdata_size}")

    # Read the compressed data
    compressed_data = handle.read(cdata_size)
    if len(compressed_data) != cdata_size:  # pragma: no cover
        raise ValueError(f"Truncated BGZF block data: expected {cdata_size}, got {len(compressed_data)}")

    # Read the trailer (CRC32 and ISIZE)
    trailer = handle.read(8)
    if len(trailer) != 8:  # pragma: no cover
        raise ValueError("Truncated BGZF trailer")

    crc32, isize = struct.unpack("<II", trailer)

    # Decompress the data
    try:
        # Use raw deflate decompression (negative window bits)
        data = zlib.decompress(compressed_data, -15)
    except zlib.error as e:  # pragma: no cover
        raise ValueError(f"Failed to decompress BGZF block: {e}")

    # Verify the uncompressed size
    if len(data) != isize:  # pragma: no cover
        raise ValueError(f"Uncompressed size mismatch: got {len(data)}, expected {isize}")

    # Verify the CRC32
    if zlib.crc32(data) & 0xFFFFFFFF != crc32:  # pragma: no cover
        raise ValueError("CRC32 mismatch in BGZF block")

    # Always convert to string using latin-1 encoding
    result = data.decode("latin-1")

    return bsize + 2, result

_load_bgzf_block__mutmut_mutants = {
'_load_bgzf_block__mutmut_1': _load_bgzf_block__mutmut_1, 
    '_load_bgzf_block__mutmut_2': _load_bgzf_block__mutmut_2, 
    '_load_bgzf_block__mutmut_3': _load_bgzf_block__mutmut_3, 
    '_load_bgzf_block__mutmut_4': _load_bgzf_block__mutmut_4, 
    '_load_bgzf_block__mutmut_5': _load_bgzf_block__mutmut_5, 
    '_load_bgzf_block__mutmut_6': _load_bgzf_block__mutmut_6, 
    '_load_bgzf_block__mutmut_7': _load_bgzf_block__mutmut_7, 
    '_load_bgzf_block__mutmut_8': _load_bgzf_block__mutmut_8, 
    '_load_bgzf_block__mutmut_9': _load_bgzf_block__mutmut_9, 
    '_load_bgzf_block__mutmut_10': _load_bgzf_block__mutmut_10, 
    '_load_bgzf_block__mutmut_11': _load_bgzf_block__mutmut_11, 
    '_load_bgzf_block__mutmut_12': _load_bgzf_block__mutmut_12, 
    '_load_bgzf_block__mutmut_13': _load_bgzf_block__mutmut_13, 
    '_load_bgzf_block__mutmut_14': _load_bgzf_block__mutmut_14, 
    '_load_bgzf_block__mutmut_15': _load_bgzf_block__mutmut_15, 
    '_load_bgzf_block__mutmut_16': _load_bgzf_block__mutmut_16, 
    '_load_bgzf_block__mutmut_17': _load_bgzf_block__mutmut_17, 
    '_load_bgzf_block__mutmut_18': _load_bgzf_block__mutmut_18, 
    '_load_bgzf_block__mutmut_19': _load_bgzf_block__mutmut_19, 
    '_load_bgzf_block__mutmut_20': _load_bgzf_block__mutmut_20, 
    '_load_bgzf_block__mutmut_21': _load_bgzf_block__mutmut_21, 
    '_load_bgzf_block__mutmut_22': _load_bgzf_block__mutmut_22, 
    '_load_bgzf_block__mutmut_23': _load_bgzf_block__mutmut_23, 
    '_load_bgzf_block__mutmut_24': _load_bgzf_block__mutmut_24, 
    '_load_bgzf_block__mutmut_25': _load_bgzf_block__mutmut_25, 
    '_load_bgzf_block__mutmut_26': _load_bgzf_block__mutmut_26, 
    '_load_bgzf_block__mutmut_27': _load_bgzf_block__mutmut_27, 
    '_load_bgzf_block__mutmut_28': _load_bgzf_block__mutmut_28, 
    '_load_bgzf_block__mutmut_29': _load_bgzf_block__mutmut_29, 
    '_load_bgzf_block__mutmut_30': _load_bgzf_block__mutmut_30, 
    '_load_bgzf_block__mutmut_31': _load_bgzf_block__mutmut_31, 
    '_load_bgzf_block__mutmut_32': _load_bgzf_block__mutmut_32, 
    '_load_bgzf_block__mutmut_33': _load_bgzf_block__mutmut_33, 
    '_load_bgzf_block__mutmut_34': _load_bgzf_block__mutmut_34, 
    '_load_bgzf_block__mutmut_35': _load_bgzf_block__mutmut_35, 
    '_load_bgzf_block__mutmut_36': _load_bgzf_block__mutmut_36, 
    '_load_bgzf_block__mutmut_37': _load_bgzf_block__mutmut_37, 
    '_load_bgzf_block__mutmut_38': _load_bgzf_block__mutmut_38, 
    '_load_bgzf_block__mutmut_39': _load_bgzf_block__mutmut_39, 
    '_load_bgzf_block__mutmut_40': _load_bgzf_block__mutmut_40, 
    '_load_bgzf_block__mutmut_41': _load_bgzf_block__mutmut_41, 
    '_load_bgzf_block__mutmut_42': _load_bgzf_block__mutmut_42, 
    '_load_bgzf_block__mutmut_43': _load_bgzf_block__mutmut_43, 
    '_load_bgzf_block__mutmut_44': _load_bgzf_block__mutmut_44, 
    '_load_bgzf_block__mutmut_45': _load_bgzf_block__mutmut_45, 
    '_load_bgzf_block__mutmut_46': _load_bgzf_block__mutmut_46, 
    '_load_bgzf_block__mutmut_47': _load_bgzf_block__mutmut_47, 
    '_load_bgzf_block__mutmut_48': _load_bgzf_block__mutmut_48, 
    '_load_bgzf_block__mutmut_49': _load_bgzf_block__mutmut_49, 
    '_load_bgzf_block__mutmut_50': _load_bgzf_block__mutmut_50, 
    '_load_bgzf_block__mutmut_51': _load_bgzf_block__mutmut_51, 
    '_load_bgzf_block__mutmut_52': _load_bgzf_block__mutmut_52, 
    '_load_bgzf_block__mutmut_53': _load_bgzf_block__mutmut_53, 
    '_load_bgzf_block__mutmut_54': _load_bgzf_block__mutmut_54, 
    '_load_bgzf_block__mutmut_55': _load_bgzf_block__mutmut_55, 
    '_load_bgzf_block__mutmut_56': _load_bgzf_block__mutmut_56, 
    '_load_bgzf_block__mutmut_57': _load_bgzf_block__mutmut_57, 
    '_load_bgzf_block__mutmut_58': _load_bgzf_block__mutmut_58, 
    '_load_bgzf_block__mutmut_59': _load_bgzf_block__mutmut_59, 
    '_load_bgzf_block__mutmut_60': _load_bgzf_block__mutmut_60, 
    '_load_bgzf_block__mutmut_61': _load_bgzf_block__mutmut_61, 
    '_load_bgzf_block__mutmut_62': _load_bgzf_block__mutmut_62, 
    '_load_bgzf_block__mutmut_63': _load_bgzf_block__mutmut_63, 
    '_load_bgzf_block__mutmut_64': _load_bgzf_block__mutmut_64, 
    '_load_bgzf_block__mutmut_65': _load_bgzf_block__mutmut_65, 
    '_load_bgzf_block__mutmut_66': _load_bgzf_block__mutmut_66, 
    '_load_bgzf_block__mutmut_67': _load_bgzf_block__mutmut_67, 
    '_load_bgzf_block__mutmut_68': _load_bgzf_block__mutmut_68, 
    '_load_bgzf_block__mutmut_69': _load_bgzf_block__mutmut_69, 
    '_load_bgzf_block__mutmut_70': _load_bgzf_block__mutmut_70, 
    '_load_bgzf_block__mutmut_71': _load_bgzf_block__mutmut_71, 
    '_load_bgzf_block__mutmut_72': _load_bgzf_block__mutmut_72, 
    '_load_bgzf_block__mutmut_73': _load_bgzf_block__mutmut_73, 
    '_load_bgzf_block__mutmut_74': _load_bgzf_block__mutmut_74, 
    '_load_bgzf_block__mutmut_75': _load_bgzf_block__mutmut_75, 
    '_load_bgzf_block__mutmut_76': _load_bgzf_block__mutmut_76, 
    '_load_bgzf_block__mutmut_77': _load_bgzf_block__mutmut_77, 
    '_load_bgzf_block__mutmut_78': _load_bgzf_block__mutmut_78, 
    '_load_bgzf_block__mutmut_79': _load_bgzf_block__mutmut_79, 
    '_load_bgzf_block__mutmut_80': _load_bgzf_block__mutmut_80, 
    '_load_bgzf_block__mutmut_81': _load_bgzf_block__mutmut_81, 
    '_load_bgzf_block__mutmut_82': _load_bgzf_block__mutmut_82, 
    '_load_bgzf_block__mutmut_83': _load_bgzf_block__mutmut_83, 
    '_load_bgzf_block__mutmut_84': _load_bgzf_block__mutmut_84, 
    '_load_bgzf_block__mutmut_85': _load_bgzf_block__mutmut_85, 
    '_load_bgzf_block__mutmut_86': _load_bgzf_block__mutmut_86, 
    '_load_bgzf_block__mutmut_87': _load_bgzf_block__mutmut_87, 
    '_load_bgzf_block__mutmut_88': _load_bgzf_block__mutmut_88, 
    '_load_bgzf_block__mutmut_89': _load_bgzf_block__mutmut_89, 
    '_load_bgzf_block__mutmut_90': _load_bgzf_block__mutmut_90, 
    '_load_bgzf_block__mutmut_91': _load_bgzf_block__mutmut_91, 
    '_load_bgzf_block__mutmut_92': _load_bgzf_block__mutmut_92, 
    '_load_bgzf_block__mutmut_93': _load_bgzf_block__mutmut_93, 
    '_load_bgzf_block__mutmut_94': _load_bgzf_block__mutmut_94, 
    '_load_bgzf_block__mutmut_95': _load_bgzf_block__mutmut_95, 
    '_load_bgzf_block__mutmut_96': _load_bgzf_block__mutmut_96, 
    '_load_bgzf_block__mutmut_97': _load_bgzf_block__mutmut_97, 
    '_load_bgzf_block__mutmut_98': _load_bgzf_block__mutmut_98
}

def _load_bgzf_block(*args, **kwargs):
    return _mutmut_trampoline(_load_bgzf_block__mutmut_orig, _load_bgzf_block__mutmut_mutants, *args, **kwargs) 

_load_bgzf_block.__signature__ = _mutmut_signature(_load_bgzf_block__mutmut_orig)
_load_bgzf_block__mutmut_orig.__name__ = '_load_bgzf_block'




class BgzfWriter(typing.IO[str]):
    def xǁBgzfWriterǁ__init____mutmut_orig(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_1(
        self,
        filename: str | None = None,
        mode: str = "XXwXX",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_2(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 7,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_3(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is not None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_4(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = None
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_5(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "XXwXX" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_6(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w"  in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_7(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "XXaXX" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_8(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a"  in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_9(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() or "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_10(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("XXMust use write or append mode, not %rXX" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_11(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" / mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_12(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is not None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_13(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("XXMust give a filename if not passing a file handleXX")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_14(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "XXaXX" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_15(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" not in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_16(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(None, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_17(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "XXabXX")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_18(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open( "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_19(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = None
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_20(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(None, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_21(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "XXwbXX")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_22(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open( "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_23(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = None
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_24(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b"  in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_25(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = None
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_26(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = None
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_27(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = None
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_28(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = None
        self._filename = filename
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_29(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = None
        self._mode = mode
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_30(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = None
        self._closed = False
    def xǁBgzfWriterǁ__init____mutmut_31(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = True
    def xǁBgzfWriterǁ__init____mutmut_32(
        self,
        filename: str | None = None,
        mode: str = "w",
        fileobj: typing.IO[bytes] | None = None,
        compresslevel: int = 6,
    ):
        if fileobj:
            assert filename is None
            handle = fileobj
        else:
            if "w" not in mode.lower() and "a" not in mode.lower():  # pragma: no cover
                raise ValueError("Must use write or append mode, not %r" % mode)
            if filename is None:  # pragma: no cover
                raise ValueError("Must give a filename if not passing a file handle")
            if "a" in mode.lower():  # pragma: no cover
                handle = open(filename, "ab")
            else:
                handle = open(filename, "wb")
        self._text: bool = "b" not in mode.lower()
        self._handle: typing.IO[bytes] = handle
        self._buffer: bytes = b""
        self.compresslevel: int = compresslevel
        self._filename = filename
        self._mode = mode
        self._closed = None

    xǁBgzfWriterǁ__init____mutmut_mutants = {
    'xǁBgzfWriterǁ__init____mutmut_1': xǁBgzfWriterǁ__init____mutmut_1, 
        'xǁBgzfWriterǁ__init____mutmut_2': xǁBgzfWriterǁ__init____mutmut_2, 
        'xǁBgzfWriterǁ__init____mutmut_3': xǁBgzfWriterǁ__init____mutmut_3, 
        'xǁBgzfWriterǁ__init____mutmut_4': xǁBgzfWriterǁ__init____mutmut_4, 
        'xǁBgzfWriterǁ__init____mutmut_5': xǁBgzfWriterǁ__init____mutmut_5, 
        'xǁBgzfWriterǁ__init____mutmut_6': xǁBgzfWriterǁ__init____mutmut_6, 
        'xǁBgzfWriterǁ__init____mutmut_7': xǁBgzfWriterǁ__init____mutmut_7, 
        'xǁBgzfWriterǁ__init____mutmut_8': xǁBgzfWriterǁ__init____mutmut_8, 
        'xǁBgzfWriterǁ__init____mutmut_9': xǁBgzfWriterǁ__init____mutmut_9, 
        'xǁBgzfWriterǁ__init____mutmut_10': xǁBgzfWriterǁ__init____mutmut_10, 
        'xǁBgzfWriterǁ__init____mutmut_11': xǁBgzfWriterǁ__init____mutmut_11, 
        'xǁBgzfWriterǁ__init____mutmut_12': xǁBgzfWriterǁ__init____mutmut_12, 
        'xǁBgzfWriterǁ__init____mutmut_13': xǁBgzfWriterǁ__init____mutmut_13, 
        'xǁBgzfWriterǁ__init____mutmut_14': xǁBgzfWriterǁ__init____mutmut_14, 
        'xǁBgzfWriterǁ__init____mutmut_15': xǁBgzfWriterǁ__init____mutmut_15, 
        'xǁBgzfWriterǁ__init____mutmut_16': xǁBgzfWriterǁ__init____mutmut_16, 
        'xǁBgzfWriterǁ__init____mutmut_17': xǁBgzfWriterǁ__init____mutmut_17, 
        'xǁBgzfWriterǁ__init____mutmut_18': xǁBgzfWriterǁ__init____mutmut_18, 
        'xǁBgzfWriterǁ__init____mutmut_19': xǁBgzfWriterǁ__init____mutmut_19, 
        'xǁBgzfWriterǁ__init____mutmut_20': xǁBgzfWriterǁ__init____mutmut_20, 
        'xǁBgzfWriterǁ__init____mutmut_21': xǁBgzfWriterǁ__init____mutmut_21, 
        'xǁBgzfWriterǁ__init____mutmut_22': xǁBgzfWriterǁ__init____mutmut_22, 
        'xǁBgzfWriterǁ__init____mutmut_23': xǁBgzfWriterǁ__init____mutmut_23, 
        'xǁBgzfWriterǁ__init____mutmut_24': xǁBgzfWriterǁ__init____mutmut_24, 
        'xǁBgzfWriterǁ__init____mutmut_25': xǁBgzfWriterǁ__init____mutmut_25, 
        'xǁBgzfWriterǁ__init____mutmut_26': xǁBgzfWriterǁ__init____mutmut_26, 
        'xǁBgzfWriterǁ__init____mutmut_27': xǁBgzfWriterǁ__init____mutmut_27, 
        'xǁBgzfWriterǁ__init____mutmut_28': xǁBgzfWriterǁ__init____mutmut_28, 
        'xǁBgzfWriterǁ__init____mutmut_29': xǁBgzfWriterǁ__init____mutmut_29, 
        'xǁBgzfWriterǁ__init____mutmut_30': xǁBgzfWriterǁ__init____mutmut_30, 
        'xǁBgzfWriterǁ__init____mutmut_31': xǁBgzfWriterǁ__init____mutmut_31, 
        'xǁBgzfWriterǁ__init____mutmut_32': xǁBgzfWriterǁ__init____mutmut_32
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁBgzfWriterǁ__init____mutmut_orig)
    xǁBgzfWriterǁ__init____mutmut_orig.__name__ = 'xǁBgzfWriterǁ__init__'



    def xǁBgzfWriterǁ_write_block__mutmut_orig(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_1(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) < 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_2(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65537
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_3(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, +15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_4(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -16, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_5(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 1)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_6(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = None
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_7(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(None) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_8(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) - c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_9(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = None
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_10(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) <= 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_11(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65537, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_12(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "XXTODO - Didn't compress enough, try less data in this blockXX"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_13(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(None)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_14(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = None
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_15(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc <= 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_16(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 1:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_17(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("XX<iXX", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_18(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", None)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_19(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i",)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_20(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = None
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_21(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("XX<IXX", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_22(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", None)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_23(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I",)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_24(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = None
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_25(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("XX<HXX", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_26(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) - 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_27(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 26)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_28(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = None  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_29(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("XX<IXX", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_30(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(None) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_31(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) | 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_32(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 4294967296)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_33(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = None
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_34(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("XX<IXX", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_35(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = None
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_36(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header - bsize + compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_37(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize - compressed + crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_38(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed - crc + uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_39(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc - uncompressed_length
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_40(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = None
        self._handle.write(data)

    def xǁBgzfWriterǁ_write_block__mutmut_41(self, block: bytes):
        # print("Saving %i bytes" % len(block))
        assert len(block) <= 65536
        # Giving a negative window bits means no gzip/zlib headers,
        # -15 used in samtools
        c = zlib.compressobj(self.compresslevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0)
        compressed = c.compress(block) + c.flush()
        del c
        assert len(compressed) < 65536, "TODO - Didn't compress enough, try less data in this block"
        crc = zlib.crc32(block)
        # Should cope with a mix of Python platforms...
        if crc < 0:  # pragma: no cover
            crc = struct.pack("<i", crc)
        else:
            crc = struct.pack("<I", crc)
        bsize = struct.pack("<H", len(compressed) + 25)  # includes -1
        crc = struct.pack("<I", zlib.crc32(block) & 0xFFFFFFFF)
        uncompressed_length = struct.pack("<I", len(block))
        # Fixed 16 bytes,
        # gzip magic bytes (4) mod time (4),
        # gzip flag (1), os (1), extra length which is six (2),
        # sub field which is BC (2), sub field length of two (2),
        # Variable data,
        # 2 bytes: block length as BC sub field (2)
        # X bytes: the data
        # 8 bytes: crc (4), uncompressed data length (4)
        data = _bgzf_header + bsize + compressed + crc + uncompressed_length
        self._handle.write(None)

    xǁBgzfWriterǁ_write_block__mutmut_mutants = {
    'xǁBgzfWriterǁ_write_block__mutmut_1': xǁBgzfWriterǁ_write_block__mutmut_1, 
        'xǁBgzfWriterǁ_write_block__mutmut_2': xǁBgzfWriterǁ_write_block__mutmut_2, 
        'xǁBgzfWriterǁ_write_block__mutmut_3': xǁBgzfWriterǁ_write_block__mutmut_3, 
        'xǁBgzfWriterǁ_write_block__mutmut_4': xǁBgzfWriterǁ_write_block__mutmut_4, 
        'xǁBgzfWriterǁ_write_block__mutmut_5': xǁBgzfWriterǁ_write_block__mutmut_5, 
        'xǁBgzfWriterǁ_write_block__mutmut_6': xǁBgzfWriterǁ_write_block__mutmut_6, 
        'xǁBgzfWriterǁ_write_block__mutmut_7': xǁBgzfWriterǁ_write_block__mutmut_7, 
        'xǁBgzfWriterǁ_write_block__mutmut_8': xǁBgzfWriterǁ_write_block__mutmut_8, 
        'xǁBgzfWriterǁ_write_block__mutmut_9': xǁBgzfWriterǁ_write_block__mutmut_9, 
        'xǁBgzfWriterǁ_write_block__mutmut_10': xǁBgzfWriterǁ_write_block__mutmut_10, 
        'xǁBgzfWriterǁ_write_block__mutmut_11': xǁBgzfWriterǁ_write_block__mutmut_11, 
        'xǁBgzfWriterǁ_write_block__mutmut_12': xǁBgzfWriterǁ_write_block__mutmut_12, 
        'xǁBgzfWriterǁ_write_block__mutmut_13': xǁBgzfWriterǁ_write_block__mutmut_13, 
        'xǁBgzfWriterǁ_write_block__mutmut_14': xǁBgzfWriterǁ_write_block__mutmut_14, 
        'xǁBgzfWriterǁ_write_block__mutmut_15': xǁBgzfWriterǁ_write_block__mutmut_15, 
        'xǁBgzfWriterǁ_write_block__mutmut_16': xǁBgzfWriterǁ_write_block__mutmut_16, 
        'xǁBgzfWriterǁ_write_block__mutmut_17': xǁBgzfWriterǁ_write_block__mutmut_17, 
        'xǁBgzfWriterǁ_write_block__mutmut_18': xǁBgzfWriterǁ_write_block__mutmut_18, 
        'xǁBgzfWriterǁ_write_block__mutmut_19': xǁBgzfWriterǁ_write_block__mutmut_19, 
        'xǁBgzfWriterǁ_write_block__mutmut_20': xǁBgzfWriterǁ_write_block__mutmut_20, 
        'xǁBgzfWriterǁ_write_block__mutmut_21': xǁBgzfWriterǁ_write_block__mutmut_21, 
        'xǁBgzfWriterǁ_write_block__mutmut_22': xǁBgzfWriterǁ_write_block__mutmut_22, 
        'xǁBgzfWriterǁ_write_block__mutmut_23': xǁBgzfWriterǁ_write_block__mutmut_23, 
        'xǁBgzfWriterǁ_write_block__mutmut_24': xǁBgzfWriterǁ_write_block__mutmut_24, 
        'xǁBgzfWriterǁ_write_block__mutmut_25': xǁBgzfWriterǁ_write_block__mutmut_25, 
        'xǁBgzfWriterǁ_write_block__mutmut_26': xǁBgzfWriterǁ_write_block__mutmut_26, 
        'xǁBgzfWriterǁ_write_block__mutmut_27': xǁBgzfWriterǁ_write_block__mutmut_27, 
        'xǁBgzfWriterǁ_write_block__mutmut_28': xǁBgzfWriterǁ_write_block__mutmut_28, 
        'xǁBgzfWriterǁ_write_block__mutmut_29': xǁBgzfWriterǁ_write_block__mutmut_29, 
        'xǁBgzfWriterǁ_write_block__mutmut_30': xǁBgzfWriterǁ_write_block__mutmut_30, 
        'xǁBgzfWriterǁ_write_block__mutmut_31': xǁBgzfWriterǁ_write_block__mutmut_31, 
        'xǁBgzfWriterǁ_write_block__mutmut_32': xǁBgzfWriterǁ_write_block__mutmut_32, 
        'xǁBgzfWriterǁ_write_block__mutmut_33': xǁBgzfWriterǁ_write_block__mutmut_33, 
        'xǁBgzfWriterǁ_write_block__mutmut_34': xǁBgzfWriterǁ_write_block__mutmut_34, 
        'xǁBgzfWriterǁ_write_block__mutmut_35': xǁBgzfWriterǁ_write_block__mutmut_35, 
        'xǁBgzfWriterǁ_write_block__mutmut_36': xǁBgzfWriterǁ_write_block__mutmut_36, 
        'xǁBgzfWriterǁ_write_block__mutmut_37': xǁBgzfWriterǁ_write_block__mutmut_37, 
        'xǁBgzfWriterǁ_write_block__mutmut_38': xǁBgzfWriterǁ_write_block__mutmut_38, 
        'xǁBgzfWriterǁ_write_block__mutmut_39': xǁBgzfWriterǁ_write_block__mutmut_39, 
        'xǁBgzfWriterǁ_write_block__mutmut_40': xǁBgzfWriterǁ_write_block__mutmut_40, 
        'xǁBgzfWriterǁ_write_block__mutmut_41': xǁBgzfWriterǁ_write_block__mutmut_41
    }

    def _write_block(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁ_write_block__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁ_write_block__mutmut_mutants"), *args, **kwargs) 

    _write_block.__signature__ = _mutmut_signature(xǁBgzfWriterǁ_write_block__mutmut_orig)
    xǁBgzfWriterǁ_write_block__mutmut_orig.__name__ = 'xǁBgzfWriterǁ_write_block'



    def xǁBgzfWriterǁwrite__mutmut_orig(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_1(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("XXI/O operation on closed file.XX")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_2(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = None
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_3(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(None)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_4(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[1]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_5(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[None]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_6(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = None

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_7(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = None
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_8(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) - data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_9(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len <= 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_10(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65537:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_11(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer -= data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_12(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer = data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_13(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer -= data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_14(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer = data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_15(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) > 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_16(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65537:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_17(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65537])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_18(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[None])
                self._buffer = self._buffer[65536:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_19(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[65537:]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_20(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = self._buffer[None]

        return original_len

    def xǁBgzfWriterǁwrite__mutmut_21(self, data: str) -> int:
        """Write string data to the BGZF file.

        Args:
            data: String data to write

        Returns:
            Number of characters written
        """
        if self._closed:  # pragma: no cover
            raise ValueError("I/O operation on closed file.")

        original_len = len(data)
        # Convert string to bytes using latin-1 encoding
        data_bytes = codecs.latin_1_encode(data)[0]

        # block_size = 2**16 = 65536
        data_len = len(data_bytes)
        if len(self._buffer) + data_len < 65536:
            # print("Cached %r" % data)
            self._buffer += data_bytes
        else:  # pragma: no cover
            # print("Got %r, writing out some data..." % data)
            self._buffer += data_bytes
            while len(self._buffer) >= 65536:
                self._write_block(self._buffer[:65536])
                self._buffer = None

        return original_len

    xǁBgzfWriterǁwrite__mutmut_mutants = {
    'xǁBgzfWriterǁwrite__mutmut_1': xǁBgzfWriterǁwrite__mutmut_1, 
        'xǁBgzfWriterǁwrite__mutmut_2': xǁBgzfWriterǁwrite__mutmut_2, 
        'xǁBgzfWriterǁwrite__mutmut_3': xǁBgzfWriterǁwrite__mutmut_3, 
        'xǁBgzfWriterǁwrite__mutmut_4': xǁBgzfWriterǁwrite__mutmut_4, 
        'xǁBgzfWriterǁwrite__mutmut_5': xǁBgzfWriterǁwrite__mutmut_5, 
        'xǁBgzfWriterǁwrite__mutmut_6': xǁBgzfWriterǁwrite__mutmut_6, 
        'xǁBgzfWriterǁwrite__mutmut_7': xǁBgzfWriterǁwrite__mutmut_7, 
        'xǁBgzfWriterǁwrite__mutmut_8': xǁBgzfWriterǁwrite__mutmut_8, 
        'xǁBgzfWriterǁwrite__mutmut_9': xǁBgzfWriterǁwrite__mutmut_9, 
        'xǁBgzfWriterǁwrite__mutmut_10': xǁBgzfWriterǁwrite__mutmut_10, 
        'xǁBgzfWriterǁwrite__mutmut_11': xǁBgzfWriterǁwrite__mutmut_11, 
        'xǁBgzfWriterǁwrite__mutmut_12': xǁBgzfWriterǁwrite__mutmut_12, 
        'xǁBgzfWriterǁwrite__mutmut_13': xǁBgzfWriterǁwrite__mutmut_13, 
        'xǁBgzfWriterǁwrite__mutmut_14': xǁBgzfWriterǁwrite__mutmut_14, 
        'xǁBgzfWriterǁwrite__mutmut_15': xǁBgzfWriterǁwrite__mutmut_15, 
        'xǁBgzfWriterǁwrite__mutmut_16': xǁBgzfWriterǁwrite__mutmut_16, 
        'xǁBgzfWriterǁwrite__mutmut_17': xǁBgzfWriterǁwrite__mutmut_17, 
        'xǁBgzfWriterǁwrite__mutmut_18': xǁBgzfWriterǁwrite__mutmut_18, 
        'xǁBgzfWriterǁwrite__mutmut_19': xǁBgzfWriterǁwrite__mutmut_19, 
        'xǁBgzfWriterǁwrite__mutmut_20': xǁBgzfWriterǁwrite__mutmut_20, 
        'xǁBgzfWriterǁwrite__mutmut_21': xǁBgzfWriterǁwrite__mutmut_21
    }

    def write(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁwrite__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁwrite__mutmut_mutants"), *args, **kwargs) 

    write.__signature__ = _mutmut_signature(xǁBgzfWriterǁwrite__mutmut_orig)
    xǁBgzfWriterǁwrite__mutmut_orig.__name__ = 'xǁBgzfWriterǁwrite'



    def xǁBgzfWriterǁflush__mutmut_orig(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_1(self):
        while len(self._buffer) > 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_2(self):
        while len(self._buffer) >= 65537:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_3(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65536])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_4(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[None])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_5(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[65536:]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_6(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[None]
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_7(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = None
        self._write_block(self._buffer)
        self._buffer = b""
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_8(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = b"XXXX"
        self._handle.flush()

    def xǁBgzfWriterǁflush__mutmut_9(self):
        while len(self._buffer) >= 65536:  # pragma: no cover
            self._write_block(self._buffer[:65535])
            self._buffer = self._buffer[65535:]
        self._write_block(self._buffer)
        self._buffer = None
        self._handle.flush()

    xǁBgzfWriterǁflush__mutmut_mutants = {
    'xǁBgzfWriterǁflush__mutmut_1': xǁBgzfWriterǁflush__mutmut_1, 
        'xǁBgzfWriterǁflush__mutmut_2': xǁBgzfWriterǁflush__mutmut_2, 
        'xǁBgzfWriterǁflush__mutmut_3': xǁBgzfWriterǁflush__mutmut_3, 
        'xǁBgzfWriterǁflush__mutmut_4': xǁBgzfWriterǁflush__mutmut_4, 
        'xǁBgzfWriterǁflush__mutmut_5': xǁBgzfWriterǁflush__mutmut_5, 
        'xǁBgzfWriterǁflush__mutmut_6': xǁBgzfWriterǁflush__mutmut_6, 
        'xǁBgzfWriterǁflush__mutmut_7': xǁBgzfWriterǁflush__mutmut_7, 
        'xǁBgzfWriterǁflush__mutmut_8': xǁBgzfWriterǁflush__mutmut_8, 
        'xǁBgzfWriterǁflush__mutmut_9': xǁBgzfWriterǁflush__mutmut_9
    }

    def flush(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁflush__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁflush__mutmut_mutants"), *args, **kwargs) 

    flush.__signature__ = _mutmut_signature(xǁBgzfWriterǁflush__mutmut_orig)
    xǁBgzfWriterǁflush__mutmut_orig.__name__ = 'xǁBgzfWriterǁflush'



    def xǁBgzfWriterǁclose__mutmut_orig(self) -> None:
        """Flush data, write 28 bytes BGZF EOF marker, and close BGZF file.
        samtools will look for a magic EOF marker, just a 28 byte empty BGZF
        block, and if it is missing warns the BAM file may be truncated. In
        addition to samtools writing this block, so too does bgzip - so this
        implementation does too.
        """
        if self._closed:  # pragma: no cover
            return

        if self._buffer:
            self.flush()
        self._handle.write(_bgzf_eof)
        self._handle.flush()
        self._handle.close()
        self._closed = True

    def xǁBgzfWriterǁclose__mutmut_1(self) -> None:
        """Flush data, write 28 bytes BGZF EOF marker, and close BGZF file.
        samtools will look for a magic EOF marker, just a 28 byte empty BGZF
        block, and if it is missing warns the BAM file may be truncated. In
        addition to samtools writing this block, so too does bgzip - so this
        implementation does too.
        """
        if self._closed:  # pragma: no cover
            return

        if self._buffer:
            self.flush()
        self._handle.write(None)
        self._handle.flush()
        self._handle.close()
        self._closed = True

    def xǁBgzfWriterǁclose__mutmut_2(self) -> None:
        """Flush data, write 28 bytes BGZF EOF marker, and close BGZF file.
        samtools will look for a magic EOF marker, just a 28 byte empty BGZF
        block, and if it is missing warns the BAM file may be truncated. In
        addition to samtools writing this block, so too does bgzip - so this
        implementation does too.
        """
        if self._closed:  # pragma: no cover
            return

        if self._buffer:
            self.flush()
        self._handle.write(_bgzf_eof)
        self._handle.flush()
        self._handle.close()
        self._closed = False

    def xǁBgzfWriterǁclose__mutmut_3(self) -> None:
        """Flush data, write 28 bytes BGZF EOF marker, and close BGZF file.
        samtools will look for a magic EOF marker, just a 28 byte empty BGZF
        block, and if it is missing warns the BAM file may be truncated. In
        addition to samtools writing this block, so too does bgzip - so this
        implementation does too.
        """
        if self._closed:  # pragma: no cover
            return

        if self._buffer:
            self.flush()
        self._handle.write(_bgzf_eof)
        self._handle.flush()
        self._handle.close()
        self._closed = None

    xǁBgzfWriterǁclose__mutmut_mutants = {
    'xǁBgzfWriterǁclose__mutmut_1': xǁBgzfWriterǁclose__mutmut_1, 
        'xǁBgzfWriterǁclose__mutmut_2': xǁBgzfWriterǁclose__mutmut_2, 
        'xǁBgzfWriterǁclose__mutmut_3': xǁBgzfWriterǁclose__mutmut_3
    }

    def close(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁclose__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁclose__mutmut_mutants"), *args, **kwargs) 

    close.__signature__ = _mutmut_signature(xǁBgzfWriterǁclose__mutmut_orig)
    xǁBgzfWriterǁclose__mutmut_orig.__name__ = 'xǁBgzfWriterǁclose'



    def xǁBgzfWriterǁtell__mutmut_orig(self) -> int:  # pragma: no cover
        """Returns a BGZF 64-bit virtual offset."""
        return make_virtual_offset(self._handle.tell(), len(self._buffer))

    xǁBgzfWriterǁtell__mutmut_mutants = {

    }

    def tell(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁtell__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁtell__mutmut_mutants"), *args, **kwargs) 

    tell.__signature__ = _mutmut_signature(xǁBgzfWriterǁtell__mutmut_orig)
    xǁBgzfWriterǁtell__mutmut_orig.__name__ = 'xǁBgzfWriterǁtell'



    def xǁBgzfWriterǁseekable__mutmut_orig(self) -> bool:  # pragma: no cover
        # Not seekable, but we do support tell...
        return False

    def xǁBgzfWriterǁseekable__mutmut_1(self) -> bool:  # pragma: no cover
        # Not seekable, but we do support tell...
        return True

    xǁBgzfWriterǁseekable__mutmut_mutants = {
    'xǁBgzfWriterǁseekable__mutmut_1': xǁBgzfWriterǁseekable__mutmut_1
    }

    def seekable(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁseekable__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁseekable__mutmut_mutants"), *args, **kwargs) 

    seekable.__signature__ = _mutmut_signature(xǁBgzfWriterǁseekable__mutmut_orig)
    xǁBgzfWriterǁseekable__mutmut_orig.__name__ = 'xǁBgzfWriterǁseekable'



    def xǁBgzfWriterǁisatty__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return False as BGZF files are not TTY."""
        return False

    def xǁBgzfWriterǁisatty__mutmut_1(self) -> bool:  # pragma: no cover
        """Return False as BGZF files are not TTY."""
        return True

    xǁBgzfWriterǁisatty__mutmut_mutants = {
    'xǁBgzfWriterǁisatty__mutmut_1': xǁBgzfWriterǁisatty__mutmut_1
    }

    def isatty(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁisatty__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁisatty__mutmut_mutants"), *args, **kwargs) 

    isatty.__signature__ = _mutmut_signature(xǁBgzfWriterǁisatty__mutmut_orig)
    xǁBgzfWriterǁisatty__mutmut_orig.__name__ = 'xǁBgzfWriterǁisatty'



    @property
    def closed(self) -> bool:  # pragma: no cover
        """Return True if the file is closed."""
        return self._closed

    @property
    def mode(self) -> str:  # pragma: no cover
        """Return the file mode."""
        return self._mode

    @property
    def name(self) -> str:  # pragma: no cover
        """Return the file name."""
        return self._filename or ""

    def xǁBgzfWriterǁreadable__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return False as this is a write-only file."""
        return False

    def xǁBgzfWriterǁreadable__mutmut_1(self) -> bool:  # pragma: no cover
        """Return False as this is a write-only file."""
        return True

    xǁBgzfWriterǁreadable__mutmut_mutants = {
    'xǁBgzfWriterǁreadable__mutmut_1': xǁBgzfWriterǁreadable__mutmut_1
    }

    def readable(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁreadable__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁreadable__mutmut_mutants"), *args, **kwargs) 

    readable.__signature__ = _mutmut_signature(xǁBgzfWriterǁreadable__mutmut_orig)
    xǁBgzfWriterǁreadable__mutmut_orig.__name__ = 'xǁBgzfWriterǁreadable'



    def xǁBgzfWriterǁwritable__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return True as this is a writable file."""
        return not self._closed

    def xǁBgzfWriterǁwritable__mutmut_1(self) -> bool:  # pragma: no cover
        """Return True as this is a writable file."""
        return  self._closed

    xǁBgzfWriterǁwritable__mutmut_mutants = {
    'xǁBgzfWriterǁwritable__mutmut_1': xǁBgzfWriterǁwritable__mutmut_1
    }

    def writable(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁwritable__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁwritable__mutmut_mutants"), *args, **kwargs) 

    writable.__signature__ = _mutmut_signature(xǁBgzfWriterǁwritable__mutmut_orig)
    xǁBgzfWriterǁwritable__mutmut_orig.__name__ = 'xǁBgzfWriterǁwritable'



    def xǁBgzfWriterǁread__mutmut_orig(self, size: int = -1) -> str:  # pragma: no cover
        """Read operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁread__mutmut_1(self, size: int = +1) -> str:  # pragma: no cover
        """Read operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁread__mutmut_2(self, size: int = -2) -> str:  # pragma: no cover
        """Read operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁread__mutmut_3(self, size: int = -1) -> str:  # pragma: no cover
        """Read operation not supported for write-only BGZF file."""
        raise OSError("XXnot readableXX")

    xǁBgzfWriterǁread__mutmut_mutants = {
    'xǁBgzfWriterǁread__mutmut_1': xǁBgzfWriterǁread__mutmut_1, 
        'xǁBgzfWriterǁread__mutmut_2': xǁBgzfWriterǁread__mutmut_2, 
        'xǁBgzfWriterǁread__mutmut_3': xǁBgzfWriterǁread__mutmut_3
    }

    def read(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁread__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁread__mutmut_mutants"), *args, **kwargs) 

    read.__signature__ = _mutmut_signature(xǁBgzfWriterǁread__mutmut_orig)
    xǁBgzfWriterǁread__mutmut_orig.__name__ = 'xǁBgzfWriterǁread'



    def xǁBgzfWriterǁreadline__mutmut_orig(self, size: int = -1) -> str:  # pragma: no cover
        """Readline operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁreadline__mutmut_1(self, size: int = +1) -> str:  # pragma: no cover
        """Readline operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁreadline__mutmut_2(self, size: int = -2) -> str:  # pragma: no cover
        """Readline operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁreadline__mutmut_3(self, size: int = -1) -> str:  # pragma: no cover
        """Readline operation not supported for write-only BGZF file."""
        raise OSError("XXnot readableXX")

    xǁBgzfWriterǁreadline__mutmut_mutants = {
    'xǁBgzfWriterǁreadline__mutmut_1': xǁBgzfWriterǁreadline__mutmut_1, 
        'xǁBgzfWriterǁreadline__mutmut_2': xǁBgzfWriterǁreadline__mutmut_2, 
        'xǁBgzfWriterǁreadline__mutmut_3': xǁBgzfWriterǁreadline__mutmut_3
    }

    def readline(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁreadline__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁreadline__mutmut_mutants"), *args, **kwargs) 

    readline.__signature__ = _mutmut_signature(xǁBgzfWriterǁreadline__mutmut_orig)
    xǁBgzfWriterǁreadline__mutmut_orig.__name__ = 'xǁBgzfWriterǁreadline'



    def xǁBgzfWriterǁreadlines__mutmut_orig(self, hint: int = -1) -> list[str]:  # pragma: no cover
        """Readlines operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁreadlines__mutmut_1(self, hint: int = +1) -> list[str]:  # pragma: no cover
        """Readlines operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁreadlines__mutmut_2(self, hint: int = -2) -> list[str]:  # pragma: no cover
        """Readlines operation not supported for write-only BGZF file."""
        raise OSError("not readable")

    def xǁBgzfWriterǁreadlines__mutmut_3(self, hint: int = -1) -> list[str]:  # pragma: no cover
        """Readlines operation not supported for write-only BGZF file."""
        raise OSError("XXnot readableXX")

    xǁBgzfWriterǁreadlines__mutmut_mutants = {
    'xǁBgzfWriterǁreadlines__mutmut_1': xǁBgzfWriterǁreadlines__mutmut_1, 
        'xǁBgzfWriterǁreadlines__mutmut_2': xǁBgzfWriterǁreadlines__mutmut_2, 
        'xǁBgzfWriterǁreadlines__mutmut_3': xǁBgzfWriterǁreadlines__mutmut_3
    }

    def readlines(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁreadlines__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁreadlines__mutmut_mutants"), *args, **kwargs) 

    readlines.__signature__ = _mutmut_signature(xǁBgzfWriterǁreadlines__mutmut_orig)
    xǁBgzfWriterǁreadlines__mutmut_orig.__name__ = 'xǁBgzfWriterǁreadlines'



    def xǁBgzfWriterǁseek__mutmut_orig(self, offset: int, whence: int = 0) -> int:  # pragma: no cover
        """Seek operation not supported for BGZF files."""
        raise OSError("seek not supported on BGZF files")

    def xǁBgzfWriterǁseek__mutmut_1(self, offset: int, whence: int = 1) -> int:  # pragma: no cover
        """Seek operation not supported for BGZF files."""
        raise OSError("seek not supported on BGZF files")

    def xǁBgzfWriterǁseek__mutmut_2(self, offset: int, whence: int = 0) -> int:  # pragma: no cover
        """Seek operation not supported for BGZF files."""
        raise OSError("XXseek not supported on BGZF filesXX")

    xǁBgzfWriterǁseek__mutmut_mutants = {
    'xǁBgzfWriterǁseek__mutmut_1': xǁBgzfWriterǁseek__mutmut_1, 
        'xǁBgzfWriterǁseek__mutmut_2': xǁBgzfWriterǁseek__mutmut_2
    }

    def seek(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁseek__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁseek__mutmut_mutants"), *args, **kwargs) 

    seek.__signature__ = _mutmut_signature(xǁBgzfWriterǁseek__mutmut_orig)
    xǁBgzfWriterǁseek__mutmut_orig.__name__ = 'xǁBgzfWriterǁseek'



    def xǁBgzfWriterǁtruncate__mutmut_orig(self, size: int | None = None) -> int:  # pragma: no cover
        """Truncate operation not supported for BGZF files."""
        raise OSError("truncate not supported on BGZF files")

    def xǁBgzfWriterǁtruncate__mutmut_1(self, size: int | None = None) -> int:  # pragma: no cover
        """Truncate operation not supported for BGZF files."""
        raise OSError("XXtruncate not supported on BGZF filesXX")

    xǁBgzfWriterǁtruncate__mutmut_mutants = {
    'xǁBgzfWriterǁtruncate__mutmut_1': xǁBgzfWriterǁtruncate__mutmut_1
    }

    def truncate(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁtruncate__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁtruncate__mutmut_mutants"), *args, **kwargs) 

    truncate.__signature__ = _mutmut_signature(xǁBgzfWriterǁtruncate__mutmut_orig)
    xǁBgzfWriterǁtruncate__mutmut_orig.__name__ = 'xǁBgzfWriterǁtruncate'



    def xǁBgzfWriterǁwritelines__mutmut_orig(self, lines: Iterable[str]) -> None:
        """Write a list of strings to the file."""
        for line in lines:
            self.write(line)

    def xǁBgzfWriterǁwritelines__mutmut_1(self, lines: Iterable[str]) -> None:
        """Write a list of strings to the file."""
        for line in lines:
            self.write(None)

    xǁBgzfWriterǁwritelines__mutmut_mutants = {
    'xǁBgzfWriterǁwritelines__mutmut_1': xǁBgzfWriterǁwritelines__mutmut_1
    }

    def writelines(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁwritelines__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁwritelines__mutmut_mutants"), *args, **kwargs) 

    writelines.__signature__ = _mutmut_signature(xǁBgzfWriterǁwritelines__mutmut_orig)
    xǁBgzfWriterǁwritelines__mutmut_orig.__name__ = 'xǁBgzfWriterǁwritelines'



    def xǁBgzfWriterǁfileno__mutmut_orig(self) -> int:
        return self._handle.fileno()

    xǁBgzfWriterǁfileno__mutmut_mutants = {

    }

    def fileno(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁfileno__mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁfileno__mutmut_mutants"), *args, **kwargs) 

    fileno.__signature__ = _mutmut_signature(xǁBgzfWriterǁfileno__mutmut_orig)
    xǁBgzfWriterǁfileno__mutmut_orig.__name__ = 'xǁBgzfWriterǁfileno'



    def xǁBgzfWriterǁ__enter____mutmut_orig(self) -> "BgzfWriter":
        return self

    xǁBgzfWriterǁ__enter____mutmut_mutants = {

    }

    def __enter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁ__enter____mutmut_mutants"), *args, **kwargs) 

    __enter__.__signature__ = _mutmut_signature(xǁBgzfWriterǁ__enter____mutmut_orig)
    xǁBgzfWriterǁ__enter____mutmut_orig.__name__ = 'xǁBgzfWriterǁ__enter__'



    def xǁBgzfWriterǁ__exit____mutmut_orig(self, type_: type[BaseException] | None, value: BaseException | None, traceback: typing.Any) -> None:
        self.close()

    xǁBgzfWriterǁ__exit____mutmut_mutants = {

    }

    def __exit__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfWriterǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁBgzfWriterǁ__exit____mutmut_mutants"), *args, **kwargs) 

    __exit__.__signature__ = _mutmut_signature(xǁBgzfWriterǁ__exit____mutmut_orig)
    xǁBgzfWriterǁ__exit____mutmut_orig.__name__ = 'xǁBgzfWriterǁ__exit__'




class BgzfReader(typing.IO[str]):
    r"""BGZF reader, acts like a read only handle but seek/tell differ."""

    def xǁBgzfReaderǁ__init____mutmut_orig(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_1(
        self,
        filename: str | None = None,
        mode: str = "XXrXX",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_2(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 101,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_3(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache <= 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_4(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 2:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_5(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("XXUse max_cache with a minimum of 1XX")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_6(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename or fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_7(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("XXSupply either filename or fileobj, not bothXX")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_8(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower()  in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_9(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("XXrXX", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_10(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "XXtrXX", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_11(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "XXrtXX", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_12(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "XXrbXX", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_13(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "XXbrXX"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_14(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("XXMust use a read mode like 'r' (default), 'rt', or 'rb' for binaryXX")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_15(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(1) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_16(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) == b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_17(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"XXXX":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_18(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("XXfileobj not opened in binary modeXX")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_19(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = None
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_20(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is not None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_21(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("XXMust provide filename if fileobj is NoneXX")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_22(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(None, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_23(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "XXrbXX")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_24(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open( "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_25(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = None

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_26(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "XX\nXX"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_27(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = None
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_28(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = None
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_29(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = None
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_30(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = None
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_31(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = +1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_32(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -2  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_33(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = None  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_34(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 1
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_35(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = None
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_36(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 1
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_37(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = None
        self._buffer: str = ""
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_38(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = None
        self._load_block(0)  # Start at offset 0

    def xǁBgzfReaderǁ__init____mutmut_39(
        self,
        filename: str | None = None,
        mode: str = "r",
        fileobj: typing.IO[bytes] | None = None,
        max_cache: int = 100,
    ):
        r"""Initialize the class for reading a BGZF file.

        You would typically use the top level ``bgzf.open(...)`` function
        which will call this class internally. Direct use is discouraged.

        Either the ``filename`` (string) or ``fileobj`` (input file object in
        binary mode) arguments must be supplied, but not both.

        Argument ``mode`` controls if the data will be returned as strings in
        text mode ("rt", "tr", or default "r"), or bytes binary mode ("rb"
        or "br"). The argument name matches the built-in ``open(...)`` and
        standard library ``gzip.open(...)`` function.

        If text mode is requested, in order to avoid multi-byte characters,
        this is hard coded to use the "latin1" encoding, and "\r" and "\n"
        are passed as is (without implementing universal new line mode). There
        is no ``encoding`` argument.

        If your data is in UTF-8 or any other incompatible encoding, you must
        use binary mode, and decode the appropriate fragments yourself.

        Argument ``max_cache`` controls the maximum number of BGZF blocks to
        cache in memory. Each can be up to 64kb thus the default of 100 blocks
        could take up to 6MB of RAM. This is important for efficient random
        access, a small value is fine for reading the file in one pass.
        """
        # TODO - Assuming we can seek, check for 28 bytes EOF empty block
        # and if missing warn about possible truncation (as in samtools)?
        if max_cache < 1:  # pragma: no cover
            raise ValueError("Use max_cache with a minimum of 1")
        # Must open the BGZF file in binary mode, but we may want to
        # treat the contents as either text or binary (unicode or
        # bytes under Python 3)
        if filename and fileobj:
            raise ValueError("Supply either filename or fileobj, not both")
        # Want to reject output modes like w, a, x, +
        if mode.lower() not in ("r", "tr", "rt", "rb", "br"):  # pragma: no cover
            raise ValueError("Must use a read mode like 'r' (default), 'rt', or 'rb' for binary")
        # If an open file was passed, make sure it was opened in binary mode.
        if fileobj:
            if fileobj.read(0) != b"":  # pragma: no cover
                raise ValueError("fileobj not opened in binary mode")
            handle = fileobj
        else:
            if filename is None:  # pragma: no cover
                raise ValueError("Must provide filename if fileobj is None")
            handle = open(filename, "rb")

        # Always read bytes from disk but return strings to the outside world
        self._newline = "\n"
        self._handle = handle
        self.max_cache = max_cache
        self._buffers: dict[int, tuple[str, int]] = {}
        self._block_start_offset: int = -1  # Force initial load
        self._block_raw_length: int = 0
        self._within_block_offset: int = 0
        self._buffer: str = ""
        self._load_block(1)  # Start at offset 0

    xǁBgzfReaderǁ__init____mutmut_mutants = {
    'xǁBgzfReaderǁ__init____mutmut_1': xǁBgzfReaderǁ__init____mutmut_1, 
        'xǁBgzfReaderǁ__init____mutmut_2': xǁBgzfReaderǁ__init____mutmut_2, 
        'xǁBgzfReaderǁ__init____mutmut_3': xǁBgzfReaderǁ__init____mutmut_3, 
        'xǁBgzfReaderǁ__init____mutmut_4': xǁBgzfReaderǁ__init____mutmut_4, 
        'xǁBgzfReaderǁ__init____mutmut_5': xǁBgzfReaderǁ__init____mutmut_5, 
        'xǁBgzfReaderǁ__init____mutmut_6': xǁBgzfReaderǁ__init____mutmut_6, 
        'xǁBgzfReaderǁ__init____mutmut_7': xǁBgzfReaderǁ__init____mutmut_7, 
        'xǁBgzfReaderǁ__init____mutmut_8': xǁBgzfReaderǁ__init____mutmut_8, 
        'xǁBgzfReaderǁ__init____mutmut_9': xǁBgzfReaderǁ__init____mutmut_9, 
        'xǁBgzfReaderǁ__init____mutmut_10': xǁBgzfReaderǁ__init____mutmut_10, 
        'xǁBgzfReaderǁ__init____mutmut_11': xǁBgzfReaderǁ__init____mutmut_11, 
        'xǁBgzfReaderǁ__init____mutmut_12': xǁBgzfReaderǁ__init____mutmut_12, 
        'xǁBgzfReaderǁ__init____mutmut_13': xǁBgzfReaderǁ__init____mutmut_13, 
        'xǁBgzfReaderǁ__init____mutmut_14': xǁBgzfReaderǁ__init____mutmut_14, 
        'xǁBgzfReaderǁ__init____mutmut_15': xǁBgzfReaderǁ__init____mutmut_15, 
        'xǁBgzfReaderǁ__init____mutmut_16': xǁBgzfReaderǁ__init____mutmut_16, 
        'xǁBgzfReaderǁ__init____mutmut_17': xǁBgzfReaderǁ__init____mutmut_17, 
        'xǁBgzfReaderǁ__init____mutmut_18': xǁBgzfReaderǁ__init____mutmut_18, 
        'xǁBgzfReaderǁ__init____mutmut_19': xǁBgzfReaderǁ__init____mutmut_19, 
        'xǁBgzfReaderǁ__init____mutmut_20': xǁBgzfReaderǁ__init____mutmut_20, 
        'xǁBgzfReaderǁ__init____mutmut_21': xǁBgzfReaderǁ__init____mutmut_21, 
        'xǁBgzfReaderǁ__init____mutmut_22': xǁBgzfReaderǁ__init____mutmut_22, 
        'xǁBgzfReaderǁ__init____mutmut_23': xǁBgzfReaderǁ__init____mutmut_23, 
        'xǁBgzfReaderǁ__init____mutmut_24': xǁBgzfReaderǁ__init____mutmut_24, 
        'xǁBgzfReaderǁ__init____mutmut_25': xǁBgzfReaderǁ__init____mutmut_25, 
        'xǁBgzfReaderǁ__init____mutmut_26': xǁBgzfReaderǁ__init____mutmut_26, 
        'xǁBgzfReaderǁ__init____mutmut_27': xǁBgzfReaderǁ__init____mutmut_27, 
        'xǁBgzfReaderǁ__init____mutmut_28': xǁBgzfReaderǁ__init____mutmut_28, 
        'xǁBgzfReaderǁ__init____mutmut_29': xǁBgzfReaderǁ__init____mutmut_29, 
        'xǁBgzfReaderǁ__init____mutmut_30': xǁBgzfReaderǁ__init____mutmut_30, 
        'xǁBgzfReaderǁ__init____mutmut_31': xǁBgzfReaderǁ__init____mutmut_31, 
        'xǁBgzfReaderǁ__init____mutmut_32': xǁBgzfReaderǁ__init____mutmut_32, 
        'xǁBgzfReaderǁ__init____mutmut_33': xǁBgzfReaderǁ__init____mutmut_33, 
        'xǁBgzfReaderǁ__init____mutmut_34': xǁBgzfReaderǁ__init____mutmut_34, 
        'xǁBgzfReaderǁ__init____mutmut_35': xǁBgzfReaderǁ__init____mutmut_35, 
        'xǁBgzfReaderǁ__init____mutmut_36': xǁBgzfReaderǁ__init____mutmut_36, 
        'xǁBgzfReaderǁ__init____mutmut_37': xǁBgzfReaderǁ__init____mutmut_37, 
        'xǁBgzfReaderǁ__init____mutmut_38': xǁBgzfReaderǁ__init____mutmut_38, 
        'xǁBgzfReaderǁ__init____mutmut_39': xǁBgzfReaderǁ__init____mutmut_39
    }

    def __init__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁ__init____mutmut_mutants"), *args, **kwargs) 

    __init__.__signature__ = _mutmut_signature(xǁBgzfReaderǁ__init____mutmut_orig)
    xǁBgzfReaderǁ__init____mutmut_orig.__name__ = 'xǁBgzfReaderǁ__init__'



    def xǁBgzfReaderǁ_load_block__mutmut_orig(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_1(self, start_offset: int | None = None) -> None:
        if start_offset is not None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_2(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset - self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_3(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = None
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_4(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset != self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_5(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 1
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_6(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = None
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_7(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset not in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_8(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[None]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_9(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = None
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_10(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 1
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_11(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = None
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_12(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = None
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_13(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) > self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_14(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = None
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_15(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is  None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_16(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(None)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_17(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = None
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_18(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(None)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_19(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = None
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_20(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 1
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_21(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = None
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_22(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = "XXXX"
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_23(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = None
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_24(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 1
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_25(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = None
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_26(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = None
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_27(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[None] = self._buffer, block_size

    def xǁBgzfReaderǁ_load_block__mutmut_28(self, start_offset: int | None = None) -> None:
        if start_offset is None:
            # If the file is being read sequentially, then _handle.tell()
            # should be pointing at the start of the next block.
            # However, if seek has been used, we can't assume that.
            start_offset = self._block_start_offset + self._block_raw_length
        if start_offset == self._block_start_offset:  # pragma: no cover
            self._within_block_offset = 0
            return
        elif start_offset in self._buffers:
            # Already in cache
            self._buffer, self._block_raw_length = self._buffers[start_offset]
            self._within_block_offset = 0
            self._block_start_offset = start_offset
            return
        # Must hit the disk... first check cache limits,
        while len(self._buffers) >= self.max_cache:  # pragma: no cover
            # TODO - Implement LRU cache removal?
            self._buffers.popitem()
        # Now load the block
        handle = self._handle
        if start_offset is not None:
            handle.seek(start_offset)
        self._block_start_offset = handle.tell()
        try:
            block_size, self._buffer = _load_bgzf_block(handle)
        except StopIteration:
            # EOF
            block_size = 0
            self._buffer = ""
        self._within_block_offset = 0
        self._block_raw_length = block_size
        # Finally save the block in our cache,
        self._buffers[self._block_start_offset] = None

    xǁBgzfReaderǁ_load_block__mutmut_mutants = {
    'xǁBgzfReaderǁ_load_block__mutmut_1': xǁBgzfReaderǁ_load_block__mutmut_1, 
        'xǁBgzfReaderǁ_load_block__mutmut_2': xǁBgzfReaderǁ_load_block__mutmut_2, 
        'xǁBgzfReaderǁ_load_block__mutmut_3': xǁBgzfReaderǁ_load_block__mutmut_3, 
        'xǁBgzfReaderǁ_load_block__mutmut_4': xǁBgzfReaderǁ_load_block__mutmut_4, 
        'xǁBgzfReaderǁ_load_block__mutmut_5': xǁBgzfReaderǁ_load_block__mutmut_5, 
        'xǁBgzfReaderǁ_load_block__mutmut_6': xǁBgzfReaderǁ_load_block__mutmut_6, 
        'xǁBgzfReaderǁ_load_block__mutmut_7': xǁBgzfReaderǁ_load_block__mutmut_7, 
        'xǁBgzfReaderǁ_load_block__mutmut_8': xǁBgzfReaderǁ_load_block__mutmut_8, 
        'xǁBgzfReaderǁ_load_block__mutmut_9': xǁBgzfReaderǁ_load_block__mutmut_9, 
        'xǁBgzfReaderǁ_load_block__mutmut_10': xǁBgzfReaderǁ_load_block__mutmut_10, 
        'xǁBgzfReaderǁ_load_block__mutmut_11': xǁBgzfReaderǁ_load_block__mutmut_11, 
        'xǁBgzfReaderǁ_load_block__mutmut_12': xǁBgzfReaderǁ_load_block__mutmut_12, 
        'xǁBgzfReaderǁ_load_block__mutmut_13': xǁBgzfReaderǁ_load_block__mutmut_13, 
        'xǁBgzfReaderǁ_load_block__mutmut_14': xǁBgzfReaderǁ_load_block__mutmut_14, 
        'xǁBgzfReaderǁ_load_block__mutmut_15': xǁBgzfReaderǁ_load_block__mutmut_15, 
        'xǁBgzfReaderǁ_load_block__mutmut_16': xǁBgzfReaderǁ_load_block__mutmut_16, 
        'xǁBgzfReaderǁ_load_block__mutmut_17': xǁBgzfReaderǁ_load_block__mutmut_17, 
        'xǁBgzfReaderǁ_load_block__mutmut_18': xǁBgzfReaderǁ_load_block__mutmut_18, 
        'xǁBgzfReaderǁ_load_block__mutmut_19': xǁBgzfReaderǁ_load_block__mutmut_19, 
        'xǁBgzfReaderǁ_load_block__mutmut_20': xǁBgzfReaderǁ_load_block__mutmut_20, 
        'xǁBgzfReaderǁ_load_block__mutmut_21': xǁBgzfReaderǁ_load_block__mutmut_21, 
        'xǁBgzfReaderǁ_load_block__mutmut_22': xǁBgzfReaderǁ_load_block__mutmut_22, 
        'xǁBgzfReaderǁ_load_block__mutmut_23': xǁBgzfReaderǁ_load_block__mutmut_23, 
        'xǁBgzfReaderǁ_load_block__mutmut_24': xǁBgzfReaderǁ_load_block__mutmut_24, 
        'xǁBgzfReaderǁ_load_block__mutmut_25': xǁBgzfReaderǁ_load_block__mutmut_25, 
        'xǁBgzfReaderǁ_load_block__mutmut_26': xǁBgzfReaderǁ_load_block__mutmut_26, 
        'xǁBgzfReaderǁ_load_block__mutmut_27': xǁBgzfReaderǁ_load_block__mutmut_27, 
        'xǁBgzfReaderǁ_load_block__mutmut_28': xǁBgzfReaderǁ_load_block__mutmut_28
    }

    def _load_block(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁ_load_block__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁ_load_block__mutmut_mutants"), *args, **kwargs) 

    _load_block.__signature__ = _mutmut_signature(xǁBgzfReaderǁ_load_block__mutmut_orig)
    xǁBgzfReaderǁ_load_block__mutmut_orig.__name__ = 'xǁBgzfReaderǁ_load_block'



    def xǁBgzfReaderǁtell__mutmut_orig(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_1(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 1 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_2(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 <= self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_3(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset != len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_4(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset or self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_5(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset - self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_6(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) >> 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_7(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 17
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_8(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset >> 16) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_9(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 17) | self._within_block_offset

    def xǁBgzfReaderǁtell__mutmut_10(self):  # pragma: no cover
        """Return a 64-bit unsigned BGZF virtual offset."""
        if 0 < self._within_block_offset and self._within_block_offset == len(self._buffer):
            # Special case where we're right at the end of a (non empty) block.
            # For non-maximal blocks could give two possible virtual offsets,
            # but for a maximal block can't use 65536 as the within block
            # offset. Therefore for consistency, use the next block and a
            # within block offset of zero.
            return (self._block_start_offset + self._block_raw_length) << 16
        else:
            # return make_virtual_offset(self._block_start_offset,
            #                           self._within_block_offset)
            # TODO - Include bounds checking as in make_virtual_offset?
            return (self._block_start_offset << 16) & self._within_block_offset

    xǁBgzfReaderǁtell__mutmut_mutants = {
    'xǁBgzfReaderǁtell__mutmut_1': xǁBgzfReaderǁtell__mutmut_1, 
        'xǁBgzfReaderǁtell__mutmut_2': xǁBgzfReaderǁtell__mutmut_2, 
        'xǁBgzfReaderǁtell__mutmut_3': xǁBgzfReaderǁtell__mutmut_3, 
        'xǁBgzfReaderǁtell__mutmut_4': xǁBgzfReaderǁtell__mutmut_4, 
        'xǁBgzfReaderǁtell__mutmut_5': xǁBgzfReaderǁtell__mutmut_5, 
        'xǁBgzfReaderǁtell__mutmut_6': xǁBgzfReaderǁtell__mutmut_6, 
        'xǁBgzfReaderǁtell__mutmut_7': xǁBgzfReaderǁtell__mutmut_7, 
        'xǁBgzfReaderǁtell__mutmut_8': xǁBgzfReaderǁtell__mutmut_8, 
        'xǁBgzfReaderǁtell__mutmut_9': xǁBgzfReaderǁtell__mutmut_9, 
        'xǁBgzfReaderǁtell__mutmut_10': xǁBgzfReaderǁtell__mutmut_10
    }

    def tell(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁtell__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁtell__mutmut_mutants"), *args, **kwargs) 

    tell.__signature__ = _mutmut_signature(xǁBgzfReaderǁtell__mutmut_orig)
    xǁBgzfReaderǁtell__mutmut_orig.__name__ = 'xǁBgzfReaderǁtell'



    def xǁBgzfReaderǁseek__mutmut_orig(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_1(self, virtual_offset: int, whence: int = 1) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_2(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset << 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_3(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 17
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_4(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = None
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_5(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset & (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_6(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset >> 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_7(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 17)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_8(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = None
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_9(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset == self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_10(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(None)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_11(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset == self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_12(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("XXstart_offset not loaded correctlyXX")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_13(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block >= len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_14(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if  (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_15(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block != 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_16(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 1 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_17(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) != 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_18(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 1):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_19(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 or len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_20(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("XXWithin offset %i but block size only %iXX" % (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_21(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" / (within_block, len(self._buffer)))
        self._within_block_offset = within_block
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    def xǁBgzfReaderǁseek__mutmut_22(self, virtual_offset: int, whence: int = 0) -> int:
        """Seek to a 64-bit unsigned BGZF virtual offset."""
        # Do this inline to avoid a function call,
        # start_offset, within_block = split_virtual_offset(virtual_offset)
        start_offset = virtual_offset >> 16
        within_block = virtual_offset ^ (start_offset << 16)
        if start_offset != self._block_start_offset:
            # Don't need to load the block if already there
            # (this avoids a function call since _load_block would do nothing)
            self._load_block(start_offset)
            if start_offset != self._block_start_offset:  # pragma: no cover
                raise ValueError("start_offset not loaded correctly")
        if within_block > len(self._buffer):
            if not (within_block == 0 and len(self._buffer) == 0):  # pragma: no cover
                raise ValueError("Within offset %i but block size only %i" % (within_block, len(self._buffer)))
        self._within_block_offset = None
        # assert virtual_offset == self.tell(), \
        #    "Did seek to %i (%i, %i), but tell says %i (%i, %i)" \
        #    % (virtual_offset, start_offset, within_block,
        #       self.tell(), self._block_start_offset,
        #       self._within_block_offset)
        return virtual_offset

    xǁBgzfReaderǁseek__mutmut_mutants = {
    'xǁBgzfReaderǁseek__mutmut_1': xǁBgzfReaderǁseek__mutmut_1, 
        'xǁBgzfReaderǁseek__mutmut_2': xǁBgzfReaderǁseek__mutmut_2, 
        'xǁBgzfReaderǁseek__mutmut_3': xǁBgzfReaderǁseek__mutmut_3, 
        'xǁBgzfReaderǁseek__mutmut_4': xǁBgzfReaderǁseek__mutmut_4, 
        'xǁBgzfReaderǁseek__mutmut_5': xǁBgzfReaderǁseek__mutmut_5, 
        'xǁBgzfReaderǁseek__mutmut_6': xǁBgzfReaderǁseek__mutmut_6, 
        'xǁBgzfReaderǁseek__mutmut_7': xǁBgzfReaderǁseek__mutmut_7, 
        'xǁBgzfReaderǁseek__mutmut_8': xǁBgzfReaderǁseek__mutmut_8, 
        'xǁBgzfReaderǁseek__mutmut_9': xǁBgzfReaderǁseek__mutmut_9, 
        'xǁBgzfReaderǁseek__mutmut_10': xǁBgzfReaderǁseek__mutmut_10, 
        'xǁBgzfReaderǁseek__mutmut_11': xǁBgzfReaderǁseek__mutmut_11, 
        'xǁBgzfReaderǁseek__mutmut_12': xǁBgzfReaderǁseek__mutmut_12, 
        'xǁBgzfReaderǁseek__mutmut_13': xǁBgzfReaderǁseek__mutmut_13, 
        'xǁBgzfReaderǁseek__mutmut_14': xǁBgzfReaderǁseek__mutmut_14, 
        'xǁBgzfReaderǁseek__mutmut_15': xǁBgzfReaderǁseek__mutmut_15, 
        'xǁBgzfReaderǁseek__mutmut_16': xǁBgzfReaderǁseek__mutmut_16, 
        'xǁBgzfReaderǁseek__mutmut_17': xǁBgzfReaderǁseek__mutmut_17, 
        'xǁBgzfReaderǁseek__mutmut_18': xǁBgzfReaderǁseek__mutmut_18, 
        'xǁBgzfReaderǁseek__mutmut_19': xǁBgzfReaderǁseek__mutmut_19, 
        'xǁBgzfReaderǁseek__mutmut_20': xǁBgzfReaderǁseek__mutmut_20, 
        'xǁBgzfReaderǁseek__mutmut_21': xǁBgzfReaderǁseek__mutmut_21, 
        'xǁBgzfReaderǁseek__mutmut_22': xǁBgzfReaderǁseek__mutmut_22
    }

    def seek(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁseek__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁseek__mutmut_mutants"), *args, **kwargs) 

    seek.__signature__ = _mutmut_signature(xǁBgzfReaderǁseek__mutmut_orig)
    xǁBgzfReaderǁseek__mutmut_orig.__name__ = 'xǁBgzfReaderǁseek'



    def xǁBgzfReaderǁread__mutmut_orig(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_1(self, size: int = +1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_2(self, size: int = -2) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_3(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size <= 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_4(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 1:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_5(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("XXDon't be greedy, that could be massive!XX")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_6(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = "XXXX"
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_7(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = None
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_8(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size or self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_9(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset - size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_10(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size < len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_11(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset - size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_12(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[None]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_13(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = None
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_14(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset -= size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_15(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset = size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_16(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if  data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_17(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("XXMust be at least 1 byteXX")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_18(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result -= data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_19(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result = data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_20(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[None]
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_21(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = None
                size -= len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_22(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size += len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_23(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size = len(data)
                self._load_block()  # will reset offsets
                result += data

        return result

    def xǁBgzfReaderǁread__mutmut_24(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result -= data

        return result

    def xǁBgzfReaderǁread__mutmut_25(self, size: int = -1) -> str:
        """Read method for the BGZF module."""
        if size < 0:  # pragma: no cover
            raise NotImplementedError("Don't be greedy, that could be massive!")

        result = ""
        while size and self._block_raw_length:
            if self._within_block_offset + size <= len(self._buffer):
                # This may leave us right at the end of a block
                # (lazy loading, don't load the next block unless we have too)
                data = self._buffer[self._within_block_offset : self._within_block_offset + size]
                self._within_block_offset += size
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:  # pragma: no cover
                data = self._buffer[self._within_block_offset :]
                size -= len(data)
                self._load_block()  # will reset offsets
                result = data

        return result

    xǁBgzfReaderǁread__mutmut_mutants = {
    'xǁBgzfReaderǁread__mutmut_1': xǁBgzfReaderǁread__mutmut_1, 
        'xǁBgzfReaderǁread__mutmut_2': xǁBgzfReaderǁread__mutmut_2, 
        'xǁBgzfReaderǁread__mutmut_3': xǁBgzfReaderǁread__mutmut_3, 
        'xǁBgzfReaderǁread__mutmut_4': xǁBgzfReaderǁread__mutmut_4, 
        'xǁBgzfReaderǁread__mutmut_5': xǁBgzfReaderǁread__mutmut_5, 
        'xǁBgzfReaderǁread__mutmut_6': xǁBgzfReaderǁread__mutmut_6, 
        'xǁBgzfReaderǁread__mutmut_7': xǁBgzfReaderǁread__mutmut_7, 
        'xǁBgzfReaderǁread__mutmut_8': xǁBgzfReaderǁread__mutmut_8, 
        'xǁBgzfReaderǁread__mutmut_9': xǁBgzfReaderǁread__mutmut_9, 
        'xǁBgzfReaderǁread__mutmut_10': xǁBgzfReaderǁread__mutmut_10, 
        'xǁBgzfReaderǁread__mutmut_11': xǁBgzfReaderǁread__mutmut_11, 
        'xǁBgzfReaderǁread__mutmut_12': xǁBgzfReaderǁread__mutmut_12, 
        'xǁBgzfReaderǁread__mutmut_13': xǁBgzfReaderǁread__mutmut_13, 
        'xǁBgzfReaderǁread__mutmut_14': xǁBgzfReaderǁread__mutmut_14, 
        'xǁBgzfReaderǁread__mutmut_15': xǁBgzfReaderǁread__mutmut_15, 
        'xǁBgzfReaderǁread__mutmut_16': xǁBgzfReaderǁread__mutmut_16, 
        'xǁBgzfReaderǁread__mutmut_17': xǁBgzfReaderǁread__mutmut_17, 
        'xǁBgzfReaderǁread__mutmut_18': xǁBgzfReaderǁread__mutmut_18, 
        'xǁBgzfReaderǁread__mutmut_19': xǁBgzfReaderǁread__mutmut_19, 
        'xǁBgzfReaderǁread__mutmut_20': xǁBgzfReaderǁread__mutmut_20, 
        'xǁBgzfReaderǁread__mutmut_21': xǁBgzfReaderǁread__mutmut_21, 
        'xǁBgzfReaderǁread__mutmut_22': xǁBgzfReaderǁread__mutmut_22, 
        'xǁBgzfReaderǁread__mutmut_23': xǁBgzfReaderǁread__mutmut_23, 
        'xǁBgzfReaderǁread__mutmut_24': xǁBgzfReaderǁread__mutmut_24, 
        'xǁBgzfReaderǁread__mutmut_25': xǁBgzfReaderǁread__mutmut_25
    }

    def read(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁread__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁread__mutmut_mutants"), *args, **kwargs) 

    read.__signature__ = _mutmut_signature(xǁBgzfReaderǁread__mutmut_orig)
    xǁBgzfReaderǁread__mutmut_orig.__name__ = 'xǁBgzfReaderǁread'



    def xǁBgzfReaderǁreadline__mutmut_orig(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_1(self, size: int = +1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_2(self, size: int = -2) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_3(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = "XXXX"
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_4(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = None
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_5(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = None
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_6(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i != -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_7(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == +1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_8(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -2:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_9(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[None]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_10(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = None
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_11(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result -= data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_12(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result = data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_13(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i - 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_14(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 2 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_15(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 != len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_16(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[None]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_17(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = None
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_18(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if  data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_19(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("XXMust be at least 1 byteXX")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_20(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result -= data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_21(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result = data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_22(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i - 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_23(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 2]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_24(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[None]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_25(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = None
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_26(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i - 1
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_27(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 2
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_28(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = None
                # assert data.endswith(self._newline)
                result += data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_29(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result -= data
                break

        return result

    def xǁBgzfReaderǁreadline__mutmut_30(self, size: int = -1) -> str:
        """Read a single line for the BGZF file."""
        result = ""
        while self._block_raw_length:
            i = self._buffer.find(self._newline, self._within_block_offset)
            # Three cases to consider,
            if i == -1:  # pragma: no cover
                # No newline, need to read in more data
                data = self._buffer[self._within_block_offset :]
                self._load_block()  # will reset offsets
                result += data
            elif i + 1 == len(self._buffer):
                # Found new line, but right at end of block (SPECIAL)
                data = self._buffer[self._within_block_offset :]
                # Must now load the next block to ensure tell() works
                self._load_block()  # will reset offsets
                if not data:  # pragma: no cover
                    raise ValueError("Must be at least 1 byte")
                result += data
                break
            else:
                # Found new line, not at end of block (easy case, no IO)
                data = self._buffer[self._within_block_offset : i + 1]
                self._within_block_offset = i + 1
                # assert data.endswith(self._newline)
                result = data
                break

        return result

    xǁBgzfReaderǁreadline__mutmut_mutants = {
    'xǁBgzfReaderǁreadline__mutmut_1': xǁBgzfReaderǁreadline__mutmut_1, 
        'xǁBgzfReaderǁreadline__mutmut_2': xǁBgzfReaderǁreadline__mutmut_2, 
        'xǁBgzfReaderǁreadline__mutmut_3': xǁBgzfReaderǁreadline__mutmut_3, 
        'xǁBgzfReaderǁreadline__mutmut_4': xǁBgzfReaderǁreadline__mutmut_4, 
        'xǁBgzfReaderǁreadline__mutmut_5': xǁBgzfReaderǁreadline__mutmut_5, 
        'xǁBgzfReaderǁreadline__mutmut_6': xǁBgzfReaderǁreadline__mutmut_6, 
        'xǁBgzfReaderǁreadline__mutmut_7': xǁBgzfReaderǁreadline__mutmut_7, 
        'xǁBgzfReaderǁreadline__mutmut_8': xǁBgzfReaderǁreadline__mutmut_8, 
        'xǁBgzfReaderǁreadline__mutmut_9': xǁBgzfReaderǁreadline__mutmut_9, 
        'xǁBgzfReaderǁreadline__mutmut_10': xǁBgzfReaderǁreadline__mutmut_10, 
        'xǁBgzfReaderǁreadline__mutmut_11': xǁBgzfReaderǁreadline__mutmut_11, 
        'xǁBgzfReaderǁreadline__mutmut_12': xǁBgzfReaderǁreadline__mutmut_12, 
        'xǁBgzfReaderǁreadline__mutmut_13': xǁBgzfReaderǁreadline__mutmut_13, 
        'xǁBgzfReaderǁreadline__mutmut_14': xǁBgzfReaderǁreadline__mutmut_14, 
        'xǁBgzfReaderǁreadline__mutmut_15': xǁBgzfReaderǁreadline__mutmut_15, 
        'xǁBgzfReaderǁreadline__mutmut_16': xǁBgzfReaderǁreadline__mutmut_16, 
        'xǁBgzfReaderǁreadline__mutmut_17': xǁBgzfReaderǁreadline__mutmut_17, 
        'xǁBgzfReaderǁreadline__mutmut_18': xǁBgzfReaderǁreadline__mutmut_18, 
        'xǁBgzfReaderǁreadline__mutmut_19': xǁBgzfReaderǁreadline__mutmut_19, 
        'xǁBgzfReaderǁreadline__mutmut_20': xǁBgzfReaderǁreadline__mutmut_20, 
        'xǁBgzfReaderǁreadline__mutmut_21': xǁBgzfReaderǁreadline__mutmut_21, 
        'xǁBgzfReaderǁreadline__mutmut_22': xǁBgzfReaderǁreadline__mutmut_22, 
        'xǁBgzfReaderǁreadline__mutmut_23': xǁBgzfReaderǁreadline__mutmut_23, 
        'xǁBgzfReaderǁreadline__mutmut_24': xǁBgzfReaderǁreadline__mutmut_24, 
        'xǁBgzfReaderǁreadline__mutmut_25': xǁBgzfReaderǁreadline__mutmut_25, 
        'xǁBgzfReaderǁreadline__mutmut_26': xǁBgzfReaderǁreadline__mutmut_26, 
        'xǁBgzfReaderǁreadline__mutmut_27': xǁBgzfReaderǁreadline__mutmut_27, 
        'xǁBgzfReaderǁreadline__mutmut_28': xǁBgzfReaderǁreadline__mutmut_28, 
        'xǁBgzfReaderǁreadline__mutmut_29': xǁBgzfReaderǁreadline__mutmut_29, 
        'xǁBgzfReaderǁreadline__mutmut_30': xǁBgzfReaderǁreadline__mutmut_30
    }

    def readline(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁreadline__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁreadline__mutmut_mutants"), *args, **kwargs) 

    readline.__signature__ = _mutmut_signature(xǁBgzfReaderǁreadline__mutmut_orig)
    xǁBgzfReaderǁreadline__mutmut_orig.__name__ = 'xǁBgzfReaderǁreadline'



    def xǁBgzfReaderǁ__next____mutmut_orig(self) -> str:
        """Return the next line."""
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def xǁBgzfReaderǁ__next____mutmut_1(self) -> str:
        """Return the next line."""
        line = None
        if not line:
            raise StopIteration
        return line

    def xǁBgzfReaderǁ__next____mutmut_2(self) -> str:
        """Return the next line."""
        line = self.readline()
        if  line:
            raise StopIteration
        return line

    xǁBgzfReaderǁ__next____mutmut_mutants = {
    'xǁBgzfReaderǁ__next____mutmut_1': xǁBgzfReaderǁ__next____mutmut_1, 
        'xǁBgzfReaderǁ__next____mutmut_2': xǁBgzfReaderǁ__next____mutmut_2
    }

    def __next__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁ__next____mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁ__next____mutmut_mutants"), *args, **kwargs) 

    __next__.__signature__ = _mutmut_signature(xǁBgzfReaderǁ__next____mutmut_orig)
    xǁBgzfReaderǁ__next____mutmut_orig.__name__ = 'xǁBgzfReaderǁ__next__'



    def xǁBgzfReaderǁ__iter____mutmut_orig(self) -> "BgzfReader":  # pragma: no cover
        """Iterate over the lines in the BGZF file."""
        return self

    xǁBgzfReaderǁ__iter____mutmut_mutants = {

    }

    def __iter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁ__iter____mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁ__iter____mutmut_mutants"), *args, **kwargs) 

    __iter__.__signature__ = _mutmut_signature(xǁBgzfReaderǁ__iter____mutmut_orig)
    xǁBgzfReaderǁ__iter____mutmut_orig.__name__ = 'xǁBgzfReaderǁ__iter__'



    def xǁBgzfReaderǁclose__mutmut_orig(self) -> None:
        """Close BGZF file."""
        self._handle.close()
        self._buffer = ""
        self._block_start_offset = 0
        self._buffers = {}

    def xǁBgzfReaderǁclose__mutmut_1(self) -> None:
        """Close BGZF file."""
        self._handle.close()
        self._buffer = "XXXX"
        self._block_start_offset = 0
        self._buffers = {}

    def xǁBgzfReaderǁclose__mutmut_2(self) -> None:
        """Close BGZF file."""
        self._handle.close()
        self._buffer = None
        self._block_start_offset = 0
        self._buffers = {}

    def xǁBgzfReaderǁclose__mutmut_3(self) -> None:
        """Close BGZF file."""
        self._handle.close()
        self._buffer = ""
        self._block_start_offset = 1
        self._buffers = {}

    def xǁBgzfReaderǁclose__mutmut_4(self) -> None:
        """Close BGZF file."""
        self._handle.close()
        self._buffer = ""
        self._block_start_offset = None
        self._buffers = {}

    def xǁBgzfReaderǁclose__mutmut_5(self) -> None:
        """Close BGZF file."""
        self._handle.close()
        self._buffer = ""
        self._block_start_offset = 0
        self._buffers = None

    xǁBgzfReaderǁclose__mutmut_mutants = {
    'xǁBgzfReaderǁclose__mutmut_1': xǁBgzfReaderǁclose__mutmut_1, 
        'xǁBgzfReaderǁclose__mutmut_2': xǁBgzfReaderǁclose__mutmut_2, 
        'xǁBgzfReaderǁclose__mutmut_3': xǁBgzfReaderǁclose__mutmut_3, 
        'xǁBgzfReaderǁclose__mutmut_4': xǁBgzfReaderǁclose__mutmut_4, 
        'xǁBgzfReaderǁclose__mutmut_5': xǁBgzfReaderǁclose__mutmut_5
    }

    def close(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁclose__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁclose__mutmut_mutants"), *args, **kwargs) 

    close.__signature__ = _mutmut_signature(xǁBgzfReaderǁclose__mutmut_orig)
    xǁBgzfReaderǁclose__mutmut_orig.__name__ = 'xǁBgzfReaderǁclose'



    def xǁBgzfReaderǁseekable__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return True indicating the BGZF supports random access."""
        return True

    def xǁBgzfReaderǁseekable__mutmut_1(self) -> bool:  # pragma: no cover
        """Return True indicating the BGZF supports random access."""
        return False

    xǁBgzfReaderǁseekable__mutmut_mutants = {
    'xǁBgzfReaderǁseekable__mutmut_1': xǁBgzfReaderǁseekable__mutmut_1
    }

    def seekable(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁseekable__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁseekable__mutmut_mutants"), *args, **kwargs) 

    seekable.__signature__ = _mutmut_signature(xǁBgzfReaderǁseekable__mutmut_orig)
    xǁBgzfReaderǁseekable__mutmut_orig.__name__ = 'xǁBgzfReaderǁseekable'



    def xǁBgzfReaderǁisatty__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return True if connected to a TTY device."""
        return False

    def xǁBgzfReaderǁisatty__mutmut_1(self) -> bool:  # pragma: no cover
        """Return True if connected to a TTY device."""
        return True

    xǁBgzfReaderǁisatty__mutmut_mutants = {
    'xǁBgzfReaderǁisatty__mutmut_1': xǁBgzfReaderǁisatty__mutmut_1
    }

    def isatty(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁisatty__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁisatty__mutmut_mutants"), *args, **kwargs) 

    isatty.__signature__ = _mutmut_signature(xǁBgzfReaderǁisatty__mutmut_orig)
    xǁBgzfReaderǁisatty__mutmut_orig.__name__ = 'xǁBgzfReaderǁisatty'



    def xǁBgzfReaderǁreadable__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return True indicating the BGZF file is readable."""
        return True

    def xǁBgzfReaderǁreadable__mutmut_1(self) -> bool:  # pragma: no cover
        """Return True indicating the BGZF file is readable."""
        return False

    xǁBgzfReaderǁreadable__mutmut_mutants = {
    'xǁBgzfReaderǁreadable__mutmut_1': xǁBgzfReaderǁreadable__mutmut_1
    }

    def readable(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁreadable__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁreadable__mutmut_mutants"), *args, **kwargs) 

    readable.__signature__ = _mutmut_signature(xǁBgzfReaderǁreadable__mutmut_orig)
    xǁBgzfReaderǁreadable__mutmut_orig.__name__ = 'xǁBgzfReaderǁreadable'



    def xǁBgzfReaderǁwritable__mutmut_orig(self) -> bool:  # pragma: no cover
        """Return False indicating the BGZF file is not writable."""
        return False

    def xǁBgzfReaderǁwritable__mutmut_1(self) -> bool:  # pragma: no cover
        """Return False indicating the BGZF file is not writable."""
        return True

    xǁBgzfReaderǁwritable__mutmut_mutants = {
    'xǁBgzfReaderǁwritable__mutmut_1': xǁBgzfReaderǁwritable__mutmut_1
    }

    def writable(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁwritable__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁwritable__mutmut_mutants"), *args, **kwargs) 

    writable.__signature__ = _mutmut_signature(xǁBgzfReaderǁwritable__mutmut_orig)
    xǁBgzfReaderǁwritable__mutmut_orig.__name__ = 'xǁBgzfReaderǁwritable'



    def xǁBgzfReaderǁfileno__mutmut_orig(self) -> int:  # pragma: no cover
        """Return integer file descriptor."""
        return self._handle.fileno()

    xǁBgzfReaderǁfileno__mutmut_mutants = {

    }

    def fileno(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁfileno__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁfileno__mutmut_mutants"), *args, **kwargs) 

    fileno.__signature__ = _mutmut_signature(xǁBgzfReaderǁfileno__mutmut_orig)
    xǁBgzfReaderǁfileno__mutmut_orig.__name__ = 'xǁBgzfReaderǁfileno'



    @property
    def closed(self) -> bool:  # pragma: no cover
        """Return True if the file is closed."""
        return self._handle.closed

    @property
    def mode(self) -> str:  # pragma: no cover
        """Return the file mode."""
        return "r"

    @property
    def name(self) -> str:
        """Return the file name."""
        return getattr(self._handle, "name", "")

    def xǁBgzfReaderǁflush__mutmut_orig(self) -> None:  # pragma: no cover
        """Flush - no-op for read-only file."""
        pass

    xǁBgzfReaderǁflush__mutmut_mutants = {

    }

    def flush(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁflush__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁflush__mutmut_mutants"), *args, **kwargs) 

    flush.__signature__ = _mutmut_signature(xǁBgzfReaderǁflush__mutmut_orig)
    xǁBgzfReaderǁflush__mutmut_orig.__name__ = 'xǁBgzfReaderǁflush'



    def xǁBgzfReaderǁreadlines__mutmut_orig(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint > 0 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_1(self, hint: int = +1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint > 0 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_2(self, hint: int = -2) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint > 0 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_3(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = None
        for line in self:
            lines.append(line)
            if hint > 0 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_4(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(None)
            if hint > 0 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_5(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint >= 0 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_6(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint > 1 and len(lines) >= hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_7(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint > 0 and len(lines) > hint:
                break
        return lines

    def xǁBgzfReaderǁreadlines__mutmut_8(self, hint: int = -1) -> list[str]:
        """Read all lines from the file."""
        lines = []
        for line in self:
            lines.append(line)
            if hint > 0 or len(lines) >= hint:
                break
        return lines

    xǁBgzfReaderǁreadlines__mutmut_mutants = {
    'xǁBgzfReaderǁreadlines__mutmut_1': xǁBgzfReaderǁreadlines__mutmut_1, 
        'xǁBgzfReaderǁreadlines__mutmut_2': xǁBgzfReaderǁreadlines__mutmut_2, 
        'xǁBgzfReaderǁreadlines__mutmut_3': xǁBgzfReaderǁreadlines__mutmut_3, 
        'xǁBgzfReaderǁreadlines__mutmut_4': xǁBgzfReaderǁreadlines__mutmut_4, 
        'xǁBgzfReaderǁreadlines__mutmut_5': xǁBgzfReaderǁreadlines__mutmut_5, 
        'xǁBgzfReaderǁreadlines__mutmut_6': xǁBgzfReaderǁreadlines__mutmut_6, 
        'xǁBgzfReaderǁreadlines__mutmut_7': xǁBgzfReaderǁreadlines__mutmut_7, 
        'xǁBgzfReaderǁreadlines__mutmut_8': xǁBgzfReaderǁreadlines__mutmut_8
    }

    def readlines(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁreadlines__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁreadlines__mutmut_mutants"), *args, **kwargs) 

    readlines.__signature__ = _mutmut_signature(xǁBgzfReaderǁreadlines__mutmut_orig)
    xǁBgzfReaderǁreadlines__mutmut_orig.__name__ = 'xǁBgzfReaderǁreadlines'



    def xǁBgzfReaderǁwritelines__mutmut_orig(self, lines: Iterable[str]) -> None:  # pragma: no cover
        """Write lines - not supported for read-only file."""
        raise OSError("not writable")

    def xǁBgzfReaderǁwritelines__mutmut_1(self, lines: Iterable[str]) -> None:  # pragma: no cover
        """Write lines - not supported for read-only file."""
        raise OSError("XXnot writableXX")

    xǁBgzfReaderǁwritelines__mutmut_mutants = {
    'xǁBgzfReaderǁwritelines__mutmut_1': xǁBgzfReaderǁwritelines__mutmut_1
    }

    def writelines(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁwritelines__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁwritelines__mutmut_mutants"), *args, **kwargs) 

    writelines.__signature__ = _mutmut_signature(xǁBgzfReaderǁwritelines__mutmut_orig)
    xǁBgzfReaderǁwritelines__mutmut_orig.__name__ = 'xǁBgzfReaderǁwritelines'



    def xǁBgzfReaderǁwrite__mutmut_orig(self, s: str) -> int:  # pragma: no cover
        """Write - not supported for read-only file."""
        raise OSError("not writable")

    def xǁBgzfReaderǁwrite__mutmut_1(self, s: str) -> int:  # pragma: no cover
        """Write - not supported for read-only file."""
        raise OSError("XXnot writableXX")

    xǁBgzfReaderǁwrite__mutmut_mutants = {
    'xǁBgzfReaderǁwrite__mutmut_1': xǁBgzfReaderǁwrite__mutmut_1
    }

    def write(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁwrite__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁwrite__mutmut_mutants"), *args, **kwargs) 

    write.__signature__ = _mutmut_signature(xǁBgzfReaderǁwrite__mutmut_orig)
    xǁBgzfReaderǁwrite__mutmut_orig.__name__ = 'xǁBgzfReaderǁwrite'



    def xǁBgzfReaderǁtruncate__mutmut_orig(self, size: int | None = None) -> int:  # pragma: no cover
        """Truncate - not supported for read-only file."""
        raise OSError("not writable")

    def xǁBgzfReaderǁtruncate__mutmut_1(self, size: int | None = None) -> int:  # pragma: no cover
        """Truncate - not supported for read-only file."""
        raise OSError("XXnot writableXX")

    xǁBgzfReaderǁtruncate__mutmut_mutants = {
    'xǁBgzfReaderǁtruncate__mutmut_1': xǁBgzfReaderǁtruncate__mutmut_1
    }

    def truncate(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁtruncate__mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁtruncate__mutmut_mutants"), *args, **kwargs) 

    truncate.__signature__ = _mutmut_signature(xǁBgzfReaderǁtruncate__mutmut_orig)
    xǁBgzfReaderǁtruncate__mutmut_orig.__name__ = 'xǁBgzfReaderǁtruncate'



    def xǁBgzfReaderǁ__enter____mutmut_orig(self):
        """Open a file operable with WITH statement."""
        return self

    xǁBgzfReaderǁ__enter____mutmut_mutants = {

    }

    def __enter__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁ__enter____mutmut_mutants"), *args, **kwargs) 

    __enter__.__signature__ = _mutmut_signature(xǁBgzfReaderǁ__enter____mutmut_orig)
    xǁBgzfReaderǁ__enter____mutmut_orig.__name__ = 'xǁBgzfReaderǁ__enter__'



    def xǁBgzfReaderǁ__exit____mutmut_orig(self, type, value, traceback):
        """Close a file with WITH statement."""
        self.close()

    xǁBgzfReaderǁ__exit____mutmut_mutants = {

    }

    def __exit__(self, *args, **kwargs):
        return _mutmut_trampoline(object.__getattribute__(self, "xǁBgzfReaderǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁBgzfReaderǁ__exit____mutmut_mutants"), *args, **kwargs) 

    __exit__.__signature__ = _mutmut_signature(xǁBgzfReaderǁ__exit____mutmut_orig)
    xǁBgzfReaderǁ__exit____mutmut_orig.__name__ = 'xǁBgzfReaderǁ__exit__'


