import sys
import obelisk
from decimal import Decimal as D

def main(argv):
    tx = obelisk.Transaction()
    for switch, param in zip(argv[1::2], argv[2::2]):
        if switch == "-i":
            tx_hash, tx_index = param.split(":")
            tx_hash = tx_hash.decode("hex")
            tx_index = int(tx_index)
            add_input(tx, tx_hash, tx_index)
        elif switch == "-o":
            address, value = param.split(":")
            value = D(value)
            add_output(tx, address, value)
    print tx

def add_input(tx, tx_hash, tx_index):
    input = obelisk.TxIn()
    input.previous_output.hash = tx_hash
    input.previous_output.index = tx_index
    tx.inputs.append(input)

def output_script(address):
    addrtype, hash_160 = obelisk.bc_address_to_hash_160(address)
    script = '\x76\xa9'                 # op_dup, op_hash_160
    script += '\x14'                    # push 0x14 bytes
    script += hash_160
    script += '\x88\xac'                # op_equalverify, op_checksig
    return script

def add_output(tx, address, value):
    output = obelisk.TxOut()
    output.value = int(value * 10**8)
    output.script = output_script(address)
    tx.outputs.append(output)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

