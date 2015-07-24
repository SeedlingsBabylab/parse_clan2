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
        self.interval_regx = re.compile("(\025\d+_\d+)")

        self.skipping = False
        self.begin_skip_start = None
        self.words = []
        self.comments = []          # includes all the comments
        self.plain_comments = []    # not including subregion/silence comments
        if not self.check_intervals():
            return
        self.parse()
        self.filter_comments()
        self.export()

    def parse(self):
        last_line = ""
        multi_line = ""

        prev_interval = [None, None]
        curr_interval = [None, None]

        with open(self.input_file, "rU") as input:
            for index, line in enumerate(input):

                if (line.startswith("%com:") and ("|" not in line)):
                    if "begin skip" in line:
                        print "Begin skip found in line# " + str(index) + "\n\n"
                        self.skipping = True
                        self.begin_skip_start = index
                        continue
                    if "end skip" in line:
                        self.skipping = False
                        self.begin_skip_start = None
                        continue
                    # get rid of quotation marks, %com's and newlines
                    comment = line.replace("%com:\t", "")\
                                  .replace("\"", "")\
                                  .replace("\n", "")

                    self.comments.append((comment, curr_interval[0], curr_interval[1]))

                if (line.startswith("%xcom:")) and ("|" not in line):
                    if "begin skip" in line:
                        print "Begin skip starts at line# " + str(index) + "\n\n"
                        self.skipping = True
                        self.begin_skip_start = index
                        continue
                    if "end skip" in line:
                        #print "Found *end skip*"
                        self.skipping = False
                        self.begin_skip_start = None
                        continue
                    # get rid of quotation marks, %xcom's and newlines
                    comment = line.replace("%xcom:\t", "")\
                                  .replace("\"", "")\
                                  .replace("\n", "")

                    self.comments.append((comment, curr_interval[0], curr_interval[1]))

                #
                # if self.skipping:
                #     print "skipping line: " + line
                #     continue

                if line.startswith("*"):

                    # reset multi_line
                    multi_line = ""
                    interval_reg_result = self.interval_regx.search(line)

                    if interval_reg_result is None:
                        #print "interval regx returned none. clan line: " + str(index)
                        last_line = line
                        continue
                     # rearrange previous and current intervals
                    prev_interval[0] = curr_interval[0]
                    prev_interval[1] = curr_interval[1]

                    # set the new curr_interval
                    interval_str = interval_reg_result.group().replace("\025", "")
                    interval = interval_str.split("_")
                    curr_interval[0] = int(interval[0])
                    curr_interval[1] = int(interval[1])

                    entries = self.entry_regx.findall(line)

                    if entries:
                        if self.skipping:
                            print "Object word was found in a skip region. Fix this in the .cha file. Line# " + str(index)
                            #print "Begin skip starts at line# " + str(self.begin_skip_start)
                            print "line: " + line
                            continue
                        else:
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
                        #print "interval regx returned none. clan line: " + str(index)
                        multi_line += line
                        #print multi_line
                        continue

                    prev_interval[0] = curr_interval[0]
                    prev_interval[1] = curr_interval[1]

                    # set the new curr_interval
                    interval_str = interval_reg_result.group().replace("\025", "")
                    interval = interval_str.split("_")
                    curr_interval[0] = int(interval[0])
                    curr_interval[1] = int(interval[1])

                    entries = self.entry_regx.findall(multi_line + line)

                    if entries:
                        if self.skipping:
                            print "Object word was found in a skip region. Fix this in the .cha file. Line# " + str(index)
                            #print "Begin skip starts at line# " + str(self.begin_skip_start)
                            print "line: " + line
                            continue
                        for entry in entries:
                            self.words.append([last_line[0:4],
                                               entry[0],            # word
                                               entry[3],            # utterance_type
                                               entry[5],            # object_present
                                               entry[7],            # speaker
                                               curr_interval[0],    # onset
                                               curr_interval[1]])   # offset

                    multi_line = "" # empty the mutiple line buffer


        #print self.words
        #print self.comments

    def export(self):

        comment_queue = collections.deque(self.plain_comments)
        curr_comment = comment_queue.popleft()

        with open(self.output_file, "w") as output:
            writer = csv.writer(output)
            writer.writerow(["tier","word","utterance_type","object_present","speaker","timestamp","basic_level","comment"])
            for entry in self.words:
                #print entry
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

    def check_intervals(self):
        """
        Makes sure there is at most 1 timestamp interval on a line
        :return: returns false if we found a problem
        """

        with open(self.input_file, "rU") as input:
            for index, line in enumerate(input):
                regx_result = self.interval_regx.findall(line)
                if regx_result:
                    if len(regx_result) > 1:
                        print "Found more than 1 interval on a single CLAN line:   line #" + str(index)
                        return False
                    else:
                        continue
            return True

if __name__ == "__main__":

    Tk().withdraw()

    filename = askopenfilename(filetypes=[("cha files", "*.cha")])

    clanfile_parser = Parser(filename)


