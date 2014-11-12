import snap
import os
import sys





if len(sys.argv) != 2:
	print "Usage: python testLoadGraph.py  <path to edge list file>"
else:
	filename = sys.argv[1]
	G = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)
	num_nodes = G.GetNodes()
	num_edges = G.GetEdges()
	print("found " + str(num_nodes) + " nodes")
	print("found " + str(num_edges) + " edges")

	