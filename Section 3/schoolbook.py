class RSA:

	def __init__(self, p, q, e=65537):
		self.p = p
		self.q = q
		self.n = self.p * self.q
		self.phi = (self.p - 1) * (self.q - 1)
		self.e = e
		self.d = self._modinv(self.e, self.phi)

	def _extended_gcd(self, a, b):
	    if a == 0:
	        return (b, 0, 1)
	    g, y, x = self._extended_gcd(b % a, a)
	    return (g, x - (b // a) * y, y)

	def _modinv(self, a, m):
	    g, x, y = self._extended_gcd(a, m)
	    if g != 1:
	        raise Exception('Element {} has no inverse' % a)
	    return x % m

	def _is_prime(self, p):
		""" Fermat primality test """

	def encrypt(self, message):
		return pow(message, self.e, self.n)

	def decrypt(self, ciphertext):
		return pow(ciphertext, self.d, self.n)


if __name__ == '__main__':
	rsa = RSA(61,53)

	encrypted = rsa.encrypt(7)
	print encrypted
	print rsa.decrypt(encrypted)
