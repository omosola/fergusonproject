'''
Usage:
python getFieldStatsHistogramVersion.py <path-to-tweets-csv-dir> <field> 
where field has a integer count value (will not work for timestamps. booleans, etc)

Behavior:

Iterates through pickled files, and through each tweet in each file to fill the sample array. 
Makes a histogram of the counts, and plots the histogram. 

TODO: may be buggy for some fields. Tested on n_friends.  



'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

directory_name = "partitioned-tweets/tweets-pickled" #default
field = 'n_followers' #default



def isNum(s):
    try:
        n =  float(s)
        return True
    except ValueError:
        return False



def setUpPlot(field):
	fig = plt.figure()
	p = fig.add_subplot(2,1,1)
	p.set_yscale('log')
	p.set_xscale('log')
	p.set_xlabel(field + " count")
	p.set_ylabel('proportional number of tweets with ' + field + " count")
	return p

def addTweetFieldValueToSamples(sampleArr, tweet, field):
	if field in tweet:

		value = tweet[field]
		if(isNum(value)):
			sampleArr.append(float(value))
			return 
 	#only add to num_absent if we werent able to apend a value
 	global num_absent
 	num_absent += 1
	

def processTweets(tweets, sampleArr, field):
	
	for t in tweets:

		addTweetFieldValueToSamples(sampleArr, t, field)




samples = []
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
			processTweets(tweets, samples, field)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."


#reporting

#clean samples
cleanedSamples = samples

#make histogram
maxVal = max(cleanedSamples)
freq, field_counts = np.histogram(cleanedSamples, maxVal + 1, (-.5, maxVal + .5), normed=True)

#plot histogram
p = setUpPlot(field)
p.scatter(field_counts[:-1], freq)
plt.show()


print("num tweets without value: " + str(num_absent))

print ("run time: " + str( time.clock() - t0))


