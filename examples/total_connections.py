import obelisk
from twisted.internet import reactor

def height_fetched(ec, height):
    print "Height:", height

def connections_fetched(ec, height):
    print "Total connections:", height

if __name__ == '__main__':
    client = obelisk.ObeliskOfLightClient("tcp://localhost:9091")
    client.fetch_last_height(height_fetched)
    client.total_connections(connections_fetched)
    reactor.run()

