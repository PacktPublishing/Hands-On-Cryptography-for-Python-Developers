import ctypes


class PythonString:
    """
        illustrates the hash function of Python2 on a 64-bit system
    """

    def __init__(self, s):
        self.string = s

    def hash(self):
        h = ord(self.string[0]) << 7
        for char in self.string:
            h = 1000003 * h ^ ord(char)
        h ^= len(self.string)
        if h == -1:
            h = -2
        return ctypes.c_int64(h % 2**64).value

if __name__ == '__main__':
    # this is our 'simulated' python-string object
    pstr = "this is a Python string"
    p = PythonString(pstr)

    # make sure it does confirm with the internal hash
    assert(p.hash() == hash(pstr))

    # it is trivial to create collision in python too!
    string1 = "\x00\x00\x00\x01\x00"
    string2 = "\x00\x00\x00\x00\x00\x01\x02"
    string3 = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x09"

    # make sure they really are collisons
    assert(hash(string1) == hash(string2))
    assert(string1 != string2)
    
    # in some implementations, this could be exploited!
    # hence, never use python's hash function for crypto.
