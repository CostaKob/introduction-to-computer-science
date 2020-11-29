// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

// words in dictionary counter
int wordsInDictionary;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    unsigned int hashedWord = hash(word);

    // linked list --->>> table[hashedWord];

    //iterate over linked list
    for (node *tmp = table[hashedWord]; tmp != NULL; tmp = tmp->next)
    {
        if ((strcasecmp(tmp->word, word)) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
// took the explanation from here: https://www.youtube.com/watch?v=F95z5Wxd9ks&ab_channel=freeCodeCamp.org
unsigned int hash(const char *word)
{
    unsigned int h = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        h += tolower(word[i]);
    }

    return h % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file;
    char word[LENGTH + 1];
    node *list = NULL;
    file = fopen(dictionary, "r");

    if (file == NULL)
    {
        return 2;
    }

    while(fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);
        n->next = NULL;
        wordsInDictionary++;
        unsigned int index = hash(word);

        // if first node in list
        if (table[index] == NULL)
        {
            table[index] = n;
        }
        // if not firs node in list
        else if (table[index] != NULL)
        {
            n->next = table[index];
            table[index] = n;
        }
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordsInDictionary;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tmp;

    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
                tmp = table[i];
                table[i] = table[i]->next;
                free(tmp);
        }
    }
    return true;
}