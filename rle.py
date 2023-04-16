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

        self.__split_byte_enumerator()

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
                for i in range(n // 256):
                    print(dec2hex(256), cluster, sep='', end='')
            byte_sequence.append(dec2hex(n % 256))
            byte_sequence.append(cluster)

        return byte_sequence

    def unpack_byte(self):

        self.__split_byte_enumerator()

        pass




s = "6E6E6E6E6E7E7E66666654545454545454D8D8D8D8D8D8D8E1EEEEEEEEEEB6B6B6B6B66A6A6A6A63636363636363A9A9A9A9A93D6767B0B0B0B2B2B2B2B2B2ADADADAD69696969696933333333333F3F3F3FCACACACACA0E0E0E0E0EF0DCDCDC787878789090909090903B3B3B3B3B3B3B3BF5F5F5F5F5F5F5DFDFDFDFDFDFA0A0A0A0A0DCDCDCDCDCDC6D6D6D6D6D94941919191919191919404040404066666666666666BFBFF3F3F3F3F3F3F3F3B9B9B9B9D9D97878F8F8F8F8F8F8F8F895CCCCCCCCCCCC858585858556565656565656080808080808686868686868B0B0B0B0B0B0B01A1A1A1A1A1A1A1AF3F3F3F3F3F3F390909090909090BBBBBBBBBBBBC9C973737373737373732F2F2F2F2F2F2F1818181818737373731111B6B6B6B6B6B6B6C6C6C6C6C6C6C6606019262626262626030303C9C9C9C98C8C8C8CF7F73C3C3C3C2F2F2F2F939393936D6DC4C4C4C4C4C4BEBEBEBEBE66666666666666B2B2B2B2B2BCBCBCBC646464646464644848484848482F2F2F2F2F2F4D4D4D8A8A8A8A1B1B1B1B6666666666666666333393E5E5E5B8B8B8B82828287C7C7C7C7C7C7CE0E0E0E0E0E0E00D0D0D0D0D0D0D0D9C8D8D8D8DF7F7F7F7F7323232323232AEAEAEAEAE75757575757532757575E6E6E6E6E6E6E6E6"
rle = RLE(s)
p = rle.pack_byte()
print(len(s), len(p))
print(p)