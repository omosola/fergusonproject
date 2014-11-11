'''
Usage:
python getFieldStats.py <path-to-tweets-pickled-dir> <field> 
where field has a integer value (will not work for timestamps. booleans, etc)
 

'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import re

coOccurCounter = Counter()

#takes in 
def addCooccurances(hashtagArr, counter):
	for i in len(hashtagArr):
		for j in len(i+1, len(hashtagArr)):
			t1 = hashtagArr[i]
			t2 = hashtagArr[j]
			#do stuff



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
			addCooccurances(arr, counter)



c = Counter()

if len(sys.argv) != 2:
	print "Usage: python hashtagCooccurV1.py <path-to-tweets-pickled-dir> "
else:
	directory_name = sys.argv[1]
	
	print("dir: " + directory_name)
	
	try:
		for filename in os.listdir(directory_name):
			
			tweets_pickle_file = open(directory_name + "/" + filename, "rb")
			tweets = cPickle.load(tweets_pickle_file)
			tweets_pickle_file.close()	
			processTweets(tweets, c)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."






