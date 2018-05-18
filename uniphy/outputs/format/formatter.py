from .storage import ObjectStorage
from . import storage

from uniphy.outputs.format.storage import ObjectStorage


class FormatterBase():
    pass


def dummy_title_formatter(*args, sep, end):
    """Convert *args* to a string

    Parameters
    ----------
    args :
    sep :
    end :

    Returns
    -------
    str : the concatenated args

    """
    text = sep.join(args) + end
    text = text.replace(sep, '', 1)  # remove leading `sep`
    return text

class Formatter(FormatterBase):

    def __init__(self):
        super().__init__()

        self.title_by_rank = [dummy_title_formatter for _ in range(10)]
