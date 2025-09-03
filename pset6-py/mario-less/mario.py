def main():
    # TODO: implement Mario less in Python
    h = int(input("Height: "))
    for i in range(1, h+1):
        print(" " * (h-i) + "#" * i)

if __name__ == "__main__":
    main()
