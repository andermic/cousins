import os
import pickle
import time
from random import Random, choice, shuffle

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
UNI_DOUB_T_RGHT = u'\u2560'
UNI_DOUB_T_LEFT = u'\u2563'
UNI_DOUB_T_DOWN = u'\u2566'
UNI_DOUB_T_UP   = u'\u2569'
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

def check_for_duplicates2(test_list, elem):
    have_seen = False
    for t in test_list:
        if t == elem and elem != None:
            if have_seen == True:
                return True
            have_seen = True
    return False

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
    def __init__(s, seed=None):
        s.seed = seed
    
    def cells_to_strings(s, board):
        return [[' ' if i == None else str(i+1) for i in j] for j in board]
    
    def display(s, board):
        print UNI_DOUB_ELB_SE + UNI_DOUB_T_DOWN.join(3*[u'\u2564'.join(3*[UNI_DOUB_HORI])]) + UNI_DOUB_ELB_SW
        for i in range(3):
            for j in range(3):
                print UNI_DOUB_VERT \
                 + UNI_DOUB_VERT.join([UNI_SING_VERT.join([(str(l) if l != None else ' ') for l in board[i*3+j][k*3:k*3+3]]) for k in range(3)]) \
                 + UNI_DOUB_VERT
                if j != 2:
                    middle = UNI_SING_INTERS.join(3*[UNI_SING_HORI])
                    print u'\u255f' + u'\u256b'.join(3*[middle]) + u'\u2562'
            if i != 2:
                middle = UNI_SIDO_INTERS.join(3*[UNI_DOUB_HORI])
                print u'\u2560' + UNI_DOUB_INTERS.join(3*[middle]) + u'\u2563'
        middle = u'\u2567'.join(3*UNI_DOUB_HORI)
        print UNI_DOUB_ELB_NE + u'\u2569'.join(3*[middle]) + UNI_DOUB_ELB_NW
    
    def solve(s, init, cur, nums_available, is_fixed, i, j):
        if i == len(cur)-1 and j == len(cur[-1])-1:
            return cur
        
        j += 1
        i += j / 9
        j %= 9        
        subsq_num = i/3*3 + j/3
        
        if is_fixed[i][j]:
            return s.solve(init, cur, nums_available, is_fixed, i, j)
        
        else:
            for k in range(1, 10):           
                cand_val = (init[i][j] + k) % 9 
                
                if not (nums_available['rows'][i][cand_val] and \
                        nums_available['cols'][j][cand_val] and \
                        nums_available['subs'][subsq_num][cand_val]):
                    continue
                
                cur[i][j] = cand_val
                
                nums_available['rows'][i][cand_val] = False
                nums_available['cols'][j][cand_val] = False
                nums_available['subs'][subsq_num][cand_val] = False
                
                result = s.solve(init, cur, nums_available, is_fixed, i, j)
                if result != None:
                    return result
                
                nums_available['rows'][i][cand_val] = True
                nums_available['cols'][j][cand_val] = True
                nums_available['subs'][subsq_num][cand_val] = True
            
            cur[i][j] = None
    
    def get_solved_board(s):
        random_ = Random(s.seed)
        init = [[random_.choice(range(9)) for i in range(9)] for j in range(9)]
        cur = [[None] * 9 for i in range(9)]
        is_fixed = [[False] * 9 for i in range(9)]
        nums_available = {}
        nums_available['rows'] = [9*[True] for i in range(9)]
        nums_available['cols'] = [9*[True] for i in range(9)]
        nums_available['subs'] = [9*[True] for i in range(9)]
        return s.solve(init, cur, nums_available, is_fixed, 0, -1)
    
    def get_puzzle(s, difficulty, seed=None):
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
        
        random_ = Random(s.seed)
        got_sudoku = False
        if s.seed != None:
            start_time = time.time()
        
        count = 0
        while not got_sudoku:
            count += 1
            print count
            
            solution = s.get_solved_board()
            seeds = [i[:] for i in solution]
            is_fixed = [[True] * 9 for i in range(9)]
            
            take_out_no = random_.choice(range(*take_out_ranges[difficulty]))
            i = 0
            while i < take_out_no:
                r,c = random_.choice(range(9)), random_.choice(range(9))
                if seeds[r][c] != None:
                    seeds[r][c] = None
                    is_fixed[r][c] = False
                    i += 1
            
            cur = [i[:] for i in seeds]
            
            nums_available = {}
            nums_available['rows'] = [9*[True] for i in range(9)]
            nums_available['cols'] = [9*[True] for i in range(9)]
            nums_available['subs'] = [9*[True] for i in range(9)]
            for i in range(9):
                for j in range(9):
                    if cur[i][j] != None:
                        nums_available['rows'][i][cur[i][j]] = False
                        nums_available['cols'][j][cur[i][j]] = False
                        nums_available['subs'][i/3*3 + j/3][cur[i][j]] = False

            got_sudoku = (solution == s.solve(solution, cur, nums_available, is_fixed, 0, -1))
        
        if s.seed != None:
            print '%.3f' % (time.time() - start_time)
        
        solution = s.cells_to_strings(solution)
        seeds = s.cells_to_strings(seeds)
        return solution, seeds


class Kenken(Puzzle):
    def semigraphics1(s, cells, n, section_matrix):
        print UNI_DOUB_ELB_SE + UNI_DOUB_T_DOWN.join(n*[UNI_DOUB_HORI]) + UNI_DOUB_ELB_SW
        for i in range(n):
            vert_separators = [' ' if ((section_matrix[i][j]) == section_matrix[i][j+1]) else UNI_DOUB_VERT for j in range(n-1)]
            print UNI_DOUB_VERT + ''.join([str(cells[i][j]) + vert_separators[j] for j in range(n-1)]) + str(cells[i][n-1]) + UNI_DOUB_VERT
            if i != n-1:
                hori_separators = [' ' if (section_matrix[i][j] == section_matrix[i+1][j]) else UNI_DOUB_HORI for j in range(n)]
                print UNI_DOUB_T_RGHT + UNI_DOUB_INTERS.join(hori_separators) + UNI_DOUB_T_LEFT
        print UNI_DOUB_ELB_NE + UNI_DOUB_T_UP.join(n*[UNI_DOUB_HORI]) + UNI_DOUB_ELB_NW
        print
    
    def semigraphics2(s, cells, n, section_matrix):
        print UNI_DOUB_ELB_SE + ' '.join(n*[4*UNI_DOUB_HORI]) + UNI_DOUB_ELB_SW
        for i in range(n):
            vert_separators = [' ' if ((section_matrix[i][j]) == section_matrix[i][j+1]) else UNI_DOUB_VERT for j in range(n-1)]
            empty_line = UNI_DOUB_VERT + 4*' ' + (4*' ').join(vert_separators) + 4*' ' + UNI_DOUB_VERT
            cells_line = UNI_DOUB_VERT + ''.join([' ' + 2*str(cells[i][j]) + ' ' + vert_separators[j] for j in range(n-1)]) + ' ' + 2*str(cells[i][n-1]) + ' ' + UNI_DOUB_VERT
            print '\n'.join([empty_line, cells_line, cells_line, empty_line])
            if i != n-1:
                hori_separators = [4*' ' if (section_matrix[i][j] == section_matrix[i+1][j]) else 4*UNI_DOUB_HORI for j in range(n)]
                print ' ' + ' '.join(hori_separators) + ' '
        print UNI_DOUB_ELB_NE + ' '.join(n*[4*UNI_DOUB_HORI]) + UNI_DOUB_ELB_NW
        print
        
    def display(s, board, sg_only=False):
        cells, section_list, section_matrix, section_labels = board
        n = len(cells)
        
        SEMIGRAPHICS = s.semigraphics2
        SEMIGRAPHICS(cells, n, section_matrix)
        
        if sg_only:
            return

        for i in range(len(section_list)):
            print 'Section %d:\t%s\t%s' % (i, section_labels[i], ' '.join([str(j) for j in section_list[i]]))
        
    def get_solve_test_cases(s):
        s.test_cases = []

        # Test case 1
        
        n = 3

        section_list = []
        section_list.append([(0,0), (0,1)])
        section_list.append([(0,2)])
        section_list.append([(1,0), (2,0)])
        section_list.append([(1,1), (1,2)])
        section_list.append([(2,1), (2,2)])
        
        # TODO: Modularize this block
        section_matrix = [n*[None] for i in range(n)]
        for i in range(len(section_list)):
            for j in range(len(section_list[i])):
                r,c = section_list[i][j][0], section_list[i][j][1]
                section_matrix[r][c] = i

        section_labels = ['-1', '1', '-1', '/3', '*6']

        solution = []
        solution.append([3,2,1])
        solution.append([2,1,3])
        solution.append([1,3,2])
        
        s.test_cases.append({})
        s.test_cases[-1]['n'] = n
        s.test_cases[-1]['section_list'] = section_list
        s.test_cases[-1]['section_matrix'] = section_matrix
        s.test_cases[-1]['section_labels'] = section_labels
        s.test_cases[-1]['solution'] = solution
        
        
        # Test case 2
        
        n = 6
        
        section_list = []
        section_list.append([(0,0), (1,0)])
        section_list.append([(0,1), (0,2)])
        section_list.append([(0,3), (0,4)])
        section_list.append([(0,5), (1,5)])
        section_list.append([(1,1), (2,1)])
        section_list.append([(1,2), (2,2)])
        section_list.append([(1,3), (2,3)])
        section_list.append([(1,4), (2,4)])
        section_list.append([(2,0), (3,0), (3,1)])
        section_list.append([(2,5), (3,4), (3,5)])
        section_list.append([(3,2), (3,3)])
        section_list.append([(4,0), (4,1), (5,0)])
        section_list.append([(4,2), (4,3)])
        section_list.append([(4,4), (4,5), (5,5)])
        section_list.append([(5,1), (5,2)])
        section_list.append([(5,3), (5,4)])
        
        section_matrix = [n*[None] for i in range(n)]
        for i in range(len(section_list)):
            for j in range(len(section_list[i])):
                r,c = section_list[i][j][0], section_list[i][j][1]
                section_matrix[r][c] = i
        
        section_labels = ['-2','-1','*10','/3','+11','+7','-5','/3','+9','*120','+3','+7','-1','+13','/3','-1']
        
        solution = []
        solution.append([6,3,4,5,2,1])
        solution.append([4,5,2,6,1,3])
        solution.append([2,6,5,1,3,4])
        solution.append([3,4,1,2,5,6])
        solution.append([5,1,3,4,6,2])
        solution.append([1,2,6,3,4,5])
        
        s.test_cases.append({})
        s.test_cases[-1]['n'] = n
        s.test_cases[-1]['section_list'] = section_list
        s.test_cases[-1]['section_matrix'] = section_matrix
        s.test_cases[-1]['section_labels'] = section_labels
        s.test_cases[-1]['solution'] = solution
        
    def run_solve_test_cases(s):
        s.get_solve_test_cases()
        
        for i in range(len(s.test_cases)):
            cur_list = s.test_cases[i]['section_list']
            cur_matrix = s.test_cases[i]['section_matrix']
            cur_labels = s.test_cases[i]['section_labels']
            cur_solution = s.test_cases[i]['solution']
            cur_n = len(cur_matrix)
            
            print 'TEST CASE %d\n' % (i+1)
            
            init = cur_n*[cur_n*[-1]]
            cur = [cur_n*[None] for i in range(cur_n)]
            found_solution = s.solve(init, cur, cur_n, cur_list, cur_matrix, cur_labels, 0, -1)
            print 'Solution found:'
            s.display((found_solution, cur_list, cur_matrix, cur_labels), True)
            print
            
            print 'Actual solution:'
            s.display((cur_solution, cur_list, cur_matrix, cur_labels), True)
            print
            
            if found_solution == cur_solution:
                print 'Puzzle was solved correctly!'
            else:
                print 'Puzzle was NOT solved correctly'
            print
            print
    
    # TODO: Strongly consider solving section-by-section rather than row-by-row.
    # Would likely make the average search space orders of magnitude smaller.
    def solve(s, init, cur, n, section_list, section_matrix, section_labels, i, j):
        #s.display((cur, section_list, section_matrix, section_labels), True)
        print cur
        #raw_input()
        print
        
        # TODO: Consider optimizing using check_for_duplicates2
        if check_for_duplicates(cur[i]) or \
         check_for_duplicates([cur[k][j] for k in range(n)]):
            return
        if i == n-1 and j == n-1:
            return cur
        
        if not(section_list == [] or j == -1):
            section_num = section_matrix[i][j]
            cur_label = section_labels[section_num]
            
            if cur_label[0] in ['+','-','*','/']:
                operator, section_result = cur_label[0], int(cur_label[1:])
            else:
                operator, section_result = '', int(cur_label)
            
            cur_section_list = section_list[section_num]
            vals = [cur[sl[0]][sl[1]] for sl in section_list[section_num]]
            vals = [str(v) for v in vals if v != None]
            
            # TODO: Consider optimizing for speed by memoizing section sub-totals
            if operator in ['+','*']:
                total = eval(operator.join(vals))
                if total > section_result:
                    return
                if len(vals) == len(cur_section_list) and total != section_result:
                    return
            elif operator in ['-','/']:
                if len(vals) == 2:
                    vals.sort(key=lambda x: str(x))
                    if eval(vals[1] + operator + vals[0]) != section_result:
                        return
            elif operator == '':
                if int(vals[0]) != section_result:
                    return
        
        j += 1
        i += j / n
        j %= n
        
        for k in range(1, n + 1):
            cur[i][j] = (init[i][j] + k) % n + 1
            result = s.solve(init, cur, n, section_list, section_matrix, section_labels, i, j)
            if result != None:
                return result
            cur[i][j] = None
    
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
        cur = n*[n*[None]]
        init_section_matrix = n*[[None]]
        cells = s.solve(init, cur, n, [], init_section_matrix, [], 0, -1)
        
        # TODO: Put the logic in this block into get_sections (?),
        #  or maybe change name of get_sections to get_section_locs.
        section_sizes = []
        while sum(section_sizes) != n**2:
            if sum(section_sizes) < n**2:
                section_sizes.append(choice(range(1,n)))
            else:
                section_sizes.pop()
        section_sizes.sort(reverse=True)
        
        section_list, section_matrix = s.get_sections([], init_section_matrix, n, section_sizes)
        
        section_labels = []
        for cur_section in section_list:
            cell_vals = sorted([cells[i[0]][i[1]] for i in cur_section], reverse=True)
            
            if len(cell_vals) > 2:
                operator_candidates = ['+','*']
            elif len(cell_vals) == 2:
                operator_candidates = ['+','-','*']
                if cell_vals[0] % cell_vals[1] == 0:
                    operator_candidates.append('/')
            elif len(cell_vals) == 1:
                operator_candidates = ['']
            
            cur_operator = choice(operator_candidates)
            section_labels.append(cur_operator + str(eval(cur_operator.join([str(i) for i in cell_vals]))))
            
        return cells, section_list, section_matrix, section_labels
    
    #TODO: Finish implementing. Ensure puzzle has a unique solution.
    def get_puzzle(s, difficulty):
        got_kenken = False
        
        count = 0
        while not got_kenken:
            count += 1
            print count
            
            cells, section_list, section_matrix, section_labels = s.get_solved_board(difficulty)            
            
            got_kenken = (solution == s.solve(solution, seeds, is_fixed, 0, -1))
        
        solution = s.cells_to_strings(solution)
        seeds = s.cells_to_strings(seeds)
        return solution, seeds
    