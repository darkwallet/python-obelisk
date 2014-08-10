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
    # initialize signing key
    key = obelisk.EllipticCurveKey()
    secret = "59cd7a1d11ef24a1687b7c20bdb9f3bb" \
             "1cb93908401c503f8d69521dbfcd1c6d".decode("hex")
    assert len(secret) == 32
    key.set_secret(secret)
    # sign input 0
    obelisk.sign_transaction_input(tx, 0, key)
    print tx
    print tx.serialize().encode("hex")


def add_input(tx, tx_hash, tx_index):
    input = obelisk.TxIn()
    input.previous_output.hash = tx_hash
    input.previous_output.index = tx_index
    tx.inputs.append(input)


def add_output(tx, address, value):
    output = obelisk.TxOut()
    output.value = int(value * 10**8)
    output.script = obelisk.output_script(address)
    tx.outputs.append(output)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
