from igraph import Graph

g = Graph(3, directed=True)


g.add_edges([(0,1),(1,0),(2,1),(0,2)])

for i in g.vs:
    print i.index

print("\n\n")

for i in g.es:
    print i.source, i.target
    
g.to_undirected(mode="mutual")

print("\n\nNao direcionada")

for i in g.es:
    print i.source, i.target

