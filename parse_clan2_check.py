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
            clan_counts.append((int(line[0]), line[1]))
    print clan_counts


def parse_parseclan_output(path):
    with open(path, "rU") as file:
        file.readline() # skip the header
        for raw_line in file:
            line = raw_line.split(",")
            parseclan_words.append(line[1])
    print parseclan_words

if __name__ == "__main__":

    parse_clan_count(sys.argv[1])
    parse_parseclan_output(sys.argv[2])

    missing_words = []
    clan_count_sum = 0

    parseclan_counted = Counter(parseclan_words)

    for entry in clan_counts:
        clan_count_sum += entry[0]
        if entry[1] not in parseclan_words:
            missing_words.append(entry[1])
            continue
        if parseclan_counted[entry[1]] != entry[0]:
            missing_words.append(entry[1])


    print "\nmissing words: " + str(missing_words)
    print
    print "# of words (clan): " + str(clan_count_sum)
    print "# of words (parse_clan2): " + str(len(parseclan_words))