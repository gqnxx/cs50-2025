CC=clang
CFLAGS=-Wall -Wextra -Werror -std=c11
INC=-I../pset1-c/local
LIB=../pset1-c/local/cs50.c

all: volume filter recover

volume: volume/volume.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

filter: filter/filter.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

recover: recover/recover.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $^ -o $@

.PHONY: clean
clean:
	rm -f volume filter recover
