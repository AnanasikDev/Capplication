from public import *
from tkinter import filedialog as fd

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


def callback_search_btn():
    global btn_execute, mode, lbl_inpath, lbl_outpath
    path.inpath = fd.askopenfilename()

    infile = Path.get_file(path.inpath)

    if Path.get_file_extension(infile) == 'seven':
        # unpacking an archive
        path.outpath = Path.get_file_path(path.inpath) + Path.get_file_name(infile) + "_UNPACKED"
        outfile = Path.get_file(path.outpath)
        btn_execute.name = "Unpack to " + Path.get_file_name(outfile)
        btn_execute.attrs["bg"] = "#9999CC"
        mode = UNPACK

    else:
        # packing a file
        path.outpath = Path.get_file_path(path.inpath) + Path.get_file_name(infile) + ".seven"
        outfile = Path.get_file(path.outpath)
        btn_execute.name = "Pack to " + Path.get_file_name(outfile) + ".seven"
        btn_execute.attrs["bg"] = "#99CC99"
        mode = PACK

    btn_execute = btn_execute.update()
    lbl_inpath.name = clamp_path(path.inpath)
    lbl_inpath = lbl_inpath.update()

    lbl_outpath.name = clamp_path(path.outpath)
    lbl_outpath = lbl_outpath.update()

    print("Inpath: " + path.inpath, "Outpath: " + path.outpath)



def callback_execute_btn():
    if mode == PACK:
        pack()
    elif mode == UNPACK:
        unpack()
    else:
        print("Error: no file is chosen to be packed or unpacked")


def renderui():
    global btn_execute, lbl_inpath, lbl_outpath
    btn_search   = Button("Search file...", callback_search_btn, (0, 0, 500, 40))
    btn_execute  = Button("Pack/Unpack", callback_execute_btn, (0, 350, 500, 50), activebackground="#ECECEC", bg="#CCCCCC")
    lbl_inpath   = Label ("File chosen: ", (0, 60, 500, 50))
    lbl_outpath  = Label ("Result file: ", (0, 110, 500, 50))