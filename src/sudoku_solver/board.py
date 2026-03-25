from dataclasses import dataclass
from typing import List, Optional, Tuple
from sudoku_solver.exceptions import *

SudokuBoardGrid = List[List[int]]

@dataclass
class SudokuBoard:
    """9x9 Sudoku board"""
    
    matrix: SudokuBoardGrid

    def __post_init__(self) -> None:
        """Perform automated validation after initialization"""
        self._validate_grid()
        if not self.is_legal():
            raise InvalidBoardError("Board has duplicate values in rows, columns, or 3x3 subgrids.")
        

    def _validate_grid(self) -> None:
        """Validate that the board between 0 and 9"""
        if len(self.matrix) != 9:
            raise InvalidBoardError("Board must have 9 rows.")
        for row in self.matrix:
            if len(row) != 9:
                raise InvalidBoardError("Board must have 9 columns.")
            for value in row:
                if not 0 <= value <= 9:
                    raise InvalidBoardError("Board values must be between 0 and 9.")
                
    
    def is_legal(self) -> bool:
        """Return true if the current board meet Sudoku rules."""
        for row in range(9):
            for col in range(9):
                v = self.matrix[row][col]

                if v == 0:
                    continue

                self.matrix[row][col] = 0
                is_valid = not (
                    self.exists_in_row(row, v)
                    or self.exists_in_col(col, v)
                    or self.exists_in_subgrid(row, col, v)
                )
                self.matrix[row][col] = v

                if not is_valid:
                    return False

        return True
    
    def get_cell(self, row: int, col: int) -> int:
            """Accesses the value at the specified coordinates."""
            return self.matrix[row][col]

    def set_cell(self, row: int, col: int, value: int) -> None:
            """Assigns a value to the specified coordinates."""
            self.matrix[row][col] = value

    def is_empty(self, row: int, col: int) -> bool:
            """Boolean check for cell vacancy."""
            return self.get_cell(row, col) == 0

    def find_next_empty(self) -> Optional[Tuple[int, int]]:
            """Returns the coordinates of the first vacant cell (0), or None if full."""
            for row in range(9):
                for col in range(9):
                    if self.matrix[row][col] == 0:
                        return row, col
            return None

    def exists_in_row(self, row: int, value: int) -> bool:
            """Row constraint validation."""
            return value in self.matrix[row]

    def exists_in_col(self, col: int, value: int) -> bool:
            """Column constraint validation."""
            return any(self.matrix[row][col] == value for row in range(9))

    def exists_in_subgrid(self, row: int, col: int, value: int) -> bool:
            """3x3 box constraint validation."""
            row_start = (row // 3) * 3
            col_start = (col // 3) * 3 

            for row in range(row_start, row_start + 3):
                for col in range(col_start, col_start + 3):
                    if self.matrix[row][col] == value:
                        return True
            return False

    def is_valid_move(self, row: int, col: int, value: int) -> bool:
            """Evaluates placing a value at the given coordinates."""
            if self.matrix[row][col] != 0:
                return False

            return not (
                self.exists_in_row(row, value)
                or self.exists_in_col(col, value)
                or self.exists_in_subgrid(row, col, value)
            )

    
    def count_candidates(self, row: int, col: int) -> List[int]:
            """Gets the list of valid candidate values for a given cell."""
            if self.matrix[row][col] != 0:
                return []

            candidates = []
            for value in range(1, 10):
                if self.is_valid_move(row, col, value):
                    candidates.append(value)

            return candidates
    
    def find_cell_with_fewest_candidates(self) -> Optional[Tuple[int, int]]:
            """Gets the coordinates of the cell with fewest valid candidates."""
            min_candidates = 10
            best_cell = None

            for row in range(9):
                for col in range(9):
                    if self.matrix[row][col] == 0:
                        candidate_count = len(self.count_candidates(row, col))
                        if candidate_count < min_candidates:
                            min_candidates = candidate_count
                            best_cell = (row, col)

                        if min_candidates == 1:
                            return best_cell

            return best_cell
    
    def copy(self) -> "SudokuBoard":
            """Generates a deep copy of the current state."""
            return SudokuBoard([row[:] for row in self.grid])