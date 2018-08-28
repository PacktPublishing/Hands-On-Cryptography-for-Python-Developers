import json
import base64
import os
from shamir import *


class KeySplitter:

    def __init__(self):
        self.splitter = Shamir()

    def split(self, numshares, threshold, key):
        xshares = [''] * numshares
        yshares = [''] * numshares

        # For each symbol in the key split into shares over GF(2^8)
        for char in key:
            xcords, ycords = self.splitter.split(
                numshares, threshold, ord(char))

            for idx in range(numshares):
                xshares[idx] += chr(xcords[idx])
                yshares[idx] += chr(ycords[idx])
        return zip(xshares, yshares)

    def unsplit(self, shares):
        recovered = ''

        # For each sub share (corresponding to symbol in key)...
        for idx in range(len(shares[0][0])):
            xcords = []
            ycords = []
            
            # Compute the secret value
            for xcord, ycord in shares:
                xcords += [ord(xcord[idx])]
                ycords += [ord(ycord[idx])]
            recovered += chr(self.splitter.unsplit(xcords, ycords, 0))
        return recovered

    def jsonify(self, shares, threshold, split):
        data = {
            'shares': shares,
            'threshold': threshold,
            'split': [
                base64.b64encode(split[0]),
                base64.b64encode(split[1])
            ]
        }
        return json.dumps(data)

if __name__ == "__main__":
    shares = 30
    threshold = 20
    print('Running test instances (30, 20) with 100 independent keys...')
    for i in range(100):
        secret_key = os.urandom(64)
        splitter = KeySplitter()
        splits = splitter.split(shares, threshold, secret_key)
        assert(splitter.unsplit(splits) == secret_key)
