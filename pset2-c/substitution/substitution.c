#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdbool.h>

bool is_valid_key(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    // Check for exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    
    string key = argv[1];
    
    // Validate the key
    if (!is_valid_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }
    
    // Get plaintext from user
    string plaintext = get_string("plaintext: ");
    
    // Encrypt and print ciphertext
    string ciphertext = encrypt(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);
    
    return 0;
}

bool is_valid_key(string key)
{
    // Check if key is exactly 26 characters
    if (strlen(key) != 26)
    {
        return false;
    }
    
    // Check for duplicate characters and ensure all are alphabetic
    bool seen[26] = {false};
    
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
        
        int index = toupper(key[i]) - 'A';
        if (seen[index])
        {
            return false; // Duplicate character
        }
        seen[index] = true;
    }
    
    return true;
}

string encrypt(string plaintext, string key)
{
    int len = strlen(plaintext);
    string ciphertext = malloc(len + 1);
    
    for (int i = 0; i < len; i++)
    {
        if (isalpha(plaintext[i]))
        {
            // Get position in alphabet (0-25)
            int pos = toupper(plaintext[i]) - 'A';
            
            // Get corresponding character from key
            char cipher_char = key[pos];
            
            // Preserve case
            if (islower(plaintext[i]))
            {
                ciphertext[i] = tolower(cipher_char);
            }
            else
            {
                ciphertext[i] = toupper(cipher_char);
            }
        }
        else
        {
            // Keep non-alphabetic characters unchanged
            ciphertext[i] = plaintext[i];
        }
    }
    
    ciphertext[len] = '\0';
    return ciphertext;
}
