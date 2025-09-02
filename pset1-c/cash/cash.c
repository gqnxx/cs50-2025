#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

    int cents = (int) roundf(dollars * 100.0f);
    int coins = 0;

    int denoms[] = {25, 10, 5, 1};
    for (int i = 0; i < 4; i++)
    {
        coins += cents / denoms[i];
        cents %= denoms[i];
    }

    printf("%i\n", coins);
}
