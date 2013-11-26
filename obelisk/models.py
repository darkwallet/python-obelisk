import bitcoin
import struct

class BlockHeader:

    def __init__(self):
        self.height = None

    @classmethod
    def deserialize(cls, raw):
        assert len(raw) == 80
        self = cls()
        self.version = struct.unpack('<I', raw[:4])[0]
        self.previous_block_hash = raw[4:36][::-1]
        assert len(self.previous_block_hash) == 32
        self.merkle = raw[36:68][::-1]
        assert len(self.merkle) == 32
        self.timestamp, self.bits, self.nonce = struct.unpack('<III', raw[68:])
        return self

    @property
    def hash(self):
        data = struct.pack('<I', self.version)
        data += self.previous_block_hash[::-1]
        data += self.merkle[::-1]
        data += struct.pack('<III', self.timestamp, self.bits, self.nonce)
        return bitcoin.Hash(data)[::-1]

    def __repr__(self):
        return '<BlockHeader %s>' % (self.hash.encode("hex"),)

