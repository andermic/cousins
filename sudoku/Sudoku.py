#! /usr/bin/env python

import wx
import re
from random import choice

import engine

OS = 'Windows 7'
if OS == 'MAC OSX':
    SCREEN_XSIZE = 300
    SCREEN_YSIZE = 275
    BUTTON_XSIZE = 27
    BUTTON_YSIZE = 25
    HORIZONTAL_DIVIDER_WIDTH = 5
    HORIZONTAL_DIVIDER_LENGTH = 290
    HORIZONTAL_DIVIDER1_Y = 75
    HORIZONTAL_DIVIDER2_Y = 153
    VERTICAL_DIVIDER_WIDTH = 6
    VERTICAL_DIVIDER_LENGTH = 227
    VERTICAL_DIVIDER1_X = 96
    VERTICAL_DIVIDER2_X = 195
    CLICK_DIALOG_XSIZE = 30
    CLICK_DIALOG_YSIZE = 300
    CLICK_BUTTON_XSIZE = BUTTON_XSIZE
    CLICK_BUTTON_YSIZE = BUTTON_YSIZE
    WIN_DIALOG_XSIZE = 350
    WIN_DIALOG_YSIZE = 225
    BEST_TIMES_XSIZE = 200
    BEST_TIMES_YSIZE = 150
elif OS == 'Windows 7':
    SCREEN_XSIZE = 410
    SCREEN_YSIZE = 430
    BUTTON_XSIZE = 37
    BUTTON_YSIZE = 33
    HORIZONTAL_DIVIDER_WIDTH = 5
    HORIZONTAL_DIVIDER_LENGTH = 385
    HORIZONTAL_DIVIDER1_Y = 113
    HORIZONTAL_DIVIDER2_Y = 230
    VERTICAL_DIVIDER_WIDTH = 5
    VERTICAL_DIVIDER_LENGTH = 342
    VERTICAL_DIVIDER1_X = 128
    VERTICAL_DIVIDER2_X = 260
    CLICK_DIALOG_XSIZE = 50
    CLICK_DIALOG_YSIZE = 443
    CLICK_BUTTON_XSIZE = 43
    CLICK_BUTTON_YSIZE = 40
    WIN_DIALOG_XSIZE = 400
    WIN_DIALOG_YSIZE = 300
    BEST_TIMES_XSIZE = 275
    BEST_TIMES_YSIZE = 200


class WinDialog(wx.Dialog):
    def __init__(s, parent, id, title, lines):
        wx.Dialog.__init__(s, parent, id, title, pos=(50,50), size=(WIN_DIALOG_XSIZE,WIN_DIALOG_YSIZE))
        sizer = s.CreateTextSizer('')
        ok_button = wx.Button(s, wx.ID_OK, label='OK', style = wx.OK)
        you_win = wx.StaticText(s, wx.ID_ANY, 'You win!', style=wx.ALIGN_CENTER)
        you_win.SetFont(wx.Font(35, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, u'Comic Sans MS'))
        your_time = wx.StaticText(s, wx.ID_ANY, lines[0], style=wx.ALIGN_CENTER)
        fnormal = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        your_time.SetFont(fnormal)
        prev_time = wx.StaticText(s, wx.ID_ANY, lines[1])
        prev_time.SetFont(fnormal)

        sizer.Add(you_win, 1, wx.ALIGN_CENTER)
        sizer.Add(your_time, 1, wx.ALIGN_CENTER)
        sizer.Add(prev_time, 1, wx.ALIGN_CENTER)
        sizer.Add(ok_button, 1, wx.ALIGN_CENTER)
    
        ok_button.Bind(wx.EVT_BUTTON, s.click_button)
        ok_button.Bind(wx.EVT_KEY_DOWN, s.keypress_button)
        s.SetSizer(sizer)

    def click_button(s, event):
        s.EndModal(-1)

    def keypress_button(s, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            s.click_button(event)

class BestTimesDialog(wx.Dialog):
    def __init__(s, parent, id, title, lines):
        wx.Dialog.__init__(s, parent, id, title, pos=(50,50), size=(BEST_TIMES_XSIZE,BEST_TIMES_YSIZE))
        sizer = s.CreateTextSizer('')
        ok_button = wx.Button(s, wx.ID_OK, label='OK', style=wx.OK)
        boxes = []
        for l in lines:
            boxes.append(wx.StaticText(s, wx.ID_ANY, l))
            boxes[-1].SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Courier'))
            sizer.Add(boxes[-1])
        boxes[0].SetFont(wx.Font(12,wx.DEFAULT, wx.NORMAL, wx.BOLD, False, u'Courier'))
        text = '\n'.join(lines) + '\n'

        sizer.Add(wx.StaticText(s, wx.ID_ANY, ''))
        sizer.Add(ok_button, 1, wx.ALIGN_CENTER|wx.ALL)
    
        ok_button.Bind(wx.EVT_BUTTON, s.click_button)
        ok_button.Bind(wx.EVT_KEY_DOWN, s.keypress_button)
        s.SetSizer(sizer)

    def click_button(s, event):
        s.EndModal(-1)

    def keypress_button(s, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            s.click_button(event)

class ClickDialog(wx.Dialog):
    def __init__(s, parent, id, title, p=(0,0)):
        wx.Dialog.__init__(s, parent, id, title, size=(CLICK_DIALOG_XSIZE,CLICK_DIALOG_YSIZE), pos=p)
        sizer = s.CreateTextSizer('')
        s.choices = []
        for i in range(10):
            s.choices.append(wx.Button(s, -1, str(i), size=(CLICK_BUTTON_XSIZE,CLICK_BUTTON_YSIZE), name=str(i)))
            sizer.Add(s.choices[-1])
            s.choices[-1].Bind(wx.EVT_BUTTON, s.click_button)
            s.choices[-1].Bind(wx.EVT_KEY_DOWN, s.keypress_button)
        s.choices[0].SetLabel(' ')
        s.SetSizer(sizer)

    def click_button(s, event):
        s.EndModal(int(event.GetEventObject().GetName()))

    def keypress_button(s, event):
        button = event.GetEventObject()
        pos = int(button.GetName())
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            s.click_button(event)
        elif key == wx.WXK_ESCAPE:
            s.EndModal(-1)
        elif key in [48, wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_NUMPAD0]:
            s.EndModal(0)
        elif key >= 48 and key <= 57:
            s.EndModal(key - 48)
        elif key >= wx.WXK_NUMPAD1 and key <= wx.WXK_NUMPAD9:
            s.EndModal(key - wx.WXK_NUMPAD0)
        elif key == wx.WXK_DOWN or key == wx.WXK_UP:
            s.choices[(pos + key - 316) % 10].SetFocus()
        elif key == wx.WXK_TAB:
            decr_or_incr = -1 if event.ShiftDown() else 1
            s.choices[(pos + decr_or_incr) % 10].SetFocus()
            
class MainWindow(wx.Frame):
    def __init__(s, parent, title):
        wx.Frame.__init__(s, parent, style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX, title=title, size=(SCREEN_XSIZE, SCREEN_YSIZE))
        s.status_bar = s.CreateStatusBar()
        s.timer = wx.Timer(s)

        # Set up the top menu
        new_menu = wx.Menu()
        measy = new_menu.Append(wx.ID_ANY, '&Easy\tCtrl+E', 'Start an easy sudoku')
        mmedium = new_menu.Append(wx.ID_ANY, '&Medium\tCtrl+D', 'Start a medium sudoku')
        mhard = new_menu.Append(wx.ID_ANY, '&Hard\tCtrl+H', 'Start a hard sudoku')
        mvhard = new_menu.Append(wx.ID_ANY, '&Very Hard\tCtrl+V', 'Start a very hard sudoku')
        #minsane = new_menu.Append(wx.ID_ANY, '&Insane\tCtrl+I', 'What are you... insane?')
        other_menu = wx.Menu()
        s.mst = other_menu.Append(wx.ID_ANY, '&Show Timer\tCtrl+T', 'Toggle timer visibility')
        mbt = other_menu.Append(wx.ID_ANY, '&Best Times\tCtrl+B', 'Display your best solving times for each difficulty level')
        other_menu.AppendSeparator()
        s.sas_text = ['an angel loses its wings', 'a kitten gets sad', 'the terrorists win', 'Justin Bieber grows more powerful', 'doves cry', 'the bell tolls for thee', 'eternal love becomes ephemeral', 'the world ends in 2012', 'Nazis march through Paris', 'children get coal in their stockings', 'the Empire beats the Rebels', "Pandora's Box gets opened", 'you cheat yourself', 'the Westboro Baptists celebrate', 'Tinkerbell ceases to exist', 'Iran gets a nuclear weapon', 'the next sudoku is unsolvable']
        s.msas = other_menu.Append(wx.ID_ANY, '&Solve a Square\tCtrl+S', 'When you cheat, ' + choice(s.sas_text))
        menu_bar = wx.MenuBar()
        menu_bar.Append(new_menu, '&New')
        menu_bar.Append(other_menu, '&Other')
        s.SetMenuBar(menu_bar)

        s.FONT_SIZE = 18
        s.fnormal = wx.Font(s.FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        s.funder = wx.Font(s.FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True, u'Comic Sans MS') 

        # Make and align the grid cells
        s.cells = []
        for i in range(9):
            s.cells.append([])
            for j in range(9):
                s.cells[-1].append(wx.Button(s, -1, ' ', size=(BUTTON_XSIZE,BUTTON_YSIZE), name=str(i) + str(j)))
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
        s.Bind(wx.EVT_MENU, s.click_sas, s.msas)
        for i in range(9):
            for j in range(9):
                s.cells[i][j].Bind(wx.EVT_BUTTON, s.click_cell)
                s.cells[i][j].Bind(wx.EVT_KEY_DOWN, s.keypress_cell)
        s.Bind(wx.EVT_PAINT, s.on_paint)
        s.Bind(wx.EVT_TIMER, s.second_tick, s.timer)

        s.Show()

        s.best_times = engine.get_best_times()
        s.solution = None
        s.show_timer = False

    def time_to_str(s, time):
        return '%.2dh%.2dm%.2ds' % tuple(time)

    def second_tick(s, event):
        s.frames += 1
        if s.show_timer:
            sb = s.status_bar.GetStatusText()
            if len(sb) == 0 or (len(sb) == 1 and ord(sb) == 0) or (re.match('\d+h\d\dm\d\ds$', sb) != None):
                s.status_bar.SetStatusText(s.time_to_str(s.time))
        
        if s.frames % 25 == 0:
            s.time[2] += 1
            if s.time[2] == 60:
                s.time[2] = 0
                s.time[1] += 1
                if s.time[1] == 60:
                    s.time[1] = 0
                    s.time[0] += 1

    def check_for_solution(s):
        for i in range(9):
            for j in range(9):
                if s.solution[i][j] != s.cells[i][j].GetLabel():
                    return

        lines = []
        lines.append('Your time was %s%s.' % (s.time_to_str(s.time), ', cheater' if s.cheated else ''))
        s.timer.Stop()
        best = s.best_times[s.difficulty]
        if not s.cheated and \
         (s.time[0]*10000 + s.time[1]*100 + s.time[2] < \
         best[0]*10000 + best[1]*100 + best[2]):
            lines.append('You beat the previously best time of %s!' % s.time_to_str(best))
            s.best_times[s.difficulty] = s.time
            engine.set_best_times(s.best_times)
        else:
            lines.append('Your best %stime for this difficulty is %s.' % ('HONEST ' if s.cheated else '', s.time_to_str(best)))

        win_dlg = WinDialog(s, wx.ID_ANY, ' Puzzle Completed', lines)
        win_dlg.ShowModal()
        win_dlg.Destroy()

        s.seeds = [[True for i in range(9)] for j in range(9)]
        s.solution = None

    def on_paint(s, event):
        dc = wx.PaintDC(s)
        dc.Clear()
        
        dc.SetPen(wx.Pen(wx.BLACK, HORIZONTAL_DIVIDER_WIDTH))
        dc.DrawLine(0, HORIZONTAL_DIVIDER1_Y, HORIZONTAL_DIVIDER_LENGTH, HORIZONTAL_DIVIDER1_Y)
        dc.DrawLine(0, HORIZONTAL_DIVIDER2_Y, HORIZONTAL_DIVIDER_LENGTH, HORIZONTAL_DIVIDER2_Y)
        
        dc.SetPen(wx.Pen(wx.BLACK, VERTICAL_DIVIDER_WIDTH))
        dc.DrawLine(VERTICAL_DIVIDER1_X, 0, VERTICAL_DIVIDER1_X, VERTICAL_DIVIDER_LENGTH)
        dc.DrawLine(VERTICAL_DIVIDER2_X, 0, VERTICAL_DIVIDER2_X, VERTICAL_DIVIDER_LENGTH)

    def draw_sudoku(s, difficulty):
        s.solution, seeds = engine.Sudoku().get_puzzle(difficulty)
        
        for i in range(9):
            for j in range(9):
                cell = s.cells[i][j]
                cell.SetLabel(seeds[i][j])
                if seeds[i][j] == ' ':
                    s.seeds[i][j] = False
                    cell.SetFont(s.fnormal)
                else:
                    s.seeds[i][j] = True
                    cell.SetFont(s.funder)
        s.cells[0][0].SetFocus()
        
        s.difficulty = difficulty
        s.best_times = engine.get_best_times()
        s.cheated = False
        s.time = [0,0,0]
        s.frames = 0
        s.timer.Start(40)

    def keypress_cell(s, event):
        cell = event.GetEventObject()
        pos = [int(i) for i in list(cell.GetName())]
        key = event.GetKeyCode()
        if key == 13:
            s.click_cell(event)
        elif key in [48, wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_NUMPAD0] and (not s.seeds[pos[0]][pos[1]]):
            cell.SetLabel(' ')
        elif key >= 49 and key <= 57 and (not s.seeds[pos[0]][pos[1]]):
            cell.SetLabel(str(key - 48))
            s.check_for_solution()
        elif key >= wx.WXK_NUMPAD1 and key <= wx.WXK_NUMPAD9 and (not s.seeds[pos[0]][pos[1]]):
            cell.SetLabel(str(key - wx.WXK_NUMPAD0))
            s.check_for_solution()
        elif key in [wx.WXK_LEFT, wx.WXK_UP, wx.WXK_RIGHT, wx.WXK_DOWN]:
            dir = (0 if key%2==0 else key-316, 0 if key%2==1 else key-315)
            s.cells[(pos[0]+dir[0])%9][(pos[1]+dir[1])%9].SetFocus()
        elif key == wx.WXK_TAB:
            decr_or_incr = -1 if event.ShiftDown() else 1
            s.cells[(pos[0] + (pos[1] + decr_or_incr) / 9) % 9][(pos[1] + decr_or_incr) % 9].SetFocus()

    def click_cell(s, event):
        cell = event.GetEventObject()
        loc = [int(i) for i in cell.GetName()]
        if not s.seeds[loc[0]][loc[1]]:
            pos = cell.GetPosition()
            choose_no = ClickDialog(s, -1, '', (pos[0], pos[1] + 50))
            choose_no.ShowModal()
            code = choose_no.GetReturnCode()
            if code / 10 == 0:
                if code == 0:
                    cell.SetLabel(' ')
                else:
                    cell.SetLabel(str(code))
                s.check_for_solution()
            choose_no.Destroy()

    def click_easy(s, event):
        s.diff = engine.SUDOKU_EASY
        s.draw_sudoku(s.diff)

    def click_medium(s, event):
        s.diff = engine.SUDOKU_MEDIUM
        s.draw_sudoku(s.diff)

    def click_hard(s, event):
        s.diff = engine.SUDOKU_HARD
        s.draw_sudoku(s.diff)

    def click_vhard(s, event):
        s.diff = engine.SUDOKU_VHARD
        s.draw_sudoku(s.diff)

    def click_insane(s, event):
        s.diff = engine.SUDOKU_INSANE
        s.draw_sudoku(s.diff)

    def click_st(s, event):
        s.show_timer = not s.show_timer
        if s.show_timer:
            s.mst.SetItemLabel('&Hide Timer\tCtrl+T')
        else:
            s.mst.SetItemLabel('&Show Timer\tCtrl+T')
            s.status_bar.SetStatusText('')
        
    def click_bt(s, event):
        best_text = []
        best_text.append('  Difficulty')
        best_text.append('  Easy')
        best_text.append('  Medium')
        best_text.append('  Hard')
        best_text.append('  Very Hard')
        #best_text.append('  Insane')
        largest = max([len(line) for line in best_text])
        best_text = [line + ' '*(largest-len(line) + 5) for line in best_text]
        best_text[0] += 'Time'
        best_text[1] += s.time_to_str(s.best_times[engine.SUDOKU_EASY])
        best_text[2] += s.time_to_str(s.best_times[engine.SUDOKU_MEDIUM])
        best_text[3] += s.time_to_str(s.best_times[engine.SUDOKU_HARD])
        best_text[4] += s.time_to_str(s.best_times[engine.SUDOKU_VHARD])
        #best_text[5] += s.time_to_str(s.best_times[engine.SUDOKU_INSANE])
        best_dlg = BestTimesDialog(s, wx.ID_ANY, '  Best Times', best_text)
        best_dlg.ShowModal()
        best_dlg.Destroy()

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
        s.seeds[pos[0]][pos[1]] = True
        cell.SetFont(s.funder)
        cell.SetFocus()
        s.cheated = True
        s.msas.SetHelp('When you cheat, ' + choice(s.sas_text))
        s.check_for_solution()

        
if __name__ == '__main__':
    app = wx.App(False)
    MainWindow(None, 'Sudoku Game')
    app.MainLoop()
    