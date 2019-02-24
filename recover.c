// Recover jpegs from a memory card

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

typedef struct
{
    BYTE image[512];
} __attribute__((__packed__))
BUFFER;


int main(int argc, char *argv[])
{
    // ensure correct usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw\n");
        return 1;
    }

    // remember filename
    char *infile = argv[1];

    // open infile
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // define array for filenames
    char filename[8];

    // temporary storage
    BUFFER *buffer;

    // allocate memory for buffer
    buffer = malloc(sizeof(BUFFER));

    // initialize counter for jpegs
    int counter = 0;

    // keep track of open jpegs
    int open = 0;

    // initialize pointer
    FILE *img = NULL;

    // loop through file until the EOF
    while (fread(buffer, 1, 512, inptr) != 0x00)
    {
        // check for the beginning of a jpeg
        if (buffer->image[0] == 0xff &&
            buffer->image[1] == 0xd8 &&
            buffer->image[2] == 0xff &&
            (buffer->image[3] & 0xf0) == 0xe0)
        {
            // if first jpeg, open for writing
            if (!img)
            {
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
            }
            open = 1;
            // otherwise close that jpeg and open another
            fclose(img);
            sprintf(filename, "%03i.jpg", counter++);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                return 3;
            }
            fwrite(buffer, 1, 512, img);
        }
        else
        {
            // if a jpeg is opened write the bytes from buffer
            if (img)
            {
                fwrite(buffer, 1, 512, img);
            }
        }
    }
    fclose(img);
    free(buffer);
    return 0;
}
