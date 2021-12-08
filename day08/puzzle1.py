#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    # List of (patterns, reading) values from input
    displays = []

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            pattern, reading = line.split(' | ')
            displays.append([pattern, reading])

    logging.debug("Display Inputs:\n%s" % "\n".join(map(str, displays)))

    easy_count = 0
    for display in displays:
        readings = display[1].split()
        logging.debug("Checking readings: %s" % readings)
        for reading in readings:
            if len(reading) in [2,3,4,7]:
                logging.debug("Found Eazy Number: %s" % reading )
                easy_count += 1

    logging.info("Answer: %s" % easy_count)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
