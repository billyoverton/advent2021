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

    gamma_rate_index = [0] * bitLength
    epsilon_rate_index = [0] * bitLength

    for i in range(bitLength):
        ones = sum([int(x[i]) for x in data])

        if ones > (totalCount / 2):
            gamma_rate_index[i] = 1
            epsilon_rate_index[i] = 0
        else:
            gamma_rate_index[i] = 0
            epsilon_rate_index[i] = 1

    logging.debug("Gamma Rate Bits: %s" % gamma_rate_index)
    logging.debug("Epsilon Rate Bits: %s" % epsilon_rate_index)

    gamma_rate = int("".join([str(x) for x in gamma_rate_index]), 2)
    epsilon_rate = int("".join([str(x) for x in epsilon_rate_index]), 2)

    logging.debug("Gamma Rate: %s" % gamma_rate)
    logging.debug("Epsilon Rate: %s" % epsilon_rate)

    logging.info("Answer: %s" % (gamma_rate * epsilon_rate))




if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
