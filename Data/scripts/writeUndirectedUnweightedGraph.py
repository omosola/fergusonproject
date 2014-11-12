import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np


def writeEdgesToFile(counter, f):
	for item in counter.items():
		pair = item[0]
		nodeId1 = pair[0] #hashtag id 1
		nodeId2 = pair[1] #hashtag id 2
		f.write(str(nodeId1) + "\t" + str(nodeId2) + "\n") #writes nodeId1	nodeId2 on each line


if len(sys.argv) != 3:
	print "Usage: python writeUndirectedUnweightedGraph.py  <co-occurance pickle path to read from> <graph text file to write to>"
else:
	cooccurance_pickle_path = sys.argv[1]
	graph_text_file = sys.argv[2]
	print("cooccurance_pickle_path: " + cooccurance_pickle_path)
	print("graph_text_file: " + graph_text_file)

	try:
		f = open(cooccurance_pickle_path, "rb") 
		cooccurance_counter = cPickle.load(f)
		f.close()
	except OSError:
		print "problem loading cooccurance_pickle_path pickle"

	try:
		graph_f = open(graph_text_file, 'w')
		writeEdgesToFile(cooccurance_counter, graph_f)
		graph_f.close()
		num_edges = len(cooccurance_counter.items())
		print("Expect " + str(num_edges) + " edges in graph in " + graph_text_file)
	except OSError:
		print "problem writing file"