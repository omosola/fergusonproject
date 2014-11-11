import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np


def pickleDicts(tagDict, dict_pickle_filename):
        ## pickle the tweets array of objects
	dict_pickle_file = open(dict_pickle_filename, "w+b")

	cPickle.dump(tagDict, dict_pickle_file)

	dict_pickle_file.close()

def populateDicts(hashtags,id2Tag_pickle_filename, tag2ID_pickle_filename):
	f = open(hashtags, 'rb')
	
	id2TagDict = {}
	tag2IDDict = {}

	## The indexKey is supposed to help with the offset of NodeId's.
	# On each new iteration of row in f... the value of i in enumerate row gets reset to 0.
	# The indexKey is supposed to track current Node ID as each row changes.
	
	indexKey = 0
	for row in f:
		
		for i, val in enumerate(row):
			if not id2TagDict.has_key(i):
				id2TagDict[i + indexKey] = val

			if not tag2IDDict.has_key(val):
				tag2IDDict[val] = i + indexKey
			indexKey += 1
	f.close()

	pickleDicts(id2TagDict,id2Tag_pickle_filename)
	pickleDicts(tag2IDDict, tag2ID_pickle_filename)
print len(sys.argv)
print sys.argv[1], sys.argv[2], sys.argv[3]
if len(sys.argv) != 4:
	print "Usage: python genPickleDicts.py <path-to-hashtags-txt-dir>"
else:
	populateDicts(sys.argv[1],sys.argv[2],sys.argv[3])