#include <cs50.h>
#include <stdio.h>
#include <stdbool.h>

static bool luhn_valid(long number)
{
    int sum = 0;
    int pos = 0;
    while (number > 0)
    {
        int d = number % 10;
        if (pos % 2 == 1)
        {
            int x = d * 2;
            sum += (x / 10) + (x % 10);
        }
        else
        {
            sum += d;
        }
        number /= 10;
        pos++;
    }
    return (sum % 10) == 0;
}

int main(void)
{
    long n;
    do
    {
        n = get_long("Number: ");
    }
    while (n <= 0);

    int len = 0;
    long tmp = n;
    while (tmp > 0)
    {
        tmp /= 10;
        len++;
    }

    tmp = n;
    while (tmp >= 100)
    {
        tmp /= 10;
    }
    int first2 = (int) tmp;
    int first = first2 / 10;

    if (!luhn_valid(n))
    {
        printf("INVALID\n");
        return 0;
    }

    if (len == 15 && (first2 == 34 || first2 == 37))
    {
        printf("AMEX\n");
    }
    else if (len == 16 && first2 >= 51 && first2 <= 55)
    {
        printf("MASTERCARD\n");
    }
    else if ((len == 13 || len == 16) && first == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
