#!/usr/bin/python3
"""
Docstring
"""

board = [
    [{ 'size': 5, 'color': None}, { 'size': 3, 'color': None}, { 'size': 2, 'color': None}, { 'size': 1, 'color': None}, { 'size': 4, 'color': None}, { 'size': 6, 'color': None}],
    [{ 'size': 4, 'color': None}, { 'size': 1, 'color': None}, { 'size': 6, 'color': None}, { 'size': 2, 'color': None}, { 'size': 5, 'color': None}, { 'size': 3, 'color': None}],
    [{ 'size': 6, 'color': None}, { 'size': 5, 'color': None}, { 'size': 3, 'color': None}, { 'size': 4, 'color': None}, { 'size': 1, 'color': None}, { 'size': 2, 'color': None}],
    [{ 'size': 1, 'color': None}, { 'size': 2, 'color': None}, { 'size': 5, 'color': None}, { 'size': 3, 'color': None}, { 'size': 6, 'color': None}, { 'size': 4, 'color': None}],
    [{ 'size': 2, 'color': None}, { 'size': 4, 'color': None}, { 'size': 1, 'color': None}, { 'size': 6, 'color': None}, { 'size': 3, 'color': None}, { 'size': 5, 'color': None}],
    [{ 'size': 3, 'color': None}, { 'size': 6, 'color': None}, { 'size': 4, 'color': None}, { 'size': 5, 'color': None}, { 'size': 2, 'color': None}, { 'size': 1, 'color': None}]
]
# Find Paths

def check_horizontal(board):
    for row in board:
        counts = {}
        for tower in row:
            if tower['color'] is not None:
                color = tower['color']
                if color not in counts:
                    counts[color] = 0
                counts[color] += 1
        invalid = len(list(filter(lambda x: x > 1, counts.values()))) > 0
        if invalid:
            return False
    return True

def check_vertical(board):
    transposed_board = list(zip(*board))
    return check_horizontal(transposed_board)

def is_board_valid():
    return check_horizontal(board) and check_vertical(board)

def find_pattern():
    # 6 pieces on the board
    # 1 piece for every row and column
    available_pieces = [2, 3, 4, 5, 6]
    current_piece = 1
    current_slot = [0, 0]
    color = 'R'

    def get_next_available_slot(piece):
        next_slot = current_slot
        next_slot[1] += 1

        # If we get to the end of the row
        if next_slot[1] >= len(board):
            next_slot[1] = 0
            next_slot[0] += 1
            # If we get to the last row go back to beginning
            if next_slot[0] == len(board):
                next_slot[0] = 0

        # The spot is invalid if it's already taken or for a different piece
        if (board[next_slot[0]][next_slot[1]]['color'] is not None) or (board[next_slot[0]][next_slot[1]]['size'] != piece):
            next_slot = get_next_available_slot(piece)

        return next_slot

    while len(available_pieces) > 0:
        slot = get_next_available_slot(current_piece)
        if slot == [0,0]:
            # If we're back to 0,0 then we traversed the entire board
            break

        board[slot[0]][slot[1]]['color'] = color
        if is_board_valid():
            available_pieces = list(filter(lambda n: n != current_piece, available_pieces))
            current_piece = available_pieces.pop()
            print_board(board)
        else:
            board[slot[0]][slot[1]]['color'] = None
            slot = get_next_available_slot(current_piece)

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

# board[0][0]['color'] = 'R'
# board[1][1]['color'] = 'R'
print("Is board valid? ", is_board_valid())
find_pattern()
print_board(board)