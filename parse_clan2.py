from Tkinter import Tk
from tkFileDialog import askopenfilename

import csv
import re
import collections

class Parser:

    def __init__(self, input_path):

        self.input_file = input_path
        self.output_file = input_path.replace(".cha", "_processed.csv")

        re1='((?:[a-z][a-z0-9_+]*))' # the word
        re2='(\\s+)'	            # whitespace
        re3='(&=)'	                # &
        re4='(.)'	                # utterance_type
        re5='(_)'	                # _
        re6='(.)'	                # object_present
        re7='(_)'	                # _
        re8='((?:[a-z][a-z0-9_]*))' # speaker

        self.entry_regx = re.compile(re1+re2+re3+re4+re5+re6+re7+re8, re.IGNORECASE | re.DOTALL)
        self.interval_regx = re.compile("(\d+_\d{3,})")

        self.words = []
        self.comments = []          # includes all the comments
        self.plain_comments = []    # not including subregion/silence comments
        self.parse()
        self.filter_comments()
        self.export()

    def parse(self):

        last_line = ""

        prev_interval = [None, None]
        curr_interval = [None, None]

        with open(self.input_file, "rU") as input:
            for index, line in enumerate(input):

                if line.startswith("*"):
                    interval_reg_result = self.interval_regx.search(line)

                    if interval_reg_result is None:
                        print "interval regx returned none. clan line: " + str(index)
                        last_line = line
                        continue
                     # rearrange previous and current intervals
                    prev_interval[0] = curr_interval[0]
                    prev_interval[1] = curr_interval[1]

                    # set the new curr_interval
                    interval_str = interval_reg_result.group()
                    interval = interval_str.split("_")
                    curr_interval[0] = int(interval[0])
                    curr_interval[1] = int(interval[1])

                    entries = self.entry_regx.findall(line)

                    if entries:
                        for entry in entries:
                            self.words.append([line[0:4],
                                               entry[0],            # word
                                               entry[3],            # utterance_type
                                               entry[5],            # object_present
                                               entry[7],            # speaker
                                               curr_interval[0],    # onset
                                               curr_interval[1]])   # offset

                    last_line = line

                if line.startswith("\t"):
                    interval_reg_result = self.interval_regx.search(line)

                    if interval_reg_result is None:
                        print "interval regx returned none. clan line: " + str(index)
                        last_line = line
                        continue
                    prev_interval[0] = curr_interval[0]
                    prev_interval[1] = curr_interval[1]

                    # set the new curr_interval
                    interval_str = interval_reg_result.group()
                    interval = interval_str.split("_")
                    curr_interval[0] = int(interval[0])
                    curr_interval[1] = int(interval[1])

                    entries = self.entry_regx.findall(line)

                    if entries:
                        for entry in entries:
                            self.words.append([last_line[0:4],
                                               entry[0],            # word
                                               entry[3],            # utterance_type
                                               entry[5],            # object_present
                                               entry[7],            # speaker
                                               curr_interval[0],    # onset
                                               curr_interval[1]])   # offset

                if (line.startswith("%com:") and ("|" not in line)):

                    comment = line.replace("%com:\t", "")\
                                  .replace("\"", "")\
                                  .replace("\n", "")

                    self.comments.append((comment, curr_interval[0], curr_interval[1]))
                if (line.startswith("%xcom:")) and ("|" not in line):
                    comment = line.replace("%xcom:\t", "")\
                                  .replace("\"", "")\
                                  .replace("\n", "")

                    self.comments.append((comment, curr_interval[0], curr_interval[1]))

        print self.words
        print self.comments

    def export(self):

        comment_queue = collections.deque(self.plain_comments)
        curr_comment = comment_queue.popleft()

        with open(self.output_file, "w") as output:
            writer = csv.writer(output)
            writer.writerow(["tier","word","utterance_type","object_present","speaker","timestamp","basic_level","comment"])
            for entry in self.words:
                print entry
                if entry[5] == curr_comment[1]:
                    writer.writerow([entry[0],
                                    entry[1],
                                    entry[2],
                                    entry[3],
                                    entry[4],
                                    "{}_{}".format(entry[5], entry[6]),
                                    " ",
                                    curr_comment[0]])

                    curr_comment = comment_queue.popleft()
                else:
                    writer.writerow([entry[0],
                                    entry[1],
                                    entry[2],
                                    entry[3],
                                    entry[4],
                                    "{}_{}".format(entry[5], entry[6]),
                                    " ",
                                    "NA"])


    def filter_comments(self):
        """
        Filter out all the subregion and silence comments,
        leaving behind only the actual comments
        """
        for comment in self.comments:
            if ("subregion" not in comment[0]) and\
                    ("silence" not in comment[0]):
                self.plain_comments.append(comment)

if __name__ == "__main__":

    Tk().withdraw()

    filename = askopenfilename(filetypes=[("cha files", "*.cha")])

    clanfile_parser = Parser(filename)


