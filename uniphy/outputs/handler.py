from .structure import SectionHolder

class Output():
    def __init__(self, name=None):
        self.name = name
        self.sections = SectionHolder()

    def print(self, *values, sep=' ', end='\n', file=None, flush=True):

        do_print = True  # TODO: determine if to print or not
        if do_print:
            print(*values, sep=sep, end=end, file=file, flush=flush)

    def section(self, number=None, name=None):
        self.sections[number] = Output(name=name)
