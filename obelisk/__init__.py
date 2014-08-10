from bitcoin import *
from client import *
from models import *
from transaction import *
from zmqbase import MAX_UINT32


def select_network(network):
    import config
    if "test" in network.lower():
        config.chain = config.testnet_chain
    else:
        config.chain = config.mainnet_chain
