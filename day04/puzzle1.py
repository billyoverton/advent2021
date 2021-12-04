#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

class BingoBoard(object):
    def __init__(self, iterable):
        self.board = []

        for row in iterable:
            self.board.append([ [x, False] for x in row])

    def mark_number(self, number):
        for row in self.board:
            for value in row:
                if value[0] == number:
                    value[1] = True

    def is_winning_board(self):
        for row in self.board:
            if all([x[1] for x in row]):
                return True

        for i in range(len(self.board[0])):
            if all(row[i][1] for row in self.board):
                return True

        return False

    def score(self):
        score = 0
        for row in self.board:
            for value in row:
                if value[1] == False:
                    score += value[0]
        return score

def main(input_file):
    number_list = None
    boards = []

    file_contents = None
    with open(input_file) as f:
        file_contents = f.readlines()

    number_list = [int(x) for x in file_contents.pop(0).strip().split(',')]
    file_contents.pop(0) # Trash line 2 blank

    board = []
    for line in file_contents:
        line = line.strip()
        if line == "":
            boards.append(BingoBoard(board))
            board = []
        else:
            board.append([int(x) for x in line.split()])
    boards.append(BingoBoard(board))

    logging.debug("Selected Numbers: %s" % number_list)
    logging.debug("Boards: %s" % boards)

    winning_board = None
    winning_number = None
    for number in number_list:
        logging.debug("Marking Number: %s" % number)
        for board in boards:
            board.mark_number(number)

            if board.is_winning_board():
                winning_board = board
                winning_number = number
                logging.debug("Winning Board Found: %s" % winning_board)

        if winning_board is not None:
            break

    board_score = winning_board.score()

    logging.debug("Board Score: %s" % board_score)

    logging.info("Answer: %s" % (board_score * winning_number))

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
