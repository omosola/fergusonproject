'''
run_edge_removal_PUNGraph.py takes a 'version' as 1st arg, timestep_sequence as second arg. The version 
is just a string that will differentiate results files. timestep_sequence is the number of edges removed between
measurements. Has default value of 50000 but will get overwritten with user input.

Outputs 3 results files. For increasing, decreasing, and random edge removal, writes a csv with 4 columns:
'timestep' is actually useless because it always has the last timestep, but the other
columns are in order of increasing timesteps. 'diameter' is the diameter measurement, num_sccs is the number
of sccs (which are also wccs in undirected graph), and max_scc_size is size of max scc as fraction of current graph. 

'''

import snap
import cPickle
import random
import sys
from collections import Counter
import numpy
timestep_sequence = 50000
version = "unknown"

INCREASING_ORDER = 0
DECREASING_ORDER = 1
RANDOM_ORDER = 2

sample_top_influence_scores = 3
sample_lowest_influence_scores = 4
sample_random_influence_scores = 5
# increasing order of co-occurrence
# decreasing order
# random order

def get_hashtag_freq_counter(filename):
    return cPickle.load(open(filename, "rb"))

def add_isolated_nodes_to_graph(Graph , hashtag_freq_counter):
    for node, frequency in hashtag_freq_counter.most_common():
        if not Graph.IsNode(node):
            Graph.AddNode(node)

    return Graph

def run_experiment(influencescore_dict,graph_filename, order, output_filename):


    hashtag_frequency_pickle_filename = "./hashtag_frequency_counters_pickled/hashtag_freq_counter.p"

    hashtag_freq_counter = get_hashtag_freq_counter(hashtag_frequency_pickle_filename)

    # returns a list of the edges in decreasing order of their frequency
    decreasing_order_hashtags = [ (node, frequency) for node, frequency in hashtag_freq_counter.most_common() ]
    # load fresh Graph
    #Graph = snap.LoadEdgeList(snap.PNEANet, graph_filename, 0, 1)
    Graph = snap.LoadEdgeList(snap.PUNGraph, graph_filename, 0, 1)

    #Graph = add_isolated_nodes_to_graph(Graph, hashtag_freq_counter)

    nodes_deleted_at_each_timestep = Graph.GetNodes()  / timestep_sequence

    print("Expect " + str(Graph.GetNodes()/timestep_sequence) + " timesteps")
    if order == INCREASING_ORDER:
        # reverse the decreasing_order_egdes
        increasing_order_hashtags = decreasing_order_hashtags
        increasing_order_hashtags.reverse()
        run_node_deletion_with_stats(influencescore_dict,Graph, nodes_deleted_at_each_timestep, increasing_order_hashtags, output_filename, order = INCREASING_ORDER)
    elif order == DECREASING_ORDER:
        # maintain the decreasing order of the cooccurrence_freq_map
        run_node_deletion_with_stats(influencescore_dict,Graph,nodes_deleted_at_each_timestep, decreasing_order_hashtags, output_filename, order = DECREASING_ORDER)        
    elif order == RANDOM_ORDER:
        # randomly permute the decreasing_order_edges list
        random_order_hashtags = random.sample(decreasing_order_hashtags, len(decreasing_order_hashtags))
        run_node_deletion_with_stats(influencescore_dict,Graph, nodes_deleted_at_each_timestep, random_order_hashtags, output_filename,order)
        
def write_stats_to_file(output_filename, stats_per_timestep, timestep):
    f = open(output_filename, "w+") # + <- indicates file
                                    # should be created if
                                    # it doesn't already exist
    
    f.write("timestep, diameter, num_sccs, max_scc_size, nodeID, hashtag,influence_score\n")
    for stat in stats_per_timestep:
        #f.write("%d %s\n" % (timestep, stat))
        print stat[0][4]
        f.write("%d, %d, %d, %f,%d,%s,%f\n" %(timestep, stat[0][0], stat[0][1], stat[0][2],stat[0][3],stat[0][4],stat[0][5]))
        #print("%d, %d, %d, %f" % (timestep, stat[0][0], stat[0][1], stat[0][2]))
    f.close()

def run_node_deletion_with_stats(influencescore_dict,Graph, nodes_deleted_at_each_timestep, node_ordering, output_filename, order):
    stats_per_timestep = []
    timestep = 0
    k = 10
    ## print initial values for the graph
    #print timestep, calculate_stats(Graph)
    randInt = numpy.random.randint(0,500)
    num_deleted_nodes = 0
    if order == DECREASING_ORDER:
        repList = [0 , 0]
    elif order == INCREASING_ORDER:
        repList = [0, 1000000]
    elif order == RANDOM_ORDER:
        repList = [0 , randInt]
    for node, node_weight in node_ordering:
        #nodeId1, nodeId2 = edge
        if order == DECREASING_ORDER:
            if node_weight > repList[1]:
                repList[0] = node
                repList[1] = node_weight
        elif order == INCREASING_ORDER:
            if node_weight < repList[1]:
                repList[0] = node
                repList[1] = node_weight
        else:
            if node_weight >= repList[1]:
                repList[0] = node
                repList[1] = node_weight
        # delete one bidirectional edge
        if Graph.IsNode(node):
            Graph.DelNode(node)
        #Graph.DelEdge(nodeId2, nodeId1)
        #print "The size of the graph is now", Graph.GetNodes()
        num_deleted_nodes += 1
        if num_deleted_nodes % nodes_deleted_at_each_timestep == 0:

            timestep += 1
               
            timestep_stats = calculate_stats(influencescore_dict,Graph,repList[0])
            #print timestep, timestep_stats, num_deleted_edges
            stats_per_timestep += [timestep_stats]
            repList = [0 , 0]


    write_stats_to_file(output_filename, stats_per_timestep, timestep)
    

def calculate_stats(influencescore_dict,Graph,repNode):
    # diameter
    diameter = snap.GetBfsFullDiam(Graph, 100, False)
    

    # number of connected components
    Sccs = snap.TCnComV()
    snap.GetSccs(Graph, Sccs)
    num_sccs = Sccs.Len()

    # size of largest connected component
    max_scc_size = snap.GetMxSccSz(Graph)

    tagName = id2Tag[repNode]

    #influenceScore of repNode
    influenceScore = numpy.mean(influencescore_dict[repNode])
    # package up stats and return
    stats = [diameter, num_sccs, max_scc_size, repNode, tagName, influenceScore ]
    return [stats]

def processArgs():
    global version #string arg to differentiate result files. 
    global timestep_sequence
    myArgs = sys.argv;
    if(len(myArgs) == 3):
        version = myArgs[1]
        timestep_sequence = int(myArgs[2])
        
    else:
        print("WARNING: using defaults.\nusage: python node_removal_experiment.py [version] [timestep_sequence]")
    print("version: " +  version)
    print("timestep_sequence: " + str(timestep_sequence))

def run():
    #graph_filename = "cooccurance_counters_pickled/id_cooccurance_counter.edges"
    graph_filename = "../Network/graph_files/unweighted_hashtag_cooccurance_graph.txt"
    processArgs()

    output_file_prefix = "results/node_"
    output_file_suffix = "V" + version + ".csv"

    influencescore_dict = cPickle.load(open("./hashtag-id-maps/id2_influence.p","rb") )



    # increasing order of co-occurrence
    print "running experiment with increasing order"
    run_experiment(influencescore_dict, graph_filename, order = INCREASING_ORDER,  output_filename=(output_file_prefix + "increasing_experiment" + output_file_suffix))

    # decreasing order of co-occurrence
    print "running experiment with decreasing order"
    run_experiment(influencescore_dict,graph_filename, order = DECREASING_ORDER, output_filename=(output_file_prefix + "decreasing_experiment" + output_file_suffix))

    # random ordering of co-occurrence
    print "running experiment with random order"
    run_experiment(influencescore_dict,graph_filename, order = RANDOM_ORDER, output_filename=(output_file_prefix + "random_experiment" + output_file_suffix))

id2Tag = cPickle.load(open('./hashtag-id-maps/id2Tag.p',"rb") )
if __name__ == "__main__":
    run()



