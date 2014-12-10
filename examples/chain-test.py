import obelisk
from twisted.internet import reactor


def tx_fetched(ec, tx):
    print "Tx:", ec, tx.encode("hex")


def spend_fetched(ec, spend):
    print "Spend:", ec, spend


def txidx_fetched(ec, height, index):
    print "Tx index:", ec, height, index


def txhashes_fetched(ec, hashes):
    print "Tx hashes:", [h.encode("hex") for h in hashes]


def height_fetched(ec, height):
    print "Height:", height

def history_fetched(ec, history):
    print "History:"
    for id, hash, index, height, value in history:
        print id, hash.encode("hex") + ":" + str(index), height, value

def stealth_fetched(ec, result):
    print "Stealth:"
    for ephemkey, address, tx_hash in result:
        print "  ephemkey:", ephemkey.encode("hex"), \
            "address:", address.encode("hex"), \
            "tx_hash:", tx_hash.encode("hex")


if __name__ == '__main__':
    client = obelisk.ObeliskOfLightClient("tcp://localhost:9091")
    tx_hash = "e9a66845e05d5abc0ad04ec80f774a7e" \
              "585c6e8db975962d069a522137b80c1d".decode("hex")
    client.fetch_transaction(tx_hash, tx_fetched)
    outpoint = obelisk.OutPoint()
    outpoint.hash = "f4515fed3dc4a19b90a317b9840c243b" \
                    "ac26114cf637522373a7d486b372600b".decode("hex")
    outpoint.index = 0
    client.fetch_spend(outpoint, spend_fetched)
    client.fetch_transaction_index(outpoint.hash, txidx_fetched)
    client.fetch_block_transaction_hashes(tx_hash, txhashes_fetched)
    blk_hash = "000000000003ba27aa200b1cecaad478" \
               "d2b00432346c3f1f3986da1afd33e506".decode("hex")
    client.fetch_block_height(blk_hash, height_fetched)
    client.fetch_last_height(height_fetched)
    client.fetch_history("13cbkpKW2DdhEUmeGC2h9HyxbBdtc7Wcth", history_fetched)
    # You can compare with blockchain db using libbitcoin-blockchain/tools/
    #  $ stealth_db scan stealth_index stealth_rows 101010101 0
    client.fetch_stealth("101010101", stealth_fetched)
    reactor.run()

