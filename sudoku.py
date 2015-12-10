import random

class Sudoku(object):

    def __init__(self, uc = 3):
        self.unit_cell = uc
        self.length = uc ** 2
        self.squares = []
        self.rows = []
        self.cols = []
        self.board = self.generate_board(self.unit_cell, self.length)
        self.print_board()

    # def generate_board(self, unit, ):
    def generate_board(self, unit, length):
        # generate variables
        hat = []
        rows = []
        cols = []
        squares = []

        for i in range(length):
            # generate list of numbers in random order
            arr = range(1, length + 1)
            random.shuffle(arr)
            hat.append(arr)
            # generate empty rows, cols (columns), and squares
            rows.append([0] * length)
            self.cols.append([0] * length)
            self.squares.append([0] * length)
        # main seed function
        # go through board cell by cell
        restart_row = True
        loop_one_safety = 0
        while(restart_row):
            if(loop_one_safety>1000):
                return 1
            hat = self.shuffle_hat(length)
            restart_row = False
            for row in range(length):
                if(restart_row):
                    break
                restart = True

                temp_arr = list(hat[row])
                safety = 0
                rows[row] = [0] * length
                while restart:
                    if(safety > 100):
                        print("safety exit - never going to happen")
                        # print("FAILED ROW: {}".format(row))
                        restart_row = True
                        break
                    restart = False
                    for col in range(length):
                        for num in temp_arr:
                            rows[row][col] = 0
                            self.update_column(rows, col)
                            self.update_square(rows, row, col)
                            if(self.check_col(num, self.cols[col])):
                                continue
                            if(self.check_square(num, row, col)):
                                continue
                            rows[row][col] = num
                            temp_arr.remove(num)
                            self.update_column(rows, col)
                            self.update_square(rows, row, col)
                            break
                    if(0 in rows[row]):
                        index = row
                        for r in range(index):
                            print("ROW {}:  {}\t{}\t{}".format(r, rows[r][0:3],rows[r][3:6],rows[r][6:]))
                            print("")
                        temp_arr = list(hat[row])
                        random.shuffle(temp_arr)
                        restart = True
                        safety += 1
                        loop_one_safety += 1
        return rows

    def check_col(self, test_num, col):
        return test_num in col

    def check_row(self, test_num, row):
        return test_num in row

    def update_column(self, rows, col):
        self.cols[col] = []
        for i in range(self.length):
            self.cols[col].append(rows[i][col])

    def update_all_columns(self):
        for col in range(self.length):
            self.cols[col] = []
            for row in range(self.length):
                self.cols[col].append(self.rows[row][col])

    def update_square(self, rows, row, col):
        sq_index = self.get_square_index(row,col)
        self.squares[sq_index] = []
        start_slice = (sq_index % self.unit_cell) * self.unit_cell
        end_slice = start_slice + self.unit_cell
        start_range = (sq_index // self.unit_cell) * self.unit_cell
        end_range = start_range + self.unit_cell
        for j in range(start_range, end_range):
            self.squares[sq_index] += rows[j][start_slice : end_slice]

    def update_all_squares(self):
        self.squares = []
        for i in range(self.length):
            self.squares.append([])
            start_slice = (i % self.unit_cell) * self.unit_cell
            end_slice = start_slice + self.unit_cell
            start_range = (i // self.unit_cell) * self.unit_cell
            end_range = start_range + self.unit_cell
            for j in range(start_range, end_range):
                self.squares[i] += self.rows[j][start_slice : end_slice]

    def get_square_index(self, row, col):
        sq_row = row // self.unit_cell
        sq_col = col // self.unit_cell
        index = (sq_row * self.unit_cell) + sq_col
        return index

    def check_square(self, test_num, row, col):
        return test_num in self.squares[self.get_square_index(row,col)]

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

    def shuffle_hat(self, length):
        hat = []
        for i in range(length):
            # generate list of numbers in random order
            arr = range(1, length +1)
            random.shuffle(arr)
            hat.append(arr)
        return hat



#tests
test = Sudoku(4)
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
for i in test.cols:
    if(sum(i) != sum(range(1,test.length+1))):
        arr.append(test.cols.index(i))
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

for i in test.cols:
    arr = []
    for j in range(1,test.length+1):
        if j not in i:
            arr.append(j)
    if(arr != []):
        print("COL: {} MISSING {}".format(test.cols.index(i),arr))

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
        if(test.cols[i].count(j) != 1):
            print("FAILURE: COL {} MISSING OR ADDITIONAL '{}'".format(i,j))

for i in range(test.length):
    for j in range(1,test.length+1):
        if(test.squares[i].count(j) != 1):
            print("FAILURE: SQU {} MISSING OR ADDITIONAL '{}'".format(i,j))


