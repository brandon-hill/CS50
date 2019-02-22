// Encrypt a message using Caesar's cypher

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check that 2 arguments were entered
    if (argc != 2)
    {   
        printf("Usage: ./caesar key\n");
        return 1;
    }    
    else
    {   
        // Check that each key argument character is a digit
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (!isdigit(argv[1][j]))
                {   
                    printf("Usage: ./caesar key\n");
                    return 1;            
                }        
            }   
        } 
        // Convert key from a string to an int
        int key = atoi(argv[1]);
        // Get plaintext from user
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        // Loop through plaintext and add the key to each applicable character
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            if (isupper(plaintext[i]))
            {
                printf("%c", plaintext[i] = (plaintext[i] - 'A' + key) % 26 + 'A');
            }
            else if (islower(plaintext[i]))
            {
                printf("%c", plaintext[i] = (plaintext[i] - 'a' + key) % 26 + 'a');
            }
            else
            {
                printf("%c", plaintext[i]);
            }
        }
    }
    printf("\n");
    return 0;
}

