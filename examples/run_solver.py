from sudoku_solver.board import SudokuBoard
from sudoku_solver.solver import SudokuSolver


def print_board(board: SudokuBoard) -> None:
    for row_index, row in enumerate(board.matrix):
        if row_index % 3 == 0 and row_index != 0:
            print("-" * 21)

        row_values = []
        for col_index, value in enumerate(row):
            if col_index % 3 == 0 and col_index != 0:
                row_values.append("|")
            row_values.append(str(value))

        print(" ".join(row_values))


def main() -> None:
    # Example puzzle 
    puzzle = [
        [0, 0, 6, 0, 0, 4, 0, 0, 2],
        [0, 0, 0, 7, 0, 3, 0, 0, 0],
        [0, 9, 0, 6, 1, 0, 0, 0, 0],
        [5, 0, 9, 0, 0, 0, 0, 7, 8],
        [0, 4, 0, 0, 0, 0, 0, 9, 0],
        [7, 1, 0, 0, 0, 0, 3, 0, 6],
        [0, 0, 0, 0, 2, 6, 0, 8, 0],
        [0, 0, 0, 1, 0, 8, 0, 0, 0],
        [3, 0, 0, 4, 0, 0, 9, 0, 0]
    ]
    board = SudokuBoard(puzzle)
    solver = SudokuSolver()

    print("Original puzzle:\n")
    print_board(board)

    # Solution without MRV heuristic for comparison
    board_basic = SudokuBoard([row[:] for row in puzzle])
    solver.reset_steps()
    solver.solve_without_MRV(board_basic)
    basic_steps = solver.steps

    # Solution with MRV heuristic
    board_mrv = SudokuBoard([row[:] for row in puzzle])
    solver.reset_steps()
    solver.solve(board_mrv)
    mrv_steps = solver.steps


    print("\nSolution of the Sudoku puzzle:\n")
    print_board(board_mrv)
    print("\nSteps tried:", solver.steps)
    print("Steps without MRV:", basic_steps)
    print()




if __name__ == "__main__":
    main()