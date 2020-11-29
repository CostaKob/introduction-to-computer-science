#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    int key;
    int lowerchar_calculation(char lowwer, int key);
    int upperchar_calculation(char upper, int key);
    string plaintext;

    // Check that program was run with one command-line argument
    if (argc != 2)
    {
        printf("Error: You have to provide 1 argument exactly\n");
        return 1;
    }
    else
    {
        // Iterate over the provided argument to make sure all characters are digits
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (!(isdigit(argv[1][i])))
            {
                printf("The key argument must be a digit!\n");
                return 1;
            }
        }

        // Convert that command-line argument from a string to an int
        key = atoi(argv[1]);

        // Get plaintext from the user
        plaintext = get_string("Plain Text: ");

        printf("ciphertext: ");

        for (int i = 0; i < strlen(plaintext); i++)
        {
            if (islower(plaintext[i]))
            {
                printf("%c", lowerchar_calculation(plaintext[i], key));
            }
            else if (isupper(plaintext[i]))
            {
                printf("%c", upperchar_calculation(plaintext[i], key));
            }
            else
            {
                printf("%c", plaintext[i]);
            }
        }
        printf("\n");
    }
}

int lowerchar_calculation(char lower, int key)
{
    return (((lower - 97) + key) % 26) + 97;
}

int upperchar_calculation(char upper, int key)
{
    return (((upper - 65) + key) % 26) + 65;
}

