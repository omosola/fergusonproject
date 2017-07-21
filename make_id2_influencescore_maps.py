
"""
Author: Kelsey
Associates a hashtag ID with the number of followers, number followed, and retweets from the tweet associated with that hashtag.
"""

import cPickle
import os
import sys
import time
from collections import Counter
from collections import defaultdict
import numpy as np
import re

def pickleDict(tagDict, dict_pickle_filename):
        ## pickle the tweets array of objects
	dict_pickle_file = open(dict_pickle_filename, "w+b")
	cPickle.dump(tagDict, dict_pickle_file)
	dict_pickle_file.close()

#Want to get average influence score of every hashtag, and co-occurrence entry.
def compute_average_influence_scores(influenceDict):
	print ("We have reached averages scores")
	for key, val in influenceDict.iteritems():
		totalLen = float(len(val))
		total = float(sum(val))
		average_influence_score =  total/totalLen
		influenceDict[key] = average_influence_score



#For each combination within the hashatag array, add the influence score. NumRetweets/numFollowers. If numFollowers = 0 then
# influence score = numRetweets + 1
def addInfluenceScores(hashtagArr,numFollowers,numRetweets, influenceDict):
	influenceScore = float(0)
	if numFollowers == 0 and numRetweets != 0:
		influenceScore = numRetweets + 1
	elif numFollowers == 0 and numRetweets == 0:
		influenceScore = 0
	else:
		influenceScore = numRetweets / numFollowers

	print ("Adding influence score %f to individual hashtags" % (influenceScore))
	for tag in hashtagArr:
		tID = tag2id_map[tag]
		print ("Appending ",tID,tag)
		influenceDict[tID].append(influenceScore)




	for i in range(len(hashtagArr)):
		for j in range(i+1, len(hashtagArr)):
			tID1 = tag2id_map[hashtagArr[i]]
			tID2 = tag2id_map[hashtagArr[j]]
			if(tID2 < tID1): #ensure alpha order to avoid duplicating (a,b) and (b,a)
				temp = tID1
				tID1 = tID2
				tID2 = temp
				print ("Appending ",tID1, hashtagArr[j],tID2,hashtagArr[i])
				influenceDict[(tID1, tID2)].append(influenceScore)



def addHashtagsToSet(tagArr, influenceDict):
	influenceDict.update(tagArr)

#Checks the tweet to see if it has retweets. If not , 0 returned.
def getnumRetweets(t):
	if 'retweets' in t:
		numRetweets = t['retweets']		
		strlen = len(numRetweets)
		try:
			numRetweets = float(numRetweets)
		except ValueError:
			#print "This retweet value won't work", numRetweets
			numRetweets = float(0)
		# if not strlen == 0:
		# 	print "numRetweets before strip ",numRetweets," with length ", len(numRetweets)
		# 	numRetweets = numRetweets[0:-2]
		# 	print "The number of retweets ", numRetweets
		# 	return numRetweets
		return numRetweets
	return float(0)

#Checks the tweet to see if it has numFollowers. If not , 0 returned.
def getnumFollowers(t):
	if 'n_followers' in t:
		numFollowers = t['n_followers']
		strlen = len(numFollowers)
		#num_followers = []
		try:
			numFollowers = float(numFollowers)
		except ValueError:
			#print "This numFollowers won't work", numFollowers
			numFollowers = float(0)
	#if not strlen == 0:
	# for n in numFollowers.split():
	# 	try:
	# 		num_followers.append(float(n))
	# 	except ValueError:
	# 		pass

		#print "numFollowers before strip ",numFollowers," with length ", len(numFollowers)
		#numFollowers = numFollowers[0:-2]
		#print "The number of Followers ", numFollowers
		return numFollowers
	return float(0)

def getHashtagArray(t):
	tagsArr = []
	if 'hashtags' in t:
		value = t['hashtags']
		if value != "set([''])": #if the list is not empty
			valueCleaned = value[5:-2] # takes off "set([" prefix and "])" suffix
			
			tagsArr = [re.sub(r'\W+', '', tag) for tag in valueCleaned.split(',')] #takes out all but alpha numeric and puts in array
			return tagsArr
	return tagsArr 

def processTweets(tweets,influenceDict):
	for t in tweets:
		hashtags = getHashtagArray(t)
		numFollowers = getnumFollowers(t)
		numRetweets = getnumRetweets(t)
		if len(hashtags) > 0:
			addInfluenceScores(hashtags, numFollowers,numRetweets, influenceDict)



influenceDict = defaultdict(list)
#to fill with all tags from all tweets 

if len(sys.argv) != 4:
	print ("Usage: python scripts/make_id2_influencescore_maps.py <path-to-pickled-tweets> <path-to-tag2id-map-pickle> <path-to-id2_influencescore_map> ")
#/Users/kelseyyoung/Documents/Junior Year/CS224W/fergProject/fergusonproject/Data/partitioned-tweets/tweets-pickled
# Users/kelseyyoung/Documents/Junior Year/CS224W/fergProject/fergusonproject/Data/hashtag-id-maps/tag2id.p
# Users/kelseyyoung/Documents/Junior Year/CS224W/fergProject/fergusonproject/Data/hashtag-id-maps/id2_influence.p
else:
	directory_name = sys.argv[1]
	tag2ID_pickle_filename = sys.argv[2]
	id2_influence_score_map_filename = sys.argv[3]

try:
	f = open(tag2ID_pickle_filename, "rb") 
	tag2id_map = cPickle.load(f)
	f.close()
except OSError:
	print ("problem loading tag2id pickle")

print("dir: " + directory_name)

try:
	for filename in os.listdir(directory_name):
		tweets_pickle_file = open(directory_name + "/" + filename, "rb")
		tweets = cPickle.load(tweets_pickle_file)
		tweets_pickle_file.close()
		processTweets(tweets, influenceDict)
		#testTweets(tweets)
except OSError: 
	print ("File reading problem using directory '" + directory_name + "'.")



compute_average_influence_scores(influenceDict)
pickleDict(influenceDict, id2_influence_score_map_filename)
