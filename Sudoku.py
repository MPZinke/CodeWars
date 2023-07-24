
# https://www.codewars.com/kata/5296bc77afba8baa690002d7/train/python


from typing import TypeVar


Puzzle = TypeVar("Puzzle")
ROW, COL = 0, 1


class Square:
    def __init__(self, puzzle: object, value: int, coordinates: list[int]):
        self._puzzle: object = puzzle
        self._value: int = value
        self._coordinates: list[int] = coordinates.copy()
        self._hints: list[int] = [value] if(self._value) else []


    def __str__(self) -> str:
        return str(self._value)


    def __repr__(self) -> str:
        return str(self)


    def __iter__(self) -> list[int]:
        return iter(self._hints.copy())


    def __int__(self) -> int:
        return self._value


    def __getitem__(self, coordinate: int) -> int:
        return self._coordinates[coordinate]


    def __contains__(self, value) -> int:
        return value in self._hints


    def __eq__(self, right) -> bool:
        return self._value == right


    def __ne__(self, right) -> bool:
        return self._value != right


    def __bool__(self) -> bool:
        return self != 0


    def determine_hints(self):
        if(self == 0):
            self._hints = self._trivial_hints()


    def _trivial_hints(self):
        if(self != 0):
            return

        known_values = [self._puzzle[row][self[COL]] for row in range(9)]  # row values
        known_values += [self._puzzle[self[ROW]][col] for col in range(9)]  # col values
        block_row, block_col = self[ROW] // 3, self[COL] // 3
        for row in range(block_row * 3, (block_row+1) * 3):
            for col in range(block_col * 3, (block_col+1) * 3):
                known_values.append(self._puzzle[row][col])

        return [value for value in range(1,10) if(value not in known_values)]


    def unique_hints(self):
        """
        Determine if any of the possible values for a square are not found for the possible values for other affecting
         squares.
        """
        # Row
        known_row_hints = []
        for row in range(9):
            if(row != self[ROW]):
                known_row_hints += list(self._puzzle[row][self[COL]])

        if(len(unique_row_hints := [hint for hint in self._hints if(hint not in known_row_hints)])):
            assert(len(unique_row_hints) == 1)
            self._hints = unique_row_hints

        # Columns
        known_col_hints = []
        for col in range(9):
            if(col != self[COL]):
                known_col_hints += list(self._puzzle[self[ROW]][col])

        if(len(unique_col_hints := [hint for hint in self._hints if(hint not in known_col_hints)])):
            assert(len(unique_col_hints) == 1)
            self._hints = unique_col_hints

        # Block
        known_block_hints = []
        block_row, block_col = self[ROW] // 3, self[COL] // 3
        for row in range(block_row * 3, (block_row+1) * 3):
            for col in range(block_col * 3, (block_col+1) * 3):
                if([row, col] != self._coordinates):
                    known_block_hints += list(self._puzzle[row][col])

        if(len(unique_block_hints := [val for val in self._hints if(val not in known_block_hints)])):
            assert(len(unique_block_hints) == 1)
            self._hints = unique_block_hints


class Puzzle:
    def __init__(self, puzzle: list[list[int]]):
        self._raw_puzzle: list[list[int]] = [[col for col in row] for row in puzzle]
        squares = [[Square(self, col, [x, y]) for y, col in enumerate(row)] for x, row in enumerate(puzzle)]
        self._squares: list[list[Square]] = squares


    def __call__(self) -> None:
        """
        Update the puzzle.
        """
        self.calculate_hints()
        for row in range(9):
            for col in range(9):
                possible_values = list(self[row][col])
                if(len(possible_values) == 1 and not self[row][col]):
                    self[row][col] = Square(self, possible_values[0], [row, col])


    def __bool__(self) -> bool:
        """
        Whether the puzzle still requires work.
        """
        return len(self) != 81


    def __getitem__(self, row: int) -> list[Square]:
        return self._squares[row]


    def __str__(self) -> str:
        puzzle = "||===|===|===||===|===|===||===|===|===||\n"
        for row in range(9):
            blocks = [self._squares[row][x: x+3] for x in range(0, 9, 3)]
            puzzle += f"""|| {" || ".join([" | ".join([f"{square}" for square in block]) for block in blocks])} ||\n"""
            if((row+1) % 3 == 0):
                puzzle += "||===|===|===||===|===|===||===|===|===||\n"
            else:
                puzzle += "||---|---|---||---|---|---||---|---|---||\n"

        return puzzle


    def possible_values_string(self) -> str:
        strings = [[str(list(square)) for square in row] for row in self._squares]
        length = max(len(col) for row in strings for col in row)

        block_delimiter = f"""||={"=||=".join(["=|=".join(["="*length for _ in range(3)]) for _ in range(3)])}==||"""
        row_delimiter = f"""||—{"—||—".join(["—|—".join(["—"*length for _ in range(3)]) for _ in range(3)])}—-||"""
        print(block_delimiter)
        for row in range(9):
            blocks = [strings[row][x: x+3] for x in range(0, 9, 3)]
            print(f"""|| {"|| ".join(["| ".join([f"{string:{length+1}}" for string in block]) for block in blocks])} ||""")
            print(block_delimiter if((row+1) % 3 == 0) else row_delimiter)


    def __repr__(self) -> str:
        return str(self)


    def __iter__(self) -> list[list[int]]:
        return iter([[int(square) for square in row] for row in self._squares])


    def __len__(self) -> int:
        return sum(1 for row in self._squares for square in row if(square))


    def calculate_hints(self):
        for row in self._squares:
            for square in row:
                square.determine_hints()

        for row in self._squares:
            for square in row:
                square.unique_hints()


def reduce_hints_limiting_groupings(puzzle_hints: list[list[list[int]]]):
    """
    Remove any possible values if they can be excluded by groups.
    EG.
    || [2,4] | [2,4] | [2,4,5] ||
      2,4 can be removed ^
    """
    pass



def sudoku(puzzle: list[list[int]]):
    puzzle = Puzzle(puzzle)
    print(puzzle)
    while(puzzle):
        puzzle()
        print(puzzle)

    return list(puzzle)


# def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    # for x in range(30):
    #     print(sum(1 for row in puzzle for col in row if(col != 0)))
    #     puzzle_hints = []
    #     for row in range(9):
    #         row_hints = []
    #         for col in range(9):
    #             if((square := puzzle[row][col]) != 0):
    #                 row_hints.append([square])
    #             else:
    #                 row_hints.append(possible_values(puzzle, [row, col]))

    #         puzzle_hints.append(row_hints)

    #     # print_board(puzzle)
    #     # print_hints(puzzle_hints)

    #     # print(sum(1 for row in puzzle for col in row if(col != 0)))
    #     for row in range(9):
    #         for col in range(9):
    #             if(len(puzzle_hints[row][col]) == 1):
    #                 puzzle[row][col] = puzzle_hints[row][col][0]




    # print_board(puzzle)
    # print_hints(puzzle_hints)

    return puzzle



puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]



sudoku(puzzle)
