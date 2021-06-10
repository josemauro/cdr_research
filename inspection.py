import networkx as nx
import matplotlib.pyplot as plt
from itertools import count


days = 3

g = nx.read_gml(f'out/largest_rio_{days}d_mutual.gml', label='id') 

regioes = ['4', '10', '23']
nos_regioes = [x for x,y in g.nodes(data=True) if y['location'] in regioes ] 
subgrafo_regioes = g.subgraph(nos_regioes) 

componente gigante
subgrafo_regioes = max(nx.connected_component_subgraphs(subgrafo_regioes), key=len)
nos_regioes = [x for x,y in subgrafo_regioes.nodes(data=True) if y['location'] in regioes]

# locations = set(nx.get_node_attributes(g,'location').values())
#mapping = dict(zip(sorted(locations), count()))
mapping = {'4': 'green', '10': 'blue', '23': 'red'}

colors = [mapping[ subgrafo_regioes.node[n]['location']] for n in subgrafo_regioes.nodes]

pos = nx.spring_layout(subgrafo_regioes)
# ec = nx.draw_networkx_edges(g, pos, alpha=0.2)

# titulo
plt.title(f'Nós da regiao do RJ considerando {days} dia(s)\nde chamadas telefonicas', fontdict=fontdict, color="black")

#legenda
botafogo = plt.scatter('temp', 'cnt', marker='o', color='green') 
copacabana = plt.scatter('temp', 'cnt', marker='o', color='blue') 
lagoa = plt.scatter('temp', 'cnt', marker='o', color='red')


plt.legend(handles=(botafogo, copacabana, lagoa), 
    labels=('Botafogo', 'Copacabana', 'Lagoa'), 
    title="Regioes", 
    scatterpoints=1, 
    bbox_to_anchor=(1, 0.7), loc=2, borderaxespad=1.0, 
    ncol=1)
nc = nx.draw_networkx(subgrafo_regioes, pos, nodelist=nos_regioes, node_color=colors, with_labels=False, node_size=100, cmap=plt.cm.jet)
    
plt.show()
