# in (Onella, 2007) paper. The first network have an edge between
# two nodes if there is at least one call between them
# (A called B OR B called A). The second network have and edge
# between two nodes if and only if both of them called to each
# other (A called B AND B called A).

import csv
from igraph import Graph
import os

files_list = []

for file_name in os.listdir("./data"):
    if file_name.endswith("*.out"):
        files_list.append(file_name)

g1 = Graph()

ncol_out_file = open("graph.ncol","w")

for file_name in files_list:
    with open(file_name, 'r') as csvfile:
        csv_read = csv.reader(csvfile, delimiter=';')
        #add nodes
        name_list = []
        for row in csv_read:
            line = row[4] + " " + row[6] + " " + row[2] + "\n" 
            ncol_out_file.write(line)

