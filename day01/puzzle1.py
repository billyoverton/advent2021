#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import math

LOG_LEVEL = logging.INFO

def main(input_file):

    increase_count = 0

    prev = math.inf
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break

            value = int(line)
            if value > prev:
                logging.debug("%s (increased)" % value)
                increase_count+=1
            else:
                logging.debug("%s (not increasing)" % value)
            prev = value

    logging.info("Answer: %s" % increase_count)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
