#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.DEBUG

def main(input_file):

    data = []

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            data.append(line)

    bitLength = len(data[0])
    totalCount = len(data)

    oxygen_gen_list = [x for x in data]
    co_scruber_list = [x for x in data]

    logging.debug("Oxygen Generator List: %s" %  oxygen_gen_list)
    logging.debug("CO Scrubber List: %s" %  co_scruber_list)

    for i in range(bitLength):

        ones_ox = sum([int(x[i]) for x in oxygen_gen_list])
        ones_co = sum([int(x[i]) for x in co_scruber_list])

        # Filter the Oxygen Generator List
        if len(oxygen_gen_list) > 1:
            if ones_ox >= (len(oxygen_gen_list) / 2):
                # Either a equal amount or more ones
                oxygen_gen_list = list(filter(lambda value: int(value[i]) == 1, oxygen_gen_list))
            else:
                oxygen_gen_list = list(filter(lambda value: int(value[i]) == 0, oxygen_gen_list))

        # Filter the CO Scrubber List
        if len(co_scruber_list) > 1:
            if ones_co >= (len(co_scruber_list) / 2):
                # Either a equal amount or more ones
                co_scruber_list = list(filter(lambda value: int(value[i]) == 0, co_scruber_list))
            else:
                co_scruber_list = list(filter(lambda value: int(value[i]) == 1, co_scruber_list))

        logging.debug("Oxygen Generator List: %s" %  oxygen_gen_list)
        logging.debug("CO Scrubber List: %s" %  co_scruber_list)

        if len(oxygen_gen_list) == 1 and len(co_scruber_list) == 1:
            break

    oxygen_rating = int(oxygen_gen_list[0], 2)
    co_rating = int(co_scruber_list[0], 2)

    logging.debug("Oxygen Generator Value: %s : %s" % (oxygen_gen_list[0], oxygen_rating))
    logging.debug("CO2 Scrubber Value: %s : %s" % (co_scruber_list[0], co_rating))

    logging.info("Answer: %s" % (oxygen_rating * co_rating))
if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
