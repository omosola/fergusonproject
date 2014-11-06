"""
Usage:
python pickleTweets.py <path-to-tweet-csv-dir>

Behavior:
Reads all .csv files in the <path-to-tweet-csv-dir>,
converts the data in the file into tweet objects

Pickles the array of tweet objects and writes
the pickled data to a file in the same dir as the csv files

The files are named the same, but instead of .csv,
the corresponding pickle file has a .p extension
"""

import cPickle
import csv
import os
import sys

def pickleTweets(tweets_csv_filename, tweets_pickle_filename):
	print "pickling %s" % tweets_csv_filename

	f = open(tweets_csv_filename, 'rb')
	
	reader = csv.reader(f)
	
	headers = [] # array of strings
	tweets = [] # array of dicts (each representing a tweet)

	## Read tweets from csv file into tweet array of objects
	
	for row in reader:
		if len(headers) == 0:
			# first row, need to read in headers
			headers = row
			# first value for tweets represents the ID
			# but this is marked as an empty string in the data
			# - override the empty string
			headers[0] = "ID"
		else:
			tweet = {}
			for i, val in enumerate(row):
				header = headers[i]
				tweet[header] = val
				tweets.append(tweet)
				
	f.close()

        ## pickle the tweets array of objects
	tweets_pickle_file = open(tweets_pickle_filename, "w+b")	
	cPickle.dump(tweets, tweets_pickle_file)
	tweets_pickle_file.close()

if len(sys.argv) != 2:
	print "Usage: python pickleTweets.py <path-to-tweets-csv-dir>"
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
