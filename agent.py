import random


class Agent:
    def __init__(self, player, seed=None):
        self.player = player
        self._rng = random.Random(seed)

    def act(self, game):
        if game.get_turn() != self.player:
            raise ValueError("not this agent's turn")
        moves = [("skip",)]
        for pole in game.get_board():
            if game._legal("lift", pole):
                moves.append(("lift", pole))
            if game._legal("place", pole):
                moves.append(("place", pole))
        return self._rng.choice(moves)
