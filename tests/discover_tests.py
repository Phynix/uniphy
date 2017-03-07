# -*- coding: utf-8 -*-

import unittest
import sys

package_path = '../uniphy'
sys.path.append(package_path)

loader = unittest.TestLoader()
tests = loader.discover('.')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
