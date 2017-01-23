import os
import numpy as np
import math
import re
import datetime

DAY = 1 # days


class Parser:
    CONFIG = None
    
    # shrink data size by averaging over a time period
    # twoD_list: list of values (one commit value for each day)
    # x: number of days to average on
    # returns list with of x elements from commit_list averaged
    @staticmethod
    def avg_x_days(twoD_list, x):
        def avg(commit_list):
            result = []
            for count in xrange(1, 1 + int(math.ceil(len(commit_list)/float(x)))):
                arr = commit_list[(count-1) * x: count * x]
                avg = sum(arr)/float(len(arr))
                result.append(avg)
            return result
        twoD_list_avg_x_days = []
        for word in twoD_list:
            twoD_list_avg_x_days.append(avg(word))
        return twoD_list_avg_x_days

    @staticmethod
    def add_dict_entry(dict_, key, num):
        if key in dict_:
            dict_[key].append(num)
        else:
            dict_[key] = [num]
            
    # Create file with list of top words
    @classmethod
    def write_word_file(cls, words):
        f = open(cls.CONFIG['DATA_DIR'] + 'commit_words.txt', 'w')
        for key in words:
            f.write(key + '\n')
        f.close()

    # Create file with list of commit dates
    @classmethod
    def write_dates_file(cls, dates):
        def to_pretty_date(date):
            year,month,day = date.split('-')
            return datetime.date(int(year), int(month), int(day)).strftime('%B %d %Y')
        
        f = open(cls.CONFIG['DATA_DIR'] + 'commit_dates.txt', 'w')
        for date in dates:
            f.write(to_pretty_date(date) + '\n')
        f.close()

    # process the input commit data file
    @classmethod
    def process_file(cls, file_name):
        f = open(file_name, 'r')
        repo_name = None
        word_dict = {}
        dates = []
        
        for line in f:
            if not repo_name:
                repo_name = line
                continue
            
            lineSplit = re.split('\t| ', line)
            
            if len(lineSplit) == 2 and lineSplit[0] is not '%':
                word = lineSplit[0]
                num = int(lineSplit[1])
                Parser.add_dict_entry(word_dict, word, num)
            elif lineSplit[0] is '%':
                dates.append(lineSplit[1])
        f.close()
        # iterate over dictionary, make into array of values
        twoD_list = [word_dict[key] for key in word_dict]

        # Create file with list of commit words
        cls.write_word_file(word_dict)

        # Create file with list of commit dates
        cls.write_dates_file(dates)

        # shrink data size by averaging over a time period
        if cls.CONFIG['granularity'] > DAY:
            twoD_list = cls.avg_x_days(twoD_list, cls.CONFIG['granularity'])
            
        if cls.CONFIG['overlay_words']:
            return twoD_list
        else:
            # order 2D array structure as a list of date entries
            # with each date entry containing a list of entries for each word
            return np.flipud(np.rot90(twoD_list)).tolist()
    
    @classmethod
    def parse(cls):
        data_dir = cls.CONFIG['BASE_DIR']
        if (cls.CONFIG['test']):
            in_file = 'test.txt'
            data_dir += '/test/'
        else:
            in_file = 'commits.txt'
            data_dir += '/Analyzer/'
        data = []
        for file_name in os.listdir(data_dir):
            if file_name.endswith(in_file):
                data += cls.process_file(data_dir + file_name)
        return data
            
