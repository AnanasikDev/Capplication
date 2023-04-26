from rle import *
from huffman import *
from utils import *

class Information:

    # Information provides interface to work with streams of data
    # It is able to read certain files both BINARY and TEXT way;
    # Detect file type automatically (BINARY or TEXT)
    # Pack and unpack with RLE and Huffman algorithms

    # little-endian

    BYTE = 0
    TEXT = 1

    RLE = 0
    HUFFMAN = 1
    def __init__(self):
        self.sequence = None
        self.filetype = None
        self.algorithm = RLE

    # Reads sequences of data from file {path} and remembers it in self.sequence
    def read_sequence(self, path):

        # Read binary
        if self.filetype == Information.BYTE:
            with open(path, "rb") as file:
                sequence = []
                while True:
                    chunk = file.read(1)
                    if chunk == b"":
                        break
                    sequence.append(hex(struct.unpack("<B", chunk)[0])[2::].upper().zfill(2))

        # Read text
        elif self.filetype == Information.TEXT:
            with open(path, 'r') as file:
                sequence = file.read()

        # Unexpected filetype
        else:
            raise Exception("Information type is undefined")

        self.sequence = sequence

    # Defines algorithm which file has been encoded with
    def define_alorithm_unpack(self, path):
        signature, file_size, algorithm, iterations, bits2ignore, dict_size = read_params(path)

        if algorithm == Information.HUFFMAN:
            self.algorithm = Information.HUFFMAN
        else:
            self.algorithm = Information.RLE

    # Determines type of file: Text or Binary
    def determine_filetype(self, path):
        with open(path, 'rb') as file:
            r = file.read()
            try:
                data = str(r, "utf-8")
                self.filetype = Information.TEXT
            except:
                self.filetype = Information.BYTE

    # Writes {packed} data into {output_file} with RLE algorithm
    def __pack_byte_rle(self, output_file, packed, iterations, file_size):
        with open(output_file, "wb") as file:
            file.write(struct.pack('<4siBiBB', bytes.fromhex(signature_str), file_size, 0, iterations, 0, 0))
            for byte in packed:
                file.write(struct.pack('<1s', bytes.fromhex(byte)))

    # Writes {packed} data into {output_file} with Huffman algorithm
    def __pack_byte_hfm(self, output_file, encoded, encoding, bits2ignore):
        Huffman.encode(encoded, output_file, encoding, bits2ignore)

    # Packs {self.sequence} into {output_file}.
    # Checks automatically whether it is more efficient to use RLE or Huffman
    def __pack_byte(self, output_file):
        r_packed, r_iterations, r_length = RLE(self.sequence).pack_byte()
        h_length, h_encoded, h_encoding, h_bits2ignore = Huffman(self.sequence).encode_data()

        if r_length != -1 and r_length < h_length:
            print(f"RLE is more efficient in this case: {r_length} compared to {h_length}")
            self.__pack_byte_rle(output_file, r_packed, r_iterations, r_length)
            return r_length
        else:
            print(f"Huffman is more efficient in this case: {h_length} compared to {r_length}")
            self.__pack_byte_hfm(output_file, h_encoded, h_encoding, h_bits2ignore)
            return h_length

    # Unpacks BINARY {self.sequence} in the file named {path}
    def __unpack_byte(self, input_file, output_file):

        if self.algorithm == Information.RLE:
            unpacked, __type = RLE(self.sequence).unpack_byte()
            if __type != '':
                output_file += '.' + __type

            with open(output_file, "wb") as file:
                for byte in unpacked:
                    file.write(struct.pack('<1s', bytes.fromhex(byte)))

            return len(unpacked)

        else:
            decoded, __type = Huffman.decode(input_file)
            if __type != '':
                output_file += '.' + __type

            with open(output_file, "wb") as file:
                for byte in decoded:
                    if byte == b'':
                        break
                    file.write(struct.pack('<1s', bytes.fromhex(byte)))

            return len(decoded)

    # Packs TEXT {self.sequence} in the file named {path}
    def __pack_text(self, output_file):
        packed = RLE(self.sequence).pack_text()
        with open(output_file, "w") as file:
            file.write(packed)
        return len(packed)

    # Unpacks TEXT {self.sequence} in the file named {path}
    def __unpack_text(self, output_file):
        unpacked = RLE(self.sequence).unpack_text()
        with open(output_file + '.txt', "w") as file:
            file.write(unpacked)
        return len(unpacked)

    # Packs data from {input_file} to {output_file}
    def pack(self, input_file, output_file):
        if not output_file.endswith(".seven"):
            output_file += ".seven"
        self.read_sequence(input_file)
        if self.filetype == Information.BYTE:
            return self.__pack_byte(output_file)
        elif self.filetype == Information.TEXT:
            return self.__pack_text(output_file)

    # Unpacks data from {input_file} to {output_file}
    def unpack(self, input_file, output_file):
        if not input_file.endswith(".seven"):
            print("Wrong file type chosen. Must be .seven")
        self.read_sequence(input_file)
        self.define_alorithm_unpack(input_file)
        if self.filetype == Information.BYTE:
            return self.__unpack_byte(input_file, output_file)
        elif self.filetype == Information.TEXT:
            return self.__unpack_text(output_file)
