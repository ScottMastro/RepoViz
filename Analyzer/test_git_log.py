import unittest
from git_log import *

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_getpipeoutput(self):
        output = getpipeoutput(['echo test'])
        self.assertEqual(output, "test")
        
    def test_strippunctuation(self):
        output = strippunctuation('''!()[]{};:'"\,<>./?@#$%^*~=+-_\t     test''')
        self.assertEqual(output, " test")

        
if __name__ == '__main__':
    unittest.main()
