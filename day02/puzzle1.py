#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

LOG_LEVEL = logging.INFO

def main(input_file):

    depth = 0
    position = 0

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            direction, amount = line.split()
            logging.debug("Direction: %s, Amount: %s", direction, amount)
            if direction == "forward":
                position += int(amount)
            elif direction == "up":
                depth -= int(amount)
            elif direction == "down":
                depth += int(amount)
            else:
                logging.critical("Unknown command %s" % line)

    logging.info("Answer: %s" % (depth * position))
if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
