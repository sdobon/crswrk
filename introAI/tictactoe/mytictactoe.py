import copy

def end(board):
    threes = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
    for each in threes:
        total = board[each[0]-1] + board[each[1]-1] + board[each[2]-1]
        if total == -3:
            return "O"
        elif total == 3:
            return "X"
    if not 0 in board:
        return "DRAW"
    return None

def get_score(board, mysymbol):
    if end(board) == mysymbol:
        return 5
    if end(board) == "DRAW":
        return 0
    else:
        return -5

def find_moves(board, mysymbol):
    moves = []
    for i in range(len(board)):
        if board[i] == 0:
            append = copy.copy(board)
            if mysymbol == "X":
                append[i] = 1
            else:
                append[i] = -1
            moves.append(append)
    return moves


def minimax(board, mysymbol, whos_turn):
    if end(board):
        return get_score(board, mysymbol)

    if mysymbol == "X":
        opponent = "O"
    else:
        opponent = "X"

    if whos_turn == mysymbol:  #maximizing
        moves = find_moves(board, mysymbol)
        scores = []
        for move in moves:
            score = minimax(move, mysymbol, opponent)
            scores.append(score)
            if score == 5:  # alpha beta pruning step
                break
        return max(scores)

    if whos_turn == opponent:  #minimizing
        moves = find_moves(board, opponent)
        scores = []
        for move in moves:
            score = minimax(move, mysymbol, mysymbol)
            scores.append(score)
            if score == -5:  # alpha beta pruning step
                break
        return min(scores)



def mymove(board,mysymbol):
    print "Board as seen by the machine:",
    print board
    print "The machine is playing:",
    print mysymbol
    # return int(raw_input("Machine? "))

    if mysymbol == "X":
        opponent = "O"
    else:
        opponent = "X"

    moves = find_moves(board, mysymbol)
    scores = []
    for move in moves:
        score = minimax(move, mysymbol, opponent)
        scores.append(score)
        if score == 5:  # alpha beta pruning step
            break
    chosen_move_index = scores.index(max(scores))
    for i in range(10):
        if board[i] != moves[chosen_move_index][i]:
            return i + 1
