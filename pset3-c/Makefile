CC=clang
CFLAGS=-Wall -Wextra -Werror -std=c11
INC=-I../pset1-c/local
LIB=../pset1-c/local/cs50.c

all: sort plurality runoff tideman

sort: sort/sort.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

plurality: plurality/plurality.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

runoff: runoff/runoff.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

tideman: tideman/tideman.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

.PHONY: clean
clean:
	rm -f sort plurality runoff tideman
