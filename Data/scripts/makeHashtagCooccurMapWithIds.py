'''
Usage:
"Usage: python makeHashtagCooccurMapWithIds.py <path-to-tweets-pickled-dir> <tag2id_pickle_file_path >  <co-occurance pickle path to write to>"

Behavior:
Iterates through pickled tweets. For each tweet, records every pair of co-occuring hashtags based on hashtag id in the tag2id pickle file. 
Writes a counter, which maps (tId1, tId2) tuples of tagIds to the count of the times those to tags co-occur in a tweet. 
To ensure non-duping (a,b) and (b,a) pairs, always uses lesser value as first in tuple.  

'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import re



#takes in a hashtagArr and a counter, adds 1 to key ((tId1, tId2) for every coocurrance
def addCooccurances(hashtagArr, counter):
	for i in range(len(hashtagArr)):
		for j in range(i+1, len(hashtagArr)):
			tId1 = tag2id_map[hashtagArr[i]]
			tId2 = tag2id_map[hashtagArr[j]]
			if(tId2 < tId1): #ensure alpha order to avoid duplicating (a,b) and (b,a)
				temp = tId1
				tId1 = tId2
				tId2 = temp
			counter[(tId1, tId2)] = counter[(tId1, tId2)] + 1



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



coOccurCounter = Counter()

if len(sys.argv) != 4:
	print "Usage: python makeHashtagCooccurMapWithIds.py <path-to-tweets-pickled-dir> <tag2id_pickle_file_path >  <co-occurance pickle path to write to>"
else:
	directory_name = sys.argv[1]
	tag2id_pickle_file_path = sys.argv[2]
	cooccurance_pickle_path = sys.argv[3]
	print("dir: " + directory_name)
	print("tag2id path:: " + tag2id_pickle_file_path)

	try:
		f = open(tag2id_pickle_file_path, "rb") 
		tag2id_map = cPickle.load(f)
		f.close()
	except OSError:
		print "problem loading tag2id pickle"
	
	try:
		for filename in os.listdir(directory_name):
			
			tweets_pickle_file = open(directory_name + "/" + filename, "rb")
			tweets = cPickle.load(tweets_pickle_file)
			tweets_pickle_file.close()	
			processTweets(tweets, coOccurCounter)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."

pickle_file_name = cooccurance_pickle_path
f = open(pickle_file_name, "w + b")
cPickle.dump(coOccurCounter, f)
f.close()






