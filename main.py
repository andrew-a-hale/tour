import argparse
import enum

import xpress as xp
from z3 import Distinct, Int, Or, Solver, sat

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
    WARNSDORFF = 2
    SAT = 3
    LINEAR = 4


class Game:
    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        start: tuple[int, int] = (0, 0),
        strategy: Strategy = Strategy.DFS,
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

    def valid_moves_ordered(
        self,
        start: tuple[int, int],
        visited: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        valid_moves = self.valid_moves(start, visited)
        onward_moves = {}
        for move in valid_moves:
            onward_moves[move] = len(self.valid_moves(move, [*visited, move]))

        return sorted(onward_moves.keys(), key=lambda k: onward_moves[k])

    def coord_tuple_to_int(self, point: tuple[int, int]) -> int:
        return (self.width) * point[0] + point[1]

    def coord_int_to_tuple(self, point: int) -> tuple[int, int]:
        return divmod(point, self.width)

    def find_tour(
        self,
        pos: tuple[int, int],
        tour: list[tuple[int, int]],
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        if len(tour) == self.total_cells:
            return pos, tour

        if len(tour) >= self.total_cells:
            return self.start, []

        for move in self.valid_moves(pos, tour):
            res_pos, res_tour = self.find_tour(move, [*tour, move])

            if res_tour:
                return res_pos, res_tour

        return self.start, []

    def find_tour_warnsdorff(
        self,
        pos: tuple[int, int],
        tour: list[tuple[int, int]],
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        if len(tour) == self.total_cells:
            return pos, tour

        if len(tour) >= self.total_cells:
            return self.start, []

        for move in self.valid_moves_ordered(pos, tour):
            res_pos, res_tour = self.find_tour_warnsdorff(move, [*tour, move])

            if res_tour:
                return res_pos, res_tour

        return self.start, []

    def find_tour_sat(
        self,
        pos: tuple[int, int],
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        # construct graph as adj matrix
        graph = {
            c: [
                self.coord_tuple_to_int(x)
                for x in self.valid_moves(self.coord_int_to_tuple(c), [])
            ]
            for c in range(self.total_cells)
        }

        solver = Solver()
        x = [Int(f"x_{i}") for i in range(self.total_cells)]
        solver.add(x[0] == self.coord_tuple_to_int(pos))

        # constraint uniqueness
        solver.add(Distinct(x))

        for i in range(self.total_cells):
            # constraint 0 <= X[i] < size
            solver.add(x[i] >= 0, x[i] < self.total_cells)

            # constaint X[i] is a valid move
            solver.add(
                Or(
                    Or([x[j] == x[i] + 1 for j in graph[i]]),
                    x[i] + 1 == self.total_cells,
                )
            )

            for j in range(self.total_cells):
                if i != j:
                    solver.add(x[i] != x[j])

        tour = []
        if solver.check() == sat:
            model = solver.model()
            tour = [model.get_interp(x_i).as_long() for x_i in x]  # index for cells
            tour = {p: i for i, p in enumerate(tour)}  # invert
            # index for knight move
            tour = [self.coord_int_to_tuple(tour[x]) for x in range(len(tour))]

        return pos, tour

    def find_tour_linear(self) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        # construct graph as adj matrix
        graph = {
            c: [
                self.coord_tuple_to_int(x)
                for x in self.valid_moves(self.coord_int_to_tuple(c), [])
            ]
            for c in range(self.total_cells)
        }

        problem = xp.problem()
        edges = {}

        for i in range(self.total_cells):
            for j in graph[i]:
                edges[(i, j)] = problem.addVariable(
                    name=f"e_{i}_{j}", vartype=xp.binary
                )

        for i in range(self.total_cells):
            ins = [v for k, v in edges.items() if k[1] == i]
            outs = [v for k, v in edges.items() if k[0] == i]

            if i == 0:  # start node: 1 out, 0 in
                problem.addConstraint(xp.Sum(ins) == 0)
                problem.addConstraint(xp.Sum(outs) == 1)
            else:  # all other nodes: 1 in, at most 1 out
                problem.addConstraint(xp.Sum(ins) == 1)
                problem.addConstraint(xp.Sum(outs) <= 1)

        x = [
            problem.addVariable(name=f"x_{i}", vartype=xp.integer)
            for i in range(self.total_cells)
        ]
        problem.addConstraint(x[0] == 0)

        for i, j in edges:  # noqa: PLC0206
            if j == 0:
                continue

            edge_var = edges[(i, j)]
            problem.addConstraint(x[j] <= x[i] + 1 + self.total_cells * (1 - edge_var))
            problem.addConstraint(
                x[j] >= x[i] + 1 - self.total_cells * (j == 0) * (1 - edge_var)
            )

        problem.solve()

        tour = list(map(int, problem.getSolution()[-self.total_cells :]))
        tour = {p: i for i, p in enumerate(tour)}  # invert
        # index for knight move
        tour = [self.coord_int_to_tuple(tour[x]) for x in range(len(tour))]

        return (0, 0), tour

    def run(
        self,
        pos: tuple[int, int],
        tour: list[tuple[int, int]],
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        match self.strategy:
            case Strategy.DFS:
                return self.find_tour(pos, tour)

            case Strategy.WARNSDORFF:
                return self.find_tour_warnsdorff(pos, tour)

            case Strategy.SAT:
                return self.find_tour_sat(pos)

            case Strategy.LINEAR:
                return self.find_tour_linear()


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

    game = Game(args.width, args.height, (0, 0), Strategy.LINEAR)
    _, tour = game.run(game.start, [game.start])
    print(tour)  # noqa: T201


if __name__ == "__main__":
    main()
