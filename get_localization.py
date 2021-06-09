from igraph import Graph

import csv


FILE_LOC_PATH = 'data/user_residence-antenna.csv'

def create_vertex_locations_dict():
    ''' Create a dict containing vertex as key and location as value.'''
    vertex_loc_list = []

    with open(FILE_LOC_PATH, newline='') as csv_file:
        spamreader = csv.reader(csv_file, delimiter=';')
        for row in spamreader:
            vertex_loc_list.append(row)
    vertex_loc_dict = dict(vertex_loc_list)
    return vertex_loc_dict

def add_location_in_network(network, vertex_loc_dict):
    '''Add locations to networks files.'''
    network_name = network.split('.')[0]

    print(f'Getting location to {network_name} component of mutual network...')

    g = Graph()
    file_network = f'./out/{network}'
    g = g.Read_Ncol(file_network, names=True, weights=True, directed=False)

    cont = 0
    vertices_to_delete = []
    for v in g.vs:
        try:
            # The substring '21' is missing for some reason at indentifiers in
            # 'residencia_presumida' file.
            location = vertex_loc_dict[v['name']]
            v['location'] = location
        except KeyError:
            vertices_to_delete.append(v.index)
            #v['location'] = 'None'
            cont = cont + 1

    g.delete_vertices(vertices_to_delete)
    g = g.clusters().giant()
    print(v.index)
    g.write_gml(f'./out/{network_name}.gml')
    print(f'Finished. {str(cont)} nodes without location at {network_name}.')


vertex_loc_dict = create_vertex_locations_dict()

#networks = ['largest_nonmutual.ncol', 'largest_mutual.ncol']
networks = ['largest_32_RISJDR_mutual.ncol',
            'largest_32_RISJDR_nonmutual.ncol']

for network in networks:
    add_location_in_network(network, vertex_loc_dict)


