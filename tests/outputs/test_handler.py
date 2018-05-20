from __future__ import print_function, division, absolute_import

import contextlib
import io
import unittest

import uniphy as up


class TestOutputManager(unittest.TestCase):

    def test_print(self):
        out = up.output()

        to_print = ['asdf', 2, 5.5, 'times']
        true_str = ' '.join([str(o) for o in to_print]) + '\n'
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            out.print(*to_print)
            self.assertEqual(true_str, stream.getvalue())
            to_print = [42, "it's the answer"]
            sep = ' no '
            end = '\n\n\n'
            true_str += sep.join([str(o) for o in to_print]) + end
            out.p(42, "it's the answer", sep=sep, end=end)
            self.assertEqual(true_str, stream.getvalue())
            sec1 = out.section()
