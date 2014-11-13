import sys
import snap
import cPickle

if len(sys.argv) == 2:
    pickle_cooccurrence_filename = sys.argv[1]
else:
    print "Usage: python generate_cooccurrence_graph.py <relative-path-to-pickled-cooccurence-counter>"
    exit(0)

## load the pickled ID coccurrence counter
f = open(pickle_cooccurrence_filename, "rb")
counter = cPickle.load(f)
f.close()

## create a snap graph (directed multigraph)
## no option for undirected multigraph
## so we're using a directed multigraph
## to represent the multiple edges that go
## between nodes (multiple occurrences
## of co-occurrence
## Requires adding two edges per edge in counter
graph = snap.TNEANet.New()

## add the edges from the counter to the snap
## graph
for edge in counter.elements():
    id1, id2 = edge
    if not graph.IsNode(id1):
        graph.AddNode(id1)
    if not graph.IsNode(id2):
        graph.AddNode(id2)

    # add bidirectional edge
    # to indicate undirected nature
    # of the co-occurrence relationship
    graph.AddEdge(id1, id2)
    graph.AddEdge(id2, id1)

## Save graph to disk
# for the filename, replace the .p extension with .edges
edges_filename = pickle_cooccurrence_filename[:-2] + ".edges"
snap.SaveEdgeList(graph, edges_filename)
