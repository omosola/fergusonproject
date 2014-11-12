'''
"Usage: python testLoadGraph.py  <path to edge list file>"

Currently this program just prints out num nodes, num edges, and then plots
the degree distribution. Other stats should be added. 

NOTE: Devney ran this using Network/graph_files/unweighted_hashtag_cooccurance_graph.txt 

The file Data/cooccurancecounters_pickled/cooccurrence_strings.edges has duplicate lines, so I'm not sure
what's going on with that file. 
'''

import snap
import os
import sys
import matplotlib.pyplot as plt


def setUpPlot():
	fig = plt.figure()
	p = fig.add_subplot(2,1,1)
	p.set_yscale('log')
	p.set_xscale('log')
	p.set_xlabel('degree')
	p.set_ylabel('num nodes with degree')
	return p


if len(sys.argv) != 2:
	print "Usage: python testLoadGraph.py  <path to edge list file>"
else:
	filename = sys.argv[1]
	G = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)
	num_nodes = G.GetNodes()
	num_edges = G.GetEdges()
	print("Network contains " + str(num_nodes) + " nodes")
	print("Network contains " + str(num_edges) + " edges")

	#get degree distribution
	CntV = snap.TIntPrV()
	snap.GetOutDegCnt(G, CntV)
	degrees = []
	node_counts = []
	for p in CntV:
		degrees.append(p.GetVal1())
		node_counts.append(p.GetVal2())

	#plot degree dist
	p = setUpPlot()
	p.scatter (degrees, node_counts)
	plt.show()
