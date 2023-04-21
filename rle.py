from signature import *

class RLE:
    def __init__(self, sequence):
        self.sequence = sequence

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


    def __split_byte_enumerator(self):
        def split(s):
            return [(s[i:i + 2]) for i in range(0, len(s), 2)]

        self.sequence = split(self.sequence)

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

        return byte_sequence

    def pack_byte(self):
        def a(seq, length):
            s = self.__pack_byte(seq)
            l = len(s)
            if l < length:
                return a(s, l)
            else:
                return seq

        return a(self.sequence, 10e10)

    def unpack_byte(self):

        self.sequence = list(map(lambda x: x.upper(), self.sequence))

        if self.sequence[0:4] != signature_bs:
            print(f"Format error: got {self.sequence[0:4]} instead of {signature_bs}.")
            return False

        file_size = int("".join(self.sequence[7:3:-1]), 16)

        unpacked = []

        for i in range(8, file_size):
            if i % 2 == 0:
                for j in range(int(self.sequence[i], 16)+1):
                    unpacked.append(self.sequence[i+1])

        return unpacked
