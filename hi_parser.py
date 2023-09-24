"""Main Module to parse csv files and create a chainreport compatible version."""

import csv
import argparse
from datetime import datetime

# Parse Input
parser = argparse.ArgumentParser(description='Hi to ChainReport converter')
parser.add_argument('input_file',
                    help='''The Hi statement filename (full path) -
                    Der Name für die Hi Statement Datei (vollständiger Pfad)''')
parser.add_argument('output_file',
                    help='''The ChainReport filename (full path) -
                    Der Name für die ChainReport Datei (vollständiger Pfad)''')
args = parser.parse_args()

# Definitions & variables
hi_statement_filename = args.input_file
hi_chainreport_filename = args.output_file

CASHBACKTRANSACTION = ['HI rebate']
DEPOSITTRANSACTION = ['Crypto deposit',
                      'crypto receive']
STAKINGTRANSACTION = ['Crypto staking yields （HI）']
WITHDRAWTRANSACTION = ['crypto send',
                       'Crypto withdraw']
EXCLUSIONSTRINGS = ['Vault HI daily release',
                   'Crypto earning stake',
                   'Crypto earning release']

def get_date_string(date):
    """Function converting the date into the correct format."""
    transaction_time = datetime.strptime(date, '%Y-%m-%d %H:%M %Z')
    return transaction_time.strftime('%d.%m.%Y %H:%M')

def get_transactiontype_string(transaction_description):
    """Function converting the transaction type to the correct string."""
    if transaction_description in CASHBACKTRANSACTION:
        return 'Cashback'
    if transaction_description in STAKINGTRANSACTION:
        return 'Staking'
    if transaction_description in DEPOSITTRANSACTION:
        return 'Deposit'
    if transaction_description in WITHDRAWTRANSACTION:
        return 'Withdrawal'
    return 'ERROR'

def convert_numbers(amount):
    """Function converting deciaml numbers."""
    return amount.replace(".", ",")


with open (hi_chainreport_filename, 'w', newline='', encoding="utf-8") as csvoutput:
    fieldnames = ['Zeitpunkt', 'Transaktions Typ', 'Anzahl Eingang', 'Währung Eingang',
                  'Anzahl Ausgang', 'Währung Ausgang', 'Transaktionsgebühr',
                  'Währung Transaktionsgebühr', 'Oder-ID der Exchange', 'Beschreibung' ]
    writer = csv.DictWriter(csvoutput, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()

    with open(hi_statement_filename, newline='', encoding="utf-8") as csvinput:
        reader = csv.DictReader(csvinput, delimiter=',')
        for row in reader:
            if row['Description'] not in EXCLUSIONSTRINGS:
                writer.writerow({'Zeitpunkt': get_date_string(row['Date']),
                                 'Transaktions Typ': get_transactiontype_string(row['Description']), 
                                 'Anzahl Eingang': convert_numbers(row['Received Amount']), 
                                 'Währung Eingang': row['Received Currency'],
                                 'Währung Ausgang': row['Sent Currency'],
                                 'Anzahl Ausgang': convert_numbers(row['Sent Amount']),
                                 'Beschreibung': row['Description']})

csvinput.close()
csvoutput.close()

print('''----------------------------------------------------------------------
Please modify all Withdrawal lines in the file. Hi does not show that at all in their export file. - 
Bitte Prüfe alle Withdrawal Zeilen. Hi zeigt immer einen Wert von 0 an.
----------------------------------------------------------------------''')
