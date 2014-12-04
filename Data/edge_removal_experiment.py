import snap
import cPickle
import random

TIMESTEP_SEQUENCE = 500000

INCREASING_ORDER = 0
DECREASING_ORDER = 1
RANDOM_ORDER = 2

# increasing order of co-occurrence
# decreasing order
# random order

def get_cooccurrence_freq_map(filename):
    return cPickle.load(open(filename, "rb"))

def run_experiment(graph_filename, order, output_filename):
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
        run_edge_deletion_with_stats(Graph, increasing_order_edges, output_filename)
    elif order == DECREASING_ORDER:
        # maintain the decreasing order of the cooccurrence_freq_map
        run_edge_deletion_with_stats(Graph, decreasing_order_edges, output_filename)        
    elif order == RANDOM_ORDER:
        # randomly permute the decreasing_order_edges list
        random_order_edges = random.sample(decreasing_order_edges, len(decreasing_order_edges))
        run_edge_deletion_with_stats(Graph, random_order_edges, output_filename)
        
def run_edge_deletion_with_stats(Graph, edge_ordering, output_filenam):
    stats_per_timestep = []
    timestep = 0

    ## print initial values for the graph
    print timestep, calculate_stats(Graph)

    num_deleted_edges = 0
    for edge, edge_weight in edge_ordering:
        nodeId1, nodeId2 = edge        
        
        # delete one bidirectional edge
        Graph.DelEdge(nodeId1, nodeId2)
        Graph.DelEdge(nodeId2, nodeId1)
        
        num_deleted_edges += 1
        if num_deleted_edges % TIMESTEP_SEQUENCE == 0:
            timestep += 1
            timestep_stats = calculate_stats(Graph)
            print timestep, timestep_stats
            stats_per_timestep += [timestep_stats]

    # write stats to the output file
    f = open(output_filename, "w+") # + <- indicates file
                                    # should be created if
                                    # it doesn't already exist
    f.write("TIMESTEP STAISTICS\n")
    for stat in stats_per_timestep:
        f.write("%d %s\n" % (timestep, stat))
    f.close()
    

def calculate_stats(Graph):
    # diameter
    diameter = snap.GetBfsFullDiam(Graph, 100, False)

    # number of connected components
    Sccs = snap.TCnComV()
    snap.GetSccs(Graph, Sccs)
    num_sccs = Sccs.Len()

    # size of largest connected component
    max_scc_size = snap.GetMxSccSz(Graph)

    # package up stats and return
    stats = [diameter, num_sccs, max_scc_size]
    return [stats]

def run():
    graph_filename = "cooccurance_counters_pickled/id_cooccurance_counter.edges"

    # increasing order of co-occurrence
    print "running experiment with increasing order"
    run_experiment(graph_filename, order = INCREASING_ORDER, output_filename = "edge_increasing_experiment.csv")

    # decreasing order of co-occurrence
    print "running experiment with decreasing order"
    run_experiment(graph_filename, order = DECREASING_ORDER, output_filename = "edge_decreasing_experiment.csv")

    # random ordering of co-occurrence
    print "running experiment with random order"
    run_experiment(graph_filename, order = RANDOM_ORDER, output_filename = "edge_random_experiment.csv")
    
if __name__ == "__main__":
    run()



