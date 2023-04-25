from collections import Counter
import struct
import pickle
import signature
from lib.utils import *

# Binary tree implementation
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right


# Function to find Huffman Code
def huffman_code_tree(node, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d


# Function to make tree
# :param nodes: Nodes
# :return: Root of the tree
def make_tree(nodes):
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]


class Huffman:

    # Based on encoding and solid binary data sequence returns encoded data
    @staticmethod
    def __encode_data(encoding, data):
        encoded_data = ''.join(encoding[char] for char in data)
        return encoded_data

    # Based on encoding and solid binary data sequence returns encoded data
    # encoding - dictionary VALUE : PATTERN
    # solidata - solid sequence of 0 and 1
    @staticmethod
    def __decode_data(encoding, solidata):

        decoded = []

        decoding = {v: k for k, v in encoding.items()}

        bullet = ''
        for c in solidata:
            bullet += c
            if bullet in list(decoding.keys()):
                decoded.append(decoding[bullet])
                bullet = ''

        return decoded

    # Splits solid block of 0 and 1 into bytes with
    # If it is impossible, then the number of bits
    # is extended to the next multiple of 8 by following zeros
    @staticmethod
    def __splitchunks(data):
        l = len(data)
        c = l // 8 * 8
        a = [data[i:i + 8] for i in range(0, c, 8)]
        if l - c > 0:
            a.append(str(data[c::])[::-1].zfill(8)[::-1])
        return a, 8 - l + c

    # Inverses the sequence of bytes
    # Little Endian -> Big Endian OR Big Endian -> Little Endian
    # Works both with string and lists
    @staticmethod
    def __inverse_bytes(seq):
        if isinstance(seq, str):
            l = len(seq)
            a = [seq[i:i + 2] for i in range(0, l, 2)]
            return ''.join(a[::-1])
        elif isinstance(seq, list):
            return seq[::-1]


    # Runs encoding process of {input_file} directly into {output_file}
    @staticmethod
    def encode(input_file, output_file):
        data = []
        with open(input_file, 'rb') as file:
            while True:
                chunk = file.read(1)
                if chunk == b'':
                    break
                chunk = int2hex(struct.unpack('<B', chunk)[0])
                data.append(chunk)

        freq = dict(Counter(data))
        freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        node = make_tree(freq)
        encoding = huffman_code_tree(node)
        encoding = dict(sorted(encoding.items(), key=lambda x: len(x[1])))
        encoded = Huffman.__encode_data(encoding, data)

        encoded, bits2ignore = Huffman.__splitchunks(encoded)

        with open(output_file, "wb") as file:
            encoded_dict = pickle.dumps(encoding)
            l = len(encoded_dict)

            file_size = 4 + 4 + 1 + 1 + 1 + 4 + 2 * 3 * 4 + l + len(encoded)

            file.write(
                struct.pack('<4siBBBiiii', bytes.fromhex(signature.signature), file_size, 1, 1, bits2ignore, l, 0, 0,
                            0))
            pickle.dump(encoding, file)
            file.write(struct.pack('<iii', 0, 0, 0))
            for byte in encoded:
                if byte == b'':
                    break
                file.write(struct.pack('<1s', bytes.fromhex(bin2hex(byte))))

    # Runs decoding process of {input_file} directly into {output_file}
    @staticmethod
    def decode(input_file, output_file):

        signature, file_size, algorithm, iterations, bits2ignore, dict_size = Huffman.__read_params(input_file)

        with open(input_file, "rb") as file:
            file.seek(27)
            d = file.read()
            encoding = pickle.loads(d)

            m = 4 + 4 + 1 + 1 + 1 + 4 + 2 * 3 * 4 + dict_size
            file.seek(m)

            data = []
            while True:
                chunk = file.read(1)
                if chunk == b'':
                    break
                data.append(int2bin(struct.unpack('<B', chunk)[0]))

            data = ''.join(data)

            decoded = Huffman.__decode_data(encoding, data)

            with open(output_file, "wb") as file:
                for byte in decoded:
                    if byte == b'':
                        break
                    file.write(struct.pack('<1s', bytes.fromhex(byte)))

    # Reads .seven parameters
    m = 0
    @staticmethod
    def __read_params(path):
        with open(path, "rb") as file:
            data = []
            while True:
                chunk = file.read(1)
                if chunk == b'':
                    break

                p = struct.unpack('<B', chunk)[0]
                data.append(int2bin(p))

            def read_bytes(n):
                Huffman.m += n
                return ''.join(Huffman.__inverse_bytes(data[(Huffman.m - n):Huffman.m:]))

            signature = read_bytes(4)
            file_size = bin2int(read_bytes(4))
            algorithm = bin2int(read_bytes(1))
            iterations = bin2int(read_bytes(1))
            bits2ignore = bin2int(read_bytes(1))
            dict_size = bin2int(read_bytes(4))

        return signature, file_size, algorithm, iterations, bits2ignore, dict_size



if __name__ == '__main__':

    Huffman.decode("./data/decoded1", "./data/decoded0")