import itertools

from main import Game, Strategy


def test_game_initialization():
    width, height = 8, 8
    game = Game(width, height, (0, 0), Strategy.DFS)
    assert game.width == width
    assert game.height == height
    assert game.curr == (0, 0)


def test_game_initialization_different_size():
    width, height = 4, 4
    game = Game(width, height, (1, 1), Strategy.DFS)
    assert game.width == width
    assert game.height == height
    assert game.curr == (1, 1)


def test_valid_moves_returns_list():
    game = Game(8, 8, (0, 0), Strategy.DFS)
    moves = game.valid_moves(game.start, [])
    assert isinstance(moves, list)


def test_valid_moves_from_corner():
    game = Game(8, 8, (0, 0), Strategy.DFS)
    moves = game.valid_moves(game.start, [])
    expected_moves = [(2, 1), (1, 2)]
    assert len(moves) == len(expected_moves)
    assert all(move in expected_moves for move in moves)


def test_valid_moves_from_center():
    game = Game(8, 8, (3, 3), Strategy.DFS)
    moves = game.valid_moves(game.start, [])
    expected_moves = [
        (5, 2),
        (5, 4),
        (4, 5),
        (2, 5),
        (1, 4),
        (1, 2),
        (2, 1),
        (4, 1),
    ]
    assert len(moves) == 8  # noqa: PLR2004
    assert all(move in expected_moves for move in moves)


def test_valid_moves_from_center_with_visited():
    game = Game(8, 8, (3, 3), Strategy.DFS)
    moves = game.valid_moves(game.start, [(5, 2)])
    expected_moves = [
        (5, 4),
        (4, 5),
        (2, 5),
        (1, 4),
        (1, 2),
        (2, 1),
        (4, 1),
    ]
    assert len(moves) == 7  # noqa: PLR2004
    assert all(move in expected_moves for move in moves)


def test_valid_moves_from_point_with_visited():
    game = Game(8, 8, (3, 7), Strategy.DFS)
    moves = game.valid_moves(game.start, [])
    expected_moves = [
        (5, 6),
        (1, 6),
        (2, 5),
        (4, 5),
    ]
    assert len(moves) == 4  # noqa: PLR2004
    assert all(move in expected_moves for move in moves)


def test_find_tour_returns_list():
    game = Game(5, 5, (0, 0), Strategy.DFS)
    _, tour = game.find_tour(game.start, [game.start])
    assert isinstance(tour, list)


def test_find_tour_returns_solution():
    game = Game(6, 6, (3, 3), Strategy.DFS)
    _, tour = game.find_tour(game.start, [game.start])

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 36  # noqa: PLR2004


def test_find_tour_returns_solution_for_rectangle():
    game = Game(4, 6, (3, 3), Strategy.DFS)
    _, tour = game.find_tour(game.start, [game.start])

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 24  # noqa: PLR2004


def test_next_move_returns_valid_move():
    game = Game(5, 5, (2, 2), Strategy.WARNSDORF)
    move = game.next_move((2, 2), [(2, 2)])
    assert move in game.valid_moves((2, 2), [(2, 2)])


def test_find_tour_optimised_returns_solution():
    game = Game(8, 8, (0, 0), Strategy.WARNSDORF)
    _, tour = game.find_tour_optimised(game.start, [game.start])

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 64  # noqa: PLR2004


def test_run_with_dfs_strategy():
    game = Game(5, 5, (0, 0), Strategy.DFS)
    _, tour = game.run(game.start, [game.start])
    assert isinstance(tour, list)
    assert len(tour) == 25  # noqa: PLR2004


def test_run_with_warnsdorf_strategy():
    game = Game(8, 8, (0, 0), Strategy.WARNSDORF)
    _, tour = game.run(game.start, [game.start])
    assert isinstance(tour, list)
    assert len(tour) == 64  # noqa: PLR2004
