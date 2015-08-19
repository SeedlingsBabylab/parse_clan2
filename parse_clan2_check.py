import sys
import os
import csv

from collections import Counter

clan_counts = []
parseclan_words = []

def parse_clan_count(path):
    with open(path, "rU") as file:
        for raw_line in file:
            line = raw_line.split()
            clan_counts.append((int(line[0]), line[1].lower()))
    #print clan_counts


def parse_parseclan_output(path):
    with open(path, "rU") as file:
        file.readline() # skip the header
        for raw_line in file:
            line = raw_line.split(",")
            parseclan_words.append(line[1].lower())
    #print parseclan_words

def print_usage():
    print "USAGE:\n"
    print "python parse_clan2_check.py clan_freq_output.txt parse_clan2_output.csv\n"

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print_usage()
        sys.exit(0)

    parse_clan_count(sys.argv[1])
    parse_parseclan_output(sys.argv[2])

    missing_words_parse = []
    missing_words_clan = []

    clan_count_sum = 0

    parseclan_counted = Counter(parseclan_words)

    for entry in clan_counts:
        clan_count_sum += entry[0]
        if entry[1] not in parseclan_words:
            missing_words_parse.append(entry[1])
            continue
        if parseclan_counted[entry[1]] != entry[0]:
            missing_words_parse.append(entry[1])

    for entry in parseclan_words:
        #clan_count_sum += entry[0]
        if entry not in [count[1] for count in clan_counts]:
            missing_words_clan.append(entry)
            continue
        if parseclan_counted[entry] != [count[0] for count in clan_counts]\
                [[count[1] for count in clan_counts].index(entry)]:
            missing_words_clan.append(entry)


    print parseclan_counted
    print "\nmissing from parse_clan2 output: {}".format(missing_words_parse)
    print "\nmissing from clan freq (but included in csv parse): {}\n".format(missing_words_clan)

    print "# of words (clan): " + str(clan_count_sum)
    print "# of words (parse_clan2): " + str(len(parseclan_words))

    with open("clan_counts.txt", "w") as file:
        for entry in clan_counts:
            file.write(str(entry) + "\n")

    with open("parseclan_counts.txt", "w") as file:
        for entry in parseclan_counted:
            file.write(str(parseclan_counted[entry]) + " " + str(entry) + "\n")