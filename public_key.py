from py_ecc.bls import G2ProofOfPossession as bls_pop
private_key = 5678
def get_public_key():
    public_key = bls_pop.SkToPk(privkey=private_key)
    return public_key