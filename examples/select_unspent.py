import obelisk
import sys
from twisted.internet import reactor

def build_output_info_list(unspent_rows):
    unspent_infos = []
    for row in unspent_rows:
        assert len(row) == 4
        outpoint = obelisk.OutPoint()
        outpoint.hash = row[0]
        outpoint.index = row[1]
        value = row[3]
        unspent_infos.append(
            obelisk.OutputInfo(outpoint, value))
    return unspent_infos

def history_fetched(ec, history):
    if ec is not None:
        print >> sys.stderr, "Error fetching history:", ec
        return
    unspent_rows = [row[:4] for row in history if row[4] is None]
    unspent = build_output_info_list(unspent_rows)
    print obelisk.select_outputs(unspent, 10000)

if __name__ == '__main__':
    client = obelisk.ObeliskOfLightClient("tcp://85.25.198.97:9091")
    client.fetch_history("1PRBVdCHoPPD3bz8sCZRTm6iAtuoqFctvx", history_fetched)
    reactor.run()

