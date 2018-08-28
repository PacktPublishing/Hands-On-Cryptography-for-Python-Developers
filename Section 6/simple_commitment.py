import os
import random
import hashlib

# let us play a game of resolving conflicts
# please add lizard and spock for more excitement
OUTCOMES = ["rock", "paper", "scissor"]


def flip():
    return OUTCOMES[random.randint(0, 2)]


def resolve(move1, move2):
    if move1 == move2:
        return 0
    if OUTCOMES.index(move1) == (OUTCOMES.index(move2) + 1) % 3:
        return 1
    else:
        return 2


class SimpleCommitment:

    def __init__(self):
        self.move = None

    def commit(self, move):
        if move not in OUTCOMES:
            raise Exception("No valid commitment")
        self.r = os.urandom(32)
        self.move = move
        return hashlib.sha256(self.r + self.move).hexdigest()

    def reveal(self):
        if self.move is None:
            raise Exception("No commitment has been done")
        return self.r, self.move

    def verify(self, commitment, r, move):
        if hashlib.sha256(r + move).hexdigest() != commitment:
            raise Exception("Commitment mismatch")

if __name__ == "__main__":
    # player 1 picks a move and commits
    s1 = SimpleCommitment()
    commitment1 = s1.commit(flip())

    # player 2 does a move and commits
    s2 = SimpleCommitment()
    commitment2 = s2.commit(flip())

    # make commitments public
    print("s1: {}".format(commitment1))
    print("s2: {}".format(commitment2))

    # wait until both parts have gotten the commitments
    r1, move1 = s1.reveal()
    r2, move2 = s2.reveal()

    # verify that commitments are ok
    s1.verify(commitment2, r2, move2)
    s2.verify(commitment1, r1, move1)

    # reolve the winner
    winner = resolve(move1, move2)
    if winner == 0:
        print("No winner (p1 = {}, p2 = {})".format(move1, move2))
    else:
        print("Player {} wins! (p1 = {}, p2 = {})".format(winner, move1, move2))
