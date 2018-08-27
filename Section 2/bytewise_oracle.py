import os
from Crypto.Cipher import AES

class BytewiseOracle:

    def __init__(self):
        self.plaintext = b"This is an secret message."
        self.key = os.urandom(16)
        self.iv = os.urandom(16)
     
    def pkcs7pad(self, s, blksize=16):
      missing = abs(len(s) - (len(s) // blksize + 1) * blksize)
      return s + (chr(missing) * missing)
     
    def encryption_oracle(self, s):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        s = self.pkcs7pad(bytes(s) + self.plaintext, 16)
        return cipher.encrypt(s)
