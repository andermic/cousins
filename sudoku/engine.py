import os
import pickle
from random import choice, shuffle

SUDOKU_DEBUG  = -1
SUDOKU_EASY   = 0
SUDOKU_MEDIUM = 1
SUDOKU_HARD   = 2
SUDOKU_VHARD  = 3
SUDOKU_INSANE = 4

# See http://en.wikipedia.org/wiki/Box-drawing_character
UNI_SING_HORI   = u'\u2500'
UNI_SING_VERT   = u'\u2502'
UNI_SING_ELB_SE = u'\u250c'
UNI_SING_ELB_SW = u'\u2510'
UNI_SING_ELB_NE = u'\u2514'
UNI_SING_ELB_NW = u'\u2518'
UNI_SING_T_RGHT = u'\u251c'
UNI_SING_T_LEFT = u'\u2514'
UNI_SING_T_DOWN = u'\u252c'
UNI_SING_T_UP   = u'\u2534'
UNI_SING_INTERS = u'\u253c'
UNI_DOUB_HORI   = u'\u2550'
UNI_DOUB_VERT   = u'\u2551'
UNI_DOUB_ELB_SE = u'\u2554'
UNI_DOUB_ELB_SW = u'\u2557'
UNI_DOUB_ELB_NE = u'\u255a'
UNI_DOUB_ELB_NW = u'\u255d'
UNI_DOUB_T_RGHT = u'\u255e'
UNI_DOUB_T_LEFT = u'\u2561'
UNI_DOUB_T_DOWN = u'\u2565'
UNI_DOUB_T_UP   = u'\u2568'
UNI_SIDO_INTERS = u'\u256a'
UNI_DOUB_INTERS = u'\u256c'

HS_FILE_NAME = 'best_times.txt'

up = lambda x,n: (x[0]-1,x[1]) if x[0]!=0 else None
down = lambda x,n: (x[0]+1,x[1]) if x[0]!=n else None
left = lambda x,n: (x[0],x[1]-1) if x[1]!=0 else None
right = lambda x,n: (x[0],x[1]+1) if x[1]!=n else None

def check_for_duplicates(test_list):
    no_empty = [i for i in test_list if i != None]
    if len(set(no_empty)) == len(no_empty):
        return False
    return True

def encrypt_decrypt(str):
    return ''.join([chr((ord(i) + 128)%256) for i in str])[::-1]

def set_best_times(times):
    times = pickle.dumps(times)
    times = encrypt_decrypt(times)
    open(HS_FILE_NAME, 'w').write(times)

def get_best_times():
    if HS_FILE_NAME not in os.listdir('.'):
        result = {}
        result[SUDOKU_EASY]   = [99,59,59]
        result[SUDOKU_MEDIUM] = [99,59,59]
        result[SUDOKU_HARD]   = [99,59,59]
        result[SUDOKU_VHARD]  = [99,59,59]
        result[SUDOKU_INSANE] = [99,59,59]
        set_best_times(result)
        return result
    result = open(HS_FILE_NAME, 'r').read()
    return pickle.loads(encrypt_decrypt(result))


class Puzzle:
    def display(s, *params):
        pass
    
    def solve(s, *params):
        pass
    
    def get_puzzle(s, *params):
        pass


class Sudoku(Puzzle):
    def cells_to_strings(s, board):
        return [[' ' if i == None else str(i+1) for i in j] for j in board]
    
    def display(s, board):
        print UNI_DOUB_ELB_SE + u'\u2566'.join(3*[u'\u2564'.join(3*[UNI_DOUB_HORI])]) + u'\u2557'
        for i in range(3):
            for j in range(3):
                print UNI_DOUB_VERT \
                 + UNI_DOUB_VERT.join([UNI_SING_VERT.join([l for l in board[i*3+j][k*3:k*3+3]]) for k in range(3)]) \
                 + UNI_DOUB_VERT
                if j != 2:
                    middle = UNI_SING_INTERS.join(3*[UNI_SING_HORI])
                    print u'\u255f' + u'\u256b'.join(3*[middle]) + u'\u2562'
            if i != 2:
                middle = UNI_SIDO_INTERS.join(3*[UNI_DOUB_HORI])
                print u'\u2560' + UNI_DOUB_INTERS.join(3*[middle]) + u'\u2563'
        middle = u'\u2567'.join(3*UNI_DOUB_HORI)
        print UNI_DOUB_ELB_NE + u'\u2569'.join(3*[middle]) + UNI_DOUB_ELB_NW
    
    def check_subsquare(s, board, number):
        test_list = []
        for i in range(3):
            for j in range(3):
                test_list.append(board[i + (number/3)*3][j + (number%3)*3])
        return check_for_duplicates(test_list)
    
    def check_all(s, board):
        for i in range(9):
            if check_for_duplicates(board[i]) or \
             check_for_duplicates([board[j][i] for j in range(9)]) or \
             s.check_subsquare(board, i):
                return True
        return False
    
    def solve(s, init, cur, is_fixed, i, j):
        if check_for_duplicates(cur[i]) or \
         check_for_duplicates([cur[k][j] for k in range(9)]) or \
         s.check_subsquare(cur, i/3*3 + j/3):
            return
        if i == len(cur)-1 and j == len(cur[-1])-1:
            return cur
        
        j += 1
        i += j / 9
        j %= 9
        
        for k in range(9 if is_fixed[i][j] else 1, 10):
            cur = [l[:] for l in cur]
            cur[i][j] = (init[i][j] + k) % 9 
            result = s.solve(init, cur, is_fixed, i, j)
            if result != None:
                return result
    
    def get_solved_board(s):
        init = [[choice(range(9)) for i in range(9)] for j in range(9)]
        cur = [[None] * 9 for i in range(9)]
        is_fixed = [[False] * 9 for i in range(9)]
        return s.solve(init, cur, is_fixed, 0, -1)
    
    def get_puzzle(s, difficulty):
        global SUDOKU_DEBUG
        global SUDOKU_EASY
        global SUDOKU_MEDIUM
        global SUDOKU_HARD
        global SUDOKU_VHARD
        global SUDOKU_INSANE
        
        take_out_ranges = {}
        take_out_ranges[SUDOKU_DEBUG] = (1,2)
        take_out_ranges[SUDOKU_EASY] = (20,30)
        take_out_ranges[SUDOKU_MEDIUM] = (30,40)
        take_out_ranges[SUDOKU_HARD] = (40,45)
        take_out_ranges[SUDOKU_VHARD] = (45,55)
        take_out_ranges[SUDOKU_INSANE] = (55,60)
        
        got_sudoku = False
        
        count = 0
        while not got_sudoku:
            count += 1
            print count
            
            solution = s.get_solved_board()
            seeds = [i[:] for i in solution]
            is_fixed = [[True] * 9 for i in range(9)]
            
            take_out_no = choice(range(*take_out_ranges[difficulty]))
            i = 0
            while i < take_out_no:
                r,c = choice(range(9)), choice(range(9))
                if seeds[r][c] != None:
                    seeds[r][c] = None
                    is_fixed[r][c] = False
                    i += 1
            
            got_sudoku = (solution == s.solve(solution, seeds, is_fixed, 0, -1))
        
        solution = s.cells_to_strings(solution)
        seeds = s.cells_to_strings(seeds)
        return solution, seeds


class Kenken(Puzzle):
    def display(s, board):
        pass
    
    def solve(s, init, cur, n, section_list, section_matrix, i, j):
        if check_for_duplicates(cur[i]) or \
         check_for_duplicates([cur[k][j] for k in range(n)]):
            return
        if i == n-1 and j == n-1:
            return cur
        
        # TODO: If latest cell belongs to a section check section constraint
        # Can backtrack on * and + as soon as current prod/sum goes over expected total
        
        j += 1
        i += j / n
        j %= n
        
        for k in range(1, n + 1):
            cur = [l[:] for l in cur]
            cur[i][j] = (init[i][j] + k) % n + 1
            result = s.solve(init, cur, n, section_list, section_matrix, i, j)
            if result != None:
                return result
    
    def get_sections(s, cur_section_list, cur_section_matrix, n, section_sizes):
        unassigned = [(i,j) for i in range(n) for j in range(n) if cur_section_matrix[i][j] == None]
        if len(unassigned) == 0:
            return cur_section_list, cur_section_matrix
        
        cur_section_list = [i[:] for i in cur_section_list]
        cur_section_matrix = [i[:] for i in cur_section_matrix]
        
        if len(cur_section_list) == 0 or (len(cur_section_list[-1]) == section_sizes[len(cur_section_list)-1]):
            cur_section_list.append([])
            cur_cell_candidates = [choice(unassigned)]          
        else:
            last_cell = cur_section_list[-1][-1]
            cur_cell_candidates = [i(last_cell, n) for i in [up, down, left, right]]
            cur_cell_candidates = [i for i in cur_cell_candidates if (i != None) and (i in unassigned)]
            shuffle(cur_cell_candidates)

        for cur_cell in cur_cell_candidates:
            cur_section_list[-1].append(cur_cell)
            cur_section_matrix[cur_cell[0]][cur_cell[1]] = len(cur_section_list) - 1
            result = s.get_sections(cur_section_list, cur_section_matrix, n, section_sizes)
            if result != None:
                return result
            cur_section_list[-1].pop()
            cur_section_matrix[cur_cell[0]][cur_cell[1]] = None
    
    def get_solved_board(s, n):
        init = [[choice(range(n)) for i in range(n)] for j in range(n)]
        cur = [[None] * n for i in range(n)]        
        init_section_list = []
        init_section_matrix = [[None] * n for i in range(n)]
        cells = s.solve(init, cur, n, init_section_list, init_section_matrix, 0, -1)
        
        # TODO: Put the logic in this block into get_sections (?),
        #  or maybe change name of get_sections to get_section_locs.
        section_sizes = []
        while sum(section_sizes) != n**2:
            if sum(section_sizes) < n**2:
                section_sizes.append(choice(range(1,n)))
            else:
                section_sizes.pop()
        section_sizes.sort(reverse=True)
        
        section_list, section_matrix = s.get_sections(init_section_list, init_section_matrix, n, section_sizes)
        
        section_labels = []
        for cur_section in section_list:
            cell_vals = sorted([cells[i[0]][i[1]] for i in cur_section], reverse=True)
            
            if len(cell_vals) > 2:
                operator_candidates = ['+','*']
            elif len(cell_vals) == 2:
                operator_candidates = ['+','-','*']
                if cell_vals[1] % cell_vals[0] == 0:
                    operator_candidates.append('/')
            elif len(cell_vals) == 1:
                operator_candidates = ['']
            
            cur_operator = choice(operator_candidates)
            section_labels.append(cur_operator + str(eval(cur_operator.join([str(i) for i in cell_vals]))))
            
        return cells, section_list, section_matrix, section_labels

    def get_puzzle(s, difficulty):
        pass
