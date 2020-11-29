from sys import argv, exit
import csv
from cs50 import SQL

# Database
db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("usage: python import.py [house name]")
    exit(1)

finalList = db.execute("SELECT first, middle, last, birth FROM students WHERE house == ? ORDER BY last, first", argv[1])

for key in finalList:
    if key['middle'] == None:
        print(f"{key['first']} {key['last']} born {key['birth']}")
    else:
        print(f"{key['first']} {key['middle']} {key['last']} born {key['birth']}")