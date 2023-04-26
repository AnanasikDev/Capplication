from signature import *
from time import time

class RLE:

    # RLE-based archiver class

    def __init__(self, sequence):
        self.sequence = sequence

    # Packs {self.sequence} and returns encoded data
    def pack_text(self):
        answer = ""

        l = len(self.sequence)
        i = 0

        def count(l, c):
            n = 0
            for i in range(len(l)):
                if l[i] == c:
                    n += 1
                else:
                    break
            return n

        while i < l:
            c = self.sequence[i]
            n = count(self.sequence[i::], c)
            i = i + n
            answer += str(n) + c

        return answer

    # Unpacks {self.sequence} and returns decoded data
    def unpack_text(self):
        answer = ""
        length = len(self.sequence)

        def parse(s):
            i = 0
            d = ""
            while s[i].isdigit():
                d += s[i]
                i += 1
            if d == '':
                return s[0], 1
            else:
                return int(d), len(d)

        i = 0
        while i < length:
            d, l = parse(self.sequence[i::])
            c = parse(self.sequence[i + l::])[0]
            answer += c * d
            i += l + 1

        return answer

    # Splits solid binary data to list of bytes
    def __split_byte_enumerator(self):
        return [(self.sequence[i:i + 2]) for i in range(0, len(self.sequence), 2)]

    # Packs BINARY sequence
    def __pack_byte(self, sequence):
        def count(lst, cluster):
            n = 0
            for i in range(len(lst)):
                if lst[i] == cluster:
                    n += 1
                else:
                    break
            return n

        def dec2hex(n):
            return str(hex(n - 1))[2::].upper().zfill(2)

        byte_sequence = []

        time_start = time()
        time_limit = 25 # seconds

        i = 0
        while i < len(sequence):
            cluster = sequence[i]
            n = count(sequence[i::], cluster)
            i += n
            if n // 256 > 1:
                for j in range(n // 256):
                    byte_sequence.append(dec2hex(256))
                    byte_sequence.append(cluster)
            byte_sequence.append(dec2hex(n % 256))
            byte_sequence.append(cluster)

            if time() - time_start > time_limit: # Time limit exceed
                return False

        return byte_sequence

    def pack_byte(self):
        def a(seq, length, i):
            s = self.__pack_byte(seq)
            if s is False: # Time limit exceed
                return -1, -1, -1
            l = len(s)
            if l < length:
                return a(s, l, i + 1)
            else:
                return seq, i, header_size + len(seq)

        return a(self.sequence, 10e10, 0)

    # Parse RLE-encoded data and returns decoded data
    def __unpack_byte(self, content):
        result = []
        for i in range(len(content)):
            if i % 2 == 0:
                for j in range(int(content[i], 16)+1):
                    result.append(content[i+1])
        return result

    # Unpacks {self.sequence} BINARY and returns decoded data and file type
    def unpack_byte(self):

        self.sequence = list(map(lambda x: x.upper(), self.sequence))

        if self.sequence[0:4] != signature_bs:
            print(f"Format error: got {self.sequence[0:4]} instead of {signature_bs}.")
            return False

        iterations = int(self.sequence[9], 16)

        self.sequence = self.__unpack_byte(self.sequence[15::])

        for i in range(iterations - 1):
            self.sequence = self.__unpack_byte(self.sequence)

        __type = determine_file_signature(self.sequence)

        return self.sequence, __type
