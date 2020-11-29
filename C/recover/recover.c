#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    int jpegs_sofar = 0;
    char filename[8] = "";
    FILE *img = NULL;
    FILE *file;
    unsigned char buffer[512];

    if (argc != 2)
    {
        printf("1 command-line argument required\n");
        return 1;
    }

    //open the file
    file = fopen(argv[1], "r");

    if (file == NULL)
    {
        return 2;
    }

    //read the card
    while ((fread(&buffer, sizeof(buffer), 1, file)) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if this is a first jpeg
            if (jpegs_sofar == 0)
            {
                sprintf(filename, "%03i.jpg", jpegs_sofar);
                img = fopen(filename, "w");
                fwrite(&buffer, sizeof(buffer), 1, img);
                jpegs_sofar++;
            }
            else if (jpegs_sofar != 0)
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", jpegs_sofar);
                img = fopen(filename, "w");
                fwrite(&buffer, sizeof(buffer), 1, img);
                jpegs_sofar++;
            }
        }
        else if (jpegs_sofar != 0)
        {
            fwrite(&buffer, sizeof(buffer), 1, img);
        }
    }

    if ((fread(&buffer, sizeof(buffer), 1, file)) == 0)
    {
        fclose(img);
        fclose(file);
    }
}

// V open memory card
// ??? repeat until end of card
// V read 512 bytes into a buffer
//
//      if start of new JPEG
//
//          if first JPEG
//              write the first 000 jpg
//          else
//              close the file and start new file
//
//      else
//          if already found jpeg
//              keep write it
//
//  close any remaining files
//
//