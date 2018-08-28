import random
from point import *


class Shamir:

    def unsplit(self, xcords, ycords, evaluation):
        P = Point(1)
        S = Point(0)
        Z = Point(evaluation)

        # Pre-compute nominator
        for xcord in xcords:
            P *= Z + Point(xcord)

        # Perform Lagrange interpolation over GF(2^8)
        for xcord, ycord in zip(xcords, ycords):
            Q = P / (Z + Point(xcord))
            Px = Point(xcord)
            Py = Point(ycord)

            # ...and evalaute it in x = 0
            for denom in xcords:
                if xcord != denom:
                    Q /= (Px + Point(denom))
            S += Py * Q
        return S.value

    def split(self, shares, threshold, secret):
        rng = random.SystemRandom()

        # Define polynomial to be P(0) = secret
        coeffs = [secret] + [rng.randint(0, 256) for _ in range(threshold - 1)]
        coords = list()
        result = list()

        # Find a set with unique shares
        while len(coords) < shares:
            drawn = rng.randint(1, 255)
            if not drawn in coords:
                coords += [drawn]

        # Evaluate polynomial in all coords
        for coord in coords:
            B = Point(1)
            S = Point(0)
            X = Point(coord)
            for coeff in coeffs:
                S += (B * Point(coeff))
                B *= X
            result.append(S.value)
        return coords, result
