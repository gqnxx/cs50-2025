import csv
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)
    
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]
    
    # Read database
    database = []
    with open(database_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            database.append(row)
    
    # Get STR names (all columns except 'name')
    strs = list(database[0].keys())[1:]
    
    # Read DNA sequence
    with open(sequence_file, 'r') as f:
        sequence = f.read().strip()
    
    # Count STR occurrences
    str_counts = {}
    for str_name in strs:
        str_counts[str_name] = longest_match(sequence, str_name)
    
    # Check for matches in database
    for person in database:
        match = True
        for str_name in strs:
            if int(person[str_name]) != str_counts[str_name]:
                match = False
                break
        if match:
            print(person['name'])
            return
    
    print("No match")

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    
    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
