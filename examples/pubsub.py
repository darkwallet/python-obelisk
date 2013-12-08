from twisted.internet import reactor

import obelisk

####################################################
# Class to receive pubsub callbacks

class ObeliskPubSubClient(obelisk.ObeliskOfLightClient):
    def on_raw_block(self, height, hash, header, tx_num, tx_hashes):
        print "* block", height, len(tx_hashes)

    def on_raw_transaction(self, hash, transaction):
        print "* tx", hash.encode('hex')


if __name__ == '__main__':
    c = ObeliskPubSubClient('tcp://85.25.198.97:9091', 'tcp://85.25.198.97:9093', 'tcp://85.25.198.97:9094')
    reactor.run()


