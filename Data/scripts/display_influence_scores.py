#@author: Kelsey
#path: /Data/scripts/display_influence_scores.py
import snap
import cPickle
import random
import sys
from collections import Counter
import numpy
#cutoff for number of rows we will write to csv file.
CUTOFF = 50000

def loadData():

	influencescore_filename = sys.argv[2]
	try:
		id2_influencescore_data = cPickle.load(open(influencescore_filename, "rb") )
	except Exception as e:
		return e
	else:
		return id2_influencescore_data


def generate_new_file(version,fileIndex):
	filename = "influencescoreV %s-%d.csv" % (version,fileIndex)
	csv_file = open(filename, "w+b")
	return csv_file

def writeToCSV(id2_influencescore_dict, id2TagDict):
	version = sys.argv[2]
	fileIndex = 1
	filename = "influencescoreV %s.csv" % (version)
	csv_file = open(filename,"w+b")
	csv_file.write("NID1, Hashtag1, NID2, Hashtag2, Influence_score\n")
	counter = 1

	for key, val in id2_influencescore_dict.iteritems():
		if counter == CUTOFF:
			csv_file.close()
			csv_file = generate_new_file(version,fileIndex)
			fileIndex += 1
			counter = 1
		print type(key)
		print type(val)
		if key == 0:
			continue		
		influenceScore = numpy.mean(val)

		if type(key) is tuple:		
			print "The key is ",key," the tag is: ", id2TagDict[key[0]] , id2TagDict[key[1]]
			print "With value ",influenceScore
			csv_file.write(" %d, %s, %d, %s, %f\n" % (key[0], id2TagDict[key[0]], key[1], id2TagDict[key[1]], influenceScore) )
		else:
			print "The key is ",key," the tag is: ", id2TagDict[key]
			print "With value ",influenceScore 
			csv_file.write(" %d, %s, %s, %s, %f\n" % (key, id2TagDict[key], "", "", influenceScore) )
		counter += 1

	csv_file.close()


def run():
	if len(sys.argv) != 3:
		print "Usage python ./scripts/display_influence_scores.p ./hashtag-id-maps/id2_influence.p [version]"
	else:

		influencescore_filename = sys.argv[1]
		try:
			id2_influencescore_dict = cPickle.load(open(influencescore_filename, "rb") )
			#print id2_influencescore_dict
			#for key, val in id2_influencescore_dict:
		#		print "Key: "+key+" Influence_score: "+val
		except Exception as e:
			print e
			return e

		try:
			id2TagDict = cPickle.load(open("./hashtag-id-maps/id2tag.p","rb"))
		except Exception as e:
			print "Theres an exception"
			return e

		writeToCSV(id2_influencescore_dict, id2TagDict)

if __name__ == "__main__":
    run()

