signature = "CAFEFADE"
signature_bs = ["CA", "FE", "FA", "DE"]
signature_size = 4


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

    n = 0
    for byte in sequence:
        if n > 16:
            return ''
        signature += byte.upper() + ' '
        if signature.strip() in sn:
            return signatures[signature.strip()]
        n += 1

    return ''
