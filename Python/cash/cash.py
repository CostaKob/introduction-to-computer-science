from cs50 import get_float
import math
from sys import exit

while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0:
        cents = round(dollars * 100)
        coins = 0

        coins += math.floor(cents / 25)
        remainingChange = cents % 25
        coins += math.floor(remainingChange / 10)
        remainingChange %= 10
        coins += math.floor(remainingChange / 5)
        remainingChange %= 5
        coins += math.floor(remainingChange / 1)
        remainingChange %= 1

        print(f"Coins: {coins}")
        exit(1)

