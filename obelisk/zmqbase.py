import sys
import random
from hashlib import sha256
import struct
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
from decimal import Decimal
from threading import enumerate

import zmqproto
from zmqproto import ZmqSocket
SNDMORE = 1

btc = Decimal('1'+'0'*8)
MAX_UINT32 = 4294967295

def to_btc(value):
    return Decimal(value)/btc

def age(blocks):
    return blocks/(7*24)

def checksum(value):
    return sha256(sha256(value).digest()).digest()[0:4]

class ClientBase(object):
    valid_messages = []
    def __init__(self, address):
        self._messages = []
        self.running = 1
        self._socket = self.setup(address)
        self._subscriptions = {}

    # Message arrived
    def on_raw_message(self, id, cmd, data):
        res = None
        short_cmd = cmd.split('.')[-1]
        if short_cmd in self.valid_messages:
            res = getattr(self, '_on_'+short_cmd)(data)
        else:
            print "Unknown Message", cmd
        if res:
            self.trigger_callbacks(id, *res)

    # Base Api
    def send_command(self, command, data='', cb=None):
        tx_id = random.randint(0, MAX_UINT32)

        self.send('', SNDMORE)      # destination
        self.send(command, SNDMORE) # command
        self.send(struct.pack('I', tx_id), SNDMORE) # id (random)
        self.send(data, SNDMORE)    # data

        self.send(checksum(data), 0)    # checksum
        if cb:
            self._subscriptions[tx_id] = cb
        return tx_id

    def trigger_callbacks(self, tx_id, *args):
        if tx_id in self._subscriptions:
            self._subscriptions[tx_id](*args)
            del self._subscriptions[tx_id]

    # Low level zmq abstraction into obelisk frames
    def send(self, *args):
        self._socket.send(*args)

    def frame_received(self, frame, more):
        self._messages.append(frame)
        if not more:
            if not len(self._messages) == 5:
                print "Sequence with wrong messages", len(self._messages)
                self._messages = []
                return
            uuid, command, id, data, chksum = self._messages
            self._messages = []
            if checksum(data) == chksum:
                id = struct.unpack('I', id)[0]
                self.on_raw_message(id, command, data)
            else:
                print "bad checksum"

    def setup(self, address):
        s = ZmqSocket(self.frame_received)
        s.connect(address)
        return s

    # Low level packing
    def get_error(data):
        return struct.unpack_from('<I', data, 0)[0]

    def unpack_table(self, row_fmt, data, start=0):
        # get the number of rows
        row_size = struct.calcsize(row_fmt)
        nrows = (len(data)-start)/row_size

        # unpack
        rows = []
        for idx in xrange(nrows):
            offset = start+(idx*row_size)
            row = struct.unpack_from(row_fmt, data, offset)
            rows.append(row)
        return rows


