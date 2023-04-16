import struct
from rle import *

class Information:
    BYTE = 0
    TEXT = 1
    signature = "B2E6C8DD"
    signature_size = 4
    def __init__(self, algorithm):
        self.sequence = None
        self.algorithm = algorithm


    def read_sequence(self, path):
        if self.algorithm == Information.BYTE:
            with open(path, "rb") as file:
                sequence = []
                while True:
                    try:
                        sequence.append(hex(struct.unpack("<1", file.read(1))[0]))
                    except:
                        break
        self.sequence = sequence


    def __pack_byte(self, path):

        packed = RLE(self.sequence).pack_byte()

        # size of the packed file: number of bytes of content + signature + 4-byte int for length
        file_size = len(packed) + Information.signature_size + 4

        with open(path, "wb") as file:
            file.write(struct.pack('<4i', bytes.fromhex(Information.signature), file_size))
            for element in packed:
                file.write(struct.pack('<b', element))


    def __unpack_byte(self, path):

        with open(path, "rb") as file:
            signature = file.read(4)
            if signature != bytes.fromhex(Information.signature):
                print("Format error")
                return False

            file_size = int(hex(struct.unpack("<i", file.read(4))[0]), 16)
            print("file size =", file_size)

            parsed = []

            for i in range(file_size - 8):
                parsed.append(hex(struct.unpack("<b", file.read(1))[0]))


        unpacked = RLE(parsed).unpack_byte()


    def pack(self):
        if self.algorithm == Information.BYTE:
            self.__pack_byte("byte_result.seven")

            pass


i = Information(Information.BYTE)
i.read_sequence("byte_test.b")
print(i.sequence)
