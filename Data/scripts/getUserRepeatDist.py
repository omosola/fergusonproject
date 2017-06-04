'''
Usage:
"Usage: python getUserRepeatDist.py <path-to-tweets-pickle-dir>"

Behavior:
plots the number of tweets per user in our data set. 

'''

import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

directory_name = "partitioned-tweets/tweets-pickled" #default
field = 'name' #default


def setUpPlot(field):
	fig = plt.figure()
	p = fig.add_subplot(2,1,1)
	p.set_yscale('log')
	p.set_xscale('log')
	p.set_xlabel("count tweets by user")
	p.set_ylabel("num users with this tweet count")
	return p

def addTweetFieldValueToCounter(counter, tweet, field):
	if field in tweet:

		value = tweet[field]
		counter[value] = counter[value] + 1
 	else:
 		global num_absent
 		num_absent += 1
	

def processTweets(tweets, counter, field):
	print(len(tweets))
	for t in tweets:

		addTweetFieldValueToCounter(counter, t, field)




nameToCount = Counter()
num_absent = 0

t0 = time.clock() #reports how long it takes to run

if len(sys.argv) != 2:
	print "Usage: python getUserRepeatDist.py <path-to-tweets-pickle-dir>"
else:
	directory_name = sys.argv[1]
	
	print("dir: " + directory_name)
	print("field: " + field)
	try:
		for filename in os.listdir(directory_name):
			
			tweets_pickle_file = open(directory_name + "/" + filename, "rb")
			tweets = cPickle.load(tweets_pickle_file)
			tweets_pickle_file.close()	
			processTweets(tweets, nameToCount, field)
			#testTweets(tweets)
			
	except OSError: 
		print "File reading problem using directory '" + directory_name + "'."


#reporting
print ("num unique values: " + str(len(nameToCount.items())))
print("num tweets without value: " + str(num_absent))

names, counts = zip(*(nameToCount.items()))
maxCount = max(counts)
hist, counts = np.histogram(counts, maxCount + 1, (-.5, maxCount + .5))


#plot histogram
p = setUpPlot(field)
p.scatter(counts[:-1], hist)
plt.show()

print ("run time: " + str( time.clock() - t0))



