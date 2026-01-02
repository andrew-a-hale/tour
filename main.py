import enum
import argparse

MOVES = {
    "UL": (2, -1),
    "UR": (2, 1),
    "RU": (1, 2),
    "RD": (-1, 2),
    "DR": (-2, 1),
    "DL": (-2, -1),
    "LD": (-1, -2),
    "LU": (1, -2),
}


class Strategy(enum.Enum):
    DFS = 1
    WARNSDORF = 2


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        start: tuple[int, int],
        strategy: Strategy,
    ):
        self.width = width
        self.height = height
        self.curr = start
        self.start = start
        self.strategy = strategy

    @property
    def total_cells(self):
        return self.width * self.height

    def valid_moves(
        self,
        start: tuple[int, int],
        visited: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        moves = []
        for _, move in MOVES.items():
            r, c = start
            r += move[0]
            c += move[1]
            if (
                (0 <= r < self.height)
                and (0 <= c < self.width)
                and (r, c) not in visited
            ):
                moves.append((r, c))

        return moves

    def next_move(
        self,
        start: tuple[int, int],
        visited: list[tuple[int, int]],
    ) -> tuple[int, int]:
        valid_moves = self.valid_moves(start, visited)
        onward_moves = {}
        for move in valid_moves:
            onward_moves[move] = len(self.valid_moves(move, visited + [move]))

        return min(onward_moves.keys(), key=lambda k: onward_moves[k])

    def find_tour(
        self,
        pos: tuple[int, int],
        tour: list[tuple[int, int]],
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        if len(tour) == self.total_cells:
            return pos, tour
        elif len(tour) >= self.total_cells:
            return self.start, []

        for move in self.valid_moves(pos, tour):
            res_pos, res_tour = self.find_tour(move, tour + [move])

            if res_tour:
                return res_pos, res_tour

        return self.start, []

    def find_tour_optimised(
        self,
        pos: tuple[int, int],
        tour: list[tuple[int, int]],
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        if len(tour) == self.total_cells:
            return pos, tour
        elif len(tour) >= self.total_cells:
            return self.start, []

        move = self.next_move(pos, tour)
        res_pos, res_tour = self.find_tour_optimised(move, tour + [move])

        if res_tour:
            return res_pos, res_tour

        return self.start, []

    def run(self, pos: tuple[int, int], tour: list[tuple[int, int]]):
        match self.strategy:
            case Strategy.DFS:
                return self.find_tour(pos, tour)

            case Strategy.WARNSDORF:
                return self.find_tour_optimised(pos, tour)


def main():
    parser = argparse.ArgumentParser(description="Knight's Tour solver")
    parser.add_argument(
        "--width",
        type=int,
        default=5,
        help="Width of the chess board (default: 5)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=5,
        help="Height of the chess board (default: 5)",
    )
    args = parser.parse_args()

    game = Game(args.width, args.height, (0, 0), Strategy.WARNSDORF)
    _, tour = game.run(game.start, [game.start])
    assert len(tour) == args.width * args.height

    print(tour)


if __name__ == "__main__":
    main()
