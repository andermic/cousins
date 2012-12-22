#! /usr/bin/python

count = 0

def check_for_win(board):
    print board
    for i in range(3):
        if board[i][0] in ['X','O'] and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] in ['X','O'] and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][i] in ['X','O'] and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] in ['X','O'] and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    return None

def make_game_tree(board, moves_made):
    global count
    count += 1
    print count

    result = {'board': board, 'next_level': []}
    if check_for_win(board) != None or moves_made == 9:
        print 'WIN'
        return result

    for i in range(3):
        for j in range(3):
            if board[i][j] not in ['X','O']:
                new_board = list(board)
                new_board[i][j] = ('X' if moves_made % 2 == 0 else 'O')
                result['next_level'].append(make_game_tree(list(new_board), moves_made + 1))

    return result

def display_board(board, clear=True):
    if clear:
        system('clear')
    for row in board:
        print ' --- --- ---'
        print '|   |   |   |'
        for cell in row:
            print '| %s' % cell,
        print '|'
        print '|   |   |   |'
    print ' --- --- ---'

make_game_tree([[' ' for i in range(3)] for j in range(3)], 0)
