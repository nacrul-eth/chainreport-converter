"""Main Module to parse csv files and create a chainreport compatible version."""

import csv
from chainreport_parser.hi_parser import HiParser
from chainreport_parser.plutus_parser import PlutusParser

class ChainreportConverter():
    """Main Class handling the csv files (open, close) and the conversion of the content"""
    def __init__(self, parsertype, inputfile, outputfile):
        super().__init__()
        self.statistics = {
            "input_linecount": 0,
            "output_linecount": 0, 
            "warnings": 0,
            "errors": 0,
            "ignored": 0
        }
        self.chainreport_filename = outputfile
        self.input_filename = inputfile
        self.parser_type = parsertype
        if parsertype == "Hi":
            self.parser = HiParser
        elif parsertype == "Plutus":
            self.parser = PlutusParser
        else:
            return

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
        self.statistics["output_linecount"] += 1

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
                reader = csv.DictReader(csvinput, delimiter=self.parser.DELIMITER)
                skip_next_line = False
                next_row = next(reader)

                for row in reader:
                    self.statistics["input_linecount"] += 1
                    # Populate required parameters
                    current_row, next_row = next_row, row
                    # Skip this line as well (didnt figure out skipping 2 lines yet)
                    if skip_next_line:
                        skip_next_line = False
                        continue
                    current_rowdata = self.parser(current_row)
                    next_rowdata = self.parser(next_row)

                    # Combine the multiline trade transaction (if there is still a next line left)
                    if current_rowdata.get_description() in self.parser.TRADETRANSACTION and self.parser == HiParser:
                        self.handle_trade_transactions(writer, current_rowdata, next_rowdata)
                        skip_next_line = True
                        continue

                    # Handle canceled withdrawactions
                    if current_rowdata.get_description() in self.parser.WITHDRAWTRANSACTION:
                        # Check for cancel of the transaction first
                        if next_rowdata.get_description() in self.parser.CANCELTRANSACTION:
                            # If the Withdraw was canceled, skip both lines
                            skip_next_line = True
                            continue
                        if _logging_callback:
                            _logging_callback("Please fix the line " + str(self.statistics["output_linecount"]) +
                                              ". The amount is 0 in the export file.")
                        self.statistics["warnings"] += 1

                    # If you ended up here, write data into the file
                    if current_rowdata.get_description() not in (self.parser.EXCLUSIONSTRINGS or
                                                                 self.parser.CANCELTRANSACTION):
                        self.write_row(writer, current_rowdata)
                        if current_rowdata.get_transaction_type() == 'ERROR':
                            self.statistics["errors"] += 1
                            if _logging_callback:
                                _logging_callback("Please report line " + str(self.statistics["output_linecount"]) +
                                                  "\n" + str(current_row) + "\nThis has to be fixed.")

        csvinput.close()
        csvoutput.close()

        if _logging_callback:
            _logging_callback("""
            ----------------------------------------------------------------------
            Read lines: """ + str(self.statistics["input_linecount"]) + """
            Written lines: """ + str(self.statistics["output_linecount"]) + """
            Number of Warnings: """ + str(self.statistics["warnings"]) + """ - Please check above
            Number of Errors: """ + str(self.statistics["errors"]) + """ - Please report them
            Please check details here: 
            https://github.com/nacrul-eth/chainreport-converter/wiki/HiParser/""" + self.parser.NAME + """
            ----------------------------------------------------------------------""")

    def handle_trade_transactions(self, writer, current_rowdata, next_rowdata):
        """Special handling for 2 line trade transactions"""
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
        self.statistics["output_linecount"] += 1
