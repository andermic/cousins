#! /usr/bin/python

from os import system

count = 0
boards = []

class TreeNode:
	def __init__(s, board):
		s.board = board
		s.children = []
		s.winner = None
		
	def add_child(s, node):
		s.children.append(node)

def check_for_win(board):
    for i in range(3):
        if board[i][0] != None and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != None and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][i] != None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != None and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    return None

def in_reflect_rotate(board):
    global boards

    temp = [row[:] for row in board]
    for reflect in [False, True]:
        if reflect:
            temp[0][1], temp[1][0] = temp[1][0], temp[0][1]
            temp[0][2], temp[2][0] = temp[2][0], temp[0][2]
            temp[1][2], temp[2][1] = temp[2][1], temp[1][2]
        # Rotate
        for i in range(4):
            swap = temp[0][1], temp[0][2]
            temp[0][1], temp[0][2] = temp[1][0], temp[0][0]
            temp[1][0], temp[0][0] = temp[2][1], temp[2][0]
            temp[2][1], temp[2][0] = temp[1][2], temp[2][2]
            temp[1][2], temp[2][2] = swap
            if temp in boards:
                return True
    return False

def display(board, clear=True):
    if clear:
        system('clear')
    for row in board:
        print ' --- --- ---'
        print '|   |   |   |'
        for cell in row:
            print '| %s' % (' ' if cell == None else ('X' if cell else 'O')),
        print '|'
        print '|   |   |   |'
    print ' --- --- ---'

def make_game_tree(board, moves_made):
    global count, boards
    count += 1
    print count
    result = TreeNode(board)
    win_status = check_for_win(board)
    if win_status != None or moves_made == 9:
        result.winner = win_status
        return result

    turn = (moves_made % 2 == 0)
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                new_board = [row[:] for row in board]
                new_board[i][j] = turn
                #if not in_reflect_rotate(new_board):
                #if child != None:
                if new_board not in boards:
                    child = make_game_tree(new_board, moves_made + 1)
                    result.add_child(child)
                    boards.append(new_board)
                #display(new_board, False)
                #print
                #raw_input()

    winners = [node.winner for node in result.children]
    #if winners == []:
    #    return None
    #display(result.board,False)
    #print winners
    result.winner = not turn
    if None in winners:
        result.winner = None
    if turn in winners:
        result.winner = turn
    #print result.winner
    #print
    #raw_input()

    return result

tree = make_game_tree([[None for i in range(3)] for j in range(3)], 0)