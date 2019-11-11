import sys

from igraph import Graph
def basic_metrics(g):
    max_degree = g.maxdegree(vertices=g.vs, loops=False)
    min_degree = min(g.degree(g.vs, loops=False))

    print('Vertices: ', g.vcount())
    print('Edges: ', g.ecount())
    print('Max degree: ', max_degree)
    print('Min degree: ', min_degree)
    print('Max weight:', max(g.es['weight']))
    print('Min weight:', min(g.es['weight']))


print("Basic metrics:")
print("\n\nMutual network\n")

g = Graph()
g = g.Read_Ncol('g_mutual.ncol')
basic_metrics(g)

print("Non-mutual network\n")

g = Graph()
g = g.Read_Ncol('g_nonmutual.ncol')
basic_metrics(g)
