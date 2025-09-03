// CS50 pset2: Scrabble
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

static const int POINTS[26] = {
    1, 3, 3, 2, 1, 4, 2, 4, 1, 8,
    5, 1, 3, 1, 1, 3, 10, 1, 1, 1,
    1, 4, 4, 8, 4, 10
};

int score_word(const char *s)
{
    int total = 0;
    for (const char *p = s; *p; ++p)
    {
        if (isalpha((unsigned char)*p))
        {
            int idx = toupper((unsigned char)*p) - 'A';
            total += POINTS[idx];
        }
    }
    return total;
}

int main(void)
{
    string a = get_string("Player 1: ");
    string b = get_string("Player 2: ");

    int sa = score_word(a);
    int sb = score_word(b);

    if (sa > sb)
    {
        printf("Player 1 wins!\n");
    }
    else if (sb > sa)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
    return 0;
}
