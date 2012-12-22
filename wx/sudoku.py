import wx
from random import choice

EASY = 0
MEDIUM = 1
HARD = 2
VERYHARD = 3
INSANE = 4

def display(board):
	for i in range(9):
		for j in range(3):
			print ''.join([str(k) for k in board[i][j*3:j*3+3]]),
		print
		if i % 3 == 2:
			print

def check_for_doubles(test_list):
	no_empty = [i for i in test_list if i != ' ']
	if len(set(no_empty)) == len(no_empty):
		return False
	return True

def check_subsquare(board, number):
	test_list = []
	for i in range(3):
		for j in range(3):
			test_list.append(board[i + (number/3)*3][j + (number%3)*3])
	return check_for_doubles(test_list)

def check_all(board):
	for i in range(9):
		if check_for_doubles(board[i]) or \
                 check_for_doubles([board[j][i] for j in range(9)]) or \
		 check_subsquare(board, i):
			return True
	return False

def gsb_recurse(init, cur, i, j):
	if check_all(cur):
		return
	if i+j == 16:
		return cur

	j += 1
	i += j / 9
	j %= 9
	for k in range(9):
		cur = [l[:] for l in cur]
		cur[i][j] = (init[i][j] + k) % 9 
		result = gsb_recurse(init, cur, i, j)
		if result != None:
			return result

def get_solved_board():
	init = [[choice(range(9)) for i in range(9)] for j in range(9)]
	cur = [[' ' for i in range(9)] for j in range(9)]
	return [[str(i+1) for i in j] for j in gsb_recurse(init, cur, 0, -1)]

def solve(sudoku, reverse=False):
	return None

def get_sudoku(difficulty):
	global EASY, MEDIUM, HARD, VERYHARD, INSANE
	take_out_ranges = {EASY:(20,30), MEDIUM:(30,40), HARD:(40,45), VERYHARD:(45,55), INSANE:(55,60)}
	got_sudoku = False
	while not got_sudoku:
		solution = get_solved_board()
		seeds = [i[:] for i in solution]
		take_out_no = choice(range(*take_out_ranges[difficulty]))
		i = 0
		while i < take_out_no:
			r,c = choice(range(9)), choice(range(9))
			if seeds[r][c] != ' ':
				seeds[r][c] = ' '
				i += 1
		if solve(seeds, False) == solve(seeds, True):
			got_sudoku = True
	return solution, seeds

class MainWindow(wx.Frame):
	# Draw things
	def __init__(s, parent, title):
		wx.Frame.__init__(s, parent, title=title, size=(400,-1))
		s.CreateStatusBar()

		# Set up the top menu
		new_menu = wx.Menu()
		measy = new_menu.Append(wx.ID_ANY, '&Easy', 'Start an easy sudoku')
		mmedium = new_menu.Append(wx.ID_ANY, '&Medium', 'Start a medium sudoku')
		mhard = new_menu.Append(wx.ID_ANY, '&Hard', 'Start a hard sudoku')
		mvhard = new_menu.Append(wx.ID_ANY, '&Very Hard', 'Start a very hard sudoku')
		minsane = new_menu.Append(wx.ID_ANY, '&Insane', 'What are you... insane?')
		menu_bar = wx.MenuBar()
		menu_bar.Append(new_menu, '&New')
		s.SetMenuBar(menu_bar)

		# Make and align the grid cells
		s.cells = [[wx.Button(s, -1, ' ', size=(27,25), name=str(i) + str(j)) for j in range(9)] for i in range(9)]
		s.seeds = [[True for i in range(9)] for j in range(9)]
		s.grid = wx.GridSizer(9,9)
		for row in s.cells:
			for cell in row:
				s.grid.Add(cell)
		s.SetSizer(s.grid)

		# Set events
		s.Bind(wx.EVT_MENU, s.click_easy, measy)
		s.Bind(wx.EVT_MENU, s.click_medium, mmedium)
		s.Bind(wx.EVT_MENU, s.click_hard, mhard)
		s.Bind(wx.EVT_MENU, s.click_vhard, mvhard)
		s.Bind(wx.EVT_MENU, s.click_insane, minsane)
		for i in range(9):
			for j in range(9):
				s.cells[i][j].Bind(wx.EVT_BUTTON, s.click_cell)

		s.Show()

	def draw_sudoku(s, difficulty):
		solution, seeds = get_sudoku(difficulty)
		for i in range(9):
			for j in range(9):
				if seeds[i][j] == ' ':
					s.seeds[i][j] = False
				else:
					s.cells[i][j].SetLabel(seeds[i][j])
		display(seeds)

	def click_cell(s, event):
		cell = event.GetEventObject()
		pos = [int(i) for i in list(button.GetName())
		if not s.seeds[pos[0]][pos[1]]:
			print cell.GetName()

	def click_easy(s, event):
		s.draw_sudoku(EASY)

	def click_medium(s, event):
		s.draw_sudoku(MEDIUM)

	def click_hard(s, event):
		s.draw_sudoku(HARD)

	def click_vhard(s, event):
		s.draw_sudoku(VERYHARD)

	def click_insane(s, event):
		s.draw_sudoku(INSANE)

app = wx.App(False)
MainWindow(None, 'Sudoku Game')
app.MainLoop()
