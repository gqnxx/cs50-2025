#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    // TODO: implement dictionary-based spell checker
    // CS50 pset5: Speller
#include <ctype.h>
#include <stdio.h>
#include <sys/resource.h>
#include <sys/time.h>

#include "dictionary.h"

#undef calculate
#undef getrusage

double calculate(const struct rusage *b, const struct rusage *a);

int main(int argc, char *argv[])
{
    struct rusage before, after;

    if (argc != 2 && argc != 3)
    {
        printf("Usage: speller [dictionary] text
");
        return 1;
    }

    char *dictionary = (argc == 3) ? argv[1] : DICTIONARY;
    char *text = (argc == 3) ? argv[2] : argv[1];

    printf("
LOADING...
");
    getrusage(RUSAGE_SELF, &before);
    bool loaded = load(dictionary);
    getrusage(RUSAGE_SELF, &after);

    if (!loaded)
    {
        printf("Could not load %s.
", dictionary);
        return 1;
    }

    printf("
LOADED!
");

    FILE *file = fopen(text, "r");
    if (file == NULL)
    {
        printf("Could not open %s.
", text);
        unload();
        return 1;
    }

    printf("
MISSPELLED WORDS

");
    getrusage(RUSAGE_SELF, &before);

    int index = 0, misspellings = 0, words = 0;
    char word[LENGTH + 1];

    for (int c = fgetc(file); c != EOF; c = fgetc(file))
    {
        if (isalpha(c) || (c == ''' && index > 0))
        {
            word[index] = c;
            index++;

            if (index > LENGTH)
            {
                while ((c = fgetc(file)) != EOF && isalpha(c));
                index = 0;
            }
        }
        else if (index > 0)
        {
            word[index] = '\0';
            words++;

            if (!check(word))
            {
                printf("%s
", word);
                misspellings++;
            }

            index = 0;
        }
    }

    if (ferror(file))
    {
        fclose(file);
        printf("Error reading %s.
", text);
        unload();
        return 1;
    }

    fclose(file);

    getrusage(RUSAGE_SELF, &after);

    printf("
WORDS MISSPELLED:     %d
", misspellings);
    printf("WORDS IN DICTIONARY:  %d
", size());
    printf("WORDS IN TEXT:        %d
", words);
    printf("TIME IN load:         %.2f
", calculate(&before, &after));

    getrusage(RUSAGE_SELF, &before);
    bool unloaded = unload();
    getrusage(RUSAGE_SELF, &after);

    if (!unloaded)
    {
        printf("Could not unload %s.
", dictionary);
        return 1;
    }

    printf("TIME IN check:        %.2f
", calculate(&before, &after));
    printf("TIME IN size:         %.2f
", 0.00);
    printf("TIME IN unload:       %.2f
", calculate(&before, &after));
    printf("TIME IN TOTAL:        %.2f

", 0.00);

    return 0;
}

double calculate(const struct rusage *b, const struct rusage *a)
{
    if (b == NULL || a == NULL)
    {
        return 0.0;
    }
    else
    {
        return ((((a->ru_utime.tv_sec * 1000000 + a->ru_utime.tv_usec) -
                  (b->ru_utime.tv_sec * 1000000 + b->ru_utime.tv_usec)) +
                 ((a->ru_stime.tv_sec * 1000000 + a->ru_stime.tv_usec) -
                  (b->ru_stime.tv_sec * 1000000 + b->ru_stime.tv_usec)))
                / 1000000.0);
    }
}
    return 0;
}
