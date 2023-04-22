# Capplication

Capplication is capable or compressing monotype files such as .BMP images. It utilizes a recurring algorithm in order to achieve maximum level of compression.

# Extension & Signature

The unique extension and corresponding signature is used for this application: .seven; the signature is CAFE FADE in the hexadecimal code. Its structure is described below:
4 bytes for extension
4 bytes for file size
1 byte for number of decoding RLE iterations - used for decoding algorithm to let it now how many iterations is it needed to conduct in order to recover original data.
