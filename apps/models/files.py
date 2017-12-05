from wrapper import Wrapper


class Files(object):

    def __init__(self):
        self.w = Wrapper()

    table_name = 'CustomerFiles'
    table_wfile = 'WriterFiles'

    def addfile(self, fields):
        return self.w.insert(fields, self.table_name)

    def updfile(self, diction, condition = ""):
        return self.w.update(diction, self.table_name,condition)

    def addremotefile(self, fields):
        return self.w.insert(fields, self.table_wfile)
