from sudoku_solver.board import SudokuBoard

class SudokuSolver:
    """Implements a recursive backtracking algorithm with MRV heuristic to find a valid solution for sudoku."""

    def __init__(self) -> None:
        self.steps = 0

    def reset_steps(self) -> None:
        self.steps = 0

    def solve(self, board: SudokuBoard) -> bool:
        empty_cell = board.find_cell_with_fewest_candidates()

        # When no empty cells left, the puzzle is solved.
        if empty_cell is None:
            return True

        row, col = empty_cell
        candidates = board.count_candidates(row, col)

        for v in candidates:
            board.set_cell(row, col, v)
            self.steps += 1

            if self.solve(board):
                return True

        return False
    
    def solve_without_MRV(self, board: SudokuBoard) -> bool:
        empty_cell = board.find_next_empty()

        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in range(1, 10):
            if board.is_valid_move(row, col, value):
                self.steps += 1
                board.set_cell(row, col, value)

                if self.solve_without_MRV(board):
                    return True

                board.set_cell(row, col, 0)

        return False