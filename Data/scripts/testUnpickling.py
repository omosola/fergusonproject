import cPickle
import os
import sys
import time



directory_name = "partitioned-tweets/tweets-pickled"

total_tweets = 0

t0 = time.clock()



for filename in os.listdir(directory_name):

	tweets_pickle_file = open(directory_name + "/" + filename, "rb")
	
	tweets = cPickle.load(tweets_pickle_file)
	total_tweets += len(tweets)

	#print tweets[0]
			
		
	tweets_pickle_file.close()
print total_tweets
print time.clock() - t0