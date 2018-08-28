import os
import hashlib

# this is only for illustrative purposes
truncated_num_bytes = 5


class TruncatedSHA1:

    def __init__(self, s):
        self.string = s
        self.hashfunction = hashlib.sha1(s)

    def digest(self):
        return self.hashfunction.digest()[:truncated_num_bytes]


if __name__ == '__main__':
    # create a lookup table
    lookup = {}

    # generate the collison table with 2^20 entries
    for i in xrange(2**(truncated_num_bytes * 8 / 2)):
        # geneate random messages
        msg = os.urandom(12)
        lookup[TruncatedSHA1(msg).digest()] = msg

    # compare against the collision table
    for i in xrange(2**(truncated_num_bytes * 8 / 2)):
        # geneate random messages
        msg = os.urandom(12)
        # collision, we print it
        if TruncatedSHA1(msg).digest() in lookup:
            hmsg1 = msg.encode("hex")
            hmsg2 = lookup[TruncatedSHA1(msg).digest()].encode("hex")
            print "Strings (hex) {} and {} collide".format(hmsg1, hmsg2)
