import sys
import struct
import json
import binascii
import pk_addr

def jsonfrom():
    return json.loads(sys.argv[len(sys.argv) - 2])

def jsonto():
    return json.loads(sys.argv[len(sys.argv) - 1])

def createtx(frm,to):
    if len(frm) >= 253:
        raise ValueError("too many inputs; varint not implemented")
    if len(to) >= 253:
        raise ValueError("too many inputs; varint not implemented")
    tx = binascii.unhexlify('01000000')
    tx = tx + chr(len(frm))
    for txi in frm:
        txid = pk_addr.hextobytes(txi[u'txid'])
        vout = txi[u'vout']
        try:
            seqno = txi[u'sequence']
        except:
            seqno = 1
        list.reverse(txid)
        for idb in txid:
            tx = tx + chr(idb)
        tx = tx + struct.pack('<I',vout)
        tx = tx + chr(0)
        tx = tx + struct.pack('<i',seqno)
    tx = tx + chr(len(to))
    for txo in to.iteritems():
        (a,v) = txo
        pk = pk_addr.pk_decode(a)
        if pk == None:
            raise ValueError("Could not decode pubkey from pk address")
        if len(pk) != 66:
            raise ValueError("pk not 33 bytes")
        v = int(100000000 * v)
        tx = tx + struct.pack('<Q',v)
        tx = tx + chr(35)
        tx = tx + chr(33)
        tx = tx + binascii.unhexlify(pk)
        tx = tx + chr(0xac)
    tx = tx + binascii.unhexlify('00000000')
    print binascii.hexlify(tx)

createtx(jsonfrom(),jsonto())
