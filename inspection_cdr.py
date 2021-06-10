"""This script is used to instpect the CDR data."""

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



def main(dir_cdr, file_out):
    """Inspect the CDR
    # calcular a duracao maxima de chamada
    #

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
