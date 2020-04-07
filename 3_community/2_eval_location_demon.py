import networkx as nx

from cdlib import algorithms, evaluation
from cdlib import NodeClustering

NETWORK_PATH = '../networks/largest_mutual.gml'

def clustering_with_location(g_network):
    communities = {}

    for v in g_mutual.nodes(data=True):
        location = v[1]['location']
        try:
            communities[location].append(v[0])
        except KeyError:
            communities[location] = [v[0]]

    by_location_coms = NodeClustering(communities.values(), g_mutual,
                                      method_name='by_location',
                                      method_parameters=None, overlap=False)
    return by_location_coms

def clustering_with_demon(g_network):
    coms = algorithms.demon(g_mutual, min_com_size=3, epsilon=0.25)
    return demon_coms

g_mutual = nx.read_gml(NETWORK_PATH, label=None)

location = clustering_with_location(g_network)
demon = clustering_with_demon(g_network)

eval_obj = evaluation.overlapping_normalized_mutual_information_LFK(location,
                                                                    demon)
