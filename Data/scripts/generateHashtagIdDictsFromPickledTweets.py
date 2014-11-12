
'''
Usage: python scripts/generateHashtagIdDictsFromPickledTweets.py <path-to-pickled-tweets> <path-to-id2tag-map-pickle> <path-to-tag2id-map-pickle>

Uses pickled tweets, creates uniq ids for hashtags. Writes the id2tag pickled dict to path-to-id2tag-map-pickle.
 Writes the tag2id pickled dict to path-to-tag2id-map-pickle

'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import re


def pickleDict(tagDict, dict_pickle_filename):
        ## pickle the tweets array of objects
	dict_pickle_file = open(dict_pickle_filename, "w+b")
	cPickle.dump(tagDict, dict_pickle_file)
	dict_pickle_file.close()

def addHashtagsToSet(tagArr, tagSet):
	tagSet.update(tagArr)

def getHashtagArray(t):
	tagsArr = []
	if 'hashtags' in t:
		value = t['hashtags']
		if value != "set([''])": #if the list is not empty
			valueCleaned = value[5:-2] # takes off "set([" prefix and "])" suffix
			
			tagsArr = [re.sub(r'\W+', '', tag) for tag in valueCleaned.split(',')] #takes out all but alpha numeric and puts in array
			return tagsArr
	return tagsArr 

def processTweets(tweets, tagSet):
	for t in tweets:
		arr = getHashtagArray(t)
		if len(arr) > 0:
			addHashtagsToSet(arr, tagSet)


def fillTagIdDicts(uniqTagList):
	id2TagDict = {}
	tag2IDDict = {}
	for i,tag in enumerate(uniqTagList):
		id2TagDict[i] = tag
		tag2IDDict[tag] = i
	return id2TagDict, tag2IDDict


tagSet = set() #to fill with all tags from all tweets 


if len(sys.argv) != 4:
	print "Usage: python scripts/generateHashtagIdDictsFromPickledTweets.py <path-to-pickled-tweets> <path-to-id2tag-map-pickle> <path-to-tag2id-map-pickle>"

else:
	directory_name = sys.argv[1]
	id2Tag_pickle_filename = sys.argv[2]
	tag2ID_pickle_filename = sys.argv[3]
	print("dir: " + directory_name)

	try:
		for filename in os.listdir(directory_name):
			
			tweets_pickle_file = open(directory_name + "/" + filename, "rb")
			tweets = cPickle.load(tweets_pickle_file)
			tweets_pickle_file.close()	
			processTweets(tweets, tagSet)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."



uniqTagList = list(tagSet)
uniqTagList.sort()

id2TagDict, tag2IDDict = fillTagIdDicts(uniqTagList)

pickleDict(id2TagDict, id2Tag_pickle_filename)
pickleDict(tag2IDDict, tag2ID_pickle_filename)

	#pickleDicts(id2TagDict,id2Tag_pickle_filename)
	#pickleDicts(tag2IDDict, tag2ID_pickle_filename)