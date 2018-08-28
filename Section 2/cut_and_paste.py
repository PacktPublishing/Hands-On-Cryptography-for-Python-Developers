import os
from Crypto.Cipher import AES

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)

plaintext1 = "this is a secret that must be always kept hidden"
plaintext2 = " that can be revealed to anyone!"

cipertext1 = cipher.encrypt(plaintext1)
cipertext2 = cipher.encrypt(plaintext2)

print cipher.decrypt(cipertext1[:16] + cipertext2)

key = os.urandom(16)
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)

plaintext1 = "this is a secret that must be always kept hidden"
plaintext2 = " that can be revealed to anyone!"

cipertext1 = cipher.encrypt(plaintext1)
cipertext2 = cipher.encrypt(plaintext2)

print[cipher.decrypt(iv + cipertext1 + cipertext2)]
