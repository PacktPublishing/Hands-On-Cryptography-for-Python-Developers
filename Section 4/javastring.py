import ctypes


class JavaString:

    def __init__(self, s):
        self.string = s

    def hash(self):
        h = 0
        n = len(self.string)
        for i in xrange(n):
            h += ord(self.string[i]) * pow(31, n - 1 - i, 2**32)
        return ctypes.c_int32(h % 2**32).value

if __name__ == '__main__':
    # create a fictional java-string object
    j = JavaString("this is a Java string")
    print(j.hash())

    # it is trivial to find collisions
    assert(JavaString("\x01\x00").hash() == JavaString("\x1f").hash())
    """
    public class MyClass {
        public static void main(String args[]) {
            String s1 = "\u0001\u0000";
            String s2 = "\u001f";
            System.out.println(s1.hashCode());
            System.out.println(s2.hashCode());
        }
    }
    prints:
    31
    31
    """
