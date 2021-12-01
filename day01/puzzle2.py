#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import math

LOG_LEVEL = logging.INFO

def main(input_file):

    values = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break

            values.append(int(line))

    increase_count = 0
    prev_sum = math.inf
    for i in range(len(values)):
        window = values[i:i+3]
        value = sum(window)
        if value > prev_sum:
            logging.debug("Windows %s increased" % window)
            increase_count += 1
        elif value == prev_sum:
            logging.debug("Windows %s no change" % window)
        else:
            logging.debug("Windows %s decreased" % window)

        prev_sum = value

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
