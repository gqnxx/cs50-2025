// CS50 pset4: Recover
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    uint8_t buffer[512];
    FILE *img = NULL;
    int counter = 0;
    char filename[8];

    while (fread(buffer, 512, 1, file) == 1)
    {
        // Check for JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous file if open
            if (img != NULL)
            {
                fclose(img);
            }

            // Create new JPEG file
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter++;
        }

        // Write to current file if one is open
        if (img != NULL)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    // Close files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(file);

    return 0;
}
