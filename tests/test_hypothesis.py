from hypothesis import given, settings
from hypothesis import strategies as st

from main import Game, Strategy


@given(
    st.integers(min_value=1, max_value=8),
    st.integers(min_value=1, max_value=8),
    st.integers(min_value=0, max_value=7),
    st.integers(min_value=0, max_value=7),
)
def test_game_initialization_properties(width, height, row, col):
    if row < height and col < width:
        game = Game(width, height, (row, col), Strategy.DFS)
        assert game.width == width
        assert game.height == height
        assert game.curr == (row, col)


@given(
    st.integers(min_value=1, max_value=8),
    st.integers(min_value=1, max_value=8),
    st.integers(min_value=0, max_value=7),
    st.integers(min_value=0, max_value=7),
)
def test_valid_moves_within_bounds(width, height, row, col):
    if row < height and col < width:
        game = Game(width, height, (row, col), Strategy.DFS)
        moves = game.valid_moves(game.start, [])
        for move in moves:
            assert 0 <= move[0] < height
            assert 0 <= move[1] < width


@given(
    st.integers(min_value=0, max_value=4).filter(lambda x: x % 2 == 0),
    st.integers(min_value=0, max_value=4).filter(lambda x: x % 2 == 0),
)
@settings(max_examples=3, deadline=None)
def test_find_tour(row, col):
    game = Game(5, 5, (row, col), Strategy.DFS)
    _, tour = game.find_tour(game.start, [game.start])
    assert len(tour) == 25  # noqa: PLR2004


@given(
    st.integers(min_value=0, max_value=7),
    st.integers(min_value=0, max_value=7),
)
@settings(max_examples=5, deadline=None)
def test_run_with_different_strategies(row, col):
    height, width = 8, 8
    if row < height and col < width:
        game = Game(width, height, (row, col), Strategy.WARNSDORF)
        _, tour = game.run(game.start, [game.start])
        assert len(tour) == width * height
