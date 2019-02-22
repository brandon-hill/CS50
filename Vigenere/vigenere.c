// Encrypt a message using Vigenere's cypher

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int shift(char c);

int main(int argc, string argv[])
{
    // Check that 2 arguments were entered
    if (argc != 2)
    {   
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }    
    else
    {   
        // Check that each key argument character is not a number
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (isdigit(argv[1][j]))
                {   
                    printf("Usage: ./vigenere keyword\n");
                    return 1;            
                }        
            }   
        } 
        // Get plaintext from user
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        // Loop through plaintext and add the key to each applicable character
        for (int i = 0, n = strlen(plaintext), k = 0; i < n; i++)
        {   
            // Revert to the first keyword character when each has been used
            if (k == strlen(argv[1]))
            {
                k = 0;
            }
            int key = shift(argv[1][k]);
            if (isupper(plaintext[i]))
            {
                printf("%c", plaintext[i] = (plaintext[i] - 'A' + key) % 26 + 'A');
                k++;
            }
            else if (islower(plaintext[i]))
            {
                printf("%c", plaintext[i] = (plaintext[i] - 'a' + key) % 26 + 'a');
                k++;
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

// Convert char to shift value
int shift(char c)
{
    if (islower(c))
    {
        c = (c - 'a') % 26;   
    }
    else 
    {
        c = (c - 'A') % 26;
    }
    return c;
}
