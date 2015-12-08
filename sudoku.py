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
        # self.print_board()

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

        #delete
        print("self.h_rows")
        for i in range(self.length):
            print(self.h_rows[i])
        print("\n")
        print("self.v_rows")
        for i in range(self.length):
            print(self.v_rows[i])
        print("\n")
        print("self.unused")
        for i in range(self.length):
            print(self.unused[i])
        print("\n")
        #/delete

        # main seed function
        # go through board cell by cell
        for row in range(self.length):

            temp_arr = self.unused[row]
            restart = True
            safety = 0
            while restart:
                if(safety > 100):
                    break
                restart = False

                for col in range(self.length):
                    if restart:
                        print("here")
                        break
                    # loop through unused numbers for a given row
                    skip = 0
                    for num in temp_arr:
                        # check if the number can go in that column and square
                        # if it can't, continue to next number in unused
                        if(self.check_col(num, self.v_rows[col])):
                            skip += 1
                            # if skip and col add to length, restart the whole while loop
                            if((skip + col) == self.length):
                                print("zero at: ({},{})".format(row,col))
                                # reset temparray with num at front
                                restart = True
                                safety += 1
                                temp_arr = self.unused[row]
                                temp_arr.remove(num)
                                temp_arr.insert(0, num)
                                # apply changes to self.unused, too
                                self.unused[row].remove(num)
                                self.unused[row].insert(0,num)
                                print("ta",temp_arr)
                                # start loop over for entire row
                                break
                            continue
                        if(self.check_square(num, row, col)):
                            skip += 1
                            if((skip + col) == self.length):
                                print("zero at: ({},{})".format(row,col))
                                # reset temparray with num at front
                                restart = True
                                safety += 1
                                temp_arr = self.unused[row]
                                temp_arr.remove(num)
                                temp_arr.insert(0, num)
                                # apply changes to self.unused, too
                                self.unused[row].remove(num)
                                self.unused[row].insert(0,num)
                                print("ta",temp_arr)
                                # start loop over for entire row
                                break
                            continue
                        # if number passes tests, insert it into row and column,
                        # remove the number from unused (since it is now used),
                        # break the loop through unused, go to next col, space
                        self.h_rows[row][col] = num
                        temp_arr.remove(num)
                        skip = 0
                        break
                    # update current column after every successful insertion
                    self.update_column(col)

                    # update square after every successful insertion
                    self.update_square(row, col)


        # delete
        print("\n")
        print("self.unused")
        for i in range(self.length):
            print(self.unused[i])
        print("\n")
        print("self.h_rows")
        for i in range(self.length):
            print(self.h_rows[i])
        print("\n")
        print("self.v_rows")
        for i in range(self.length):
            print(self.v_rows[i])
        print("\n")
        print("self.squares")
        for i in range(self.length):
            print(self.squares[i])
        print("\n")
        # /delete

        self.board = self.h_rows

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

    def print_board(self):
        for row in self.board:
            print(row)

test = Sudoku()
print(test.get_square_index(8,8))
