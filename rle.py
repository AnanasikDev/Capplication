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