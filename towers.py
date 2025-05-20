#!/usr/bin/python3
"""
3D 6-Factor Tower Puzzle Solver
"""
board = [
    [{ 'size': 5, 'color': None}, { 'size': 3, 'color': None}, { 'size': 2, 'color': None}, { 'size': 1, 'color': None}, { 'size': 4, 'color': None}, { 'size': 6, 'color': None}],
    [{ 'size': 4, 'color': None}, { 'size': 1, 'color': None}, { 'size': 6, 'color': None}, { 'size': 2, 'color': None}, { 'size': 5, 'color': None}, { 'size': 3, 'color': None}],
    [{ 'size': 6, 'color': None}, { 'size': 5, 'color': None}, { 'size': 3, 'color': None}, { 'size': 4, 'color': None}, { 'size': 1, 'color': None}, { 'size': 2, 'color': None}],
    [{ 'size': 1, 'color': None}, { 'size': 2, 'color': None}, { 'size': 5, 'color': None}, { 'size': 3, 'color': None}, { 'size': 6, 'color': None}, { 'size': 4, 'color': None}],
    [{ 'size': 2, 'color': None}, { 'size': 4, 'color': None}, { 'size': 1, 'color': None}, { 'size': 6, 'color': None}, { 'size': 3, 'color': None}, { 'size': 5, 'color': None}],
    [{ 'size': 3, 'color': None}, { 'size': 6, 'color': None}, { 'size': 4, 'color': None}, { 'size': 5, 'color': None}, { 'size': 2, 'color': None}, { 'size': 1, 'color': None}]
]
n = len(board)
patterns = set()

def check_horizontal(board):
    for row in board:
        counts = {}
        
        for tower in row:
            if tower['color'] is not None:
                color = tower['color']
                if color not in counts:
                    counts[color] = 0
                counts[color] += 1
        
        if counts:
            invalid = max(counts.values()) > 1
            if invalid:
                return False
    return True

def check_vertical(board):
    transposed_board = list(zip(*board))
    return check_horizontal(transposed_board)

def is_board_valid():
    return check_horizontal(board) and check_vertical(board)

def are_colors_complete(board):
    counts = {color: 0 for color in color_choices}
    for i in range(n):
        for j in range(n):
            tower = board[i][j]
            color = tower['color']
            if color is not None:
                counts[color] += 1
    return len([val for val in counts.values() if val > 0 and val < n]) == 0

def print_board(board):
    middle = []
    top_length = 0
    for row in board:
        content = ''
        for i, col in enumerate(row):
            if i == 0:
                content += "| "
            else:
                content += " | "
            content += str(col['size'])
            color = col['color'] if col['color'] is not None else '·'
            content += ' - ' + color + ' '
            if i == len(row) - 1:
                content += " |"
        middle.append(content)
        if len(content) > top_length:
            top_length = len(content)
    top = "-" * top_length

    print(top)
    for line in middle:
        print(line)
    print(top)

valid_configurations = [
    [5, 3, 1, 2, 6, 4],
    [4, 2, 3, 1, 5, 6],
    [3, 6, 4, 1, 5, 2]
]

def place_pattern_on_board(pattern, color = 'R'):
    # print(f"Placing pattern {pattern} on board...")
    for i, num in enumerate(pattern):
        row = board[i]
        col = [tower for tower in row if tower['size'] == num][0]
        col['color'] = color

def remove_pattern_from_board(pattern):
    # print(f"Removing pattern {pattern} from board...")
    for i, num in enumerate(pattern):
        row = board[i]
        col = [tower for tower in row if tower['size'] == num][0]
        col['color'] = None

def get_edges(path):
    print(f"Path is {path}. Attempting to get next row.")
    next_row = [t['size'] for t in board[len(path)]]
    print(f"Next row is {next_row}.")
    edges = [num for num in next_row if num not in path]
    print(f"Edges = {edges}")
    return edges

def hash(pattern):
    return "|".join([str(num) for num in pattern])

def dehash(string):
    return [int(s) for s in string.split("|")]

def is_pattern_valid(pattern):
    print(f"Is board valid? {is_board_valid()}")
    place_pattern_on_board(pattern)
    is_valid = is_board_valid()
    print_board(board)
    print(f"Pattern {pattern} valid? {is_valid}")
    remove_pattern_from_board(pattern)
    return is_valid

def find_patterns(path, patterns):
    if len(path) == n:
        print(f"Pattern {path} assembled. Checking validity...")
        hashed_pattern = hash(path)
        if is_pattern_valid(path) and hashed_pattern not in patterns:
            print(f"Pattern is VALID!. Adding to list.")
            patterns.add(hashed_pattern)
        return

    for edge in get_edges(path):
        path.append(edge)
        find_patterns(path, patterns)
        path.pop()

print("Is board valid? ", is_board_valid())
print_board(board)
print("Finding valid configurations...")
find_patterns([], patterns)
print(f"DONE. {len(patterns)} valid patterns detected.")

for hashed_string in patterns:
    pattern = dehash(hashed_string)
    print(f"Pattern = {pattern}")
    place_pattern_on_board(pattern)
    print_board(board)
    remove_pattern_from_board(pattern)

print('Complete.')

print("+++++ NOW +++++")
print("Finding a combination of valid configurations that actually solves the puzzle...")
solutions = set()
color_choices = {'R', 'O', 'Y', 'G', 'B', 'P'}

def hash2(solution):
    return "\n".join([hash(pattern) for pattern in solution])

def dehash2(string):
    return [dehash(s) for s in string.split("\n")]

def get_available_color():
    first_row = board[0]
    colors_used = set([tower['color'] for tower in first_row if tower['color'] is not None])
    return list(color_choices - colors_used)

def linearize_board():
    return "\n".join(
        ["|".join(
            [t['color'] if t['color'] is not None else 'X' for t in row]
        ) for row in board]
    )

def pattern_overlaps(pattern, patterns):
    for p in patterns:
        if len(pattern) != len(p):
            raise ArgumentError("Can't determine overlap on mismatched arrays.")
        
        for i in range(len(p)):
            if p[i] == pattern[i]:
                return True

    return False

def get_patterns(attempted_patterns):
    options = []
    for h in patterns:
        pattern = dehash(h)
        if not pattern_overlaps(pattern, [dehash(p) for p in attempted_patterns]):
            options.append(pattern)
    return options

def find_solution(attempted_patterns):
    if len(attempted_patterns) == n:
        print(f"Attempted solution: {attempted_patterns}")
        h = linearize_board()
        if h not in solutions:
            print('Solution found (maybe):')
            print_board(board)
            solutions.add(h)
        return

    for pattern in get_patterns(attempted_patterns):
        place_pattern_on_board(pattern, get_available_color()[0])
        if not is_board_valid() or not are_colors_complete(board):
            remove_pattern_from_board(pattern)
            continue
        
        attempted_patterns.append(hash(pattern))
        find_solution(attempted_patterns)
        attempted_patterns.pop()
        remove_pattern_from_board(pattern)

find_solution([])
print(f"We found {len(solutions)} solution(s).")