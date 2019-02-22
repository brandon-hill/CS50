// Abstraction and scope

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt user for height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while(n < 1 || n > 8);
    
    // Print the pyramid
    for(int i = 0; i < n; i++)
    {
        // Print spaces before blocks
        for(int j = 0; j < n - 1 - i; j++)
        {
            printf(" ");
        }
        
        //Print first set of blocks
        for(int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        
        //Print gap
        printf("  ");
        
        //Print second set of blocks
        for(int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }               
}

