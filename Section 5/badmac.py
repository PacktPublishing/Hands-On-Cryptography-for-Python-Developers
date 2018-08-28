import hashlib


class BadMAC:

    def __init__(self, key, message):
        self.key = key
        self.message = message
        self.hashfunction = hashlib.md5(self.key + self.message)

    def digest(self):
        return self.hashfunction.digest()

    def hexdigest(self):
        return self.hashfunction.hexdigest()


class LengthExtension:

    def __init__(self, secret_length, message, digest):
        self.secret_length = secret_length
        self.message = message
        self.digest = digest

    def extend(self, fun, additional_message):
        fun.update(additional_message)
        return self.message + "\x80" + "\x00" * (20 - len(self.message) - 1 - self.secret_length) + additional_message, fun.hexdigest()


if __name__ == '__main__':
    b = BadMAC("hunter2", "this is a good mac")
    mac = b.digest()
    l = LengthExtension(7, "this is a good mac", mac)
    print l.extend(b.hashfunction, "test")
