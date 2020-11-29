from sys import argv, exit
import csv
from cs50 import SQL

# Database
db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("usage: python import.py [cvs file]")
    exit(1)

# open csv file
file = open(argv[1], "r")
# read characters
charReader = csv.reader(file)

# start from second line
next(charReader, None)

# start reading
for row in charReader:
    for i in range(len(row)):
        #the name
        if i == 0:
            fullName = row[i].split()
            # middle name exist
            if(len(fullName) == 3):
                first = fullName[0]
                middle = fullName[1]
                last = fullName[2]
            #middle name does not exist
            elif(len(fullName) == 2):
                first = fullName[0]
                middle = None
                last = fullName[1]
        # final values
        parsedName = [first, middle, last]
        house = row[1]
        birth = row[2]

    # insert into a table
    db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
        parsedName[0], parsedName[1], parsedName[2], house, birth)

    # print(parsedName, house, birth)