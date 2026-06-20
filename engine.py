class Hanoi:
    def __init__(self, n_disks, turns):
        self._board = {
            "1a": [2 * i - 1 for i in range(n_disks, 0, -1)],
            "3a": [],
            "2": [],
            "1b": [2 * i for i in range(n_disks, 0, -1)],
            "3b": [],
        }
        self._turns = tuple(turns)
        self._n_disks = n_disks
        self._hands = [None, None]
        self._turn = 0
        self._history = []
        self._record()

    def step(self, *args):
        legal = self._legal(*args)
        if legal:
            kind = args[0]
            if kind == "lift":
                self._lift(*args[1:])
            elif kind == "place":
                self._place(*args[1:])
            else:
                self._skip(*args[1:])
        self._turn += 1
        self._record()
        return legal

    def _legal(self, *args):
        kind = args[0]
        if kind == "skip":
            return True
        player = self._turns[self._turn]
        pole = args[1]
        suffix = "ab"[player]
        if pole not in ("1" + suffix, "2", "3" + suffix):
            return False
        stack = self._board[pole]
        hand = self._hands[player]
        if kind == "lift":
            return hand is None and bool(stack)
        if kind == "place":
            return hand is not None and (not stack or hand < stack[-1])
        return False

    def _lift(self, *args):
        player = self._turns[self._turn]
        self._hands[player] = self._board[args[0]].pop()

    def _place(self, *args):
        player = self._turns[self._turn]
        self._board[args[0]].append(self._hands[player])
        self._hands[player] = None

    def _skip(self, *args):
        pass

    def winner(self):
        for player in (0, 1):
            suffix = "ab"[player]
            if (
                self._hands[player] is None
                and not self._board["1" + suffix]
                and not self._board["2"]
                and self._board["3" + suffix]
            ):
                return player
        return None

    def _record(self):
        self._history.append(
            (
                self._turn,
                {pole: tuple(stack) for pole, stack in self._board.items()},
                tuple(self._hands),
            )
        )

    def save(self, path):
        import json

        file = open(path, "w")
        json.dump(
            {
                "n_disks": self._n_disks,
                "turns": list(self._turns),
                "history": [
                    [turn, {pole: list(stack) for pole, stack in board.items()}, list(hands)]
                    for turn, board, hands in self._history
                ],
            },
            file,
        )
        file.close()
        return file
