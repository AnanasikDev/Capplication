# Capplication

Capplication is an archiver which is capable of compressing both text and binary files such as .bmp, .png, .mp3 and other files. It utilizes a recurring algorithm in order to achieve maximum level of compression. It chooses between RLE and Huffman archivation to achieve less size.

# Extension & Signature

The unique extension and corresponding signature is used for this application: .seven; the signature is CAFE FADE in the hexadecimal code. Its structure is described below:
4 bytes : signature
4 bytes : total file size
1 byte  : algorithm of encoding & decoding (0 is RLE; 1 is Huffman)
1 byte  : iterations - the number of iterations are necessary to conduct 
        in order to decode original file
1 byte  : bits to ignore - number of following bits at the 
        end of the file that have been appended to constitute a byte (Only huffman)
4 bytes : dict_size; the size of huffman-encoding dictionary in bytes (Only huffman)

Decoded file has recoveried extension if the original one was .txt, .bmp, .jpg, .png, .mp3, .mp4, .docx, .exe or .doc

# UI

Program provides users with basic user interface: a button to search for target file; two labels to display input path and output path; and a button to commit packaging/unpackaging.
