from kdf import KDF
from diffiehellman import DiffieHellman

class State:

	def __init__(self):
		self.dh = DiffieHellman()

	def setup(self, secret_key, public_key):
		self.dh = DiffieHellman()
		self.kdf = KDF(secret_key, self.dh.shared(public_key))

	def update(self):
		return self.kdf.update()

def debug(*args):
	print ("debug", " ".join(args))

class Client:

	def __init__(self, name):
		self.state = State()
		self.name = name
		self.sk = "secret"
		self.seq = 0

	def connect(self, other_client):
		# think of this as a socket connection
		self.other_client = other_client

	def send(self, message):
		if self.seq == 0:
			self.send_dh_ratchet()
			self.other_client.receive_dh_ratchet()
		self.seq += 1
		# do a kdf update to get message key
		message_key = self.state.update()
		# encrypt the message
		encrypted_message = self.encrypt(message)
		# print to debug
		debug(self.name, "sends message", message, "encrypted as", encrypted_message, "key =", message_key)
		# signal to other client to receive
		self.other_client.receive(encrypted_message)

	def encrypt(self, message):
		return message

	def receive(self, encrypted_message):
		message_key = self.state.update()
		debug(self.name, "gets message", encrypted_message, "key =", message_key)

	def decrypt(self, encrypted_message):
		return encrypted_message

	def send_dh_ratchet(self):
		self.state.setup(self.sk, self.other_client.state.dh.public_key)
		debug(self.name, "sends DH ratchet")

	def receive_dh_ratchet(self):
		self.seq = 0
		self.state.setup(self.sk, self.other_client.state.dh.public_key)
		debug(self.name, "receives DH ratchet")


alice = Client("Alice")
bob = Client("Bob")

alice.connect(bob)
bob.connect(alice)

alice.send("hello")
alice.send("whatsapp?")
bob.send("hi")
bob.send("signal!")