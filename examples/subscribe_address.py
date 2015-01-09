import obelisk

from twisted.internet import reactor

####################################################
# Testing Code


def print_event(address_version, address_hash, height, block_hash, tx):
    address = obelisk.bitcoin.hash_160_to_bc_address(
        address_hash, address_version
    )
    print "update for", address, height

if __name__ == '__main__':
    c = obelisk.ObeliskOfLightClient('tcp://localhost:9091')
    c.subscribe_address("1LuckyY9fRzcJre7aou7ZhWVXktxjjBb9S", print_event)

    reactor.run()
