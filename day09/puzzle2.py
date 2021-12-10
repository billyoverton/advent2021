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

def get_neighbors(baseGrid, point):
    neighbor_points = list(map(lambda x: (point[0] + x[0], point[1] + x[1]), NEIGHBOR_DIRECTIONS))
    return list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < len(baseGrid[0]) and x[1] < len(baseGrid), neighbor_points))

def get_neighbor_values(baseGrid, point):
    valid_points = get_neighbors(baseGrid, point)
    return list(map(lambda x: baseGrid[x[1]][x[0]], valid_points))

def get_basin_points(baseGrid, low_point):
    to_visit = [low_point]
    visited = []

    while len(to_visit) > 0:
        poi = to_visit.pop(0)
        visited.append(poi)

        neighbors = get_neighbors(baseGrid, poi)
        for neighbor in neighbors:
            value = int(baseGrid[neighbor[1]][neighbor[0]])
            if value < 9 and neighbor not in visited and neighbor not in to_visit:
                to_visit.append(neighbor)

    logging.debug("Basin: %s, Size: %s, Points: %s" % (low_point, len(visited), visited))
    return visited

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

            if all([ x>value for x in neighbor_values]):
                # Lower than all neighbors
                low_points.append(point)
                logging.debug("Lowpoint found: %s, Value: %s" % (point, value))


    logging.debug("All lowpoints: %s" % low_points)

    size_map = {}
    for low_point in low_points:
        basin = get_basin_points(cave_floor, low_point)
        size = len(basin)
        size_map[low_point] = size
        logging.debug("Basin at point %s has size %s" % (low_point, size))

    ordered_by_size = sorted(size_map.items(), key=lambda x: x[1])

    logging.debug("Basin Sizes: %s" % ordered_by_size)

    answer = ordered_by_size.pop()[1] * ordered_by_size.pop()[1] * ordered_by_size.pop()[1]

    logging.info("Answer: %s" % answer)


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
