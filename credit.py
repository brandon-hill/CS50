# Check the validity and type of a card number
from cs50 import get_int


def main():
    card = check_usage("Number: ")
    if check_sum(card):
        check_type(card)
    else:
        print("INVALID")


# Ensure proper usage
def check_usage(prompt):
    while True:
        n = get_int(prompt)
        if n > 0:
            return n


# Check number with Luhn's Algorithm
def check_sum(card):
    numCard = card
    evenTotal = 0
    oddTotal = 0

    # Iterate through cards digits and operating on each according to the algorithm
    for i in range(len(str(card))):
        if i % 2 != 0:
            even = divmod(numCard, 10)
            evenTotal = evenTotal + sum_digits(even[1] * 2)
            numCard //= 10

        else:
            odd = divmod(numCard, 10)
            oddTotal = oddTotal + odd[1]
            numCard //= 10

    # Add the totals of the even and odd numbers and check if divisible by 10
    if (evenTotal + oddTotal) % 10 == 0:
        return True
    else:
        return False


# From stackoverflow, URL: 'https://stackoverflow.com/questions/14939953/sum-the-digits-of-a-number-python'
def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


# Checks the card type based on number length and the first two digits
def check_type(card):
    subCard = slice(2)
    firstTwoDigits = int(str(card)[subCard])
    if len(str(card)) == 15 and firstTwoDigits == 34 or firstTwoDigits == 37:
        print("AMEX")
    elif len(str(card)) == 13:
        print("VISA")
    elif len(str(card)) == 16:
        if firstTwoDigits > 50 and firstTwoDigits < 56 or firstTwoDigits == 22:
            print("MASTERCARD")
        elif firstTwoDigits > 39 and firstTwoDigits < 50:
            print("VISA")
    else:
        print("INVALID")
        return 0


if __name__ == "__main__":
    main()