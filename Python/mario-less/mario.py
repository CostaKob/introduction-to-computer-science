from cs50 import get_int
from sys import exit

while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        for i in range(height):
            space = height - i
            while space > 1:
                print(" ", end="")
                space -= 1
            for j in range(i+1):
                print("#", end="")
            print()
        exit(0)