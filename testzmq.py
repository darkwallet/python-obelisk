import os, sys
import struct
import time
from decimal import Decimal

from twisted.internet import reactor

from zmqbase import to_btc, btc, age
from zmqbase import ClientBase, checksum, MAX_UINT32

from btclib import to_hash160, to_addr, BlockHeader

def unpack_error(data):
    return struct.unpack_from('<I', data, 0)[0]

class ObeliskOfLightClient(ClientBase):
    valid_messages = ['fetch_block_header', 'fetch_history', 'subscribe', 'fetch_last_height', 'update', 'renew']
    subscribed = 0
    # Command implementations
    def renew_address(self, address):
        # prepare parameters
        data = struct.pack('B', 0)            # address version
        data += address[::-1]   # address
        #data += struct.pack('<I', 0)          # from_height

        # run command
        self.send_command('address.renew', data)
        # renew triggered again on response
        reactor.callLater(120, self.renew_address, address)

    def subscribe_address(self, address):
        # prepare parameters
        data = struct.pack('B', 0)            # address version
        data += address[::-1]   # address
        #data += struct.pack('<I', 0)          # from_height

        # run command
        self.send_command('address.subscribe', data)
        reactor.callLater(120, self.renew_address, address)

    def fetch_block_header(self, blk_hash, cb):
        data = blk_hash[::-1]
        self.send_command('blockchain.fetch_block_header', data, cb)

    def fetch_history(self, address, cb):
        # prepare parameters
        data = struct.pack('B', 0)            # address version
        data += address[::-1]   # address
        data += struct.pack('<I', 0)          # from_height

        # run command
        self.send_command('address.fetch_history', data, cb)

    def fetch_last_height(self, cb):
        self.send_command('blockchain.fetch_last_height', cb=cb)

    # receive handlers
    def on_fetch_block_header(self, data):
        error = unpack_error(data)
        assert len(data[4:]) == 80
        header = BlockHeader.deserialize(data[4:])
        return (header,)

    def on_fetch_history(self, data):
        error = unpack_error(data)
        # parse results
        rows = self.unpack_table("<32sIIQ32sII", data, 4)

        # sum the row values
        total = reduce(lambda a, b: a+to_btc(b[3]), rows, Decimal())

        return (rows, total)

    def on_fetch_last_height(self, data):
        error, height = struct.unpack('<II', data)
        return (height,)
        
    def on_subscribe(self, data):
        self.subscribed += 1
        error = unpack_error(data)
        if error:
            print "Error subscribing"
        if not self.subscribed%1000:
            print "Subscribed ok", self.subscribed

    def on_update(self, data):
        print "Update for address"

    def on_renew(self, data):
        self.subscribed += 1
        error = unpack_error(data)
        if error:
            print "Error subscribing"
        if not self.subscribed%1000:
            print "Renew ok", self.subscribed


####################################################
# Testing Code
height = 0

def print_height(data):
    global height
    print 'height', data
    height = data

def print_blk_header(header):
    print 'version', header.version
    print 'previous block hash', header.previous_block_hash.encode("hex")
    print 'merkle', header.merkle.encode("hex")
    print 'timestamp', header.timestamp
    print 'bits', header.bits
    print 'nonce', header.nonce
    print header

def print_history(address, history, total):
    global height
    if total == 0:
        return
    print 'history', address, len(history), total
    if not '--full' in sys.argv:
        return
    for row in history:
        o_hash, o_index, o_height, value, s_hash, s_index, s_height = row

        print "+", to_btc(value), age(height-o_height), 'days'
        if s_index == MAX_UINT32:
            total += value
        else:
            print "-", to_btc(value), age(height-s_height), 'days'

def bootstrap_address(hash):
    def print_history_address(history, total):
        print_history(hash, history, total)

    addr = to_hash160(hash)
    #print len(addr)
    c.fetch_history(addr, print_history_address)
    c.subscribe_address(addr)

def dummy(*args):
    pass

if __name__ == '__main__':
    c = ObeliskOfLightClient('tcp://37.139.11.99:9091')
    c.fetch_last_height(print_height)
    blk_hash = "000000000000000471988cc24941335b" \
               "91d35d646971b7de682b4236dc691919".decode("hex")
    assert len(blk_hash) == 32
    c.fetch_block_header(blk_hash, print_blk_header)

    addresses = ['1Evy47MqD82HGx6n1KHkHwBgCwbsbQQT8m', '1GUUpMm899Tr1w5mMvwnXcxbs77fmspTVC']
    if os.path.exists('addresses.txt'):
        f = open('addresses.txt')
        addresses = map(lambda s: s.strip(), f.readlines())
        addresses = filter(lambda s: s, addresses)
        f.close()

    for hash in addresses:
        bootstrap_address(hash)
    reactor.run()

