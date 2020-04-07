import os

from igraph import Graph
from random import randint
from igraph import *

NETWORK_PATH = ''

def inspect_network():
    '''Apply the inspection (Onella, 2007) in one sample of the network.'''
    def get_color(v):
        color = ''
        if v<0.1:
            color = "orange"
        if v >= 0.1 and v<0.2:
            color = "yellow"
        if v>=0.2 and v<0.3:
            color = "green"
        if v>=0.3 and v<0.4:
            color = "cyan"
        if v>=0.4 and v<0.5:
            color = "blue"
        if v>=0.5 and v<0.6:
            color = "purple"
        if v>=0.6 and v<0.7:
            color = "pink"
        if v>=0.7:
            color = "red" 
        return color

    '''
    Since this 
    '''
    #out_dir = './2_inspecting_sample_out'
    #num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(name)])

    num_nodes = g_mutual.vcount()

    random_node = randint(0, num_nodes-1)

    #topological distance
    l = 5

    neighboors = g_mutual.neighborhood(vertices=random_node, order=l)
    g = g_mutual.induced_subgraph(neighboors, implementation="create_from_scratch")

    es = g_mutual.es["weight"]

    max_weight = max(es)

    for e in g.es:
        e["color"] = get_color(float(e["weight"])/float(max_weight))

    g.vs["color"] = "red"

    g.vs[0]['color'] = "blue"

    layout = g.layout('circle')

    plot(g, layout = layout)

def basic_metrics(g):
    max_degree = g.maxdegree(vertices=g.vs, loops=False)
    min_degree = min(g.degree(g.vs, loops=False))

    print('Vertices: ', g.vcount())
    print('Edges: ', g.ecount())
    print('Max degree: ', max_degree)
    print('Min degree: ', min_degree)
    print('Max weight:', max(g.es['weight']))
    print('Min weight:', min(g.es['weight']))

def weight_distribution(weights, prefix):
    # x is a list that contains all degrees existing in the graph
    x = list(set(weights))

    #y will have how many times a specific degree (in x) are repeated
    y = []

    for i in x:
        y.append(weights.count(i))

    max_y = max(y)
    y_fraction = [float(i)/float(max_y) for i in y]

    # Plot
    plt.scatter(x, y, alpha=0.5)
    plt.title('Weights distribuition')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(prefix+'scatter_plot.png')
    plt.clf()

    # Plot log log
    w = 4
    h = 3
    d = 300
    plt.figure(figsize=(w, h), dpi=d)
    plt.loglog(x, y)
    plt.title('Weights distribuition')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(prefix+'loglog_plot.png')
    plt.clf()

    # Plot CCDF

    weights_freq = zip(x,y)
    weights_freq = sorted(weights_freq, key=operator.itemgetter(0))
    y_ccdf = []
    x_ccdf = []

    total_nodes = g.vcount()

    cumulative = 0
    for i in weights_freq:
        x_ccdf.append(i[0])
        cumulative = i[1]/float(total_nodes) + cumulative
        y_ccdf.append( (1 - cumulative))


    plt.scatter(x_ccdf, y_ccdf, alpha=0.5, marker='x')
    plt.title('CCWF')
    plt.xlabel('Grau k')
    plt.ylabel('P[W=k]')
    plt.savefig('ccdf_plot.png')
    plt.scatter(x, y, alpha=0.5)

def degree_distribution(degrees, prefix, total_nodes):
    '''This function plot the degree distribuitions.'''
    # x is a list that contains all degrees existing in the graph
    max_x = max(degrees)
    x_degree = list(range(0, max_x + 1)) # '+ 1' is used to include max_x

    #y is a list that contains all frequency for each degree (in x)
    y_freq = [degrees.count(i) for i in x_degree]

    '''
    # Scatter Plot
    plt.scatter(x_degree, y_freq, alpha=0.5)
    plt.title('Degree distribuition')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(prefix+'degree_scatter_plot.png')
    plt.clf()
    print('Scatter plot done!')
    '''
    # Plot CCDF
    y_ccdf = []
    x_ccdf = x_degree

    accumulated = 0
    for i in y_freq:
        accumulated = i/float(total_nodes) + accumulated
        y_ccdf.append((1 - accumulated))


    plt.scatter(x_ccdf, y_ccdf, alpha=0.5, marker='x')
    plt.title('CCDF')
    plt.xlabel('Grau k')
    plt.ylabel('P[D=k]')
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.savefig(f'{prefix}degree_ccdf_plot.png')
    print(f'{prefix}CCDF plot done!')

def count_num_calls(g, e_1):
    x_num = 0
    y_duration = 0
    
    for e_2 in g.es:
        if (e_1.tuple == e_2.tuple):
            x_num = x_num + 1
            y_duration = y_duration + e_2['weight']
    
    return x_num, y_duration

def plot_scatter_dur_num(x, y)
    # Plot
    plt.scatter(x, y, alpha=0.5)
    plt.title('Scatter plot of call duration and number of calls')
    plt.xlabel('number calls')
    plt.ylabel('duration calls')
    plt.savefig(prefix+'num_duration_scatter_plot.png')
    plt.clf()
    
g_mutual = Graph()
g_mutual = g_mutual.Read_Ncol(NETWORK_PATH, weights=True, directed=True)



