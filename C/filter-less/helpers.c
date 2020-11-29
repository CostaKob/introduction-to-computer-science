#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = round(((float)image[i][j].rgbtBlue + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtRed) / 3);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaGreen, sepiaBlue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            sepiaRed = round((image[i][j].rgbtRed * 0.393) + (image[i][j].rgbtGreen * 0.769) + (image[i][j].rgbtBlue * 0.189));
            sepiaGreen = round((image[i][j].rgbtRed * 0.349) + (image[i][j].rgbtGreen * 0.686) + (image[i][j].rgbtBlue * 0.168));
            sepiaBlue = round((image[i][j].rgbtRed * 0.272) + (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtBlue * 0.131));

            if (sepiaRed < 0)
            {
                image[i][j].rgbtRed = 0;
            }
            else if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            if (sepiaGreen < 0)
            {
                image[i][j].rgbtGreen = 0;
            }
            else if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }

            if (sepiaBlue < 0)
            {
                image[i][j].rgbtBlue = 0;
            }
            else if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            tmp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // copy of the image
    RGBTRIPLE bluredImage[height][width];

    int numofpixels, red, green, blue;
    int counter;
    float redsum, greensum, bluesum;

    RGBTRIPLE corner[2][2];
    RGBTRIPLE lredge[3][2];
    RGBTRIPLE udedge[2][3];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            redsum = greensum = bluesum = 0;
            counter = 0;

            //if corner
            if ((i == 0 && j == 0) || (i == 0 && j == (width - 1)) || (i == (height - 1) && j == 0) || (i == (height - 1) && j == (width - 1)))
            {
                //left up corner
                if (i == 0 && j == 0)
                {
                    corner[0][0] = image[i][j];
                    corner[0][1] = image[i][j + 1];
                    corner[1][0] = image[i + 1][j];
                    corner[1][1] = image[i + 1][j + 1];
                }

                //right up corner
                else if (i == 0 && j == (width - 1))
                {
                    corner[0][0] = image[i][j - 1];
                    corner[0][1] = image[i][j];
                    corner[1][0] = image[i + 1][j - 1];
                    corner[1][1] = image[i + 1][j];
                }

                //left down corner
                else if (i == (height - 1) && j == 0)
                {
                    corner[0][0] = image[i - 1][j];
                    corner[0][1] = image[i - 1][j + 1];
                    corner[1][0] = image[i][j];
                    corner[1][1] = image[i][j + 1];
                }

                //right down corner
                else if (i == (height - 1) && j == (width - 1))
                {
                    corner[0][0] = image[i - 1][j - 1];
                    corner[0][1] = image[i - 1][j];
                    corner[1][0] = image[i][j - 1];
                    corner[1][1] = image[i][j];
                }

                for (int y = 0; y < 2; y++)
                {
                    for (int x = 0; x < 2; x++)
                    {
                        redsum += corner[y][x].rgbtRed;
                        greensum += corner[y][x].rgbtGreen;
                        bluesum += corner[y][x].rgbtBlue;
                        counter ++;
                    }
                }
            }

            //if edge left or right edge
            else if ((j == 0 && i != 0 && i != (height - 1)) || (j == (width - 1) && i != 0 && i != (height - 1)))
            {
                //left edge
                if (j == 0 && i != 0 && i != (height - 1))
                {
                    lredge[0][0] = image[i - 1][j];
                    lredge[0][1] = image[i - 1][j + 1];
                    lredge[1][0] = image[i][j];
                    lredge[1][1] = image[i][j + 1];
                    lredge[2][0] = image[i + 1][j];
                    lredge[2][1] = image[i + 1][j + 1];
                }
                //right edge
                else if (j == (width - 1) && i != 0 && i != (height - 1))
                {
                    lredge[0][0] = image[i - 1][j - 1];
                    lredge[0][1] = image[i - 1][j];
                    lredge[1][0] = image[i][j - 1];
                    lredge[1][1] = image[i][j];
                    lredge[2][0] = image[i + 1][j - 1];
                    lredge[2][1] = image[i + 1][j];
                }

                for (int y = 0; y < 3; y++)
                {
                    for (int x = 0; x < 2; x++)
                    {
                        redsum += lredge[y][x].rgbtRed;
                        greensum += lredge[y][x].rgbtGreen;
                        bluesum += lredge[y][x].rgbtBlue;
                        counter ++;
                    }
                }
            }
            // up and down edge
            else if ((i == 0 && j != 0 && j != (width - 1)) || (i == (height - 1) && j != 0 && j != (width - 1)))
            {
                //up edge
                if (i == 0 && j != 0 && j != (width - 1))
                {
                    udedge[0][0] = image[i][j - 1];
                    udedge[0][1] = image[i][j];
                    udedge[0][2] = image[i][j + 1];
                    udedge[1][0] = image[i + 1][j - 1];
                    udedge[1][1] = image[i + 1][j];
                    udedge[1][2] = image[i + 1][j + 1];
                }

                //down edge
                else if (i == (height - 1) && j != 0 && j != (width - 1))
                {
                    udedge[0][0] = image[i - 1][j - 1];
                    udedge[0][1] = image[i - 1][j];
                    udedge[0][2] = image[i - 1][j + 1];
                    udedge[1][0] = image[i][j - 1];
                    udedge[1][1] = image[i][j];
                    udedge[1][2] = image[i][j + 1];
                }

                for (int y = 0; y < 2; y++)
                {
                    for (int x = 0; x < 3; x++)
                    {
                        redsum += udedge[y][x].rgbtRed;
                        greensum += udedge[y][x].rgbtGreen;
                        bluesum += udedge[y][x].rgbtBlue;
                        counter ++;
                    }
                }
            }
            // if middle pixel
            else if (i != 0 && j != 0 && i != height - 1 && j != width - 1)
            {
                redsum = greensum = bluesum = 0;
                counter = 0;

                RGBTRIPLE middle[3][3] =
                {
                    {image[i - 1][j - 1], image[i - 1][j], image[i - 1][j + 1]},
                    {image[i][j - 1], image[i][j], image[i][j + 1]},
                    {image[i + 1][j - 1], image[i + 1][j], image[i + 1][j + 1]}
                };

                for (int y = 0; y < 3; y++)
                {
                    for (int x = 0; x < 3; x++)
                    {
                        redsum += middle[y][x].rgbtRed;
                        greensum += middle[y][x].rgbtGreen;
                        bluesum += middle[y][x].rgbtBlue;
                        counter ++;
                    }
                }
            }

            bluredImage[i][j].rgbtRed = round(redsum / counter);
            bluredImage[i][j].rgbtGreen = round(greensum / counter);
            bluredImage[i][j].rgbtBlue = round(bluesum / counter);
        }
    }
    // copy back to the original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = bluredImage[i][j];
        }
    }

    return;
}