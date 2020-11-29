from sys import argv, exit
import csv

if len(argv) != 3:
    print("usage: python dna.py [cvs file] [file.txt]")
    exit(1)
# STRs array
strs = []

# open database and sequence
database = open(argv[1], "r")
sequence = open(argv[2], "r")

# read database
dbReader = csv.reader(database)

# read sequences file
sequencesReader = sequence.read()

# read STRs from the first line and place them to list
for row in dbReader:
    for i in row:
        if i != "name":
            strs.append(i)
    break

# array for counters with same length as strs array
counters = [0] * len(strs)
tmpCounters = [0] * len(strs)

# calculation
# iterate on every STR in str array
for j in range(len(strs)):
    counters[j] = 0
# iterate on every charachter in txt file
    for k in range(len(sequencesReader) - len(strs[j])):
        # calculations
        str = sequencesReader[k : len(strs[j]) + k] == strs[j]
        next = sequencesReader[k + len(strs[j]) : k + len(strs[j]) * 2] == strs[j]
        prev = sequencesReader[k - len(strs[j]) : k] == strs[j]
        # match
        if str:
            # single str or first str
            if not prev:
                if not next:
                    # print("single")
                    if counters[j] == 0 or counters[j] == 1:
                        counters[j] = 1
                else:
                    tmpCounters[j] = 0
                    tmpCounters[j] += 1
            # middle str
            if next and prev:
                tmpCounters[j] += 1
            # last str
            if not next and prev:
                tmpCounters[j] += 1
                if tmpCounters[j] > counters[j]:
                    counters[j] = tmpCounters[j]
                    tmpCounters[j] = 0

# compare
for row in dbReader:
    matchCounter = 0
    for x in range(len(row)):
        if x != 0:
            if int(row[x]) == counters[x-1]:
                matchCounter += 1
                if matchCounter == len(strs):
                    print(row[0])
                    exit(0)
print("No match")
