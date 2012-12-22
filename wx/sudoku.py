import wx
from random import choice

def get_a_board():
	result = [[' ' for i in range(9)] for j in range(9)]
	

def get_sudoku():
	pass

class BoardWindow:
	def __init__(s, initial_tiles, parent):
		# Draw board
		s.tiles = [[wx.Button(parent, ) for i in range(9)] for j in range(9)]


class MainWindow(wx.Frame):
	def __init__(s, parent, title):
		wx.Frame.__init__(s, parent, title=title, size=(400,-1))
		initial_tiles = [[choice(range(1,10) + [' ']) for i in range(9)] for j in range(9)]


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

app = wx.App(False)
MainWindow(None, 'Sudoku Generator')
app.MainLoop()
