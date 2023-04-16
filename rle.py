class RLE:
    def __init__(self, enumerator):
        self.enumerator = enumerator

    def pack_text(self):
        answer = ""

        l = len(self.enumerator)
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
            c = self.enumerator[i]
            n = count(self.enumerator[i::], c)
            i = i + n
            answer += str(n) + c

        return answer


    def unpack_text(self):
        answer = ""
        length = len(self.enumerator)

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
            d, l = parse(self.enumerator[i::])
            c = parse(self.enumerator[i + l::])[0]
            answer += c * d
            i += l + 1

        return answer


    def __split_byte_enumerator(self):
        def split(s):
            return [(s[i:i + 2]) for i in range(0, len(s), 2)]

        self.enumerator = split(self.enumerator)

    def pack_byte(self):

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
        while i < len(self.enumerator):
            cluster = self.enumerator[i]
            n = count(self.enumerator[i::], cluster)
            i += n
            if n // 256 > 1:
                for j in range(n // 256):
                    byte_sequence.append(dec2hex(256))
                    byte_sequence.append(cluster)
            byte_sequence.append(dec2hex(n % 256))
            byte_sequence.append(cluster)

        return byte_sequence

    def unpack_byte(self):

        self.__split_byte_enumerator()

        pass
