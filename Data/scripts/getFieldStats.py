'''
Usage:
python getFieldStats.py <path-to-tweets-csv-dir> <field> 
where field has a integer value (will not work for timestamps. booleans, etc)

Behavior:
Creates a counter to collect the frequency of values for the field. 
Iterates through pickled files, and through each tweet in each file to fill the counter. 
Counts unique values. 
Counts tweets where the field is absent.

TODO: I have been testing this on n_followers, which occasionally has 'True' and other string 
values. I'm not sure if those are a bug in our stuff, or a fluke in the data. It makes
doing other things (like plotting) a little tricky - we need to clean those out of the counter. 

Choice: I decided to make a Counter to avoid having an array of length = num_tweets. I haven't tried doing that
but don't let me stop you. It might be good for using numpy's histogram. 

'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np


directory_name = "partitioned-tweets/tweets-pickled" #default
field = 'n_followers' #default



def addTweetFieldValueToFreqDist(counter, tweet, field):
	if field in tweet:
		value = tweet[field]
		
		if not(value == 'True'):
			counter[value] = counter[value] + 1
		
 	else:
 		global num_absent
 		num_absent += 1
	

def processTweets(tweets, counter, field):
	for t in tweets:
		addTweetFieldValueToFreqDist(counter, t, field)




distribution = Counter()
num_absent = 0

t0 = time.clock() #reports how long it takes to run

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
			tweets_pickle_file.close()	
			processTweets(tweets, distribution, field)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."


#reporting
print ("num unique values: " + str(len(distribution.items())))
print("num tweets without value: " + str(num_absent))

mostCommon = distribution.most_common(2000)
for t in mostCommon:
	print t

print ("run time: " + str( time.clock() - t0))



