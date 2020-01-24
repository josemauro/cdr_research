from igraph import Graph
from unidecode import unidecode

localizations_file = open('data/residencia_presumida', 'r')
localizations_file = localizations_file.read().split('\n')
list_aux = []
for line in localizations_file:
    list_aux.append(line.split('\t'))

list_aux = list(filter(None, list_aux))
list_aux.pop(2593911)

localizations = dict(list_aux)

print('Getting localization to largest component of mutual network...')
g = Graph()
g = g.Read_Ncol('./out/largest_mutual.ncol', names=True, weights=True, directed=False)

cont = 0
for v in g.vs:
    try:
        v['localization'] = localizations['21'+v['name']]
    except:
        v['localization'] = 'None'
        cont = cont + 1

g.write_gml('./out/largest_mutual.gml')
print('Finished... '+str(cont)+' nodes without localization at mutual network.')


print('\n\nGetting localization to largest component of non-mutual network...')
g = Graph()
g = g.Read_Ncol('./out/largest_nonmutual.ncol', names=True, weights=True, directed=False)

cont = 0
for v in g.vs:
    try:
        v['localization'] = localizations['21'+v['name']]
    except:
        v['localization'] = 'None'
        cont = cont + 1

g.write_gml('./out/largest_nonmutual.gml')
print('Finished... '+str(cont)+' nodes without localization at mutual network.')

