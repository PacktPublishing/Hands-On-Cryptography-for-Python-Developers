class JavaString:

    def __init__(self, s):
        self.string = s

    def hash(self):
        h = 0
        n = len(self.string)
        for i in xrange(n):
            h += ord(self.string[i]) * pow(31, n-1-i, 2**32)
        return h

if __name__ == '__main__':
    j = JavaString("this is a Java string")
    print j.hash()

    # it is trivial to find collisions
    assert(JavaString("\x01\x00").hash() == JavaString("\x1f").hash())
