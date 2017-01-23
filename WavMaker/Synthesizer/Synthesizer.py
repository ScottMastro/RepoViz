import math
import os
#from pysynth_o import make_wav

# silent note
SILENCE = [('a0', 4)]

# default name for temporary output channel file
TEMP_OUT_FNAME = "channel{0}.wav"

# frequency array: each channel gets its own note
frequency_array = [43.6535289291, 61.735412657, 123.470825314, 246.941650628, 493.883301256, 987.766602512, 1975.53320502]


class Synthesizer:
    CONFIG = None
    
    # more commits == shorter note    
    @staticmethod
    def compute_note_length(commits_list, commit):
        note_length = Synthesizer.CONFIG['NOTE_LENGTH']
        # max note length difference
        max_step = note_length - 2

        length = len(commits_list)
        if length == 0 or commit == 0:
            return note_length
        
        avg = sum(commits_list) / float(length)
        if avg == 0:
            return note_length
        ratio = commit / avg
        abs_ratio = ratio
        if ratio < 1:
            abs_ratio = 1 / ratio
        step = min(abs_ratio - 1, max_step)
        if ratio < 1:
            step *= -1
        return note_length + step
        
    # maps an arbitrary pitch to one of the pitches in the pitch_list
    # basically a ceiling function
    @staticmethod
    def pitch_map(hz):
        pitch_list = Synthesizer.CONFIG['pitch_list']
        if (hz < 0):
            raise Error("got negative value for hz: {0}".format(hz))
        k = None
        for i in range(0, len(pitch_list)):
            k = pitch_list[i]
            if (k > hz):
                return k
        return k

    # maps an arbitrary pitch to a PySynth key
    @staticmethod
    def hz_to_key(hz):
        hz = Synthesizer.pitch_map(hz)
        return Synthesizer.CONFIG['inv_pitchhz'][hz]

    # maps commit number to a pitch
    # this is an arbitrary algorithm and could be made a lot fancier
    # (e.g. consider rate of change in commits (dx) as well as commits (x))
    @classmethod
    def commit_to_hz(cls, x, num):
        ''' old code
        # exponential function with the following properties:
        # f(2) = 140
        # f(100) = 2100
        a = 132.473
        b = 0.027633
        # where num is the number of the word currently being processed
        return a * math.pow(math.e, (b * x))
        '''
        # pick note from frequency_array
        return frequency_array[num % cls.CONFIG['number_words']]


    # maps commit number to a PySynth key
    @staticmethod
    def commit_to_key(x, num):
        hz = Synthesizer.commit_to_hz(x, num)
        return Synthesizer.hz_to_key(hz)
        
    # now we can produce a song!
    @classmethod
    def commits_to_song(cls, commits_list, num):
        song = []
        vol_list = []
        if len(commits_list) == 0:
            return song, vol_list
        
        for i in range(0, len(commits_list)):
            commit = commits_list[i]
            if cls.CONFIG['variable_note_length']:
                # adjust note length by commit number
                note_len = cls.compute_note_length(commits_list, commit)
            else:
                note_len = cls.CONFIG['NOTE_LENGTH']
            note = (cls.commit_to_key(commit, i), note_len)
            song.append(note)
            if cls.CONFIG['variable_volume']: 
                # add note volume to vol_list
                vol_list.append(Synthesizer.commit_to_vol(commit))
         
        return song, vol_list
        
    @staticmethod    
    def commit_to_vol(commit):
    	c = float(commit)/75 # arbitrary divisor, chosen because it sounds ok?
    	c = min(c, 1.1)
    	c = max(c, 0.1)
    	return c
        
    @classmethod
    def make_wav_file(cls, song, out_dir, out_name, vol_list):
        if len(vol_list) > 0:
            cls.CONFIG['pysynth'].make_wav(song,
                                       fn=os.path.join(out_dir, out_name),
                                       leg_stac=cls.CONFIG['LEG_STAC'],
                                       bpm=cls.CONFIG['BPM'],
                                       vol_list=vol_list)
        else:
            cls.CONFIG['pysynth'].make_wav(song,
                                       fn=os.path.join(out_dir, out_name),
                                       leg_stac=cls.CONFIG['LEG_STAC'],
                                       bpm=cls.CONFIG['BPM'])

    # turns commits history for a word into a wav file
    @classmethod
    def synth(cls, commits_history, outputdir, i):
        song, vol_list = cls.commits_to_song(commits_history, i) 
        fname = TEMP_OUT_FNAME.format(i)
        cls.make_wav_file(song, outputdir, fname, vol_list)
    
    # turns commits history for a list of words into a single output wav file
    # with name given by OUT_FNAME   
    @classmethod
    def synth_list(cls, commits_history, outputdir):
        output = []
        vol_list = []
        # concatenates songs rather than stacking them
        for i,commits in enumerate(commits_history):
            song, vols = cls.commits_to_song(commits, i)
            output += song + SILENCE
            vol_list += vols + [0]
        cls.make_wav_file(output[:-1], outputdir, cls.CONFIG['OUT_FNAME'], vol_list[:-1])
        
