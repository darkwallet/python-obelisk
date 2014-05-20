def hex2(n):
    x = '%x' % (n,)
    return ('0' * (len(x) % 2)) + x

class Bitset:

    def __init__(self, size=0, value=0, binary=None):
        self._size = size
        self._value = value
        if binary is not None:
            self._size = len(binary)
            self._value = int(binary, 2)

    def deserialize(self, data):
        self._value = int(data[::-1].encode("hex"), 16)

    def serialize(self):
        return hex2(self._value).decode("hex")[::-1]

    @property
    def size(self):
        return self._size

    def __str__(self):
        # TODO: use format instead
        self_str = bin(self._value)[2:]
        if len(self_str) <= self._size:
            # Pad with zeros
            self_str = "0" * (self._size - len(self_str)) + self_str
            assert len(self_str) == self._size
        else:
            self_str = self_str[-self._size:]
        return self_str

    def __repr__(self):
        return "Bitset(%s)" % str(self)

if __name__ == "__main__":
    b = Bitset(binary="001101110001010101111010101010011101")
    assert b.serialize().encode("hex") == "9daa577103"
    assert b.size == 36
    assert str(b) == "001101110001010101111010101010011101"
    b = Bitset(36)
    b.deserialize("9daa577103".decode("hex"))
    assert b.size == 36
    assert str(b) == "001101110001010101111010101010011101"
    b = Bitset(8)
    b.deserialize("9daa577103".decode("hex"))
    assert b.size == 8
    assert str(b) == "10011101"

