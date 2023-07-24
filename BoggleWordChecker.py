

# https://www.codewars.com/kata/57680d0128ed87c94f000bfd/train/python


def find_word(board, word):
	search_patterns = [
		[-1, -1], [-1, 0], [-1, 1],
		[ 0, -1], [ 0, 0], [ 0, 1],
		[ 1, -1], [ 1, 0], [ 1, 1]
	]
	def recurse(board, word, current_position=[0, 0]):
		if(word == ""):
			return True

		if(word[0] != board[current_position[0]][current_position[1]]):
			return False

		board[current_position[0]][current_position[1]] = None
		for pattern in search_patterns:
			next_position = [current_position[x] + pattern[x] for x in [0, 1]]
			if(all(0 <= coordinate < len(board) for coordinate in next_position)
			  and recurse(board, word[1:], next_position) is True):
				return True

		board[current_position[0]][current_position[1]] = word[0]  # Restore position
		return False

	board_copy = [[character for character in row] for row in board]  # Deepcopy board
	for x in range(len(board)):
		for y in range(len(board)):
			if(recurse(board_copy, word, [x, y])):
				return True

	return False


def match_word(board, word, current_square, pattern) -> bool:
    for x in range(len(word)):
        if(board[current_square[0]][current_square[1]] != word[x]):
            return False

        current_square = [current_square[y] + pattern[y] for y in [0, 1]]

    return True


def find_crossword_word(board, word):
    search_patterns = [
        [0, 1], [0, -1],  # horizontal
        [1, 0], [-1, 0],  # vertical
        [1, 1], [1, -1], [-1, 1], [-1, -1]  # diagonal
    ]

    for pattern in search_patterns:
        row_start = {-1: len(board) - 1}.get(pattern[0], 0)
        # `len(word) - (1+1)` -1 for index conversion, then additional -1 because end value is excluded
        row_end = {1: len(board) - (len(word)-1), -1: len(word) - 2}.get(pattern[0], len(board))
        for row in range(row_start, row_end, pattern[0] or 1):
            col_start = {-1: len(board) - 1}.get(pattern[1], 0)
            # `len(word) - (1+1)` -1 for index conversion, then additional -1 because end value is excluded
            col_end = {1: len(board) - (len(word)-1), -1: len(word) - 2}.get(pattern[1], len(board))
            for col in range(col_start, col_end, pattern[1] or 1):
                current_square = [row, col]
                if(match_word(board, word, [row, col], pattern)):
                    return True

    return False

testBoard = [
  ["E","A","R","A"],
  ["N","L","E","C"],
  ["I","A","I","S"],
  ["B","Y","O","R"]
]

print("""  ["E","A","R","A"],
  ["N","L","E","C"],
  ["I","A","I","S"],
  ["B","Y","O","R"]""")
    
find_word(testBoard, "C"               )
print()
find_word(testBoard, "EAR"             )
print()
find_word(testBoard, "BAILER"          )
print()
find_word(testBoard, "RSCAREIOYBAILNEA")
print()
