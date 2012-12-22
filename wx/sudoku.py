import wx
from random import choice

def display(board):
	for i in range(9):
		for j in range(3):
			print ''.join([str(k) for k in board[i][j*3:j*3+3]]),
		print
		if i % 3 == 2:
			print

def check_for_doubles(test_list):
	no_empty = [i for i in test_list if i != '-']
	if len(set(no_empty)) == len(no_empty):
		return False
	return True

def check_subsquare(board, number):
	test_list = []
	for i in range(3):
		for j in range(3):
			test_list.append(board[i + number/3][j + number%3])
	return check_for_doubles(test_list)

def check_all(board):
	for i in range(9):
		if check_for_doubles(board[i]) or \
                 check_for_doubles([board[j][i] for j in range(9)]) or \
		 check_subsquare(board, i):
			return True
	return False

def gsb_recurse(init, cur, i, j):
	display(init)
	display(cur)
	raw_input()
	if check_all(cur):
		return
	#if i+j == 16:
	#	return cur

	j += 1
	i += j / 9
	j %= 9
	for k in range(9):
		temp = list(cur)
		temp[i][j] = (init[i][j] + k) % 9 
		result = gsb_recurse(init, temp, i, j)
		if result != None:
			return result

def get_solved_board():
	init = [[choice(range(9)) for i in range(9)] for j in range(9)]
	cur = [['-' for i in range(9)] for j in range(9)]
	return [[str(i+1) for i in range(9)] for j in gsb_recurse(init, cur, 0, -1)]

def get_sudoku(difficulty):
	init = get_solved_sudoku()

class MainWindow(wx.Frame):
	def __init__(s, parent, title):
		wx.Frame.__init__(s, parent, title=title, size=(400,-1))
		initial_tiles = [[choice(range(1,10) + ['-']) for i in range(9)] for j in range(9)]
		s.CreateStatusBar()

		# Draw everything
		#s.board = new Board(initial_tiles)
		
		s.tiles = [[wx.Button(s, -1, str(initial_tiles[i][j]), size=(27,25)) for i in range(9)] for j in range(9)]
		s.grid = wx.GridSizer(9,9)
		for row in s.tiles:
			for tile in row:
				s.grid.Add(tile)

		s.SetSizer(s.grid)
		s.Show()

"""
app = wx.App(False)
MainWindow(None, 'Sudoku Generator')
app.MainLoop()
"""
