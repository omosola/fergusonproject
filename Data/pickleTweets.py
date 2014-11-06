import cPickle, csv

tweetCsvFilename = "first10kTweets.csv"
tweetPickleFilename = "first10kTweets.p"

f = open(tweetCsvFilename, 'rb')

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
cPickle.dump( tweets, open(tweetPickleFilename, "wb"))
