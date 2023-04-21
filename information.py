import struct
from rle import *
from signature import *

class Information:
    # Information provides interface to work with streams of data
    # It is able to read certain files both BINARY and TEXT way;
    # Detect file type automatically (BINARY or TEXT)
    # Pack and unpack with RLE algorithm

    # little-endian

    BYTE = 0
    TEXT = 1
    def __init__(self):
        self.sequence = None
        self.algorithm = None

    # Reads sequences of data from file {path} and remembers it in self.sequence
    def read_sequence(self, path):

        # Read binary
        if self.algorithm == Information.BYTE:
            with open(path, "rb") as file:
                sequence = []
                while True:
                    chunk = file.read(1)
                    if chunk == b"":
                        break
                    sequence.append(hex(struct.unpack("<B", chunk)[0])[2::].upper().zfill(2))

        # Read text
        elif self.algorithm == Information.TEXT:
            with open(path, 'r') as file:
                sequence = file.read()

        self.sequence = sequence


    # Detects type of file (Binary or Text) and defines the packaging algorthm
    def define_algorithm(self, file):
        if isbyte(file):
            self.algorithm = Information.BYTE
        else:
            self.algorithm = Information.TEXT


    # Packs BINARY self.sequence in the file named {path}
    def __pack_byte(self, path):

        packed, iterations = RLE(self.sequence).pack_byte()

        # size of the packed file: number of bytes of content + signature + 4-byte int for length + number of iterations to be unpacked
        file_size = len(packed) + signature_size + 4 + 1

        assert iterations < 256, f"Iterations for packaging exceeds the limitations of 1 byte: {iterations}/{255}"

        with open(path, "wb") as file:
            file.write(struct.pack('<4siB', bytes.fromhex(signature), file_size, iterations))
            for byte in packed:
                file.write(struct.pack('<1s', bytes.fromhex(byte)))


    # Unpacks BINARY self.sequence in the file named {path}
    def __unpack_byte(self, path):

        unpacked = RLE(self.sequence).unpack_byte()

        with open(path, "wb") as file:
            for byte in unpacked:
                file.write(struct.pack('<1s', bytes.fromhex(byte)))


    # Packs TEXT self.sequence in the file named {path}
    def __pack_text(self, path):

        packed = RLE(self.sequence).pack_text()

        with open(path, "w") as file:
            file.write(packed)


    # Unpacks TEXT self.sequence in the file named {path}
    def __unpack_text(self, path):

        unpacked = RLE(self.sequence).unpack_text()

        with open(path, "w") as file:
            file.write(unpacked)


    # Packs data from {input_file} to {output_file}
    def pack(self, input_file, output_file):
        if not output_file.endswith(".seven"):
            output_file += ".seven"
        self.read_sequence(input_file)
        if self.algorithm == Information.BYTE:
            self.__pack_byte(output_file)
        elif self.algorithm == Information.TEXT:
            self.__pack_text(output_file)

    # Unpacks data from {input_file} to {output_file}
    def unpack(self, input_file, output_file):
        if not input_file.endswith(".seven"):
            input_file += ".seven"
        self.read_sequence(input_file)
        if self.algorithm == Information.BYTE:
            self.__unpack_byte(output_file)
        elif self.algorithm == Information.TEXT:
            self.__unpack_text(output_file)
