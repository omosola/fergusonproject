import cPickle
import os
import sys
import time
from collections import Counter

directory_name = "partitioned-tweets/tweets-pickled" #default
field = 'n_followers'

distribution = Counter()
num_absent = 0

def addTweetFieldValueToFreqDist(counter, tweet, field):
	if field in tweet:
		value = tweet[field]
		print value
		counter[value] = counter[value] + 1
 	else:
 		global num_absent
 		num_absent += 1
	

def processTweets(tweets, counter, field):
	for t in tweets:
		print t['tweet_text']
		print t['n_followers']
		addTweetFieldValueToFreqDist(counter, t, field)


	
def testTweets(tweets):
	print len(tweets)



t0 = time.clock()

if len(sys.argv) != 3:
	print "Usage: python getFieldStats.py <path-to-tweets-csv-dir> <field>\n fields: n_statuses, retweets, n_friends, n_followers, original_followers"
else:
	directory_name = sys.argv[1]
	field = sys.argv[2]
	print("dir: " + directory_name)
	print("field: " + field)
	try:
		for filename in os.listdir(directory_name):
			tweets_pickle_file = open(directory_name + "/" + filename, "rb")
			tweets = cPickle.load(tweets_pickle_file)
			#processTweets(tweets, distribution, field)
			testTweets(tweets)
			tweets_pickle_file.close()	
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."

print ("num unique values: " + str(len(distribution.items())))
mostCommon = distribution.most_common(2000)

for t in mostCommon:
	print t

print time.clock() - t0,