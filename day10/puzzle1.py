#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

CHUNK_BOUNDRIES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

ILLEGAL_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

def main(input_file):

    lines = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            lines.append(line)

    file_score = 0
    for line in lines:
        stack = []

        for char in line:
            if char in CHUNK_BOUNDRIES:
                # We have a opening chunk character push it on the stack
                stack.append(char)
            elif char in CHUNK_BOUNDRIES.values():
                # We have a closing character lets try and close the chunk
                opening = stack.pop()
                if CHUNK_BOUNDRIES[opening] != char:
                    # Syntax Error: Illegal Character
                    logging.debug("Syntax Error: Expected %s, but found %s instead." % (CHUNK_BOUNDRIES[opening], char))
                    file_score += ILLEGAL_POINTS[char]
                    break

    logging.info("Answer: %s" % file_score)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
