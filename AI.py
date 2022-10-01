from player import *

class playerAI(Player(name)):
    def __init__(self):
        Player.__init__(self, "AI")
        self.safe_tile = set()
        self.safe_tile.