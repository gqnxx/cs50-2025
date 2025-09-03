#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int coins = 0;
    int denoms[] = {25, 10, 5, 1};
    for (int i = 0; i < 4; i++)
    {
        coins += cents / denoms[i];
        cents %= denoms[i];
    }

    printf("%i\n", coins);
}
