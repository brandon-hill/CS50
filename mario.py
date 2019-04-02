# Print a staircase of blocks sized by user input
from cs50 import get_int


def main():
    height = get_positive_int("Height: ")
    build(height)


# Prompt user for height
def get_positive_int(prompt):
    while True:
        n = get_int(prompt)
        if n > 0 and n < 9:
            return n

# Print spaces and blocks
def build(height):
    for x in range(height):

        for y in range(height - 1 - x):
            print(" ", end='')

        for y in range(x + 1):
            print("#", end='')

        print()


if __name__ == "__main__":
    main()
