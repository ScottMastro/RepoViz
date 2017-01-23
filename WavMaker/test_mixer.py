import unittest
from Mixer import Mixer

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        Mixer.CONFIG = {'parallel_synth': False, 'overlay_words': False}
        self.sounds = [1,2,3,4]
        
    def test_rec_merge(self):
        self.assertEqual(Mixer.rec_merge(self.sounds), sum(self.sounds))
        

if __name__ == '__main__':
    unittest.main()
