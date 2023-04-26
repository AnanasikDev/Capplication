from collections import Counter
import pickle
from signature import *
from utils import *

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

    def __init__(self, sequence=None):
        self.sequence = sequence
        self.__bits2ignore = 0
        self.__encoded = None

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


    # Runs encoding process of {input_file} directly into {output_file}
    def encode_data(self):
        freq = dict(Counter(self.sequence))
        freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        node = make_tree(freq)
        encoding = huffman_code_tree(node)
        encoding = dict(sorted(encoding.items(), key=lambda x: len(x[1])))
        encoded = Huffman.__encode_data(encoding, self.sequence)

        encoded, bits2ignore = Huffman.__splitchunks(encoded)

        encoded_dict = pickle.dumps(encoding)
        dictionary_size = len(encoded_dict)
        file_size = header_size + dictionary_size + len(encoded)

        return file_size, encoded, encoding, bits2ignore

    # Writes given encoded data in {output_file}
    @staticmethod
    def encode(encoded, output_file, encoding, bits2ignore):
        with open(output_file, "wb") as file:
            encoded_dict = pickle.dumps(encoding)
            dictionary_size = len(encoded_dict)

            file_size = header_size + dictionary_size + len(encoded)

            file.write(
                struct.pack('<4siBBBi',
                            bytes.fromhex(signature_str), file_size, 1, 1, bits2ignore, dictionary_size)
                      )
            pickle.dump(encoding, file)
            for byte in encoded:
                if byte == b'':
                    break
                file.write(struct.pack('<1s', bytes.fromhex(bin2hex(byte))))

    # Runs decoding process of {input_file} directly into {output_file}
    @staticmethod
    def decode(input_file):

        signature, file_size, algorithm, iterations, bits2ignore, dict_size = read_params(input_file)

        with open(input_file, "rb") as file:
            file.seek(15)
            d = file.read()
            encoding = pickle.loads(d)

            m = header_size + dict_size
            file.seek(m)

            data = []
            while True:
                chunk = file.read(1)
                if chunk == b'':
                    break
                data.append(int2bin(struct.unpack('<B', chunk)[0]))

            data = ''.join(data)
            data = data[:len(data)-bits2ignore:]

            decoded = Huffman.__decode_data(encoding, data)

        __type = determine_file_signature(decoded)

        return decoded, __type