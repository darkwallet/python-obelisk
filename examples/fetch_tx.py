import obelisk
import sys
from twisted.internet import reactor

def main(txhash):
    c = obelisk.ObeliskOfLightClient("tcp://localhost:9091")
    txhash = txhash.decode("hex")

    def cb_txpool(ec, result):
        if ec:
            c.fetch_transaction(txhash, cb_chain)
        else:
            print "From Txpool:"
            print result.encode("hex")
            reactor.stop()

    def cb_chain(ec, result):
        if ec:
            print ec
        else:
            print "From Blockchain:"
            print result.encode("hex")
        reactor.stop()

    c.fetch_txpool_transaction(txhash, cb_txpool)

    reactor.run()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Need TXHASH argument."
    else:
        main(sys.argv[1])

