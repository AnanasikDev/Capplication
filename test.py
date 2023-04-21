
def determine_type(path):
    with open(path, 'rb') as file:
        r = file.read()
        try:
            data = str(r, "utf-8")
            return "TEXT"
        except:
            return "BYTE"


print(determine_type("file.txt"))
print(determine_type("img_UNPACKED"))
print(determine_type("img.seven"))
print(determine_type("img.bmp"))
print(determine_type("Text File"))


"""

def define_algorithm(self, file):
    text_ = ["txt", "py", "cpp", "cs"]
    if Path.get_file_extension(Path.get_file(file)) in text_:
        self.algorithm = Information.TEXT
    else:
        self.algorithm = Information.BYTE

"""