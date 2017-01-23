#!/usr/bin/env python
#word frequency counter algorithm from:
#http://www.yasyf.com/coding/simple-python-word-frequency-count/ 

import sys
import os


#file is output from previous step - all word changes separated by spaces/lines
def get_top_words():
    words_to_ignore = ['the']
    words_min_size = 3
    text = ""
    
    f = open('words.txt','rU')

    #from http://www.yasyf.com/coding/simple-python-word-frequency-count/ 
    #finds the most frequent words
    for line in f:
	    text += line
     
    words = text.split()
    wordcount = {}
    for word in words:
	    if word not in words_to_ignore and len(word) >= words_min_size:
		    if word in wordcount:
			    wordcount[word] += 1
		    else:
			    wordcount[word] = 1			

    f.close()
    return sorted(wordcount,key=wordcount.get,reverse=True)
    
#function for writing number of times a common word was added/removed on a certain day
def writedata(file, date, cat):
    #write commit date
    file.write("%\t" + date + "\n")

    #compute word frequency

    counter = 0;
    #for each top ranking word
    for word in sortedbyfrequency:
	    #write the word and a tab separator
	    file.write(word + "\t")
	
	    #find the # of times that word was used on a given day
	    hits = 0;
	    for w in cat.split():
		    if w == word:	
			    hits += 1
	    file.write(str(hits) + "\n")
	
	    #only consider top n words
	    counter += 1
	    if counter >= n:
		    break

if __name__ == '__main__':
    #n is the argument given for the cut-off of top words to analyze
    #(ex. n = 3 will analyze top 3 most frequent words)
    n = int(sys.argv[1])
    if not n:
        n = 7

    #file is output from previous step - all word changes separated by spaces/lines
    sortedbyfrequency = get_top_words()

    #start to create final output file
    #-----------------------------------------

    analyzer_dir = os.path.dirname(os.path.realpath(__file__))

    #file with git log commit changes
    data = open('all.txt', 'r')
    #final output file
    commits = open(analyzer_dir + '/commits.txt', 'w')

    #get folder currently working in -> write git repository name
    commits.write(os.getcwd().split("/")[len(os.getcwd().split("/")) - 1] + "\n")

    date = ""
    #holds every word inserted and deleted on a given day
    cat = ""

    #iterates though all commits
    for line in data:

	    #commits separated by &&&
	    if line.startswith('&&&'):
		    d  = line.split()[2]
		    #if the current commit happened on the same day as the previous one, append them
		    #(requirement: already sorted by age)
		    if d != date:
			    if(date != ""):
				    writedata(commits, date, cat)
			    date = d
			    cat = ""
			    continue
		    else:
			    continue
	    #these lines denote a line addition or removal happening in a commit
	    if line.startswith('+') or line.startswith('-'):
		    cat += line

    #writes last commit
    writedata(commits, date, cat)

    commits.close()
    data.close()
