"""This script run an experiment testing if demon works to CD for location."""
from cdlib import NodeClustering, algorithms, evaluation

import networkx as nx

NETWORK_PATH = '../networks/largest_mutual.gml'
# This const is used in demon algorithm to set the minimum community size. This
# value can be set using smallest community found in communities by location.
MIN_COM_SIZE = 11


def clustering_with_location(network):
    """Return a NodeClustering object with nodes grouped by location."""
    print('Clustering nodes using their location info...')
    communities = {}

    for vertex in network.nodes(data=True):
        loc = vertex[1]['location']
        try:
            communities[loc].append(vertex[0])
        except KeyError:
            communities[loc] = [vertex[0]]

    by_location_coms = NodeClustering(communities.values(), network,
                                      method_name='by_location',
                                      method_parameters=None, overlap=False)
    print('Done!\n')
    return by_location_coms


def get_size_min_community(node_clustering_obj):
    """Return a integer value with the size of the smallest community."""
    print('Obtaining the size of the smalles community...')
    min_com = len(node_clustering_obj.communities[0])

    for com in node_clustering_obj.communities:
        if len(com) < min_com:
            min_com = len(com)
    print(f'Done!\n The min size is {min_com}.\n')

    return min_com


def get_suitable_range(network, min_size):
    """Try to reduce the range used in search by communities using demon."""
    print('Obtaining the suitable range...')
    # x_epsilons = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    x_epsilons = [0.4, 0.5]
    y_sizes = []
    coms = []
    # 'evaluate' will be used as an alias for the method below
    # evaluate = evaluation.overlapping_normalized_mutual_information_LFK

    for epsilon in x_epsilons:
        print(f'\t--> testing epsilon={epsilon}')
        demon = algorithms.demon(network, min_size, epsilon)
        y_sizes.append(len(demon.communities))
        print("number of communities: ", len(demon.communities))
        coms.append(demon)

    # Check if there is any community detection with community number expected.
    founded_range = (None, None)
    expect_coms_size = 54

    if expect_coms_size in y_sizes:
        for i in range(y_sizes):
            if y_sizes[i] == expect_coms_size:
                if founded_range[0] is None:
                    founded_range = (x_epsilons[i], None)
                else:
                    founded_range[1] = (founded_range[0], x_epsilons)

    if founded_range[0] is not None and founded_range[1] is None:
        if founded_range[0] >= 1:
            founded_range = (founded_range[0] - 1, founded_range[0] + 1)
        elif founded_range[0] == 0:
            founded_range = (founded_range[0], founded_range[0] + 1)
        elif founded_range[0] == 1.0:
            founded_range = (founded_range[0] - 1, founded_range[0])
    print(f'Done!\n The range founded is {founded_range}.\n')

    return founded_range[0], founded_range[1]


def get_communities_in_suitable_range(lower_lim, upper_lim):
    """Get coms with demon and 10 values of epsilon in the given range."""
    print('Obtaining communities in the suitable range.')
    epsilon = lower_lim
    coms_founded = []
    while epsilon <= upper_lim:
        demon = algorithms.demon(g_network, min_com_size, epsilon)
        coms_founded.append(demon)
        epsilon = epsilon + 0.1
    print('Done!\n')

    return coms_founded


def eval_communities(coms_demon, loc):
    """Evaluate each community founded using the suitable range."""
    print('Evaluating communities founded...')
    evaluate = evaluation.overlapping_normalized_mutual_information_LFK
    evals = []

    for com in coms_demon:
        evals.append(evaluate(loc, com))
    print('Done!\n')

    return evals


if __name__ == '__main__':

    print('Reading network...')
    g_network = nx.read_gml(NETWORK_PATH, label=None)
    print('Done!\n')

    location = clustering_with_location(g_network)

    # Get the size of the smallest community from CD using location method.
    # This is necessary
    min_com_size = get_size_min_community(location)

    # Find the suitable in epsilon possible values [0,1]

    lower, upper = get_suitable_range(g_network, min_com_size)

    # Get communities for each value of epsilon in suitable_range

    coms_in_suitable_range = get_communities_in_suitable_range(lower, upper)

    # Evaluate communities for each value of epsilon in suitable_range
    evaluations = eval_communities(coms_in_suitable_range, location)

    print(evaluations)
