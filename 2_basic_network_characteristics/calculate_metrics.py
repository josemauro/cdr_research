#This script calulate the basic metrics to a graph in .ncol format

import sys
from igraph import Graph
import numpy as np
import matplotlib.pyplot as plt
import operator

#Open the graph

g = Graph()
g = g.Read_Ncol(sys.argv[1])

# Degree distribuition

# degrees is list that contains a degree for each node in the graph
degrees = g.vs.degree()

# x is a list that contains all degrees existing in the graph
x = list(set(degrees))

#y will have how many times a specific degree (in x) are repeated
y = []

for i in x:
    y.append(degrees.count(i))

max_y = max(y)
y_fraction = [i/float(max_y) for i in y]

# Plot
plt.scatter(x, y, alpha=0.5)
plt.title('Degree distribuition')
plt.xlabel('k')
plt.ylabel('P(k)')
plt.savefig('scatter_plot.png')
plt.clf()

# Plot log log
w = 4
h = 3
d = 300
plt.figure(figsize=(w, h), dpi=d)
plt.loglog(x, y)
plt.title('Degree distribuition')
plt.xlabel('k')
plt.ylabel('P(k)')
plt.savefig('loglog_plot.png')
plt.clf()

# Plot CCDF

degrees_freq = zip(x,y)
dgrees_freq = sorted(degrees_freq, key=operator.itemgetter(0))
y_ccdf = []
x_ccdf = []

total_nodes = g.vcount()

cumulative = 0
for i in degrees_freq:
    x_ccdf.append(i[0])
    cumulative = i[1]/float(total_nodes) + cumulative
    y_ccdf.append( (1 - cumulative))


plt.scatter(x_ccdf, y_ccdf, alpha=0.5, marker='x')
plt.title('CCDF')
plt.xlabel('Grau k')
plt.ylabel('P[D=k]')
plt.savefig('ccdf_plot.png')
plt.scatter(x, y, alpha=0.5)
