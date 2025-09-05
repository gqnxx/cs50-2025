#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average of RGB values
            float avg = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            uint8_t gray_value = (uint8_t)round(avg);
            
            image[i][j].rgbtRed = gray_value;
            image[i][j].rgbtGreen = gray_value;
            image[i][j].rgbtBlue = gray_value;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float red_sum = 0, green_sum = 0, blue_sum = 0;
            int count = 0;
            
            // Check surrounding pixels (3x3 grid)
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;
                    
                    // Check if pixel is within bounds
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        red_sum += copy[ni][nj].rgbtRed;
                        green_sum += copy[ni][nj].rgbtGreen;
                        blue_sum += copy[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }
            
            // Calculate average and assign
            image[i][j].rgbtRed = (uint8_t)round(red_sum / count);
            image[i][j].rgbtGreen = (uint8_t)round(green_sum / count);
            image[i][j].rgbtBlue = (uint8_t)round(blue_sum / count);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create copy of original image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    
    // Sobel kernels
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gx_red = 0, gx_green = 0, gx_blue = 0;
            int gy_red = 0, gy_green = 0, gy_blue = 0;
            
            // Apply Sobel operator
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;
                    
                    // Treat out-of-bounds as black
                    uint8_t red = 0, green = 0, blue = 0;
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        red = copy[ni][nj].rgbtRed;
                        green = copy[ni][nj].rgbtGreen;
                        blue = copy[ni][nj].rgbtBlue;
                    }
                    
                    gx_red += gx[di + 1][dj + 1] * red;
                    gx_green += gx[di + 1][dj + 1] * green;
                    gx_blue += gx[di + 1][dj + 1] * blue;
                    
                    gy_red += gy[di + 1][dj + 1] * red;
                    gy_green += gy[di + 1][dj + 1] * green;
                    gy_blue += gy[di + 1][dj + 1] * blue;
                }
            }
            
            // Calculate final values
            int final_red = (int)round(sqrt(gx_red * gx_red + gy_red * gy_red));
            int final_green = (int)round(sqrt(gx_green * gx_green + gy_green * gy_green));
            int final_blue = (int)round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));
            
            // Cap at 255
            image[i][j].rgbtRed = (final_red > 255) ? 255 : final_red;
            image[i][j].rgbtGreen = (final_green > 255) ? 255 : final_green;
            image[i][j].rgbtBlue = (final_blue > 255) ? 255 : final_blue;
        }
    }
}
