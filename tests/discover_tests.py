# -*- coding: utf-8 -*-

import unittest
import sys

# Append uniphy package to python path.
package_path = '../uniphy'
sys.path.append(package_path)

# Load and run tests.
loader = unittest.TestLoader()
tests = loader.discover('.')
testRunner = unittest.runner.TextTestRunner()
finished_test = testRunner.run(tests)

# If failed, finish with exit status != 0
failed = not finished_test.wasSuccessful()
sys.exit(failed)
