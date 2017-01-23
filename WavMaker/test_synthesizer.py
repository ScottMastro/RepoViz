import unittest
from Parser import Parser
from Synthesizer import Synthesizer
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(THIS_DIR + os.pardir)

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        import pysynth
        inv_pitchhz = dict((v,k) for k,v in pysynth.pitchhz.iteritems())
        pitch_list = sorted(inv_pitchhz.keys())[8:-8]
        
        config = {'BASE_DIR': BASE_DIR,
                         'DATA_DIR': BASE_DIR + '/Narratives2_ESS2/Narratives2_ESS2/data/',
                         'test': True,
                         'granularity': 1,
                         'overlay_words': False,
                         'pysynth': pysynth,
                         'pitch_list': pitch_list,
                         'inv_pitchhz': inv_pitchhz,
                         'number_words': 7,
                         'variable_note_length': False,
                         'NOTE_LENGTH': 6,
                         'variable_volume': True}
        Synthesizer.CONFIG = config
        Parser.CONFIG = config
        self.data_list = Parser.parse()

        
    def test_commits_to_hz(self):
        self.assertEqual(int(Synthesizer.commit_to_hz(30, 1)), 61)
        
    def test_hz_to_key(self):
        self.assertEqual(Synthesizer.hz_to_key(5500), 'e7')
        self.assertEqual(Synthesizer.hz_to_key(0), 'f1')
        self.assertEqual(Synthesizer.hz_to_key(2200.5), 'c#7')
        
    def test_commits_to_song(self):
        output = Synthesizer.commits_to_song(self.data_list[0], 5)
        self.assertEqual(type(output), tuple)
        self.assertEqual(len(output), 2)
        self.assertEqual(type(output[0]), list)
        self.assertEqual(type(output[1]), list)
        self.assertEqual(len(output[0]), 5)
        self.assertEqual(len(output[1]), 5)
        
    def test_commits_to_key(self):
        self.assertEqual(Synthesizer.commit_to_key(30, 2), 'b2')
        
    def test_commit_to_vol(self):
        self.assertEqual(Synthesizer.commit_to_vol(75*2), 1.1)
        self.assertEqual(Synthesizer.commit_to_vol(0.01), 0.1)
        self.assertEqual(Synthesizer.commit_to_vol(75/2.0), 0.5)
        
    def test_pitch_map(self):
        self.assertEqual(int(Synthesizer.pitch_map(41)), 43)
        self.assertEqual(int(Synthesizer.pitch_map(2000)), 2093)
        
if __name__ == '__main__':
    unittest.main()
