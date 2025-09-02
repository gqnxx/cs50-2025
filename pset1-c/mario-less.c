#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    for (int i = 1; i <= h; i++)
    {
        // left padding
        for (int s = 0; s < h - i; s++)
        {
            printf(" ");
        }
        // left hashes (single half-pyramid)
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
