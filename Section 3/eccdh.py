from random import SystemRandom
from ecc import Secp256k1


class ECCDiffieHellman:

	def __init__(self):
		self.curve = Secp256k1()
		self.priv = SystemRandom().randint(0, self.curve.p - 1)
		self.pub = self.curve.gen() * self.priv

	def shared(self, pub):
		return pub * self.priv

	def public_key(self):
		return self.pub


if __name__ == '__main__':
	ecdh1 = ECCDiffieHellman()
	ecdh2 = ECCDiffieHellman()

	shared_secret1 = ecdh1.shared(ecdh2.public_key()) 
	shared_secret2 = ecdh2.shared(ecdh1.public_key())

	assert(shared_secret1 == shared_secret2)
