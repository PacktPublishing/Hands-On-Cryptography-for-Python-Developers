from bytewise_oracle import BytewiseOracle

bo = BytewiseOracle()

def attack(blocksize, known):
    index = len(known) / blocksize
    prefix = "a"*(blocksize-len(known)%blocksize-1)
    lookup = {}    
    for char in range(0, 256): 
        lookup[bo.encryption_oracle(prefix+known+chr(char))[index*16:index*16+16]] = chr(char)
    substring = bo.encryption_oracle(prefix)[16*index:16*index+16]
    if lookup.has_key(substring):
        return lookup[substring]
    else:
        return None

plain = ""
while attack(16, plain) != None:
    plain += attack(16, plain)
print "Found plaintext:\n", plain