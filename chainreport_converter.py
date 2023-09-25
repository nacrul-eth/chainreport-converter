"""Main Module to parse csv files and create a chainreport compatible version."""

import csv
import argparse
from parser.hi_parser import HiParser

# Parse Input
parser = argparse.ArgumentParser(description='ChainReport converter')
parser.add_argument('exchange_type',
                    help='''Name of a supported exchange/blockchain, currently -
                    Name einer unterstützen Exchange/Blockchain, aktuell:
                    - HI ''')
parser.add_argument('input_file',
                    help='''The exchange/blockchain filename (full path) -
                    Der Name von der Echange/Blockchain Datei (vollständiger Pfad)''')
parser.add_argument('output_file',
                    help='''The ChainReport filename (full path) -
                    Der Name für die ChainReport Datei (vollständiger Pfad)''')
args = parser.parse_args()

# Definitions & variables
exchange_type = args.exchange_type
exchange_filename = args.input_file
chainreport_filename = args.output_file

# Main function
with open (chainreport_filename, 'w', newline='', encoding="utf-8") as csvoutput:
    fieldnames = ['Zeitpunkt', 'Transaktions Typ', 'Anzahl Eingang', 'Währung Eingang',
                  'Anzahl Ausgang', 'Währung Ausgang', 'Transaktionsgebühr',
                  'Währung Transaktionsgebühr', 'Oder-ID der Exchange', 'Beschreibung' ]
    writer = csv.DictWriter(csvoutput, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()

    with open(exchange_filename, newline='', encoding="utf-8") as csvinput:
        reader = csv.DictReader(csvinput, delimiter=',')
        for row in reader:
            if row['Description'] not in HiParser.EXCLUSIONSTRINGS:
                rowdata = HiParser(row)
                writer.writerow({'Zeitpunkt': rowdata.get_date_string(),
                                 'Transaktions Typ': rowdata.get_transaction_type(), 
                                 'Anzahl Eingang': rowdata.get_received_amount(), 
                                 'Währung Eingang': rowdata.get_received_currency(),
                                 'Anzahl Ausgang': rowdata.get_sent_amount(),
                                 'Währung Ausgang': rowdata.get_sent_currency(),
                                 'Transaktionsgebühr': rowdata.get_transaction_fee_amount(),
                                 'Währung Transaktionsgebühr': rowdata.get_transaction_fee_currency(),
                                 'Oder-ID der Exchange': rowdata.get_order_id(),
                                 'Beschreibung': rowdata.get_description()})                
            if row['Description'] in HiParser.WITHDRAWTRANSACTION:
                print({'Zeitpunkt': rowdata.get_date_string(),
                                 'Transaktions Typ': rowdata.get_transaction_type(), 
                                 'Anzahl Eingang': rowdata.get_received_amount(), 
                                 'Währung Eingang': rowdata.get_received_currency(),
                                 'Anzahl Ausgang': rowdata.get_sent_amount(),
                                 'Währung Ausgang': rowdata.get_sent_currency(),
                                 'Transaktionsgebühr': rowdata.get_transaction_fee_amount(),
                                 'Währung Transaktionsgebühr': rowdata.get_transaction_fee_currency(),
                                 'Oder-ID der Exchange': rowdata.get_order_id(),
                                 'Beschreibung': rowdata.get_description()})   

csvinput.close()
csvoutput.close()

print('''----------------------------------------------------------------------
Please modify all Withdrawal lines (see output above) in the file. Hi does not show that at all in their export file. - 
Bitte Prüfe alle Withdrawal Zeilen (siehe Ausgabe oben). Hi zeigt immer einen Wert von 0 an.
----------------------------------------------------------------------''')
