from engine import Hanoi


def test_example():
    game = Hanoi(1, [0, 1, 0])
    assert game.step("lift", "1a")
    assert game.step("lift", "1b")
    assert game.step("place", "3a")
    assert game.winner() == 0


def test_illegal():
    game = Hanoi(1, [0, 0])
    assert not game._legal("lift", "1b")
    assert not game.step("lift", "1b")
    assert game._board["1a"] == [1]
    assert game.step("lift", "1a")


def test_history():
    game = Hanoi(1, [0, 1, 0])
    assert game._history[0] == (0, {"1a": (1,), "3a": (), "2": (), "1b": (2,), "3b": ()}, (None, None))
    game.step("lift", "1a")
    game.step("lift", "1b")
    game.step("place", "3a")
    assert len(game._history) == 4
    file = game.save("match.json")
    assert file.name == "match.json"


if __name__ == "__main__":
    test_example()
    test_illegal()
    test_history()
    print("all tests passed")
