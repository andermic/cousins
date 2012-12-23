#! /usr/bin/env python

import wx
import os
import pickle
import re
from random import choice

DEBUG = -1
EASY = 0
MEDIUM = 1
HARD = 2
VERYHARD = 3
INSANE = 4
HS_FILE_NAME = 'best_times.txt'

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
	if check_for_doubles(cur[i]) or \
         check_for_doubles([cur[k][j] for k in range(9)]) or \
         check_subsquare(cur, i/3*3 + j/3):
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

def solve(cur, i, j, rev=False):
	if check_for_doubles(cur[i]) or \
         check_for_doubles([cur[k][j] for k in range(9)]) or \
         check_subsquare(cur, i/3*3 + j/3):
		return
	if i+j == 16:
		return cur

	while True:
		j += 1
		i += j / 9
		j %= 9
		try:
			if cur[i][j] == ' ':
				break
		except:
			return cur 

	for k in (range(1,10)[::-1] if rev else range(1,10)):
		cur = [l[:] for l in cur]
		cur[i][j] = str(k)
		result = solve(cur, i, j, rev)
		if result != None:
			return result 

def get_sudoku(difficulty):
	global DEBUG, EASY, MEDIUM, HARD, VERYHARD, INSANE
	take_out_ranges = {DEBUG:(1,2), EASY:(20,30), MEDIUM:(30,40), HARD:(40,45), VERYHARD:(45,55), INSANE:(55,60)}
	got_sudoku = False
	
	count = 0
	while not got_sudoku:
		count += 1
		print count

		solution = get_solved_board()
		seeds = [i[:] for i in solution]
		take_out_no = choice(range(*take_out_ranges[difficulty]))
		i = 0
		while i < take_out_no:
			r,c = choice(range(9)), choice(range(9))
			if seeds[r][c] != ' ':
				seeds[r][c] = ' '
				i += 1
		if solve(seeds, 0, -1, False) == solve(seeds, 0, -1, True):
			got_sudoku = True
	return solution, seeds

def encrypt_decrypt(str):
	return ''.join([chr((ord(i) + 128)%256) for i in str])[::-1]

def store_best_times(times):
	times = pickle.dumps(times)
	times = encrypt_decrypt(times)
	open(HS_FILE_NAME, 'w').write(times)

def get_best_times():
	if HS_FILE_NAME not in os.listdir('.'):
		result = {}
		result['EASY'] = [99,59,59]
		result['MEDIUM'] = [99,59,59]
		result['HARD'] = [99,59,59]
		result['VHARD'] = [99,59,59]
		result['INSANE'] = [99,59,59]
		store_best_times(result)
		return result

	result = open(HS_FILE_NAME, 'r').read()
	return pickle.loads(encrypt_decrypt(result))

class ClickDialog(wx.Dialog):
	def __init__(s, parent, id, title, p=(0,0)):
		wx.Dialog.__init__(s, parent, id, title, size=(30,275), pos=p)
		sizer = s.CreateTextSizer('')
		s.choices = []
		for i in range(1,10):
			s.choices.append(wx.Button(s, -1, str(i), size=(27,25), name=str(i)))
			sizer.Add(s.choices[-1])
			s.choices[-1].Bind(wx.EVT_BUTTON, s.click_button)
			s.choices[-1].Bind(wx.EVT_KEY_DOWN, s.keypress_button)
		s.SetSizer(sizer)

	def click_button(s, event):
		s.EndModal(int(event.GetEventObject().GetName()))

	def keypress_button(s, event):
		button = event.GetEventObject()
		pos = int(button.GetName()) - 1
		key = event.GetKeyCode()
		if key == 13:
			s.click_button(event)
		if key >= 49 and key <= 57:
			s.EndModal(int(key - 48))
		elif key == 315 or key == 317:
			s.choices[(pos + key - 316)%9].SetFocus()

class MainWindow(wx.Frame):
	def __init__(s, parent, title):
		wx.Frame.__init__(s, parent, style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER, title=title, size=(300,275))
		s.status_bar = s.CreateStatusBar()
		s.timer = wx.Timer(s)

		# Set up the top menu
		new_menu = wx.Menu()
		measy = new_menu.Append(wx.ID_ANY, '&Easy', 'Start an easy sudoku')
		mmedium = new_menu.Append(wx.ID_ANY, '&Medium', 'Start a medium sudoku')
		mhard = new_menu.Append(wx.ID_ANY, '&Hard', 'Start a hard sudoku')
		mvhard = new_menu.Append(wx.ID_ANY, '&Very Hard', 'Start a very hard sudoku')
		#minsane = new_menu.Append(wx.ID_ANY, '&Insane', 'What are you... insane?')
		other_menu = wx.Menu()
		s.mst = other_menu.Append(wx.ID_ANY, '&Show Timer', 'Toggle timer visibility')
		mbt = other_menu.Append(wx.ID_ANY, '&Best Times', 'Display your best solving times for each difficulty level')
		other_menu.AppendSeparator()
		sas_text = choice(['an angel loses its wings', 'a kitten gets sad', 'the terrorists win', 'Justin Bieber grows stronger'])
		msas = other_menu.Append(wx.ID_ANY, '&Solve A Square', 'When you cheat, %s' % sas_text)
		menu_bar = wx.MenuBar()
		menu_bar.Append(new_menu, '&New')
		menu_bar.Append(other_menu, '&Other')
		s.SetMenuBar(menu_bar)

		s.FONT_SIZE = 18
		s.fnormal = wx.Font(s.FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
		s.fbold = wx.Font(s.FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True, u'Comic Sans MS') 

		# Make and align the grid cells
		s.cells = []
		for i in range(9):
			s.cells.append([])
			for j in range(9):
				s.cells[-1].append(wx.Button(s, -1, ' ', size=(27,25), name=str(i) + str(j)))
				s.cells[i][j].SetFont(s.fnormal)
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
		#s.Bind(wx.EVT_MENU, s.click_insane, minsane)
		s.Bind(wx.EVT_MENU, s.click_st, s.mst)
		s.Bind(wx.EVT_MENU, s.click_bt, mbt)
		s.Bind(wx.EVT_MENU, s.click_sas, msas)
		for i in range(9):
			for j in range(9):
				s.cells[i][j].Bind(wx.EVT_BUTTON, s.click_cell)
				s.cells[i][j].Bind(wx.EVT_KEY_DOWN, s.keypress_cell)
		s.Bind(wx.EVT_PAINT, s.on_paint)
		s.Bind(wx.EVT_TIMER, s.second_tick, s.timer)

		s.Show()

		s.best_times = get_best_times()
		s.solution = None
		s.show_timer = False

	def second_tick(s, event):
		s.time[2] += 1
		if s.time[2] == 60:
			s.time[2] = 0
			s.time[1] += 1
			if s.time[1] == 60:
				s.time[1] = 0
				s.time[0] += 1
		if s.show_timer:
			sb = s.status_bar.GetStatusText()
			if (len(sb) == 1 and ord(sb) == 0) or (re.match('\d+h\d\dm\d\ds$', sb) != None):
				s.status_bar.SetStatusText('%dh%.2dm%.2ds' % tuple(s.time))

	def check_for_solution(s):
		for i in range(9):
			for j in range(9):
				if s.solution[i][j] != s.cells[i][j].GetLabel():
					return

		print 'solution'

	def on_paint(s, event):
		dc = wx.PaintDC(s)
		dc.Clear()
		dc.SetPen(wx.Pen(wx.BLACK, 5))
		dc.DrawLine(0, 75, 290, 75)
		dc.DrawLine(0, 153, 290, 153)

		dc.SetPen(wx.Pen(wx.BLACK, 6))
		dc.DrawLine(96, 0, 96, 227)
		dc.DrawLine(195, 0, 195, 227)

	def draw_sudoku(s, difficulty):
		s.solution, seeds = get_sudoku(difficulty)
		for i in range(9):
			for j in range(9):
				cell = s.cells[i][j]
				cell.SetLabel(seeds[i][j])
				if seeds[i][j] == ' ':
					s.seeds[i][j] = False
					cell.SetFont(s.fnormal)
				else:
					s.seeds[i][j] = True
					cell.SetFont(s.fbold)
		s.best_times = get_best_times()
		s.save_best_time = True
		s.time = [0,0,0]
		s.timer.Start(1000)

	def keypress_cell(s, event):
		cell = event.GetEventObject()
		pos = [int(i) for i in list(cell.GetName())]
		key = event.GetKeyCode()
		if key == 13:
			s.click_cell(event)
		elif key >= 49 and key <= 57 and (not s.seeds[pos[0]][pos[1]]):
			cell.SetLabel(str(key - 48))
			s.check_for_solution()
		elif key >= 314 and key <= 317:
			dir = (0 if key%2==0 else key-316, 0 if key%2==1 else key-315)
			s.cells[(pos[0]+dir[0])%9][(pos[1]+dir[1])%9].SetFocus()

	def click_cell(s, event):
		cell = event.GetEventObject()
		loc = [int(i) for i in cell.GetName()]
		if not s.seeds[loc[0]][loc[1]]:
			pos = cell.GetPosition()
			choose_no = ClickDialog(s, -1, '', (pos[0], pos[1] + 50))
			choose_no.ShowModal()
			if choose_no.GetReturnCode() / 10 == 0:
				cell.SetLabel(str(choose_no.GetReturnCode()))
				s.check_for_solution()
			choose_no.Destroy()

	def click_easy(s, event):
		s.diff = EASY
		s.draw_sudoku(EASY)

	def click_medium(s, event):
		s.diff = MEDIUM
		s.draw_sudoku(MEDIUM)

	def click_hard(s, event):
		s.diff = HARD
		s.draw_sudoku(HARD)

	def click_vhard(s, event):
		s.diff = VHARD
		s.draw_sudoku(VERYHARD)

	def click_insane(s, event):
		s.diff = INSANE
		s.draw_sudoku(INSANE)

	def click_st(s, event):
		s.show_timer = not s.show_timer
		if s.show_timer:
			s.mst.SetItemLabel('Hide Timer')
		else:
			s.status_bar.SetStatusText(chr(0))
			s.mst.SetItemLabel('Show Timer')
		

	def click_bt(s, event):
		print 'click_bt'

	def click_sas(s, event):
		if s.solution == None:
			return
		unsolved = []
		for i in range(9):
			for j in range(9):
				cell = s.cells[i][j]
				if cell.GetLabel() == ' ':
					unsolved.append(cell.GetName())
		pos = [int(i) for i in list(choice(unsolved))]
		cell = s.cells[pos[0]][pos[1]]
		cell.SetLabel(s.solution[pos[0]][pos[1]])
		cell.SetFocus()
		s.check_for_solution()

app = wx.App(False)
MainWindow(None, 'Sudoku Game')
app.MainLoop()
