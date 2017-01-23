import unittest
from word_counter import get_top_words

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_top_words(self):
        top_words = get_top_words()
        self.assertEqual(type(top_words), list)
        self.assertEqual(len(top_words), 1329)

        
if __name__ == '__main__':
    unittest.main()
