from py_ecc.bls.ciphersuites import G2ProofOfPossession as bls_pop

private_key1 = 5566

public_key = bls_pop.SkToPk(private_key1)

message = b'abc' * 32  # The message to be signed

# Signing
signature = bls_pop.Sign(private_key1, message)
print(signature)
# Verifying
out = bls_pop.Verify(public_key, message, signature)
print(out)