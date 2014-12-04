import snap
import cPickle
import random

TIMESTEP_SEQUENCE = 10000

INCREASING_ORDER = 0
DECREASING_ORDER = 1
RANDOM_ORDER = 2

# increasing order of co-occurrence
# decreasing order
# random order

def get_cooccurrence_freq_map(filename):
    return cPickle.load(open(filename, "rb"))

def run_experiment(graph_filename, order):
    cooccurrence_pickle_filename = "cooccurance_counters_pickled/id_cooccurance_counter.p"
    cooccurrence_freq_map = get_cooccurrence_freq_map(cooccurrence_pickle_filename)

    # returns a list of the edges in decreasing order of their frequency
    decreasing_order_edges = [ (edge, frequency) for edge, frequency in cooccurrence_freq_map.most_common() ]

    # load fresh Graph
    Graph = snap.LoadEdgeList(snap.PNEANet, graph_filename, 0, 1)
    
    if order == INCREASING_ORDER:
        # reverse the decreasing_order_egdes
        increasing_order_edges = decreasing_order_edges
        increasing_order_edges.reverse()
        run_edge_deletion_with_stats(Graph, increasing_order_edges)
    elif order == DECREASING_ORDER:
        # maintain the decreasing order of the cooccurrence_freq_map
        run_edge_deletion_with_stats(Graph, decreasing_order_edges)        
    elif order == RANDOM_ORDER:
        # randomly permute the decreasing_order_edges list
        random_order_edges = random.sample(decreasing_order_edges, len(decreasing_order_edges))
        run_edge_deletion_with_stats(Graph, random_order_edges)
        
def run_edge_deletion_with_stats(Graph, edge_ordering):
    stats_per_timestep = []

    numDeletedEdges = 0
    for edge, edge_weight in edge_ordering:
        nodeId1, nodeId2 = edge        
        
        # delete one bidirectional edge
        Graph.DelEdge(nodeId1, nodeId2)
        Graph.DelEdge(nodeId2, nodeId1)
        
        numDeletedEdges += 1
        if numDeletedEdges % TIMESTEP_SEQUENCE == 0:
            stats_per_timestep += [calculate_stats(Graph)]

    print stats_per_timestep

def calculate_stats(Graph):
    print "calculating stats"
    diameter = snap.GetBfsFullDiam(Graph, 20, False)
    stats = (diameter)
    return [stats]

def run():
    graph_filename = "cooccurance_counters_pickled/id_cooccurance_counter.edges"

    # increasing order of co-occurrence
    run_experiment(graph_filename, order = INCREASING_ORDER)

    # decreasing order of co-occurrence
    run_experiment(graph_filename, order = DECREASING_ORDER)

    # random ordering of co-occurrence
    run_experiment(graph_filename, order = RANDOM_ORDER)
    
if __name__ == "__main__":
    run()



