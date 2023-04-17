import struct
from rle import *

class Information:
    # little-endian

    BYTE = 0
    TEXT = 1
    signature = "CAFEFADE"
    signature_bs = ["CA", "FE", "FA", "DE"]
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
                        sequence.append(hex(struct.unpack("<B", file.read(1))[0])[2::].upper().zfill(2))
                    except:
                        break
        self.sequence = sequence


    def __pack_byte(self, path):

        packed = RLE(self.sequence).pack_byte()

        # size of the packed file: number of bytes of content + signature + 4-byte int for length
        file_size = len(packed) + Information.signature_size + 4

        with open(path, "wb") as file:
            file.write(struct.pack('<4si', bytes.fromhex(Information.signature), file_size))
            for byte in packed:
                print(byte)
                file.write(struct.pack('<1s', bytes.fromhex(byte)))


    def __unpack_byte(self, path):

        unpacked = RLE(self.sequence).unpack_byte(Information.signature_bs)

        with open(path, "wb") as file:
            for byte in unpacked:
                # print(byte)
                file.write(struct.pack('<1s', bytes.fromhex(byte)))


    def pack(self, input_file, output_file):
        if self.algorithm == Information.BYTE:
            self.read_sequence(input_file)
            self.__pack_byte(f"{output_file}.seven")

    def unpack(self, input_file, output_file):
        if self.algorithm == Information.BYTE:
            self.read_sequence(f"{input_file}.seven")
            self.__unpack_byte(output_file)

i = Information(Information.BYTE)
# i.pack(input_file="img", output_file="byte_result")
# i.unpack(input_file="byte_result", output_file="unpacked")
i.pack(input_file="byte_result.seven", output_file="byte_result2")
