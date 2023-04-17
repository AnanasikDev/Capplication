signature = "CAFEFADE"
signature_bs = ["CA", "FE", "FA", "DE"]
signature_size = 4

text_formats = ["txt"]

def isbyte(file):
    extension = file.split('.')[-1]

    if extension in text_formats:
        return False
    return True
