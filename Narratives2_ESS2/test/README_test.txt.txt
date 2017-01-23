Manual tests on visualization; 
 -testing if words match up with frequencies and if frequencies match up with lines:

(1) set boolean spiral = false to switch to linear visualization

(2) set wav_filename = "by_frequency/x.wav" where x is
     - 43
     - 61
     - 123
     - 246
     - 493
     - 987
     - 1975

    These .wav files play one frequency for 10 seconds.

 (3) run program, look for colour activity on a single line.
 (4) if more than one line is responding to sound, increase min_cutoff and/or decrease amplifier
     if no line is responding to sound, decrease min_cutoff and/or increase amplifier
	-> these variables prevent "sound contamination" when used correctly
 (5) look for only one line responding to the frequency, see Narratives2_ESS2\test\testing_output.png for example
  

