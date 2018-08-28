import os
import hashlib


class ProofOfWork:

    def __init__(self, difficulty):
        self.difficulty = difficulty

    def challenge(self):
        self.challenge_string = os.urandom(32)
        return self.challenge_string, self.difficulty

    def verify(self, proof):
        h = hashlib.sha256(self.challenge_string + proof)
        hi_bits = bin(int(h.hexdigest(), 16))[2:].zfill(h.digest_size * 8)

        # quite inefficient comparison, this does however only pose
        # a problem for the solver, which should implement a faster
        # simulator for its own purposes.
        if hi_bits[:self.difficulty] == "0" * self.difficulty:
            return True
        return False


class Solver:

    def __init__(self, challenge_string, difficulty):
        self.difficulty = difficulty
        self.challenge_string = challenge_string

    def solve(self):
        # create a simulated verifier, for a real-world scenario
        # the verifier should be implemented more efficiently.
        # for instance, in bitcoin, asics are highly efficient
        # implementions of the simulator.
        simulated_verifier = ProofOfWork(self.difficulty)
        simulated_verifier.challenge_string = self.challenge_string
        while True:
            proof = os.urandom(32)
            if simulated_verifier.verify(proof):
                return proof


if __name__ == '__main__':
    # proof of work requiring ~ 2^18 iterations
    p = ProofOfWork(18)

    # generate challenge
    challenge, difficulty = p.challenge()

    # create a solver
    s = Solver(challenge, difficulty)

    # and solve corresponding challenge
    proof = s.solve()
    assert(p.verify(proof))
