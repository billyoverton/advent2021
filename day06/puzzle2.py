#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO
DAYS_TO_SIMULATE = 256

def main(input_file):

    with open(input_file) as f:
        input = f.readline().strip().split(',')

    fishes = [int(x) for x in input]

    total_fishes = len(fishes)

    fish_map = [0] * 9

    # Load initial map
    for fish in input:
        fish_map[int(fish)] = fish_map[int(fish)] + 1

    logging.debug("Initial fish map: %s" % fish_map)

    for day in range(DAYS_TO_SIMULATE):

        new_fish_count = fish_map[0]
        for i in range(1, len(fish_map)):
            fish_map[i-1] = fish_map[i]

        # Add the new fish
        fish_map[8] = new_fish_count

        # Add the old fish back to the pool
        fish_map[6] = fish_map[6] + new_fish_count

        logging.debug("After %s Day: %s" % (day+1, fish_map))

    logging.info("Answer: %s" % sum(fish_map))




if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
