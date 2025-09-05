import string

def main():
    text = input("Text: ")
    
    # Count letters, words, and sentences
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    
    # Calculate Coleman-Liau index
    L = letters / words * 100
    S = sentences / words * 100
    
    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)
    
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")

def count_letters(text):
    return sum(1 for c in text if c.isalpha())

def count_words(text):
    return len(text.split())

def count_sentences(text):
    return sum(1 for c in text if c in '.!?')

if __name__ == "__main__":
    main()
