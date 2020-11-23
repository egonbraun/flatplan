import unittest
from src import __version__


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.0.0")
