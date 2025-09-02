CC = clang
CFLAGS = -std=c11 -Wall -Wextra -Werror
LIBS = -lcs50 -lm

PROGS = mario-less mario-more cash credit

all: $(PROGS)

mario-less: mario-less.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

mario-more: mario-more.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

cash: cash.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

credit: credit.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

# Local build (no libcs50 required)
local: mario-less-local mario-more-local cash-local credit-local

mario-less-local: mario-less.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o mario-less-local mario-less.c local/cs50.c -lm

mario-more-local: mario-more.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o mario-more-local mario-more.c local/cs50.c -lm

cash-local: cash.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o cash-local cash.c local/cs50.c -lm

credit-local: credit.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o credit-local credit.c local/cs50.c -lm

clean:
	rm -f $(PROGS) mario-*-local *-local *.o a.out
