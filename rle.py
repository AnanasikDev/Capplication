def pack(string):
    answer = ""

    l = len(string)
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
        c = string[i]
        n = count(string[i::], c)
        i = i + n
        answer += str(n) + c

    return answer


def unpack(string):
    answer = ""
    length = len(string)

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
        d, l = parse(string[i::])
        c = parse(string[i + l::])[0]
        answer += c * d
        i += l + 1

    return answer
