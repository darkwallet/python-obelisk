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
    prevout_address = "1JdbgyywETKEssy4jqFcKiZBmn7oxVKxcT"
    script_code = output_script(prevout_address)
    sighash = generate_signature_hash(tx, 0, script_code)
    print sighash.encode("hex")
    key = obelisk.EllipticCurveKey()
    secret = "59cd7a1d11ef24a1687b7c20bdb9f3bb" \
             "1cb93908401c503f8d69521dbfcd1c6d".decode("hex")
    assert len(secret) == 32
    key.set_secret(secret)
    # The public key and sighash are correct
    signature = key.sign(sighash) + "\x01"
    public_key = key.public_key
    script = obelisk.op_push(len(signature)).decode("hex")
    script += signature
    script += obelisk.op_push(len(public_key)).decode("hex")
    script += public_key
    tx.inputs[0].script = script
    print tx
    print tx.serialize().encode("hex")

def add_input(tx, tx_hash, tx_index):
    input = obelisk.TxIn()
    input.previous_output.hash = tx_hash
    input.previous_output.index = tx_index
    tx.inputs.append(input)

def output_script(address):
    addrtype, hash_160 = obelisk.bc_address_to_hash_160(address)
    assert addrtype == 0
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

#------------------

def copy_tx(tx):
    # This is a hack.
    raw_tx = tx.serialize()
    return obelisk.Transaction.deserialize(raw_tx)

def generate_signature_hash(parent_tx, input_index, script_code):
    tx = copy_tx(parent_tx)
    if input_index >= len(tx.inputs):
        return None
    for input in tx.inputs:
        input.script = ""
    tx.inputs[input_index].script = script_code
    raw_tx = tx.serialize() + "\x01\x00\x00\x00"
    print "encoded:", raw_tx.encode("hex")
    return obelisk.Hash(raw_tx)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

