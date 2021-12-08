#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util
import math

LOG_LEVEL = logging.INFO

def fuel_usage(location, target):
    steps = abs(location - target)

    fuel = 0
    fuel_per_step = 1
    for i in range(steps):
        fuel += fuel_per_step
        fuel_per_step += 1

    return fuel

def main(input_file):

    with open(input_file) as f:
        input = f.readline().strip().split(',')

    values = [int(x) for x in input]
    logging.debug("Values: %s" % values)

    min_val, max_val = util.min_max(values)
    logging.debug("Min: %s, Max: %s" % (min_val, max_val))

    minimal_fuel = math.inf
    final_target = -1
    for target in range(min_val, max_val+1):
        current_target_fuel = 0
        logging.debug("=== Testing target %s ===" % target)
        for crab in values:
            fuel = fuel_usage(crab, target)
            logging.debug("Move from %s to %s: %s fuel" % (crab, target, fuel))
            current_target_fuel += fuel
            if current_target_fuel > minimal_fuel:
                # No need to check more so short circut
                break

        if current_target_fuel < minimal_fuel:
            minimal_fuel = current_target_fuel
            final_target = target

    logging.debug("Minimal Target: %s" % final_target)
    logging.info("Answer: %s" % minimal_fuel)



if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
