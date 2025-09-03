CC=clang
CFLAGS=-Wall -Wextra -Werror -std=c11
INC=-I../pset1-c/local
LIB=../pset1-c/local/cs50.c

all: scrabble readability caesar substitution

scrabble: scrabble/scrabble.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

readability: readability/readability.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

caesar: caesar/caesar.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

substitution: substitution/substitution.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

.PHONY: clean
clean:
	rm -f scrabble readability caesar substitution
