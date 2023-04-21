class Path:
    def __init__(self):
        self.inpath = ''
        self.outpath = ''

    @staticmethod
    def get_file(path):
        return path.split('/')[-1]

    @staticmethod
    def get_file_name(file):
        p = file.split('.')
        if len(p) <= 1:
            return p[0]
        return '.'.join(p[:len(p) - 1])

    @staticmethod
    def get_file_extension(file):
        p = file.split('.')
        if len(p) > 1:
            return p[-1]
        return ''

    @staticmethod
    def get_file_path(path):
        pathparts = path.split('/')
        return '/'.join(pathparts[:len(pathparts) - 1:]) + '/'

path = Path()
