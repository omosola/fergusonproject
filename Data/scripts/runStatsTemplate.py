import cPickle
import os
import sys
import time

directory_name = "partitioned-tweets/tweets-pickled"

total_tweets = 0

t0 = time.clock()

c = 10

for filename in os.listdir(directory_name):

	tweets_pickle_file = open(directory_name + "/" + filename, "rb")
	
	tweets = cPickle.load(tweets_pickle_file)
	total_tweets += len(tweets)
	if c > 0:
		print tweets[0]
			
		c -= 1
	tweets_pickle_file.close()
print total_tweets
print time.clock() - t0,

if len(sys.argv) != 3:
	print "Usage: python getFieldStats.py <path-to-tweets-csv-dir>"
else:
	directory_name = sys.argv[1]
	try:
		for filename in os.listdir(directory_name):
			if filename.endswith(".csv"):
				pickle_filename = filename[:-4] + ".p"

				pickleTweets(os.path.join(directory_name, filename), \
						     os.path.join(directory_name,pickle_filename))
	except OSError: 
		print "Directory '" + directory_name + "' does not exist."
