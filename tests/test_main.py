import itertools

import pytest

from main import Game, Strategy


def test_game_default_initialization():
    game = Game()
    assert game.width == 5  # noqa: PLR2004
    assert game.height == 5  # noqa: PLR2004
    assert game.curr == (0, 0)


def test_game_initialization_different_size():
    width, height = 4, 4
    game = Game(width, height, (1, 1))
    assert game.width == width
    assert game.height == height
    assert game.curr == (1, 1)


def test_valid_moves_returns_list():
    game = Game()
    moves = game.valid_moves(game.start, [])
    assert isinstance(moves, list)


def test_valid_moves_from_corner():
    game = Game(8, 8, (0, 0))
    moves = game.valid_moves(game.start, [])
    expected_moves = [(2, 1), (1, 2)]
    assert len(moves) == len(expected_moves)
    assert all(move in expected_moves for move in moves)


def test_valid_moves_from_center():
    game = Game(8, 8, (3, 3))
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
    game = Game(8, 8, (3, 3))
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
    game = Game(8, 8, (3, 7))
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
    game = Game()
    _, tour = game.find_tour(game.start, [game.start])
    assert isinstance(tour, list)


def test_find_tour_returns_solution():
    game = Game(6, 6, (3, 3))
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
    game = Game(4, 6, (3, 3))
    _, tour = game.find_tour(game.start, [game.start])

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 24  # noqa: PLR2004


def test_valid_moves_ordered_returns_valid_move():
    game = Game(5, 5, (2, 2))
    moves = game.valid_moves_ordered((2, 2), [(2, 2)])
    for move in moves:
        assert move in game.valid_moves((2, 2), [(2, 2)])


def test_find_tour_optimised_returns_solution():
    game = Game(8, 8, (0, 0), Strategy.WARNSDORFF)
    _, tour = game.find_tour_warnsdorff(game.start, [game.start])

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 64  # noqa: PLR2004


def test_find_tour_sat_returns_solution():
    game = Game(5, 5, (0, 0), Strategy.SAT)
    _, tour = game.find_tour_sat(game.start)

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 25  # noqa: PLR2004


def test_find_tour_linear_returns_solution():
    game = Game(8, 8, (0, 0), Strategy.LINEAR)
    _, tour = game.find_tour_linear()

    visited = [tour[0]]
    for prev, curr in itertools.pairwise(tour):
        dx = abs(prev[0] - curr[0])
        dy = abs(prev[1] - curr[1])
        assert dx + dy == 3  # noqa: PLR2004
        assert curr not in visited
        visited.append(curr)

    assert len(tour) == 64  # noqa: PLR2004


@pytest.mark.parametrize(
    ("width", "height", "point", "expected"),
    [
        (5, 5, (0, 0), 0),
        (5, 5, (4, 4), 24),
        (8, 8, (0, 0), 0),
        (8, 8, (7, 7), 63),
        (4, 6, (0, 0), 0),
        (4, 6, (3, 5), 17),
    ],
)
def test_coord_tuple_to_int(width, height, point, expected):
    game = Game(width, height)
    assert game.coord_tuple_to_int(point) == expected


@pytest.mark.parametrize(
    ("width", "height", "point", "expected"),
    [
        (5, 5, 0, (0, 0)),
        (5, 5, 24, (4, 4)),
        (8, 8, 0, (0, 0)),
        (8, 8, 63, (7, 7)),
        (4, 6, 0, (0, 0)),
        (4, 6, 17, (4, 1)),
    ],
)
def test_coord_int_to_tuple(width, height, point, expected):
    game = Game(width, height)
    assert game.coord_int_to_tuple(point) == expected
