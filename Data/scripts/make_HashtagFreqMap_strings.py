'''
Usage:
	 "Usage: python make_HashtageFreqMap_strings.py <path-to-tweets-pickled-dir> >  <hashtag_frequency_STRINGS_pickle_path to write to>"

Behavior:
Iterates through pickled tweets. For each tweet, records every hashtag. 
Writes a counter, which maps (hashtag) tuples of each hashtage string to the count of the times that hashtag occurs across all tweets.

'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import re



#takes in a hashtagArr and a counter, adds 1 to key (tId) for every coocurrance
def addFrequencies(hashtagArr, counter):
	for i in range(len(hashtagArr)):
		tag = hashtagArr[i]
		counter[tag] = counter[tag] + 1
		



#expects tweet object where 'hashtags'
#returns empty array if no hashtags. returns array of hashtags as strings if they are there.
def getHashtagArray(t):
	tagsArr = []
	if 'hashtags' in t:
		value = t['hashtags']
		if value != "set([''])": #if the list is not empty
			valueCleaned = value[5:-2] # takes off "set([" prefix and "])" suffix
			
			tagsArr = [re.sub(r'\W+', '', tag) for tag in valueCleaned.split(',')] #takes out all but alpha numeric and puts in array
			return tagsArr
	return tagsArr # returns empty arr if no hashtag field, or if field is empty


def processTweets(tweets, counter):
	for t in tweets:
		arr = getHashtagArray(t)
		if len(arr) > 0:
			addFrequencies(arr, counter)



freqCounter = Counter()

if len(sys.argv) != 3:
	print "Usage: python make_HashtageFreqMap_strings.py <path-to-tweets-pickled-dir> >  <hashtag_frequency_STRINGS_pickle_path to write to>"
else:
	directory_name = sys.argv[1]
	hashtag_frequency_pickle_path = sys.argv[2]
	print("dir: " + directory_name)
	
	try:
		for filename in os.listdir(directory_name):
			
			tweets_pickle_file = open(directory_name + "/" + filename, "rb")
			tweets = cPickle.load(tweets_pickle_file)
			tweets_pickle_file.close()	
			processTweets(tweets, freqCounter)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."

pickle_file_name = hashtag_frequency_pickle_path
f = open(pickle_file_name, "w + b")
cPickle.dump(freqCounter, f)
f.close()