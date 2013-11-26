import struct
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
        data = struct.pack('B', 0)          # address version
        data += address[::-1]               # address

        # run command
        self.send_command('address.renew', data)
        # renew triggered again on response
        reactor.callLater(120, self.renew_address, address)

    def subscribe_address(self, address):
        # prepare parameters
        data = struct.pack('B', 0)          # address version
        data += address[::-1]               # address

        # run command
        self.send_command('address.subscribe', data)
        reactor.callLater(120, self.renew_address, address)

    def fetch_block_header(self, index, cb):
        if type(index) == str:
            data = index[::-1]
        elif type(index) == int:
            data = struct.pack('<I', index)
        else:
            raise ValueError("Unknown index type")
        self.send_command('blockchain.fetch_block_header', data, cb)

    def fetch_history(self, address, cb):
        # prepare parameters
        data = struct.pack('B', 0)          # address version
        data += address[::-1]               # address
        data += struct.pack('<I', 0)        # from_height

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

