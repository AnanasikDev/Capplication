import tkinter as tk
from tkinter import filedialog as fd


def rle(string):
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


def pack(path):
    with open(path, 'r') as file:
        text = file.read()
        with open("output.seven", 'w') as output:
            output.write(rle(text))


def callback():
    name = fd.askopenfilename()
    print(name)
    pack(name)


errmsg = 'Error!'
tk.Button(text='Click to Open File',
          command=callback).pack(fill=tk.X)
tk.mainloop()
