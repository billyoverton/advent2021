#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

from util import Point, LineSegment
import math

LOG_LEVEL = logging.INFO

def main(input_file):
    lines = []

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            p1, p2 = line.split(" -> ")
            line = LineSegment(Point.from_iterable([int(x) for x in p1.split(',')]), Point.from_iterable([int(x) for x in p2.split(',')]))
            logging.debug("Line Input: %s, Slope: %s" % (line, line.slope()))
            lines.append(line)

    logging.debug('Filtered Lines: %s', '\n\t'.join(map(str, lines)))

    # Hashmap of Point -> coverd count
    points_covered = {}
    for line in lines:
        start_point = line.p1
        end_point = line.p2
        slope = line.slope()

        logging.debug("Walking Line %s with slope %s" % (line, slope))
        # Initialy add our start point
        if start_point in points_covered:
            points_covered[start_point] = points_covered[start_point] + 1
        else:
            points_covered[start_point] = 1

        while start_point != end_point:

            if slope == 0:
                # Horizontal Line
                direction = int(math.copysign(1, end_point.x - start_point.x))
                start_point = Point(start_point.x + direction, start_point.y)

            elif slope is math.nan:
                # Vertical Line
                direction = int(math.copysign(1, end_point.y - start_point.y))
                start_point = Point(start_point.x, start_point.y + direction)
            else:
                # Diagonal Line
                directionx = int(math.copysign(1, end_point.x - start_point.x))
                directiony = int(math.copysign(1, end_point.y - start_point.y))

                start_point = Point(start_point.x + directionx, start_point.y + directiony)

            # Add our new point
            if start_point in points_covered:
                points_covered[start_point] = points_covered[start_point] + 1
            else:
                points_covered[start_point] = 1

            logging.debug("Added point %s" % start_point)

    # Count all points covered by more than one line
    count = 0
    for point, value in points_covered.items():
        if value > 1:
            logging.debug("Counting point %s with value %s" % (point, value))
            count += 1

    logging.info("Answer: %s" % count)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
