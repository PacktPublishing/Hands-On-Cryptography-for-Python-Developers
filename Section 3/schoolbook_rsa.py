from field import modinv

class SchoolbookRSA:

    def __init__(self, p, q, e=65537):
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = e
        self.d = modinv(self.e, self.phi)

    def _is_prime(self, p):
        """ Fermat primality test """

    def encrypt(self, message):
        return pow(message, self.e, self.n)

    def decrypt(self, ciphertext):
        return pow(ciphertext, self.d, self.n)


if __name__ == '__main__':
    rsa = SchoolbookRSA(61,53)

    encrypted = rsa.encrypt(7)
    print encrypted
    print rsa.decrypt(encrypted)
