#!/usr/bin/env python
#punctuation stripping algorithm from:
#http://www.programiz.com/python-programming/examples/remove-punctuation
#command line interaction from:
#https://github.com/hoxu/gitstats

import subprocess
import sys
import string
import re
import time

#from https://github.com/hoxu/gitstats
#allows code to send commands to terminal and retrieve stdout
def getpipeoutput(cmds, quiet = False):
	global exectime_external
	start = time.time()
	print '>> ' + ' | '.join(cmds),
	sys.stdout.flush()
	p = subprocess.Popen(cmds[0], stdout = subprocess.PIPE, shell = True)
	processes=[p]
	for x in cmds[1:]:
		p = subprocess.Popen(x, stdin = p.stdout, stdout = subprocess.PIPE, shell = True)
		processes.append(p)
	output = p.communicate()[0]
	for p in processes:
		p.wait()
	end = time.time()
	if not quiet:
		print '\r',
		print '[%.5f] >> %s' % (end - start, ' | '.join(cmds))
	return output.rstrip('\n')

#from http://www.programiz.com/python-programming/examples/remove-punctuation
#removes all given punctuation from a string
def strippunctuation(str):
	# define punctuations
	punctuations = '''!()[]{};:'"\,<>./?@#$%^*~=+-_'''
	no_punct = ""
	
	for char in str:
		if char not in punctuations:
			no_punct = no_punct + char
		else:
			no_punct = no_punct + " ";
			
	#condenses variable sized whitespace to single whitespace
	no_punct = re.sub('\s+',' ',no_punct)
	return no_punct


if __name__ == '__main__':
    n = len(sys.argv)
    lines = ""

    #send git log command to fetch all relevant information

    #may or may not use directory to repository .git -> depends on if it was given as argument
    if n > 1:	
	    arg = str(sys.argv[1])
	    if not arg.endswith('.git'):
	        if not arg.endswith('/'):
	            arg += '/'
            arg += '.git'
	
	    lines = getpipeoutput(['git --git-dir ' + arg + ' log -p --shortstat --date-order --reverse --date=short --pretty=format:"&&& %H %ad %cn"']).split('\n')

    else:
	    #send git log command to fetch all relevant information
	    lines = getpipeoutput(['git log -p --shortstat --date-order --reverse --date=short --pretty=format:"&&& %H %ad %cn"']).split('\n')

    #example output:

    #&&& c00bb58dbe86e7d9b656dd4bac2e76e7c80b456c 2014-02-02 Scott Mastro
    #1 files changed, 2 insertions(+), 1 deletions(-)
    #
    #diff --git a/README.txt b/README.txt
    #index 83fee50..eecfe47 100644
    #--- a/README.txt
    #+++ b/README.txt
    #@@ -1,15 +1,6 @@
    # + this was added
    # + so was this
    # - this was removed

    first_line = False
    all = open('all.txt', 'w')
    words = open('words.txt', 'w')

    for line in lines:
	    if len(line) == 0:
		    continue
	
	    #write line with commit hash, date and author
	    if line.startswith('&&&'):
		    all.write(line + '\n')
		    first_line = True
		    continue
	
	    #write line containing insert/delete summary
	    if first_line == True:
		    all.write(line.lstrip() + '\n')
		    first_line = False
		    continue
	
	    #write line specifying a deletion, remove all punctuation
	    if line.startswith('-') and not line.startswith('--'):
		    l = strippunctuation(line)
		
		    words.write(l + '\n')
		    all.write('-' + l + '\n')
		    continue
		
	    #write line specifying an insertion, remove all punctuation	
	    if line.startswith('+') and not line.startswith('++'):
		    l = strippunctuation(line)
		
		    words.write(l + '\n')
		    all.write('+' + l + '\n')
		    continue

    all.close()
    words.close()
