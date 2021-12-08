#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    # List of (patterns, reading) values from input
    displays = []

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            pattern, reading = line.split(' | ')
            displays.append([pattern, reading])

    logging.debug("Display Inputs:\n%s" % "\n".join(map(str, displays)))

    display_sum = 0
    for display in displays:
        patterns = display[0].split()
        readings = display[1].split()

        identified_patterns = [None] * 10

        easy_patterns = [x for x in patterns if len(x) in [2,3,4,7]]
        unknown_six = [x for x in patterns if len(x) == 6 ]
        unknown_five = [x for x in patterns if len(x) == 5 ]

        # Find all the easy to find patterns
        for easy_pattern in easy_patterns:
            l = len(easy_pattern)
            if l == 2:
                identified_patterns[1] = {x for x in easy_pattern}
            elif l == 3:
                identified_patterns[7] = {x for x in easy_pattern}
            elif l == 4:
                identified_patterns[4] = {x for x in easy_pattern}
            elif l == 7:
                identified_patterns[8] = {x for x in easy_pattern}
            else:
                logging.critical("Unknown easy pattern %s" % easy_pattern)

        # Find the 6 value. It is the only 6 length value missing one of the wires from 1
        # Also this tells us what segment c and f are
        segment_c = None
        segment_f = None
        for pattern in unknown_six:
            set_value = {x for x in pattern}
            leftover_set = identified_patterns[1] - set_value
            if len(leftover_set) > 0:
                # We found our 6
                logging.debug("Found pattern %s for value 6" % pattern)
                identified_patterns[6] = set_value

                segment_f = (identified_patterns[1] - leftover_set).pop()
                logging.debug("Identified Segment f wire: %s" % segment_f)

                segment_c = leftover_set.pop()
                logging.debug("Identified Segment c wire: %s" % segment_c)

                unknown_six.remove(pattern)
                break

        # Identify all the 5 lengths now that we know segment c and f
        for pattern in unknown_five:
            set_value = {x for x in pattern}
            if segment_c not in set_value:
                # This is the 5
                logging.debug("Found pattern %s for value 5" % pattern)
                identified_patterns[5] = set_value
            elif segment_f not in set_value:
                # this is the 2
                logging.debug("Found pattern %s for value 2" % pattern)
                identified_patterns[2] = set_value
            else:
                # It has both so it must be the 3
                logging.debug("Found pattern %s for value 3" % pattern)
                identified_patterns[3] = set_value

        # Grab the unknown wires from the 4. which  gives us the b/d segments
        bd_segments = identified_patterns[4] - identified_patterns[1]

        # Identify the rest of the sixes
        for pattern in unknown_six:
            set_value = {x for x in pattern}
            leftover_set = bd_segments - set_value
            if len(leftover_set) > 0:
                # We found our zero as the d segment is off
                logging.debug("Found pattern %s for value 0" % pattern)
                identified_patterns[0] = set_value
            else:
                # The only number left is the 9
                logging.debug("Found pattern %s for value 9" % pattern)
                identified_patterns[9] = set_value

        logging.debug("Identified Patterns in order: %s: " % identified_patterns)

        value_digits = []
        for digit in readings:
            digit_set = {x for x in digit}
            for i in range(len(identified_patterns)):
                if digit_set == identified_patterns[i]:
                    value_digits.append(str(i))
                    break

        value = int("".join(value_digits))
        logging.debug("Display Reading: %s", value)
        display_sum += value

    logging.info("Answer: %s" % display_sum)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
