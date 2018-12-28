import csv
import sys
import os
from shutil import move

import parse_clan2

''' to run this on all cha files in subject_files '''
## could use files from scatter?
# 1. get path from scatter path
# 2. move processed.csv to processed_no_id.csv
# 3. Parse sparse_code.cha, no output

def print_usage():
    print "USAGE:\n"
    print "$: python batch_parse_clan2.py /folder/with/cha/files  /output/folder"

def process_folder(folder):
    # for file in os.listdir(folder):
        # if file.endswith("processed.csv"):
            # print("processed", file)
            # move(os.path.join(folder,file), os.path.join(folder, file.replace(".csv", "_no_id.csv")))
    for file in os.listdir(folder):
        if file.endswith("sparse_code.cha"):
            print("sparse", file)
            file_parser = parse_clan2.Parser(os.path.join(folder, file))

if __name__ == "__main__":

    # if len(sys.argv) != 3:
    #     print_usage()
    #     sys.exit(0)

    cha_paths = sys.argv[1]
    # output = sys.argv[2]

    with open(cha_paths, 'r') as f:
        lines = f.readlines()

        for line in lines:

            print(line)
            line = line.strip()
            process_folder(line)

    # for file in os.listdir(input):
    #     file_parser = parse_clan2.Parser(os.path.join(input, file), output)
