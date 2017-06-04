# Copyright (c) 2017 Diane Reynolds
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Test implementation for p2pk addresses using Bech32."""

import binascii
import segwit_addr

def hextobytes(h):
    d = binascii.unhexlify(h)
    r = []
    for c in d:
        r = r + [ord(c)]
    return r

def bytestohex(bl):
    d = b''
    for b in bl:
        d = d + chr(b)
    return binascii.hexlify(d)

def pk_encode(k):
    pk8 = hextobytes(k)
    pk5 = segwit_addr.convertbits(pk8,8,5)
    a = segwit_addr.bech32_encode('pk',pk5)
    return a

def pk_decode(a):
    (hrp, pk5) = segwit_addr.bech32_decode(a)
    if hrp != 'pk':
        return None
    pk8 = segwit_addr.convertbits(pk5,5,8)
    if len(pk8) < 33:
        return None
    if len(pk8) > 33:
        for b in pk8[33:]:
            if b > 0:
                return None
        pk8 = pk8[0:33]
    return bytestohex(pk8)
