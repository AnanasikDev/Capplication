from collections import Counter
import struct

class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return self.left, self.right


def huffman_code_tree(node, binString=''):
    '''
    Function to find Huffman Code
    '''
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d


def make_tree(nodes):
    '''
    Function to make tree
    :param nodes: Nodes
    :return: Root of the tree
    '''
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]


def encode_data(encoding):
    encoded_data = ''.join(encoding[char] for char in data)
    return encoded_data


# solidata - solid sequence of 0 and 1
def decode_data(encoding, solidata):

    decoded = []

    decoding = {v: k for k, v in encoding.items()}

    print("decoding", decoding)

    bullet = ''
    for c in solidata:
        bullet += c
        if bullet in list(decoding.keys()):
            decoded.append(decoding[bullet])
            bullet = ''

    return decoded


def splitchunks(data):
    l = len(data)
    c = l // 8 * 8
    print(l, c)
    a = [data[i:i+8] for i in range(0, c, 8)]
    if l - c > 0:
        a.append(str(data[c::])[::-1].zfill(8)[::-1])
    return a


def int2hex(i):
    return hex(i)[2::].zfill(2)

def bin2hex(b):
    return hex(int(b, 2))[2::].zfill(2)

def int2bin(i):
    return bin(i)[2::].zfill(8)

def hex2bin(h):
    return bin(int(h, 16))[2::].zfill(8)


if __name__ == '__main__':

    # path = '/home/jam/IT/Graphs/Capplication/myapp/myapp/data/text.txt'
    path = '/home/jam/IT/Graphs/Capplication/myapp/myapp/data/img2.bmp'
    data = []
    with open(path, 'rb') as file:
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
    for i in encoding:
        print(f'{i} : {encoding[i]}')
    encoded = encode_data(encoding)

    encoded = splitchunks(encoded)

    with open("./data/sencoded", "wb") as file:
        for byte in encoded:
            if byte == b'':
                break
            file.write(struct.pack('<1s', bytes.fromhex(bin2hex(byte))))

    with open("./data/sencoded", "rb") as file:
        data = []
        while True:
            chunk = file.read(1)
            if chunk == b'':
                break

            p = struct.unpack('<B', chunk)[0]
            data.append(int2bin(p))
        data = ''.join(data)

        decoded = decode_data(encoding, data)

        with open("./data/sdecoded", "wb") as file:
            for byte in decoded:
                if byte == b'':
                    break
                file.write(struct.pack('<1s', bytes.fromhex(byte)))
