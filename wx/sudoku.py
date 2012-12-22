import wx
from random import choice

class BoardWindow()
	def __init__(s, initial_tiles):
		# Draw board
		s.tiles = initial_tiles


class MainWindow(wx.Frame)
	def __init__(s):
		initial_tiles = [[choice(range(1,10) for i in range(9)] for j in range(9)]

		# Draw everything
		s.board = new Board(initial_tiles)

app = wx.App(False)
MainWindow(None, 'Sudoku Application')
app.MainLoop()
