import obelisk

secret = "6aa6f40c1ad36825bf7be87226f42a72" \
         "f5ae28e7daa737611c8c971e4d462a18".decode("hex")
key = obelisk.EllipticCurveKey()
key.set_secret(secret)

digest = obelisk.Hash("message")
signature = key.sign(digest)
assert key.verify(digest, signature)

