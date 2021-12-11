#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO
STEP_COUNT = 100

NEIGHBOR_DIRECTIONS = [
    (0,1),
    (1,0),
    (-1,0),
    (0,-1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]

def get_neighbors(baseGrid, point):
    neighbor_points = list(map(lambda x: (point[0] + x[0], point[1] + x[1]), NEIGHBOR_DIRECTIONS))
    return list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < len(baseGrid[0]) and x[1] < len(baseGrid), neighbor_points))

def main(input_file):

    grid = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            grid.append([int(x) for x in line])

    logging.debug("Initial Grid:\n\n\t%s\n" % util.pretty_grid(grid, ysep="\n\t"))

    flash_count = 0
    for step in range(STEP_COUNT):
        going_to_flash = []
        already_flashed = []

        # Increment all values, mark ones that are going to flash
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                value = grid[y][x]+1
                if value > 9:
                    going_to_flash.append((x,y))
                grid[y][x] = value

        # Flash all the things
        while len(going_to_flash) > 0:
            point = going_to_flash.pop(0)
            already_flashed.append(point)
            flash_count += 1

            logging.debug("Flashing point: %s" % str(point))

            neighbors = get_neighbors(grid, point)
            filtered_neighbors = list(filter(lambda x: x not in already_flashed and x not in going_to_flash, neighbors))

            logging.debug("Filtered Neighbors: %s" % filtered_neighbors)

            for neighbor in filtered_neighbors:
                value = grid[neighbor[1]][neighbor[0]] + 1
                if value > 9:
                    going_to_flash.append(neighbor)
                grid[neighbor[1]][neighbor[0]] = value

        # Set the value for everything that flashed to zero
        for flashed in already_flashed:
            grid[flashed[1]][flashed[0]] = 0

        logging.debug("After Step %s:\n\n\t%s\n" % (step+1, util.pretty_grid(grid, ysep="\n\t")))

    logging.info("Answer: %s" % flash_count)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
