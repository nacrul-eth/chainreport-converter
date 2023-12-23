"""Commmand line module to convert files to chainreport compatible formats"""

import argparse
from chainreport_converter import ChainreportConverter

# Parse Input
parser = argparse.ArgumentParser(description='ChainReport converter command line tool')
parser.add_argument('exchange_type',
                    help='''Name of a supported exchange/blockchain, currently -
                    Name einer unterstützen Exchange/Blockchain, aktuell:
                    - Hi-CSV
                    - Hi-PDF
                    - Plutus-CSV ''')
parser.add_argument('input_file',
                    help='''The exchange/blockchain filename (full path) -
                    Der Name von der Echange/Blockchain Datei (vollständiger Pfad)''')
parser.add_argument('output_file',
                    help='''The ChainReport filename (full path) -
                    Der Name für die ChainReport Datei (vollständiger Pfad)''')
args = parser.parse_args()

# Definitions & variables
exchange_type = args.exchange_type
input_filename = args.input_file
chainreport_filename = args.output_file

executor = ChainreportConverter(exchange_type, input_filename, chainreport_filename)
executor.convert()
