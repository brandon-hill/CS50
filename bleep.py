# Censors certain specified words in a given string
from cs50 import get_string
from sys import argv


def main():
    text = get_text("What message would you like to censor?\n")
    dictionary = open(argv[1])
    banned = make_banned(dictionary)
    censor_text(text, banned)
    dictionary.close()


# Prompt user for text to censor
def get_text(prompt):
    while True:
        if len(argv) == 2:
            s = get_string(prompt)
            s_list = s.split()
            return s_list
        else:
            exit("Usage: python bleep.py dictionary")


# Make a list from the dictionary
def make_banned(dictionary):
    banned = []
    for x in dictionary:
        banned.append(x.strip())
    return banned


# Censor the text and print
def censor_text(text, banned):
    for x in text:
        bleeped = False

        # Loop through ban list and compare
        for j in banned:
            stripped = x.strip()
            if j.strip() == stripped.lower():
                bleeped = True
                print(("*" * len(j.strip())) + " ", end="")
        if bleeped == False:
            print(x, end=" ")
    print()


if __name__ == "__main__":
    main()
