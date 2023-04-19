import tkinter as tk
from tkinter import filedialog as fd
from information import *
import os

file2pack = ""
file2unpack = ""

pack_label_inputname = None
pack_label_filesize = None

unpack_label_inputname = None
unpack_label_filesize = None

pack_result_entry = None
unpack_result_entry = None

result_label = None


def pack():
    global result_label
    if result_label:
        result_label.destroy()

    if pack_result_entry.get() == "":
        result_label = tk.Label(text="Error: enter the output file name", fg="red")
        result_label.pack()
    else:
        info = Information()
        info.define_algorithm(file2pack)
        print("file2pack", file2pack, "pack_result_entry_get", pack_result_entry.get())
        info.pack(input_file=file2pack, output_file=pack_result_entry.get())


def unpack():
    global result_label
    if result_label:
        result_label.destroy()

    if unpack_result_entry.get() == "":
        result_label = tk.Label(text="Error: enter the output file name", fg="red")
        result_label.pack()
    else:
        info = Information()
        info.define_algorithm(file2unpack)
        info.unpack(input_file=file2unpack, output_file=unpack_result_entry.get())


def callback_pack():
    global pack_label_inputname, pack_label_filesize, file2pack
    file2pack = fd.askopenfilename()
    if pack_label_inputname is not None:
        pack_label_inputname.destroy()

    _path2show = file2pack
    l = len(_path2show)
    maxl = 40
    if l > maxl:
        _path2show = "..." + _path2show[l-maxl:l:]
    pack_label_inputname = tk.Label(text="Path to the file: " + _path2show)
    pack_label_inputname.pack(side=tk.LEFT)
    pack_label_inputname.place(x=10, y=70)

    if pack_label_filesize:
       pack_label_filesize.destroy()
    file_stats = os.stat(file2pack)
    pack_label_filesize = tk.Label(window, text="input file size: " + str(file_stats.st_size) + " bytes")
    pack_label_filesize.pack(side=tk.LEFT)
    pack_label_filesize.place(x=10, y=100)


def callback_unpack():
    global unpack_label_inputname, unpack_label_filesize, file2unpack
    file2unpack = fd.askopenfilename()
    if unpack_label_inputname is not None:
        unpack_label_inputname.destroy()

    _path2show = file2unpack
    l = len(_path2show)
    maxl = 40
    if l > maxl:
        _path2show = "..." + _path2show[l-maxl:l:]
    unpack_label_inputname = tk.Label(text="Path to the file: " + _path2show)
    unpack_label_inputname.pack(side=tk.LEFT)
    unpack_label_inputname.place(x=510, y=70)

    if unpack_label_filesize:
       unpack_label_filesize.destroy()
    file_stats = os.stat(file2unpack)
    unpack_label_filesize = tk.Label(window, text="input file size: " + str(file_stats.st_size) + " bytes")
    unpack_label_filesize.pack(side=tk.LEFT)
    unpack_label_filesize.place(x=510, y=100)


window = tk.Tk()
window.title("SEVEN File pack")
center_x = 1920//2
center_y = 1080//2

# set the position of the window to the center of the screen
window.geometry(f'{1000}x{400}+{center_x}+{center_y}')
window.resizable(False, False)


def render_left():

    global pack_label_filesize, pack_label_inputname, path2pack, pack_result_entry

    left = tk.Frame(window, width=500, height=400)
    left.pack()
    left.place(x=0, y=0)

    btn_pack = tk.Button(left, text='Search file to pack...', command=callback_pack)
    btn_pack.pack(side=tk.LEFT)
    btn_pack.place(x=0, y=0, width=500)

    output_name_frame = tk.Frame(left)
    output_name_frame.pack()
    output_name_frame.place(x=0, y=300)

    tk.Label(output_name_frame, text="output file name: ", width=15).pack(side=tk.LEFT)
    pack_result_entry = tk.Entry(output_name_frame, width=35)
    pack_result_entry.pack(side=tk.RIGHT)

    btn = tk.Button(window, text='Pack', command=pack)
    btn.pack()
    btn.place(x=0, y=350, width=500)


def render_right():

    global unpack_label_filesize, unpack_label_inputname, path2unpack, unpack_result_entry

    right = tk.Frame(window, width=500, height=400)
    right.pack()
    right.place(x=500, y=0)

    btn_pack = tk.Button(right, text='Search file to unpack...', command=callback_unpack)
    btn_pack.pack(side=tk.LEFT)
    btn_pack.place(x=0, y=0, width=500)

    unpack_output_name_frame = tk.Frame(right)
    unpack_output_name_frame.pack()
    unpack_output_name_frame.place(x=0, y=300)

    tk.Label(unpack_output_name_frame, text="output file name: ", width=15).pack(side=tk.LEFT)
    unpack_result_entry = tk.Entry(unpack_output_name_frame, width=35)
    unpack_result_entry.pack(side=tk.RIGHT)

    btn = tk.Button(window, text='Unpack', command=unpack)
    btn.pack()
    btn.place(x=500, y=350, width=500)


render_left()
render_right()

tk.mainloop()
