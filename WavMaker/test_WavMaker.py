import unittest
from Parser import Parser
from Synthesizer import Synthesizer
from Mixer import Mixer
import WavMaker

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.conf = WavMaker.get_config()
    
    def test_get_config(self):
        conf = self.conf
        self.assertTrue('pitch_list' in conf)
        self.assertTrue('DATA_DIR' in conf)
        self.assertTrue('pysynth' in conf)
        self.assertTrue('use_mixer' in conf)
        self.assertTrue('variable_volume' in conf)
        
    def test_set_config(self):
        conf = self.conf
        WavMaker.set_config(conf)
        self.assertEqual(conf, Parser.CONFIG)
        self.assertEqual(conf, Synthesizer.CONFIG)
        self.assertEqual(conf, Mixer.CONFIG)
        
if __name__ == '__main__':
    unittest.main()
