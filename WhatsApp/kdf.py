import hashlib
import hmac

class KDF:

	def __init__(self, secret_key, shared):
		self.sk = secret_key
		self.rk, self.ck = self._kdf(shared)

	def _kdf(self, data):
		data = hmac.new(self.sk, data, hashlib.sha512).digest()
		return data[:32], data[32:]

	def update(self):
		self.ck, mk = self._kdf(self.ck)
		return mk
