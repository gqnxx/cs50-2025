// CS50 pset2: Readability (Coleman-Liau)
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    string text = get_string("Text: ");

    int letters = 0, words = 0, sentences = 0;
    for (char *p = text; *p; ++p)
    {
        unsigned char c = (unsigned char)*p;
        if (isalpha(c))
            letters++;
        if (c == ' ')
            words++;
        if (c == '.' || c == '!' || c == '?')
            sentences++;
    }
    // Count the last word if input isn't empty
    if (text[0] != '\0')
        words++;

    // Avoid division by zero
    if (words == 0)
    {
        printf("Before Grade 1\n");
        return 0;
    }

    double L = (letters * 100.0) / words;
    double S = (sentences * 100.0) / words;
    double idx = 0.0588 * L - 0.296 * S - 15.8;

    int grade = (int)(idx >= 0 ? idx + 0.5 : idx - 0.5); // round to nearest

    if (grade < 1)
        printf("Before Grade 1\n");
    else if (grade >= 16)
        printf("Grade 16+\n");
    else
        printf("Grade %d\n", grade);

    return 0;
}
