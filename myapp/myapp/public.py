import tkinter as tk
from information import *
from path import *

window = tk.Tk()
window.title("SEVEN File pack")
center_x = 1920//2
center_y = 1080//2

# set the position of the window to the center of the screen
window.geometry(f'{500}x{400}+{center_x}+{center_y}')
window.resizable(False, False)

PACK = 0
UNPACK = 1

mode = -1

# Starts the process of packing the given file
def pack():
    global mode
    info = Information()
    info.define_filetype(Path.inpath)
    info.pack(input_file=Path.inpath, output_file=Path.outpath)
    mode = -1


# Starts the process of unpacking the given file
def unpack():
    global mode
    info = Information()
    info.define_filetype(Path.inpath)
    info.unpack(input_file=Path.inpath, output_file=Path.outpath)
    mode = -1


# Clamp the given path {string} and leaves only the end
# of it if it is too long. The default limit is 50 characters.
def clamp_path(path):
    l = len(path)
    maxl = 50
    if l > maxl:
        return "..." + path[l - maxl:l:]
    return path
