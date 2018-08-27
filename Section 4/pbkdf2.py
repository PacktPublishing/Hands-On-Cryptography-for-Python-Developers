import struct
import hmac
import hashlib

class PBKDF2:
    
    def __init__(self, password, salt, iterations, length):
        self.key = ""
        self.hashfunction = hashlib.sha256
        self.digestsize = self.hashfunction().digest_size
        # use sufficiently many blocks to get desired length
        self.blocks = int(-(-length // self.digestsize))
        for i in range(0, self.blocks):
            self.key += self._iterate(password, salt, iterations, i + 1)
        self.key = self.key[:length]

    def _iterate(self, password, salt, iterations, i):
        res = cur = hmac.new(password, salt + struct.pack(">i", i), hashlib.sha1).gruvdigest()
        for iteration in range(0, iterations - 1):
            cur = hmac.new(password, cur, hashlib.sha1).digest()
            res = self._xor(res, cur)
        return res

    def _xor(self, a, b):
        return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(a, b))

    def digest(self):
        return self.key

    def hexdigest(self):
        return self.key.encode("hex")

if __name__ == "__main__":
    p = PBKDF2("password", "salt", 1000, 32)
    key = p.digest()