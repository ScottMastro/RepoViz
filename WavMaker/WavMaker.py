from Parser import Parser
from Synthesizer import Synthesizer
from Mixer import Mixer

import sys, os
import shutil

from multiprocessing.pool import ThreadPool

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(THIS_DIR + os.pardir)


def cleanup(tmpdir):
    shutil.rmtree(tmpdir)
    
# read project config file
def get_config():
    def get_value(string):
        try:
            return eval(string)
        except:
            return string

    config = open(BASE_DIR + '/config.txt', 'r')
    option_dict = {'BASE_DIR': BASE_DIR}
    option_dict['DATA_DIR'] = BASE_DIR + '/Narratives2_ESS2/Narratives2_ESS2/data/'
    
    for line in config:
        line = line.strip()
        if line and not line.startswith('#'):
            lineSplit = line.split('=')
            if len(lineSplit) == 2:
                key, value = lineSplit
                option_dict[key] = get_value(value)
    config.close()
    
    # set synthesizer
    if option_dict ['synth'] == 'pysynth_o':
        import pysynth_o
        option_dict ['pysynth'] = pysynth_o
    elif option_dict ['synth'] == 'pysynth_b':
        import pysynth_b
        option_dict ['pysynth'] = pysynth_b
    else:
        import pysynth
        option_dict ['pysynth'] = pysynth
        
    # pitchhz is a dict of key->hz entries
    # we need to inverse the dict to perform hz->key lookup.
    inv_pitchhz = dict((v,k) for k,v in option_dict ['pysynth'].pitchhz.iteritems())

    # remove 8 lowest pitches that are inaudiable and 8 highest pitches to make it sound better
    pitch_list = sorted(inv_pitchhz.keys())[8:-8]
    
    option_dict ['pitch_list'] = pitch_list
    option_dict ['inv_pitchhz'] = inv_pitchhz
    return option_dict
    
    
# set the config file in all of the submodules
def set_config(CONFIG):
    Parser.CONFIG = CONFIG
    Synthesizer.CONFIG = CONFIG
    Mixer.CONFIG = CONFIG

# main function
def main():
    CONFIG = get_config()
    set_config(CONFIG)

    outdir = CONFIG['DATA_DIR']
    tmpdir = os.path.join(outdir, "tmp")
    
    if os.path.isdir(tmpdir):
        cleanup(tmpdir)
    os.mkdir(tmpdir)
    
    commits_list = Parser.parse()

    print "synthesizing channels into {0}".format(tmpdir)
    
    # parallel synth
    pool = ThreadPool(processes=len(commits_list))
    synth_threads = []
    
    if CONFIG['use_mixer']:
        if CONFIG['parallel_synth']:
            for x in xrange(0, len(commits_list)):
                async = pool.apply_async(Synthesizer.synth, (commits_list[x], tmpdir, x))
                synth_threads.append(async)
                
            for x in xrange(0, len(commits_list)):
                synth_threads[x].get()
        else:
            for x in xrange(0, len(commits_list)):
                Synthesizer.synth(commits_list[x], tmpdir, x)
        
        print "mixing channels in {0}".format(tmpdir)
        
        outfile = Mixer.mix(tmpdir, outdir)
        
        print "cleaning up tmp directory {0}".format(tmpdir)
        cleanup(tmpdir)
    else:
        Synthesizer.synth_list(commits_list, outdir)
    
    
if __name__ == '__main__':
    main()
