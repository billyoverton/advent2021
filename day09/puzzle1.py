#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

NEIGHBOR_DIRECTIONS = [
    (0,1),
    (1,0),
    (-1,0),
    (0,-1)
]

def get_neighbor_values(baseGrid, point):
    neighbor_points = map(lambda x: (point[0] + x[0], point[1] + x[1]), NEIGHBOR_DIRECTIONS)
    valid_points = filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < len(baseGrid[0]) and x[1] < len(baseGrid), neighbor_points)
    return list(map(lambda x: baseGrid[x[1]][x[0]], valid_points))


def main(input_file):

    cave_floor = []

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            cave_floor.append(list(line))

    logging.debug("Floor Grid:\n\t%s" % util.pretty_grid(cave_floor, ysep="\n\t"))

    low_points = []
    risk_sum = 0

    neighbor_directions = [
        (0,1),
        (1,0),
        (-1,0),
        (0,-1)
    ]

    for y in range(len(cave_floor)):
        for x in range(len(cave_floor[y])):
            point = (x, y)
            value = cave_floor[y][x]

            neighbor_values = get_neighbor_values(cave_floor, point)
            logging.debug("Neighbor values for point %s: %s" % (point, neighbor_values))

            if all([ x>value for x in neighbor_values]):
                # Lower than all neighbors
                low_points.append(point)
                logging.debug("Lowpoint found: %s, Value: %s" % (point, value))
                risk_sum += (int(value) + 1)


    logging.info("Answer: %s" % risk_sum)
if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
