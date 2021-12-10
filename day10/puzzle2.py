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

COMPLETION_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def main(input_file):

    lines = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            lines.append(line)

    line_number = 0 # Used just for debugging

    line_scores = []
    for line in lines:
        stack = []
        has_syntax_error = False
        line_number+=1

        logging.debug("Looking at line %s" % line_number)

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
                    has_syntax_error = True
                    break

        if has_syntax_error or len(stack) == 0:
            # We had a syntax error
            continue

        if len(stack) == 0:
            # Stack is empty so this is a complete line, also ignore
            logging.debug("Stack Empty: Line is Complete")
            continue

        line_score = 0
        completion_list = []
        while len(stack) > 0:
            opening = stack.pop()
            closing_char = CHUNK_BOUNDRIES[opening]
            completion_list.append(closing_char)

            line_score = line_score * 5
            line_score += COMPLETION_POINTS[closing_char]

        logging.debug("Incomplete Line: Close with %s with a score of %s" % ("".join(completion_list), line_score))
        line_scores.append(line_score)

    sorted_scores = sorted(line_scores)
    logging.info("Answer: %s" % sorted_scores[len(sorted_scores)//2])

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
