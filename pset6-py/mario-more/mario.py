def main():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
        except ValueError:
            pass
    
    for i in range(height):
        left_spaces = " " * (height - i - 1)
        left_hashes = "#" * (i + 1)
        gap = "  "
        right_hashes = "#" * (i + 1)
        print(left_spaces + left_hashes + gap + right_hashes)

if __name__ == "__main__":
    main()
