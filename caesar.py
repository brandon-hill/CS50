# Encipher a message using Caesar's cipher
from cs50 import get_string
from sys import argv


# Ensure proper usage
if len(argv) != 2:
    exit("Usage: python caesar.py k")

else:
    # Get key from user
    k = int(argv[1])
    # Get plaintext from user
    p = get_string("plaintext: ")
    # Begin printing ciphertext
    print("ciphertext: ", end="")
    # Loop through plaintext preserving case and shifting by k
    for c in p:
        if c.isalpha():
            if c.isupper():
                print(chr((ord(c) - ord('A') + k) % 26 + ord('A')), end="")
            else:
                print(chr((ord(c) - ord('a') + k) % 26 + ord('a')), end="")
        else:
            print(c, end="")
    print()
