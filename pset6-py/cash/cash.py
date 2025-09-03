def main():
    # TODO: implement Cash in Python
    cents = int(input("Change owed (cents): "))
    coins = 0
    for v in [25, 10, 5, 1]:
        coins += cents // v
        cents %= v
    print(coins)

if __name__ == "__main__":
    main()
