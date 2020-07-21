from igraph import Graph
from unidecode import unidecode

import csv


FILE_LOC_PATH = 'data/residencia_presumida'

def generate_id_locations():
    ''' Create an id for each location.'''
    locations = []

    with open(FILE_LOC_PATH, newline='') as csv_file:
        spamreader = csv.reader(csv_file, delimiter='\t')
        for row in spamreader:
            row = ' '.join(row[1:])
            locations.append(row)

    locations = list(set(locations))
    locations.sort()

    #print(locations)

    index = list(range(0,len(locations)))

    #id_location_dict = dict(zip(index, locations))
    location_id_dict = dict(zip(locations, index))


    return location_id_dict

def write_file_mapping_id_locations(location_id_dict):
    '''Create a file named containing id and location in each line.'''
    file_map_path = 'data/residencia_presumida_mapping.csv'

    with open(file_map_path, 'w') as file_write:
        for location, index in location_id_dict.items():
            file_write.write(str(index) +',' + location + '\n')

def create_vertex_locations_dict():
    ''' Create a dict containing vertex as key and location as value..'''
    vertex_loc_list = []

    with open(FILE_LOC_PATH, newline='') as csv_file:
        spamreader = csv.reader(csv_file, delimiter='\t')
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
            location = vertex_loc_dict['21' + v['name']]
            v['location'] = str(location_id_dict[ location ])
        except KeyError:
            vertices_to_delete.append(v.index)
            #v['location'] = 'None'
            cont = cont + 1

    g.delete_vertices(vertices_to_delete)
    print(v.index)
    g.write_gml(f'./out/{network_name}.gml')
    print(f'Finished. {str(cont)} nodes without location at {network_name}.')


location_id_dict = generate_id_locations()

write_file_mapping_id_locations(location_id_dict)

vertex_loc_dict = create_vertex_locations_dict()

#networks = ['largest_nonmutual.ncol', 'largest_mutual.ncol']
networks = ['largest_rio_1d_nonmutual.ncol']

for network in networks:
    add_location_in_network(network, vertex_loc_dict)


