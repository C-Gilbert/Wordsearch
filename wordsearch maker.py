from random import choice, randint, randrange
import string

DIRECTIONS = ((0, 1), (1, 0), (1, 1), (-1, 1))
NO_OF_DIR = len(DIRECTIONS)
WORD_MIN = 4   # length of shortest word allowed
WORD_MAX = 8  # length of longest word allowed

def read_puzzle(file_name: str) -> list:
    """Return a 2D list read from a text file and representing 
       a wordsearch puzzle. 
    """
    with open(file_name) as file:
        puzzle = []
        for line in file:
            word = line.strip()
            r = list(word)
            puzzle.append(r)
    return puzzle

def display_puzzle(puzzle: list) -> None:
    """Display a 2D list formatted as a wordsearch puzzle."""
    print((4*len(puzzle)+1)*'-')
    for row in puzzle:
        print('|', end="" )
        for letter in row:
            print(' ' + letter + ' |', end="" )
        print()
    print((4*len(puzzle)+1)*'-')

def read_words(file_name: str) -> set:
    """Return a set of words read from a text file. 
    
       The words will be in upper case and of length L where 
       WORD_MIN <= L <= WORD_MAX.
    """
    valid_words = set()
    with open(file_name) as file:
        for line in file:
            word = line.strip()
            if WORD_MIN <= len(word) <= WORD_MAX:
                valid_words.add(word.upper())
    return valid_words

def create_empty_grid(puzzle_size : int) -> list:
    puzzle = []
    for row in range(puzzle_size):
        puzzle.append(list(puzzle_size*' '))       
    return puzzle

def random_fill_blanks(puzzle: list) -> list:
    """ Fill all non-blank entries in the puzzle grid with random upper case letters. """
    p = len(puzzle)
    for i in range(p):
        for j in range(p):
            if puzzle[i][j] == ' ':
                puzzle[i][j] = choice(string.ascii_uppercase)
    return(puzzle)

def random_dir() -> tuple:
    """Return a random direction for a word."""
    return(DIRECTIONS[randrange(0, NO_OF_DIR)])

def random_pos(start, end) -> tuple:
    """Return a random (row, col) position within a range.

    Postcondition:
    - returned values in tuple are integers in range 'start' to 'end-1'
    """
    return (randrange(start, end), randrange(start, end))

def is_in_grid(grid: list, row: int, col: int) -> bool:
    """Check if row and column position lies within a grid."""
    return -1 < row < (len(grid)) and -1 < col < (len(grid))

def add_word(grid: list, word: str, start_pos: tuple, direction: tuple) -> None:
    """Add word to the grid in specified direction, starting at specified point.

    Precondition:
    - word fits within the grid
    """
    row = start_pos[0]
    col = start_pos[1]
    for letter in word:
        puzzle[row][col] = letter
        row += direction[0]
        col += direction[1]

def create_word_search(grid: list, words: set) -> (list, list):
    """Create a wordsearch grid containing hidden words from the given list.

    Preconditions:
    - grid is a square table (2D list) of characters, all initially blank
    - words is a set of strings representing words to be hidden in the grid
    Postconditions:
    - first returned value is the grid containing hidden words
    - second returned value is a list of the words that have been hidden
    """
    solutions = []
    extensions = []

    #build the inital candidates:
    for word in words:
        remaining = list(word)
        start = random_pos(0, len(grid) - len(word))
        direction = random_dir()
        extensions.append((word, start, direction, remaining[0], remaining))

    #check each candidate:
    for items in extensions:
        word = items[0]
        start_pos = items[1]
        direction = items[2]
        letter = items[3]
        remaining = items[4]
        extend( word, start_pos, start_pos, direction, letter, remaining, solutions, grid)

    return grid, solutions

def can_extend(row:int, col:int, letter: str, grid: list):
    """Check if square is in grid and empty or the same value needed to be placed."""
    if not(is_in_grid(grid, row, col)):
        return False
    if grid[row][col] == letter:
        return True
    return grid[row][col] == ' '

def extend(word: str, start_pos: list, pos: list, direction:tuple, letter:str, remaining:list, solutions:list, grid:list):
    """Extend the propsed word in the grid by one square. Add valid words to grid and to solutions."""
    if remaining == []:
        add_word(grid, word, start_pos, direction)
        solutions.append(word)
        return

    if can_extend(pos[0],pos[1], remaining[0], grid):
        pos = (pos[0]+direction[0],pos[1]+direction[1])
        extend(word, start_pos, pos, direction, remaining[0], remaining[1:], solutions, grid)
puzzle = create_empty_grid(int(input("Enter a grid size:")))
words_to_hide = read_words("vocabulary.txt")
puzzle, hidden_words = create_word_search(puzzle, words_to_hide)
display_puzzle(puzzle)
print(hidden_words)
display_puzzle(random_fill_blanks(puzzle))
input("Press Enter to close")