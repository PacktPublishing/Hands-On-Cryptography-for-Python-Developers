import os
import hashlib


class TruncatedSHA1:

    def __init__(self, s):
        self.string = s
        self.hashfunction = hashlib.sha1(s)

    def digest(self):
        return self.hashfunction.digest()[:5]


if __name__ == '__main__':
    lookup = {}
    print "Generating table..."
    for i in xrange(2**(20)):
        msg = os.urandom(12)
        lookup[TruncatedSHA1(msg).digest()] = msg
    print "Generating collisions..."
    for i in xrange(2**(20)):
        msg = os.urandom(12)
        if TruncatedSHA1(msg).digest() in lookup:
            print "Strings (hex) {} and {} collide".format(msg.encode("hex"), lookup[TruncatedSHA1(msg).digest()].encode("hex"))
