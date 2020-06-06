"""This script create a network in './data' folder and save this in ncol."""

import csv
import os
import sys
import time
from os import path
from pathlib import Path
from igraph import Graph


def process_cdr_data(dir_cdr, file_out):
    """Open CDR files and create one ncol file with the data."""
    print('Initializing CDR data processing...')

    files_list = []

    for file_name in os.listdir(dir_cdr):
        files_list.append(file_name)

    ncol_out_file = open(f'./out/g_{file_out}.ncol', 'w')

    for file_name in files_list:
        dir_name = Path(dir_cdr) / file_name
        with open(str(dir_name), 'r') as csvfile:
            csv_read = csv.reader(csvfile, delimiter=';')
            # add nodes
            for row in csv_read:
                line = row[4] + " " + row[6] + " " + row[2] + "\n"
                ncol_out_file.write(line)

    ncol_out_file.close()

    print('Processing finished!')


# In (Onella, 2007) paper there are 2 types of network:
#
#    -Non-mutual: connected 2 users with an undirected link if there had been
#     at least one phone call between. (A called B OR B called A)
#
#    -Mutual: connected 2 users with an undirected link if there had been at
#    least one reciprocated pair of phone calls between them.
#    (A called B AND B called A)
#
# The social network created above (graph.ncol) in this script can be read in
# one of this two formats.


def generate_nonmutual_network(file_out):
    """Read ncol file as non-mutual network."""
    print('\nStarting to generate non-mutual network...')

    g_nonmutual = Graph()
    g_nonmutual = g_nonmutual.Read_Ncol(f'./out/g_{file_out}.ncol', names=True,
                                        weights=True, directed=True)

    # Remove arrows from each edge.
    g_nonmutual.to_undirected(mode='each')

    # Simplifies a graph by removing self-loops and/or multiple edges.
    g_nonmutual = g_nonmutual.simplify(multiple=True, loops=True,
                                       combine_edges='sum')

    vertices_2delete = []

    for vertex in g_nonmutual.vs:
        if vertex.degree() > 150:
            vertices_2delete.append(vertex.index)

    g_nonmutual.delete_vertices(vertices_2delete)

    g_nonmutual.write_ncol(f'./out/g_{file_out}_nonmutual.ncol', names='name',
                           weights='weight')

    largest = g_nonmutual.clusters().giant()

    largest.write_ncol(f'./out/largest_{file_out}_nonmutual.ncol',
                       names='name', weights='weight')
    print('Finished!')


def generate_mutual_network(file_out):
    """Read ncol file as mutual network."""
    print('\nGenerating mutual network...')
    g_mutual = Graph()
    g_mutual = g_mutual.Read_Ncol(f'./out/g_{file_out}.ncol', names=True,
                                  weights=True, directed=True)

    edges_2delete = []

    for edge in g_mutual.es:
        if g_mutual.get_eid(edge.target, edge.source, directed=True,
                            error=False) == -1:
            edges_2delete.append(edge)

    g_mutual.delete_edges(edges_2delete)

    # Remove arrows from each edge.
    g_mutual.to_undirected(mode="each")

    # Simplifies a graph by removing self-loops and/or multiple edges.
    g_mutual = g_mutual.simplify(multiple=True, loops=True,
                                 combine_edges="sum")

    g_mutual.write_ncol(f'./out/g_{file_out}.ncol', names="name",
                        weights="weight")

    largest = g_mutual.clusters().giant()

    largest.write_ncol(f'./out/largest_{file_out}_mutual.ncol', names="name",
                       weights="weight")
    print('Finished!')


# https://igraph.org/python/doc/igraph.GraphBase-class.html

def main(dir_cdr, file_out):
    """Build the networks."""
    start_time = time.time()
    process_cdr_data(dir_cdr, file_out)

    sec = (time.time() - start_time)
    print(f"--- {sec} seconds ---")

    start_time = time.time()
    generate_nonmutual_network(file_out)
    sec = (time.time() - start_time)
    print(f"--- {sec} seconds ---")

    start_time = time.time()
    generate_mutual_network(file_out)
    sec = (time.time() - start_time)
    print("--- {sec} seconds ---")


if __name__ == '__main__':
    try:
        dir_cdr = sys.argv[1]
        file_out = sys.argv[2]
    except IndexError:
        print('\nMissing argument.\n\nExample: python build_networks.py CDR_DI'
              'RECTORY FILE_OUTPUT_NAME\n\n')
        sys.exit(-1)

    if not path.exists(dir_cdr):
        print(f'The directory {dir_cdr} does not exists.')
        sys.exit(-1)
    if not os.listdir(dir_cdr):
        print(f'The directory {dir_cdr} is empty!')
        sys.exit(-1)

    main(dir_cdr, file_out)
