from schoolbook_rsa import SchoolbookRSA

rsa = SchoolbookRSA(61,53)
encrypted1 = rsa.encrypt(7)
encrypted2 = rsa.encrypt(3)
# Schoolbook RSA is malleable, meaning that we can
# alter two messages and make them decrypt to a
# desired result.
encrypted3 = encrypted1 * encrypted2
# Why is this bad? What about signing?
print rsa.decrypt(encrypted3)