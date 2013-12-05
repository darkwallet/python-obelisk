import obelisk
import os, sys

from twisted.internet import reactor

####################################################
# Testing Code
height = 0

def print_height(ec, data):
    global height
    print 'height', data
    height = data

def print_blk_header(ec, header):
    print 'version', header.version
    print 'previous block hash', header.previous_block_hash.encode("hex")
    print 'merkle', header.merkle.encode("hex")
    print 'timestamp', header.timestamp
    print 'bits', header.bits
    print 'nonce', header.nonce
    print header

def print_history(ec, history, address):
    global height
    print 'history', address, len(history)
    if not '--full' in sys.argv:
        return
    for row in history:
        o_hash, o_index, o_height, value, s_hash, s_index, s_height = row

        print "+", to_btc(value), age(height - o_height), 'confirms'
        if s_index != MAX_UINT32:
            print "-", to_btc(value), age(height - s_height), 'confirms'

def bootstrap_address(address):
    def print_history_address(ec, history):
        print_history(ec, history, address)

    c.fetch_history(address, print_history_address)
    #c.subscribe_address(addr)

def dummy(*args):
    pass

def poll_latest(client):
    print "poll_latest..."
    def last_height_fetched(ec, height):
        client.fetch_block_header(height, header_fetched)
    def header_fetched(ec, header):
        print "Last:", header
    client.fetch_last_height(last_height_fetched)
    reactor.callLater(20, poll_latest, client)

if __name__ == '__main__':
    c = obelisk.ObeliskOfLightClient('tcp://37.139.11.99:9091')
    #c.fetch_last_height(print_height)
    #blk_hash = "000000000000000471988cc24941335b" \
    #           "91d35d646971b7de682b4236dc691919".decode("hex")
    #assert len(blk_hash) == 32
    #c.fetch_block_header(blk_hash, print_blk_header)
    #c.fetch_block_header(270778, print_blk_header)

    addresses = ['1Evy47MqD82HGx6n1KHkHwBgCwbsbQQT8m', '1GUUpMm899Tr1w5mMvwnXcxbs77fmspTVC']
    if os.path.exists('addresses.txt'):
        f = open('addresses.txt')
        addresses = map(lambda s: s.strip(), f.readlines())
        addresses = filter(lambda s: s, addresses)
        f.close()

    for hash in addresses:
        # Subscribe to an address to receive updates.
        bootstrap_address(hash)
    reactor.callLater(0, poll_latest, c)
    reactor.run()


