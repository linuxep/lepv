import os
import unittest

test_dir = os.path.join(os.getcwd())
discover = unittest.defaultTestLoader.discover(
    test_dir, pattern='unitTests.py')
runner = unittest.TextTestRunner()
runner.run(discover)
