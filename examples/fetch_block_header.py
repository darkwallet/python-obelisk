import obelisk
import os, sys

from twisted.internet import reactor

from obelisk.util import to_btc
from obelisk import MAX_UINT32

if __name__ == '__main__':
    c = obelisk.ObeliskOfLightClient("tcp://obelisk.unsystem.net:9091")
    h = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    def cb(*args):
        ec, result = args
        print result.encode("hex")
        reactor.stop()
    c.fetch_block_header(h.decode("hex"), cb)

    reactor.run()
