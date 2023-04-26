import struct
from rle import *
from signature import *
from huffman import *

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

        else:
            raise Exception("Information type is undefined")

        self.sequence = sequence

    @staticmethod
    def determine_type(path):
        with open(path, 'rb') as file:
            r = file.read()
            try:
                data = str(r, "utf-8")
                return "TEXT"
            except:
                return "BYTE"

    # Detects type of file (Binary or Text) and defines the packaging algorthm
    def define_algorithm(self, path):
        with open(path, 'rb') as file:
            r = file.read()
            try:
                data = str(r, "utf-8")
                self.algorithm = Information.TEXT
            except:
                self.algorithm = Information.BYTE

    def __pack_byte_rle(self, output_file, packed, iterations, file_size):
        with open(output_file, "wb") as file:
            file.write(struct.pack('<4siBiBB', bytes.fromhex(signature_str), file_size, 0, iterations, 0, 0))
            for byte in packed:
                file.write(struct.pack('<1s', bytes.fromhex(byte)))

    def __pack_byte_hfm(self, output_file, encoded, encoding, bits2ignore):
        Huffman.encode(encoded, output_file, encoding, bits2ignore)


    def __pack_byte(self, output_file):
        r_packed, r_iterations, r_length = RLE(self.sequence).pack_byte()
        h_length, h_encoded, h_encoding, h_bits2ignore = Huffman(self.sequence).encode_data()

        if r_length != -1 and r_length < h_length:
            print(f"RLE is more efficient in this case: {r_length} compared to {h_length}")
            self.__pack_byte_rle(output_file, r_packed, r_iterations, r_length)
        else:
            print(f"Huffman is more efficient in this case: {h_length} compared to {r_length}")
            self.__pack_byte_hfm(output_file, h_encoded, h_encoding, h_bits2ignore)



    # Unpacks BINARY self.sequence in the file named {path}
    def __unpack_byte(self, output_file):

        unpacked, __type = RLE(self.sequence).unpack_byte()

        if __type != '':
            output_file += '.' + __type

        with open(output_file, "wb") as file:
            for byte in unpacked:
                file.write(struct.pack('<1s', bytes.fromhex(byte)))

    # Packs TEXT self.sequence in the file named {path}
    def __pack_text(self, output_file):

        packed = RLE(self.sequence).pack_text()

        with open(output_file, "w") as file:
            file.write(packed)

    # Unpacks TEXT self.sequence in the file named {path}
    def __unpack_text(self, output_file):

        unpacked = RLE(self.sequence).unpack_text()

        with open(output_file + '.txt', "w") as file:
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
