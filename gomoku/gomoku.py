import sys
import re
import copy
import string


class Gomoku(object):
    def __init__(self, player_no, board_values, board_legal_positions, board_size, cutoffdepth, depth):
        self.player_no = player_no
        if player_no == 1:
            self.player_value = 'b'
            self.player2_value = 'w'
        else:
            self.player_value = 'w'
            self.player2_value = 'b'
        self.board_values = board_values
        self.board_legal_positions = board_legal_positions
        self.cutoffdepth = cutoffdepth
        self.board_size = board_size
        self.depth = depth

                    ####Greedy####
    def greedy(self, player, legal_moves, curr_board_values):
        max_score = 0
        best_move = ''
        for position in legal_moves:
            coord_list = re.split(r",", position)
            row = int(coord_list[0])
            col = int(coord_list[1])

            score = 0
            # win check
            win = self.win(row, col, self.player_value, self.board_values)
            if win:
                score = score + 50000

            block_open3 = self.block_open3(row, col, self.player2_value, self.board_values)
            block_closed = self.block_closed(row, col, self.player2_value, self.board_values)
            # CreateOpen
            create_open = self.create_open(row, col, self.player_value, self.board_values)
            create_closed = self.create_closed(row, col, self.player_value, self.board_values)
            if block_open3 > 0:
                score += block_open3 * 500

            if block_closed[0] != 0 or block_closed[1] != 0 or block_closed[2] != 0:
                score += block_closed[0] * 10000 + block_closed[1] * 100

            if create_open[0] != 0 or create_open[1] != 0 or create_open[2] != 0:
                score += create_open[0] * 5000 + create_open[1] * 50 + create_open[2] * 5

            if create_closed[0] != 0 or create_closed[1] != 0 or create_closed[2] != 0:
                score += create_closed[0] * 1000 + create_closed[1] * 10 + create_closed[2] * 1

            if max_score < score:
                max_score = score
                best_move = str(row) + "," + str(col)
        return best_move

    def win(self, row, col, player_value, curr_board_values):
        count = 0
        for i in range(1, 5):
            if (col - i > -1):
                if curr_board_values[row][col - i] != player_value:
                    break
                else:
                    count += 1
        for i in range(1, 5):
            if col + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row][col + i] != player_value:
                    break
                else:
                    count += 1
        if count >= 4:
            return True
        else:
            count = 0

        for i in range(1, 5):
            if (row - i > -1):
                if curr_board_values[row - i][col] != player_value:
                    break
                else:
                    count += 1
        for i in range(1, 5):
            if row + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row + i][col] != player_value:
                    break
                else:
                    count += 1
        if count >= 4:
            return True
        else:
            count = 0

        for i in range(1, 5):
            if (row - i > -1 and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row - i][col + i] != player_value:
                    break
                else:
                    count += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col - i > -1):
                if curr_board_values[row + i][col - i] != player_value:
                    break
                else:
                    count += 1
        if count >= 4:
            return True
        else:
            count = 0

        for i in range(1, 5):
            if (row - i > -1 and col - i > -1):
                if curr_board_values[row - i][col - i] != player_value:
                    break
                else:
                    count += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row + i][col + i] != player_value:
                    break
                else:
                    count += 1
        if count >= 4:
            return True
        else:
            count = 0

    def create_open(self, row, col, player_value, curr_board_values):
        count_side1 = 0
        count_side2 = 0
        foundo4 = 0
        foundo3 = 0
        foundo2 = 0
        for i in range(1, 5):
            if (col - i > -1):
                if curr_board_values[row][col - i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if col + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row][col + i] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (col - (count_side2 + 1) > -1 and curr_board_values[row][col - (count_side2 + 1)] == ".") \
                and ((col + count_side1 + 1) <= (len(curr_board_values[row]) - 1) and curr_board_values[row][
                        col + (count_side1 + 1)] == "."):
            if count == 3:
                foundo4 += 1
            elif count == 2:
                foundo3 += 1
            elif count == 1:
                foundo2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1):
                if curr_board_values[row - i][col] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if row + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row + i][col] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (row - (count_side2 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][col] == ".") \
                and ((row + count_side1 + 1) <= (len(curr_board_values[row]) - 1) and
                             curr_board_values[row + (count_side1 + 1)][col] == "."):
            if count == 3:
                foundo4 += 1
            elif count == 2:
                foundo3 += 1
            elif count == 1:
                foundo2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row - i][col + i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col - i > -1):
                if curr_board_values[row + i][col - i] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (row - (count_side2 + 1) > -1 and col + (count_side2 + 1) <= (len(curr_board_values[row]) - 1) and row + (
                    count_side1 + 1) <= (len(curr_board_values[row]) - 1) and \
                            col - (count_side1 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][
                    col + count_side2 + 1] == '.' \
                    and curr_board_values[row + (count_side1 + 1)][col - (count_side1 + 1)] == '.'):
            if count == 3:
                foundo4 += 1
            elif count == 2:
                foundo3 += 1
            elif count == 1:
                foundo2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col - i > -1):
                if curr_board_values[row - i][col - i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row + i][col + i] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (row - (count_side2 + 1) > -1 and col - (count_side2 + 1) > -1 and row + (count_side1 + 1) <= (
                    len(curr_board_values[row]) - 1) and \
                            col + (count_side1 + 1) <= (len(curr_board_values[row]) - 1) and
                    curr_board_values[row - (count_side2 + 1)][col - (count_side2 + 1)] == '.' \
                    and curr_board_values[row + (count_side1 + 1)][col + (count_side1 + 1)] == '.'):
            if count == 3:
                foundo4 += 1
            elif count == 2:
                foundo3 += 1
            elif count == 1:
                foundo2 += 1

        foundolist = [foundo4, foundo3, foundo2]
        return foundolist

    def block_closed(self, row, col, player_value, curr_board_values):
        count_side1 = 0
        count_side2 = 0
        foundc4 = 0
        foundc3 = 0
        foundc2 = 0
        for i in range(1, 5):
            if (col - i > -1):
                if curr_board_values[row][col - i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if col + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row][col + i] != player_value:
                    break
                else:
                    count_side1 += 1
        if count_side1 == 4:
            if (col + count_side1 + 1) < (len(curr_board_values[row]) - 1) and curr_board_values[row][
                        col + (count_side1 + 1)] == self.opponent(player_value):
                foundc4 += 1
        if count_side2 == 4:
            if (col - (count_side2 + 1) > -1 and curr_board_values[row][col - (count_side2 + 1)] == self.opponent(player_value)):
                foundc4 += 1
        if count_side1 == 3:
            if (col + count_side1 + 1) < (len(curr_board_values[row]) - 1) and curr_board_values[row][
                        col + (count_side1 + 1)] == self.opponent(player_value):
                foundc3 += 1
        if count_side2 == 3:
            if (col - (count_side2 + 1) > -1 and curr_board_values[row][col - (count_side2 + 1)] == self.opponent(player_value)):
                foundc3 += 1
        if count_side1 == 2:
            if (col + count_side1 + 1) < (len(curr_board_values[row]) - 1) and curr_board_values[row][
                        col + (count_side1 + 1)] == self.opponent(player_value):
                foundc2 += 1
        if count_side2 == 2:
            if (col - (count_side2 + 1) > -1 and curr_board_values[row][col - (count_side2 + 1)] == self.opponent(player_value)):
                foundc2 += 1


        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if row - i > -1:
                if curr_board_values[row - i][col] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if row + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row + i][col] != player_value:
                    break
                else:
                    count_side1 += 1
        if count_side2 == 4:
            if (row - (count_side2 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][col] == self.opponent(player_value)):
                foundc4 += 1
        if count_side1 == 4:
            if (row + count_side1 + 1) < (len(curr_board_values[row]) - 1) and \
                            curr_board_values[row + (count_side1 + 1)][col] == self.opponent(player_value):
                foundc4 += 1
        if count_side2 == 3:
            if (row - (count_side2 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][col] == self.opponent(player_value)):
                foundc3 += 1
        if count_side1 == 3:
            if (row + count_side1 + 1) < (len(curr_board_values[row]) - 1) and \
                            curr_board_values[row + (count_side1 + 1)][col] == self.opponent(player_value):
                foundc3 += 1
        if count_side2 == 2:
            if (row - (count_side2 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][col] == self.opponent(player_value)):
                foundc2 += 1
        if count_side1 == 2:
            if (row + count_side1 + 1) < (len(curr_board_values[row]) - 1) and \
                            curr_board_values[row + (count_side1 + 1)][col] == self.opponent(player_value):
                foundc2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row - i][col + i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col - i > -1):
                if curr_board_values[row + i][col - i] != player_value:
                    break
                else:
                    count_side1 += 1
        if count_side2 == 4:
            if row - (count_side2 + 1) > -1 and col + (count_side2 + 1) <= (len(curr_board_values[row]) - 1) \
                    and curr_board_values[row - (count_side2 + 1)][col + count_side2 + 1] == self.opponent(player_value):
                foundc4 += 1
        if count_side1 == 4:
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col - (count_side1 + 1) > -1 \
                    and curr_board_values[row + (count_side1 + 1)][col - (count_side1 + 1)] == self.opponent(player_value):
                foundc4 += 1
        if count_side2 == 3:
            if row - (count_side2 + 1) > -1 and col + (count_side2 + 1) <= (len(curr_board_values[row]) - 1) \
                    and curr_board_values[row - (count_side2 + 1)][col + count_side2 + 1] == self.opponent(player_value):
                foundc3 += 1
        if count_side1 == 3:
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col - (count_side1 + 1) > -1 \
                    and curr_board_values[row + (count_side1 + 1)][col - (count_side1 + 1)] == self.opponent(player_value):
                foundc3 += 1
        if count_side2 == 2:
            if row - (count_side2 + 1) > -1 and col + (count_side2 + 1) <= (len(curr_board_values[row]) - 1) \
                    and curr_board_values[row - (count_side2 + 1)][col + count_side2 + 1] == self.opponent(player_value):
                foundc2 += 1
        if count_side1 == 2:
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col - (count_side1 + 1) > -1 \
                    and curr_board_values[row + (count_side1 + 1)][col - (count_side1 + 1)] == self.opponent(player_value):
                foundc2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col - i > -1):
                if curr_board_values[row - i][col - i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row + i][col + i] != player_value:
                    break
                else:
                    count_side1 += 1
        if count_side2 == 4:
            if row - (count_side2 + 1) > -1 and col - (count_side2 + 1) > -1 and \
                            curr_board_values[row - (count_side2 + 1)][col - (count_side2 + 1)] == self.opponent(player_value):
                foundc4 += 1
        if count_side1 == 4:
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col + (count_side1 + 1) < (
                        len(curr_board_values[row]) - 1) \
                    and curr_board_values[row + (count_side1 + 1)][col + (count_side1 + 1)] == self.opponent(player_value):
                foundc4 += 1
        if count_side2 == 3:
            if row - (count_side2 + 1) > -1 and col - (count_side2 + 1) > -1 and \
                            curr_board_values[row - (count_side2 + 1)][col - (count_side2 + 1)] == self.opponent(player_value):
                foundc3 += 1
        if count_side1 == 3:
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col + (count_side1 + 1) < (
                len(curr_board_values[row]) - 1) \
                    and curr_board_values[row + (count_side1 + 1)][col + (count_side1 + 1)] == self.opponent(player_value):
                foundc3 += 1
        if count_side2 == 2:
            if row - (count_side2 + 1) > -1 and col - (count_side2 + 1) > -1 and \
                            curr_board_values[row - (count_side2 + 1)][col - (count_side2 + 1)] == self.opponent(player_value):
                foundc2 += 1
        if count_side1 == 2:
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col + (count_side1 + 1) < (
                        len(curr_board_values[row]) - 1) \
                    and curr_board_values[row + (count_side1 + 1)][col + (count_side1 + 1)] == self.opponent(player_value):
                foundc2 += 1

        foundclist = [foundc4, foundc3, foundc2]
        return foundclist

    def block_open3(self, row, col, player, curr_board_values):
        count_side1 = 0
        count_side2 = 0
        foundo3 = 0
        for i in range(1, 5):
            if (col - i > -1):
                if curr_board_values[row][col - i] != player:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if col + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row][col + i] != player:
                    break
                else:
                    count_side1 += 1
        if count_side1 == 3 :
            if (col + count_side1 + 1) < (len(curr_board_values[row]) - 1) and curr_board_values[row][col + (count_side1 + 1)] == ".":
                foundo3 += 1
        if count_side2 == 3:
            if (col - (count_side2 + 1) > -1 and curr_board_values[row][col - (count_side2 + 1)] == ".") :
                foundo3 +=1

        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if row - i > -1 :
                if curr_board_values[row - i][col] != player:
                    break
                else :
                    count_side2 += 1
        for i in range(1, 5):
            if row + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row + i][col] != player:
                    break
                else:
                    count_side1 += 1
        if count_side2 == 3 :
            if (row - (count_side2 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][col] == ".") :
                foundo3 += 1
        if count_side1 == 3 :
            if (row + count_side1 + 1) < (len(curr_board_values[row]) - 1) and curr_board_values[row + (count_side1 + 1)][col] == ".":
                foundo3 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row - i][col + i] != player:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col - i > -1):
                if curr_board_values[row + i][col - i] != player:
                    break
                else:
                    count_side1 += 1
        if count_side2 == 3 :
            if row - (count_side2 + 1) > -1 and col + (count_side2 + 1) <= (len(curr_board_values[row]) - 1)\
            and curr_board_values[row - (count_side2 + 1)][col + count_side2 + 1] == "." :
                foundo3+=1
        if count_side1 ==3 :
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col - (count_side1 + 1) > -1 \
            and curr_board_values[row + (count_side1 + 1)][col - (count_side1 + 1)] == "." :
                foundo3 +=1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col - i > -1) :
                if curr_board_values[row - i][col - i] != player:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row + i][col + i] != player:
                    break
                else:
                    count_side1 += 1
        if count_side2 == 3 :
            if row - (count_side2 + 1) > -1 and col - (count_side2 + 1) > -1 and \
            curr_board_values[row - (count_side2 + 1)][col - (count_side2 + 1)] == "." :
                foundo3 +=1
        if count_side1==3 :
            if row + (count_side1 + 1) < (len(curr_board_values[row]) - 1) and col + (count_side1 + 1) < (len(curr_board_values[row]) - 1) \
            and curr_board_values[row + (count_side1 + 1)][col + (count_side1 + 1)] == "." :
                foundo3+=1

        return foundo3

    def create_closed(self, row, col, player_value, curr_board_values):
        count_side1 = 0
        count_side2 = 0
        foundc4 = 0
        foundc3 = 0
        foundc2 = 0
        for i in range(1, 5):
            if (col - i > -1):
                if curr_board_values[row][col - i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if col + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row][col + i] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if ((col - (count_side2 + 1) > -1 and curr_board_values[row][col - (count_side2 + 1)] == ".") \
                    + ((col + count_side1 + 1) <= (len(curr_board_values[row]) - 1) and curr_board_values[row][
                    col + (count_side1 + 1)] == ".") == 1):
            if count == 3:
                foundc4 += 1
            elif count == 2:
                foundc3 += 1
            elif count == 1:
                foundc2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1):
                if curr_board_values[row - i][col] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if row + i <= (len(curr_board_values[row]) - 1):
                if curr_board_values[row + i][col] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (row - (count_side2 + 1) > -1 and curr_board_values[row - (count_side2 + 1)][col] == ".") \
                + ((row + count_side1 + 1) <= (len(curr_board_values[row]) - 1) and
                           curr_board_values[row + (count_side1 + 1)][col] == ".") == 1:
            if count == 3:
                foundc4 += 1
            elif count == 2:
                foundc3 += 1
            elif count == 1:
                foundc2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row - i][col + i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col - i > -1):
                if curr_board_values[row + i][col - i] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (row - (count_side2 + 1) > -1 and col + (count_side2 + 1) <= (len(curr_board_values[row]) - 1) \
                    and curr_board_values[row - (count_side2 + 1)][col + count_side2 + 1] == '.') \
                + (row + (count_side1 + 1) <= (len(curr_board_values[row]) - 1) and col - (count_side1 + 1) > -1 \
                           and curr_board_values[row + (count_side1 + 1)][col - (count_side1 + 1)] == '.') == 1:
            if count == 3:
                foundc4 += 1
            elif count == 2:
                foundc3 += 1
            elif count == 1:
                foundc2 += 1
        count_side1 = 0
        count_side2 = 0

        for i in range(1, 5):
            if (row - i > -1 and col - i > -1):
                if curr_board_values[row - i][col - i] != player_value:
                    break
                else:
                    count_side2 += 1
        for i in range(1, 5):
            if (row + i <= (len(curr_board_values[row]) - 1) and col + i <= (len(curr_board_values[row]) - 1)):
                if curr_board_values[row + i][col + i] != player_value:
                    break
                else:
                    count_side1 += 1
        count = count_side2 + count_side1
        if (row - (count_side2 + 1) > -1 and col - (count_side2 + 1) > -1 and
                    curr_board_values[row - (count_side2 + 1)][col - (count_side2 + 1)] == '.') \
                + (row + (count_side1 + 1) <= (len(curr_board_values[row]) - 1) and col + (count_side1 + 1) <= (
                            len(curr_board_values[row]) - 1) \
                           and curr_board_values[row + (count_side1 + 1)][col + (count_side1 + 1)] == '.') == 1:
            if count == 3:
                foundc4 += 1
            elif count == 2:
                foundc3 += 1
            elif count == 1:
                foundc2 += 1

        foundclist = [foundc4, foundc3, foundc2]
        return foundclist

    def labelling(self, position):
        coord_list = re.split(r",", position)
        row = int(coord_list[0])
        col = int(coord_list[1])
        labels = string.ascii_uppercase
        pos_to_lab = (labels[col] + str(((row) + 1)))
        return pos_to_lab

    def de_label(self, position):
        coord_list = re.findall(r"\d+|\D+", position)
        labels = string.ascii_uppercase
        row = int(coord_list[1])
        col = labels.index(coord_list[0])
        lab_to_pos = str(row - 1) + "," + str(col)
        return lab_to_pos

    def update_board(self, board_to_update, move, player_value):
        best_coord_list = re.split(r",", move)
        row = int(best_coord_list[0])
        col = int(best_coord_list[1])
        new_board_value = copy.deepcopy(board_to_update)
        new_board_value[row][col] = player_value
        return new_board_value

    def write_to_file(self, player_value, board_to_write):
        for i in range(len(board_to_write) - 1, -1, -1):
            for j in range(len(board_to_write[i])):
                sys.stdout.write(board_to_write[i][j])
            sys.stdout.write("\n")

                    ####Minimax####
    def minimax(self, board_legal_positions, curr_board_values):
        start = 'root'
        bestvalue = sys.maxsize * -1
        depth = 0
        line1 = "{0},{1},{2}".format(start, str(depth), str(bestvalue))
        line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
        print line1
        for position in board_legal_positions:
            depth = 0
            value = 0
            value = (self.min(position, curr_board_values, self.player_value, value, depth + 1))
            if value > bestvalue:
                bestvalue = value
                best_position = position
            line1 = "{0},{1},{2}".format(start, str(depth), str(bestvalue))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
        return best_position

    def max(self, position, curr_board_values, player, value, depth):
        bestvalue = sys.maxsize * -1
        val = self.evaluate(position, curr_board_values, self.opponent(player))
        if depth == self.cutoffdepth:
            value -= val
            line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), value)
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        if val >= 50000:
            value -= val
            line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), value)
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), bestvalue)
        line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
        print line1
        value -= val
        new_board_value = self.update_board(curr_board_values, position, self.opponent(player))
        curr_legal = self.find_legal_position(new_board_value)
        for el in curr_legal:
            bestvalue = max(bestvalue, self.min(el, new_board_value, player, value, depth + 1))
            line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), bestvalue)
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
        return bestvalue

    def min(self, position, curr_board_values, player, value, depth):
        bestvalue = sys.maxsize
        val = self.evaluate(position, curr_board_values, player)
        if depth == self.cutoffdepth:
            value += val
            line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), value)
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        elif val >= 50000:
            value += val
            line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), value)
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), bestvalue)
        line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
        print line1
        value += val
        new_board_value = self.update_board(curr_board_values, position, player)
        curr_legal = self.find_legal_position(new_board_value)
        for el in curr_legal:
            bestvalue = min(bestvalue, self.max(el, new_board_value, player, value, depth + 1))
            line1 = "{0},{1},{2}".format(self.labelling(position), str(depth), bestvalue)
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
        return bestvalue

                ####Alpha-beta#####
    def minimax_alphabeta(self, board_legal_positions, curr_board_values):
        start = 'root'
        alpha=  sys.maxsize * -1
        beta= sys.maxsize
        bestvalue = sys.maxsize * -1
        depth = 0
        line1 = "{0},{1},{2},{3},{4}".format(start, str(depth), str(bestvalue),str(alpha),str(beta))
        line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
        print line1
        for position in board_legal_positions:
            depth = 0
            value = 0
            value = (self.min_alphabeta(position, curr_board_values, self.player_value, value, depth + 1,alpha,beta))
            if value > bestvalue:
                bestvalue = value
                best_position = position
            alpha=max(alpha,bestvalue)
            line1 = "{0},{1},{2},{3},{4}".format(start, str(depth), str(bestvalue), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
        return best_position

    def max_alphabeta(self, position, curr_board_values, player, value, depth,alpha,beta):
        bestvalue = sys.maxsize * -1
        val = self.evaluate(position, curr_board_values, self.opponent(player))
        if depth == self.cutoffdepth:
            value -= val
            line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(value), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        if val >= 50000:
            value -= val
            line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(value), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(bestvalue), str(alpha), str(beta))
        line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
        print line1
        value -= val
        new_board_value = self.update_board(curr_board_values, position, self.opponent(player))
        curr_legal = self.find_legal_position(new_board_value)
        for el in curr_legal:
            bestvalue = max(bestvalue, self.min_alphabeta(el, new_board_value, player, value, depth + 1,alpha,beta))
            if bestvalue >= beta:
                line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(bestvalue), str(alpha),
                                                     str(beta))
                line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
                print line1
                return bestvalue
            alpha = max(alpha, bestvalue)
            line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(bestvalue), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
        return bestvalue

    def min_alphabeta(self, position, curr_board_values, player, value, depth,alpha,beta):
        bestvalue = sys.maxsize
        val = self.evaluate(position, curr_board_values, player)
        if depth == self.cutoffdepth:
            value += val
            line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(value), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        elif val >= 50000:
            value += val
            line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(value), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
            return value
        line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(bestvalue), str(alpha), str(beta))
        line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
        print line1
        value += val
        new_board_value = self.update_board(curr_board_values, position, player)
        curr_legal = self.find_legal_position(new_board_value)
        for el in curr_legal:
            bestvalue = min(bestvalue, self.max_alphabeta(el, new_board_value, player, value, depth + 1,alpha,beta))
            if bestvalue <= alpha:
                line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(bestvalue), str(alpha),
                                                     str(beta))
                line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
                print line1
                return bestvalue
            beta=min(beta,bestvalue)
            line1 = "{0},{1},{2},{3},{4}".format(self.labelling(position), str(depth), str(bestvalue), str(alpha), str(beta))
            line1 = re.sub(r'\b{0}\b'.format(re.escape("9223372036854775807")), 'Infinity', line1)
            print line1
        return bestvalue


    def opponent(self, player_value):
        if player_value == 'w':
            return 'b'
        else:
            return 'w'

    def evaluate(self, position, curr_board_values, player):
        coord_list = re.split(r",", position)
        row = int(coord_list[0])
        col = int(coord_list[1])
        score = 0
        # win check
        win = self.win(row, col, player, curr_board_values)
        if win:
            score = score + 50000

        block_open3 = self.block_open3(row, col, self.opponent(player), curr_board_values)
        block_closed = self.block_closed(row, col, self.opponent(player), curr_board_values)
        # CreateOpen
        create_open = self.create_open(row, col, player, curr_board_values)
        create_closed = self.create_closed(row, col, player, curr_board_values)
        if block_open3 > 0:
            score += block_open3 * 500

        if block_closed[0] != 0 or block_closed[1] != 0 or block_closed[2] != 0:
            score += block_closed[0] * 10000 + block_closed[1] * 100

        if create_open[0] != 0 or create_open[1] != 0 or create_open[2] != 0:
            score += create_open[0] * 5000 + create_open[1] * 50 + create_open[2] * 5

        if create_closed[0] != 0 or create_closed[1] != 0 or create_closed[2] != 0:
            score += create_closed[0] * 1000 + create_closed[1] * 10 + create_closed[2] * 1

        return score

    def find_legal_position(self, board_values):
        board_legal_positions = []
        for i in range(len(board_values)):
            for j in range(len(board_values[i])):
                if board_values[i][j] == '.':
                    if (j - 1 > -1 and board_values[i][j - 1] != '.') or (
                                        j + 1 < (len(board_values[i]) - 1) and board_values[i][j + 1] != '.'):
                        board_legal_positions.append(str(i) + ',' + str(j))
                    elif (i - 1 > -1 and board_values[i - 1][j] != '.') or (
                                        i + 1 < (len(board_values[i]) - 1) and board_values[i + 1][j] != '.'):
                        board_legal_positions.append(str(i) + ',' + str(j))
                    elif (i - 1 > -1 and j - 1 > -1 and board_values[i - 1][j - 1] != '.') or i + 1 < (
                                len(board_values[i]) - 1) and (
                                        j + 1 < (len(board_values[i]) - 1) and board_values[i + 1][j + 1] != '.'):
                        board_legal_positions.append(str(i) + ',' + str(j))
                    elif (i - 1 > -1 and j + 1 < (len(board_values[i]) - 1) and board_values[i - 1][j + 1] != '.') or (
                                            i + 1 < (len(board_values[i]) - 1) and j - 1 > -1 and board_values[i + 1][
                                    j - 1] != '.'):
                        board_legal_positions.append(str(i) + ',' + str(j))

        sorted_board_legal_positions = []
        for position in board_legal_positions:
            sorted_board_legal_positions.append(self.labelling(position))
        sorted_board_legal_positions.sort(key=self.natural_sort_key)
        board_legal_positions = []
        for position in sorted_board_legal_positions:
            board_legal_positions.append((self.de_label(position)))
        return board_legal_positions

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(_nsre, s)]


_nsre = re.compile('([0-9]+)')


def main():
    filename = sys.argv[1]
    f1 = open(filename, "r")
    if f1.mode == 'r':
        data = f1.read().splitlines()

    task = int(data[0])
    player_no = int(data[1])
    cutoffdepth = int(data[2])
    board_size = int(data[3])
    board_values = []
    board_legal_positions = []

    for i in range(3 + board_size, 3, -1):
        board_values.append(list(str(data[i])))
    isempty = True
    isfull = True
    if player_no==1:
        player='b'
    else: player='w'
    for i in range(len(board_values)):
        if 'w' in board_values[i] or 'b' in board_values[i] :
            isempty = False

    for i in range(len(board_values)):
        if '.' in board_values[i] :
            isfull = False


    if isempty == True:
        board_values[int((len(board_values))/2)][int((len(board_values))/2)] = player

    for i in range(len(board_values)):
        for j in range(len(board_values[i])):
            if board_values[i][j] == '.':
                if (j - 1 > -1 and board_values[i][j - 1] != '.') or (
                                    j + 1 < (len(board_values[i]) - 1) and board_values[i][j + 1] != '.'):
                    board_legal_positions.append(str(i) + ',' + str(j))
                elif (i - 1 > -1 and board_values[i - 1][j] != '.') or (
                                    i + 1 < (len(board_values[i]) - 1) and board_values[i + 1][j] != '.'):
                    board_legal_positions.append(str(i) + ',' + str(j))
                elif (i - 1 > -1 and j - 1 > -1 and board_values[i - 1][j - 1] != '.') or i + 1 < (
                            len(board_values[i]) - 1) and (
                                    j + 1 < (len(board_values[i]) - 1) and board_values[i + 1][j + 1] != '.'):
                    board_legal_positions.append(str(i) + ',' + str(j))
                elif (i - 1 > -1 and j + 1 < (len(board_values[i]) - 1) and board_values[i - 1][j + 1] != '.') or (
                                        i + 1 < (len(board_values[i]) - 1) and j - 1 > -1 and board_values[i + 1][
                                j - 1] != '.'):
                    board_legal_positions.append(str(i) + ',' + str(j))

    goku = Gomoku(player_no, board_values, board_legal_positions, board_size, cutoffdepth, 0)
    sorted_board_legal_positions = []
    for position in board_legal_positions:
        sorted_board_legal_positions.append(goku.labelling(position))
    sorted_board_legal_positions.sort(key=goku.natural_sort_key)
    board_legal_positions = []
    for position in sorted_board_legal_positions:
        board_legal_positions.append((goku.de_label(position)))

    goku.board_legal_positions = board_legal_positions

    if task == 1:
        f0 = open("next_state.txt", "w+")
        sys.stdout = f0
        if(not isempty and not isfull):
            move = goku.greedy(player_no, board_legal_positions, board_values)
            new_board_value = goku.update_board(board_values, move, goku.player_value)
            goku.write_to_file(goku.player_value, new_board_value)
        else: goku.write_to_file(goku.player_value, board_values)
        f0.close()
    elif task == 2:
        f1 = open("traverse_log.txt", "w+")
        stdout = sys.stdout
        sys.stdout = f1
        print 'Move,Depth,Value'
        best_position = goku.minimax(board_legal_positions, board_values)
        sys.stdout = stdout
        f1.close()

        f2 = open("next_state.txt", "w+")
        sys.stdout = f2
        if (not isempty or not isfull):
            new_board_value = goku.update_board(board_values, best_position, goku.player_value)
            goku.write_to_file(goku.player_value, new_board_value)
            sys.stdout = stdout
        else: goku.write_to_file(goku.player_value, board_values)
        sys.stdout = stdout
        f2.close()
    elif task == 3:
        f1 = open("traverse_log.txt", "w+")
        stdout = sys.stdout
        sys.stdout = f1
        print 'Move,Depth,Value,Alpha,Beta'
        best_position = ''
        best_position = goku.minimax_alphabeta(board_legal_positions, board_values)
        sys.stdout = stdout
        f1.close()
        f2 = open("next_state.txt", "w+")
        sys.stdout = f2
        if (not isempty or not isfull):
            new_board_value = goku.update_board(board_values, best_position, goku.player_value)
            goku.write_to_file(goku.player_value, new_board_value)
            sys.stdout = stdout
        else: goku.write_to_file(goku.player_value, board_values)
        sys.stdout = stdout

        f2.close()


if __name__ == '__main__':
    main()
