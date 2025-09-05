def main():
    # Get dollars from user
    while True:
        try:
            dollars = float(input("Change owed: "))
            if dollars >= 0:
                break
        except ValueError:
            pass
    
    # Convert to cents and round to avoid floating point errors
    cents = round(dollars * 100)
    
    # Count coins
    coins = 0
    for coin_value in [25, 10, 5, 1]:  # quarters, dimes, nickels, pennies
        coins += cents // coin_value
        cents %= coin_value
    
    print(coins)

if __name__ == "__main__":
    main()
