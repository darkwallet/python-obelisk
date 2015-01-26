from binary import *
from bitcoin import *
from client import *
from models import *
from transaction import *
from zmqbase import MAX_UINT32
from twisted.internet import reactor

def select_network(network):
    import config
    if "test" in network.lower():
        config.chain = config.testnet_chain
    else:
        config.chain = config.mainnet_chain

def start():
    reactor.run()
def stop():
    reactor.stop()

