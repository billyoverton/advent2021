#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO
DAYS_TO_SIMULATE = 80

# Note: I know this is inefficient. Still included because it did solve puzzle 1

def main(input_file):

    with open(input_file) as f:
        input = f.readline().strip().split(',')

    fishes = [int(x) for x in input]

    logging.debug("Initial Fish List: %s" % fishes)

    for day in range(DAYS_TO_SIMULATE):
        fish_to_add = 0
        for i in range(len(fishes)):
            fishes[i] = fishes[i] - 1
            if fishes[i] < 0:
                fish_to_add += 1
                fishes[i] = 6
        fishes.extend([8]*fish_to_add)

        logging.debug("After %s days: %s" % (day+1, fishes))

    logging.info("Answer: %s" % len(fishes))



if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
