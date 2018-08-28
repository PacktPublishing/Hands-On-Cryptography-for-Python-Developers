from field import modinv


class Curve:

    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        # assert discriminant is non-zero to avoid singular points
        if 4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p) % self.p == 0:
            raise Exception("Singular curve")

    def __eq__(self, other):
        if isinstance(other, Curve):
            return (self.a == other.a) and (self.b == other.b) and (self.p == other.p)
        return NotImplemented

    def __contains__(self, point):
        yy = pow(point.y, 2, self.p)
        xx = pow(point.x, 3, self.p) + point.x * self.a + self.b
        return yy == xx % self.p

    def __str__(self):
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.p)

    def zero(self):
        return Point(0, 0, self, zero=True)


class Point:

    def __init__(self, x, y, curve, zero=False):
        self.curve = curve
        self.x = x % self.curve.p
        self.y = y % self.curve.p
        if not self in self.curve and not zero:
            raise Exception("Not on curve")

    def is_zero(self):
        # the zero element is not on the curve
        return self.x == 0 and self.y == 0

    def __add__(self, point):
        if self.is_zero():
            return point
        if point.is_zero():
            return self
        if self == -point:
            return self.curve.zero()
        if self == point:
            s = (3 * self.x ** 2 + self.curve.a) * \
                modinv(2 * self.y, self.curve.p) % self.curve.p
        else:
            s = (self.y - point.y) * modinv(self.x -
                                            point.x, self.curve.p) % self.curve.p
        xx = (s ** 2 - self.x - point.x) % self.curve.p
        yy = (s * (self.x - xx) - self.y) % self.curve.p
        return Point(xx, yy, self.curve)

    def __mul__(self, scalar):
        try:
            scalar = int(scalar)
        except:
            raise Exception("Needs to be a scalar")
        if scalar < 0:
            return - (self * scalar)
        if scalar == 0:
            return self.curve.zero()
        x = self.curve.zero()
        y = self
        while scalar > 1:
            if scalar % 2 == 0:
                y = y + y
                scalar = scalar / 2
            else:
                x = x + y
                y = y + y
                scalar = (scalar - 1) / 2
        return x + y

    def __neg__(self):
        return Point(self.x, -self.y, self.curve)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        return NotImplemented

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Secp256k1(Curve):

    def __init__(self):
        self.a = 0
        self.b = 7
        self.p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f

    def gen(self):
        return Point(
            0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
            self
        )

if __name__ == '__main__':
    c = Secp256k1()
    g = c.gen()
