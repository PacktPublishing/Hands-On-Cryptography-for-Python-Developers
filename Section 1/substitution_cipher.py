import string
import random


class SubstitutionCipher:

	def __init__(self):
		# Our cipher will operate on uppercase letters and space.
		self.alphabet = list(
			letter for letter in string.ascii_uppercase + " "
		)
		self.scrambled_alphabet = random.sample(self.alphabet, len(self.alphabet))
		self.lookup = {
			x: y for x, y in zip(self.alphabet, self.scrambled_alphabet)
		}
		self.inverse_lookup = {
			y: x for x, y in zip(self.alphabet, self.scrambled_alphabet)
		}

	def encrypt(self, plaintext):
		return "".join(self.lookup[letter] for letter in plaintext)

	def decrypt(self, ciphertext):
		return "".join(self.inverse_lookup[letter] for letter in ciphertext)

if __name__ == '__main__':
	plaintext = "HI BOB"
	s = SubstitutionCipher()

	ciphertext = s.encrypt(plaintext)

	print "ciphertext =", ciphertext
	print "decrypted =", s.decrypt(ciphertext)

