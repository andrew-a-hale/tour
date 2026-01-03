from hypothesis import given
from hypothesis import strategies as st

from main import Game


@given(
    st.integers(min_value=1, max_value=8),
    st.integers(min_value=1, max_value=8),
    st.integers(min_value=0, max_value=7),
    st.integers(min_value=0, max_value=7),
)
def test_game_initialization_properties(width, height, row, col):
    if row < height and col < width:
        game = Game(width, height, (row, col))
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
        game = Game(width, height, (row, col))
        moves = game.valid_moves(game.start, [])
        for move in moves:
            assert 0 <= move[0] < height
            assert 0 <= move[1] < width


@given(
    st.integers(min_value=0, max_value=7),
    st.integers(min_value=0, max_value=7),
)
def test_coord_conversion(x, y):
    game = Game(8, 9, (0, 0))
    assert game.coord_int_to_tuple(game.coord_tuple_to_int((y, x))) == (y, x)
