import hashlib
import struct


def hmac(message):
    return hashlib.sha1("keykeykey1" + message).digest()


class SHA1LengthExtension:

    digest_size = 20
    block_size = 64

    def __init__(self, digest, data, key_len):
        # set constants
        self.h0 = struct.unpack(b'>I', digest[0:4])[0]
        self.h1 = struct.unpack(b'>I', digest[4:8])[0]
        self.h2 = struct.unpack(b'>I', digest[8:12])[0]
        self.h3 = struct.unpack(b'>I', digest[12:16])[0]
        self.h4 = struct.unpack(b'>I', digest[16:20])[0]

        # set the length of the unknown key
        self.key_len = key_len
        self.message = "\x00" * self.key_len + data
        self.total_message_length = 0

        # only used to reveal what message we need to feed the hmac with.
        self.message = self.append(self.message)

    def extend(self, new_data):
        # adjust so that the total bit length includes the key
        # and the known messge
        self.total_message_length = -(int(-len(self.message) // 64)) * 64
        chunk = self.append(new_data)
        return self.process(chunk), self.message[self.key_len:] + new_data

    def append(self, message):
        self.total_message_length += len(message)
        message_length = len(message)
        message += b'\x80'
        message += b'\x00' * ((56 - (message_length + 1) % 64) % 64)
        message_bit_length = self.total_message_length * 8
        message += struct.pack(b'>Q', message_bit_length)
        return message

    def process(self, chunk):

        w = [0] * 80
        for i in range(16):
            w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]

        # message expansion
        for i in range(16, 80):
            w[i] = self.rotate_left(
                w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1
            )

        a = self.h0
        b = self.h1
        c = self.h2
        d = self.h3
        e = self.h4

        for i in xrange(80):

            if 0 <= i <= 19:
                f = d ^ (b & (c ^ d))
                k = 0x5a827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6eD9eba1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1bbcdc
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xca62C1D6

            a, b, c, d, e = ((
                self.rotate_left(a, 5) + f + e + k + w[i]) & 0xffffffff,
                a,
                self.rotate_left(b, 30),
                c,
                d
            )

        h0 = struct.pack(b'>I', (self.h0 + a) & 0xffffffff)
        h1 = struct.pack(b'>I', (self.h1 + b) & 0xffffffff)
        h2 = struct.pack(b'>I', (self.h2 + c) & 0xffffffff)
        h3 = struct.pack(b'>I', (self.h3 + d) & 0xffffffff)
        h4 = struct.pack(b'>I', (self.h4 + e) & 0xffffffff)

        return h0 + h1 + h2 + h3 + h4

    def rotate_left(self, n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff


if __name__ == '__main__':
    # the length-extension with sha1 constants set as initial digest
    # reduces to normal sha1, i.e., using the algorithm for length extension,
    # we can compute normal sha1 digests.
    s = SHA1LengthExtension(
        "67452301efcdab8998badcfe10325476c3d2e1f0".decode("hex"), "", 0
    )
    # this is a test to make sure the length-extension code works as
    # it should.
    assert(
        s.process(s.append("hello")) == hashlib.sha1("hello").digest()
    )

    # first, we compute the bad hmac using the key+message concatentation
    # construction, i.e., we find the initial constants for sha1.
    digest = hmac("hello")

    # feeding the unknown key length to the length extension, along with
    # the known message (note, the key length can be bruteforced if given
    # access to an oracle, which usually is the case in reality)
    s = SHA1LengthExtension(digest, "hello", 10)

    # extend the hmac with additional data and verify against oracle
    new_digest, m = s.extend("file")
    assert(hmac(m) == new_digest)
