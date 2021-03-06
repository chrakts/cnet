"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class cnet_constants_t(object):
    __slots__ = []

    answerTrue = 0
    timeout = 1
    answerFalse = 2
    crcError = 3
    answerWrong = 4

    def __init__(self):
        pass

    def encode(self):
        buf = BytesIO()
        buf.write(cnet_constants_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        pass

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != cnet_constants_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return cnet_constants_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = cnet_constants_t()
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if cnet_constants_t in parents: return 0
        tmphash = (0x12345678) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if cnet_constants_t._packed_fingerprint is None:
            cnet_constants_t._packed_fingerprint = struct.pack(">Q", cnet_constants_t._get_hash_recursive([]))
        return cnet_constants_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

