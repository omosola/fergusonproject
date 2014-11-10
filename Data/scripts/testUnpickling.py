import cPickle
import os
import sys
import time

directory_name = "partitioned-tweets/tweets-pickled"

total_tweets = 0

t0 = time.clock()

c = 0
low_test = 20
num_test = 10

for filename in os.listdir(directory_name):

	tweets_pickle_file = open(directory_name + "/" + filename, "rb")
	
	tweets = cPickle.load(tweets_pickle_file)
	total_tweets += len(tweets)
	if c > low_test and c < num_test + low_test:
		print tweets[0]
			
		c += 1
	tweets_pickle_file.close()
print total_tweets
print time.clock() - t0