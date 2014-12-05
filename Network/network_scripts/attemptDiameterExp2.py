import snap
import random
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import cPickle
import os
import sys
import time
from collections import Counter
import numpy as np
import re
import operator

Y = 2

X_denom = 100

def setUpPlot(Y, X_denom):
	fig = plt.figure()
	p = fig.add_subplot(2,1,1)
	p.set_xlabel('percentage of graph removed, Y = ' + str(Y) + " X_denom = " + str(X_denom))
	p.set_ylabel('diameter')
	return p

def plotLine(p, x, y,  clr, name):
	p.plot(x, y, color=clr, label=name)

def RemoveHighFreqNodes(G_temp, idSortedByFreq, num_nodes_to_remove):
	print("need to implement Remove High Freq Nodes")

#takes in id to freq map, returns arr of ids in descending order of freq
def SortIdsByFreq(freqMap):
	sorted_id_freq_tuples = sorted(freqMap.items(), key=operator.itemgetter(1))
	print sorted_id_freq_tuples
	sorted_freqs = [id_freq_tuple[0] for id_freq_tuple in sorted_id_freq_tuples]
	sorted_freqs.reverse()
	print sorted_freqs
	#you need to check this by loading in the string-id map and printing the most freq hashtags. 


#takes in an array of ids sorted by frequency in descending order
def runStats(filePrefix, p,  clr1, clr2, sorted_ids):
	
	remaining_ids = sorted_ids
	fileName = filePrefix + ".txt"
	
	G = snap.LoadEdgeList(snap.PUNGraph, fileName, 0, 1)
	num_nodes = G.GetNodes()

	#sanity check
	num_edges = (G.GetEdges())
	print("num edges: " + str(num_edges))
	print("num nodes: " + str(num_nodes))

	min_size = Y * .01 * num_nodes
	curr_size = num_nodes
	num_nodes_to_remove= int(math.floor(num_nodes/float(X_denom)))

	percentages = []
	diameters = []

	G_temp = G

	#attack
	G_temp = G
	curr_size = G_temp.GetNodes()
	while(curr_size >= min_size):
		ids_to_remove = remaining_ids[0:num_nodes_to_remove]
		remaining_ids = remaining_ids[num_nodes_to_remove:] #the rest of the ids
		V_to_remove = snap.TIntV()
		for i in range(len(ids_to_remove)):
    		V_to_remove.Add(ids_to_remove[i])
		snap.DelNodes(G_temp, V_to_remove)
		diameter = snap.GetBfsFullDiam(G_temp, 100, False)
		diameters.append(diameter)
		curr_size = G_temp.GetNodes()
	plotLine(p, percentages, attack_diameters, clr2, filePrefix)



#test pickling of freq
if len(sys.argv) != 3:
	print "Usage: python attemptDiameterExp2.py <graph_path> <hashtag_frequency_ID_pickle_path>"
else:
	graph_path = sys.argv[1]
	hashtag_ID_frequency_pickle_path = sys.argv[2]
	print("graph_path: " +graph_path)
	print("hashtag_ID_frequency_pickle_path : " + hashtag_ID_frequency_pickle_path)

	try:
		f = open(hashtag_ID_frequency_pickle_path, "rb") 
		hashtagIdFreqMap = cPickle.load(f)
		sorted_ids = SortIdsByFreq(hashtagIdFreqMap)
		f.close()
	except OSError:
		print "problem loading hashtag_ID_frequency_pickle"
	

pickle_file_name = hashtag_frequency_pickle_path
f = open(pickle_file_name, "w + b")
cPickle.dump(freqCounter, f)
f.close()

p = setUpPlot(Y, X_denom)
runStats("testgraph", p, 'blue', 'red')


fontP = FontProperties()
fontP.set_size('xx-small')
plt.legend(loc='upper right', prop=fontP)
plt.show()


