from public import *
from tkinter import filedialog as fd
import os

class Button:

    # Provides all functions of tkinter.Button; some are with simplified usage

    def __init__(self, text, callback, transform=None, **kwargs):
        self.name = text            # displayed title
        self.callback = callback    # functon being executed when pressed
        self.transform = transform  # (x, y, width, height)
                                    # **kwargs - other essential parameters of tk.Button
        self.attrs = {}
        self.attrs.update(kwargs)

        self.instance = tk.Button(text=text, command=callback, **kwargs)
        self.render()
        if self.transform:
            self.instance.place(x=transform[0], y=transform[1], width=transform[2], height=transform[3])


    def destroy(self):
        if self.instance:
            self.instance.destroy()

    def render(self):
        if self.instance:
            self.instance.pack()

    def update(self):
        btn = Button(self.name, self.callback, self.transform, **self.attrs)
        self.destroy()
        return btn


class Label:

    # Provides all functions of tkinter.Label; some are with simplified usage

    def __init__(self, text, transform=None, **kwargs):
        self.name = text                 # displayed title
        self.transform = transform       # (x, y, width, height)
                                         # **kwargs - other essential parameters of tk.Button
        self.attrs = {}
        self.attrs.update(kwargs)

        self.instance = tk.Label(text=text, **kwargs)
        self.render()
        if self.transform:
            self.instance.place(x=transform[0], y=transform[1], width=transform[2], height=transform[3])

    def destroy(self):
        if self.instance:
            self.instance.destroy()

    def render(self, **kwargs):
        if self.instance:
            self.instance.pack(**kwargs)

    def update(self):
        btn = Label(self.name, self.transform, **self.attrs)
        self.destroy()
        return btn

original_size = 0
packed_size = 0

# Callback function of button SEARCH
def callback_search_btn():
    global btn_execute, mode, lbl_inpath, lbl_outpath, lbl_original_size, lbl_result_size, original_size, lbl_eff
    Path.inpath = fd.askopenfilename()

    infile = Path.get_file(Path.inpath)

    if Path.get_file_extension(infile) == 'seven':
        # unpacking an archive
        Path.outpath = Path.get_file_path(Path.inpath) + "unpacked_" + Path.get_file_name(infile)
        outfile = Path.get_file(Path.outpath)
        btn_execute.name = "Unpack to " + Path.get_file_name(outfile)
        btn_execute.attrs["bg"] = "#9999CC"
        mode = UNPACK

        lbl_result_size.name = ""
        lbl_result_size = lbl_result_size.update()

    else:
        # packing a file
        Path.outpath = Path.get_file_path(Path.inpath) + Path.get_file_name(infile) + ".seven"
        outfile = Path.get_file(Path.outpath)
        btn_execute.name = "Pack to " + Path.get_file_name(outfile) + ".seven"
        btn_execute.attrs["bg"] = "#99CC99"
        mode = PACK

    btn_execute = btn_execute.update()
    lbl_inpath.name = "from: " + clamp_path(Path.inpath)
    lbl_inpath = lbl_inpath.update()

    lbl_outpath.name = "to: " + clamp_path(Path.outpath)
    lbl_outpath = lbl_outpath.update()

    if Path.inpath != '':
        original_size = os.stat(Path.inpath).st_size
        text_size = "Original size: " + str(original_size) + "B"
    else:
        original_size = 0
        text_size = ''

    lbl_eff.name = ''
    lbl_eff = lbl_eff.update()

    lbl_original_size.name = text_size
    lbl_original_size = lbl_original_size.update()

    lbl_result_size.name = ""
    lbl_result_size = lbl_result_size.update()


# Callback function of button EXECUTE
def callback_execute_btn():
    global lbl_result_size, lbl_eff, packed_size
    if mode == PACK:
        packed_size = pack()
        lbl_result_size.name = "Packed size: " + str(packed_size) + "B"
        lbl_result_size = lbl_result_size.update()

        if packed_size != 0:
            lbl_eff.name = "Size reduced by " + str(round((original_size / packed_size - 1) * 100)) + "%"
        else:
            lbl_eff.name = ''
        lbl_eff = lbl_eff.update()

    elif mode == UNPACK:
        size = unpack()
        lbl_result_size.name = "Unpacked size: " + str(size) + "B"
        lbl_result_size = lbl_result_size.update()

    else:
        print("Error: no file is chosen to be packed or unpacked")


# Function to initialize rendering of the whole UI
def renderui():
    global btn_execute, lbl_inpath, lbl_outpath, lbl_original_size, lbl_result_size, lbl_eff
    btn_search   = Button("Search file...", callback_search_btn, (0, 0, 500, 40), bg="#EEEDFF")
    btn_execute  = Button("Pack/Unpack", callback_execute_btn, (0, 350, 500, 50), activebackground="#ECECEC", bg="#CCCCCC")
    lbl_inpath   = Label ("File chosen: ", (0, 60, 500, 50))
    lbl_outpath  = Label ("Result file: ", (0, 110, 500, 50))
    lbl_original_size = Label("Original size: ", (0, 160, 500, 50))
    lbl_result_size = Label("Packed size: ", (0, 210, 500, 50))
    lbl_eff = Label('', (0, 260, 500, 50))
