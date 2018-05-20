from collections import OrderedDict
import copy
import sys

from .structure import SectionHolder
from .format.formatter import Formatter


class Output():
    verbosity = 5
    verbosity_save = 5
    default_formatter = Formatter
    __TOP_LEVEL = 0

    def __init__(self, name=None, level=0, formatter=None):
        self.name = name
        self.level = level
        self.formatter = Formatter() if formatter is None else formatter
        self.sections = SectionHolder()
        self.output_raw = []
        self.cur_sec = self

        # if self.name is not None:
        #     self.cur_sec.p(name, layout=self.formatter.title_by_rank[self.level])

    @property
    def top_level_section(self):
        return self.level == self.__TOP_LEVEL

    @property
    def cur_sec(self):
        if self.top_level_section and self._cur_sec is self:
            self.section()
        return self._cur_sec

    @cur_sec.setter
    def cur_sec(self, section):
        self._cur_sec = section

    def _reset_to_self(self):
        self.cur_sec = self

    def p(self, *values, sep=' ', end='\n', file=None, flush=True, layout=None, tags=None,
          nice=5, nice_save=None):
        """

        Parameters
        ----------
        values : obj
        sep : obj
        end :
        file :
        flush :
        layout : str or callable (with print signature)
            The layout of the values. Can be 'title', 'subtitle' etc or a callable taking
            the arguments `values`, `sep` and `end`.
        tags : iterable
            Tags that better describe the output like 'fit', 'result', 'info'...
        nice : int
            If the verbosity >= nice, then the normal print function is invoked.
        nice_save : int (default is = nice)
            If verbosity_save >= nice_save, then the content will be saved.
        """
        nice_save = nice if nice_save is None else nice_save

        self.cur_sec.output_raw.append({'values': values, 'sep': sep, 'end': end,
                                        'file': file, 'flush': flush,
                                        'layout': layout, 'tags': tags,
                                        'nice': nice, 'nice_save': nice_save})

        do_print = self.cur_sec.verbosity >= nice  # TODO: determine if to print or not
        if do_print:
            print(*values, sep=sep, end=end, file=file, flush=flush)

    if sys.version_info[0] > 2:
        print = p  # creating alias for `p`

    def section(self, name=None, number=None):
        section = self.sections[number]
        if section is None:
            section = Output(name=name, level=self.level + 1)
            self.sections[number] = section
        self.cur_sec = section
        return section

    def save(self, file, verbosity_save):
        pass

    def dev_save_str(self):
        save_str = ''
        if self.name is not None:
            save_str += str(self.name) + '\n' + "=" * len(str(self.name))
        save_str += self.formatter.to_string(self.output_raw)
        save_str += ' '.join([v.dev_save_str() for _, v in self.sections.items()])
        return save_str
