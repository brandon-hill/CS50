// Determine the type and validity of a card number

// Abstraction and scope
#include <stdio.h>
#include <cs50.h>

int main(void)
{   
    // Get card number
    long n;
    do 
    {
        n = get_long("Number: ");   
    }
    while (n <= 0);
    
    // Iterate through number
    string cardType = "string";
    int sum;
    for (int i = 1; n != 0; i++)
    {   
        // Get card type
        if (i == 13)
        {
            cardType = "VISA";
        }
        else if (i == 15)
        {
            cardType = "AMEX";
        }
        else if (i == 16)
        {
            if(n > 4 || n == 2)
            {
                cardType = "MASTERCARD";
            }
            else
            {
                cardType = "VISA";
            }
        }
        else
        {
            cardType= "INVALID";
        }
        
        // Pull Digits
        int digit;
        int digit2;
        digit = n % 10;
        n /= 10;
          
        // Multiply every other digit by 2
        for (int j = 0; i % 2 == 0 && digit != 0; j++)
        {   
            if (j < 1)
            {
                digit *= 2;    
            }
            // Separate and add products digits
            digit2 = digit % 10;
            digit /= 10;
            sum = sum + digit2;
        }
        
        // Add other digits
        for (int j = 0; i % 2 != 0 && digit != 0; j++)
        {
            digit2 = digit % 10;
            digit /= 10;
            sum = sum + digit2;
        }        
    }
    
    // Check sum and print card type
    if (sum % 10 == 0)
    {
        printf("%s\n", cardType);  
    }
    else
    {
        printf("INVALID\n");
    }
} 



