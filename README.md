# Hanoi Crossing

A small engine for the two-player Hanoi Crossing game (see
`HANOI_CROSSING-v1.1.md`), plus a random agent and a CLI.

## Files

- `engine.py` — the game core. No I/O, no frontend assumptions.
- `agent.py` — a player that picks a random valid move.
- `main.py` — the CLI: `random`, `replay`, `test`.

## Run

```
python main.py test                                  # engine tests
python main.py random --disks 3 --turns 200 --seed 1 # two random agents
python main.py random --disks 2 --turns 40 --out m.json
python main.py replay m.json                          # replay recorded moves
```

`--disks`/`--turns` default to 3/200. `--out` saves the played moves so the
game can be replayed.

## Model

The board is a dict of pole → stack (list, bottom disk first). Poles `1a/3a`
are player 0's, `1b/3b` are player 1's, `2` is shared. Player 0 owns the odd
disks and starts on `1a`; player 1 the even disks on `1b`. A player is just
the index `0` or `1`.

An **action** is `(kind, pole)` with `kind` in `lift`/`place`/`skip` (skip
takes no pole). The acting player is read from the external turn order
(`self._turns[self._turn]`), never passed in — so a recorded move and a live
agent move are identical and nobody acts out of turn.

`step(action)` checks legality, dispatches to `_lift`/`_place`/`_skip`, and
advances the turn once — even for an illegal move, which wastes the turn.

## Reuse

The engine is pure state plus `step`, which is all an RL loop or a many-games
service needs — no engine changes required. The agent consumes it the
external way: `Agent.act(game)` reads only `observe(player)` (its own visible
poles and hand, never the opponent's), computes legal moves, and proposes an
action; the caller applies it with `game.step(*action)`. Swap `Agent` for a
trained policy and nothing else changes. The agent holds no game, so one
instance can drive many concurrent games.

## Design decisions

- **Players are indices.** Visibility and win poles derive from the index via
  `"ab"[player]`, so there's no separate player table to keep in sync.
- **Strict size check.** Placement uses `hand < stack[-1]`; disk sizes are
  unique (odd vs even) so strict `<` is correct.
- **Illegal moves waste the turn** instead of raising — matches the rules and
  suits an RL environment, where a policy may emit an invalid action.
- **Win tie-break.** `winner()` checks player 0 first if both somehow qualify.
- **History stores states, not moves**, starting from the initial state, so
  each entry *is* a state. `save()` writes setup + history as JSON; the
  replay file (`--out`) is the complementary move log.
- **Partial observability is a real interface.** `observe(player)` exposes
  only that player's poles and hand; `get_board()` is the full referee view
  used by the CLI to print state. Both return copies.

## AI use

Claude Code was used for ~90% of code generation and template generation,
developed iteratively and reviewed against the spec.
