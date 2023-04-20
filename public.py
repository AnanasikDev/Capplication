import tkinter as tk
from information import *

window = tk.Tk()
window.title("SEVEN File pack")
center_x = 1920//2
center_y = 1080//2

# set the position of the window to the center of the screen
window.geometry(f'{500}x{400}+{center_x}+{center_y}')
window.resizable(False, False)

inpath = ''
outpath = ''

PACK = 0
UNPACK = 1

mode = -1

def pack():
    global result_label, mode
    if result_label:
        result_label.destroy()

    if outpath == '':
        result_label = tk.Label(text="Error: enter the output file name", fg="red")
        result_label.pack()
    else:
        info = Information()
        info.define_algorithm(inpath)
        info.pack(input_file=inpath, output_file=outpath)

    mode = -1


def unpack():
    global result_label, mode
    if result_label:
        result_label.destroy()

    if outpath == '':
        result_label = tk.Label(text="Error: enter the output file name", fg="red")
        result_label.pack()
    else:
        info = Information()
        info.define_algorithm(inpath)
        info.unpack(input_file=inpath, output_file=outpath)
    mode = -1