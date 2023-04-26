import struct

def int2hex(i):
    return hex(i)[2::].zfill(2)

def bin2hex(b):
    return hex(int(b, 2))[2::].zfill(2)

def int2bin(i):
    return bin(i)[2::].zfill(8)

def hex2bin(h):
    return bin(int(h, 16))[2::].zfill(8)

def bin2int(b):
    return int(b, 2)


# Inverses the sequence of bytes
# Little Endian -> Big Endian OR Big Endian -> Little Endian
# Works both with string and lists
def inverse_bytes(seq):
    if isinstance(seq, str):
        l = len(seq)
        a = [seq[i:i + 2] for i in range(0, l, 2)]
        return ''.join(a[::-1])
    elif isinstance(seq, list):
        return seq[::-1]


# Reads .seven parameters
__m = 0
def read_params(path):
    global __m
    with open(path, "rb") as file:
        data = []

        length = 15

        for i in range(length):
            chunk = file.read(1)
            if chunk == b'':
                break

            p = struct.unpack('<B', chunk)[0]
            data.append(int2bin(p))

        def read_bytes(n):
            global __m
            __m += n
            a = ''.join(inverse_bytes(data[(__m - n):__m:]))
            return a

        signature = read_bytes(4)
        file_size = bin2int(read_bytes(4))
        algorithm = bin2int(read_bytes(1))
        iterations = bin2int(read_bytes(1))
        bits2ignore = bin2int(read_bytes(1))
        dict_size = bin2int(read_bytes(4))

    __m = 0
    return signature, file_size, algorithm, iterations, bits2ignore, dict_size