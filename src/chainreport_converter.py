"""Main Module to parse csv files and create a chainreport compatible version."""

import csv
from chainreport_parser.hi_parser import HiParser

class ChainreportConverter():
    """Main Class handling the csv files (open, close) and the conversion of the content"""
    def __init__(self, parsertype, inputfile, outputfile):
        super().__init__()
        self.chainreport_filename = outputfile
        self.input_filename = inputfile
        self.parser_type = parsertype

    def load_parser(self):
        """Setup the correct parser for use"""

    def convert(self, _logging_callback = None):
        """Convert the input file to a compatible chainreport file depending on the parser selection"""
        linecount = 0

        with open (self.chainreport_filename, 'w', newline='', encoding="utf-8") as csvoutput:
            fieldnames = ['Zeitpunkt', 'Transaktions Typ', 'Anzahl Eingang', 'Währung Eingang',
                        'Anzahl Ausgang', 'Währung Ausgang', 'Transaktionsgebühr',
                        'Währung Transaktionsgebühr', 'Oder-ID der Exchange', 'Beschreibung' ]
            writer = csv.DictWriter(csvoutput, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()

            with open(self.input_filename, newline='', encoding="utf-8") as csvinput:
                reader = csv.DictReader(csvinput, delimiter=',')
                for row in reader:
                    linecount = linecount + 1
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
                        if _logging_callback:
                            _logging_callback("Please fix the line " + str(linecount) +
                                              ". The amount is 0 in the export file.")
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

        if self.parser_type == "Hi":
            print('''----------------------------------------------------------------------
            Please modify all Withdrawal lines (see output above) in the file. Hi does not show that at all in their export file. - 
            Bitte Prüfe alle Withdrawal Zeilen (siehe Ausgabe oben). Hi zeigt immer einen Wert von 0 an.
            ----------------------------------------------------------------------''')
