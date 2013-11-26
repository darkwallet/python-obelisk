import bitcoin

def test_bip32(seed, sequence):
    """
    run a test vector,
    see https://en.bitcoin.it/wiki/BIP_0032_TestVectors
    """

    wallet = bitcoin.HighDefWallet.root(seed)
        
    print "secret key", wallet.secret.encode('hex')
    print "chain code", wallet.chain.encode('hex')

    print "keyid", wallet.key_id.encode("hex")
    print "base58"
    print "address", wallet.address
    print "secret key", wallet.secret_key

    s = ['m']
    for n in sequence.split('/'):
        s.append(n)
        print "Chain [%s]" % '/'.join(s)
        
        if n[-1] == "'":
            n = int(n[:-1])
            wallet = wallet.branch_prime(n)
        else:
            n = int(n)
            wallet = wallet.branch(n)


        print "* Identifier"
        print "  * (main addr)", wallet.address

        print "* Secret Key"
        print "  * (hex)", wallet.secret.encode("hex")
        print "  * (wif)", wallet.secret_key

        print "* Chain Code"
        print "   * (hex)", wallet.chain.encode("hex")
    print "----"

        


if __name__ == '__main__':
    test_bip32("000102030405060708090a0b0c0d0e0f", "0'/1/2'/2/1000000000")
    test_bip32("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542","0/2147483647'/1/2147483646'/2")

