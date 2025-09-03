CC = clang
CFLAGS = -std=c11 -Wall -Wextra -Werror
LIBS = -lcs50 -lm

PROGS = hello mario-less mario-more cash credit

all: $(PROGS)

hello: hello.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

mario-less: mario-less.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

mario-more: mario-more.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

cash: cash.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

credit: credit.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

# Local build (no libcs50 required)
local: hello-local mario-less-local mario-more-local cash-local credit-local

hello-local: hello.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o hello-local hello.c local/cs50.c -lm

mario-less-local: mario-less.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o mario-less-local mario-less.c local/cs50.c -lm

mario-more-local: mario-more.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o mario-more-local mario-more.c local/cs50.c -lm

cash-local: cash.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o cash-local cash.c local/cs50.c -lm

credit-local: credit.c local/cs50.c
	$(CC) $(CFLAGS) -Ilocal -o credit-local credit.c local/cs50.c -lm

clean:
	rm -f $(PROGS) *-local *.o a.out
