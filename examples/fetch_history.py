import obelisk
import sys
from twisted.internet import reactor

def main(address):
    c = obelisk.ObeliskOfLightClient("tcp://localhost:9091")

    def history_fetched(ec, history):
        if ec:
            print ec
        else:
            for id, hash, index, height, value in history:
                if id == obelisk.PointIdent.Output:
                    type = "Output"
                    #print "  checksum =", obelisk.spend_checksum(hash, index)
                else: # == obelisk.PointIdent.Spend
                    type = "Spend "
                print type, hash.encode("hex") + ":" + str(index), height, value
        reactor.stop()

    c.fetch_history2(address, history_fetched)

    reactor.run()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Need ADDRESS argument."
    else:
        main(sys.argv[1])

