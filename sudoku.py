import random

class Sudoku(object):

    def __init__(self, uc = 3):
        self.unit_cell = uc
        self.length = uc ** 2
        self.board = []
        self.squares = []
        self.unused = []
        self.h_rows = []
        self.v_rows = []
        self.generate_board()
        self.print_board()

    def generate_board(self):
        for i in range(self.length):
            # generate list of numbers in random order
            arr = range(1, self.length +1)
            random.shuffle(arr)
            self.unused.append(arr)
            # generate empty h_rows, v_rows (columns), and squares
            self.h_rows.append([0] * self.length)
            self.v_rows.append([0] * self.length)
            self.squares.append([0] * self.length)
        # main seed function
        # go through board cell by cell
        restart_row = True
        loop_safety = 0
        while(restart_row):
            if(loop_safety>1000):
                return 1
            self.shuffle_unused()
            restart_row = False
            for row in range(self.length):
                if(restart_row):
                    break
                restart = True
                temp_arr = list(self.unused[row])
                safety = 0
                self.h_rows[row] = [0] * self.length
                while restart:
                    if(safety > 100):
                        print("safety exit - never going to happen")
                        print("FAILED ROW: {}".format(row))
                        # restart = False
                        restart_row = True
                        break
                        # return 1
                    restart = False
                    for col in range(self.length):
                        for num in temp_arr:
                            self.h_rows[row][col] = 0
                            self.update_column(col)
                            self.update_square(row, col)
                            if(self.check_col(num, self.v_rows[col])):
                                continue
                            if(self.check_square(num, row, col)):
                                continue
                            self.h_rows[row][col] = num
                            temp_arr.remove(num)
                            self.update_column(col)
                            self.update_square(row, col)
                            break
                    if(0 in self.h_rows[row]):
                        index = row
                        for r in range(index):
                            print("ROW {}:  {}\t{}\t{}".format(r, self.h_rows[r][0:3],self.h_rows[r][3:6],self.h_rows[r][6:]))
                            print("")
                        temp_arr = list(self.unused[row])
                        random.shuffle(temp_arr)
                        restart = True
                        safety += 1
        self.board = self.h_rows
        return 0

    def check_col(self, test_num, col):
        return test_num in col

    def check_row(self, test_num, row):
        return test_num in row

    def update_column(self, col):
        self.v_rows[col] = []
        for i in range(self.length):
            self.v_rows[col].append(self.h_rows[i][col])

    def update_all_columns(self):
        for col in range(self.length):
            self.v_rows[col] = []
            for row in range(self.length):
                self.v_rows[col].append(self.h_rows[row][col])

    def update_square(self, row, col):
        sq_index = self.get_square_index(row,col)
        self.squares[sq_index] = []
        start_slice = (sq_index % self.unit_cell) * self.unit_cell
        end_slice = start_slice + self.unit_cell
        start_range = (sq_index // self.unit_cell) * self.unit_cell
        end_range = start_range + self.unit_cell
        for j in range(start_range, end_range):
            self.squares[sq_index] += self.h_rows[j][start_slice : end_slice]

    def update_all_squares(self):
        self.squares = []
        for i in range(self.length):
            self.squares.append([])
            start_slice = (i % self.unit_cell) * self.unit_cell
            end_slice = start_slice + self.unit_cell
            start_range = (i // self.unit_cell) * self.unit_cell
            end_range = start_range + self.unit_cell
            for j in range(start_range, end_range):
                self.squares[i] += self.h_rows[j][start_slice : end_slice]

    def get_square_index(self, row, col):
        sq_row = row // self.unit_cell
        sq_col = col // self.unit_cell
        index = (sq_row * self.unit_cell) + sq_col
        return index

    def check_square(self, test_num, row, col):
        return test_num in self.squares[self.get_square_index(row,col)]

    # def print_board(self):
    #     for row in self.board:
    #         print(row)
    def print_board(self):
        for row in self.board:
            print_text = ""
            row_copy = list(row)
            row_copy = map(self.alpha, row_copy)
            # for j in row_copy:
            #     row_copy[row_copy.index(j)] = str(j)
            for i in range(self.unit_cell):
                print_text += " ".join(row_copy[(i*self.unit_cell):(i*self.unit_cell)+self.unit_cell])
                print_text += '   '
            if (self.board.index(row)%self.unit_cell == 0):
                print("")
            print(print_text)
            # print(print_text.format(row[0:3],row[3:6],row[6:]))

    def alpha(self, item):
        if(item > 9):
            return chr(item+55)
        else: 
            return str(item)

    def shuffle_unused(self):
        self.unused = []
        for i in range(self.length):
            # generate list of numbers in random order
            arr = range(1, self.length +1)
            random.shuffle(arr)
            self.unused.append(arr)

#tests
test = Sudoku(5)
print("")
print("TESTS RUNNING:")

arr = []
for i in test.board:
    if(0 in i):
        arr.append(test.board.index(i))
if(arr == []):
    print("PASS - NO ZEROES")
else:
    print("FAIL - ZEROES - ROWS: {}".format(arr))

arr = []
for i in test.board:
    if(sum(i) != sum(range(1,test.length+1))):
        arr.append(test.board.index(i))
if(arr == []):
    print("PASS - SUM ROWS")
else:
    print("FAIL - SUM ROWS: {}".format(arr))

arr = []
for i in test.v_rows:
    if(sum(i) != sum(range(1,test.length+1))):
        arr.append(test.v_rows.index(i))
if(arr == []):
    print("PASS - SUM COLS")
else:
    print("FAIL - SUM COLS: {}".format(arr))

arr = []
for i in test.squares:
    if(sum(i) != sum(range(1,test.length+1))):
        arr.append(test.squares.index(i))
if(arr == []):
    print("PASS - SUM SQUARES")
else:
    print("FAIL - SUM SQUARES: {}".format(arr))

for i in test.board:
    arr = []
    for j in range(1,test.length+1):
        if j not in i:
            arr.append(j)
    if(arr != []):
        print("ROW: {} MISSING {}".format(test.board.index(i),arr))

for i in test.v_rows:
    arr = []
    for j in range(1,test.length+1):
        if j not in i:
            arr.append(j)
    if(arr != []):
        print("COL: {} MISSING {}".format(test.v_rows.index(i),arr))

for i in test.squares:
    arr = []
    for j in range(1,test.length+1):
        if j not in i:
            arr.append(j)
    if(arr != []):
        print("SQUARE: {} MISSING {}".format(test.squares.index(i),arr))


for i in range(test.length):
    for j in range(1,test.length+1):
        if(test.board[i].count(j) != 1):
            print("FAILURE: ROW {} MISSING OR ADDITIONAL '{}'".format(i,j))

for i in range(test.length):
    for j in range(1,test.length+1):
        if(test.v_rows[i].count(j) != 1):
            print("FAILURE: COL {} MISSING OR ADDITIONAL '{}'".format(i,j))

for i in range(test.length):
    for j in range(1,test.length+1):
        if(test.squares[i].count(j) != 1):
            print("FAILURE: SQU {} MISSING OR ADDITIONAL '{}'".format(i,j))


