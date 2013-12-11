import obelisk

from twisted.internet import reactor

####################################################
# Testing Code

def print_event(address_version, address_hash, height, block_hash, tx):
    address = obelisk.bitcoin.hash_160_to_bc_address(address_hash, address_version)
    print "update for", address, height

if __name__ == '__main__':
    c = obelisk.ObeliskOfLightClient('tcp://85.25.198.97:8081')
    c.subscribe_address("1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp", print_event)

    reactor.run()


