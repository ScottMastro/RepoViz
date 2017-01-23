import sys
from os import listdir
from os.path import isfile, join
from pydub import AudioSegment as AS

from multiprocessing.pool import ThreadPool


# return a list of temporary .wav files to be mixed
def get_channel_files(inputdir):
    files = [ join(inputdir, f) for f in listdir(inputdir) if isfile(join(inputdir, f)) ] # all files in dir
    wav_files = [ f for f in files if f.endswith(".wav") ] # wav files in dir
    return wav_files


class Mixer:
    CONFIG = None
    
    # may be able to adjust time between songs by something like
    #return a[:100] + b             # or
    #a.append(b, crossfade=1000)
    @classmethod
    def combine(cls, a, b):
        if cls.CONFIG['overlay_words']:
            return a.overlay(b)
        return a + b
        
    # merge sounds
    @classmethod
    def rec_merge(cls, sounds, pool=None):
        l = len(sounds)
        if l == 0:
            return
        elif l == 1:
            return sounds[0]
        elif l == 2:
            a = sounds[0]
            b = sounds[1]
            return cls.combine(a,b)
        else:
            # recurse on left and right in parallel
            mid = len(sounds)/2
            left = sounds[:mid]
            right = sounds[mid:]
            
            if cls.CONFIG['parallel_synth']:
                # do a parallel merge
                async_left = pool.apply_async(cls.rec_merge, (left, pool))
                async_right = pool.apply_async(cls.rec_merge, (right, pool))
                a = async_left.get()
                b = async_right.get()
            else:
                # sequential merge
                a = cls.rec_merge(left)
                b = cls.rec_merge(right)
            return cls.combine(a,b)
    
    @classmethod
    def mix(cls, channeldir, outputdir):
        channel_files = get_channel_files(channeldir)
        sounds = []
        for each in channel_files:
            sounds.append(AS.from_file(each))
            
        if (len(sounds) == 0):
            print "no channels to mix"
            return None
            
        if cls.CONFIG['parallel_synth']:
            # do a parallel merge
            pool = ThreadPool(processes=len(sounds))
        else:
            pool = None
        
        # merge sounds
        combined_sounds = cls.rec_merge(sounds, pool)
        
        fname = join(outputdir, cls.CONFIG['OUT_FNAME'])
        combined_sounds.export(fname, format='wav')
        return fname
        
        
