import random


class Agent:
    def __init__(self, player, seed=None):
        self.player = player
        self._rng = random.Random(seed)

    def act(self, game):
        if game.get_turn() != self.player:
            raise ValueError("not this agent's turn")
        obs = game.observe(self.player)
        hand = obs["hand"]
        moves = [("skip",)]
        for pole, stack in obs["poles"].items():
            if hand is None:
                if stack:
                    moves.append(("lift", pole))
            elif not stack or hand < stack[-1]:
                moves.append(("place", pole))
        return self._rng.choice(moves)
