#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    with open(input_file) as f:
        input = f.readline().strip().split(',')

    values = [int(x) for x in input]
    logging.debug("Values: %s" % values)

    median = int(util.median(values))
    logging.debug("Median value: %s" % median)

    total_fuel = 0
    for crab in values:
        fuel = abs((crab - median))
        total_fuel += fuel
        logging.debug("Move from %s to %s: %s fuel" % (crab, median, fuel))

    logging.info("Answer: %s" % total_fuel)


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
