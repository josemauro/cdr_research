'''
In (Onella, 2007) an inspection of the network in one sample of the mutual 
network. This script apply this step to the social network of this work.

'''

import os
from igraph import Graph
from random import randint
from igraph import *
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

g_mutual = Graph()
g_mutual = g_mutual.Read_Ncol('g_mutual_undirected.ncol', weights=True, directed=True)

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


