def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = extended_gcd(a % m, m)
    if g != 1:
        raise Exception('Element has no inverse')
    return x % m
