// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Count amount of words in dictionary
int word_count = 0;

// Represents number of buckets in a hash table
#define N 65536

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hashtable
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    while (*word)
    {
        hash = (hash << 2) ^ (*word | 0x20);
        word++;
    }
    return hash % N;
}

// Initialize head pointer
node *head = NULL;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hashtable
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Initialize new node
    node *new_node = NULL;

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate space for each new node
        new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Store word in node
        strcpy(new_node->word, word);

        // Hash word
        int bucket = hash(word);

        // Initialize hashtable index if necessary else push node to correct bucket
        if (hashtable[bucket] == NULL)
        {
            new_node->next = NULL;
            hashtable[bucket] = new_node;
            word_count++;
        }
        else
        {
            new_node->next = hashtable[bucket];
            hashtable[bucket] = new_node;
            head = new_node;
            word_count++;
        }
    }
    // printf("head: %s\n", head->word);
    // printf("wordcount: %i\n", word_count);

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash word
    int bucket = hash(word);

    // Initialize cursor
    node *cursor = &hashtable[bucket][0];

    // Traverse linked list checking for match
    while (cursor != NULL)
    {
        // Compare until a match is found
        if (strcasecmp(word, cursor->word) != 0)
        {
            cursor = cursor->next;
        }
        else
        {
            return true;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = &hashtable[i][0];
        while (cursor)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}