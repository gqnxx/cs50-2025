CC=clang
CFLAGS=-Wall -Wextra -Werror -std=c11
INC=-I../pset1-c/local
LIB=../pset1-c/local/cs50.c

all: inheritance speller

inheritance: inheritance/inheritance.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

speller: speller/speller.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

.PHONY: clean
clean:
	rm -f inheritance speller
