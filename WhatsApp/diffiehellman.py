def _int2bin(num):
	c = hex(num)[2:]
	c = "0" * (len(c) % 2) + c
	return c.decode("hex")

def _bin2int(bins):
	return int(bins.encode("hex"), 16)

class DiffieHellman:

	# pre-defined constants
	modulus = _int2bin(13)
	gen = _int2bin(2)

	def __init__(self):
		self.priv = _int2bin(2) # random
		self.pub = self._pow(self.gen, self.priv, self.modulus)

	def _pow(self, a, b, c):
		return _int2bin(pow(_bin2int(a), _bin2int(b), _bin2int(c)))

	def shared(self, pub):
		return self._pow(self.pub, self.priv, self.modulus)

	def public_key(self):
		return self.pub