import obelisk

from twisted.internet import reactor

####################################################
# Testing Code

def print_event(*args):
    print args

if __name__ == '__main__':
    c = obelisk.ObeliskOfLightClient('tcp://85.25.198.97:8081')
    c.subscribe_address("1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp", print_event)

    reactor.run()


