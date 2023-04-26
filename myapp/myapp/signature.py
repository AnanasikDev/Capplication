signature_str = "CAFEFADE"
signature_bs = ["CA", "FE", "FA", "DE"]
signature_size = 4

header_size = signature_size + 4 + 1 + 1 + 1 + 4

"""
---------------------
        HEADER:
---------------------

  [ ] 4 bytes : signature
  [ ] 4 bytes : file size (including header, [huffman dictionary] and content)
  [ ] 1 byte  : algorithm of encoding & decoding (0 is RLE; 1 is Huffman)
  [ ] 1 byte  : iterations - the number of iterations are necessary to conduct 
                in order to decode original file
  [H] 1 byte  : bits to ignore - number of following bits at the 
                end of the file that have been appended to constitute a byte
  [H] 4 bytes : dict_size; the size of huffman-encoding dictionary in bytes

* [ ] - versatile parameter
* [H] - huffman-only parameter
* [R] - rle-only parameter
"""

# Determines file type based on byte signature
def determine_file_signature(sequence):
    signatures = {"FF FE"                                   : "txt",
                  "FF FE 00 00"                             : "txt",
                  "42 4D"                                   : "bmp",
                  "FF D8 FF E0"                             : "jpg",
                  "FF D8 FF DB"                             : "jpg",
                  "FF D8 FF E0 00 10 4A 46 49 46 00 01"     : "jpg",
                  "FF D8 FF EE"                             : "jpg",
                  "89 50 4E 47 0D 0A 1A 0A"                 : "png",
                  "49 44 33"                                : "mp3",
                  "FF FB"                                   : "mp3",
                  "FF F3"                                   : "mp3",
                  "FF F2"                                   : "mp3",
                  "66 74 79 70 69 73 6F 6D"                 : "mp4",
                  "50 4B 03 04"                             : "docx",
                  "5A 4D"                                   : "exe",
                  "0E FE FF"                                : "txt",
                  "D0 CF 11 E0 A1 B1 1A E1"                 : "doc",
                  }

    signature = ""

    sn = list(signatures.keys())

    signature_size_limit = 16

    n = 0
    for byte in sequence:
        if n > signature_size_limit:
            return ''
        signature += byte.upper() + ' '
        if signature.strip() in sn:
            return signatures[signature.strip()]
        n += 1

    return ''
