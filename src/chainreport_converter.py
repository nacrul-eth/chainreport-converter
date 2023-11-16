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

    DATESTRING_CR = 'Zeitpunkt'
    TRANSACTIONTYP_CR = 'Transaktions Typ'
    RECEIVED_AMOUNT_CR = 'Anzahl Eingang'
    RECEIVED_CURRENCY_CR = 'Währung Eingang'
    SENT_AMOUNT_CR = 'Anzahl Ausgang'
    SENT_CURRENCY_CR = 'Währung Ausgang'
    TRANS_FEE_AMOUNT_CR = 'Transaktionsgebühr'
    TRANS_FEE_CURRENCY_CR = 'Währung Transaktionsgebühr'
    ORDERID_CR = 'Oder-ID der Exchange'
    DESCRIPTION_CR = 'Beschreibung'

    def load_parser(self):
        """Setup the correct parser for use"""

    def write_row(self, csv_writer, row):
        """Write the row into the csv file"""
        csv_writer.writerow({self.DATESTRING_CR: row.get_date_string(),
                             self.TRANSACTIONTYP_CR: row.get_transaction_type(),
                             self.RECEIVED_AMOUNT_CR: row.get_received_amount(),
                             self.RECEIVED_CURRENCY_CR: row.get_received_currency(),
                             self.SENT_AMOUNT_CR: row.get_sent_amount(),
                             self.SENT_CURRENCY_CR: row.get_sent_currency(),
                             self.TRANS_FEE_AMOUNT_CR: row.get_transaction_fee_amount(),
                             self.TRANS_FEE_CURRENCY_CR: row.get_transaction_fee_currency(),
                             self.ORDERID_CR: row.get_order_id(),
                             self.DESCRIPTION_CR: row.get_description()})

    def convert(self, _logging_callback = None):
        """Convert the input file to a compatible chainreport file depending on the parser selection"""

        with open (self.chainreport_filename, 'w', newline='', encoding="utf-8") as csvoutput:
            fieldnames = [self.DATESTRING_CR, self.TRANSACTIONTYP_CR,
                          self.RECEIVED_AMOUNT_CR, self.RECEIVED_CURRENCY_CR,
                          self.SENT_AMOUNT_CR, self.SENT_CURRENCY_CR,
                          self.TRANS_FEE_AMOUNT_CR, self.TRANS_FEE_CURRENCY_CR,
                          self.ORDERID_CR, self.DESCRIPTION_CR ]
            writer = csv.DictWriter(csvoutput, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()

            with open(self.input_filename, newline='', encoding="utf-8") as csvinput:
                reader = csv.DictReader(csvinput, delimiter=',')
                linecount = 0
                next_row = next(reader)

                for row in reader:
                    del row
                    # populate required parameters
                    linecount = linecount + 1
                    current_row, next_row = next_row, next(reader)
                    current_rowdata = HiParser(current_row)
                    next_rowdata = HiParser(next_row)

                    # Combine the multiline trade transaction (if there is still a next line left)
                    if current_rowdata.get_description() in HiParser.TRADETRANSACTION and next_row:
                        receive_amount = ""
                        receive_currency = ""
                        sent_amount = ""
                        sent_currency = ""

                        if current_rowdata.get_received_amount():
                            receive_amount = current_rowdata.get_received_amount()
                            receive_currency = current_rowdata.get_received_currency()
                            sent_amount = next_rowdata.get_sent_amount()
                            sent_currency = next_rowdata.get_sent_currency()
                        else:
                            receive_amount = next_rowdata.get_received_amount()
                            receive_currency = next_rowdata.get_received_currency()
                            sent_amount = current_rowdata.get_sent_amount()
                            sent_currency = current_rowdata.get_sent_currency()

                        writer.writerow({self.DATESTRING_CR: current_rowdata.get_date_string(),
                                         self.TRANSACTIONTYP_CR: current_rowdata.get_transaction_type(),
                                         self.RECEIVED_AMOUNT_CR: receive_amount,
                                         self.RECEIVED_CURRENCY_CR: receive_currency,
                                         self.SENT_AMOUNT_CR: sent_amount,
                                         self.SENT_CURRENCY_CR: sent_currency,
                                         self.TRANS_FEE_AMOUNT_CR: current_rowdata.get_transaction_fee_amount(),
                                         self.TRANS_FEE_CURRENCY_CR: current_rowdata.get_transaction_fee_currency(),
                                         self.ORDERID_CR: current_rowdata.get_order_id(),
                                         self.DESCRIPTION_CR: current_rowdata.get_description()})

                    # Handle canceled withdrawactions
                    elif current_rowdata.get_description() in HiParser.WITHDRAWTRANSACTION and next_row:
                        # Check for cancel of the transaction first
                        if next_rowdata.get_description() in HiParser.CANCELTRANSACTION:
                            # If the Withdraw was canceled, skip both lines
                            next(reader)
                            continue
                        if _logging_callback:
                            _logging_callback("Please fix the line " + str(linecount) +
                                              ". The amount is 0 in the export file.")

                    # If you ended up here, write data into the file
                    if current_rowdata.get_description() not in HiParser.EXCLUSIONSTRINGS:
                        self.write_row(writer, current_rowdata)

        csvinput.close()
        csvoutput.close()

        if self.parser_type == "Hi" and _logging_callback:
            _logging_callback('''
            ----------------------------------------------------------------------
            Please modify all Withdrawal lines (see output above) in the file. Hi does not show that at all in their export file. - 
            Bitte Prüfe alle Withdrawal Zeilen (siehe Ausgabe oben). Hi zeigt immer einen Wert von 0 an.
            ----------------------------------------------------------------------''')
