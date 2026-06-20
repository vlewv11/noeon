import argparse
import json

from engine import Hanoi
from agent import Agent


def run(n_disks, turns, moves=None, seed=None):
    game = Hanoi(n_disks, turns)
    agents = (Agent(0, seed), Agent(1, None if seed is None else seed + 1))
    queue = None if moves is None else [tuple(move) for move in moves]
    played = []
    while game.get_turn() is not None and game.winner() is None:
        player = game.get_turn()
        if queue is None:
            action = agents[player].act(game)
        elif queue:
            action = queue.pop(0)
        else:
            break
        legal = game.step(*action)
        played.append(list(action))
        print(f"#{len(played):>3} p{player} {' '.join(action):<10} {'' if legal else 'ILLEGAL'} -> {game.get_board()}")
    print(f"winner: {game.winner()} after {len(played)} moves")
    return game, played


def test():
    game = Hanoi(1, [0, 1, 0])
    assert game.step("lift", "1a") and game.step("lift", "1b") and game.step("place", "3a")
    assert game.winner() == 0
    assert game._history[0] == (0, {"1a": (1,), "3a": (), "2": (), "1b": (2,), "3b": ()}, (None, None))
    assert len(game._history) == 4
    bad = Hanoi(1, [0, 0])
    assert not bad._legal("lift", "1b") and not bad.step("lift", "1b")
    assert bad._board["1a"] == [1] and bad.step("lift", "1a")
    assert not Hanoi(1, [0]).step("place", "3a")
    print("all tests passed")


def main():
    parser = argparse.ArgumentParser(prog="hanoi")
    sub = parser.add_subparsers(dest="mode", required=True)
    rnd = sub.add_parser("random")
    rnd.add_argument("--disks", type=int, default=3)
    rnd.add_argument("--turns", type=int, default=200)
    rnd.add_argument("--seed", type=int)
    rnd.add_argument("--out")
    sub.add_parser("replay").add_argument("file")
    sub.add_parser("test")
    args = parser.parse_args()

    if args.mode == "test":
        test()
    elif args.mode == "replay":
        with open(args.file) as file:
            data = json.load(file)
        run(data["n_disks"], data["turns"], data["moves"])
    else:
        turns = [i % 2 for i in range(args.turns)]
        played = run(args.disks, turns, seed=args.seed)[1]
        if args.out:
            with open(args.out, "w") as file:
                json.dump({"n_disks": args.disks, "turns": turns, "moves": played}, file, indent=2)


if __name__ == "__main__":
    main()
