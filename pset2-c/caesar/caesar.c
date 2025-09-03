// CS50 pset2: Caesar
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

static int is_digits(const char *s)
{
    if (!s || !*s) return 0;
    for (const char *p = s; *p; ++p)
        if (!isdigit((unsigned char)*p)) return 0;
    return 1;
}

int main(int argc, string argv[])
{
    if (argc != 2 || !is_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]) % 26;
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");
    for (char *p = plaintext; *p; ++p)
    {
        unsigned char c = (unsigned char)*p;
        if (isupper(c))
            putchar(((c - 'A' + key) % 26) + 'A');
        else if (islower(c))
            putchar(((c - 'a' + key) % 26) + 'a');
        else
            putchar(c);
    }
    putchar('\n');
    return 0;
}
