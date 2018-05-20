import unittest

import uniphy as up

class TestOutputManager(unittest.TestCase):


    def test_creation(self):
        import uniphy.outputs.handler
        default_out = up.output()
        self.assertIsInstance(default_out, up.outputs.handler.Output)
        self. assertIs(up.output('test1'), up.output('test1'))
        self. assertIs(default_out, up.output())
        self. assertIsNot(up.output('test1'), up.output('test2'))

