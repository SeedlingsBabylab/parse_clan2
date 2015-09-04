import csv
import sys
import os

import parse_clan2


def print_usage():
    print "USAGE:\n"
    print "$: python batch_parse_clan2.py /folder/with/cha/files  /output/folder"


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print_usage()
        sys.exit(0)

    input = sys.argv[1]
    output = sys.argv[2]



    for file in os.listdir(input):
        file_parser = parse_clan2.Parser(os.path.join(input, file), output)