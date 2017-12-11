#!/usr/bin/python
# progressioncheck.py
# Purpose: To check the completion of manual transcription
# Last modified on: 19th October 2017

# ------------------------------------------
# Import modules
from __future__ import print_function

import os
import re
import sys
from datetime import datetime

try:
    raw_input = input
except BaseException:
    pass


# ------------------------------------------
# Input/Output
def fileinput(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
        return data


def fileoutput(filename, content):
    with open(filename, 'a') as f:
        f.write(content)


# ------------------------------------------
# To check for "**"
def progcheck(textgrid):
    global counter, counter_sc, duration
    for lines in textgrid:
        search1 = re.search('text\s=\s\"[/*a-z<>\s\-()\']+\"', lines)
        search2 = re.search('text\s=\s\"\*+[/a-z\s\'-<>A-Z]+\"', lines)
        time = re.search('\d\d.\d\d', lines)
        if search1:
            counter += 1
            # print search1.group()
        if search2:
            counter_sc += 1
            # print search2.group()
        if time:
            duration = time.group()


# ------------------------------------------
# To calculate percentage of completion
def countpercent():
    diff = float(counter - counter_sc)
    per_done = round(float((diff / counter) * 100), 2)
    return per_done


# ------------------------------------------
# For output to progression_log.txt
def log_inform(textgridname, tname, fileid):
    information = ''
    completion_percent = countpercent()
    information = '{0} {1:^50} {2}'.format('\n\n', str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                           '\n-----------------------'
                                           '-------------------------'
                                           '-------')
    information += '{0} {1} {2}'.format('\n', 'Filename: ', fileid)
    information += '{0} {1} {2:^15}'.format('\n', 'Transcriber: ', tname)
    information += '{0} {1} {2:>8}s'.format('\n', 'File Duration: ', duration)
    information += '{0} {1} {2:>5}%\n'.format('\n', 'File transcribed: ', completion_percent)
    return information


# ------------------------------------------
# Main caller
def main():
    if len(sys.argv) < 2:
        print('Usage: python progressioncheck.py <TextGridFile>')
        exit()
    textgridname = sys.argv[1]
    # textgridname = '/home/zhihao/Desktop/for_manual_transcription/mml-3-nov-2017-b-session1-2-clean.TextGrid'
    fileid = os.path.basename(os.path.splitext(textgridname)[0])
    tname = raw_input('Please enter your name: ')
    # tname = 'test'
    # textgri23 dname = 'test.TextGrid' #For debugging
    content = fileinput(textgridname)
    progcheck(content)
    print(log_inform(textgridname, tname, fileid))
    fileoutput('progression_log.txt', str(log_inform(textgridname, tname, fileid)))
    # print '\nPlease check "progression_log.txt"'
    return


# ------------------------------------------
# Frame
counter = 0
counter_sc = 0
duration = 0
main()
