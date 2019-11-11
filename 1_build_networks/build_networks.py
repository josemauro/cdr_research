"""This script create one social network from files in "./data" folder and save
this network in ncol file format called "graph.ncol".
"""

import csv
from igraph import Graph


files_list = []

for file_name in ios.listdir("./data"):
    if file_name.endswith(".out"):
        files_list.append(file_name)

ncol_out_file = open("graph.ncol","w")

for file_name in files_list:
    dir_name = "./data/" + file_name
    with open(dir_name, 'r') as csvfile:
        csv_read = csv.reader(csvfile, delimiter=';')
        #add nodes
        name_list = []
        for row in csv_read:
            line = row[4] + " " + row[6] + " " + row[2] + "\n" 
            ncol_out_file.write(line)

ncol_out_file.close()

"""
In (Onella, 2007) paper there are 2 types of network:

    -Non-mutual: connected 2 users with an undirected link if there had been 
     at least one phone call between. (A called B OR B called A)

    -Mutual: connected 2 users with an undirected link if there had been at 
    least one reciprocated pair of phone calls between them.
    (A called B AND B called A)

The social network created above (graph.ncol) in this script can be read in one
of this two formats.
"""


# Code to read ncol file as non-mutual network:
'''
g_nonmutual = Graph()
g_nonmutual.Read_Ncol("graph.ncol", weights=True, directed=True)

# Remove arrows from each edge.
g_nonmutual.to_undirected(mode="each")

# Simplifies a graph by removing self-loops and/or multiple edges. 
g_nonmutual = g_nonmutual.simplify(multiple=True, loops=True, combine_edges="sum")


'''


# Code to read ncol file as mutual network:

'''
g_mutual = Graph()
g_mutual = g_mutual.Read_Ncol("graph.ncol", names=True, weights=True, directed=True)

edges_2delete = []

for e in g_mutual.es:
    if g_mutual.get_eid(e.target, e.source, directed=True, error=False) == -1:
        edges_2delete.append(e)

g_mutual.delete_edges(edges_2delete)

# Remove arrows from each edge.
g_mutual.to_undirected(mode="each")

# Simplifies a graph by removing self-loops and/or multiple edges. 
g_mutual = g_mutual.simplify(multiple=True, loops=True, combine_edges="sum")

'''

'''
https://igraph.org/python/doc/igraph.GraphBase-class.html

'''

