import networkx as nx

from cdlib import algorithms, evaluation
from cdlib import NodeClustering

NETWORK_PATH = '../networks/largest_mutual.gml'
# This const is used in demon algorithm to set the minimum community size. This
# value can be set using smallest community found in communities by location.
MIN_COM_SIZE = 11

def clustering_with_location(g_network):
    """Return a NodeClustering object with nodes grouped by location."""
    print('Clustering nodes using their location info...')
    communities = {}

    for v in g_network.nodes(data=True):
        location = v[1]['location']
        try:
            communities[location].append(v[0])
        except KeyError:
            communities[location] = [v[0]]

    by_location_coms = NodeClustering(communities.values(), g_network,
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

def get_suitable_range(g_network, min_com_size):
    """Try to reduce the range used in search by communities using demon."""
    print('Obtaining the suitable range...')
    x_epsilons = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    y_sizes = []
    coms = []
    # 'evaluate' will be used as an alias for the method below
    evaluate = evaluation.overlapping_normalized_mutual_information_LFK

    for epsilon in x_epsilons:
        print(f'\t--> testing epsilon={epsilon}')
        demon = algorithms.demon(g_network, min_com_size, epsilon)
        y_sizes.append(len(demon.communities))
        coms.append(demon)

    # Check if there is any community detection with community number expected.
    expected_number_found = False
    founded_range = (None, None)

    if expect_coms_size in y_sizes:
        for i in range(y_sizes):
            if y_sizes[i] == expect_coms_size:
                if founded_range[0] == None:
                    founded_range = (x_epsilons[i], None)
                else:
                    founded_range[1] = (founded_range[0], x_epsilons)

    if founded_range[0]!=None and founded_range[1] == None:
        if founded_range[0] >= 1:
            founded_range = (founded_range[0] - 1, founded_range[0] + 1)
        elif founded_range[0] == 0:
            founded_range = (founded_range[0], founded_range[0] + 1)
        elif founded_range[0] == 1.0:
            founded_range = (founded_range[0] - 1, founded_range[0])
    print(f'Done!\n The range founded is {founded_range}.\n')

    return founded_range[0], founded_range[1]

def get_communities_in_suitable_range(lower, upper):
    """Get coms with demon and 10 values of epsilon in the given range."""
    print(f'Obtaining communities in the suitable range.')
    epsilon = lower
    coms_in_suitable_range
    while(epsilon <= upper):
        demon = algorithms.demon(g_network, min_com_size, epsilon)
        coms_in_suitable_range.append(demon)
        epsilon = epsilon + 0.1
    print('Done!\n')

    return coms_in_suitable_range

def eval_communities(coms_in_suitable_range):
    """Evaluate each community founded using the suitable range."""
    print('Evaluating communities founded...')
    evaluate = evaluation.overlapping_normalized_mutual_information_LFK
    evaluations = []

    for coms in coms_in_suitable_range:
        evalutions.append(evaluate(location, demon))
    print('Done!\n')

    return evaluations


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
evaluations = eval_communities(coms_in_suitable_range)

print(evaluations)

