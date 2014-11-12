''''
 "Usage: python testTagIdAndCooccurPickling.py <id2tag_pickle_file_path> <tag2id_pickle_file_path >  <co-occurance-string-pickle-path > <cooccurance_id_pickle_path"

For testing purposes, makes sure that id-tag association is consistant, relying on the co-occurance counters. 

'''


import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import re

numStrPasses = 0
numIdPasses = 0

def assertStrEquivId(string_item):
	string_tuple = string_item[0]
	str_count = string_item[1]
	str1 = string_tuple[0]
	str2 = string_tuple[1]
	id1 = tag2id_map[str1]
	id2 = tag2id_map[str2]
	id_count = id_cooccur_counter[(id1, id2)]
	if(str_count != id_count):
		print("failure for string co_occur count to match id count")
		print(string_item)
	else:
		global numStrPasses 
		numStrPasses += 1


def assertIdEquivStr(id_item):
	id_tuple = id_item[0]
	id_count = id_item[1]
	id1 = id_tuple[0]
	id2 = id_tuple[1]

	str1 = id2tag_map[id1]
	str2 = id2tag_map[id2]
	str_count = string_cooccur_counter[(str1, str2)]
	if(str_count != id_count):
		print("failure for id co_occur to match string count")
		print(id_item)
	else:
		global numIdPasses
		numIdPasses += 1


if len(sys.argv) != 5:
	print "Usage: python testTagIdAndCooccurPickling.py <id2tag_pickle_file_path> <tag2id_pickle_file_path >  <co-occurance-string-pickle-path > <cooccurance_id_pickle_path"
else:
	id2tag_pickle_file_path = sys.argv[1]
	tag2id_pickle_file_path = sys.argv[2]
	cooccurance_string_pickle_path = sys.argv[3]
	cooccurance_id_pickle_path = sys.argv[4]
	try:
		f = open(id2tag_pickle_file_path, "rb") 
		id2tag_map = cPickle.load(f)
		f.close()
	except OSError:
		print "problem loading id2tag_pickle_file_path "

	try:
		f = open(tag2id_pickle_file_path, "rb") 
		tag2id_map = cPickle.load(f)
		f.close()
	except OSError:
		print "problem loading tag2id pickle"
	try:
		f = open(cooccurance_string_pickle_path, "rb") 
		string_cooccur_counter = cPickle.load(f)
		f.close()
	except OSError:
		print "problem loading cooccurance_string_pickle_path "
	try:
		f = open(cooccurance_id_pickle_path, "rb") 
		id_cooccur_counter = cPickle.load(f)
		f.close()
	except OSError:
		print "problem loading cooccurance_id_pickle_path "

	for item in string_cooccur_counter.items():
		assertStrEquivId(item)
	for item in id_cooccur_counter.items():
		assertIdEquivStr(item)

	print("the following four numbers should be the same, and greater than 0:")
	print (str(len(string_cooccur_counter.items())) + " items in str cooccur counter")
	print (str(len(id_cooccur_counter.items()))+ " items in id cooccur counter")
	print (str(numIdPasses) + " id passes")
	print (str(numStrPasses) + " string passes")


