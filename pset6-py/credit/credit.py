def main():
    number = input("Number: ")
    
    if is_valid(number):
        card_type = get_card_type(number)
        print(card_type)
    else:
        print("INVALID")

def is_valid(number):
    if not number.isdigit():
        return False
    
    # Luhn's algorithm
    total = 0
    reverse_digits = number[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Every second digit from right
            n *= 2
            if n > 9:
                n = n // 10 + n % 10
        total += n
    
    return total % 10 == 0

def get_card_type(number):
    length = len(number)
    
    if length == 15 and (number.startswith("34") or number.startswith("37")):
        return "AMEX"
    elif length == 16 and number.startswith(("51", "52", "53", "54", "55")):
        return "MASTERCARD"
    elif (length == 13 or length == 16) and number.startswith("4"):
        return "VISA"
    else:
        return "INVALID"

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
