import obelisk
import obelisk.config

if __name__ == "__main__":
    
    obelisk.select_network("testnet")
    assert obelisk.config.chain.magic_bytes == obelisk.config.testnet_chain.magic_bytes,\
        "select testnet fail"

    obelisk.select_network("mainnet")
    assert obelisk.config.chain.magic_bytes == obelisk.config.mainnet_chain.magic_bytes,\
        "select mainnet fail"
