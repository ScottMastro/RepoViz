import unittest
from Parser import Parser
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(THIS_DIR + os.pardir)

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        Parser.CONFIG = {'BASE_DIR': BASE_DIR,
                         'DATA_DIR': BASE_DIR + '/Narratives2_ESS2/Narratives2_ESS2/data/',
                         'test': True,
                         'granularity': 1,
                         'overlay_words': False}
        self.data_list = Parser.parse()
        
    def test_data_list(self):
        self.assertTrue(type(self.data_list) is type([]))
        self.assertEqual(len(self.data_list), 107)
        self.assertTrue(type(self.data_list[0]) is type([]))
        self.assertEqual(len(self.data_list[0]), 5)
        self.assertTrue(type(self.data_list[0][0]) is int)
        
    def test_avg_x_days(self):
        twoD_list = [[1,2],[3,4],[5,6]]
        self.assertEqual(Parser.avg_x_days(twoD_list, 1), twoD_list)
        self.assertEqual(Parser.avg_x_days(twoD_list, 2), [[1.5], [3.5], [5.5]])

if __name__ == '__main__':
    unittest.main()
