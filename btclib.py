import bitcoin
from bitcoin import ElectrumSequence


def to_addr(hash):
    return bitcoin.hash_160_to_bc_address(hash)

def to_hash160(hash):
    return bitcoin.bc_address_to_hash_160(hash)[1]


class Wallet(object):
    def __init__(self, mpk):
        self.seq = ElectrumSequence(mpk)
        self.mpk = mpk

    def get_address(self, idx):
        return self.seq.get_address((0,idx))

if __name__ == '__main__':
    mpk = "9b698964276caedf1626efe6e7da9b586a7c1847128b8d461d47c0b35f4f8ac5a97788d99d6a801e66d4b2beb0582e0071d999bee36ff70a0b803ec603f76ecb"
    w = Wallet(mpk)
    for idx in xrange(100):
        print w.get_address(idx)

